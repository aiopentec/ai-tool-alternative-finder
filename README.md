# 🤖 AI Tool Alternative Finder — v2 (AI-Generated Pipeline)

Compares paid AI tools to free alternatives. Content AI-written by Groq (Llama 3.3). $0/month to run.

**Live site:** https://aiopentec.github.io/ai-tool-alternative-finder

## How it works

```
data/tool_pairs.json          ← source of truth: 80 tool pairs
        ↓
scripts/generate.py           ← calls Groq API, writes rich JSON
        ↓
.cache/comparisons/*.json     ← one file per comparison (cached)
        ↓
scripts/build.py              ← generates all HTML pages
        ↓
GitHub Pages                  ← serves the site
```

The pipeline runs daily via GitHub Actions. Only new/missing comparisons
are regenerated — existing cached files are reused. Total API cost: ~$0
(Groq free tier handles ~80 comparisons in a single run).

## Local development

```bash
# Build with hardcoded fallback data (no API key needed)
python scripts/build.py

# Generate AI content for all 80 tool pairs
export GROQ_API_KEY=gsk_your_key_here
python scripts/generate.py

# Generate only new pairs (skips cached)
python scripts/generate.py

# Force regenerate everything
python scripts/generate.py --force

# Generate just one pair
python scripts/generate.py --slug chatgpt-plus-vs-openrouter

# Test first 5 pairs only
python scripts/generate.py --limit 5

# Check what data source build.py will use
python scripts/build.py --check
```

## Setup

1. Fork this repo
2. Add `GROQ_API_KEY` as a GitHub Actions secret (Settings → Secrets → Actions)
3. Enable GitHub Pages (Settings → Pages → Deploy from branch → main)
4. Run the workflow manually once (Actions → Run workflow)

## Adding new tool pairs

Edit `data/tool_pairs.json` and add a new entry:

```json
{
  "slug": "toolname-vs-alternative",
  "category": "AI Coding",
  "category_emoji": "💻",
  "paid_tool": "Tool Name",
  "paid_price": "$X/month",
  "paid_url": "https://tool.com",
  "free_tool": "Free Alternative",
  "free_price": "Free",
  "free_url": "https://free-tool.com",
  "github_repo": "owner/repo"
}
```

The pipeline auto-generates the comparison content on next run.

## File structure

```
data/
  tool_pairs.json           ← edit this to add comparisons
scripts/
  generate.py               ← Groq API → .cache/comparisons/
  build.py                  ← .cache/comparisons/ → HTML pages
.cache/
  comparisons/              ← AI-generated JSON (committed to repo)
.github/
  workflows/
    pipeline.yml            ← daily Generate → Build → Push
```

---
$0/month · GitHub Pages · Groq API (free tier) · Daily auto-update
