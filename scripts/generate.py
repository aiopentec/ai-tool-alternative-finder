#!/usr/bin/env python3
"""
generate.py — AI Tool Alternative Finder
Generates comparison content for paid AI tools vs free alternatives.

Provider waterfall:
  1. Groq  (llama-3.3-70b-versatile) — free, fast
  2. Gemini Flash                      — free, reliable fallback
  3. Template engine                   — always works, no API needed

Usage:
  python scripts/generate.py              # generate all missing
  python scripts/generate.py --index 1   # batch mode (10 per batch)
  python scripts/generate.py --force     # regenerate all even if cached
"""

import argparse, json, logging, os, sys, time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)-8s | %(message)s')
logger = logging.getLogger(__name__)

DATA_FILE   = Path(__file__).parent.parent / 'data' / 'tool_pairs.json'
CACHE_DIR   = Path(__file__).parent.parent / '.cache' / 'comparisons'


# ── Load tool data ─────────────────────────────────────────────────────────────
def load_data() -> Tuple[Dict, List]:
    with open(DATA_FILE) as f:
        data = json.load(f)
    return data['tools'], data['pairs']


# ── Prompt builder ─────────────────────────────────────────────────────────────
def build_prompt(paid: Dict, free: Dict) -> str:
    month = datetime.now().strftime('%B %Y')
    return f"""You are a technical writer producing a comparison page for an AI tools directory.

# {paid['name']} vs {free['name']}

Write the following sections in Markdown. Be objective, factual, and concise.
Focus on: cost savings, privacy, local processing, and practical switching advice.

## Overview
2-3 sentences. What each tool does and who benefits from switching.

## Key Differences
Exactly 5 bullet points covering: cost, privacy/data, setup difficulty, quality parity, and ecosystem.

## Pricing Comparison
| Aspect | {paid['name']} | {free['name']} |
|--------|---------------|----------------|
| Base Cost | {paid['pricing']} | {free['pricing']} |
| License | {paid['license']} | {free['license']} |
| Data privacy | Sent to vendor servers | Local / self-hosted |
| Cost at 10 users/month | Calculate | Calculate |
| Cost at 100 users/month | Calculate | Calculate |

## Pros and Cons
Bullet pros and cons for EACH tool (4 bullets each).

## When to Choose Each
One focused paragraph per tool describing the ideal user.

## Migration / Getting Started
3 concrete steps to switch from {paid['name']} to {free['name']}.

---
*Verified {month}. Check {paid.get('website','')} and {free.get('website','')} for latest pricing.*

Return ONLY the Markdown. No preamble, no code fences."""


# ── AI Provider 1: Groq (free, primary) ───────────────────────────────────────
def generate_with_groq(prompt: str) -> str:
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        raise ValueError('GROQ_API_KEY not set')
    r = requests.post(
        'https://api.groq.com/openai/v1/chat/completions',
        headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'},
        json={
            'model': 'llama-3.3-70b-versatile',
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 1400,
            'temperature': 0.6,
        },
        timeout=45,
    )
    r.raise_for_status()
    return r.json()['choices'][0]['message']['content']


# ── AI Provider 2: Gemini Flash (free, fallback) ───────────────────────────────
def generate_with_gemini(prompt: str) -> str:
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError('GEMINI_API_KEY not set')
    r = requests.post(
        f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}',
        headers={'Content-Type': 'application/json'},
        json={'contents': [{'parts': [{'text': prompt}]}]},
        timeout=45,
    )
    r.raise_for_status()
    return r.json()['candidates'][0]['content']['parts'][0]['text']


