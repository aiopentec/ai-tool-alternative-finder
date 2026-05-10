#!/usr/bin/env python3
"""
build.py — AI Tool Alternative Finder
Generates the complete static site from comparison data.

Data priority (highest to lowest):
  1. .cache/comparisons/*.json  — AI-generated via generate.py
  2. FALLBACK_COMPARISONS below — hardcoded, always available offline

Usage:
    python scripts/build.py          # build site
    python scripts/build.py --check  # show what data source will be used
"""

import os
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

SITE_URL       = "https://aiopentec.github.io/ai-tool-alternative-finder"
SITE_TITLE     = "AI Tool Alternative Finder"
SITE_DESC      = "Discover free and cheaper alternatives to popular paid AI tools — with detailed comparisons. Save hundreds per year."
GA_ID          = "G-FGB481RVVS"
BUILD_DATE     = datetime.now(timezone.utc).strftime("%B %d, %Y")
BUILD_DATE_ISO = datetime.now(timezone.utc).strftime("%Y-%m-%d")
CACHE_DIR      = Path(".cache/comparisons")

# ─────────────────────────────────────────────────────────────────────────────
# FALLBACK DATA — used when .cache/comparisons/ is empty or missing
# Replace with generate.py output in production
# ─────────────────────────────────────────────────────────────────────────────

