"""
expand_tool_pairs.py
  python expand_tool_pairs.py

Adds 72 new pairs to data/tool_pairs.json, taking total from 58 → 130.
Adds all required new tool definitions to the tools object.
Creates data/tool_pairs.json.bak before writing.
"""

import json
import shutil
from pathlib import Path

FILE = Path("data/tool_pairs.json")
BAK  = Path("data/tool_pairs.json.bak")

if not FILE.exists():
    raise SystemExit("ERROR: data/tool_pairs.json not found.")

shutil.copy(FILE, BAK)
print(f"✅ Backup → {BAK}\n")

data = json.loads(FILE.read_text(encoding="utf-8"))

# ── NEW TOOL DEFINITIONS ──────────────────────────────────────────────────────

NEW_TOOLS = {

    # ── PAID TOOLS ──────────────────────────────────────────────────────────

    "poe-premium": {
        "name": "Poe Premium",
        "category": "text-generation",
        "pricing": "$19.99/month",
        "license": "Proprietary",
        "website": "https://poe.com",
        "description": "Quora's AI chat aggregator giving access to Claude, GPT-4o, Gemini, and custom bots. Premium removes limits and adds exclusive models.",
        "company": "Quora",
        "founded": "2022"
    },
    "character-ai": {
        "name": "Character.AI",
        "category": "text-generation",
        "pricing": "Free / $9.99/month (c.ai+)",
        "license": "Proprietary",
        "website": "https://character.ai",
        "description": "AI platform for creating and chatting with custom AI personas and characters. 20 million daily active users. Popular for entertainment and roleplay.",
        "company": "Character.AI",
        "founded": "2021"
    },
    "quillbot-premium": {
        "name": "QuillBot Premium",
        "category": "text-generation",
        "pricing": "$9.95/month",
        "license": "Proprietary",
        "website": "https://quillbot.com",
        "description": "AI writing assistant for paraphrasing, grammar checking, summarising, and citation generation. Used by 35 million monthly users.",
        "company": "QuillBot",
        "founded": "2017"
    },
    "wordtune": {
        "name": "Wordtune",
        "category": "text-generation",
        "pricing": "$9.99/month",
        "license": "Proprietary",
        "website": "https://wordtune.com",
        "description": "AI writing companion that rewrites, shortens, and expands sentences. Browser extension integrates into Google Docs, Gmail, and social media.",
        "company": "AI21 Labs",
        "founded": "2020"
    },
    "you-pro": {
        "name": "You.com Pro",
        "category": "research-ai",
        "pricing": "$15/month",
        "license": "Proprietary",
        "website": "https://you.com",
        "description": "AI-powered search and assistant with access to GPT-4o, Claude, and web search. Combines search results with AI chat for research workflows.",
        "company": "You.com",
        "founded": "2020"
    },
    "amazon-codewhisperer": {
        "name": "Amazon Q Developer",
        "category": "code-assistance",
        "pricing": "Free (individual) / $19/month (Pro)",
        "license": "Proprietary",
        "website": "https://aws.amazon.com/q/developer/",
        "description": "AWS AI coding assistant (formerly CodeWhisperer) with inline code suggestions, security scanning, and AWS service integration.",
        "company": "Amazon",
        "founded": "2022"
    },
    "replit-ai": {
        "name": "Replit AI",
        "category": "code-assistance",
        "pricing": "$25/month (Core)",
        "license": "Proprietary",
        "website": "https://replit.com/ai",
        "description": "AI-powered cloud IDE with code generation, explanation, and debugging. Instant deployment and built-in multiplayer collaboration.",
        "company": "Replit",
        "founded": "2021"
    },
    "supermaven-paid": {
        "name": "Supermaven Pro",
        "category": "code-assistance",
        "pricing": "$10/month",
        "license": "Proprietary",
        "website": "https://supermaven.com",
        "description": "Ultra-fast AI code completion with 1M token context window. 2x faster than Copilot with whole-codebase awareness. VS Code and JetBrains.",
        "company": "Supermaven",
        "founded": "2023"
    },
    "leonardo-ai": {
        "name": "Leonardo AI",
        "category": "image-generation",
        "pricing": "$12–$48/month",
        "license": "Proprietary",
        "website": "https://leonardo.ai",
        "description": "AI image generation platform with fine-tuned models for game assets, concept art, and marketing. Used by game studios and creative professionals.",
        "company": "Leonardo AI",
        "founded": "2022"
    },
    "ideogram": {
        "name": "Ideogram",
        "category": "image-generation",
        "pricing": "$8–$25/month",
        "license": "Proprietary",
        "website": "https://ideogram.ai",
        "description": "AI image generator that excels at text rendering inside images — logos, posters, and typography. A direct challenge to Midjourney for design work.",
        "company": "Ideogram AI",
        "founded": "2023"
    },
    "playground-ai": {
        "name": "Playground AI",
        "category": "image-generation",
        "pricing": "Free / $15–$45/month",
        "license": "Proprietary",
        "website": "https://playground.com",
        "description": "Consumer-friendly AI image creation and editing tool. Combines AI generation with a design canvas for social media graphics and art.",
        "company": "Playground AI",
        "founded": "2022"
    },
    "pika-labs": {
        "name": "Pika Labs",
        "category": "video-ai",
        "pricing": "$8–$28/month",
        "license": "Proprietary",
        "website": "https://pika.art",
        "description": "AI video generation from text and images. Known for fast iteration and creative video effects. Competes with Runway and Kling.",
        "company": "Pika Labs",
        "founded": "2023"
    },
    "heygen": {
        "name": "HeyGen",
        "category": "video-ai",
        "pricing": "$29–$89/month",
        "license": "Proprietary",
        "website": "https://heygen.com",
        "description": "AI avatar video creation platform. Create talking-head videos in 175 languages from text. Used for training, marketing, and localisation videos.",
        "company": "HeyGen",
        "founded": "2020"
    },
    "loom-ai": {
        "name": "Loom AI",
        "category": "video-ai",
        "pricing": "$12.50–$16/month",
        "license": "Proprietary",
        "website": "https://loom.com",
        "description": "Screen recording with AI features: auto-generated titles, summaries, action items, and filler word removal. Used by 25 million people.",
        "company": "Loom (Atlassian)",
        "founded": "2015"
    },
    "suno-ai": {
        "name": "Suno AI",
        "category": "audio-ai",
        "pricing": "$8–$24/month",
        "license": "Proprietary",
        "website": "https://suno.com",
        "description": "AI music generation from text prompts. Creates complete songs with vocals and instrumentation in seconds. The leading AI music creation tool.",
        "company": "Suno AI",
        "founded": "2023"
    },
    "udio": {
        "name": "Udio",
        "category": "audio-ai",
        "pricing": "$10–$30/month",
        "license": "Proprietary",
        "website": "https://udio.com",
        "description": "AI music generation platform creating high-quality songs from text descriptions. Praised for musical coherence and production quality.",
        "company": "Udio",
        "founded": "2024"
    },
    "fireflies-ai": {
        "name": "Fireflies.ai",
        "category": "audio-ai",
        "pricing": "$10–$19/month",
        "license": "Proprietary",
        "website": "https://fireflies.ai",
        "description": "AI meeting assistant that records, transcribes, and summarises meetings. Integrates with Zoom, Teams, and Google Meet. Searchable meeting database.",
        "company": "Fireflies.ai",
        "founded": "2016"
    },
    "krisp": {
        "name": "Krisp",
        "category": "audio-ai",
        "pricing": "$8/month",
        "license": "Proprietary",
        "website": "https://krisp.ai",
        "description": "AI noise cancellation app that removes background noise and echo in real time from any voice app — Zoom, Teams, Discord, and more.",
        "company": "Krisp Technologies",
        "founded": "2017"
    },
    "zapier-ai": {
        "name": "Zapier (AI features)",
        "category": "productivity-ai",
        "pricing": "$19.99–$69/month",
        "license": "Proprietary",
        "website": "https://zapier.com",
        "description": "No-code automation platform with AI features for building workflows, chatbots, and data processing pipelines across 7,000+ apps.",
        "company": "Zapier",
        "founded": "2011"
    },
    "make-com": {
        "name": "Make.com",
        "category": "productivity-ai",
        "pricing": "$9–$29/month",
        "license": "Proprietary",
        "website": "https://make.com",
        "description": "Visual workflow automation platform with AI integration modules. Connects 1,500+ apps with drag-and-drop scenario builder.",
        "company": "Make (Celonis)",
        "founded": "2012"
    },
    "mem-ai": {
        "name": "Mem.ai",
        "category": "productivity-ai",
        "pricing": "$14.99/month",
        "license": "Proprietary",
        "website": "https://mem.ai",
        "description": "AI-powered personal knowledge base that auto-organises notes and surfaces relevant information. Chat with your notes using built-in AI.",
        "company": "Mem Labs",
        "founded": "2020"
    },
    "intercom-fin": {
        "name": "Intercom Fin AI",
        "category": "productivity-ai",
        "pricing": "$39/month + $0.99/resolution",
        "license": "Proprietary",
        "website": "https://intercom.com/fin",
        "description": "AI customer service agent that resolves 50%+ of support queries instantly. Trained on your content and seamlessly hands off to human agents.",
        "company": "Intercom",
        "founded": "2023"
    },
    "drift-ai": {
        "name": "Drift AI",
        "category": "productivity-ai",
        "pricing": "$2,500/month (enterprise)",
        "license": "Proprietary",
        "website": "https://drift.com",
        "description": "AI-powered conversational marketing and sales platform. Qualifies leads, books meetings, and personalises buyer journeys 24/7.",
        "company": "Drift (Salesloft)",
        "founded": "2014"
    },

    # ── FREE TOOLS ───────────────────────────────────────────────────────────

    "sillytavern": {
        "name": "SillyTavern",
        "category": "text-generation",
        "pricing": "Free (self-hosted)",
        "license": "AGPL 3.0",
        "website": "https://github.com/SillyTavern/SillyTavern",
        "description": "Advanced open-source frontend for AI characters and roleplay. Connects to any LLM backend with rich persona, lorebook, and extension system.",
        "github": "SillyTavern/SillyTavern",
        "stars_approx": "8k"
    },
    "perplexica": {
        "name": "Perplexica",
        "category": "research-ai",
        "pricing": "Free (self-hosted)",
        "license": "MIT",
        "website": "https://github.com/ItzCrazyKns/Perplexica",
        "description": "Open-source AI search engine — a self-hostable Perplexity alternative. Uses SearXNG for web search and any LLM for answer synthesis.",
        "github": "ItzCrazyKns/Perplexica",
        "stars_approx": "17k"
    },
    "flux-1": {
        "name": "Flux.1",
        "category": "image-generation",
        "pricing": "Free (local)",
        "license": "Apache 2.0 (Schnell) / Dev license (Dev)",
        "website": "https://blackforestlabs.ai",
        "description": "State-of-the-art open-weight image generation model from Black Forest Labs. FLUX.1 [schnell] outperforms Midjourney v6 and DALL-E 3 on benchmarks.",
        "github": "black-forest-labs/flux",
        "stars_approx": "19k"
    },
    "cogvideox": {
        "name": "CogVideoX",
        "category": "video-ai",
        "pricing": "Free (local)",
        "license": "Apache 2.0",
        "website": "https://github.com/THUDM/CogVideo",
        "description": "Open-source text-to-video generation model from Tsinghua University. Generates 6-second 480p videos from text prompts with temporal consistency.",
        "github": "THUDM/CogVideo",
        "stars_approx": "6k"
    },
    "sadtalker": {
        "name": "SadTalker",
        "category": "video-ai",
        "pricing": "Free (local)",
        "license": "MIT",
        "website": "https://github.com/OpenTalker/SadTalker",
        "description": "AI talking head generator that animates a single photo using audio. Creates realistic lip-sync video from any portrait + audio file, runs locally.",
        "github": "OpenTalker/SadTalker",
        "stars_approx": "13k"
    },
    "wav2lip": {
        "name": "Wav2Lip",
        "category": "video-ai",
        "pricing": "Free (local)",
        "license": "MIT",
        "website": "https://github.com/Rudrabha/Wav2Lip",
        "description": "Lip-sync any video to any audio with near-perfect accuracy. Open-source talking face generation for creating multilingual video dubbing locally.",
        "github": "Rudrabha/Wav2Lip",
        "stars_approx": "10k"
    },
    "obs-whisper": {
        "name": "OBS + Whisper",
        "category": "video-ai",
        "pricing": "Free (local)",
        "license": "GPL 2.0 / MIT",
        "website": "https://obsproject.com",
        "description": "OBS Studio for free screen recording and streaming, combined with OpenAI Whisper for automatic transcription. Full Loom alternative at zero cost.",
        "github": "obsproject/obs-studio",
        "stars_approx": "58k"
    },
    "musicgen": {
        "name": "MusicGen",
        "category": "audio-ai",
        "pricing": "Free (local)",
        "license": "MIT",
        "website": "https://huggingface.co/facebook/musicgen-large",
        "description": "Meta AI's open-source music generation model. Generate high-quality music from text descriptions. Available via Hugging Face and runs locally.",
        "github": "facebookresearch/audiocraft",
        "stars_approx": "21k"
    },
    "audiocraft": {
        "name": "AudioCraft",
        "category": "audio-ai",
        "pricing": "Free (local)",
        "license": "MIT",
        "website": "https://github.com/facebookresearch/audiocraft",
        "description": "Meta AI's open-source audio generation library including MusicGen and AudioGen. Generate music and sound effects from text. Runs locally on GPU.",
        "github": "facebookresearch/audiocraft",
        "stars_approx": "21k"
    },
    "deepfilternet": {
        "name": "DeepFilterNet",
        "category": "audio-ai",
        "pricing": "Free (local)",
        "license": "MIT",
        "website": "https://github.com/Rikorose/DeepFilterNet",
        "description": "Real-time speech enhancement using deep learning. Removes background noise with near-Krisp quality, running locally with no subscription.",
        "github": "Rikorose/DeepFilterNet",
        "stars_approx": "3k"
    },
    "rnnoise": {
        "name": "RNNoise",
        "category": "audio-ai",
        "pricing": "Free",
        "license": "BSD 3-Clause",
        "website": "https://github.com/xiph/rnnoise",
        "description": "Mozilla's open-source noise suppression library using a recurrent neural network. Lightweight, real-time noise reduction used by Zoom and Jitsi.",
        "github": "xiph/rnnoise",
        "stars_approx": "4k"
    },
    "buzz": {
        "name": "Buzz",
        "category": "audio-ai",
        "pricing": "Free (local)",
        "license": "MIT",
        "website": "https://github.com/chidiwilliams/buzz",
        "description": "Desktop app for transcribing audio and video using OpenAI Whisper locally. Clean GUI for Mac, Windows, Linux with real-time transcription.",
        "github": "chidiwilliams/buzz",
        "stars_approx": "12k"
    },
    "n8n": {
        "name": "n8n",
        "category": "productivity-ai",
        "pricing": "Free (self-hosted) / $24/month (cloud)",
        "license": "Sustainable Use License",
        "website": "https://n8n.io",
        "description": "Open-source workflow automation with 400+ integrations and an AI agent builder. Self-hostable alternative to Zapier and Make with full code access.",
        "github": "n8n-io/n8n",
        "stars_approx": "47k"
    },
    "obsidian-ai": {
        "name": "Obsidian + Smart Connections",
        "category": "productivity-ai",
        "pricing": "Free (local)",
        "license": "Free (Obsidian) / MIT (plugin)",
        "website": "https://obsidian.md",
        "description": "Obsidian local-first note-taking combined with Smart Connections plugin for AI-powered note retrieval and chat using local Ollama models.",
        "github": "brianpetro/obsidian-smart-connections",
        "stars_approx": "3k"
    },
    "supermaven": {
        "name": "Supermaven",
        "category": "code-assistance",
        "pricing": "Free (individual)",
        "license": "Proprietary (free tier)",
        "website": "https://supermaven.com",
        "description": "Ultra-fast AI code completion with 1M token context for free. Fastest autocomplete on the market — used as a free GitHub Copilot alternative.",
        "github": "",
        "stars_approx": ""
    },
    "chatwoot": {
        "name": "Chatwoot",
        "category": "productivity-ai",
        "pricing": "Free (self-hosted)",
        "license": "MIT",
        "website": "https://chatwoot.com",
        "description": "Open-source customer engagement platform with AI-assisted replies, live chat, email, and social media inbox. Self-hostable Intercom alternative.",
        "github": "chatwoot/chatwoot",
        "stars_approx": "22k"
    },
    "botpress": {
        "name": "Botpress",
        "category": "productivity-ai",
        "pricing": "Free (community) / $89/month",
        "license": "MIT",
        "website": "https://botpress.com",
        "description": "Open-source AI chatbot builder with GPT-native flows, knowledge base integration, and omnichannel deployment. Build customer service bots without code.",
        "github": "botpress/botpress",
        "stars_approx": "12k"
    }
}

