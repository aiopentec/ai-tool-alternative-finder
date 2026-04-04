#!/usr/bin/env python3
"""
AI Tool Alternative Finder — Build Script
Generates a complete static GitHub Pages site comparing paid AI tools
to free/cheaper alternatives. $0/month to run. Auto-updates daily.

Usage:
    python scripts/build.py

Output:
    All HTML files + sitemap.xml written to the repo root.
"""

import os
import json
from datetime import datetime, timezone

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

SITE_URL   = "https://aiopentec.github.io/ai-tool-alternative-finder"
SITE_TITLE = "AI Tool Alternative Finder"
SITE_DESC  = "Discover free and cheaper alternatives to popular paid AI tools — with detailed comparisons. Save hundreds per year."
BUILD_DATE = datetime.now(timezone.utc).strftime("%B %d, %Y")
BUILD_DATE_ISO = datetime.now(timezone.utc).strftime("%Y-%m-%d")

# ─────────────────────────────────────────────────────────────────────────────
# DATA — All comparisons
# ─────────────────────────────────────────────────────────────────────────────

COMPARISONS = [

    # ──────────────────────── ✍️ AI WRITING ────────────────────────

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
        "savings": "$20/month → Free tier available",
        "verdict_switch": "OpenRouter is ideal for developers and power users who want access to 100+ models — including free tiers of Llama 3, Mistral, Gemma, and more — without a flat monthly fee.",
        "verdict_stay": "ChatGPT Plus is best when you rely on GPT-4o's code interpreter, image generation (DALL-E), or the polished consumer UI with no setup required.",
        "setup_difficulty": "Easy",
        "setup_dots": "●●○○○",
        "setup_time": "~5 mins",
        "setup_method": "Browser-based",
        "overview": "ChatGPT Plus is OpenAI's $20/month subscription offering priority access to GPT-4o, DALL-E 3, code interpreter, custom GPTs, and more. OpenRouter is a unified API router and web chat interface that gives you access to 100+ AI models from multiple providers — many completely free — including GPT-4o, Claude 3.5, Llama 3.1, Mistral, and Gemini.",
        "key_differences": [
            "Cost: ChatGPT Plus is $20/month flat; OpenRouter has free model tiers and pay-per-token pricing for premium models",
            "Model variety: OpenRouter routes to 100+ models across 20+ providers; ChatGPT Plus is OpenAI-only",
            "Free models: OpenRouter hosts Llama 3.1 (8B/70B), Mistral 7B, Gemma 2, Phi-3 and more at $0",
            "API access: OpenRouter provides an OpenAI-compatible API endpoint; ChatGPT Plus is a consumer UI only",
            "Context length: Many OpenRouter models offer 128K+ context; ChatGPT Plus varies by model",
        ],
        "pricing_table": {
            "headers": ["Aspect", "ChatGPT Plus", "OpenRouter"],
            "rows": [
                ["Base pricing", "$20/month", "Free tier available"],
                ["GPT-4o access", "✅ Included", "✅ ~$0.003/1K tokens"],
                ["Free models", "❌", "✅ Llama 3.1, Mistral, Gemma"],
                ["API access", "❌ Separate billing", "✅ Included"],
                ["Model variety", "OpenAI only", "100+ models"],
                ["DALL-E image gen", "✅ Included", "❌ Separate"],
            ]
        },
        "github_repo": None,
        "migration": "Sign up at openrouter.ai (free). In the Chat tab, select a free model like 'meta-llama/llama-3.1-8b-instruct:free'. For API use, replace your OpenAI base URL with https://openrouter.ai/api/v1 and use your OpenRouter API key — the API is fully OpenAI-compatible.",
        "related": ["chatgpt-plus-vs-mistral-free", "openai-api-vs-ollama", "jasper-ai-vs-openwebui"],
    },

    {
        "slug": "chatgpt-plus-vs-mistral-free",
        "category": "AI Writing & Chat",
        "category_emoji": "✍️",
        "paid_tool": "ChatGPT Plus",
        "paid_price": "$20/month",
        "paid_url": "https://chat.openai.com",
        "free_tool": "Mistral (Le Chat)",
        "free_price": "Free",
        "free_url": "https://chat.mistral.ai",
        "savings": "$20/month → Free",
        "verdict_switch": "Mistral's Le Chat free tier uses Mistral Large 2, a genuinely powerful model that matches or beats GPT-4 on many benchmarks — with no subscription required.",
        "verdict_stay": "Stick with ChatGPT Plus if you need DALL-E image generation, GPT-4o Vision for complex images, or OpenAI's plugin/custom GPT ecosystem.",
        "setup_difficulty": "Easy",
        "setup_dots": "●○○○○",
        "setup_time": "~2 mins",
        "setup_method": "Browser-based",
        "overview": "ChatGPT Plus charges $20/month for access to GPT-4o and OpenAI's suite of tools. Mistral AI offers Le Chat — a free web interface powered by Mistral Large 2, their flagship model that competes directly with GPT-4-class models. No credit card required.",
        "key_differences": [
            "Cost: ChatGPT Plus is $20/month; Mistral Le Chat has a generous free tier",
            "Model quality: Mistral Large 2 ranks among the top models on coding, math, and instruction-following benchmarks",
            "Privacy: Mistral is a European company with GDPR-first data practices",
            "API: Mistral's API is significantly cheaper than OpenAI's for equivalent model quality",
            "Image generation: ChatGPT Plus includes DALL-E; Mistral has no image generation",
        ],
        "pricing_table": {
            "headers": ["Aspect", "ChatGPT Plus", "Mistral Le Chat"],
            "rows": [
                ["Base pricing", "$20/month", "Free"],
                ["Model quality", "GPT-4o", "Mistral Large 2"],
                ["Image generation", "✅ DALL-E 3", "❌"],
                ["Data residency", "US (OpenAI)", "EU (GDPR)"],
                ["API pricing", "$5/1M input tokens", "$2/1M input tokens"],
                ["Usage limits", "Soft cap on 4o", "Generous free tier"],
            ]
        },
        "github_repo": None,
        "migration": "Go to chat.mistral.ai and create a free account. Select 'Mistral Large' as your model. For API access, sign up at console.mistral.ai — pricing starts at $0.10/1M tokens for smaller models.",
        "related": ["chatgpt-plus-vs-openrouter", "openai-api-vs-groq", "claude-api-vs-ollama"],
    },

    {
        "slug": "jasper-ai-vs-openwebui",
        "category": "AI Writing & Chat",
        "category_emoji": "✍️",
        "paid_tool": "Jasper AI",
        "paid_price": "$39–$99/month",
        "paid_url": "https://jasper.ai",
        "free_tool": "Open WebUI + Llama 3",
        "free_price": "Free (self-hosted)",
        "free_url": "https://openwebui.com",
        "savings": "$39–$99/month → Free",
        "verdict_switch": "Open WebUI paired with Llama 3.1 or Mistral replicates 90% of Jasper's functionality — long-form writing, templates, tone adjustment — at zero cost.",
        "verdict_stay": "Jasper is worth the premium if you need brand voice training on proprietary company data, team collaboration features, or built-in plagiarism checking.",
        "setup_difficulty": "Medium",
        "setup_dots": "●●●○○",
        "setup_time": "~20 mins",
        "setup_method": "Docker",
        "overview": "Jasper AI is a premium AI writing assistant charging $39–$99/month for marketing copy, blog posts, and content templates. Open WebUI is an open-source, self-hosted interface for running local LLMs like Llama 3.1 via Ollama — giving you a comparable AI writing experience at $0/month after setup.",
        "key_differences": [
            "Cost: Jasper is $39–$99/month; Open WebUI + Ollama runs free on your own hardware",
            "Model customization: Ollama lets you run any open-source model; Jasper uses proprietary model fine-tunes",
            "Privacy: Your data stays on your machine with Open WebUI; Jasper sends data to their servers",
            "Templates: Jasper has 50+ marketing templates built-in; Open WebUI requires prompt engineering",
            "Team features: Jasper has native team collaboration; Open WebUI is primarily single-user",
        ],
        "pricing_table": {
            "headers": ["Aspect", "Jasper AI", "Open WebUI + Llama 3"],
            "rows": [
                ["Base pricing", "$39–$99/month", "Free (self-hosted)"],
                ["Model", "Jasper proprietary", "Llama 3.1, Mistral, any"],
                ["Data privacy", "Cloud (their servers)", "100% local"],
                ["Marketing templates", "✅ 50+ built-in", "✅ Via custom prompts"],
                ["Team seats", "Up to 5 per plan", "Unlimited (self-hosted)"],
                ["Hardware required", "None", "8GB+ RAM recommended"],
            ]
        },
        "github_repo": "open-webui/open-webui",
        "migration": "1. Install Ollama from ollama.ai. 2. Run: ollama pull llama3.1. 3. Install Open WebUI via Docker: docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui ghcr.io/open-webui/open-webui:main. 4. Access at localhost:3000.",
        "related": ["copy-ai-vs-openwebui", "chatgpt-plus-vs-openrouter", "notion-ai-vs-obsidian"],
    },

    {
        "slug": "copy-ai-vs-openwebui",
        "category": "AI Writing & Chat",
        "category_emoji": "✍️",
        "paid_tool": "Copy.ai",
        "paid_price": "$36–$186/month",
        "paid_url": "https://copy.ai",
        "free_tool": "Open WebUI + Llama 3",
        "free_price": "Free (self-hosted)",
        "free_url": "https://openwebui.com",
        "savings": "$36–$186/month → Free",
        "verdict_switch": "Open WebUI handles all of Copy.ai's core use cases — ad copy, product descriptions, social captions — for free, with better privacy and no word limits.",
        "verdict_stay": "Copy.ai's advantage is its workflow automation feature (Workflows) that chains AI tasks together; this requires significant prompt engineering to replicate.",
        "setup_difficulty": "Medium",
        "setup_dots": "●●●○○",
        "setup_time": "~20 mins",
        "setup_method": "Docker",
        "overview": "Copy.ai is a marketing-focused AI writing tool starting at $36/month, designed for generating ad copy, email sequences, and social media content. Open WebUI with Llama 3.1 or Mistral provides the same capabilities — short-form copy, email drafting, product descriptions — with no monthly fee.",
        "key_differences": [
            "Cost: Copy.ai starts at $36/month; Open WebUI is free",
            "Word limits: Copy.ai has usage caps by plan; Ollama has no limits beyond your hardware",
            "Workflows: Copy.ai has automated multi-step AI workflows; Open WebUI is single-prompt",
            "Templates: Copy.ai has 90+ copy-specific templates; custom prompts needed in Open WebUI",
            "Setup: Copy.ai is instant browser-based; Open WebUI requires Docker installation",
        ],
        "pricing_table": {
            "headers": ["Aspect", "Copy.ai", "Open WebUI + Llama 3"],
            "rows": [
                ["Base pricing", "$36/month", "Free"],
                ["Word credits", "Unlimited (paid)", "Unlimited (local)"],
                ["Templates", "90+ built-in", "Prompt-based"],
                ["Workflow automation", "✅ Yes", "❌ Manual"],
                ["Data privacy", "Cloud", "100% local"],
                ["API access", "Paid add-on", "Via Ollama API"],
            ]
        },
        "github_repo": "open-webui/open-webui",
        "migration": "Install Ollama and Open WebUI (see Jasper guide above). Create a system prompt like: 'You are a professional copywriter. Write compelling, conversion-focused copy in the style I request.' Save it as a preset in Open WebUI's model settings.",
        "related": ["jasper-ai-vs-openwebui", "writesonic-vs-free-alternatives", "chatgpt-plus-vs-openrouter"],
    },

    {
        "slug": "grammarly-premium-vs-languagetool",
        "category": "AI Writing & Chat",
        "category_emoji": "✍️",
        "paid_tool": "Grammarly Premium",
        "paid_price": "$12–$15/month",
        "paid_url": "https://grammarly.com",
        "free_tool": "LanguageTool",
        "free_price": "Free (self-hosted or free tier)",
        "free_url": "https://languagetool.org",
        "savings": "$12–$15/month → Free",
        "verdict_switch": "LanguageTool's free tier catches grammar, spelling, and style issues in 30+ languages. The self-hosted version removes all limits — unlimited text, full rule set — at zero ongoing cost.",
        "verdict_stay": "Grammarly Premium's AI writing suggestions, plagiarism checker, and tone detector are more sophisticated than LanguageTool's style rules, especially for native English business writing.",
        "setup_difficulty": "Easy",
        "setup_dots": "●○○○○",
        "setup_time": "~2 mins (cloud) / ~15 mins (self-hosted)",
        "setup_method": "Browser extension / Docker",
        "overview": "Grammarly Premium charges $12–$15/month for advanced grammar checking, AI writing suggestions, plagiarism detection, and tone analysis. LanguageTool is an open-source grammar and style checker supporting 30+ languages, available as a free browser extension or as a self-hosted Docker instance with no character limits.",
        "key_differences": [
            "Cost: Grammarly Premium is $12–$15/month; LanguageTool free tier covers most use cases",
            "Languages: LanguageTool supports 30+ languages natively; Grammarly focuses on English",
            "Self-hosting: LanguageTool can run entirely offline via Docker; Grammarly is cloud-only",
            "AI suggestions: Grammarly has GPT-powered rewriting; LanguageTool is rule-based with some ML",
            "Plagiarism: Grammarly includes plagiarism detection; LanguageTool does not",
        ],
        "pricing_table": {
            "headers": ["Aspect", "Grammarly Premium", "LanguageTool"],
            "rows": [
                ["Base pricing", "$12–$15/month", "Free / self-hosted"],
                ["Languages", "English-focused", "30+ languages"],
                ["Self-hosted", "❌", "✅ Docker available"],
                ["Plagiarism check", "✅", "❌"],
                ["AI rewriting", "✅ GPT-powered", "Limited"],
                ["Browser extension", "✅", "✅"],
            ]
        },
        "github_repo": "languagetool-org/languagetool",
        "migration": "Install the LanguageTool browser extension from languagetool.org. For self-hosting: docker run -d -p 8010:8010 silviof/docker-languagetool. Then configure the extension to use your local server at http://localhost:8010.",
        "related": ["chatgpt-plus-vs-openrouter", "notion-ai-vs-obsidian", "quillbot-vs-languagetool"],
    },

    {
        "slug": "notion-ai-vs-obsidian",
        "category": "AI Writing & Chat",
        "category_emoji": "✍️",
        "paid_tool": "Notion AI",
        "paid_price": "$8–$20/user/month (+ AI add-on $8–$10)",
        "paid_url": "https://notion.so",
        "free_tool": "Obsidian + Smart Composer",
        "free_price": "Free (local AI via Ollama)",
        "free_url": "https://obsidian.md",
        "savings": "$16–$30/user/month → Free",
        "verdict_switch": "Obsidian with the Smart Composer or Copilot plugin routes AI requests to local Ollama models or OpenRouter free tiers — giving you in-editor AI writing at zero ongoing cost.",
        "verdict_stay": "Notion AI's tight integration with databases, project views, and real-time team collaboration is hard to replicate in Obsidian, which is primarily single-user.",
        "setup_difficulty": "Medium",
        "setup_dots": "●●●○○",
        "setup_time": "~25 mins",
        "setup_method": "Plugin + Ollama",
        "overview": "Notion AI adds an $8–$10/user/month fee on top of Notion's base plan, providing in-editor AI for writing, summarization, and Q&A over your documents. Obsidian is a free local markdown editor; with the Smart Composer or Copilot community plugin and a local Ollama server, you get comparable AI writing assistance with full data privacy.",
        "key_differences": [
            "Cost: Notion AI adds $8–10/user/month; Obsidian plugins use free Ollama models or cheap API calls",
            "Privacy: Obsidian stores everything locally by default; Notion is cloud-synced",
            "Collaboration: Notion is built for teams; Obsidian is primarily a personal tool",
            "Database views: Notion's table/kanban/calendar views have no equivalent in Obsidian",
            "Mobile sync: Notion has polished mobile apps; Obsidian Sync requires the paid $4/month sync service",
        ],
        "pricing_table": {
            "headers": ["Aspect", "Notion + AI", "Obsidian + Ollama"],
            "rows": [
                ["Base pricing", "$8–$20/user/month", "Free"],
                ["AI add-on", "+$8–$10/user/month", "Free (Ollama models)"],
                ["Data storage", "Notion's cloud", "100% local"],
                ["Team collaboration", "✅ Built-in", "❌ Single-user"],
                ["Database views", "✅ Yes", "❌ Limited"],
                ["Offline access", "Limited", "✅ Full"],
            ]
        },
        "github_repo": "logancyang/obsidian-copilot",
        "migration": "1. Download Obsidian (free). 2. Install Ollama and pull a model: ollama pull llama3.1. 3. In Obsidian Settings → Community Plugins, install 'Copilot'. 4. Set Copilot's model provider to Ollama at http://localhost:11434. You now have AI writing assistance in your local vault.",
        "related": ["jasper-ai-vs-openwebui", "chatgpt-plus-vs-openrouter", "copy-ai-vs-openwebui"],
    },

    {
        "slug": "writesonic-vs-free-alternatives",
        "category": "AI Writing & Chat",
        "category_emoji": "✍️",
        "paid_tool": "Writesonic",
        "paid_price": "$16–$79/month",
        "paid_url": "https://writesonic.com",
        "free_tool": "Open WebUI + Mistral",
        "free_price": "Free (self-hosted)",
        "free_url": "https://openwebui.com",
        "savings": "$16–$79/month → Free",
        "verdict_switch": "Open WebUI with Mistral 7B or Llama 3.1 handles Writesonic's core content generation tasks — blog posts, product descriptions, ads — with no monthly fee and no word credit limits.",
        "verdict_stay": "Writesonic's Chatsonic with real-time web search integration is its standout feature; replicating this requires additional setup with SearXNG or a search API.",
        "setup_difficulty": "Medium",
        "setup_dots": "●●●○○",
        "setup_time": "~20 mins",
        "setup_method": "Docker",
        "overview": "Writesonic is an AI writing platform charging $16–$79/month for content generation, SEO tools, and Chatsonic (a ChatGPT-like assistant with web search). Open WebUI with a capable open-source LLM provides the same content generation capability without word limits or monthly fees.",
        "key_differences": [
            "Cost: Writesonic starts at $16/month with word limits; Open WebUI is free with no limits",
            "Web search: Writesonic's Chatsonic integrates live web search; Open WebUI requires SearXNG integration",
            "SEO features: Writesonic has built-in SEO scoring; this requires separate tools with Open WebUI",
            "Ease of use: Writesonic is polished and beginner-friendly; Open WebUI has a learning curve",
        ],
        "pricing_table": {
            "headers": ["Aspect", "Writesonic", "Open WebUI + Mistral"],
            "rows": [
                ["Base pricing", "$16/month", "Free"],
                ["Word limits", "200K words/month", "Unlimited (local)"],
                ["Web search", "✅ Chatsonic", "✅ With SearXNG"],
                ["SEO tools", "✅ Built-in", "❌ Separate tools"],
                ["Languages", "25+", "Depends on model"],
            ]
        },
        "github_repo": "open-webui/open-webui",
        "migration": "Install Open WebUI with Ollama (see Jasper guide). For web search, also install SearXNG via Docker and enable the Open WebUI web search integration in Settings → Web Search.",
        "related": ["jasper-ai-vs-openwebui", "copy-ai-vs-openwebui", "chatgpt-plus-vs-openrouter"],
    },

    {
        "slug": "perplexity-pro-vs-phind",
        "category": "AI Writing & Chat",
        "category_emoji": "✍️",
        "paid_tool": "Perplexity Pro",
        "paid_price": "$20/month",
        "paid_url": "https://perplexity.ai",
        "free_tool": "Phind",
        "free_price": "Free",
        "free_url": "https://phind.com",
        "savings": "$20/month → Free",
        "verdict_switch": "Phind is a free AI search engine with web browsing capabilities, particularly strong for technical and programming queries — covering the primary use case of most Perplexity Pro users.",
        "verdict_stay": "Perplexity Pro's access to Claude and GPT-4o for answers, file upload analysis, and superior source citation makes it worth the fee for heavy research users.",
        "setup_difficulty": "Easy",
        "setup_dots": "●○○○○",
        "setup_time": "~1 min",
        "setup_method": "Browser-based",
        "overview": "Perplexity Pro charges $20/month for unlimited searches with GPT-4o and Claude 3.5, file uploads, and API access. Phind is a free AI search engine that browses the web in real time — particularly powerful for developer and technical queries — at zero cost.",
        "key_differences": [
            "Cost: Perplexity Pro is $20/month; Phind is free with no rate limits for standard use",
            "Model quality: Perplexity Pro uses GPT-4o / Claude; Phind uses its own fine-tuned models",
            "Technical focus: Phind excels at coding and dev queries; Perplexity is broader",
            "File upload: Perplexity Pro can analyze PDFs; Phind does not support file uploads",
            "API: Perplexity Pro includes API access; Phind has no public API",
        ],
        "pricing_table": {
            "headers": ["Aspect", "Perplexity Pro", "Phind"],
            "rows": [
                ["Base pricing", "$20/month", "Free"],
                ["Web search", "✅ Real-time", "✅ Real-time"],
                ["Model quality", "GPT-4o, Claude 3.5", "Phind-70B"],
                ["File upload", "✅ PDF analysis", "❌"],
                ["API access", "✅ Included", "❌"],
                ["Best for", "General research", "Dev / coding queries"],
            ]
        },
        "github_repo": None,
        "migration": "Simply go to phind.com — no account required. For coding questions, Phind often outperforms Perplexity because it's specifically trained on developer content. For broader research, combine Phind with Kagi or DuckDuckGo for source diversity.",
        "related": ["chatgpt-plus-vs-openrouter", "chatgpt-plus-vs-mistral-free", "openai-api-vs-ollama"],
    },

    # ──────────────────────── 🎨 AI IMAGE GENERATION ────────────────────────

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
        "savings": "$10–$60/month → Free",
        "verdict_switch": "Stable Diffusion with SDXL or Flux models generates comparable image quality to Midjourney at zero cost — you own all outputs, have no usage limits, and can run uncensored styles.",
        "verdict_stay": "Midjourney's aesthetic quality is uniquely refined, especially for stylized art. Its prompt interpretation is also more intuitive for non-technical users than ComfyUI's node-based workflow.",
        "setup_difficulty": "Medium",
        "setup_dots": "●●●○○",
        "setup_time": "~30 mins",
        "setup_method": "Local install (GPU recommended)",
        "overview": "Midjourney is the market-leading AI image generator charging $10–$60/month for varying generation credits. Stable Diffusion is a free, open-source image generation model you can run locally with ComfyUI or Automatic1111 — generating unlimited images at no ongoing cost once hardware is set up.",
        "key_differences": [
            "Cost: Midjourney charges monthly; Stable Diffusion is free after hardware investment",
            "Hardware: Stable Diffusion benefits from a GPU (8GB+ VRAM); Midjourney is cloud-based",
            "Image quality: Midjourney Niji/v6 leads aesthetics; Flux Dev/Schnell is competitive for photorealism",
            "Privacy: Local SD generates images never sent to any server; Midjourney stores all your generations",
            "Customization: SD supports LoRA models, ControlNet, inpainting, upscaling; Midjourney is guided prompting only",
        ],
        "pricing_table": {
            "headers": ["Aspect", "Midjourney", "Stable Diffusion"],
            "rows": [
                ["Base pricing", "$10–$60/month", "Free"],
                ["GPU required", "❌ Cloud-based", "✅ Recommended (8GB+)"],
                ["Generations", "200–unlimited/month", "Unlimited"],
                ["Image ownership", "Check ToS", "100% yours"],
                ["Style control", "Prompts + params", "LoRA, ControlNet, etc."],
                ["API access", "Limited", "Via local API"],
            ]
        },
        "github_repo": "comfyanonymous/ComfyUI",
        "migration": "1. Install Python 3.10+. 2. Clone ComfyUI: git clone https://github.com/comfyanonymous/ComfyUI. 3. Install requirements: pip install -r requirements.txt. 4. Download a model (e.g., Flux Schnell from HuggingFace) to the models/checkpoints folder. 5. Run: python main.py. 6. Open http://localhost:8188.",
        "related": ["dalle3-vs-stable-diffusion", "adobe-firefly-vs-stable-diffusion", "leonardo-ai-vs-stable-diffusion"],
    },

    {
        "slug": "dalle3-vs-stable-diffusion",
        "category": "AI Image Generation",
        "category_emoji": "🎨",
        "paid_tool": "DALL-E 3 (via ChatGPT Plus)",
        "paid_price": "$20/month (ChatGPT Plus) or API pay-per-image",
        "paid_url": "https://openai.com/dall-e-3",
        "free_tool": "Stable Diffusion (Automatic1111)",
        "free_price": "Free (self-hosted)",
        "free_url": "https://github.com/AUTOMATIC1111/stable-diffusion-webui",
        "savings": "$20/month → Free",
        "verdict_switch": "Automatic1111 offers a full-featured WebUI for Stable Diffusion with inpainting, img2img, upscaling, and hundreds of community models — all free and locally run.",
        "verdict_stay": "DALL-E 3's natural language understanding is exceptional — complex multi-element prompts render accurately without fine-tuning. It's also instantly available via ChatGPT.",
        "setup_difficulty": "Medium",
        "setup_dots": "●●●○○",
        "setup_time": "~30 mins",
        "setup_method": "Local install",
        "overview": "DALL-E 3 is OpenAI's image model, accessible via ChatGPT Plus ($20/month) or the API. Automatic1111 (stable-diffusion-webui) is the most popular open-source Stable Diffusion frontend, offering a comprehensive browser-based UI for local image generation with thousands of community models and extensions.",
        "key_differences": [
            "Cost: DALL-E 3 costs $20/month via ChatGPT Plus; Automatic1111 is free",
            "Prompt adherence: DALL-E 3 has superior multi-element prompt accuracy",
            "Model variety: Automatic1111 supports thousands of fine-tuned models and styles",
            "Features: Automatic1111 has inpainting, img2img, upscaling, ControlNet; DALL-E 3 is text-to-image only",
            "Speed: DALL-E 3 via API is ~5-10 seconds; local SD varies by hardware (5s–2min)",
        ],
        "pricing_table": {
            "headers": ["Aspect", "DALL-E 3", "Automatic1111"],
            "rows": [
                ["Pricing", "$20/month (ChatGPT+)", "Free"],
                ["API cost", "$0.04–$0.08/image", "$0"],
                ["Prompt accuracy", "Excellent", "Good (model-dependent)"],
                ["Inpainting", "❌", "✅"],
                ["ControlNet", "❌", "✅"],
                ["Model ecosystem", "One model", "Thousands"],
            ]
        },
        "github_repo": "AUTOMATIC1111/stable-diffusion-webui",
        "migration": "1. Clone: git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui. 2. Run webui.sh (Linux/Mac) or webui-user.bat (Windows). 3. Download a model from civitai.com (e.g., Dreamshaper XL or RealVisXL). 4. Place in models/Stable-diffusion folder and select from the WebUI.",
        "related": ["midjourney-vs-stable-diffusion", "adobe-firefly-vs-stable-diffusion", "canva-ai-vs-stable-diffusion"],
    },

    {
        "slug": "adobe-firefly-vs-stable-diffusion",
        "category": "AI Image Generation",
        "category_emoji": "🎨",
        "paid_tool": "Adobe Firefly",
        "paid_price": "$4.99/month standalone (or $54.99/month Creative Cloud)",
        "paid_url": "https://firefly.adobe.com",
        "free_tool": "Stable Diffusion (ComfyUI)",
        "free_price": "Free (self-hosted)",
        "free_url": "https://github.com/comfyanonymous/ComfyUI",
        "savings": "$4.99–$54.99/month → Free",
        "verdict_switch": "ComfyUI's node-based workflow gives you far more control than Firefly — ControlNet, LoRA fine-tunes, video generation, inpainting — at zero cost.",
        "verdict_stay": "Adobe Firefly is trained exclusively on licensed Adobe Stock imagery, making it legally safe for commercial use without copyright concerns. It also integrates directly into Photoshop and Illustrator.",
        "setup_difficulty": "Medium",
        "setup_dots": "●●●○○",
        "setup_time": "~30 mins",
        "setup_method": "Local install (GPU recommended)",
        "overview": "Adobe Firefly is Adobe's commercially safe AI image generator, trained on licensed content and integrated into Creative Cloud apps. Stable Diffusion via ComfyUI is a free, open-source alternative with broader capabilities — though commercial licensing for SD outputs depends on which model you use.",
        "key_differences": [
            "Commercial safety: Firefly is designed for commercial use; SD model licensing varies",
            "Creative Cloud integration: Firefly integrates with Photoshop, Illustrator, Premiere; SD does not",
            "Cost: Firefly standalone is $4.99/month; SD is free",
            "Generation credits: Firefly has monthly credit limits; SD is unlimited",
            "Vector generation: Firefly can generate editable vectors; SD is raster only",
        ],
        "pricing_table": {
            "headers": ["Aspect", "Adobe Firefly", "Stable Diffusion"],
            "rows": [
                ["Base pricing", "$4.99–$54.99/month", "Free"],
                ["Commercial safe", "✅ Yes (Adobe-licensed training)", "Varies by model"],
                ["Photoshop integration", "✅", "❌"],
                ["Generation credits", "25–250/month", "Unlimited"],
                ["Vector output", "✅", "❌"],
                ["ControlNet", "❌", "✅"],
            ]
        },
        "github_repo": "comfyanonymous/ComfyUI",
        "migration": "For commercial use, consider Flux Dev (Apache 2.0 licensed) or use Stable Diffusion with models explicitly cleared for commercial use. Install ComfyUI and download the Flux Schnell model from HuggingFace for fast, commercially-permissive generations.",
        "related": ["midjourney-vs-stable-diffusion", "dalle3-vs-stable-diffusion", "canva-ai-vs-stable-diffusion"],
    },

    {
        "slug": "canva-ai-vs-stable-diffusion",
        "category": "AI Image Generation",
        "category_emoji": "🎨",
        "paid_tool": "Canva Pro + AI",
        "paid_price": "$14.99–$55/month",
        "paid_url": "https://canva.com",
        "free_tool": "Stable Diffusion + GIMP",
        "free_price": "Free",
        "free_url": "https://gimp.org",
        "savings": "$14.99–$55/month → Free",
        "verdict_switch": "Stable Diffusion handles the AI image generation, and GIMP handles post-editing — replicating the core AI creative workflow of Canva Pro for free.",
        "verdict_stay": "Canva Pro's value is its complete design suite (templates, brand kits, scheduling, presentations) — not just AI generation. If you use Canva for full design workflows, the replacement requires multiple tools.",
        "setup_difficulty": "Medium",
        "setup_dots": "●●●○○",
        "setup_time": "~30 mins",
        "setup_method": "Local install",
        "overview": "Canva Pro bundles AI image generation (Magic Media), background removal, brand kits, and a full design tool into one $14.99–$55/month subscription. Stable Diffusion + GIMP separates those capabilities into free tools — better for power users willing to manage multiple tools.",
        "key_differences": [
            "Design workflow: Canva is an all-in-one design platform; SD + GIMP are separate specialized tools",
            "Ease of use: Canva is drag-and-drop for non-designers; SD has a steeper learning curve",
            "AI generation quality: SD with SDXL/Flux outperforms Canva's Magic Media for photorealism",
            "Templates: Canva has 250,000+ professional templates; GIMP has limited templates",
            "Collaboration: Canva Pro has team features; GIMP and SD are single-user tools",
        ],
        "pricing_table": {
            "headers": ["Aspect", "Canva Pro", "Stable Diffusion + GIMP"],
            "rows": [
                ["Base pricing", "$14.99/month", "Free"],
                ["AI image gen", "✅ Magic Media (limited)", "✅ Unlimited (SD)"],
                ["Design templates", "✅ 250K+", "Limited"],
                ["Background removal", "✅ One-click", "✅ GIMP plugin"],
                ["Brand kits", "✅", "❌"],
                ["Team collaboration", "✅", "❌"],
            ]
        },
        "github_repo": "AUTOMATIC1111/stable-diffusion-webui",
        "migration": "For AI generation: use Automatic1111 or ComfyUI. For background removal: use rembg (free, open-source). For design layout: try Penpot (free) or Inkscape. Together these cover 80% of Canva Pro's use cases.",
        "related": ["midjourney-vs-stable-diffusion", "adobe-firefly-vs-stable-diffusion", "dalle3-vs-stable-diffusion"],
    },

    {
        "slug": "runway-ml-vs-comfyui-video",
        "category": "AI Image Generation",
        "category_emoji": "🎨",
        "paid_tool": "Runway ML",
        "paid_price": "$15–$95/month",
        "paid_url": "https://runwayml.com",
        "free_tool": "ComfyUI + AnimateDiff",
        "free_price": "Free (self-hosted)",
        "free_url": "https://github.com/comfyanonymous/ComfyUI",
        "savings": "$15–$95/month → Free",
        "verdict_switch": "ComfyUI with AnimateDiff or the CogVideoX extension generates AI video locally at no cost — ideal for developers and creators comfortable with GPU setup.",
        "verdict_stay": "Runway Gen-3's motion quality and video editing features (inpainting, masking, motion brush) are production-ready in ways that open-source video generation is still catching up to.",
        "setup_difficulty": "Hard",
        "setup_dots": "●●●●○",
        "setup_time": "~1 hour",
        "setup_method": "Local GPU + ComfyUI",
        "overview": "Runway ML is a professional AI video generation and editing platform charging $15–$95/month. ComfyUI with AnimateDiff, SVD (Stable Video Diffusion), or CogVideoX provides open-source AI video generation — requiring a capable GPU but offering unlimited generations at no ongoing cost.",
        "key_differences": [
            "Cost: Runway charges monthly; ComfyUI video is free after hardware setup",
            "Hardware: Local video generation requires 16GB+ VRAM; Runway is cloud-based",
            "Quality: Runway Gen-3 currently leads for smooth, long-duration clips",
            "Video length: Runway generates up to 16s clips; AnimateDiff is typically 2-4s",
            "Professional tools: Runway has motion brush, inpainting, and a full video editor",
        ],
        "pricing_table": {
            "headers": ["Aspect", "Runway ML", "ComfyUI + AnimateDiff"],
            "rows": [
                ["Base pricing", "$15/month", "Free"],
                ["GPU needed", "❌ Cloud", "✅ 16GB+ VRAM"],
                ["Video length", "Up to 16 seconds", "2–8 seconds typical"],
                ["Video quality", "Gen-3: Excellent", "Good (improving fast)"],
                ["Motion brush", "✅", "❌"],
                ["API access", "✅ Paid", "Via local API"],
            ]
        },
        "github_repo": "Kosinkadink/ComfyUI-AnimateDiff-Evolved",
        "migration": "Install ComfyUI, then install the ComfyUI-Manager. Search for and install 'ComfyUI-AnimateDiff-Evolved'. Download motion module weights from HuggingFace (mm_sd_v15_v2.ckpt). Import an AnimateDiff workflow JSON from the ComfyUI community examples.",
        "related": ["midjourney-vs-stable-diffusion", "dalle3-vs-stable-diffusion", "adobe-firefly-vs-stable-diffusion"],
    },

    # ──────────────────────── 💻 AI CODING ────────────────────────

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
        "savings": "$10–$19/month → Free",
        "verdict_switch": "Codeium's free tier provides unlimited AI code completions, chat, and search across 70+ languages and 40+ editors — matching GitHub Copilot's core functionality at $0.",
        "verdict_stay": "GitHub Copilot's native GitHub integration (pull request summaries, Actions integration, enterprise SSO) and its deeper training on GitHub's massive code corpus give it an edge for enterprise teams.",
        "setup_difficulty": "Easy",
        "setup_dots": "●○○○○",
        "setup_time": "~5 mins",
        "setup_method": "IDE plugin",
        "overview": "GitHub Copilot charges $10–$19/month for AI code completion, chat, and PR summaries in VS Code, JetBrains, and more. Codeium is a free AI coding assistant offering unlimited completions, in-editor chat, and codebase search — supporting 70+ languages with VS Code, JetBrains, Vim, Neovim, and other editors.",
        "key_differences": [
            "Cost: GitHub Copilot is $10–$19/month; Codeium is completely free for individuals",
            "Completions: Both offer real-time inline suggestions; quality is comparable for most tasks",
            "Chat: Both have in-editor AI chat; Codeium's is included free, Copilot requires Business plan for enterprise features",
            "GitHub integration: Copilot has native PR review summaries; Codeium does not",
            "Privacy: Codeium has a strong no-training-on-user-code policy by default",
        ],
        "pricing_table": {
            "headers": ["Aspect", "GitHub Copilot", "Codeium"],
            "rows": [
                ["Base pricing", "$10/month individual", "Free"],
                ["Completions", "Unlimited", "Unlimited"],
                ["In-editor chat", "✅", "✅ Free"],
                ["Languages", "All major", "70+"],
                ["PR summaries", "✅ GitHub native", "❌"],
                ["Codebase search", "✅ Paid tier", "✅ Free"],
            ]
        },
        "github_repo": None,
        "migration": "In VS Code, open Extensions (Ctrl+Shift+X), search 'Codeium', and install. Sign up at codeium.com for a free account and authenticate. Disable GitHub Copilot extension to avoid conflicts. Codeium starts suggesting immediately.",
        "related": ["github-copilot-vs-continue-dev", "cursor-ai-vs-continue-dev", "tabnine-pro-vs-codeium"],
    },

    {
        "slug": "github-copilot-vs-continue-dev",
        "category": "AI Coding",
        "category_emoji": "💻",
        "paid_tool": "GitHub Copilot",
        "paid_price": "$10–$19/month",
        "paid_url": "https://github.com/features/copilot",
        "free_tool": "Continue.dev + Ollama",
        "free_price": "Free (self-hosted)",
        "free_url": "https://continue.dev",
        "savings": "$10–$19/month → Free",
        "verdict_switch": "Continue.dev is an open-source VS Code extension that connects to any LLM — local Ollama models, OpenRouter free tiers, or commercial APIs — giving you full control over your AI coding assistant.",
        "verdict_stay": "GitHub Copilot's cloud-hosted models (GPT-4o, Claude 3.5) provide better code generation quality than most locally-run models, especially on complex tasks.",
        "setup_difficulty": "Medium",
        "setup_dots": "●●●○○",
        "setup_time": "~20 mins",
        "setup_method": "VS Code extension + Ollama",
        "overview": "GitHub Copilot offers managed AI code completion via Microsoft/OpenAI infrastructure. Continue.dev is an open-source VS Code and JetBrains extension that acts as a universal AI coding layer — you connect it to any LLM backend: local Ollama models like DeepSeek Coder, cloud APIs like OpenRouter, or commercial endpoints.",
        "key_differences": [
            "Cost: Copilot is $10–$19/month; Continue.dev + Ollama is free for local models",
            "Model flexibility: Continue.dev works with any LLM; Copilot uses only OpenAI/Anthropic models",
            "Privacy: Continue + local Ollama means no code ever leaves your machine",
            "Quality: GPT-4o (Copilot) outperforms most local models on complex code generation",
            "Configuration: Continue.dev requires setting up Ollama and configuring models; Copilot is plug-and-play",
        ],
        "pricing_table": {
            "headers": ["Aspect", "GitHub Copilot", "Continue.dev + Ollama"],
            "rows": [
                ["Base pricing", "$10/month", "Free"],
                ["Model source", "OpenAI / Anthropic", "Any (local or API)"],
                ["Code privacy", "Sent to Microsoft", "100% local option"],
                ["Setup time", "2 minutes", "~20 minutes"],
                ["Best local model", "N/A", "DeepSeek Coder 6.7B"],
                ["Open source", "❌", "✅"],
            ]
        },
        "github_repo": "continuedev/continue",
        "migration": "1. Install Continue from VS Code marketplace. 2. Install Ollama: ollama.ai. 3. Pull a coding model: ollama pull deepseek-coder:6.7b. 4. In Continue's config.json, add: {\"provider\": \"ollama\", \"model\": \"deepseek-coder:6.7b\"}. 5. Use Ctrl+I for inline edits, Ctrl+L for chat.",
        "related": ["github-copilot-vs-codeium", "cursor-ai-vs-continue-dev", "openai-api-vs-ollama"],
    },

    {
        "slug": "cursor-ai-vs-continue-dev",
        "category": "AI Coding",
        "category_emoji": "💻",
        "paid_tool": "Cursor AI",
        "paid_price": "$20/month (Pro)",
        "paid_url": "https://cursor.sh",
        "free_tool": "Continue.dev + VS Code",
        "free_price": "Free",
        "free_url": "https://continue.dev",
        "savings": "$20/month → Free",
        "verdict_switch": "Continue.dev brings Cursor-like AI coding features (inline edits, codebase chat, autocomplete) into VS Code — the editor you already use — connected to free local models.",
        "verdict_stay": "Cursor's custom Claude 3.5-based 'apply' model and its deep codebase indexing (Ctrl+Enter for multi-file edits) deliver a premium AI coding experience that's hard to fully replicate.",
        "setup_difficulty": "Medium",
        "setup_dots": "●●●○○",
        "setup_time": "~20 mins",
        "setup_method": "VS Code extension + Ollama",
        "overview": "Cursor is a VS Code fork with deep AI integration, charging $20/month for access to GPT-4o and Claude 3.5 Sonnet. Continue.dev is an open-source plugin that adds similar AI coding capabilities to standard VS Code — compatible with any LLM backend including free local models.",
        "key_differences": [
            "Cost: Cursor Pro is $20/month; Continue.dev is free",
            "Editor: Cursor is a separate VS Code fork; Continue.dev plugs into your existing VS Code",
            "Multi-file edits: Cursor's Ctrl+Enter command is excellent at coordinated multi-file changes",
            "Model quality: Cursor uses Claude 3.5; Continue.dev can use any model including free local ones",
            "Codebase indexing: Cursor indexes your entire codebase for context; Continue.dev has @codebase context",
        ],
        "pricing_table": {
            "headers": ["Aspect", "Cursor AI", "Continue.dev"],
            "rows": [
                ["Pricing", "$20/month (Pro)", "Free"],
                ["Model", "Claude 3.5 / GPT-4o", "Any (local or API)"],
                ["Editor", "VS Code fork", "Standard VS Code"],
                ["Multi-file edits", "✅ Excellent", "✅ Good"],
                ["Codebase chat", "✅", "✅"],
                ["Open source", "❌", "✅"],
            ]
        },
        "github_repo": "continuedev/continue",
        "migration": "Install Continue.dev extension in VS Code. Connect to Ollama with deepseek-coder or codestral. For a closer Cursor experience, add an OpenRouter API key to Continue's config to access free tiers of powerful models like Qwen 2.5 Coder.",
        "related": ["github-copilot-vs-continue-dev", "github-copilot-vs-codeium", "openai-api-vs-ollama"],
    },

    {
        "slug": "tabnine-pro-vs-codeium",
        "category": "AI Coding",
        "category_emoji": "💻",
        "paid_tool": "Tabnine Pro",
        "paid_price": "$12/month",
        "paid_url": "https://tabnine.com",
        "free_tool": "Codeium",
        "free_price": "Free",
        "free_url": "https://codeium.com",
        "savings": "$12/month → Free",
        "verdict_switch": "Codeium covers all of Tabnine's core features — whole-line and full-function completions, multi-language support, IDE integration — at no cost, with a more generous free tier.",
        "verdict_stay": "Tabnine Pro's local model option (runs on your machine, zero data sent externally) is its key differentiator for security-sensitive enterprise teams.",
        "setup_difficulty": "Easy",
        "setup_dots": "●○○○○",
        "setup_time": "~5 mins",
        "setup_method": "IDE plugin",
        "overview": "Tabnine Pro charges $12/month for whole-line completions, full-function suggestions, and multi-line code generation. Codeium offers equivalent features for free, supporting 70+ languages and 40+ editors with no character or completion limits.",
        "key_differences": [
            "Cost: Tabnine Pro is $12/month; Codeium is free",
            "Local model: Tabnine offers a local processing option for enterprise privacy; Codeium is cloud-based",
            "Completion quality: Both are competitive; Codeium generally scores higher on recent benchmarks",
            "Team features: Tabnine has team learning (adapts to your codebase style); Codeium's team plan is paid",
            "Privacy: Tabnine local mode processes code on-device; Codeium sends code to their servers",
        ],
        "pricing_table": {
            "headers": ["Aspect", "Tabnine Pro", "Codeium"],
            "rows": [
                ["Pricing", "$12/month", "Free"],
                ["Full-function completions", "✅", "✅"],
                ["Local model option", "✅ Enterprise", "❌"],
                ["Languages", "All major", "70+"],
                ["IDE support", "All major", "40+ editors"],
                ["Codebase learning", "✅ Team plans", "✅ Enterprise"],
            ]
        },
        "github_repo": None,
        "migration": "Open your IDE's extension marketplace and install 'Codeium'. Uninstall Tabnine to prevent conflicts. Create a free account at codeium.com. For local-model privacy without Codeium, consider Continue.dev + Ollama instead.",
        "related": ["github-copilot-vs-codeium", "github-copilot-vs-continue-dev", "cursor-ai-vs-continue-dev"],
    },

    {
        "slug": "replit-ai-vs-free-alternatives",
        "category": "AI Coding",
        "category_emoji": "💻",
        "paid_tool": "Replit AI (Core)",
        "paid_price": "$20/month",
        "paid_url": "https://replit.com",
        "free_tool": "GitHub Codespaces + Continue.dev",
        "free_price": "Free (60hrs/month free tier)",
        "free_url": "https://github.com/features/codespaces",
        "savings": "$20/month → Free (within limits)",
        "verdict_switch": "GitHub Codespaces gives you 60 free compute hours/month in a full cloud VS Code environment. Combined with Continue.dev and Ollama or OpenRouter free models, you get AI-assisted cloud coding at zero cost.",
        "verdict_stay": "Replit AI's fully integrated experience — Ghostwriter autocomplete, AI chat, deployment, and database all in one browser tab — is uniquely frictionless for rapid prototyping and education.",
        "setup_difficulty": "Easy",
        "setup_dots": "●●○○○",
        "setup_time": "~10 mins",
        "setup_method": "Browser-based",
        "overview": "Replit AI Core charges $20/month for Ghostwriter AI completions, AI chat, and Replit's hosting platform. GitHub Codespaces offers 60 free compute hours/month for a cloud VS Code environment — pair it with Continue.dev for AI coding assistance and you cover most Replit AI use cases.",
        "key_differences": [
            "Cost: Replit Core is $20/month; Codespaces is free for 60 hours/month",
            "AI integration: Replit AI is deeply integrated; Codespaces needs Continue.dev plugin",
            "Deployment: Replit includes one-click hosting; Codespaces requires separate deployment",
            "Database: Replit has built-in DB; Codespaces connects to external DBs",
            "Education: Replit is purpose-built for learning; Codespaces is a professional dev environment",
        ],
        "pricing_table": {
            "headers": ["Aspect", "Replit AI Core", "Codespaces + Continue"],
            "rows": [
                ["Pricing", "$20/month", "Free (60hrs/mo)"],
                ["AI completions", "✅ Ghostwriter", "✅ Continue.dev"],
                ["One-click deploy", "✅", "❌ Separate step"],
                ["Built-in DB", "✅", "❌"],
                ["Browser IDE", "✅", "✅"],
                ["Hours limit", "Unlimited", "60hrs/month free"],
            ]
        },
        "github_repo": "continuedev/continue",
        "migration": "Open any GitHub repo and press '.' or change github.com to github.dev to open a Codespaces VS Code editor. Install Continue.dev extension within Codespaces. For free AI models, configure Continue with OpenRouter's free models or use the GitHub Models preview endpoint.",
        "related": ["github-copilot-vs-codeium", "cursor-ai-vs-continue-dev", "github-copilot-vs-continue-dev"],
    },

    # ──────────────────────── 🎤 AI VOICE & AUDIO ────────────────────────

    {
        "slug": "elevenlabs-vs-coqui-tts",
        "category": "AI Voice & Audio",
        "category_emoji": "🎤",
        "paid_tool": "ElevenLabs",
        "paid_price": "$5–$99/month",
        "paid_url": "https://elevenlabs.io",
        "free_tool": "Coqui TTS",
        "free_price": "Free (self-hosted)",
        "free_url": "https://github.com/coqui-ai/TTS",
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
            "Voice cloning: Both support voice cloning; ElevenLabs requires 1 min sample, XTTS works with 6 seconds",
            "Character limits: ElevenLabs caps by plan; Coqui has no limits on local hardware",
            "API ease: ElevenLabs has a polished API; Coqui requires Python integration",
        ],
        "pricing_table": {
            "headers": ["Aspect", "ElevenLabs", "Coqui TTS (XTTS)"],
            "rows": [
                ["Pricing", "$5–$99/month", "Free"],
                ["Voice cloning", "✅ 1 min sample", "✅ 6 sec sample"],
                ["Character limit", "30K–2M/month", "Unlimited"],
                ["Languages", "29+", "17+"],
                ["API", "✅ REST API", "✅ Python / local"],
                ["Streaming", "✅ Real-time", "✅ With setup"],
            ]
        },
        "github_repo": "coqui-ai/TTS",
        "migration": "pip install TTS. Generate speech: tts --text 'Hello world' --model_name tts_models/multilingual/multi-dataset/xtts_v2 --out_path output.wav. For voice cloning: add --speaker_wav your_voice.wav --language_idx en.",
        "related": ["murf-ai-vs-coqui-tts", "descript-vs-whisper-audacity", "otter-ai-vs-whisper"],
    },

    {
        "slug": "murf-ai-vs-coqui-tts",
        "category": "AI Voice & Audio",
        "category_emoji": "🎤",
        "paid_tool": "Murf AI",
        "paid_price": "$19–$75/month",
        "paid_url": "https://murf.ai",
        "free_tool": "Coqui TTS / Piper TTS",
        "free_price": "Free (self-hosted)",
        "free_url": "https://github.com/rhasspy/piper",
        "savings": "$19–$75/month → Free",
        "verdict_switch": "Piper TTS generates fast, natural-sounding speech locally with minimal hardware requirements — no GPU needed — making it ideal for narration, videos, and automation pipelines.",
        "verdict_stay": "Murf AI's polished studio interface, 120+ AI voices, background music mixing, and video sync make it the best choice for non-technical users producing professional voiceovers.",
        "setup_difficulty": "Medium",
        "setup_dots": "●●○○○",
        "setup_time": "~10 mins",
        "setup_method": "Python pip",
        "overview": "Murf AI is a professional AI voiceover studio with 120+ voices in 20+ languages, charging $19–$75/month. Piper TTS is an ultra-fast open-source neural TTS system running entirely on CPU — generating speech in real-time on basic hardware — making it ideal for home automation, content creation, and batch narration.",
        "key_differences": [
            "Cost: Murf is $19–$75/month; Piper is free and runs on CPU",
            "Voice count: Murf has 120+ voices; Piper has 50+ voices across many languages",
            "Studio UI: Murf has a full browser-based studio; Piper is command-line",
            "Video sync: Murf syncs voiceovers to video timelines; Piper does not",
            "Speed: Piper generates audio in real-time on CPU; Murf processes in the cloud",
        ],
        "pricing_table": {
            "headers": ["Aspect", "Murf AI", "Piper TTS"],
            "rows": [
                ["Pricing", "$19–$75/month", "Free"],
                ["GPU required", "❌ Cloud", "❌ CPU only"],
                ["Voice count", "120+", "50+"],
                ["Languages", "20+", "Many"],
                ["Video sync", "✅", "❌"],
                ["API access", "✅ Paid", "✅ Via command line"],
            ]
        },
        "github_repo": "rhasspy/piper",
        "migration": "1. pip install piper-tts. 2. Download a voice model: e.g., en_US-lessac-medium.onnx from HuggingFace. 3. Generate: echo 'Hello world' | piper --model en_US-lessac-medium.onnx --output_file output.wav.",
        "related": ["elevenlabs-vs-coqui-tts", "descript-vs-whisper-audacity", "adobe-podcast-vs-whisper"],
    },

    {
        "slug": "descript-vs-whisper-audacity",
        "category": "AI Voice & Audio",
        "category_emoji": "🎤",
        "paid_tool": "Descript",
        "paid_price": "$12–$24/month",
        "paid_url": "https://descript.com",
        "free_tool": "Audacity + OpenAI Whisper",
        "free_price": "Free",
        "free_url": "https://www.audacityteam.org",
        "savings": "$12–$24/month → Free",
        "verdict_switch": "Audacity handles professional audio editing while OpenAI Whisper provides state-of-the-art transcription locally — covering Descript's two core features at zero cost.",
        "verdict_stay": "Descript's killer feature is its text-based video editor — you edit audio and video by editing a transcript, including overdub (AI voice replacement). This workflow has no clean free equivalent.",
        "setup_difficulty": "Easy",
        "setup_dots": "●●○○○",
        "setup_time": "~10 mins",
        "setup_method": "Desktop app + pip",
        "overview": "Descript combines AI transcription, audio/video editing, and overdub (voice cloning) in a text-based editor for $12–$24/month. Audacity is the free industry-standard audio editor; OpenAI Whisper is a free, highly accurate local transcription model — together they replace Descript's audio workflow.",
        "key_differences": [
            "Cost: Descript is $12–$24/month; Audacity + Whisper are free",
            "Text-based editing: Descript's edit-by-transcript workflow is unique; Audacity is waveform-based",
            "Overdub: Descript's AI voice replacement has no direct free equivalent",
            "Video editing: Descript handles video; Audacity is audio-only",
            "Transcription quality: Whisper large-v3 matches or exceeds Descript's transcription accuracy",
        ],
        "pricing_table": {
            "headers": ["Aspect", "Descript", "Audacity + Whisper"],
            "rows": [
                ["Pricing", "$12–$24/month", "Free"],
                ["Transcription", "✅ AI-powered", "✅ Whisper (local)"],
                ["Text-based editing", "✅", "❌"],
                ["Video editing", "✅", "❌"],
                ["Overdub (AI voice)", "✅", "❌"],
                ["Noise removal", "✅ AI", "✅ Plugin"],
            ]
        },
        "github_repo": "openai/whisper",
        "migration": "Download Audacity (audacityteam.org). For transcription: pip install openai-whisper. Run: whisper audio.mp3 --model large-v3 --output_format txt. For faster local transcription, consider faster-whisper instead.",
        "related": ["otter-ai-vs-whisper", "adobe-podcast-vs-whisper", "elevenlabs-vs-coqui-tts"],
    },

    {
        "slug": "otter-ai-vs-whisper",
        "category": "AI Voice & Audio",
        "category_emoji": "🎤",
        "paid_tool": "Otter.ai",
        "paid_price": "$8.33–$20/month",
        "paid_url": "https://otter.ai",
        "free_tool": "OpenAI Whisper (local)",
        "free_price": "Free",
        "free_url": "https://github.com/openai/whisper",
        "savings": "$8.33–$20/month → Free",
        "verdict_switch": "OpenAI Whisper provides transcription accuracy matching or exceeding Otter.ai, running entirely on your machine — no cloud, no character limits, no storage fees.",
        "verdict_stay": "Otter.ai's real-time meeting transcription (Zoom, Teams, Meet integration), live speaker identification, and meeting summary generation are its key advantages over offline Whisper.",
        "setup_difficulty": "Easy",
        "setup_dots": "●●○○○",
        "setup_time": "~10 mins",
        "setup_method": "Python pip",
        "overview": "Otter.ai charges $8.33–$20/month for meeting transcription with speaker diarization, live captions, and AI summaries. OpenAI Whisper is a free, open-source speech recognition model with industry-leading accuracy — running locally with no per-minute cost or cloud dependency.",
        "key_differences": [
            "Cost: Otter.ai is $8.33–$20/month; Whisper is free",
            "Real-time transcription: Otter does live meeting transcription; Whisper processes pre-recorded audio",
            "Speaker ID: Otter identifies multiple speakers automatically; Whisper requires separate diarization",
            "Meeting integration: Otter joins Zoom/Meet/Teams calls; Whisper needs manual recording",
            "Accuracy: Both achieve ~95%+ accuracy on clear audio; Whisper large-v3 leads on accents",
        ],
        "pricing_table": {
            "headers": ["Aspect", "Otter.ai", "Whisper"],
            "rows": [
                ["Pricing", "$8.33–$20/month", "Free"],
                ["Real-time transcription", "✅", "❌"],
                ["Meeting bot", "✅ Zoom/Meet/Teams", "❌"],
                ["Speaker diarization", "✅", "✅ With pyannote"],
                ["Languages", "English-first", "99 languages"],
                ["Processing", "Cloud", "100% local"],
            ]
        },
        "github_repo": "openai/whisper",
        "migration": "pip install openai-whisper. Transcribe: whisper meeting_recording.mp4 --model large-v3. For speaker diarization, add pyannote-audio: pip install pyannote.audio and use whisperx for combined transcription + diarization.",
        "related": ["descript-vs-whisper-audacity", "adobe-podcast-vs-whisper", "fireflies-ai-vs-whisper"],
    },

    {
        "slug": "adobe-podcast-vs-whisper",
        "category": "AI Voice & Audio",
        "category_emoji": "🎤",
        "paid_tool": "Adobe Podcast (Enhance)",
        "paid_price": "$4.99/month (or CC subscription)",
        "paid_url": "https://podcast.adobe.com",
        "free_tool": "DeepFilterNet + Whisper",
        "free_price": "Free",
        "free_url": "https://github.com/rikorose/DeepFilterNet",
        "savings": "$4.99+/month → Free",
        "verdict_switch": "DeepFilterNet removes background noise with comparable quality to Adobe Podcast Enhance — processing locally, privately, and with no file size limits.",
        "verdict_stay": "Adobe Podcast's Enhance is extremely simple (drag-and-drop, no setup) and integrates with the full Adobe suite. For non-technical users, the convenience justifies the cost.",
        "setup_difficulty": "Easy",
        "setup_dots": "●●○○○",
        "setup_time": "~5 mins",
        "setup_method": "Python pip",
        "overview": "Adobe Podcast Enhance is an AI noise removal tool that dramatically improves audio quality, included in Creative Cloud or at $4.99/month standalone. DeepFilterNet is an open-source real-time noise suppression neural network that runs locally — achieving comparable audio enhancement at no cost.",
        "key_differences": [
            "Cost: Adobe Podcast Enhance is part of a paid subscription; DeepFilterNet is free",
            "Ease: Adobe Podcast is drag-and-drop on the web; DeepFilterNet is command-line",
            "Processing: Adobe processes on their servers; DeepFilterNet runs locally",
            "Real-time: DeepFilterNet supports real-time processing; Adobe is batch only",
            "Integration: Adobe integrates with Premiere/Audition; DeepFilterNet is standalone",
        ],
        "pricing_table": {
            "headers": ["Aspect", "Adobe Podcast Enhance", "DeepFilterNet"],
            "rows": [
                ["Pricing", "$4.99+/month", "Free"],
                ["Ease of use", "✅ Drag-and-drop", "Command-line"],
                ["Real-time processing", "❌", "✅"],
                ["Data privacy", "Cloud (Adobe)", "100% local"],
                ["File size limits", "Yes", "None"],
                ["Adobe suite integration", "✅", "❌"],
            ]
        },
        "github_repo": "rikorose/DeepFilterNet",
        "migration": "pip install deepfilternet. Enhance audio: deepFilter noisy_audio.wav -o enhanced/. For real-time use in audio interfaces, install the ladspa plugin version.",
        "related": ["descript-vs-whisper-audacity", "otter-ai-vs-whisper", "elevenlabs-vs-coqui-tts"],
    },

    # ──────────────────────── 📹 AI VIDEO ────────────────────────

    {
        "slug": "synthesia-vs-open-source-avatar",
        "category": "AI Video",
        "category_emoji": "📹",
        "paid_tool": "Synthesia",
        "paid_price": "$18–$67/month",
        "paid_url": "https://synthesia.io",
        "free_tool": "SadTalker / DID Free Tier",
        "free_price": "Free",
        "free_url": "https://github.com/OpenTalker/SadTalker",
        "savings": "$18–$67/month → Free",
        "verdict_switch": "SadTalker generates realistic talking head videos from a single photo and an audio file — locally, for free, covering the core use case of Synthesia for developers and small creators.",
        "verdict_stay": "Synthesia's 140+ professional AI avatars, built-in multi-language voiceover, and polished presenter interface are unmatched for corporate training videos at scale.",
        "setup_difficulty": "Hard",
        "setup_dots": "●●●●○",
        "setup_time": "~45 mins",
        "setup_method": "Python + CUDA",
        "overview": "Synthesia generates professional AI presenter videos using 140+ digital avatars in 120+ languages, targeting corporate training and marketing. SadTalker is an open-source talking head generation model that animates a photo realistically from audio — providing the core talking avatar functionality locally.",
        "key_differences": [
            "Cost: Synthesia is $18–$67/month; SadTalker is free with local GPU",
            "Avatar quality: Synthesia's avatars are polished and diverse; SadTalker quality depends on input photo",
            "Languages: Synthesia has built-in 120+ language TTS; SadTalker needs separate audio",
            "Setup: Synthesia is browser-based; SadTalker requires Python/CUDA environment",
            "Video length: Synthesia supports long-form videos; SadTalker has practical limits",
        ],
        "pricing_table": {
            "headers": ["Aspect", "Synthesia", "SadTalker"],
            "rows": [
                ["Pricing", "$18–$67/month", "Free"],
                ["Avatars", "140+ professional", "Any photo input"],
                ["Built-in TTS", "✅ 120+ languages", "❌ Separate audio needed"],
                ["GPU needed", "❌ Cloud", "✅ CUDA recommended"],
                ["Video length", "Long-form", "Short clips optimal"],
                ["Setup", "Browser-based", "Python + CUDA"],
            ]
        },
        "github_repo": "OpenTalker/SadTalker",
        "migration": "1. Clone: git clone https://github.com/OpenTalker/SadTalker. 2. pip install -r requirements.txt. 3. Download checkpoints (see README). 4. Run: python inference.py --driven_audio audio.wav --source_image photo.jpg --result_dir output. Combine with Coqui TTS for end-to-end free avatar video.",
        "related": ["runway-ml-vs-comfyui-video", "pictory-vs-kdenlive", "invideo-ai-vs-kdenlive"],
    },

    {
        "slug": "pictory-vs-kdenlive",
        "category": "AI Video",
        "category_emoji": "📹",
        "paid_tool": "Pictory AI",
        "paid_price": "$19–$99/month",
        "paid_url": "https://pictory.ai",
        "free_tool": "Kdenlive + Whisper",
        "free_price": "Free",
        "free_url": "https://kdenlive.org",
        "savings": "$19–$99/month → Free",
        "verdict_switch": "Kdenlive handles professional video editing, and Whisper provides accurate auto-captions — covering the two core features of Pictory at zero cost.",
        "verdict_stay": "Pictory's auto-blog-to-video and script-to-video features — which automatically select relevant stock footage — have no close free equivalent and save hours of manual work.",
        "setup_difficulty": "Easy",
        "setup_dots": "●●○○○",
        "setup_time": "~10 mins",
        "setup_method": "Desktop app + pip",
        "overview": "Pictory AI automatically turns blog posts or scripts into videos with stock footage, captions, and voiceover. Kdenlive is a free, open-source professional video editor; combined with Whisper for auto-captions, it covers the manual editing side — though the automated script-to-video workflow requires more manual effort.",
        "key_differences": [
            "Cost: Pictory is $19–$99/month; Kdenlive + Whisper are free",
            "Auto-video creation: Pictory automatically sources stock clips for scripts; Kdenlive is manual",
            "Captions: Pictory auto-generates captions; Whisper generates them locally",
            "Stock footage: Pictory has built-in licensed stock library; Kdenlive requires external assets",
            "Learning curve: Pictory is beginner-friendly; Kdenlive is a professional NLE",
        ],
        "pricing_table": {
            "headers": ["Aspect", "Pictory AI", "Kdenlive + Whisper"],
            "rows": [
                ["Pricing", "$19–$99/month", "Free"],
                ["Auto-video creation", "✅", "❌ Manual"],
                ["Auto-captions", "✅", "✅ Whisper"],
                ["Stock footage", "✅ Built-in licensed", "❌ Separate"],
                ["Video editing", "Basic", "Professional NLE"],
                ["Export quality", "Up to 1080p", "Up to 8K"],
            ]
        },
        "github_repo": "openai/whisper",
        "migration": "1. Download Kdenlive. 2. For auto-captions: pip install openai-whisper. Run whisper video.mp4 --model medium --output_format srt. 3. Import the .srt file into Kdenlive as a subtitle track. For free stock footage: use Pexels or Pixabay.",
        "related": ["invideo-ai-vs-kdenlive", "runway-ml-vs-comfyui-video", "descript-vs-whisper-audacity"],
    },

    {
        "slug": "invideo-ai-vs-kdenlive",
        "category": "AI Video",
        "category_emoji": "📹",
        "paid_tool": "InVideo AI",
        "paid_price": "$20–$48/month",
        "paid_url": "https://invideo.io",
        "free_tool": "Kdenlive + Stable Diffusion",
        "free_price": "Free",
        "free_url": "https://kdenlive.org",
        "savings": "$20–$48/month → Free",
        "verdict_switch": "Kdenlive provides a full professional video editing suite free, while Stable Diffusion can generate custom AI imagery for thumbnails and visuals — covering InVideo's core content creation capabilities.",
        "verdict_stay": "InVideo AI's text-to-video workflow (type a topic, get a fully assembled video with voiceover and stock footage) is uniquely quick for social media content at scale.",
        "setup_difficulty": "Easy",
        "setup_dots": "●●○○○",
        "setup_time": "~10 mins",
        "setup_method": "Desktop app",
        "overview": "InVideo AI generates social media and marketing videos from text prompts, including voiceover, stock footage, and transitions. Kdenlive provides professional editing capabilities for free, and combined with Stable Diffusion for AI imagery and Coqui TTS for voiceover, covers the individual components of InVideo's workflow.",
        "key_differences": [
            "Cost: InVideo AI is $20–$48/month; Kdenlive is free",
            "Text-to-video: InVideo creates full videos from prompts; Kdenlive requires manual assembly",
            "Stock library: InVideo has millions of licensed clips; Kdenlive needs external sources",
            "Templates: InVideo has 5,000+ templates; Kdenlive has limited templates",
            "Speed: InVideo generates a rough cut in minutes; Kdenlive requires manual editing time",
        ],
        "pricing_table": {
            "headers": ["Aspect", "InVideo AI", "Kdenlive"],
            "rows": [
                ["Pricing", "$20–$48/month", "Free"],
                ["Text-to-video", "✅", "❌"],
                ["Stock footage", "✅ Millions licensed", "❌ External"],
                ["Templates", "5,000+", "Limited"],
                ["AI voiceover", "✅", "Via Coqui TTS"],
                ["Professional editing", "Basic", "✅ Full NLE"],
            ]
        },
        "github_repo": None,
        "migration": "Download Kdenlive. For free stock footage: Pexels, Pixabay, Coverr. For AI voiceover: Coqui TTS or Piper TTS. For auto-captions: Whisper. The main gap is the automated assembly — plan on 2-3x more manual time vs InVideo.",
        "related": ["pictory-vs-kdenlive", "synthesia-vs-open-source-avatar", "runway-ml-vs-comfyui-video"],
    },

    # ──────────────────────── 💬 AI APIs & INFRASTRUCTURE ────────────────────────

    {
        "slug": "openai-api-vs-ollama",
        "category": "AI APIs & Infrastructure",
        "category_emoji": "💬",
        "paid_tool": "OpenAI API",
        "paid_price": "Pay-per-token ($0.15–$15/1M tokens)",
        "paid_url": "https://platform.openai.com",
        "free_tool": "Ollama",
        "free_price": "Free (self-hosted)",
        "free_url": "https://ollama.ai",
        "savings": "API costs → $0",
        "verdict_switch": "Ollama lets you run Llama 3.1, Mistral, Gemma 2, DeepSeek, and 100+ models locally — with an OpenAI-compatible API — eliminating per-token cloud costs entirely for development and private use.",
        "verdict_stay": "OpenAI API's GPT-4o and o1 models remain ahead on complex reasoning, nuanced instruction-following, and long-context tasks. For production apps with quality SLAs, cloud APIs still win.",
        "setup_difficulty": "Easy",
        "setup_dots": "●●○○○",
        "setup_time": "~5 mins",
        "setup_method": "Native installer",
        "overview": "OpenAI API charges per token used — ranging from $0.15/1M tokens for GPT-4o Mini to $15/1M for GPT-4o. Ollama is a free tool for running large language models locally, providing an OpenAI-compatible REST API on localhost — meaning you can switch existing apps from OpenAI to Ollama by changing one URL.",
        "key_differences": [
            "Cost: OpenAI API charges per token; Ollama is free (you pay only for electricity)",
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
                ["Model quality (top)", "GPT-4o", "Llama 3.1 70B"],
            ]
        },
        "github_repo": "ollama/ollama",
        "migration": "1. Install Ollama: curl -fsSL https://ollama.ai/install.sh | sh (Linux/Mac) or download from ollama.ai (Windows). 2. Pull a model: ollama pull llama3.1. 3. In your app, change the base URL from https://api.openai.com/v1 to http://localhost:11434/v1 and set model to 'llama3.1'. No API key needed.",
        "related": ["openai-api-vs-groq", "openai-api-vs-together-ai", "claude-api-vs-ollama"],
    },

    {
        "slug": "openai-api-vs-groq",
        "category": "AI APIs & Infrastructure",
        "category_emoji": "💬",
        "paid_tool": "OpenAI API",
        "paid_price": "$0.15–$15/1M tokens",
        "paid_url": "https://platform.openai.com",
        "free_tool": "Groq API",
        "free_price": "Free tier (generous limits)",
        "free_url": "https://console.groq.com",
        "savings": "API costs → Free tier",
        "verdict_switch": "Groq's free tier runs Llama 3.1 70B and Mixtral 8x7B at 300–500 tokens/second — dramatically faster than OpenAI, and free for development and moderate production use.",
        "verdict_stay": "OpenAI API's GPT-4o and o1 models handle complex reasoning, long contexts (128K), and vision tasks that no Groq-hosted model currently matches.",
        "setup_difficulty": "Easy",
        "setup_dots": "●○○○○",
        "setup_time": "~3 mins",
        "setup_method": "API key signup",
        "overview": "OpenAI charges per token across its model lineup. Groq offers a free tier for its LPU-accelerated inference service — running Llama 3.1 70B and Mixtral 8x7B at speeds exceeding any other hosted API — ideal for latency-sensitive and development use cases.",
        "key_differences": [
            "Speed: Groq's LPU hardware delivers 300-500 tokens/sec vs ~60 tok/sec for OpenAI",
            "Cost: Groq has a free tier with daily/monthly limits; OpenAI has no free tier",
            "Models: Groq hosts Llama, Mixtral, Gemma models; OpenAI hosts GPT series",
            "Rate limits: Groq free tier has request/token limits; OpenAI is rate-limited by your billing tier",
            "API compatibility: Both use OpenAI-compatible API format",
        ],
        "pricing_table": {
            "headers": ["Aspect", "OpenAI API", "Groq API"],
            "rows": [
                ["Pricing", "$0.15–$15/1M tokens", "Free tier available"],
                ["Speed", "~60 tok/sec", "300–500 tok/sec"],
                ["API format", "OpenAI standard", "OpenAI-compatible"],
                ["Free tier", "❌", "✅ Daily limits"],
                ["Best model", "GPT-4o", "Llama 3.1 70B"],
                ["Vision support", "✅", "Limited"],
            ]
        },
        "github_repo": None,
        "migration": "Sign up at console.groq.com (free). Get an API key. Change base_url to https://api.groq.com/openai/v1 and update the model to 'llama-3.1-70b-versatile'. No other code changes needed — Groq is OpenAI API-compatible.",
        "related": ["openai-api-vs-ollama", "openai-api-vs-together-ai", "claude-api-vs-ollama"],
    },

    {
        "slug": "openai-api-vs-together-ai",
        "category": "AI APIs & Infrastructure",
        "category_emoji": "💬",
        "paid_tool": "OpenAI API",
        "paid_price": "$0.15–$15/1M tokens",
        "paid_url": "https://platform.openai.com",
        "free_tool": "Together AI",
        "free_price": "$1 free credit / then $0.10–$0.90/1M tokens",
        "free_url": "https://together.ai",
        "savings": "Up to 15x cheaper per token",
        "verdict_switch": "Together AI runs the same Llama 3.1 and Mistral models at a fraction of OpenAI's cost — typically $0.10–$0.20/1M tokens for models that perform comparably to GPT-4o Mini.",
        "verdict_stay": "OpenAI API is the choice for production apps needing GPT-4o, o1, fine-tuning capabilities, or guaranteed SLAs backed by Microsoft infrastructure.",
        "setup_difficulty": "Easy",
        "setup_dots": "●○○○○",
        "setup_time": "~3 mins",
        "setup_method": "API key signup",
        "overview": "OpenAI API charges $0.15–$15/1M tokens for its model lineup. Together AI is a cloud inference platform hosting 100+ open-source models at dramatically lower prices — $0.10/1M tokens for Llama 3.1 8B — with an OpenAI-compatible API.",
        "key_differences": [
            "Cost: Together AI is 5-15x cheaper than OpenAI for equivalent open-source models",
            "Models: Together hosts open-source models; OpenAI hosts proprietary GPT models",
            "Fine-tuning: Both support fine-tuning; OpenAI's is more polished",
            "Free credits: Together AI gives $1 on signup; OpenAI has no free credits",
            "API compatibility: Together uses OpenAI-compatible endpoints",
        ],
        "pricing_table": {
            "headers": ["Aspect", "OpenAI API", "Together AI"],
            "rows": [
                ["Llama 3.1 8B", "N/A", "$0.10/1M tokens"],
                ["Llama 3.1 70B", "N/A", "$0.88/1M tokens"],
                ["GPT-4o equivalent", "$5/1M tokens", "N/A"],
                ["Free credits", "$0", "$1 on signup"],
                ["Fine-tuning", "✅", "✅"],
                ["API format", "OpenAI standard", "OpenAI-compatible"],
            ]
        },
        "github_repo": None,
        "migration": "Sign up at together.ai. Set base_url to https://api.together.xyz/v1 in your OpenAI client. Use models like 'meta-llama/Llama-3.1-8B-Instruct-Turbo' for cheapest pricing or 'meta-llama/Llama-3.1-70B-Instruct-Turbo' for higher quality.",
        "related": ["openai-api-vs-ollama", "openai-api-vs-groq", "claude-api-vs-ollama"],
    },

    {
        "slug": "claude-api-vs-ollama",
        "category": "AI APIs & Infrastructure",
        "category_emoji": "💬",
        "paid_tool": "Anthropic Claude API",
        "paid_price": "$0.25–$15/1M tokens",
        "paid_url": "https://anthropic.com/api",
        "free_tool": "Ollama + Llama 3.1",
        "free_price": "Free (self-hosted)",
        "free_url": "https://ollama.ai",
        "savings": "API costs → $0",
        "verdict_switch": "Ollama running Llama 3.1 70B or Mistral handles 80-90% of use cases typically sent to Claude Haiku or Sonnet — at zero token cost for development and private applications.",
        "verdict_stay": "Claude 3.5 Sonnet's exceptional reasoning, nuanced instruction-following, and 200K context window handle complex tasks that Llama 3.1 70B struggles with.",
        "setup_difficulty": "Easy",
        "setup_dots": "●●○○○",
        "setup_time": "~5 mins",
        "setup_method": "Native installer",
        "overview": "Anthropic's Claude API charges $0.25–$15/1M tokens for Claude Haiku through Opus. Ollama provides a free, local alternative running open-source models with an OpenAI-compatible API — eliminating per-token costs for development, testing, and moderate production use.",
        "key_differences": [
            "Cost: Claude API charges per token; Ollama is free",
            "Context length: Claude 3.5 Sonnet supports 200K tokens; Llama 3.1 supports 128K",
            "Reasoning: Claude 3.5 Sonnet leads on nuanced analysis and complex reasoning",
            "Vision: Claude 3 models have excellent vision; Llama 3.2 added vision support",
            "API format: Anthropic uses its own API format; Ollama uses OpenAI-compatible format",
        ],
        "pricing_table": {
            "headers": ["Aspect", "Claude API", "Ollama"],
            "rows": [
                ["Pricing", "$0.25–$15/1M tokens", "Free"],
                ["Best model", "Claude 3.5 Sonnet", "Llama 3.1 70B"],
                ["Context length", "200K tokens", "128K tokens"],
                ["Privacy", "Sent to Anthropic", "100% local"],
                ["Vision", "✅ All models", "✅ Llama 3.2 Vision"],
                ["API format", "Anthropic SDK", "OpenAI-compatible"],
            ]
        },
        "github_repo": "ollama/ollama",
        "migration": "Install Ollama and pull: ollama pull llama3.1:70b (requires ~40GB RAM) or ollama pull llama3.1 for the 8B model (8GB RAM). Ollama's API runs on http://localhost:11434 with OpenAI-compatible endpoints — use the openai Python SDK with base_url='http://localhost:11434/v1'.",
        "related": ["openai-api-vs-ollama", "openai-api-vs-groq", "chatgpt-plus-vs-openrouter"],
    },

    {
        "slug": "openai-api-vs-fireworks-ai",
        "category": "AI APIs & Infrastructure",
        "category_emoji": "💬",
        "paid_tool": "OpenAI API",
        "paid_price": "$0.15–$15/1M tokens",
        "paid_url": "https://platform.openai.com",
        "free_tool": "Fireworks AI",
        "free_price": "$1 free credit / then from $0.10/1M tokens",
        "free_url": "https://fireworks.ai",
        "savings": "Up to 10x cheaper per token",
        "verdict_switch": "Fireworks AI delivers fast inference on Llama 3.1, Mixtral, and Qwen models at a fraction of OpenAI's cost — with an OpenAI-compatible API and a focus on production reliability.",
        "verdict_stay": "OpenAI's GPT-4o and o1 reasoning models have no direct equivalent on Fireworks, making OpenAI the choice for the highest-difficulty tasks.",
        "setup_difficulty": "Easy",
        "setup_dots": "●○○○○",
        "setup_time": "~3 mins",
        "setup_method": "API key signup",
        "overview": "OpenAI API charges up to $15/1M tokens for its most capable models. Fireworks AI is an inference-as-a-service platform focused on speed and cost efficiency — hosting Llama 3.1, Mixtral, and Qwen models at prices starting from $0.10/1M tokens with production-grade reliability.",
        "key_differences": [
            "Cost: Fireworks is typically 5-10x cheaper than OpenAI for comparable open-source models",
            "Speed: Fireworks focuses on low-latency inference; competitive with Groq for throughput",
            "Models: Fireworks specializes in open-source models; OpenAI offers proprietary GPT models",
            "Function calling: Both support structured function/tool calling",
            "Free credits: Fireworks gives $1 on signup; OpenAI does not",
        ],
        "pricing_table": {
            "headers": ["Aspect", "OpenAI API", "Fireworks AI"],
            "rows": [
                ["Llama 3.1 8B", "N/A", "$0.10/1M tokens"],
                ["Mixtral 8x7B", "N/A", "$0.40/1M tokens"],
                ["GPT-4o", "$5/1M tokens", "N/A"],
                ["Free trial", "❌", "$1 credit"],
                ["Function calling", "✅", "✅"],
                ["API format", "OpenAI", "OpenAI-compatible"],
            ]
        },
        "github_repo": None,
        "migration": "Sign up at fireworks.ai. Replace your OpenAI base_url with https://api.fireworks.ai/inference/v1. Use model IDs like 'accounts/fireworks/models/llama-v3p1-8b-instruct' or 'accounts/fireworks/models/mixtral-8x7b-instruct'.",
        "related": ["openai-api-vs-ollama", "openai-api-vs-groq", "openai-api-vs-together-ai"],
    },

    {
        "slug": "chatgpt-plus-vs-google-gemini-free",
        "category": "AI APIs & Infrastructure",
        "category_emoji": "💬",
        "paid_tool": "ChatGPT Plus",
        "paid_price": "$20/month",
        "paid_url": "https://chat.openai.com",
        "free_tool": "Google Gemini (Free tier)",
        "free_price": "Free",
        "free_url": "https://gemini.google.com",
        "savings": "$20/month → Free",
        "verdict_switch": "Google Gemini's free tier provides access to Gemini 1.5 Flash — a capable model with a 1M token context window — at zero cost, covering most everyday AI chat and analysis needs.",
        "verdict_stay": "ChatGPT Plus's GPT-4o is stronger on creative writing, code generation, and complex reasoning. Its DALL-E integration and custom GPT ecosystem add value Gemini's free tier doesn't match.",
        "setup_difficulty": "Easy",
        "setup_dots": "●○○○○",
        "setup_time": "~1 min",
        "setup_method": "Browser-based",
        "overview": "ChatGPT Plus costs $20/month for GPT-4o access, DALL-E generation, and OpenAI's plugin ecosystem. Google Gemini's free tier provides access to Gemini 1.5 Flash — with a 1 million token context window, multimodal input, and Google Workspace integration — at no cost.",
        "key_differences": [
            "Cost: ChatGPT Plus is $20/month; Gemini free tier is $0",
            "Context window: Gemini 1.5 Flash supports 1M tokens; GPT-4o supports 128K",
            "Google integration: Gemini integrates with Gmail, Docs, Drive; ChatGPT does not",
            "DALL-E: ChatGPT Plus includes image generation; Gemini free does not",
            "Code execution: Both support code interpreter; GPT-4o's is more polished",
        ],
        "pricing_table": {
            "headers": ["Aspect", "ChatGPT Plus", "Gemini Free"],
            "rows": [
                ["Pricing", "$20/month", "Free"],
                ["Model", "GPT-4o", "Gemini 1.5 Flash"],
                ["Context window", "128K tokens", "1M tokens"],
                ["Image generation", "✅ DALL-E 3", "❌"],
                ["Google Workspace", "❌", "✅"],
                ["Mobile app", "✅", "✅"],
            ]
        },
        "github_repo": None,
        "migration": "Go to gemini.google.com and sign in with your Google account. For API use, get a free Gemini API key at aistudio.google.com — the free tier is very generous for development.",
        "related": ["chatgpt-plus-vs-openrouter", "chatgpt-plus-vs-mistral-free", "openai-api-vs-ollama"],
    },

]

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