# ── Fallback: Rich Template Engine (zero-API, always works) ───────────────────
TEMPLATE_DETAILS = {
    ('chatgpt-plus', 'open-webui'): {
        'overview': "ChatGPT Plus gives access to OpenAI's GPT-4o for $20/month — but the same quality conversation experience is available locally through Open WebUI connected to Ollama. You get a near-identical chat interface, total privacy, and no monthly fees.",
        'differences': [
            "**Cost**: ChatGPT Plus is $20/month per person; Open WebUI + Ollama is completely free forever",
            "**Privacy**: Open WebUI processes everything locally — no conversation data ever leaves your machine",
            "**Model choice**: Open WebUI lets you run Llama 3, Mistral, Gemma, Phi-3 and swap between them freely",
            "**Internet required**: ChatGPT needs a connection; Open WebUI works fully offline after model download",
            "**Setup**: ChatGPT is instant; Open WebUI requires installing Ollama and pulling a model (~10 minutes)"
        ],
        'when_paid': "ChatGPT Plus is the right choice when you need GPT-4o's cutting-edge reasoning, DALL-E 3 image generation, real-time web browsing, or the ChatGPT plugin ecosystem without any setup.",
        'when_free': "Open WebUI + Ollama is ideal for privacy-conscious users, developers, teams processing sensitive documents, or anyone who wants unlimited AI usage with zero ongoing cost.",
        'migration': "1. Install Ollama from ollama.com and run `ollama pull llama3.3` to download a model. 2. Install Open WebUI via Docker: `docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway ghcr.io/open-webui/open-webui:main`. 3. Open http://localhost:3000 — identical chat experience, zero cost, 100% private."
    },
    ('github-copilot', 'continue-dev'): {
        'overview': "GitHub Copilot charges $10–19/month for AI code completions inside VS Code and JetBrains. Continue is a free, open-source alternative that connects to any LLM — including local Ollama models — giving you the same inline completions and codebase chat with zero subscription fees.",
        'differences': [
            "**Cost**: Copilot costs $10–19/month per developer; Continue is completely free",
            "**Privacy**: Continue with Ollama sends no code to external servers — critical for proprietary codebases",
            "**Model flexibility**: Continue works with Ollama, Claude, GPT-4, Gemini, or any OpenAI-compatible API",
            "**IDE support**: Both support VS Code and JetBrains; Continue also supports Cursor and Neovim",
            "**Quality**: Copilot's cloud models are typically stronger; local Ollama models are competitive for common tasks"
        ],
        'when_paid': "GitHub Copilot is the right choice when your team is on GitHub Enterprise, you need the strongest possible model quality for complex completions, and code privacy is not a concern.",
        'when_free': "Continue is ideal for developers working on proprietary or sensitive codebases, teams wanting to avoid per-seat AI costs, or anyone who wants to self-host their AI coding assistant.",
        'migration': "1. Install the Continue extension from VS Code Marketplace. 2. Install Ollama and run `ollama pull qwen2.5-coder:7b` for a strong coding model. 3. Open Continue settings and add Ollama as your provider — you'll have inline completions and codebase chat immediately."
    },
    ('midjourney', 'stable-diffusion-webui'): {
        'overview': "Midjourney charges $10–60/month for AI image generation through Discord with no free tier. Stable Diffusion WebUI (Automatic1111) lets you generate unlimited images locally on your own GPU — same Stable Diffusion models, zero cost per image, and full control over every parameter.",
        'differences': [
            "**Cost**: Midjourney costs $10–60/month with image limits; Stable Diffusion WebUI is free with unlimited generations",
            "**Privacy**: Local generation means your prompts and images never leave your machine",
            "**Control**: SDWUI exposes every sampler, CFG scale, and extension; Midjourney abstracts all of this",
            "**Quality**: Midjourney v6 produces exceptionally aesthetic images; SDXL and FLUX models are now competitive",
            "**Setup**: Midjourney is instant via Discord; SDWUI requires GPU, Python, and a one-time install (~30 mins)"
        ],
        'when_paid': "Midjourney is the right choice when you want consistently stunning artistic images without any technical setup, have a GPU-free machine, or need Midjourney's unique aesthetic and community features.",
        'when_free': "Stable Diffusion WebUI is ideal for power users who want unlimited generations, full parameter control, custom model fine-tuning (LoRA/DreamBooth), and complete image privacy.",
        'migration': "1. Install Python 3.10+ and a compatible GPU (4GB+ VRAM recommended). 2. Clone the repo: `git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui` and run `webui.sh`. 3. Download SDXL or FLUX models from HuggingFace — you're generating immediately with no subscription."
    },
    ('elevenlabs', 'coqui-tts'): {
        'overview': "ElevenLabs charges up to $99/month for realistic AI voice synthesis and cloning. Coqui XTTS is an open-source alternative that clones any voice from a 3-second audio clip and runs entirely on your local machine — no API costs, no character limits, no data sharing.",
        'differences': [
            "**Cost**: ElevenLabs costs $5–99/month with character limits; Coqui TTS is completely free with no limits",
            "**Voice cloning**: Both clone voices from short audio clips; Coqui's XTTS v2 is production-quality",
            "**Privacy**: Local processing means voice samples and generated audio never reach external servers",
            "**Languages**: Coqui XTTS supports 16 languages; ElevenLabs supports 32 languages",
            "**Setup**: ElevenLabs is instant via browser; Coqui requires Python and ~4GB disk space for models"
        ],
        'when_paid': "ElevenLabs is the right choice when you need the widest language support, the most polished voice quality, real-time streaming, or a simple browser-based workflow with no local setup.",
        'when_free': "Coqui XTTS is ideal for developers, content creators producing large volumes, privacy-sensitive applications (legal, medical), or anyone with a Python environment who wants zero ongoing costs.",
        'migration': "1. Install TTS: `pip install TTS`. 2. Clone your voice: `tts --model_name tts_models/multilingual/multi-dataset/xtts_v2 --speaker_wav your_voice.wav --language en --text 'Hello world' --out_path output.wav`. 3. Integrate the Python API into your workflow for batch generation with no character limits."
    },
    ('descript', 'whisper'): {
        'overview': "Descript charges $12–24/month for AI-powered podcast and video transcription and editing. OpenAI's Whisper model is open-source and runs locally — transcribing audio in 99 languages with near-human accuracy at zero cost per minute.",
        'differences': [
            "**Cost**: Descript costs $12–24/month; Whisper is free with no per-minute charges",
            "**Privacy**: Local Whisper processing keeps your audio files entirely on your machine",
            "**Accuracy**: Both achieve near-human transcription accuracy; Whisper excels with accents and technical vocabulary",
            "**Editing**: Descript provides a full transcript-based editor; Whisper is transcription-only (pair with Audacity)",
            "**Speed**: Descript cloud processing is instant; local Whisper varies by GPU (real-time on modern hardware)"
        ],
        'when_paid': "Descript is the right choice when you need a complete podcast editing workflow — transcript-based editing, filler word removal, multi-track recording, and screen recording — in one polished app.",
        'when_free': "Whisper is ideal for developers, journalists, researchers, or anyone who needs accurate transcription without subscription costs and wants audio files to stay on their own hardware.",
        'migration': "1. Install Whisper: `pip install openai-whisper`. 2. Transcribe any file: `whisper audio.mp3 --language English --output_format srt`. 3. Use faster-whisper for 4x speed improvement, and pair with Audacity for editing the resulting transcript."
    },
    ('deepl-pro', 'libreTranslate'): {
        'overview': "DeepL Pro charges up to $57/month for high-quality AI translation with API access. LibreTranslate is an open-source translation API that can be self-hosted — offering the same API-accessible translations with no rate limits, no data collection, and zero ongoing cost.",
        'differences': [
            "**Cost**: DeepL Pro costs $8.74–$57.49/month; LibreTranslate is free to self-host",
            "**Quality**: DeepL consistently ranks best-in-class; LibreTranslate (via Argos) is strong for common language pairs",
            "**Privacy**: Self-hosted LibreTranslate processes text locally — critical for confidential documents",
            "**API compatibility**: LibreTranslate has a simple REST API; some libraries provide a DeepL-compatible wrapper",
            "**Languages**: DeepL supports 31 languages; LibreTranslate supports 30 languages"
        ],
        'when_paid': "DeepL Pro is the right choice when translation quality is paramount, you're working with high-stakes documents (legal, medical, marketing), or you need seamless integration with DeepL's official SDKs.",
        'when_free': "LibreTranslate is ideal for developers building privacy-sensitive applications, organizations processing confidential documents, or high-volume translation workflows where per-character costs add up.",
        'migration': "1. Deploy LibreTranslate via Docker: `docker run -ti --rm -p 5000:5000 libretranslate/libretranslate`. 2. Replace DeepL API calls with LibreTranslate's endpoint: POST /translate with source, target, and q parameters. 3. Install language packs as needed — European languages have the strongest support."
    },
    ('openai-api', 'localai'): {
        'overview': "The OpenAI API charges per token — costs that scale rapidly with volume. LocalAI is an open-source, OpenAI API-compatible server that runs entirely on your hardware, giving you a zero-cost drop-in replacement for OpenAI API calls with no usage fees.",
        'differences': [
            "**Cost**: OpenAI API costs $0.002–$0.06/1K tokens; LocalAI has zero per-request cost after setup",
            "**Compatibility**: LocalAI is a drop-in replacement — change the base URL and your existing code works",
            "**Privacy**: All inference happens locally — no prompts, responses, or data sent to OpenAI",
            "**Model options**: LocalAI supports any GGUF model plus image generation and TTS — not just OpenAI models",
            "**Latency**: Cloud API is generally faster for large requests; local inference depends on your hardware"
        ],
        'when_paid': "OpenAI API is the right choice when you need the absolute best model quality (GPT-4o), have latency-sensitive production workloads, or don't have GPU hardware available for local inference.",
        'when_free': "LocalAI is ideal for developers building privacy-sensitive applications, teams with high API volume, internal tools that can't send data externally, or anyone wanting zero inference costs.",
        'migration': "1. Install LocalAI via Docker: `docker run -p 8080:8080 -v $PWD/models:/build/models localai/localai:latest`. 2. Download a model: `curl http://localhost:8080/models/apply -d '{\"id\":\"llama-3.2-3b\"}'`. 3. Change your OpenAI base URL to `http://localhost:8080/v1` — all existing API calls work immediately."
    },
}