FALLBACK_COMPARISONS = [
    {
        "slug": "chatgpt-plus-vs-openrouter",
        "category": "AI Writing & Chat",
        "category_emoji": "✍️",
        "paid_tool": "ChatGPT Plus",
        "paid_price": "$20/month",
        "paid_url": "https://chat.openai.com",
        "free_tool": "OpenRouter",
        "free_price": "Free tier / pay-per-use",
        "free_url": "https://openrouter.ai",
        "github_repo": None,
        "savings": "$20/month → Free tier available",
        "verdict_switch": "OpenRouter is ideal for developers and power users who want access to 100+ models including free tiers of Llama 3, Mistral, Gemma, and more without a flat monthly fee.",
        "verdict_stay": "ChatGPT Plus is best when you rely on GPT-4o's code interpreter, image generation (DALL-E), or the polished consumer UI with no setup required.",
        "setup_difficulty": "Easy",
        "setup_dots": "●●○○○",
        "setup_time": "~5 mins",
        "setup_method": "Browser-based",
        "overview": "ChatGPT Plus is OpenAI's $20/month subscription offering priority access to GPT-4o, DALL-E 3, code interpreter, custom GPTs, and more. OpenRouter is a unified API router and web chat interface that gives you access to 100+ AI models from multiple providers — many completely free — including GPT-4o, Claude 3.5, Llama 3.1, Mistral, and Gemini.",
        "key_differences": [
            "Cost: ChatGPT Plus is $20/month flat; OpenRouter has free model tiers and pay-per-token pricing",
            "Model variety: OpenRouter routes to 100+ models across 20+ providers; ChatGPT Plus is OpenAI-only",
            "Free models: OpenRouter hosts Llama 3.1, Mistral 7B, Gemma 2 and more at $0",
            "API access: OpenRouter provides an OpenAI-compatible API endpoint; ChatGPT Plus is a consumer UI",
            "Context length: Many OpenRouter models offer 128K+ context windows",
        ],
        "pricing_table": {
            "headers": ["Aspect", "ChatGPT Plus", "OpenRouter"],
            "rows": [
                ["Base pricing", "$20/month", "Free tier available"],
                ["GPT-4o access", "✅ Included", "✅ Pay-per-token"],
                ["Free models", "❌", "✅ Llama 3.1, Mistral, Gemma"],
                ["API access", "❌ Separate billing", "✅ Included"],
                ["Model variety", "OpenAI only", "100+ models"],
            ]
        },
        "migration": "Sign up at openrouter.ai (free). In the Chat tab, select a free model like meta-llama/llama-3.1-8b-instruct:free. For API use, replace your OpenAI base URL with https://openrouter.ai/api/v1 and use your OpenRouter API key — the API is fully OpenAI-compatible.",
        "related": ["chatgpt-plus-vs-mistral-free", "openai-api-vs-ollama"],
    },
    {
        "slug": "github-copilot-vs-codeium",
        "category": "AI Coding",
        "category_emoji": "💻",
        "paid_tool": "GitHub Copilot",
        "paid_price": "$10–$19/month",
        "paid_url": "https://github.com/features/copilot",
        "free_tool": "Codeium",
        "free_price": "Free",
        "free_url": "https://codeium.com",
        "github_repo": None,
        "savings": "$10–$19/month → Free",
        "verdict_switch": "Codeium's free tier provides unlimited AI code completions, chat, and search across 70+ languages and 40+ editors — matching GitHub Copilot's core functionality at $0.",
        "verdict_stay": "GitHub Copilot's native GitHub integration, pull request summaries, and deeper training on GitHub's massive code corpus give it an edge for enterprise teams.",
        "setup_difficulty": "Easy",
        "setup_dots": "●○○○○",
        "setup_time": "~5 mins",
        "setup_method": "IDE plugin",
        "overview": "GitHub Copilot charges $10–$19/month for AI code completion, chat, and PR summaries. Codeium is a free AI coding assistant offering unlimited completions, in-editor chat, and codebase search — supporting 70+ languages with VS Code, JetBrains, Vim, and other editors.",
        "key_differences": [
            "Cost: GitHub Copilot is $10–$19/month; Codeium is completely free for individuals",
            "Completions: Both offer real-time inline suggestions; quality is comparable for most tasks",
            "GitHub integration: Copilot has native PR review summaries; Codeium does not",
            "Privacy: Codeium has a strong no-training-on-user-code policy by default",
            "Editor support: Both support all major editors; Codeium supports 40+ editors",
        ],
        "pricing_table": {
            "headers": ["Aspect", "GitHub Copilot", "Codeium"],
            "rows": [
                ["Base pricing", "$10/month individual", "Free"],
                ["Completions", "Unlimited", "Unlimited"],
                ["In-editor chat", "✅", "✅ Free"],
                ["PR summaries", "✅ GitHub native", "❌"],
                ["Codebase search", "✅ Paid tier", "✅ Free"],
            ]
        },
        "migration": "In VS Code, open Extensions (Ctrl+Shift+X), search 'Codeium', and install. Sign up at codeium.com for a free account and authenticate. Disable GitHub Copilot extension to avoid conflicts.",
        "related": ["github-copilot-vs-continue-dev", "cursor-ai-vs-continue-dev"],
    },
    {
        "slug": "openai-api-vs-ollama",
        "category": "AI APIs & Infrastructure",
        "category_emoji": "💬",
        "paid_tool": "OpenAI API",
        "paid_price": "$0.15–$15/1M tokens",
        "paid_url": "https://platform.openai.com",
        "free_tool": "Ollama",
        "free_price": "Free (self-hosted)",
        "free_url": "https://ollama.ai",
        "github_repo": "ollama/ollama",
        "savings": "API costs → $0",
        "verdict_switch": "Ollama lets you run Llama 3.1, Mistral, Gemma 2, DeepSeek, and 100+ models locally with an OpenAI-compatible API — eliminating per-token cloud costs entirely for development and private use.",
        "verdict_stay": "OpenAI API's GPT-4o and o1 models remain ahead on complex reasoning and long-context tasks. For production apps with quality SLAs, cloud APIs still win.",
        "setup_difficulty": "Easy",
        "setup_dots": "●●○○○",
        "setup_time": "~5 mins",
        "setup_method": "Native installer",
        "overview": "OpenAI API charges per token used — ranging from $0.15/1M tokens for GPT-4o Mini to $15/1M for GPT-4o. Ollama is a free tool for running large language models locally, providing an OpenAI-compatible REST API on localhost — meaning you can switch existing apps from OpenAI to Ollama by changing one URL.",
        "key_differences": [
            "Cost: OpenAI API charges per token; Ollama is free (electricity only)",
            "Privacy: All Ollama inference stays on your machine — no data sent externally",
            "Model quality: GPT-4o leads on complex tasks; Llama 3.1 70B is competitive for most use cases",
            "Setup: Ollama installs in 5 minutes; OpenAI API requires signup and billing setup",
            "Internet required: Ollama runs fully offline; OpenAI requires internet",
        ],
        "pricing_table": {
            "headers": ["Aspect", "OpenAI API", "Ollama"],
            "rows": [
                ["Pricing", "$0.15–$15/1M tokens", "Free"],
                ["Hardware needed", "None (cloud)", "8GB+ RAM"],
                ["API compatibility", "OpenAI standard", "OpenAI-compatible"],
                ["Privacy", "Sent to OpenAI", "100% local"],
                ["Offline use", "❌", "✅"],
            ]
        },
        "migration": "1. Install Ollama: curl -fsSL https://ollama.ai/install.sh | sh (Linux/Mac) or download from ollama.ai (Windows). 2. Pull a model: ollama pull llama3.1. 3. In your app, change base_url from https://api.openai.com/v1 to http://localhost:11434/v1. No API key needed.",
        "related": ["openai-api-vs-groq", "claude-api-vs-ollama"],
    },
    {
        "slug": "midjourney-vs-stable-diffusion",
        "category": "AI Image Generation",
        "category_emoji": "🎨",
        "paid_tool": "Midjourney",
        "paid_price": "$10–$60/month",
        "paid_url": "https://midjourney.com",
        "free_tool": "Stable Diffusion (ComfyUI)",
        "free_price": "Free (self-hosted)",
        "free_url": "https://github.com/comfyanonymous/ComfyUI",
        "github_repo": "comfyanonymous/ComfyUI",
        "savings": "$10–$60/month → Free",
        "verdict_switch": "Stable Diffusion with SDXL or Flux models generates comparable image quality to Midjourney at zero cost — you own all outputs, have no usage limits, and can run uncensored styles.",
        "verdict_stay": "Midjourney's aesthetic quality is uniquely refined, especially for stylized art. Its prompt interpretation is more intuitive for non-technical users than ComfyUI's node-based workflow.",
        "setup_difficulty": "Medium",
        "setup_dots": "●●●○○",
        "setup_time": "~30 mins",
        "setup_method": "Local install (GPU recommended)",
        "overview": "Midjourney is the market-leading AI image generator charging $10–$60/month for varying generation credits. Stable Diffusion is a free, open-source image generation model you can run locally with ComfyUI — generating unlimited images at no ongoing cost once hardware is set up.",
        "key_differences": [
            "Cost: Midjourney charges monthly; Stable Diffusion is free after hardware investment",
            "Hardware: Stable Diffusion benefits from a GPU (8GB+ VRAM); Midjourney is cloud-based",
            "Privacy: Local SD generates images never sent to any server; Midjourney stores all generations",
            "Customization: SD supports LoRA models, ControlNet, inpainting; Midjourney is prompt-only",
            "Image ownership: Midjourney has complex ToS; local SD output is fully yours",
        ],
        "pricing_table": {
            "headers": ["Aspect", "Midjourney", "Stable Diffusion"],
            "rows": [
                ["Base pricing", "$10–$60/month", "Free"],
                ["GPU required", "❌ Cloud-based", "✅ Recommended"],
                ["Generations", "200–unlimited/month", "Unlimited"],
                ["Image ownership", "Check ToS", "100% yours"],
                ["Style control", "Prompts + params", "LoRA, ControlNet, etc"],
            ]
        },
        "migration": "1. Install Python 3.10+. 2. Clone ComfyUI: git clone https://github.com/comfyanonymous/ComfyUI. 3. Install requirements: pip install -r requirements.txt. 4. Download a model (e.g., Flux Schnell from HuggingFace) into models/checkpoints/. 5. Run: python main.py. 6. Open http://localhost:8188.",
        "related": ["dalle3-vs-stable-diffusion", "adobe-firefly-vs-stable-diffusion"],
    },
    {
        "slug": "elevenlabs-vs-coqui-tts",
        "category": "AI Voice & Audio",
        "category_emoji": "🎤",
        "paid_tool": "ElevenLabs",
        "paid_price": "$5–$99/month",
        "paid_url": "https://elevenlabs.io",
        "free_tool": "Coqui TTS (XTTS)",
        "free_price": "Free (self-hosted)",
        "free_url": "https://github.com/coqui-ai/TTS",
        "github_repo": "coqui-ai/TTS",
        "savings": "$5–$99/month → Free",
        "verdict_switch": "Coqui TTS generates high-quality, expressive text-to-speech locally — including voice cloning from short samples — at zero ongoing cost and with full data privacy.",
        "verdict_stay": "ElevenLabs' voice quality, especially for emotional range, is still industry-leading. Its streaming API and pre-made voice library make it much easier for production use.",
        "setup_difficulty": "Medium",
        "setup_dots": "●●●○○",
        "setup_time": "~15 mins",
        "setup_method": "Python pip",
        "overview": "ElevenLabs is the premium text-to-speech and voice cloning service charging $5–$99/month based on character limits. Coqui TTS is an open-source TTS library with 17+ models including XTTS — which supports voice cloning from a short audio sample — running entirely on your own hardware.",
        "key_differences": [
            "Cost: ElevenLabs is $5–$99/month; Coqui TTS is free and self-hosted",
            "Voice quality: ElevenLabs leads for emotional realism; XTTS is competitive for natural speech",
            "Voice cloning: Both support cloning; ElevenLabs needs 1 min sample, XTTS works with 6 seconds",
            "Character limits: ElevenLabs caps by plan; Coqui has no limits on local hardware",
            "Privacy: All Coqui processing stays on your machine; ElevenLabs is cloud-only",
        ],
        "pricing_table": {
            "headers": ["Aspect", "ElevenLabs", "Coqui TTS (XTTS)"],
            "rows": [
                ["Pricing", "$5–$99/month", "Free"],
                ["Voice cloning", "✅ 1 min sample", "✅ 6 sec sample"],
                ["Character limit", "30K–2M/month", "Unlimited"],
                ["Languages", "29+", "17+"],
                ["Privacy", "Cloud", "100% local"],
            ]
        },
        "migration": "pip install TTS. Generate speech: tts --text 'Hello world' --model_name tts_models/multilingual/multi-dataset/xtts_v2 --out_path output.wav. For voice cloning: add --speaker_wav your_voice.wav --language_idx en.",
        "related": ["murf-ai-vs-piper-tts", "otter-ai-vs-whisper"],
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# LOAD COMPARISONS — cache first, fallback second
# ─────────────────────────────────────────────────────────────────────────────

def load_comparisons():
    """Load from .cache/comparisons/ if available, else use FALLBACK_COMPARISONS."""
    if CACHE_DIR.exists():
        files = sorted(CACHE_DIR.glob("*.json"))
        if files:
            loaded = []
            errors = []
            for f in files:
                try:
                    data = json.loads(f.read_text(encoding="utf-8"))
                    # Validate minimally
                    if data.get("slug") and data.get("paid_tool") and data.get("free_tool"):
                        loaded.append(data)
                    else:
                        errors.append(f.name)
                except Exception as e:
                    errors.append(f"{f.name}: {e}")
            if errors:
                print(f"  ⚠️  Skipped {len(errors)} malformed cache files: {errors[:3]}")
            if loaded:
                print(f"  📦 Loaded {len(loaded)} comparisons from .cache/comparisons/")
                return loaded

    print(f"  📋 Using {len(FALLBACK_COMPARISONS)} hardcoded fallback comparisons")
    print(f"     (Run 'python scripts/generate.py' to generate AI-written content)")
    return FALLBACK_COMPARISONS


COMPARISONS = load_comparisons()

# ─────────────────────────────────────────────────────────────────────────────
# DERIVED LOOKUPS
# ─────────────────────────────────────────────────────────────────────────────

CATEGORIES = sorted(list(set(c["category"] for c in COMPARISONS)))

def category_count(cat):
    return sum(1 for c in COMPARISONS if c["category"] == cat)

def paid_key(c):
    return c["slug"].split("-vs-")[0]

def free_key(c):
    return "-vs-".join(c["slug"].split("-vs-")[1:])

# ─────────────────────────────────────────────────────────────────────────────
# FILE I/O
# ─────────────────────────────────────────────────────────────────────────────

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓  {path}")

# ─────────────────────────────────────────────────────────────────────────────
# SHARED CSS
# ─────────────────────────────────────────────────────────────────────────────

CSS = """
<style>
  :root {
    --bg: #0D1117; --surface: #161B22; --border: #30363D;
    --text: #E6EDF3; --muted: #8B949E; --accent: #58A6FF;
    --green: #3FB950; --yellow: #D29922; --red: #F85149; --radius: 8px;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: var(--bg); color: var(--text); font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif; font-size: 15px; line-height: 1.6; }
  a { color: var(--accent); text-decoration: none; }
  a:hover { text-decoration: underline; }
  .container { max-width: 960px; margin: 0 auto; padding: 0 20px; }
  nav { background: var(--surface); border-bottom: 1px solid var(--border); padding: 12px 0; }
  nav .container { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
  nav .brand { font-weight: 700; font-size: 15px; color: var(--text); }
  nav .brand:hover { text-decoration: none; }
  header { padding: 48px 0 32px; text-align: center; }
  header h1 { font-size: 2.2rem; font-weight: 800; margin-bottom: 12px; }
  header p { color: var(--muted); font-size: 1.05rem; max-width: 600px; margin: 0 auto; }
  .stats { display: flex; gap: 24px; justify-content: center; flex-wrap: wrap; margin-top: 24px; }
  .stat { text-align: center; }
  .stat .num { font-size: 1.8rem; font-weight: 700; color: var(--accent); }
  .stat .lbl { font-size: 0.8rem; color: var(--muted); text-transform: uppercase; letter-spacing: .05em; }
  .filters { margin: 24px 0 16px; display: flex; gap: 8px; flex-wrap: wrap; }
  .filter-btn { background: var(--surface); border: 1px solid var(--border); color: var(--muted); padding: 6px 14px; border-radius: 20px; cursor: pointer; font-size: 13px; transition: all .15s; }
  .filter-btn:hover, .filter-btn.active { background: var(--accent); border-color: var(--accent); color: #fff; }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; padding-bottom: 48px; }
  .card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 20px; transition: border-color .15s, transform .15s; display: flex; flex-direction: column; }
  .card:hover { border-color: var(--accent); transform: translateY(-2px); }
  .card-cat { font-size: 12px; color: var(--muted); margin-bottom: 10px; }
  .card-tools { display: flex; align-items: center; gap: 10px; margin-bottom: 14px; }
  .card-tools .tool { font-weight: 600; font-size: 14px; }
  .card-tools .vs { color: var(--muted); font-size: 12px; }
  .card-savings { font-size: 12px; color: var(--green); margin-bottom: 14px; }
  .card .btn-row { display: flex; gap: 6px; margin-top: auto; }
  .card a.btn { display: inline-block; background: var(--accent); color: #fff; padding: 7px 16px; border-radius: 6px; font-size: 13px; font-weight: 600; text-align: center; }
  .card a.btn-alt { display: inline-block; background: rgba(63,185,80,.15); color: var(--green); padding: 7px 12px; border-radius: 6px; font-size: 12px; font-weight: 600; text-align: center; border: 1px solid rgba(63,185,80,.3); }
  .card a.btn:hover, .card a.btn-alt:hover { opacity: 0.85; text-decoration: none; }
  h2 { font-size: 1.4rem; margin: 32px 0 16px; }
  h3 { font-size: 1.1rem; margin: 24px 0 10px; }
  .badge { display: inline-block; padding: 2px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; margin: 0 4px 4px 0; }
  .badge-green { background: rgba(63,185,80,.15); color: var(--green); border: 1px solid rgba(63,185,80,.3); }
  .badge-blue { background: rgba(88,166,255,.15); color: var(--accent); border: 1px solid rgba(88,166,255,.3); }
  .badge-yellow { background: rgba(210,153,34,.15); color: var(--yellow); border: 1px solid rgba(210,153,34,.3); }
  table { width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 14px; }
  th { background: var(--surface); color: var(--muted); text-align: left; padding: 10px 14px; border-bottom: 2px solid var(--border); }
  td { padding: 9px 14px; border-bottom: 1px solid var(--border); }
  tr:hover td { background: rgba(255,255,255,.02); }
  .verdict-box { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 20px; margin: 20px 0; }
  .verdict-row { margin-bottom: 14px; }
  .verdict-row:last-child { margin-bottom: 0; }
  .verdict-label { font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: .05em; margin-bottom: 4px; }
  .verdict-switch .verdict-label { color: var(--green); }
  .verdict-stay .verdict-label { color: var(--yellow); }
  .hero-tools { display: flex; gap: 16px; align-items: center; background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 20px; margin: 24px 0; flex-wrap: wrap; }
  .hero-tool { flex: 1; min-width: 160px; }
  .hero-tool .label { font-size: 11px; color: var(--muted); margin-bottom: 4px; text-transform: uppercase; }
  .hero-tool .name { font-size: 1.2rem; font-weight: 700; }
  .hero-tool .price { font-size: 13px; color: var(--muted); margin-top: 4px; }
  .hero-vs { font-size: 1.4rem; font-weight: 700; color: var(--border); }
  ul.diffs { padding-left: 20px; }
  ul.diffs li { margin-bottom: 8px; }
  .migration-box { background: var(--surface); border: 1px solid var(--border); border-left: 3px solid var(--accent); border-radius: var(--radius); padding: 20px; margin: 20px 0; font-size: 14px; }
  .migration-box pre { background: var(--bg); border: 1px solid var(--border); border-radius: 6px; padding: 12px; margin-top: 12px; overflow-x: auto; font-size: 13px; white-space: pre-wrap; }
  .related { display: flex; gap: 10px; flex-wrap: wrap; margin: 16px 0; }
  .related a { background: var(--surface); border: 1px solid var(--border); padding: 8px 14px; border-radius: 6px; font-size: 13px; }
  .related a:hover { border-color: var(--accent); text-decoration: none; }
  .alt-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 14px; margin: 20px 0; }
  .alt-card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 18px; display: flex; flex-direction: column; gap: 10px; transition: border-color .15s; }
  .alt-card:hover { border-color: var(--green); }
  .alt-card .alt-name { font-size: 1.1rem; font-weight: 700; color: var(--green); }
  .alt-card .alt-price { font-size: 12px; color: var(--muted); }
  .alt-card .alt-links { display: flex; gap: 8px; margin-top: auto; }
  .alt-card .alt-links a { flex: 1; text-align: center; padding: 6px 10px; border-radius: 5px; font-size: 12px; font-weight: 600; }
  .btn-compare { background: var(--accent); color: #fff !important; }
  .btn-migrate { background: rgba(63,185,80,.15); color: var(--green) !important; border: 1px solid rgba(63,185,80,.3); }
  .step-list { list-style: none; padding: 0; counter-reset: steps; }
  .step-list li { counter-increment: steps; display: flex; gap: 14px; padding: 14px 0; border-bottom: 1px solid var(--border); }
  .step-list li:last-child { border-bottom: none; }
  .step-list li::before { content: counter(steps); background: var(--accent); color: #fff; border-radius: 50%; width: 28px; height: 28px; font-size: 13px; font-weight: 700; display: flex; align-items: center; justify-content: center; flex-shrink: 0; margin-top: 2px; }
  footer { border-top: 1px solid var(--border); padding: 32px 0; text-align: center; font-size: 13px; color: var(--muted); }
  footer a { color: var(--muted); }
  .search-bar { width: 100%; max-width: 500px; margin: 16px auto 0; display: block; background: var(--surface); border: 1px solid var(--border); border-radius: 8px; color: var(--text); padding: 10px 16px; font-size: 14px; }
  .search-bar:focus { outline: none; border-color: var(--accent); }
  @media (max-width: 600px) { header h1 { font-size: 1.5rem; } .hero-tools { flex-direction: column; } }
</style>"""

GA_SNIPPET = f"""<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA_ID}');</script>"""

# ─────────────────────────────────────────────────────────────────────────────
# NAV + FOOTER
# ─────────────────────────────────────────────────────────────────────────────

def nav(root=""):
    return f"""<nav>
  <div class="container">
    <a href="{root}index.html" class="brand">🤖 AI Tool Alternative Finder</a>
    <a href="{root}savings-calculator/index.html" style="font-size:13px;color:var(--muted)">💰 Calculator</a>
    <a href="{root}changelog/index.html" style="font-size:13px;color:var(--muted)">📋 Changelog</a>
    <a href="{root}stats/index.html" style="font-size:13px;color:var(--muted)">📊 Stats</a>
    <a href="{root}blog/index.html" style="font-size:13px;color:var(--muted)">📝 Blog</a>
    <a href="{root}about/index.html" style="font-size:13px;color:var(--muted)">About</a>
  </div>
</nav>"""

def footer_html(root=""):
    return f"""<footer>
  <div class="container">
    <p><strong>AI Tool Alternative Finder</strong> &nbsp;·&nbsp;
    <a href="{root}about/index.html">About</a> &nbsp;·&nbsp;
    <a href="{root}privacy/index.html">Privacy Policy</a> &nbsp;·&nbsp;
    <a href="{root}contact/index.html">Contact</a> &nbsp;·&nbsp;
    <a href="{root}changelog/index.html">Changelog</a> &nbsp;·&nbsp;
    <a href="{root}stats/index.html">Stats</a></p>
    <p style="margin-top:8px">Updated {BUILD_DATE} &nbsp;·&nbsp; $0/month to operate &nbsp;·&nbsp; AI-generated content for informational purposes only</p>
  </div>
</footer>"""

# ─────────────────────────────────────────────────────────────────────────────
# PAGE SHELL — Schema.org, OG, Twitter Card, GA4
# ─────────────────────────────────────────────────────────────────────────────

def page_shell(title, desc, body, root="", canonical="", schema="", keywords="", page_type="website"):
    can  = f'<link rel="canonical" href="{SITE_URL}/{canonical}" />' if canonical else ""
    kw   = f'<meta name="keywords" content="{keywords}" />' if keywords else ""
    sc   = f'<script type="application/ld+json">\n{schema}\n</script>' if schema else ""
    og_t = "article" if page_type == "article" else "website"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  {kw}
  {can}
  <meta name="robots" content="index, follow" />
  <meta property="og:type" content="{og_t}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="{SITE_URL}/{canonical}" />
  <meta property="og:site_name" content="{SITE_TITLE}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{desc}" />
  {sc}
  {CSS}
  {GA_SNIPPET}
</head>
<body>
{nav(root)}
{body}
{footer_html(root)}
<script>
  document.querySelectorAll('.filter-btn').forEach(btn => {{
    btn.addEventListener('click', () => {{
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const cat = btn.dataset.cat;
      document.querySelectorAll('.card[data-cat]').forEach(c => {{
        c.style.display = (cat === 'all' || c.dataset.cat === cat) ? '' : 'none';
      }});
    }});
  }});
  const sb = document.querySelector('.search-bar');
  if (sb) sb.addEventListener('input', () => {{
    const q = sb.value.toLowerCase();
    document.querySelectorAll('.card[data-cat]').forEach(c => {{
      c.style.display = c.textContent.toLowerCase().includes(q) ? '' : 'none';
    }});
  }});
</script>
</body>
</html>"""

# ─────────────────────────────────────────────────────────────────────────────
# INDEX
# ─────────────────────────────────────────────────────────────────────────────

def build_index():
    filters = '<button class="filter-btn active" data-cat="all">All</button>'
    for cat in CATEGORIES:
        emoji = next(c["category_emoji"] for c in COMPARISONS if c["category"] == cat)
        filters += f'<button class="filter-btn" data-cat="{cat}">{emoji} {cat} ({category_count(cat)})</button>'

    unique_paid = len(set(c["paid_tool"] for c in COMPARISONS))
    cards = ""
    for c in COMPARISONS:
        pk = paid_key(c)
        cards += f"""
<div class="card" data-cat="{c['category']}">
  <div class="card-cat">{c['category_emoji']} {c['category']}</div>
  <div class="card-tools">
    <span class="tool">{c['paid_tool']}</span>
    <span class="vs">VS</span>
    <span class="tool">{c['free_tool']}</span>
  </div>
  <div class="card-savings">💰 {c['savings']}</div>
  <div class="btn-row">
    <a href="{c['slug']}/index.html" class="btn" style="flex:2">Compare →</a>
    <a href="alternatives-to-{pk}/index.html" class="btn-alt" style="flex:1">All Alts</a>
  </div>
</div>"""

    schema = f'''{{"@context":"https://schema.org","@type":"WebSite","name":"{SITE_TITLE}","url":"{SITE_URL}/","description":"{SITE_DESC}"}}'''
    body = f"""
<header>
  <div class="container">
    <h1>🤖 AI Tool Alternative Finder</h1>
    <p>{SITE_DESC}</p>
    <div class="stats">
      <div class="stat"><div class="num">{len(COMPARISONS)}</div><div class="lbl">Comparisons</div></div>
      <div class="stat"><div class="num">{unique_paid}</div><div class="lbl">Tools Covered</div></div>
      <div class="stat"><div class="num">$0</div><div class="lbl">Cost to Run</div></div>
      <div class="stat"><div class="num">Daily</div><div class="lbl">Auto-Updated</div></div>
    </div>
    <input type="text" class="search-bar" placeholder="Search AI tools (e.g. ChatGPT, Midjourney, Copilot)..." />
  </div>
</header>
<div class="container">
  <div style="background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:20px;margin-bottom:24px">
    <strong>💰 AI Tool Savings Calculator</strong>
    <p style="color:var(--muted);font-size:13px;margin-top:6px">Enter your team size → see exactly how much you save</p>
    <a href="savings-calculator/index.html" style="display:inline-block;margin-top:12px;background:var(--accent);color:#fff;padding:8px 18px;border-radius:6px;font-size:13px;font-weight:600">Calculate My Savings →</a>
  </div>
  <div class="filters">{filters}</div>
  <div class="grid">{cards}</div>
</div>"""
    write("index.html", page_shell(SITE_TITLE, SITE_DESC, body, canonical="", schema=schema,
          keywords="AI tool alternatives, free AI tools, ChatGPT alternative, Midjourney alternative"))

# ─────────────────────────────────────────────────────────────────────────────
# COMPARISON PAGES
# ─────────────────────────────────────────────────────────────────────────────

def build_comparison(c):
    pk = paid_key(c)
    fk = free_key(c)
    diffs = "".join(f"<li>{d}</li>" for d in (c.get("key_differences") or []))

    pt = c.get("pricing_table", {})
    headers = "".join(f"<th>{h}</th>" for h in (pt.get("headers") or ["Aspect", c["paid_tool"], c["free_tool"]]))
    rows    = "".join("<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in (pt.get("rows") or []))

    github_block = ""
    if c.get("github_repo"):
        github_block = f"""<div style="background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:16px;margin:20px 0">
  📦 <strong>{c['free_tool']} on GitHub</strong><br/>
  <a href="https://github.com/{c['github_repo']}" target="_blank" rel="noopener">github.com/{c['github_repo']}</a>
</div>"""

    related_links = ""
    for slug in (c.get("related") or []):
        rel = next((x for x in COMPARISONS if x["slug"] == slug), None)
        if rel:
            related_links += f'<a href="../{slug}/index.html">{rel["paid_tool"]} vs {rel["free_tool"]}</a>'

    schema = f'''{{"@context":"https://schema.org","@graph":[{{"@type":"Article","headline":"{c['paid_tool']} vs {c['free_tool']}","dateModified":"{BUILD_DATE_ISO}","publisher":{{"@type":"Organization","name":"{SITE_TITLE}","url":"{SITE_URL}"}}}},{{"@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"{SITE_URL}/"}},{{"@type":"ListItem","position":2,"name":"{c['paid_tool']} vs {c['free_tool']}","item":"{SITE_URL}/{c['slug']}/"}}]}}]}}'''

    setup_diff  = c.get("setup_difficulty", "Medium")
    setup_dots  = c.get("setup_dots", "●●●○○")
    setup_time  = c.get("setup_time", "varies")
    setup_method= c.get("setup_method", "varies")

    body = f"""<div class="container" style="padding-top:24px">
  <p style="font-size:13px;color:var(--muted);margin-bottom:16px">
    <a href="../index.html">🤖 Home</a> /
    <a href="../alternatives-to-{pk}/index.html">Alternatives to {c['paid_tool']}</a> /
    {c['paid_tool']} vs {c['free_tool']}
  </p>
  <div style="font-size:12px;color:var(--muted);margin-bottom:8px">{c.get('category_emoji','')} {c.get('category','')}</div>
  <h1 style="font-size:1.8rem;margin-bottom:12px">{c['paid_tool']} vs {c['free_tool']}</h1>
  <p style="color:var(--muted);margin-bottom:16px">Detailed comparison: pricing, features, setup, and which is right for you.</p>
  <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:20px">
    <span class="badge badge-green">✅ Free: {c['free_price']}</span>
    <span class="badge badge-blue">🤖 AI-Analyzed</span>
    <span class="badge badge-yellow">🖥️ Setup: {setup_diff}</span>
    <span class="badge badge-blue">📅 {BUILD_DATE}</span>
  </div>
  <div class="hero-tools">
    <div class="hero-tool">
      <div class="label">Paid Tool</div>
      <div class="name">{c['paid_tool']}</div>
      <div class="price">{c['paid_price']}</div>
      <a href="{c['paid_url']}" target="_blank" rel="noopener" style="font-size:12px;color:var(--muted)">Visit →</a>
    </div>
    <div class="hero-vs">VS</div>
    <div class="hero-tool">
      <div class="label">Free Alternative ✅</div>
      <div class="name">{c['free_tool']}</div>
      <div class="price">{c['free_price']}</div>
      <a href="{c['free_url']}" target="_blank" rel="noopener" style="font-size:12px;color:var(--muted)">Visit →</a>
    </div>
  </div>
  <div class="verdict-box">
    <h3>🤖 AI Verdict</h3>
    <div class="verdict-row verdict-switch">
      <div class="verdict-label">✅ Switch to {c['free_tool']} if</div>
      <div>{c.get('verdict_switch','')}</div>
    </div>
    <div class="verdict-row verdict-stay">
      <div class="verdict-label">⚠️ Stay with {c['paid_tool']} if</div>
      <div>{c.get('verdict_stay','')}</div>
    </div>
    <div style="margin-top:14px;border-top:1px solid var(--border);padding-top:14px;font-size:13px">
      🖥️ <strong>Setup:</strong> {setup_diff} &nbsp;·&nbsp;
      <span style="letter-spacing:3px;color:var(--accent)">{setup_dots}</span> &nbsp;·&nbsp;
      ⏱️ {setup_time} &nbsp;·&nbsp; 🐳 {setup_method}
    </div>
  </div>
  <h2>Overview</h2>
  <p>{c.get('overview','')}</p>
  <h2>Key Differences</h2>
  <ul class="diffs">{diffs}</ul>
  <h2>Pricing Comparison</h2>
  <table><thead><tr>{headers}</tr></thead><tbody>{rows}</tbody></table>
  <h2>Migration Path</h2>
  <div class="migration-box">
    <strong>How to switch from {c['paid_tool']} to {c['free_tool']}:</strong>
    <pre>{c.get('migration','')}</pre>
  </div>
  {github_block}
  <div style="background:var(--surface);border:1px solid rgba(63,185,80,.3);border-radius:8px;padding:16px;margin:20px 0;display:flex;gap:10px;flex-wrap:wrap;align-items:center">
    <span style="color:var(--green);font-size:13px;font-weight:600">📦 Ready to switch?</span>
    <a href="../migrate-{pk}-to-{fk}/index.html" style="background:rgba(63,185,80,.15);color:var(--green);padding:6px 14px;border-radius:6px;font-size:13px;font-weight:600;border:1px solid rgba(63,185,80,.3)">Step-by-Step Migration Guide →</a>
    <a href="../alternatives-to-{pk}/index.html" style="background:var(--surface);color:var(--accent);padding:6px 14px;border-radius:6px;font-size:13px;font-weight:600;border:1px solid var(--border)">All {c['paid_tool']} Alternatives →</a>
  </div>
  <p style="margin:20px 0;font-size:13px;color:var(--muted)"><em>Data sourced {BUILD_DATE}. Verify at official websites before making decisions.</em></p>
  <h3>🔗 Related</h3>
  <div class="related">{related_links}</div>
  <p style="margin:20px 0"><a href="../index.html" style="color:var(--muted);font-size:13px">← All Comparisons</a></p>
</div>"""

    desc = f"Is {c['free_tool']} a good free alternative to {c['paid_tool']}? {c['savings']}. Detailed comparison with pricing, features, and migration guide."
    write(f"{c['slug']}/index.html", page_shell(
        f"{c['paid_tool']} vs {c['free_tool']} ({BUILD_DATE[:4]}) — Free AI Alternative",
        desc, body, root="../", canonical=f"{c['slug']}/",
        schema=schema, page_type="article",
        keywords=f"{c['paid_tool']} alternative, free {c['paid_tool']}, {c['free_tool']} vs {c['paid_tool']}"
    ))

# ─────────────────────────────────────────────────────────────────────────────
# MIGRATION PAGES
# ─────────────────────────────────────────────────────────────────────────────

def build_migration(c):
    pk   = paid_key(c)
    fk   = free_key(c)
    slug = f"migrate-{pk}-to-{fk}"
    raw  = c.get("migration", "")

    steps = []
    for line in raw.replace(". ", ".\n").split("\n"):
        line = line.strip().lstrip("0123456789. ").strip()
        if len(line) > 20:
            steps.append(line)
    if not steps:
        steps = [raw]

    steps_html = "".join(f"<li><span>{s}</span></li>" for s in steps)
    steps_schema = ", ".join(f'{{"@type":"HowToStep","text":"{s.replace(chr(34),chr(39))}"}}' for s in steps[:8])
    schema = f'''{{"@context":"https://schema.org","@type":"HowTo","name":"How to Migrate from {c['paid_tool']} to {c['free_tool']}","description":"Step-by-step migration guide. Save {c['paid_price']}.","step":[{steps_schema}]}}'''

    body = f"""<div class="container" style="padding-top:24px">
  <p style="font-size:13px;color:var(--muted);margin-bottom:16px">
    <a href="../index.html">🤖 Home</a> /
    <a href="../{c['slug']}/index.html">{c['paid_tool']} vs {c['free_tool']}</a> /
    Migration Guide
  </p>
  <div style="font-size:12px;color:var(--muted);margin-bottom:8px">📦 Migration Guide</div>
  <h1 style="font-size:1.8rem;margin-bottom:16px">Migrate from {c['paid_tool']} to {c['free_tool']}</h1>
  <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:24px">
    <span class="badge badge-green">💰 Save {c['paid_price']}</span>
    <span class="badge badge-blue">⏱️ {c.get('setup_time','varies')}</span>
    <span class="badge badge-blue">📅 {BUILD_DATE}</span>
  </div>
  <div style="background:rgba(63,185,80,.08);border:1px solid rgba(63,185,80,.3);border-radius:8px;padding:20px;margin-bottom:24px">
    <strong style="color:var(--green)">💰 Why switch?</strong>
    <p style="margin-top:8px;font-size:14px">{c['paid_tool']} costs <strong>{c['paid_price']}</strong>. {c['free_tool']} is <strong>{c['free_price']}</strong>.</p>
  </div>
  <h2>Migration Steps</h2>
  <div class="migration-box">
    <ul class="step-list">{steps_html}</ul>
  </div>
  <div style="display:flex;gap:12px;flex-wrap:wrap;margin:24px 0">
    <a href="{c['free_url']}" target="_blank" rel="noopener" style="background:rgba(63,185,80,.15);color:var(--green);padding:10px 20px;border-radius:6px;font-weight:600;font-size:14px;border:1px solid rgba(63,185,80,.3)">Set Up {c['free_tool']} →</a>
    <a href="../{c['slug']}/index.html" style="background:var(--surface);color:var(--accent);padding:10px 20px;border-radius:6px;font-weight:600;font-size:14px;border:1px solid var(--border)">Full Comparison →</a>
  </div>
  <p style="margin-top:24px;font-size:13px;color:var(--muted)"><em>Steps are AI-generated. Verify with official documentation before proceeding.</em></p>
  <p style="margin-top:16px"><a href="../index.html" style="color:var(--muted);font-size:13px">← All Comparisons</a></p>
</div>"""

    desc = f"Step-by-step guide to migrating from {c['paid_tool']} to {c['free_tool']}. Save {c['paid_price']}. Setup: {c.get('setup_time','varies')}."
    write(f"{slug}/index.html", page_shell(
        f"Migrate from {c['paid_tool']} to {c['free_tool']} ({BUILD_DATE[:4]})",
        desc, body, root="../", canonical=f"{slug}/",
        schema=schema, page_type="article",
        keywords=f"migrate {c['paid_tool']} to {c['free_tool']}, switch from {c['paid_tool']}, {c['free_tool']} setup guide"
    ))
    return slug

# ─────────────────────────────────────────────────────────────────────────────
# ALTERNATIVES-TO PAGES
# ─────────────────────────────────────────────────────────────────────────────

def build_alternatives_to(paid_tool_name, comps):
    pk   = paid_key(comps[0])
    slug = f"alternatives-to-{pk}"

    alt_cards = ""
    items = []
    for i, c in enumerate(comps, 1):
        fk = free_key(c)
        alt_cards += f"""<div class="alt-card">
  <div class="alt-name">{c['free_tool']}</div>
  <div class="alt-price">{c['free_price']}</div>
  <div style="font-size:12px;color:var(--muted)">Setup: {c.get('setup_difficulty','Medium')} · {c.get('setup_time','varies')}</div>
  <div style="font-size:13px;color:var(--muted);margin-top:4px">{(c.get('verdict_switch') or '')[:100]}...</div>
  <div class="alt-links">
    <a href="../{c['slug']}/index.html" class="btn-compare">Compare →</a>
    <a href="../migrate-{pk}-to-{fk}/index.html" class="btn-migrate">Migrate →</a>
  </div>
</div>"""
        items.append(f'{{"@type":"ListItem","position":{i},"name":"{c["free_tool"]}","url":"{SITE_URL}/{c["slug"]}/"}}')

    schema = f'''{{"@context":"https://schema.org","@type":"ItemList","name":"Best Free Alternatives to {paid_tool_name}","numberOfItems":{len(comps)},"itemListElement":[{", ".join(items)}]}}'''

    body = f"""<div class="container" style="padding-top:24px">
  <p style="font-size:13px;color:var(--muted);margin-bottom:16px">
    <a href="../index.html">🤖 Home</a> / Alternatives to {paid_tool_name}
  </p>
  <h1 style="font-size:1.8rem;margin-bottom:12px">Best Free Alternatives to {paid_tool_name}</h1>
  <p style="color:var(--muted);margin-bottom:20px">We compared <strong>{len(comps)} free alternative{'s' if len(comps)>1 else ''}</strong> to {paid_tool_name} — with pricing, setup difficulty, and step-by-step migration guides.</p>
  <div style="background:rgba(63,185,80,.08);border:1px solid rgba(63,185,80,.3);border-radius:8px;padding:16px;margin-bottom:24px">
    <strong style="color:var(--green)">💰 Why switch from {paid_tool_name}?</strong>
    <p style="margin-top:6px;font-size:14px">{paid_tool_name} costs {comps[0]['paid_price']}. Every alternative below is free or dramatically cheaper.</p>
  </div>
  <div class="alt-grid">{alt_cards}</div>
  <p style="margin-top:32px;font-size:13px;color:var(--muted)"><em>Data sourced {BUILD_DATE}. Verify current pricing at official websites.</em></p>
  <p style="margin-top:16px"><a href="../index.html" style="color:var(--muted);font-size:13px">← All Comparisons</a></p>
</div>"""

    desc = f"The {len(comps)} best free alternatives to {paid_tool_name} in {BUILD_DATE[:4]}. Detailed comparisons with pricing, setup guides, and migration paths."
    write(f"{slug}/index.html", page_shell(
        f"Best Free Alternatives to {paid_tool_name} ({BUILD_DATE[:4]})",
        desc, body, root="../", canonical=f"{slug}/", schema=schema,
        keywords=f"alternatives to {paid_tool_name}, free {paid_tool_name}, {paid_tool_name} replacement"
    ))
    return slug

# ─────────────────────────────────────────────────────────────────────────────
# SAVINGS CALCULATOR
# ─────────────────────────────────────────────────────────────────────────────

def build_calculator():
    tool_rows = "".join(
        f"<tr><td>{c['paid_tool']}</td><td>{c['paid_price']}</td><td style='color:var(--green)'>{c['free_tool']} — {c['free_price']}</td></tr>"
        for c in COMPARISONS
    )
    tools_json = json.dumps([{"name": c["paid_tool"], "free": c["free_tool"], "slug": c["slug"]} for c in COMPARISONS])
    body = f"""<header><div class="container"><h1>💰 AI Tool Savings Calculator</h1><p>See how much you save switching from paid AI tools to free alternatives</p></div></header>
<div class="container">
  <div style="background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:24px;margin-bottom:32px;max-width:600px">
    <label style="display:block;margin-bottom:8px;font-weight:600">Team / Seat Count</label>
    <input id="seats" type="number" value="5" min="1" style="width:100%;background:var(--bg);border:1px solid var(--border);color:var(--text);padding:10px;border-radius:6px;font-size:16px" />
    <div style="margin-top:20px;display:grid;gap:12px" id="results"></div>
  </div>
  <h2>All Free Alternatives</h2>
  <table><thead><tr><th>Paid AI Tool</th><th>Paid Price</th><th>Free Alternative</th></tr></thead><tbody>{tool_rows}</tbody></table>
  <p style="margin-top:32px"><a href="../index.html">← All Comparisons</a></p>
</div>
<script>
const tools={tools_json};
const savings=[
  {{name:'ChatGPT Plus',monthly:20,per:'flat'}},
  {{name:'GitHub Copilot',monthly:10,per:'seat'}},
  {{name:'Midjourney',monthly:30,per:'flat'}},
  {{name:'ElevenLabs',monthly:22,per:'flat'}},
  {{name:'Jasper AI',monthly:49,per:'flat'}},
  {{name:'Cursor AI',monthly:20,per:'seat'}},
  {{name:'Otter.ai',monthly:10,per:'seat'}},
  {{name:'Grammarly Premium',monthly:13,per:'seat'}},
  {{name:'Runway ML',monthly:35,per:'flat'}},
  {{name:'Perplexity Pro',monthly:20,per:'flat'}},
];
function calc(){{
  const seats=parseInt(document.getElementById('seats').value)||1;
  let html='',total=0;
  savings.forEach(t=>{{
    const m=t.per==='seat'?t.monthly*seats:t.monthly;
    total+=m;
    html+=`<div style="display:flex;justify-content:space-between;background:var(--bg);padding:10px 14px;border-radius:6px"><span>${{t.name}}</span><span style="color:var(--green)">Save ${{m.toLocaleString()}}/mo</span></div>`;
  }});
  html=`<div style="background:rgba(63,185,80,.1);border:1px solid rgba(63,185,80,.3);border-radius:8px;padding:16px;text-align:center;margin-bottom:16px"><div style="font-size:2rem;font-weight:800;color:var(--green)">${{total.toLocaleString()}}/month</div><div style="color:var(--muted);font-size:13px">Estimated savings for ${{seats}} seat(s)</div></div>`+html;
  document.getElementById('results').innerHTML=html;
}}
document.getElementById('seats').addEventListener('input',calc);
calc();
</script>"""
    write("savings-calculator/index.html", page_shell(
        f"AI Tool Savings Calculator — {SITE_TITLE}",
        "Calculate how much you save switching from paid AI tools to free alternatives.",
        body, root="../", canonical="savings-calculator/"
    ))

# ─────────────────────────────────────────────────────────────────────────────
# CHANGELOG
# ─────────────────────────────────────────────────────────────────────────────

def build_changelog():
    rows = "".join(
        "<tr><td>" + c.get('category_emoji','') + ' ' + c.get('category','') + "</td>"
        "<td><strong>" + c['paid_tool'] + "</strong></td>"
        "<td><strong style='color:var(--green)'>" + c['free_tool'] + "</strong></td>"
        "<td style='color:var(--green);font-size:12px'>" + c['savings'] + "</td>"
        "<td style='font-size:12px'><a href='../" + c['slug'] + "/index.html'>Compare →</a> &nbsp;"
        "<a href='../migrate-" + paid_key(c) + "-to-" + free_key(c) + "/index.html' style='color:var(--green)'>Migrate →</a></td></tr>"
        for c in COMPARISONS
    )
    body = f"""<header><div class="container">
  <h1>📋 Weekly Changelog</h1>
  <p>All {len(COMPARISONS)} comparisons auto-updated daily.</p>
  <div class="stats">
    <div class="stat"><div class="num">{len(COMPARISONS)}</div><div class="lbl">Comparisons</div></div>
    <div class="stat"><div class="num">{len(COMPARISONS)}</div><div class="lbl">Migration Guides</div></div>
    <div class="stat"><div class="num">{len(CATEGORIES)}</div><div class="lbl">Categories</div></div>
    <div class="stat"><div class="num">$0</div><div class="lbl">Cost to Run</div></div>
  </div>
</div></header>
<div class="container">
  <div style="background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:20px;margin:24px 0">
    <h2 style="margin:0 0 12px">🟢 Latest Update — {BUILD_DATE}</h2>
    <ul style="padding-left:20px;color:var(--muted);font-size:14px;line-height:2">
      <li>All {len(COMPARISONS)} comparison pages refreshed</li>
      <li>All {len(COMPARISONS)} migration guides updated</li>
      <li>Alternatives-to pages regenerated</li>
      <li>Sitemap updated</li>
    </ul>
  </div>
  <table><thead><tr><th>Category</th><th>Paid Tool</th><th>Free Alternative</th><th>Savings</th><th>Links</th></tr></thead><tbody>{rows}</tbody></table>
  <p style="margin-top:32px"><a href="../index.html">← All Comparisons</a></p>
</div>"""
    write("changelog/index.html", page_shell(
        f"Changelog — {SITE_TITLE}",
        f"All {len(COMPARISONS)} AI tool comparisons auto-updated daily.",
        body, root="../", canonical="changelog/"
    ))

# ─────────────────────────────────────────────────────────────────────────────
# STATS
# ─────────────────────────────────────────────────────────────────────────────

def build_stats():
    by_cat = {}
    for c in COMPARISONS:
        by_cat.setdefault(c["category"], []).append(c)
    cat_rows = "".join(
        f"<tr><td>{next(x['category_emoji'] for x in v)} {k}</td><td>{len(v)}</td><td>{len(v)}</td></tr>"
        for k, v in sorted(by_cat.items())
    )
    unique_paid = len(set(c["paid_tool"] for c in COMPARISONS))
    body = f"""<header><div class="container"><h1>📊 Site Statistics</h1><p>Live stats — updated {BUILD_DATE}</p></div></header>
<div class="container">
  <div class="stats" style="justify-content:flex-start;margin:24px 0">
    <div class="stat"><div class="num">{len(COMPARISONS)}</div><div class="lbl">Comparisons</div></div>
    <div class="stat"><div class="num">{len(COMPARISONS)}</div><div class="lbl">Migration Guides</div></div>
    <div class="stat"><div class="num">{unique_paid}</div><div class="lbl">Alternatives-to Pages</div></div>
    <div class="stat"><div class="num">{len(CATEGORIES)}</div><div class="lbl">Categories</div></div>
    <div class="stat"><div class="num">$0</div><div class="lbl">Monthly Cost</div></div>
  </div>
  <h2>Coverage by Category</h2>
  <table><thead><tr><th>Category</th><th>Comparisons</th><th>Migration Guides</th></tr></thead><tbody>{cat_rows}</tbody></table>
  <div style="background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:16px;margin-top:24px">
    <strong>📎 Cite This Data</strong>
    <p style="color:var(--muted);font-size:13px;margin-top:6px">Free to cite with attribution: <em>AI Tool Alternative Finder ({BUILD_DATE}). Retrieved from {SITE_URL}/stats/</em></p>
  </div>
  <p style="margin-top:32px"><a href="../index.html">← Home</a></p>
</div>"""
    write("stats/index.html", page_shell(f"Stats — {SITE_TITLE}", "Statistics for AI Tool Alternative Finder.", body, root="../", canonical="stats/"))

# ─────────────────────────────────────────────────────────────────────────────
# BLOG
# ─────────────────────────────────────────────────────────────────────────────

BLOG_POSTS = [
    {"slug":"chatgpt-alternatives","title":f"7 Free ChatGPT Alternatives That Work in {BUILD_DATE[:4]}","intro":"ChatGPT Plus costs $20/month. Here are the best free alternatives — and when each one makes sense.","comps":["chatgpt-plus-vs-openrouter","chatgpt-plus-vs-mistral-free"],"tags":["AI Chat","ChatGPT","Free"]},
    {"slug":"github-copilot-alternatives","title":f"GitHub Copilot Is $10/Month — These Free Alternatives Are Almost As Good ({BUILD_DATE[:4]})","intro":"We tested three free AI coding assistants that cover the same use cases as GitHub Copilot.","comps":["github-copilot-vs-codeium","github-copilot-vs-continue-dev"],"tags":["AI Coding","Copilot","Free"]},
    {"slug":"midjourney-alternatives","title":f"Best Free Midjourney Alternatives in {BUILD_DATE[:4]} — Tested","intro":"Midjourney costs $10–$60/month. Stable Diffusion runs locally for free. Here's the full breakdown.","comps":["midjourney-vs-stable-diffusion","dalle3-vs-stable-diffusion"],"tags":["AI Image","Midjourney","Stable Diffusion"]},
    {"slug":"free-ai-api-alternatives","title":f"Stop Paying OpenAI Bills — These Free Alternatives Work ({BUILD_DATE[:4]})","intro":"OpenAI API costs add up fast. Ollama and Groq offer free or dramatically cheaper inference.","comps":["openai-api-vs-ollama","openai-api-vs-groq"],"tags":["AI API","OpenAI","Free"]},
    {"slug":"elevenlabs-alternatives","title":f"ElevenLabs vs Free TTS Alternatives: What Works in {BUILD_DATE[:4]}","intro":"ElevenLabs charges $5–$99/month for text-to-speech. Coqui TTS runs locally with no limits.","comps":["elevenlabs-vs-coqui-tts"],"tags":["AI Voice","ElevenLabs","TTS"]},
]

def build_blog():
    comp_by_slug = {c["slug"]: c for c in COMPARISONS}

    post_cards = ""
    for post in BLOG_POSTS:
        tags_html = "".join(f'<span style="background:rgba(88,166,255,.15);color:var(--accent);padding:2px 8px;border-radius:12px;font-size:11px;font-weight:600">{t}</span>' for t in post["tags"])
        post_cards += f"""<div class="card" style="flex-direction:column;gap:10px">
  <div style="display:flex;gap:6px;flex-wrap:wrap">{tags_html}</div>
  <div style="font-weight:700;font-size:15px">{post['title']}</div>
  <div style="font-size:13px;color:var(--muted)">{post['intro']}</div>
  <a href="{post['slug']}/index.html" style="color:var(--accent);font-size:13px;font-weight:600;margin-top:auto">Read →</a>
</div>"""

    blog_body = f"""<header><div class="container"><h1>📝 Blog</h1><p style="color:var(--muted)">Guides on replacing paid AI tools with free alternatives.</p></div></header>
<div class="container"><div class="grid" style="padding-top:24px">{post_cards}</div></div>"""
    write("blog/index.html", page_shell(f"Blog — {SITE_TITLE}", "Guides on switching from paid AI tools to free alternatives.", blog_body, root="../", canonical="blog/"))

    for post in BLOG_POSTS:
        comps = [comp_by_slug[s] for s in post["comps"] if s in comp_by_slug]
        comp_cards = ""
        for c in comps:
            pk = paid_key(c); fk = free_key(c)
            comp_cards += f"""<div style="background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:16px;margin-bottom:12px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px">
  <div><strong>{c['paid_tool']}</strong> <span style="color:var(--muted)">vs</span> <strong style="color:var(--green)">{c['free_tool']}</strong>
  <div style="font-size:12px;color:var(--muted);margin-top:4px">{c['savings']}</div></div>
  <div style="display:flex;gap:6px">
    <a href="../../{c['slug']}/index.html" style="background:var(--accent);color:#fff;padding:5px 12px;border-radius:5px;font-size:12px;font-weight:600">Compare →</a>
    <a href="../../migrate-{pk}-to-{fk}/index.html" style="background:rgba(63,185,80,.15);color:var(--green);padding:5px 12px;border-radius:5px;font-size:12px;font-weight:600;border:1px solid rgba(63,185,80,.3)">Migrate →</a>
  </div>
</div>"""
        tags_html = "".join(f'<span style="background:rgba(88,166,255,.15);color:var(--accent);padding:3px 10px;border-radius:12px;font-size:12px;font-weight:600">{t}</span>' for t in post["tags"])
        schema = f'''{{"@context":"https://schema.org","@type":"Article","headline":"{post['title']}","description":"{post['intro']}","dateModified":"{BUILD_DATE_ISO}","publisher":{{"@type":"Organization","name":"{SITE_TITLE}","url":"{SITE_URL}"}}}}'''
        post_body = f"""<div class="container" style="padding-top:24px">
  <p style="font-size:13px;color:var(--muted);margin-bottom:16px"><a href="../../index.html">🤖 Home</a> / <a href="../index.html">Blog</a></p>
  <div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:12px">{tags_html}</div>
  <h1 style="font-size:1.6rem;margin-bottom:12px">{post['title']}</h1>
  <p style="color:var(--muted);font-size:13px;margin-bottom:24px">📅 {BUILD_DATE} &nbsp;·&nbsp; 🤖 AI-assisted</p>
  <div style="background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:20px;margin-bottom:24px">
    <p style="font-size:15px;line-height:1.7">{post['intro']}</p>
  </div>
  <h2 style="margin-bottom:16px">The Comparisons</h2>
  {comp_cards}
  <div style="background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:20px;margin:24px 0">
    <strong>💰 Calculate your savings</strong>
    <p style="color:var(--muted);font-size:13px;margin-top:6px">Enter your team size and see how much you save.</p>
    <a href="../../savings-calculator/index.html" style="display:inline-block;margin-top:10px;background:var(--accent);color:#fff;padding:7px 16px;border-radius:6px;font-size:13px;font-weight:600">Open Calculator →</a>
  </div>
  <p style="margin-top:20px"><a href="../index.html" style="color:var(--muted);font-size:13px">← All Blog Posts</a></p>
</div>"""
        write(f"blog/{post['slug']}/index.html", page_shell(
            post["title"] + f" — {SITE_TITLE}", post["intro"], post_body,
            root="../../", canonical=f"blog/{post['slug']}/", schema=schema, page_type="article"
        ))

# ─────────────────────────────────────────────────────────────────────────────
# UTILITY PAGES
# ─────────────────────────────────────────────────────────────────────────────

def build_about():
    body = f"""<header><div class="container"><h1>About AI Tool Alternative Finder</h1></div></header>
<div class="container" style="max-width:720px;padding-bottom:48px">
  <h2>What is this?</h2>
  <p>AI Tool Alternative Finder is a free directory comparing popular paid AI tools to free alternatives. Every comparison includes pricing, feature comparisons, setup guides, and migration instructions — auto-updated daily.</p>
  <h2 style="margin-top:24px">How does it work?</h2>
  <p>A Python pipeline runs daily on GitHub Actions: <code>generate.py</code> calls the Groq API (Llama 3.3) to write comparison content, then <code>build.py</code> generates all HTML pages from that data. Total infrastructure cost: $0/month.</p>
  <h2 style="margin-top:24px">Why?</h2>
  <p>AI tool subscriptions add up fast. ChatGPT Plus, Copilot, Midjourney, ElevenLabs together can cost $100–$300/month. Excellent free alternatives exist for almost every use case — this site helps you find them.</p>
  <p style="margin-top:32px"><a href="../index.html">← View All Comparisons</a></p>
</div>"""
    write("about/index.html", page_shell(f"About — {SITE_TITLE}", "About AI Tool Alternative Finder.", body, root="../", canonical="about/"))

def build_privacy():
    body = f"""<header><div class="container"><h1>Privacy Policy</h1></div></header>
<div class="container" style="max-width:720px;padding-bottom:48px">
  <p style="color:var(--muted)">Last updated: {BUILD_DATE}</p>
  <h2>Data Collection</h2>
  <p>AI Tool Alternative Finder uses Google Analytics (GA4) for aggregate traffic analysis and may display Google AdSense ads. We do not collect personal data directly.</p>
  <h2 style="margin-top:24px">Cookies</h2>
  <p>Google Analytics and AdSense use cookies. You can opt out via your browser settings or Google's ad settings.</p>
  <h2 style="margin-top:24px">Content Disclaimer</h2>
  <p>All comparison content is AI-generated for informational purposes. Verify current pricing at official vendor websites before making decisions.</p>
  <p style="margin-top:32px"><a href="../index.html">← Home</a></p>
</div>"""
    write("privacy/index.html", page_shell(f"Privacy Policy — {SITE_TITLE}", "Privacy Policy for AI Tool Alternative Finder.", body, root="../", canonical="privacy/"))

def build_contact():
    body = f"""<header><div class="container"><h1>Contact</h1></div></header>
<div class="container" style="max-width:600px;padding-bottom:48px">
  <p>Suggestions, errors, or outdated pricing? Open a GitHub Issue.</p>
  <div style="background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:24px;margin-top:20px">
    <h2 style="margin-bottom:16px">GitHub Issues</h2>
    <a href="https://github.com/aiopentec/ai-tool-alternative-finder/issues/new" target="_blank"
       style="display:inline-block;background:var(--accent);color:#fff;padding:10px 20px;border-radius:6px;font-weight:600;margin-top:8px;font-size:14px">Open a GitHub Issue →</a>
  </div>
  <p style="margin-top:32px"><a href="../index.html">← Home</a></p>
</div>"""
    write("contact/index.html", page_shell(f"Contact — {SITE_TITLE}", "Contact AI Tool Alternative Finder.", body, root="../", canonical="contact/"))

# ─────────────────────────────────────────────────────────────────────────────
# EXTRA FILES
# ─────────────────────────────────────────────────────────────────────────────

def build_robots():
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")

def build_ads_txt():
    write("ads.txt", "google.com, pub-4633315697698743, DIRECT, f08c47fec0942fa0\n")

def build_404():
    body = f"""<div style="text-align:center;padding:80px 20px">
  <h1 style="font-size:4rem;color:var(--accent)">404</h1>
  <p style="color:var(--muted);margin:16px 0 32px">This page doesn't exist.</p>
  <a href="{SITE_URL}/" style="background:var(--accent);color:#fff;padding:10px 24px;border-radius:6px;font-weight:600">← Back to All Comparisons</a>
</div>"""
    write("404.html", page_shell(f"Page Not Found — {SITE_TITLE}", "Page not found.", body, canonical="404"))

# ─────────────────────────────────────────────────────────────────────────────
# SITEMAP
# ─────────────────────────────────────────────────────────────────────────────

def build_sitemap(migration_slugs, alt_slugs, blog_slugs):
    urls = [
        f"  <url><loc>{SITE_URL}/</loc><changefreq>daily</changefreq><priority>1.0</priority></url>",
        f"  <url><loc>{SITE_URL}/savings-calculator/</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>",
        f"  <url><loc>{SITE_URL}/changelog/</loc><changefreq>daily</changefreq><priority>0.7</priority></url>",
        f"  <url><loc>{SITE_URL}/stats/</loc><changefreq>weekly</changefreq><priority>0.6</priority></url>",
        f"  <url><loc>{SITE_URL}/blog/</loc><changefreq>weekly</changefreq><priority>0.7</priority></url>",
        f"  <url><loc>{SITE_URL}/about/</loc><changefreq>monthly</changefreq><priority>0.5</priority></url>",
        f"  <url><loc>{SITE_URL}/privacy/</loc><changefreq>monthly</changefreq><priority>0.4</priority></url>",
        f"  <url><loc>{SITE_URL}/contact/</loc><changefreq>monthly</changefreq><priority>0.4</priority></url>",
    ]
    for c in COMPARISONS:
        urls.append(f"  <url><loc>{SITE_URL}/{c['slug']}/</loc><changefreq>weekly</changefreq><priority>0.9</priority><lastmod>{BUILD_DATE_ISO}</lastmod></url>")
    for s in migration_slugs:
        urls.append(f"  <url><loc>{SITE_URL}/{s}/</loc><changefreq>monthly</changefreq><priority>0.8</priority><lastmod>{BUILD_DATE_ISO}</lastmod></url>")
    for s in alt_slugs:
        urls.append(f"  <url><loc>{SITE_URL}/{s}/</loc><changefreq>weekly</changefreq><priority>0.9</priority><lastmod>{BUILD_DATE_ISO}</lastmod></url>")
    for s in blog_slugs:
        urls.append(f"  <url><loc>{SITE_URL}/blog/{s}/</loc><changefreq>weekly</changefreq><priority>0.7</priority><lastmod>{BUILD_DATE_ISO}</lastmod></url>")

    write("sitemap.xml",
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "\n".join(urls) + "\n</urlset>")

# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Show data source and exit")
    args = parser.parse_args()

    if args.check:
        if CACHE_DIR.exists() and list(CACHE_DIR.glob("*.json")):
            print(f"✅ Will use AI-generated cache: {len(list(CACHE_DIR.glob('*.json')))} files in {CACHE_DIR}")
        else:
            print(f"📋 Will use hardcoded fallback: {len(FALLBACK_COMPARISONS)} comparisons")
            print(f"   Run 'python scripts/generate.py' to generate AI content")
        return

    paid_groups = {}
    for c in COMPARISONS:
        paid_groups.setdefault(c["paid_tool"], []).append(c)

    unique_paid = len(paid_groups)

    print(f"\n🤖 AI Tool Alternative Finder — Build")
    print(f"   Date:             {BUILD_DATE}")
    print(f"   Comparisons:      {len(COMPARISONS)}")
    print(f"   Categories:       {len(CATEGORIES)}")
    print(f"   Migration pages:  {len(COMPARISONS)}")
    print(f"   Alternatives-to:  {unique_paid}")
    print(f"   Blog posts:       {len(BLOG_POSTS)}")
    estimated = 1 + len(COMPARISONS)*2 + unique_paid + len(BLOG_POSTS) + 1 + 8 + 3
    print(f"   Estimated total:  ~{estimated} files\n")

    print("📄 Building index...")
    build_index()

    print(f"\n📄 Building {len(COMPARISONS)} comparison pages...")
    for c in COMPARISONS:
        build_comparison(c)

    print(f"\n📦 Building {len(COMPARISONS)} migration pages...")
    migration_slugs = [build_migration(c) for c in COMPARISONS]

    print(f"\n🎯 Building {unique_paid} alternatives-to pages...")
    alt_slugs = [build_alternatives_to(name, comps) for name, comps in paid_groups.items()]

    print(f"\n📝 Building blog...")
    build_blog()

    print("\n📄 Building utility pages...")
    build_calculator()
    build_changelog()
    build_stats()
    build_about()
    build_privacy()
    build_contact()

    print("\n📄 Building extra files...")
    build_robots()
    build_ads_txt()
    build_404()

    print("\n🗺️  Building sitemap...")
    build_sitemap(migration_slugs, alt_slugs, [p["slug"] for p in BLOG_POSTS])

    total = (1 + len(COMPARISONS)*2 + len(alt_slugs)
             + len(BLOG_POSTS) + 1 + len(CATEGORIES) + 8 + 3)
    print(f"\n✅ Build complete — {total} files generated\n")

if __name__ == "__main__":
    main()