# ── NEW PAIRS ─────────────────────────────────────────────────────────────────
# 72 new pairs → total 58 + 72 = 130

NEW_PAIRS = [
    # ── AI Chat / LLM Interface (8) ──────────────────────────────────────────
    ["poe-premium",     "open-webui"],
    ["poe-premium",     "jan-ai"],
    ["character-ai",    "sillytavern"],
    ["you-pro",         "perplexica"],
    ["you-pro",         "morphic"],
    ["chatgpt-plus",    "perplexica"],
    ["claude-pro",      "jan-ai"],
    ["gemini-advanced", "jan-ai"],

    # ── AI Writing (8) ───────────────────────────────────────────────────────
    ["quillbot-premium", "languagetool"],
    ["wordtune",         "languagetool"],
    ["jasper-ai",        "languagetool"],
    ["copy-ai",          "languagetool"],
    ["writesonic",       "languagetool"],
    ["copy-ai",          "ollama"],
    ["writesonic",       "ollama"],
    ["copy-ai",          "anything-llm"],

    # ── AI Coding (8) ────────────────────────────────────────────────────────
    ["amazon-codewhisperer", "codeium"],
    ["amazon-codewhisperer", "continue-dev"],
    ["amazon-codewhisperer", "tabby"],
    ["replit-ai",            "aider"],
    ["replit-ai",            "continue-dev"],
    ["cursor-pro",           "tabby"],
    ["github-copilot",       "supermaven"],
    ["github-copilot",       "void-editor"],

    # ── AI Image Generation (10) ─────────────────────────────────────────────
    ["leonardo-ai",   "stable-diffusion-webui"],
    ["leonardo-ai",   "comfyui"],
    ["ideogram",      "flux-1"],
    ["ideogram",      "stable-diffusion-webui"],
    ["playground-ai", "fooocus"],
    ["playground-ai", "comfyui"],
    ["dalle3",        "fooocus"],
    ["dalle3",        "invokeai"],
    ["adobe-firefly", "comfyui"],
    ["canva-ai",      "invokeai"],

    # ── AI Video (8) ─────────────────────────────────────────────────────────
    ["pika-labs",  "wan-video"],
    ["pika-labs",  "stable-video"],
    ["heygen",     "wav2lip"],
    ["heygen",     "sadtalker"],
    ["synthesia",  "sadtalker"],
    ["loom-ai",    "obs-whisper"],
    ["runway-ml",  "cogvideox"],
    ["luma-ai",    "stable-video"],

    # ── AI Voice (6) ─────────────────────────────────────────────────────────
    ["elevenlabs", "piper-tts"],
    ["murf-ai",    "kokoro"],
    ["krisp",      "rnnoise"],
    ["elevenlabs", "bark"],     # may already exist — deduplicated below
    ["murf-ai",    "coqui-tts"],# may already exist — deduplicated below
    ["heygen",     "coqui-tts"],

    # ── AI Audio & Music (8) ─────────────────────────────────────────────────
    ["suno-ai",      "musicgen"],
    ["suno-ai",      "audiocraft"],
    ["udio",         "audiocraft"],
    ["udio",         "musicgen"],
    ["fireflies-ai", "whisper"],
    ["fireflies-ai", "whisperx"],
    ["otter-ai",     "buzz"],
    ["adobe-podcast", "deepfilternet"],

    # ── AI Automation (4) ────────────────────────────────────────────────────
    ["zapier-ai", "n8n"],
    ["make-com",  "n8n"],
    ["zapier-ai", "botpress"],
    ["make-com",  "chatwoot"],

    # ── AI Productivity / Notes (4) ──────────────────────────────────────────
    ["mem-ai",              "obsidian-ai"],
    ["notion-ai",           "obsidian-ai"],
    ["microsoft-copilot-365", "n8n"],
    ["microsoft-copilot-365", "obsidian-ai"],

    # ── AI Customer Service (4) ──────────────────────────────────────────────
    ["intercom-fin", "chatwoot"],
    ["intercom-fin", "botpress"],
    ["drift-ai",     "chatwoot"],
    ["drift-ai",     "botpress"],

    # ── Additional Research / Search (2) ─────────────────────────────────────
    ["perplexity-pro", "perplexica"],
    ["you-pro",        "farfalle"],
]