def generate_with_template(paid_key: str, free_key: str, paid: Dict, free: Dict) -> str:
    month = datetime.now().strftime('%B %Y')
    pair_key = (paid_key, free_key)
    details = TEMPLATE_DETAILS.get(pair_key)

    if details:
        overview   = details['overview']
        diff_pts   = '\n'.join(f'- {d}' for d in details['differences'])
        when_paid  = details['when_paid']
        when_free  = details['when_free']
        migration  = details['migration']
    else:
        overview = (
            f"{paid['description']} "
            f"{free['name']} is a free, open-source alternative that gives you "
            f"the same capability locally or self-hosted — with no monthly fees and complete data privacy."
        )
        diff_pts = (
            f"- **Cost**: {paid['name']} costs {paid['pricing']}; {free['name']} is {free['pricing']}\n"
            f"- **Privacy**: {free['name']} processes data locally — no information sent to external servers\n"
            f"- **License**: {paid['name']} is {paid['license']}; {free['name']} is {free['license']}\n"
            f"- **Setup**: {paid['name']} requires no setup; {free['name']} takes 10–30 minutes to install\n"
            f"- **Limits**: {paid['name']} has usage limits tied to your plan; {free['name']} has no usage caps"
        )
        when_paid = (
            f"{paid['name']} is the right choice when you need the most polished experience, "
            f"guaranteed uptime, the widest integrations, and professional support — and budget is not a constraint."
        )
        when_free = (
            f"{free['name']} is ideal for privacy-conscious users, developers, "
            f"teams with high usage volume, or anyone wanting to eliminate per-seat AI subscription costs."
        )
        migration = (
            f"1. Visit {free.get('website', 'the project website')} and follow the quick-start installation guide. "
            f"2. Run a few test queries to validate quality parity for your use case. "
            f"3. Cancel your {paid['name']} subscription once you've confirmed the free alternative meets your needs."
        )

    # Build pricing table
    raw = paid.get('pricing', '$0')
    try:
        num_str = ''.join(c for c in raw.split('–')[0].split('/')[0] if c.isdigit() or c == '.')
        ppu = float(num_str)
        c10  = f'~${ppu * 10:,.0f}/month'
        c100 = f'~${ppu * 100:,.0f}/month'
    except Exception:
        c10 = c100 = 'See pricing page'

    github_line = ''
    if free.get('github'):
        github_line = f"\n> ⭐ GitHub: [github.com/{free['github']}](https://github.com/{free['github']}) · ~{free.get('stars_approx','N/A')} stars"

    return f"""## Overview

{overview}

## Key Differences

{diff_pts}

## Pricing Comparison

| Aspect | {paid['name']} | {free['name']} |
|--------|---------------|----------------|
| Base cost | {paid['pricing']} | {free['pricing']} |
| License | {paid['license']} | {free['license']} |
| Data privacy | Sent to vendor servers | Local / self-hosted |
| Cost at 10 users/month | {c10} | $0/month |
| Cost at 100 users/month | {c100} | $0/month |
| Vendor lock-in | High | None |

## Pros and Cons

### {paid['name']}

**Pros:**
- Polished, fully managed interface — no setup or maintenance
- Access to state-of-the-art frontier models
- Reliable uptime backed by enterprise SLAs
- Continuous updates and new features

**Cons:**
- Significant monthly cost that scales with usage or seat count
- All data is processed on vendor servers — privacy concerns
- No control over model changes or deprecations
- Usage limits enforced by plan tier

### {free['name']}

**Pros:**
- Free to use — no subscription, no usage limits{github_line}
- Complete data privacy — everything stays on your machine or server
- Full control over models, parameters, and updates
- Active open-source community

**Cons:**
- Requires initial technical setup (typically 10–30 minutes)
- Model quality may vary from frontier commercial offerings
- You are responsible for updates and maintenance
- Support is community-based rather than a dedicated helpdesk

## When to Choose Each

**Choose {paid['name']} if:** {when_paid}

**Choose {free['name']} if:** {when_free}

## Migration / Getting Started

{migration}

---
*Verified {month}. Verify current pricing and features at [{paid['name']}]({paid.get('website','')}) and [{free['name']}]({free.get('website','')}) before switching.*
"""


