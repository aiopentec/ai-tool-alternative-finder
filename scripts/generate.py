#!/usr/bin/env python3
"""
generate.py — AI Tool Alternative Finder
Reads data/tool_pairs.json, generates comparison content via AI APIs,
writes rich JSON to .cache/comparisons/{slug}.json

API strategy (mirrors OSALFinder pipeline):
  1. Try Groq (Llama 3.3-70b) — fast and free
  2. If Groq rate-limits beyond cap or fails → fall back to Gemini Flash
  3. If both fail → log error, skip pair, continue with next

This means the pipeline never hangs waiting 3000 seconds for Groq to reset.

Usage:
    python scripts/generate.py                  # generate only new/missing
    python scripts/generate.py --force          # regenerate everything
    python scripts/generate.py --slug chatgpt-plus-vs-openrouter
    python scripts/generate.py --dry-run        # validate setup only
    python scripts/generate.py --limit 5        # first N pairs only

Environment (at least one required):
    GROQ_API_KEY      — console.groq.com (starts with gsk_)
    GEMINI_API_KEY    — aistudio.google.com (or GOOGLE_API_KEY)
"""

import argparse
import json
import logging
import os
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# LOGGING
# ─────────────────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.DEBUG if os.getenv("GENERATE_DEBUG") else logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    stream=sys.stdout,
    force=True,
)
log = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────────────────────

GROQ_API_KEY   = os.getenv("GROQ_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "") or os.getenv("GOOGLE_API_KEY", "")

PAIRS_FILE     = Path("data/tool_pairs.json")
CACHE_DIR      = Path(".cache/comparisons")

MAX_RETRIES    = 2
RETRY_DELAY    = 8
API_TIMEOUT    = 90
INTER_DELAY    = 5          # seconds between calls
RATE_LIMIT_CAP = 60         # if Groq wants to wait longer than this -> use Gemini

GROQ_MODEL   = "llama-3.3-70b-versatile"
GEMINI_MODEL = "gemini-1.5-flash"

# ─────────────────────────────────────────────────────────────────────────────
# PROMPT
# ─────────────────────────────────────────────────────────────────────────────

PROMPT = """You are a technical writer creating a structured comparison between a paid AI tool and a free alternative.

Generate a complete, accurate comparison between {paid_tool} and {free_tool}.

Return ONLY a valid JSON object - no markdown fences, no preamble, no explanation.

The JSON must have EXACTLY this structure:

{{
  "slug": "{slug}",
  "category": "{category}",
  "category_emoji": "{category_emoji}",
  "paid_tool": "{paid_tool}",
  "paid_price": "{paid_price}",
  "paid_url": "{paid_url}",
  "free_tool": "{free_tool}",
  "free_price": "{free_price}",
  "free_url": "{free_url}",
  "github_repo": {github_repo_json},
  "savings": "[concise savings summary e.g. $20/month to Free]",
  "verdict_switch": "[2-3 sentences on when to switch to the free tool]",
  "verdict_stay": "[2-3 sentences on when to stay with the paid tool]",
  "setup_difficulty": "[Easy or Medium or Hard]",
  "setup_dots": "[5 dots: for Easy use 2 filled, Medium use 3 filled, Hard use 4 filled]",
  "setup_time": "[e.g. 5 mins or 30 mins]",
  "setup_method": "[e.g. Browser-based or Docker or pip install]",
  "overview": "[3-4 sentence paragraph comparing both tools accurately]",
  "key_differences": [
    "Cost: [comparison]",
    "Features: [comparison]",
    "Privacy: [comparison]",
    "Setup: [comparison]",
    "Quality: [comparison]"
  ],
  "pricing_table": {{
    "headers": ["Aspect", "{paid_tool}", "{free_tool}"],
    "rows": [
      ["Base pricing", "[paid price]", "[free price]"],
      ["[aspect 2]", "[paid]", "[free]"],
      ["[aspect 3]", "[paid]", "[free]"],
      ["[aspect 4]", "[paid]", "[free]"],
      ["[aspect 5]", "[paid]", "[free]"]
    ]
  }},
  "migration": "[Practical numbered steps to switch from {paid_tool} to {free_tool}. Include real commands and URLs.]",
  "related": []
}}

Rules:
- All content must be factually accurate as of 2025
- setup_dots must be exactly 5 characters using filled circle and empty circle
- pricing_table headers must be exactly: Aspect, {paid_tool}, {free_tool}
- migration must have practical specific steps with real commands
- related must be an empty array
- Return ONLY the JSON object, nothing else"""


# ─────────────────────────────────────────────────────────────────────────────
# PRE-FLIGHT
# ─────────────────────────────────────────────────────────────────────────────

def preflight():
    errors = []

    if not GROQ_API_KEY and not GEMINI_API_KEY:
        errors.append(
            "No API keys set. Need at least one:\n"
            "  GROQ_API_KEY:   console.groq.com -> API Keys\n"
            "  GEMINI_API_KEY: aistudio.google.com -> Get API Key\n"
            "  Add to: Repo -> Settings -> Secrets -> Actions -> New repository secret"
        )
    else:
        if GROQ_API_KEY:
            if not GROQ_API_KEY.startswith("gsk_"):
                errors.append(f"GROQ_API_KEY looks invalid (expected gsk_ prefix, got {GROQ_API_KEY[:8]}...)")
            else:
                log.info("GROQ_API_KEY set (prefix: %s...)", GROQ_API_KEY[:8])
        else:
            log.info("GROQ_API_KEY not set - will use Gemini only")

        if GEMINI_API_KEY:
            log.info("GEMINI_API_KEY set (prefix: %s...)", GEMINI_API_KEY[:8])
        else:
            log.info("GEMINI_API_KEY not set - Groq only, no fallback")

    if not PAIRS_FILE.exists():
        errors.append(f"Tool pairs file not found: {PAIRS_FILE}")
    else:
        with open(PAIRS_FILE) as f:
            pairs = json.load(f)
        log.info("Tool pairs file: %d pairs loaded", len(pairs))

    try:
        import requests
        log.info("requests package available")
    except ImportError:
        errors.append("requests not installed. Run: pip install requests")

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    log.info("Cache dir ready: %s", CACHE_DIR)

    if errors:
        log.error("PRE-FLIGHT FAILED:")
        for i, e in enumerate(errors, 1):
            log.error("  %d. %s", i, e)
        sys.exit(1)

    log.info("All pre-flight checks passed\n")


# ─────────────────────────────────────────────────────────────────────────────
# API CONNECTIVITY TESTS
# ─────────────────────────────────────────────────────────────────────────────

def test_groq():
    import requests
    log.info("Testing Groq API...")
    try:
        resp = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
            json={"model": GROQ_MODEL, "messages": [{"role": "user", "content": "Say OK"}], "max_tokens": 5},
            timeout=20,
        )
        if resp.status_code == 401:
            log.error("Groq 401 - key invalid or revoked. Get a new key at console.groq.com")
            return False
        if resp.status_code == 429:
            log.warning("Groq 429 at startup - already rate limited. Will use Gemini as primary.")
            return False
        if not resp.ok:
            log.warning("Groq returned %d - will fall back to Gemini", resp.status_code)
            return False
        log.info("Groq API OK - %s", GROQ_MODEL)
        return True
    except Exception as e:
        log.warning("Groq connectivity error: %s - will fall back to Gemini", e)
        return False


