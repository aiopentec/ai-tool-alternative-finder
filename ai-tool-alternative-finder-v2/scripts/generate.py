#!/usr/bin/env python3
"""
generate.py — AI Tool Alternative Finder
Reads data/tool_pairs.json, calls Groq API for each pair,
writes rich comparison JSON to .cache/comparisons/{slug}.json

Usage:
    python scripts/generate.py                  # generate only new/missing
    python scripts/generate.py --force          # regenerate everything
    python scripts/generate.py --slug chatgpt-plus-vs-openrouter   # one pair
    python scripts/generate.py --dry-run        # validate setup, no API calls
    python scripts/generate.py --limit 5        # generate first N pairs only

Environment:
    GROQ_API_KEY   required
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

GROQ_API_KEY  = os.getenv("GROQ_API_KEY", "")
PAIRS_FILE    = Path("data/tool_pairs.json")
CACHE_DIR     = Path(".cache/comparisons")
MAX_RETRIES   = 3
RETRY_DELAY   = 8      # seconds between retries
API_TIMEOUT   = 90     # seconds per request
INTER_DELAY   = 2      # seconds between successful calls (rate limit buffer)
GROQ_MODEL    = "llama-3.3-70b-versatile"

# ─────────────────────────────────────────────────────────────────────────────
# PROMPT
# ─────────────────────────────────────────────────────────────────────────────

PROMPT = """You are a technical writer creating a structured comparison between a paid AI tool and a free alternative.

Generate a complete, accurate comparison between {paid_tool} and {free_tool}.

Return ONLY a valid JSON object — no markdown fences, no preamble, no explanation.

The JSON must have EXACTLY this structure (fill every field with real, accurate information):

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
  "savings": "[concise savings summary e.g. '$20/month → Free tier available']",
  "verdict_switch": "[2-3 sentences: when you should switch to the free tool]",
  "verdict_stay": "[2-3 sentences: when you should stay with the paid tool]",
  "setup_difficulty": "[one of: Easy / Medium / Hard]",
  "setup_dots": "[difficulty as 5 dots e.g. '●●○○○' for Easy, '●●●○○' for Medium, '●●●●○' for Hard]",
  "setup_time": "[realistic setup time e.g. '~5 mins' or '~30 mins']",
  "setup_method": "[primary setup method e.g. 'Browser-based' or 'Docker' or 'pip install']",
  "overview": "[3-4 sentence paragraph comparing both tools accurately]",
  "key_differences": [
    "[difference 1: start with the aspect e.g. 'Cost: ...']",
    "[difference 2]",
    "[difference 3]",
    "[difference 4]",
    "[difference 5]"
  ],
  "pricing_table": {{
    "headers": ["{paid_tool}", "{free_tool}", "Notes"],
    "rows": [
      ["[aspect 1]", "[paid value]", "[free value]"],
      ["[aspect 2]", "[paid value]", "[free value]"],
      ["[aspect 3]", "[paid value]", "[free value]"],
      ["[aspect 4]", "[paid value]", "[free value]"],
      ["[aspect 5]", "[paid value]", "[free value]"]
    ]
  }},
  "migration": "[Step-by-step migration instructions as a single paragraph or numbered steps. Be specific and technical.]",
  "related": []
}}

Rules:
- All content must be factually accurate about both tools as of 2025
- The setup_dots field uses ● for filled and ○ for empty, always 5 characters total
- The pricing_table headers array has 3 items: paid tool name, free tool name, then "Notes" as third header - wait actually make the headers be the aspect names and values:
  headers: ["Aspect", "{paid_tool}", "{free_tool}"]
  rows: each row is [aspect, paid_value, free_value]