# ── Main generation function ───────────────────────────────────────────────────
def generate_comparison(paid_key: str, free_key: str, tools: Dict) -> Dict:
    paid = tools[paid_key]
    free = tools[free_key]
    prompt = build_prompt(paid, free)

    content = None
    provider = None

    for attempt in range(2):  # two Groq attempts with backoff
        try:
            content = generate_with_groq(prompt)
            provider = 'groq'
            logger.info('    ✅ Generated with Groq')
            break
        except Exception as e:
            logger.warning(f'    ⚠️  Groq failed ({type(e).__name__}): {e}')
            if attempt == 0:
                time.sleep(60)  # Groq rate-limit window

    if content is None:
        try:
            content = generate_with_gemini(prompt)
            provider = 'gemini'
            logger.info('    ✅ Generated with Gemini')
        except Exception as e:
            logger.warning(f'    ⚠️  Gemini failed ({type(e).__name__}): {e}')

    if content is None:
        content = generate_with_template(paid_key, free_key, paid, free)
        provider = 'template'
        logger.info('    ✅ Generated with template engine')

    return {
        'id': f'{paid_key}-vs-{free_key}',
        'slug': f'{paid_key}-vs-{free_key}',
        'title': f'{paid["name"]} vs {free["name"]}',
        'paid_tool': paid['name'],
        'paid_key': paid_key,
        'free_tool': free['name'],
        'free_key': free_key,
        'category': paid.get('category', 'text-generation'),
        'paid_pricing': paid.get('pricing', 'N/A'),
        'free_pricing': free.get('pricing', 'Free'),
        'paid_website': paid.get('website', ''),
        'free_website': free.get('website', ''),
        'free_github': free.get('github', ''),
        'free_stars': free.get('stars_approx', ''),
        'comparison_markdown': content,
        'provider': provider,
        'generated_at': datetime.utcnow().isoformat() + 'Z',
        'status': 'generated',
    }