def test_gemini():
    import requests
    log.info("Testing Gemini API...")
    try:
        resp = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}",
            json={"contents": [{"parts": [{"text": "Say OK"}]}]},
            timeout=20,
        )
        if resp.status_code == 403:
            log.error("Gemini 403 - key invalid. Get a new key at aistudio.google.com")
            return False
        if resp.status_code == 429:
            log.warning("Gemini 429 at startup - already rate limited.")
            return False
        if not resp.ok:
            log.warning("Gemini returned %d", resp.status_code)
            return False
        log.info("Gemini API OK - %s", GEMINI_MODEL)
        return True
    except Exception as e:
        log.warning("Gemini connectivity error: %s", e)
        return False


def test_apis():
    groq_ok   = test_groq()   if GROQ_API_KEY   else False
    gemini_ok = test_gemini() if GEMINI_API_KEY else False

    if not groq_ok and not gemini_ok:
        log.error("FATAL: Both Groq and Gemini API tests failed.")
        log.error("Check your API keys in GitHub Secrets.")
        sys.exit(1)

    log.info("")
    return groq_ok, gemini_ok


# ─────────────────────────────────────────────────────────────────────────────
# GROQ API CALL
# ─────────────────────────────────────────────────────────────────────────────

class RateLimitExceeded(Exception):
    pass


def call_groq(prompt):
    import requests

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
                json={
                    "model": GROQ_MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 3000,
                    "temperature": 0.2,
                },
                timeout=API_TIMEOUT,
            )

            if resp.status_code == 429:
                wait = int(resp.headers.get("retry-after", RETRY_DELAY * attempt))
                if wait > RATE_LIMIT_CAP:
                    raise RateLimitExceeded(
                        f"Groq wants to wait {wait}s (cap={RATE_LIMIT_CAP}s). Switching to Gemini."
                    )
                log.warning("Groq rate limited. Waiting %ds (attempt %d/%d)...", wait, attempt, MAX_RETRIES)
                time.sleep(wait)
                continue

            if resp.status_code == 503:
                if attempt < MAX_RETRIES:
                    log.warning("Groq 503. Waiting %ds...", RETRY_DELAY * attempt)
                    time.sleep(RETRY_DELAY * attempt)
                    continue
                raise RuntimeError("Groq 503 after retries")

            if resp.status_code == 401:
                raise RuntimeError("Groq 401 - key invalid or revoked")

            if not resp.ok:
                raise RuntimeError(f"Groq HTTP {resp.status_code}: {resp.text[:200]}")

            return resp.json()["choices"][0]["message"]["content"]

        except RateLimitExceeded:
            raise
        except RuntimeError:
            raise
        except Exception as e:
            if attempt < MAX_RETRIES:
                log.warning("Groq network error attempt %d: %s. Retrying...", attempt, e)
                time.sleep(RETRY_DELAY)
                continue
            raise RuntimeError(f"Groq network error: {e}") from e

    raise RuntimeError(f"Groq failed after {MAX_RETRIES} attempts")


