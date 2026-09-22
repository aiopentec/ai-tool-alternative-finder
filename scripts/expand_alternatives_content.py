#!/usr/bin/env python3
"""
expand_alternatives_content.py — AI Tool Alternative Finder

Generates an expanded intro + FAQ for each "alternatives-to-<tool>" hub page,
so those pages stop being a one-paragraph link list and get real unique
content per paid tool (mirrors the pattern used for OSALFinder's category
hub pages).

Provider waterfall (same as generate.py):
  1. Groq   (free, fast)
  2. Gemini Flash (free, fallback)
  3. Template engine (always works, no API needed)

Usage:
  python scripts/expand_alternatives_content.py              # generate all missing
  python scripts/expand_alternatives_content.py --force      # regenerate all
  python scripts/expand_alternatives_content.py --index 1    # batch mode (10 per batch)
"""

import argparse, json, logging, os, re, time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)-8s | %(message)s')
logger = logging.getLogger(__name__)

DATA_FILE = Path(__file__).parent.parent / 'data' / 'tool_pairs.json'
CACHE_DIR = Path(__file__).parent.parent / '.cache' / 'alternatives'

MIN_WORDS = 300  # target floor for the expanded intro, similar to OSALFinder's category-page fix


# ── Load data ────────────────────────────────────────────────────────────────
def load_data() -> Tuple[Dict, List]:
    with open(DATA_FILE) as f:
        data = json.load(f)
    return data['tools'], data['pairs']


def paid_tools_with_pages(tools: Dict, pairs: List) -> Dict[str, List[str]]:
    """Maps paid_key -> list of free_keys that alternatives-to-<paid> will list."""
    by_paid: Dict[str, List[str]] = {}
    for paid_key, free_key in pairs:
        by_paid.setdefault(paid_key, []).append(free_key)
    return by_paid


# ── Prompt builder ───────────────────────────────────────────────────────────
def build_prompt(paid: Dict, free_names: List[str]) -> str:
    free_list = ', '.join(free_names)
    return f"""You are a technical writer producing a hub page for an AI tools directory.
The page lists free/open-source alternatives to a paid tool. The free alternatives
already have their own card list below this content — do NOT repeat that list.
Write only the sections below, in Markdown, at least {MIN_WORDS} words total.

# Free Alternatives to {paid['name']}

Tool being replaced: {paid['name']} ({paid.get('company', 'N/A')}, founded {paid.get('founded', 'N/A')})
What it does: {paid.get('description', '')}
Pricing: {paid.get('pricing', 'N/A')}
Free alternatives being compared on this page: {free_list}

## Why People Look for a Free Alternative to {paid['name']}
2-3 sentences on the specific pain points that send {paid['name']} users looking
for a free option (cost, privacy, usage limits, vendor lock-in — pick what's
actually relevant to this specific tool, not generic filler).

## What to Look For in a Free {paid['name']} Alternative
A short paragraph or 3-4 bullet points on the concrete criteria that matter for
THIS category of tool specifically (e.g. for image generation: GPU requirements
and model quality; for transcription: language support and accuracy; for coding
assistants: IDE integration and model flexibility). Be specific to this tool's
category, not generic.

## Frequently Asked Questions
Exactly 3 question-and-answer pairs as:
**Q: <question>**
A: <2-3 sentence answer>

Questions should be ones a real user of {paid['name']} would actually ask when
evaluating free alternatives — not generic AI-tool boilerplate.

Return ONLY the Markdown. No preamble, no code fences."""


# ── AI Provider 1: Groq ──────────────────────────────────────────────────────
def generate_with_groq(prompt: str) -> str:
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        raise ValueError('GROQ_API_KEY not set')
    r = requests.post(
        'https://api.groq.com/openai/v1/chat/completions',
        headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'},
        json={
            'model': 'openai/gpt-oss-120b',
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 1400,
            'temperature': 0.6,
        },
        timeout=45,
    )
    r.raise_for_status()
    return r.json()['choices'][0]['message']['content']


# ── AI Provider 2: Gemini Flash ──────────────────────────────────────────────
def generate_with_gemini(prompt: str) -> str:
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError('GEMINI_API_KEY not set')
    r = requests.post(
        'https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-lite-latest:generateContent?key={}'.format(api_key),
        headers={'Content-Type': 'application/json'},
        json={'contents': [{'parts': [{'text': prompt}]}]},
        timeout=45,
    )
    r.raise_for_status()
    return r.json()['candidates'][0]['content']['parts'][0]['text']


# ── Fallback: template engine (uses real per-tool fields, not filler) ───────
def generate_with_template(paid_key: str, paid: Dict, free_names: List[str]) -> str:
    name = paid['name']
    company = paid.get('company', 'its vendor')
    desc = paid.get('description', f"{name} is a paid AI tool.")
    pricing = paid.get('pricing', 'a recurring subscription')
    category = paid.get('category', 'text-generation').replace('-', ' ')
    count = len(free_names)

    return f"""## Why People Look for a Free Alternative to {name}

{desc} At {pricing}, the cost adds up quickly for individuals and small teams,
and every request is processed on {company}'s servers rather than your own —
two of the most common reasons {name} users start evaluating free,
self-hosted options in the {category} space.

## What to Look For in a Free {name} Alternative

- **Feature parity** — does it cover the specific {category} workflow you use {name} for today, not just the headline feature?
- **Setup cost vs. subscription cost** — self-hosted tools trade a recurring bill for a one-time setup investment; make sure that trade actually pays off for your usage volume.
- **Data handling** — confirm whether the alternative processes data locally or still calls out to a third-party API.
- **Maintenance** — open-source tools need occasional updates; factor that ongoing time cost in alongside the {count} option{'s' if count != 1 else ''} compared below.

## Frequently Asked Questions

**Q: Is a free alternative to {name} actually as good?**
A: It depends on your use case. Free and open-source tools in the {category} space have closed much of the quality gap, but {name} still has advantages in polish, support, and integrations that some workflows depend on — the comparisons below break down where each option wins.

**Q: Will switching from {name} save money?**
A: Usually, yes, if your usage is moderate to high — {pricing} adds up over a year. The main offsetting cost is setup and maintenance time, which is worth weighing against what you're currently paying.

**Q: Can I use a free alternative to {name} for commercial work?**
A: Most open-source alternatives allow commercial use, but licensing varies by project — check the specific license listed in each comparison below before relying on it for client or production work.
"""


