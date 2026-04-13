# 🤖 AI Tool Alternative Finder

Automatically compares paid AI tools to free/cheaper alternatives. AI-analyzed, self-updating, **$0/month to run**.

Live site: https://aiopentec.github.io/ai-tool-alternative-finder

## What's inside

- **33 comparisons** across 5 categories (AI Writing, Image Generation, Coding, Voice/Audio, Video, APIs)
- Individual comparison pages with pricing tables, verdict boxes, and step-by-step migration guides
- Interactive savings calculator — enter your seat count, see exact savings
- Daily auto-update via GitHub Actions
- Sitemap auto-submitted for SEO

## Categories

| Category | Tools Covered |
|---|---|
| ✍️ AI Writing & Chat | ChatGPT Plus, Jasper, Copy.ai, Grammarly, Notion AI, Writesonic, Perplexity |
| 🎨 AI Image Generation | Midjourney, DALL-E 3, Adobe Firefly, Canva AI, Runway ML |
| 💻 AI Coding | GitHub Copilot, Cursor AI, Tabnine, Replit AI |
| 🎤 AI Voice & Audio | ElevenLabs, Murf, Descript, Otter.ai, Adobe Podcast |
| 📹 AI Video | Synthesia, Pictory, InVideo AI |
| 💬 AI APIs | OpenAI API, Anthropic API — vs Ollama, Groq, Together AI, Fireworks |

## Run locally

```bash
git clone https://github.com/aiopentec/ai-tool-alternative-finder
cd ai-tool-alternative-finder
python scripts/build.py
# Open index.html in your browser
```

## How it works

1. `scripts/build.py` generates all HTML from a Python data dictionary
2. GitHub Actions runs the build daily (`cron: '0 6 * * *'`)
3. Generated files are committed back to `main` branch
4. GitHub Pages serves the `main` branch automatically

## Deploy to GitHub Pages

1. Fork or create repo on GitHub
2. Go to **Settings → Pages → Source: Deploy from branch → main / (root)**
3. Push to `main` — the Action builds and deploys automatically

## Adding new comparisons

Edit the `COMPARISONS` list in `scripts/build.py` and add a new dictionary following the existing schema. The build generates all pages and updates the sitemap automatically.

---

$0/month to operate · Hosted on GitHub Pages · Auto-updated daily