# ─────────────────────────────────────────────────────────────────────────────
# GEMINI API CALL
# ─────────────────────────────────────────────────────────────────────────────

def call_gemini(prompt):
    import requests

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    )

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.post(
                url,
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"maxOutputTokens": 3000, "temperature": 0.2},
                },
                timeout=API_TIMEOUT,
            )

            if resp.status_code == 429:
                wait = RETRY_DELAY * attempt
                if attempt < MAX_RETRIES:
                    log.warning("Gemini rate limited. Waiting %ds...", wait)
                    time.sleep(wait)
                    continue
                raise RuntimeError("Gemini rate limited after all retries")

            if resp.status_code == 403:
                raise RuntimeError("Gemini 403 - key invalid or lacks permissions")

            if not resp.ok:
                raise RuntimeError(f"Gemini HTTP {resp.status_code}: {resp.text[:200]}")

            data = resp.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]

        except RuntimeError:
            raise
        except Exception as e:
            if attempt < MAX_RETRIES:
                log.warning("Gemini network error attempt %d: %s. Retrying...", attempt, e)
                time.sleep(RETRY_DELAY)
                continue
            raise RuntimeError(f"Gemini network error: {e}") from e

    raise RuntimeError(f"Gemini failed after {MAX_RETRIES} attempts")


# ─────────────────────────────────────────────────────────────────────────────
# SMART API ROUTER — Groq first, Gemini fallback
# ─────────────────────────────────────────────────────────────────────────────

def call_api(prompt):
    """Try Groq first. On rate limit or failure, immediately try Gemini."""

    if GROQ_API_KEY:
        try:
            content = call_groq(prompt)
            return content, "groq"
        except RateLimitExceeded as e:
            log.warning("Groq rate limit exceeded cap -> switching to Gemini. (%s)", e)
        except RuntimeError as e:
            log.warning("Groq failed -> trying Gemini. Error: %s", e)

    if GEMINI_API_KEY:
        try:
            content = call_gemini(prompt)
            return content, "gemini"
        except RuntimeError as e:
            raise RuntimeError(f"Both APIs failed. Last Gemini error: {e}")

    raise RuntimeError(
        "No working API. GROQ_API_KEY failed and GEMINI_API_KEY is not set."
    )


# ─────────────────────────────────────────────────────────────────────────────
# PARSE + VALIDATE RESPONSE
# ─────────────────────────────────────────────────────────────────────────────