# ── Word count helper ────────────────────────────────────────────────────────
def word_count(markdown: str) -> int:
    return len(re.sub(r'[#*`>-]', ' ', markdown).split())


# ── Main generation function ─────────────────────────────────────────────────
_groq_consecutive_429s = 0
_GROQ_429_CIRCUIT_BREAKER = 3  # after this many consecutive 429s, stop calling Groq for the rest of this run


def generate_alternatives_content(paid_key: str, paid: Dict, free_keys: List[str], tools: Dict) -> Dict:
    global _groq_consecutive_429s
    free_names = [tools.get(fk, {}).get('name', fk) for fk in free_keys]
    prompt = build_prompt(paid, free_names)

    content = None
    provider = None

    if _groq_consecutive_429s < _GROQ_429_CIRCUIT_BREAKER:
        try:
            content = generate_with_groq(prompt)
            provider = 'groq'
            _groq_consecutive_429s = 0
            logger.info('    ✅ Generated with Groq')
        except requests.exceptions.HTTPError as e:
            if e.response is not None and e.response.status_code == 429:
                _groq_consecutive_429s += 1
                logger.warning('    ⚠️  Groq rate-limited (429) — skipping retry, falling to Gemini')
                if _groq_consecutive_429s >= _GROQ_429_CIRCUIT_BREAKER:
                    logger.warning(
                        f'    🛑 Groq rate-limited {_GROQ_429_CIRCUIT_BREAKER}x in a row — '
                        f'disabling Groq for the rest of this run'
                    )
            else:
                logger.warning(f'    ⚠️  Groq failed ({type(e).__name__}): {e}')
                time.sleep(10)
                try:
                    content = generate_with_groq(prompt)
                    provider = 'groq'
                    _groq_consecutive_429s = 0
                    logger.info('    ✅ Generated with Groq (retry)')
                except Exception as e2:
                    logger.warning(f'    ⚠️  Groq retry failed ({type(e2).__name__}): {e2}')
        except Exception as e:
            logger.warning(f'    ⚠️  Groq failed ({type(e).__name__}): {e}')
            time.sleep(10)
            try:
                content = generate_with_groq(prompt)
                provider = 'groq'
                _groq_consecutive_429s = 0
                logger.info('    ✅ Generated with Groq (retry)')
            except Exception as e2:
                logger.warning(f'    ⚠️  Groq retry failed ({type(e2).__name__}): {e2}')
    else:
        logger.info('    ⏭️  Skipping Groq this item (circuit breaker tripped earlier this run)')

    if content is None:
        try:
            content = generate_with_gemini(prompt)
            provider = 'gemini'
            logger.info('    ✅ Generated with Gemini')
        except Exception as e:
            logger.warning(f'    ⚠️  Gemini failed ({type(e).__name__}): {e}')

    if content is None or word_count(content) < MIN_WORDS:
        if content is not None:
            logger.warning(f'    ⚠️  AI output too thin ({word_count(content)} words) — using template instead')
        content = generate_with_template(paid_key, paid, free_names)
        provider = 'template'
        logger.info('    ✅ Generated with template engine')

    return {
        'paid_key': paid_key,
        'paid_name': paid['name'],
        'free_keys': free_keys,
        'expanded_markdown': content,
        'word_count': word_count(content),
        'provider': provider,
        'generated_at': datetime.utcnow().isoformat() + 'Z',
    }


# ── CLI ───────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--force', action='store_true', help='Regenerate even if cached')
    parser.add_argument('--index', type=int, default=None, help='Batch index (10 per batch)')
    args = parser.parse_args()

    tools, pairs = load_data()
    by_paid = paid_tools_with_pages(tools, pairs)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    items = sorted(by_paid.items())
    if args.index is not None:
        start = args.index * 10
        items = items[start:start + 10]

    built, skipped = 0, 0
    for paid_key, free_keys in items:
        cache_file = CACHE_DIR / f'{paid_key}.json'
        if cache_file.exists() and not args.force:
            skipped += 1
            continue

        paid = tools.get(paid_key)
        if not paid:
            logger.warning(f'  ⚠️  No tool data for {paid_key}, skipping')
            continue

        logger.info(f'Generating alternatives-to-{paid_key} ({len(free_keys)} alternatives)...')
        result = generate_alternatives_content(paid_key, paid, free_keys, tools)
        cache_file.write_text(json.dumps(result, indent=2), encoding='utf-8')
        logger.info(f'    → {result["provider"]}, {result["word_count"]} words')
        built += 1

    logger.info(f'Done. Built {built}, skipped {skipped} (already cached).')


if __name__ == '__main__':
    main()