# ── CLI ────────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description='Generate AI tool comparison content')
    parser.add_argument('--index', '-i', type=int, default=None, help='Batch index (10 pairs per batch)')
    parser.add_argument('--force', '-f', action='store_true', help='Regenerate even if cached')
    parser.add_argument('--output', '-o', default=str(CACHE_DIR))
    args = parser.parse_args()

    tools, pairs = load_data()
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_dir = Path(args.output)
    cache_dir.mkdir(parents=True, exist_ok=True)

    # Select batch or all
    if args.index is not None:
        start = (args.index - 1) * 10
        target_pairs = pairs[start:start + 10]
        if not target_pairs:
            logger.warning(f'No pairs in batch {args.index} (max: {len(pairs)//10 + 1})')
            return
        logger.info(f'🎯 Batch {args.index}: {len(target_pairs)} pairs')
    else:
        target_pairs = pairs
        logger.info(f'🎯 All pairs: {len(target_pairs)} comparisons')

    ok, skip, fail = 0, 0, 0

    for paid_key, free_key in target_pairs:
        slug = f'{paid_key}-vs-{free_key}'
        out_path = cache_dir / f'{slug}.json'

        if out_path.exists() and not args.force:
            logger.info(f'  ⏭  Skipping (cached): {slug}')
            skip += 1
            continue

        if paid_key not in tools or free_key not in tools:
            logger.error(f'  ❌ Unknown key: {paid_key} or {free_key}')
            fail += 1
            continue

        paid_name = tools[paid_key]['name']
        free_name = tools[free_key]['name']
        logger.info(f'  ⚙️  {paid_name} vs {free_name}')

        try:
            result = generate_comparison(paid_key, free_key, tools)
            with open(out_path, 'w') as f:
                json.dump(result, f, indent=2)
            ok += 1
            time.sleep(0.5)
        except Exception as e:
            logger.error(f'  ❌ Failed {slug}: {e}')
            fail += 1

    logger.info('=' * 60)
    logger.info(f'  ✅ Generated: {ok}  |  ⏭  Skipped: {skip}  |  ❌ Failed: {fail}')


if __name__ == '__main__':
    main()