def parse_response(raw, slug, paid_tool, free_tool):
    raw = raw.strip()
    if raw.startswith("```"):
        lines = raw.split("\n")
        raw = "\n".join(lines[1:])
    if raw.endswith("```"):
        raw = raw.rsplit("```", 1)[0]
    raw = raw.strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise RuntimeError(
            f"Invalid JSON for {slug}. Error: {e}\nRaw (first 500):\n{raw[:500]}"
        )

    required = ["slug", "paid_tool", "free_tool", "savings",
                "verdict_switch", "verdict_stay", "overview",
                "key_differences", "migration"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        raise RuntimeError(f"Missing required fields for {slug}: {missing}")

    data["slug"] = slug
    data["generated_at"] = datetime.now(timezone.utc).isoformat()
    return data


# ─────────────────────────────────────────────────────────────────────────────
# GENERATE ONE COMPARISON
# ─────────────────────────────────────────────────────────────────────────────

def generate(pair):
    slug   = pair["slug"]
    github = pair.get("github_repo")

    prompt = PROMPT.format(
        slug             = slug,
        category         = pair["category"],
        category_emoji   = pair["category_emoji"],
        paid_tool        = pair["paid_tool"],
        paid_price       = pair["paid_price"],
        paid_url         = pair["paid_url"],
        free_tool        = pair["free_tool"],
        free_price       = pair["free_price"],
        free_url         = pair["free_url"],
        github_repo_json = f'"{github}"' if github else "null",
    )

    raw, api_used = call_api(prompt)
    data = parse_response(raw, slug, pair["paid_tool"], pair["free_tool"])
    return data, api_used


# ─────────────────────────────────────────────────────────────────────────────
# RELATED LINKS
# ─────────────────────────────────────────────────────────────────────────────

def populate_related(all_data):
    for item in all_data:
        related = []
        for other in all_data:
            if other["slug"] == item["slug"]:
                continue
            if (other.get("paid_tool") == item.get("paid_tool") or
                    other.get("free_tool") == item.get("free_tool") or
                    other.get("paid_tool") == item.get("free_tool")):
                related.append(other["slug"])
            if len(related) >= 3:
                break
        item["related"] = related
    return all_data


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--force",   action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--slug",    type=str, default="")
    parser.add_argument("--limit",   type=int, default=0)
    args = parser.parse_args()

    log.info("=" * 60)
    log.info("AI Tool Alternative Finder - Generate")
    log.info("Primary:  Groq (%s)", GROQ_MODEL)
    log.info("Fallback: Gemini (%s)", GEMINI_MODEL)
    log.info("Rate limit cap: %ds then switch to Gemini", RATE_LIMIT_CAP)
    log.info("Inter-call delay: %ds", INTER_DELAY)
    log.info("=" * 60)

    preflight()

    if not args.dry_run:
        groq_ok, gemini_ok = test_apis()
        log.info("Groq: %s | Gemini: %s\n",
                 "OK" if groq_ok else "FAIL",
                 "OK" if gemini_ok else ("FAIL" if GEMINI_API_KEY else "not configured"))

    with open(PAIRS_FILE) as f:
        pairs = json.load(f)

    if args.slug:
        pairs = [p for p in pairs if p["slug"] == args.slug]
        if not pairs:
            log.error("No pair with slug: %s", args.slug)
            sys.exit(1)

    if args.limit:
        pairs = pairs[:args.limit]

    to_generate = []
    skipped     = []
    for pair in pairs:
        if (CACHE_DIR / f"{pair['slug']}.json").exists() and not args.force:
            skipped.append(pair["slug"])
        else:
            to_generate.append(pair)

    log.info("Total: %d | Cached (skip): %d | To generate: %d",
             len(pairs), len(skipped), len(to_generate))

    if args.dry_run:
        log.info("\nDry run complete. Would generate: %s", [p["slug"] for p in to_generate])
        return

    if not to_generate:
        log.info("\nAll comparisons cached. Use --force to regenerate.")
        return

    # ── GENERATION LOOP ──────────────────────────────────────────────────────

    succeeded  = []
    failed     = []
    api_counts = {"groq": 0, "gemini": 0}

    for i, pair in enumerate(to_generate, 1):
        log.info("\n[%d/%d] %s vs %s", i, len(to_generate), pair["paid_tool"], pair["free_tool"])

        try:
            data, api_used = generate(pair)
            cache_file = CACHE_DIR / f"{pair['slug']}.json"
            cache_file.write_text(json.dumps(data, indent=2, ensure_ascii=False))
            api_counts[api_used] += 1
            succeeded.append(pair["slug"])
            log.info("  Saved via %s -> %s", api_used.upper(), cache_file.name)

            if i < len(to_generate):
                delay = INTER_DELAY if api_used == "groq" else INTER_DELAY * 2
                time.sleep(delay)

        except Exception as e:
            log.error("  FAILED: %s - %s", pair["slug"], str(e)[:200])
            if os.getenv("GENERATE_DEBUG"):
                log.debug(traceback.format_exc())
            failed.append({"slug": pair["slug"], "error": str(e)})

    # ── RELATED LINKS ─────────────────────────────────────────────────────────

    log.info("\nUpdating related links...")
    all_cached = []
    for f in sorted(CACHE_DIR.glob("*.json")):
        try:
            all_cached.append(json.loads(f.read_text()))
        except Exception:
            pass

    all_cached = populate_related(all_cached)
    for item in all_cached:
        (CACHE_DIR / f"{item['slug']}.json").write_text(
            json.dumps(item, indent=2, ensure_ascii=False)
        )

    # ── SUMMARY ───────────────────────────────────────────────────────────────

    total_cached = len(list(CACHE_DIR.glob("*.json")))
    log.info("\n" + "=" * 60)
    log.info("DONE: Succeeded=%d (Groq=%d Gemini=%d) | Failed=%d | Skipped=%d | Total cached=%d",
             len(succeeded), api_counts["groq"], api_counts["gemini"],
             len(failed), len(skipped), total_cached)

    if failed:
        log.warning("Failed slugs:")
        for f in failed:
            log.warning("  - %s: %s", f["slug"], f["error"][:100])

    if to_generate and not succeeded:
        log.error("FATAL: Zero comparisons generated. Check your API keys.")
        sys.exit(1)

    log.info("Run 'python scripts/build.py' to rebuild the site.")


if __name__ == "__main__":
    main()