- migration should be practical, specific instructions someone can follow
- related is an empty array (will be populated later)
- Return ONLY the JSON object, nothing else"""


# ─────────────────────────────────────────────────────────────────────────────
# PRE-FLIGHT
# ─────────────────────────────────────────────────────────────────────────────

def preflight():
    errors = []

    if not GROQ_API_KEY:
        errors.append(
            "GROQ_API_KEY is not set.\n"
            "  Fix: Go to console.groq.com → API Keys → create a key\n"
            "  Then set it as a GitHub Actions secret:\n"
            "  Repo → Settings → Secrets → Actions → New secret → GROQ_API_KEY"
        )
    elif not GROQ_API_KEY.startswith("gsk_"):
        errors.append(
            f"GROQ_API_KEY does not look valid (should start with 'gsk_', got '{GROQ_API_KEY[:8]}...')"
        )
    else:
        log.info("✅ GROQ_API_KEY is set (prefix: %s...)", GROQ_API_KEY[:8])

    if not PAIRS_FILE.exists():
        errors.append(f"Tool pairs file not found: {PAIRS_FILE}")
    else:
        with open(PAIRS_FILE) as f:
            pairs = json.load(f)
        log.info("✅ Tool pairs file: %d pairs loaded", len(pairs))

    try:
        import requests
        log.info("✅ requests package available")
    except ImportError:
        errors.append("'requests' package not installed. Run: pip install requests")

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    log.info("✅ Cache dir ready: %s", CACHE_DIR)

    if errors:
        log.error("\n❌ PRE-FLIGHT FAILED:\n")
        for i, e in enumerate(errors, 1):
            log.error("  %d. %s", i, e)
        sys.exit(1)

    log.info("✅ All pre-flight checks passed\n")


# ─────────────────────────────────────────────────────────────────────────────
# API CONNECTIVITY TEST
# ─────────────────────────────────────────────────────────────────────────────

def test_api():
    import requests
    log.info("Testing Groq API connectivity...")

    resp = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
        json={
            "model": GROQ_MODEL,
            "messages": [{"role": "user", "content": "Reply with the single word: OK"}],
            "max_tokens": 5,
        },
        timeout=30,
    )

    if resp.status_code == 401:
        log.error("❌ Groq API returned 401 Unauthorized.")
        log.error("   Your GROQ_API_KEY is invalid or has been revoked.")
        log.error("   Fix: Go to console.groq.com → API Keys → create a new key")
        log.error("   Then update the GROQ_API_KEY secret in your repo.")
        sys.exit(1)
    elif resp.status_code == 429:
        log.error("❌ Groq API returned 429 — rate limit or quota exceeded.")
        log.error("   Response: %s", resp.text[:200])
        log.error("   Fix: Wait for rate limit reset, or check console.groq.com/usage")
        sys.exit(1)
    elif not resp.ok:
        log.error("❌ Groq API returned %d: %s", resp.status_code, resp.text[:200])
        sys.exit(1)

    log.info("✅ Groq API OK — model: %s\n", GROQ_MODEL)


# ─────────────────────────────────────────────────────────────────────────────
# GROQ API CALL
# ─────────────────────────────────────────────────────────────────────────────

def call_groq(prompt: str) -> str:
    import requests

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json",
                },
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
                log.warning("Rate limited. Waiting %ds (attempt %d/%d)...", wait, attempt, MAX_RETRIES)
                time.sleep(wait)
                continue

            if resp.status_code == 503:
                log.warning("Groq 503. Waiting %ds...", RETRY_DELAY * attempt)
                time.sleep(RETRY_DELAY * attempt)
                continue

            if not resp.ok:
                raise RuntimeError(f"Groq HTTP {resp.status_code}: {resp.text[:300]}")

            return resp.json()["choices"][0]["message"]["content"]

        except (Exception,) as e:
            if "timed out" in str(e).lower() or "connection" in str(e).lower():
                if attempt < MAX_RETRIES:
                    log.warning("Network error attempt %d: %s. Retrying...", attempt, e)
                    time.sleep(RETRY_DELAY * attempt)
                    continue
            raise

    raise RuntimeError(f"Groq API failed after {MAX_RETRIES} attempts")


# ─────────────────────────────────────────────────────────────────────────────
# GENERATE ONE COMPARISON
# ─────────────────────────────────────────────────────────────────────────────

def generate(pair: dict) -> dict:
    slug       = pair["slug"]
    paid_tool  = pair["paid_tool"]
    free_tool  = pair["free_tool"]
    github     = pair.get("github_repo")
    github_json = f'"{github}"' if github else "null"

    prompt = PROMPT.format(
        slug             = slug,
        category         = pair["category"],
        category_emoji   = pair["category_emoji"],
        paid_tool        = paid_tool,
        paid_price       = pair["paid_price"],
        paid_url         = pair["paid_url"],
        free_tool        = free_tool,
        free_price       = pair["free_price"],
        free_url         = pair["free_url"],
        github_repo_json = github_json,
    )

    raw = call_groq(prompt).strip()

    # Strip markdown fences if model added them
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
    if raw.endswith("```"):
        raw = raw.rsplit("```", 1)[0]
    raw = raw.strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise RuntimeError(
            f"Invalid JSON from Groq for {slug}.\n"
            f"JSON error: {e}\n"
            f"Raw (first 600 chars):\n{raw[:600]}"
        )

    # Validate required fields
    required = ["slug", "paid_tool", "free_tool", "verdict_switch", "verdict_stay",
                "overview", "key_differences", "migration"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        raise RuntimeError(
            f"Generated JSON for {slug} is missing fields: {missing}"
        )

    # Ensure slug matches what we requested
    data["slug"] = slug
    data["generated_at"] = datetime.now(timezone.utc).isoformat()

    return data


# ─────────────────────────────────────────────────────────────────────────────
# RELATED LINKS  — populate after all comparisons generated
# ─────────────────────────────────────────────────────────────────────────────

def populate_related(all_data: list) -> list:
    """For each comparison, find up to 3 others sharing a paid or free tool."""
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
    parser = argparse.ArgumentParser(description="Generate AI tool comparisons via Groq")
    parser.add_argument("--force",    action="store_true", help="Regenerate even if cached")
    parser.add_argument("--dry-run",  action="store_true", help="Validate setup only, no API calls")
    parser.add_argument("--slug",     type=str,            help="Generate one specific slug only")
    parser.add_argument("--limit",    type=int, default=0, help="Only process first N pairs")
    args = parser.parse_args()

    log.info("=" * 60)
    log.info("AI Tool Alternative Finder — Generate")
    log.info("Model:    %s", GROQ_MODEL)
    log.info("Cache:    %s", CACHE_DIR)
    log.info("Force:    %s", args.force)
    log.info("Dry run:  %s", args.dry_run)
    log.info("=" * 60)

    # Pre-flight
    preflight()

    # API test
    if not args.dry_run:
        test_api()

    # Load pairs
    with open(PAIRS_FILE) as f:
        pairs = json.load(f)

    # Filter
    if args.slug:
        pairs = [p for p in pairs if p["slug"] == args.slug]
        if not pairs:
            log.error("No pair found with slug: %s", args.slug)
            sys.exit(1)
        log.info("Single slug mode: %s", args.slug)

    if args.limit:
        pairs = pairs[:args.limit]
        log.info("Limit mode: processing first %d pairs", args.limit)

    # Determine which need generation
    to_generate = []
    skipped     = []
    for pair in pairs:
        cache_file = CACHE_DIR / f"{pair['slug']}.json"
        if cache_file.exists() and not args.force:
            skipped.append(pair["slug"])
        else:
            to_generate.append(pair)

    log.info("Total pairs:  %d", len(pairs))
    log.info("Already cached (skipping): %d", len(skipped))
    log.info("To generate:  %d", len(to_generate))

    if args.dry_run:
        log.info("\nDry run complete — no API calls made.")
        log.info("Would generate: %s", [p["slug"] for p in to_generate])
        return

    if not to_generate:
        log.info("\n✅ All comparisons already cached. Use --force to regenerate.")
        return

    # Generate
    succeeded = []
    failed    = []

    for i, pair in enumerate(to_generate, 1):
        slug = pair["slug"]
        log.info("\n[%d/%d] Generating: %s vs %s",
                 i, len(to_generate), pair["paid_tool"], pair["free_tool"])

        try:
            data = generate(pair)
            cache_file = CACHE_DIR / f"{slug}.json"
            cache_file.write_text(json.dumps(data, indent=2, ensure_ascii=False))
            log.info("  ✅ Saved: %s", cache_file)
            succeeded.append(slug)

            # Rate limit buffer between calls
            if i < len(to_generate):
                time.sleep(INTER_DELAY)

        except Exception as e:
            log.error("  ❌ FAILED: %s", slug)
            log.error("     %s", e)
            if os.getenv("GENERATE_DEBUG"):
                log.debug(traceback.format_exc())
            failed.append({"slug": slug, "error": str(e)})

    # Populate related links across all cached files
    log.info("\nPopulating related links...")
    all_cached = []
    for f in sorted(CACHE_DIR.glob("*.json")):
        try:
            all_cached.append(json.loads(f.read_text()))
        except Exception:
            pass

    all_cached = populate_related(all_cached)
    for item in all_cached:
        out = CACHE_DIR / f"{item['slug']}.json"
        out.write_text(json.dumps(item, indent=2, ensure_ascii=False))

    # Summary
    log.info("\n" + "=" * 60)
    log.info("GENERATION COMPLETE")
    log.info("  Succeeded: %d", len(succeeded))
    log.info("  Failed:    %d", len(failed))
    log.info("  Skipped:   %d", len(skipped))
    log.info("  Total cached: %d files in %s", len(list(CACHE_DIR.glob("*.json"))), CACHE_DIR)

    if failed:
        log.warning("\nFailed slugs:")
        for f in failed:
            log.warning("  - %s: %s", f["slug"], f["error"][:100])
        log.warning("\nThese will use hardcoded fallback data in build.py if available.")

    # Exit 1 if ALL pairs failed (nothing was generated)
    if to_generate and not succeeded:
        log.error("\n❌ FATAL: Zero comparisons were generated.")
        log.error("Check your GROQ_API_KEY and try again.")
        sys.exit(1)

    log.info("\n✅ Done. Run 'python scripts/build.py' to rebuild the site.")


if __name__ == "__main__":
    main()