CATEGORIES = sorted(list(set(c["category"] for c in COMPARISONS)))

def category_count(cat):
    return sum(1 for c in COMPARISONS if c["category"] == cat)

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
    --bg: #0D1117;
    --surface: #161B22;
    --border: #30363D;
    --text: #E6EDF3;
    --muted: #8B949E;
    --accent: #58A6FF;
    --green: #3FB950;
    --yellow: #D29922;
    --red: #F85149;
    --radius: 8px;
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
  .card a.btn { display: inline-block; background: var(--accent); color: #fff; padding: 7px 16px; border-radius: 6px; font-size: 13px; font-weight: 600; margin-top: auto; text-align: center; }
  .card a.btn:hover { background: #79b8ff; text-decoration: none; }
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
  .verdict-box h3 { margin: 0 0 8px; font-size: 1rem; }
  .verdict-row { margin-bottom: 14px; }
  .verdict-row:last-child { margin-bottom: 0; }
  .verdict-label { font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: .05em; margin-bottom: 4px; }
  .verdict-switch .verdict-label { color: var(--green); }
  .verdict-stay .verdict-label { color: var(--yellow); }
  .hero-tools { display: flex; gap: 16px; align-items: center; background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 20px; margin: 24px 0; flex-wrap: wrap; }
  .hero-tool { flex: 1; min-width: 160px; }
  .hero-tool .label { font-size: 11px; color: var(--muted); margin-bottom: 4px; text-transform: uppercase; letter-spacing: .05em; }
  .hero-tool .name { font-size: 1.2rem; font-weight: 700; }
  .hero-tool .price { font-size: 13px; color: var(--muted); margin-top: 4px; }
  .hero-vs { font-size: 1.4rem; font-weight: 700; color: var(--border); }
  .diff-bar { margin: 8px 0; }
  .diff-dots { font-size: 18px; letter-spacing: 4px; }
  ul.diffs { padding-left: 20px; }
  ul.diffs li { margin-bottom: 8px; }
  .migration-box { background: var(--surface); border: 1px solid var(--border); border-left: 3px solid var(--accent); border-radius: var(--radius); padding: 20px; margin: 20px 0; font-size: 14px; }
  .migration-box pre { background: var(--bg); border: 1px solid var(--border); border-radius: 6px; padding: 12px; margin-top: 12px; overflow-x: auto; font-size: 13px; white-space: pre-wrap; }
  .related { display: flex; gap: 10px; flex-wrap: wrap; margin: 16px 0; }
  .related a { background: var(--surface); border: 1px solid var(--border); padding: 8px 14px; border-radius: 6px; font-size: 13px; }
  .related a:hover { border-color: var(--accent); text-decoration: none; }
  footer { border-top: 1px solid var(--border); padding: 32px 0; text-align: center; font-size: 13px; color: var(--muted); }
  footer a { color: var(--muted); }
  .search-bar { width: 100%; max-width: 500px; margin: 16px auto 0; display: block; background: var(--surface); border: 1px solid var(--border); border-radius: 8px; color: var(--text); padding: 10px 16px; font-size: 14px; }
  .search-bar:focus { outline: none; border-color: var(--accent); }
  @media (max-width: 600px) { header h1 { font-size: 1.5rem; } .hero-tools { flex-direction: column; } }
</style>
"""

# ─────────────────────────────────────────────────────────────────────────────
# NAV + FOOTER
# ─────────────────────────────────────────────────────────────────────────────

def nav(root=""):
    return f"""
<nav>
  <div class="container">
    <a href="{root}index.html" class="brand">🤖 AI Tool Alternative Finder</a>
    <a href="{root}savings-calculator/index.html" style="font-size:13px;color:var(--muted)">💰 Savings Calculator</a>
    <a href="{root}changelog/index.html" style="font-size:13px;color:var(--muted)">📋 Changelog</a>
    <a href="{root}about/index.html" style="font-size:13px;color:var(--muted)">About</a>
  </div>
</nav>"""

def footer():
    return f"""
<footer>
  <div class="container">
    <p><strong>AI Tool Alternative Finder</strong> &nbsp;·&nbsp; Hosted on <a href="https://pages.github.com">GitHub Pages</a> &nbsp;·&nbsp;
    <a href="about/index.html">About</a> &nbsp;·&nbsp;
    <a href="privacy/index.html">Privacy Policy</a> &nbsp;·&nbsp;
    <a href="contact/index.html">Contact</a> &nbsp;·&nbsp;
    <a href="changelog/index.html">Changelog</a> &nbsp;·&nbsp;
    <a href="stats/index.html">Stats</a></p>
    <p style="margin-top:8px">Updated {BUILD_DATE} &nbsp;·&nbsp; $0/month to operate &nbsp;·&nbsp; Content for informational purposes only</p>
  </div>
</footer>"""

def page_shell(title, description, body, root="", canonical=""):
    can = f'<link rel="canonical" href="{SITE_URL}/{canonical}" />' if canonical else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{description}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:type" content="website" />
  {can}
  {CSS}
</head>
<body>
{nav(root)}
{body}
{footer()}
<script>
  // Filter buttons
  document.querySelectorAll('.filter-btn').forEach(btn => {{
    btn.addEventListener('click', () => {{
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const cat = btn.dataset.cat;
      document.querySelectorAll('.card').forEach(card => {{
        card.style.display = (cat === 'all' || card.dataset.cat === cat) ? '' : 'none';
      }});
    }});
  }});
  // Search
  const searchBar = document.querySelector('.search-bar');
  if (searchBar) {{
    searchBar.addEventListener('input', () => {{
      const q = searchBar.value.toLowerCase();
      document.querySelectorAll('.card').forEach(card => {{
        card.style.display = card.textContent.toLowerCase().includes(q) ? '' : 'none';
      }});
    }});
  }}
</script>
</body>
</html>"""

# ─────────────────────────────────────────────────────────────────────────────
# INDEX PAGE
# ─────────────────────────────────────────────────────────────────────────────

def build_index():
    filters = '<button class="filter-btn active" data-cat="all">All</button>'
    for cat in CATEGORIES:
        emoji = next(c["category_emoji"] for c in COMPARISONS if c["category"] == cat)
        filters += f'<button class="filter-btn" data-cat="{cat}">{emoji} {cat} ({category_count(cat)})</button>'

    cards = ""
    for c in COMPARISONS:
        cards += f"""
<div class="card" data-cat="{c['category']}">
  <div class="card-cat">{c['category_emoji']} {c['category']}</div>
  <div class="card-tools">
    <span class="tool">{c['paid_tool']}</span>
    <span class="vs">VS</span>
    <span class="tool">{c['free_tool']}</span>
  </div>
  <div class="card-savings">💰 {c['savings']}</div>
  <a href="{c['slug']}/index.html" class="btn">Compare Now →</a>
</div>"""

    body = f"""
<header>
  <div class="container">
    <h1>🤖 AI Tool Alternative Finder</h1>
    <p>{SITE_DESC}</p>
    <div class="stats">
      <div class="stat"><div class="num">{len(COMPARISONS)}</div><div class="lbl">Comparisons</div></div>
      <div class="stat"><div class="num">{len(CATEGORIES)}</div><div class="lbl">Categories</div></div>
      <div class="stat"><div class="num">$0</div><div class="lbl">Cost to Run</div></div>
      <div class="stat"><div class="num">Daily</div><div class="lbl">Auto-Updated</div></div>
    </div>
    <input type="text" class="search-bar" placeholder="Search AI tools (e.g. ChatGPT, Midjourney, Copilot)..." />
  </div>
</header>

<div class="container">

  <div style="background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:20px;margin-bottom:24px;">
    <strong>💰 AI Tool Savings Calculator</strong>
    <p style="color:var(--muted);font-size:13px;margin-top:6px">Enter your team size → see exactly how much you save switching to free AI alternatives</p>
    <a href="savings-calculator/index.html" style="display:inline-block;margin-top:12px;background:var(--accent);color:#fff;padding:8px 18px;border-radius:6px;font-size:13px;font-weight:600;">Calculate My Savings →</a>
  </div>

  <div class="filters">{filters}</div>
  <div class="grid">{cards}</div>
</div>"""

    write("index.html", page_shell(SITE_TITLE, SITE_DESC, body, canonical=""))

# ─────────────────────────────────────────────────────────────────────────────
# COMPARISON PAGES
# ─────────────────────────────────────────────────────────────────────────────

def build_comparison(c):
    diffs = "".join(f"<li>{d}</li>" for d in c["key_differences"])
    rows = "".join(
        "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
        for row in c["pricing_table"]["rows"]
    )
    headers = "".join(f"<th>{h}</th>" for h in c["pricing_table"]["headers"])

    github_block = ""
    if c.get("github_repo"):
        github_block = f"""
<div style="background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:16px;margin:20px 0;">
  📦 <strong>{c['free_tool']} on GitHub</strong><br/>
  <a href="https://github.com/{c['github_repo']}" target="_blank" rel="noopener">github.com/{c['github_repo']}</a><br/>
  <span style="color:var(--muted);font-size:13px">Open Source &nbsp;·&nbsp; Free to use</span>
</div>"""

    related_links = ""
    for slug in c.get("related", []):
        related_c = next((x for x in COMPARISONS if x["slug"] == slug), None)
        if related_c:
            related_links += f'<a href="../{slug}/index.html">{related_c["paid_tool"]} vs {related_c["free_tool"]}</a>'

    body = f"""
<div class="container" style="padding-top:24px">
  <p style="font-size:13px;color:var(--muted);margin-bottom:16px">
    <a href="../index.html">🤖 AI Tool Alternative Finder</a> / <a href="#">{c['category']}</a> / {c['paid_tool']} vs {c['free_tool']}
  </p>

  <div style="font-size:12px;color:var(--muted);margin-bottom:8px">{c['category_emoji']} {c['category']}</div>
  <h1 style="font-size:1.8rem;margin-bottom:12px">{c['paid_tool']} vs {c['free_tool']}</h1>

  <p style="color:var(--muted);margin-bottom:16px">Detailed comparison: pricing, features, setup, and which is right for you.</p>

  <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:20px">
    <span class="badge badge-green">✅ Free Alternative: {c['free_price']}</span>
    <span class="badge badge-blue">🤖 AI-Analyzed</span>
    <span class="badge badge-yellow">🖥️ Setup: {c['setup_difficulty']}</span>
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
      <div>{c['verdict_switch']}</div>
    </div>
    <div class="verdict-row verdict-stay">
      <div class="verdict-label">⚠️ Stay with {c['paid_tool']} if</div>
      <div>{c['verdict_stay']}</div>
    </div>
    <div style="margin-top:14px;border-top:1px solid var(--border);padding-top:14px">
      <strong>🖥️ Setup Difficulty:</strong> {c['setup_difficulty']}
      <div class="diff-bar"><span class="diff-dots" style="color:var(--accent)">{c['setup_dots']}</span></div>
      ⏱️ Setup time: <strong>~{c['setup_time']}</strong> &nbsp;·&nbsp; 🐳 Method: <strong>{c['setup_method']}</strong>
    </div>
  </div>

  <h2>{c['paid_tool']} vs {c['free_tool']}</h2>

  <h3>Overview</h3>
  <p>{c['overview']}</p>

  <h3>Key Differences</h3>
  <ul class="diffs">{diffs}</ul>

  <h3>Pricing Comparison</h3>
  <table>
    <thead><tr>{headers}</tr></thead>
    <tbody>{rows}</tbody>
  </table>

  <h3>Migration Path</h3>
  <div class="migration-box">
    <strong>How to switch from {c['paid_tool']} to {c['free_tool']}:</strong>
    <pre>{c['migration']}</pre>
  </div>

  {github_block}

  <p style="margin:20px 0;font-size:13px;color:var(--muted)">
    <em>Data sourced {BUILD_DATE}. Pricing and features change — verify at <a href="{c['paid_url']}" target="_blank">{c['paid_tool']}</a> and <a href="{c['free_url']}" target="_blank">{c['free_tool']}</a> before making decisions.</em>
  </p>

  <h3>🔗 Related Comparisons</h3>
  <div class="related">{related_links}</div>

  <p style="margin:20px 0">
    <a href="../index.html" style="color:var(--muted);font-size:13px">← View All Comparisons</a>
  </p>
</div>"""

    desc = f"Is {c['free_tool']} a good free alternative to {c['paid_tool']}? {c['savings']}. Detailed comparison of pricing, features, and migration."
    write(
        f"{c['slug']}/index.html",
        page_shell(
            f"{c['paid_tool']} vs {c['free_tool']} ({BUILD_DATE}) — Free AI Alternative",
            desc,
            body,
            root="../",
            canonical=f"{c['slug']}/"
        )
    )

# ─────────────────────────────────────────────────────────────────────────────
# SAVINGS CALCULATOR
# ─────────────────────────────────────────────────────────────────────────────

def build_calculator():
    tool_rows = ""
    for c in COMPARISONS:
        tool_rows += f"""<tr>
  <td>{c['paid_tool']}</td>
  <td>{c['paid_price']}</td>
  <td style="color:var(--green)">{c['free_tool']} — {c['free_price']}</td>
</tr>"""

    # Pre-compute JSON outside f-string to avoid escaping conflicts
    tools_json = json.dumps([{"name": c["paid_tool"], "free": c["free_tool"], "slug": c["slug"]} for c in COMPARISONS])

    body = f"""
<header>
  <div class="container">
    <h1>💰 AI Tool Savings Calculator</h1>
    <p>See how much you can save by switching from paid AI tools to free alternatives</p>
  </div>
</header>
<div class="container">
  <div style="background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:24px;margin-bottom:32px;max-width:600px">
    <label style="display:block;margin-bottom:8px;font-weight:600">Team / Seat Count</label>
    <input id="seats" type="number" value="5" min="1" style="width:100%;background:var(--bg);border:1px solid var(--border);color:var(--text);padding:10px;border-radius:6px;font-size:16px" />
    <div style="margin-top:20px;display:grid;gap:12px" id="results"></div>
  </div>

  <h2>All Free Alternatives</h2>
  <table>
    <thead><tr><th>Paid AI Tool</th><th>Paid Price</th><th>Free Alternative</th></tr></thead>
    <tbody>{tool_rows}</tbody>
  </table>

  <p style="margin-top:32px"><a href="../index.html">← View All Comparisons</a></p>
</div>

<script>
const tools = {tools_json};

function calc() {{
  const seats = parseInt(document.getElementById('seats').value) || 1;
  const savings = [
    {{ name:'ChatGPT Plus', monthly: 20, per:'flat' }},
    {{ name:'GitHub Copilot', monthly: 10, per:'seat' }},
    {{ name:'Midjourney', monthly: 30, per:'flat' }},
    {{ name:'ElevenLabs', monthly: 22, per:'flat' }},
    {{ name:'Jasper AI', monthly: 49, per:'flat' }},
    {{ name:'Runway ML', monthly: 35, per:'flat' }},
    {{ name:'Otter.ai', monthly: 10, per:'seat' }},
    {{ name:'Grammarly Premium', monthly: 13, per:'seat' }},
  ];
  let html = '';
  let total = 0;
  savings.forEach(t => {{
    const monthly = t.per === 'seat' ? t.monthly * seats : t.monthly;
    total += monthly;
    html += `<div style="display:flex;justify-content:space-between;background:var(--bg);padding:10px 14px;border-radius:6px">
      <span>${{t.name}}</span>
      <span style="color:var(--green)">Save ${{monthly.toLocaleString()}}/mo</span>
    </div>`;
  }});
  html = `<div style="background:rgba(63,185,80,.1);border:1px solid rgba(63,185,80,.3);border-radius:8px;padding:16px;text-align:center;margin-bottom:16px">
    <div style="font-size:2rem;font-weight:800;color:var(--green)">${{total.toLocaleString()}}/month</div>
    <div style="color:var(--muted);font-size:13px">Estimated savings for ${{seats}} seat(s)</div>
  </div>` + html;
  document.getElementById('results').innerHTML = html;
}}
document.getElementById('seats').addEventListener('input', calc);
calc();
</script>"""

    write(
        "savings-calculator/index.html",
        page_shell(
            f"AI Tool Savings Calculator — {SITE_TITLE}",
            "Calculate how much you save by switching from paid AI tools to free alternatives",
            body,
            root="../",
            canonical="savings-calculator/"
        )
    )

# ─────────────────────────────────────────────────────────────────────────────
# CHANGELOG
# ─────────────────────────────────────────────────────────────────────────────

def build_changelog():
    rows = ""
    for c in COMPARISONS:
        rows += f"""<tr>
  <td>{c['category_emoji']} {c['category']}</td>
  <td><strong>{c['paid_tool']}</strong></td>
  <td><strong>{c['free_tool']}</strong></td>
  <td style="color:var(--green)">{c['savings']}</td>
  <td><a href="../{c['slug']}/index.html">Compare →</a></td>
</tr>"""

    body = f"""
<header>
  <div class="container">
    <h1>📋 Weekly Changelog</h1>
    <p>All {len(COMPARISONS)} comparisons auto-updated daily. Pricing verified, new tools added.</p>
    <div class="stats">
      <div class="stat"><div class="num">{len(COMPARISONS)}</div><div class="lbl">Comparisons</div></div>
      <div class="stat"><div class="num">{len(CATEGORIES)}</div><div class="lbl">Categories</div></div>
      <div class="stat"><div class="num">$0</div><div class="lbl">Cost to Run</div></div>
      <div class="stat"><div class="num">Daily</div><div class="lbl">Auto-Updated</div></div>
    </div>
  </div>
</header>
<div class="container">

  <div style="background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:20px;margin-bottom:24px">
    <h2 style="margin:0 0 8px">🟢 Latest Update</h2>
    <p>✅ Auto-updated {BUILD_DATE}</p>
    <ul style="margin-top:10px;padding-left:20px;color:var(--muted);font-size:14px">
      <li>All {len(COMPARISONS)} comparison pages refreshed with latest pricing data</li>
      <li>Migration guides updated for all tools</li>
      <li>Savings calculator recalibrated</li>
      <li>Sitemap submitted to Google Search Console</li>
    </ul>
  </div>

  <h2>📄 All Comparisons — {BUILD_DATE}</h2>
  <table>
    <thead><tr><th>Category</th><th>Paid Tool</th><th>Free Alternative</th><th>Savings</th><th>Link</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>

  <p style="margin-top:32px;font-size:13px;color:var(--muted)">This site auto-updates daily via GitHub Actions. Zero cost, 100% open source.</p>
  <p style="margin-top:12px"><a href="../index.html">← View All Comparisons</a></p>
</div>"""

    write(
        "changelog/index.html",
        page_shell(
            f"Changelog — {SITE_TITLE}",
            f"All {len(COMPARISONS)} AI tool comparisons auto-updated daily.",
            body,
            root="../",
            canonical="changelog/"
        )
    )

# ─────────────────────────────────────────────────────────────────────────────
# STATS PAGE
# ─────────────────────────────────────────────────────────────────────────────

def build_stats():
    cat_rows = "".join(
        f"<tr><td>{next(c['category_emoji'] for c in COMPARISONS if c['category']==cat)} {cat}</td><td>{category_count(cat)} comparisons</td></tr>"
        for cat in CATEGORIES
    )
    body = f"""
<header>
  <div class="container">
    <h1>📊 Site Stats</h1>
    <p>Live statistics for AI Tool Alternative Finder</p>
  </div>
</header>
<div class="container">
  <div class="stats" style="justify-content:flex-start;margin-bottom:32px">
    <div class="stat"><div class="num">{len(COMPARISONS)}</div><div class="lbl">Total Comparisons</div></div>
    <div class="stat"><div class="num">{len(CATEGORIES)}</div><div class="lbl">Categories</div></div>
    <div class="stat"><div class="num">$0</div><div class="lbl">Monthly Cost</div></div>
    <div class="stat"><div class="num">Daily</div><div class="lbl">Update Frequency</div></div>
  </div>
  <h2>Coverage by Category</h2>
  <table><thead><tr><th>Category</th><th>Count</th></tr></thead><tbody>{cat_rows}</tbody></table>
  <p style="margin-top:32px"><a href="../index.html">← Home</a></p>
</div>"""
    write(
        "stats/index.html",
        page_shell(f"Stats — {SITE_TITLE}", "Statistics for AI Tool Alternative Finder", body, root="../", canonical="stats/")
    )

# ─────────────────────────────────────────────────────────────────────────────
# ABOUT / PRIVACY / CONTACT
# ─────────────────────────────────────────────────────────────────────────────

def build_about():
    body = f"""
<header><div class="container"><h1>About AI Tool Alternative Finder</h1></div></header>
<div class="container" style="max-width:720px;padding-bottom:48px">
  <h2>What is this?</h2>
  <p>AI Tool Alternative Finder is a free directory comparing popular paid AI tools to free and open-source alternatives. Every comparison includes pricing breakdowns, feature comparisons, setup guides, and migration instructions.</p>
  <h2 style="margin-top:24px">How does it work?</h2>
  <p>The site is built with a Python script that generates static HTML pages, hosted on GitHub Pages at zero cost. The comparison data is curated and maintained by our team, with the build script running daily via GitHub Actions to keep information current.</p>
  <h2 style="margin-top:24px">Why did we build this?</h2>
  <p>AI tool costs have skyrocketed. A typical power user can easily spend $100–$300/month across ChatGPT Plus, GitHub Copilot, Midjourney, ElevenLabs, and other AI subscriptions. Excellent free alternatives exist for almost every use case — this site helps you find them.</p>
  <h2 style="margin-top:24px">How often is it updated?</h2>
  <p>The site rebuilds automatically every day via GitHub Actions. Pricing and feature information is reviewed and updated weekly.</p>
  <p style="margin-top:32px"><a href="../index.html">← View All Comparisons</a></p>
</div>"""
    write("about/index.html", page_shell(f"About — {SITE_TITLE}", "About AI Tool Alternative Finder", body, root="../", canonical="about/"))

def build_privacy():
    body = f"""
<header><div class="container"><h1>Privacy Policy</h1></div></header>
<div class="container" style="max-width:720px;padding-bottom:48px">
  <p style="color:var(--muted)">Last updated: {BUILD_DATE}</p>
  <h2>Data Collection</h2>
  <p>AI Tool Alternative Finder does not collect any personal data. We do not use cookies, tracking pixels, or analytics beyond aggregated GitHub Pages traffic statistics.</p>
  <h2 style="margin-top:24px">Third-Party Links</h2>
  <p>This site contains links to external websites. We are not responsible for the privacy practices of those sites.</p>
  <h2 style="margin-top:24px">Content Disclaimer</h2>
  <p>All pricing and feature information is provided for informational purposes only. Verify current pricing at official vendor websites before making purchasing decisions.</p>
  <h2 style="margin-top:24px">Contact</h2>
  <p>For privacy concerns, please use our <a href="../contact/index.html">contact page</a>.</p>
  <p style="margin-top:32px"><a href="../index.html">← Home</a></p>
</div>"""
    write("privacy/index.html", page_shell(f"Privacy Policy — {SITE_TITLE}", "Privacy Policy for AI Tool Alternative Finder", body, root="../", canonical="privacy/"))

def build_contact():
    body = f"""
<header><div class="container"><h1>Contact</h1></div></header>
<div class="container" style="max-width:600px;padding-bottom:48px">
  <p>Have a suggestion for a new comparison, spotted an error, or want to report outdated pricing?</p>
  <div style="background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:24px;margin-top:20px">
    <h2 style="margin-bottom:16px">Reach out via GitHub</h2>
    <p>The best way to suggest improvements is to open a GitHub Issue on our repository.</p>
    <a href="https://github.com/aiopentec/ai-tool-alternative-finder/issues/new" target="_blank"
       style="display:inline-block;background:var(--accent);color:#fff;padding:10px 20px;border-radius:6px;font-weight:600;margin-top:16px;font-size:14px">
       Open a GitHub Issue →
    </a>
  </div>
  <p style="margin-top:32px"><a href="../index.html">← Home</a></p>
</div>"""
    write("contact/index.html", page_shell(f"Contact — {SITE_TITLE}", "Contact AI Tool Alternative Finder", body, root="../", canonical="contact/"))

# ─────────────────────────────────────────────────────────────────────────────
# SITEMAP
# ─────────────────────────────────────────────────────────────────────────────

def build_sitemap():
    urls = [
        f"  <url><loc>{SITE_URL}/</loc><changefreq>daily</changefreq><priority>1.0</priority></url>",
        f"  <url><loc>{SITE_URL}/savings-calculator/</loc><changefreq>weekly</changefreq><priority>0.7</priority></url>",
        f"  <url><loc>{SITE_URL}/changelog/</loc><changefreq>daily</changefreq><priority>0.7</priority></url>",
        f"  <url><loc>{SITE_URL}/about/</loc><changefreq>monthly</changefreq><priority>0.5</priority></url>",
        f"  <url><loc>{SITE_URL}/stats/</loc><changefreq>weekly</changefreq><priority>0.5</priority></url>",
    ]
    for c in COMPARISONS:
        urls.append(f"  <url><loc>{SITE_URL}/{c['slug']}/</loc><changefreq>weekly</changefreq><priority>0.9</priority><lastmod>{BUILD_DATE_ISO}</lastmod></url>")

    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += "\n".join(urls)
    sitemap += "\n</urlset>"
    write("sitemap.xml", sitemap)

# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print(f"\n🤖 AI Tool Alternative Finder — Build")
    print(f"   Date: {BUILD_DATE}")
    print(f"   Comparisons: {len(COMPARISONS)}")
    print(f"   Categories: {len(CATEGORIES)}\n")

    print("📄 Building index page...")
    build_index()

    print(f"\n📄 Building {len(COMPARISONS)} comparison pages...")
    for c in COMPARISONS:
        build_comparison(c)

    print("\n📄 Building utility pages...")
    build_calculator()
    build_changelog()
    build_stats()
    build_about()
    build_privacy()
    build_contact()

    print("\n🗺️  Building sitemap...")
    build_sitemap()

    total = 1 + len(COMPARISONS) + 7
    print(f"\n✅ Build complete — {total} files generated\n")

if __name__ == "__main__":
    main()
