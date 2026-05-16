# 🤖 AI Tool Alternative Finder

> Free AI alternatives to ChatGPT Plus, GitHub Copilot, Midjourney, ElevenLabs, and more.  
> AI-researched daily. $0/month to operate. 100% static.

**Live site:** [aiopentec.github.io/ai-tool-alternative-finder](https://aiopentec.github.io/ai-tool-alternative-finder)

---

## What This Is

A programmatic SEO site that compares paid AI tools to their free, open-source alternatives. Every comparison page covers:

- Side-by-side pricing breakdown
- Privacy and data ownership analysis
- Setup difficulty rating
- Step-by-step migration guide
- Quick verdict (when to switch, when to stay)

**~200 pages generated per run** across 10 AI tool categories.

---

## Architecture

```
data/tool_pairs.json         ← 57 tools, 59 comparison pairs
    ↓
scripts/generate.py          ← Groq (primary) → Gemini (fallback) → template
    ↓
.cache/comparisons/*.json    ← one JSON file per comparison
    ↓
scripts/build.py             ← generates all HTML pages
    ↓
site/                        ← static output
    ↓
GitHub Pages                 ← live at aiopentec.github.io/ai-tool-alternative-finder
```

**Provider waterfall in generate.py:**
1. Groq API (`llama-3.3-70b-versatile`) — free, fast
2. Google Gemini Flash — free, reliable fallback
3. Template engine — built-in, always works, zero API calls

---

## Pages Generated

| Type | Count | Example |
|------|-------|---------|
| Comparison pages | ~59 | `chatgpt-plus-vs-open-webui/` |
| Alternatives-to pages | ~20 | `alternatives-to-chatgpt-plus/` |
| Blog posts | 6 | `blog/free-local-ai-chatgpt-alternatives/` |
| Utility pages | 4 | `about/`, `contact/`, `privacy/`, `404` |
| Sitemap + robots | 2 | `sitemap.xml`, `robots.txt` |

---

## Categories

| Category | Icon | Examples |
|----------|------|---------|
| Text Generation | 📝 | ChatGPT Plus, Claude Pro, Jasper |
| Code Assistance | 💻 | GitHub Copilot, Cursor Pro, Tabnine |
| Image Generation | 🎨 | Midjourney, DALL-E 3, Adobe Firefly |
| Voice AI | 🎤 | ElevenLabs, Murf AI |
| Video AI | 🎬 | Runway ML, Luma AI, Synthesia |
| Research AI | 🔍 | Perplexity Pro |
| Audio & Transcription | 🎵 | Descript, Otter.ai |
| Translation AI | 🌐 | DeepL Pro |
| Productivity AI | 📊 | Notion AI, Microsoft Copilot 365 |
| AI APIs | ⚡ | OpenAI API |

---

## Setup

### 1. Clone

```bash
git clone https://github.com/aiopentec/ai-tool-alternative-finder.git
cd ai-tool-alternative-finder
pip install -r requirements.txt
```

### 2. Add API keys (optional — template fallback works without them)

```bash
export GROQ_API_KEY="gsk_..."       # get free at console.groq.com
export GEMINI_API_KEY="AIza..."     # get free at aistudio.google.com
```

### 3. Generate content

```bash
# Generate all missing comparisons
python scripts/generate.py

# Generate a specific batch of 10
python scripts/generate.py --index 1

# Force regenerate everything
python scripts/generate.py --force
```

### 4. Build site

```bash
python scripts/build.py
# → outputs to site/
```

### 5. Preview locally

```bash
cd site && python -m http.server 8000
# open http://localhost:8000
```

---

## GitHub Actions Pipeline

The pipeline runs automatically every day at 6 AM UTC:

1. **Generate** — runs `generate.py`, fills `.cache/comparisons/`
2. **Build** — runs `build.py`, outputs to `site/`
3. **Deploy** — pushes `site/` to `gh-pages` branch via `peaceiris/actions-gh-pages`

### Required GitHub Secrets

| Secret | Required | Source |
|--------|----------|--------|
| `GROQ_API_KEY` | Recommended | [console.groq.com](https://console.groq.com) |
| `GEMINI_API_KEY` | Recommended | [aistudio.google.com](https://aistudio.google.com) |
| `GA_ID` | Optional | Google Analytics 4 measurement ID |
| `ADSENSE_ID` | Optional | Google AdSense publisher ID |

### Manual triggers

Go to **Actions → Generate & Build AI Tool Alternative Finder → Run workflow**

Options:
- **batch_index** — run only 10 comparisons (e.g. `1` for pairs 1-10, `2` for 11-20)
- **force_rebuild** — set `true` to regenerate all even if cached

---

## Adding New Tool Pairs

Edit `data/tool_pairs.json`:

```json
{
  "tools": {
    "new-paid-tool": {
      "name": "New Paid Tool",
      "category": "text-generation",
      "pricing": "$X/month",
      "license": "Proprietary",
      "website": "https://example.com",
      "description": "What it does.",
      "company": "Company Name",
      "founded": "2023"
    },
    "new-free-tool": {
      "name": "New Free Tool",
      "category": "text-generation",
      "pricing": "Free (self-hosted)",
      "license": "MIT",
      "website": "https://example.com",
      "description": "What it does.",
      "github": "owner/repo",
      "stars_approx": "10k"
    }
  },
  "pairs": [
    ["new-paid-tool", "new-free-tool"]
  ]
}
```

Then run `generate.py` to create the comparison content, and `build.py` to rebuild the site.

---

## Cost

| Component | Cost |
|-----------|------|
| GitHub Pages hosting | $0 |
| GitHub Actions CI/CD | $0 |
| Groq API (LLM) | $0 (free tier) |
| Gemini Flash API (fallback) | $0 (free tier) |
| **Total** | **$0/month** |

---

## Tech Stack

- Python 3.11 — generation + build
- GitHub Actions — daily automation
- GitHub Pages — static hosting
- Groq API — primary LLM (free tier)
- Google Gemini Flash — fallback LLM (free tier)
- Zero JS frameworks — plain HTML/CSS/JS

---

Built by [aiopentec](https://github.com/aiopentec) · Inspired by [osalfinder.com](https://osalfinder.com)