# ── MERGE ─────────────────────────────────────────────────────────────────────

# Add new tools (skip if key already exists)
added_tools = 0
for key, tool in NEW_TOOLS.items():
    if key not in data["tools"]:
        data["tools"][key] = tool
        added_tools += 1
    else:
        print(f"  ℹ️  Tool already exists, skipped: {key}")

# Add new pairs (deduplicate)
existing_set = set(tuple(p) for p in data["pairs"])
added_pairs = 0
for pair in NEW_PAIRS:
    t = tuple(pair)
    if t not in existing_set:
        # Verify both tools exist
        if pair[0] not in data["tools"]:
            print(f"  ⚠️  Paid tool not found, skipped pair: {pair[0]} — add to tools first")
            continue
        if pair[1] not in data["tools"]:
            print(f"  ⚠️  Free tool not found, skipped pair: {pair[1]} — add to tools first")
            continue
        data["pairs"].append(pair)
        existing_set.add(t)
        added_pairs += 1
    else:
        print(f"  ℹ️  Pair already exists, skipped: {pair}")

# ── WRITE ─────────────────────────────────────────────────────────────────────
FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"""
✅ Done.
   Tools added:  {added_tools}
   Pairs added:  {added_pairs}
   Total pairs:  {len(data['pairs'])}

── NEXT ────────────────────────────────────────────────────────

  1. Verify the count:
       python -c "import json; d=json.load(open('data/tool_pairs.json')); print(len(d['pairs']), 'pairs,', len(d['tools']), 'tools')"

  2. Commit the updated data file:
       git add data/tool_pairs.json
       git commit -m "feat: expand tool_pairs.json to {len(data['pairs'])} pairs"
       git push

  3. Run GitHub Actions with Force regenerate: true
     This generates fresh AI content for all new pairs (~45 min).

  4. Check the live site for new comparison pages after deployment.
""")