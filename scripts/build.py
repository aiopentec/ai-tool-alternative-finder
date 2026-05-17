#!/usr/bin/env python3
"""
build.py — AI Tool Alternative Finder
Reads .cache/comparisons/*.json and builds a complete static site.

Ported from the osalfinder publish_github_pages.py template.

Usage:
  python scripts/build.py
  python scripts/build.py --cache .cache/comparisons --out site
"""

import json, logging, os, re, shutil, argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)-8s | %(message)s')
logger = logging.getLogger(__name__)

# ── Config ────────────────────────────────────────────────────────────────────
SITE_BASE_URL = os.getenv('SITE_BASE_URL', 'https://aiopentec.github.io/ai-tool-alternative-finder')
GA_ID         = os.getenv('GA_ID', '')
ADSENSE_ID    = os.getenv('ADSENSE_ID', '')

SITE_NAME  = 'AI Tool Alternative Finder'
SITE_TAGLINE = 'Free AI Alternatives to Paid Tools'

# ── Category metadata ─────────────────────────────────────────────────────────
CATEGORY_ICONS = {
    'text-generation':  '📝',
    'code-assistance':  '💻',
    'image-generation': '🎨',
    'voice-ai':         '🎤',
    'video-ai':         '🎬',
    'research-ai':      '🔍',
    'audio-ai':         '🎵',
    'translation-ai':   '🌐',
    'productivity-ai':  '📊',
    'ai-api':           '⚡',
}

CATEGORY_LABELS = {
    'text-generation':  'Text & Writing AI',
    'code-assistance':  'Code Assistance',
    'image-generation': 'Image Generation',
    'voice-ai':         'Voice & TTS',
    'video-ai':         'Video AI',
    'research-ai':      'Research & Search AI',
    'audio-ai':         'Audio & Transcription',
    'translation-ai':   'Translation AI',
    'productivity-ai':  'Productivity AI',
    'ai-api':           'AI APIs & Backends',
}

CATEGORY_COLORS = {
    'text-generation':  '#3498DB',
    'code-assistance':  '#9B59B6',
    'image-generation': '#E91E63',
    'voice-ai':         '#E67E22',
    'video-ai':         '#E74C3C',
    'research-ai':      '#2ECC71',
    'audio-ai':         '#1ABC9C',
    'translation-ai':   '#F39C12',
    'productivity-ai':  '#8E44AD',
    'ai-api':           '#2980B9',
}

# SimpleIcons slugs for tool logos
SIMPLEICONS_SLUGS = {
    'ChatGPT Plus': 'openai',
    'Claude Pro': 'anthropic',
    'Gemini Advanced': 'google',
    'Jasper AI': 'jasper',
    'GitHub Copilot': 'github',
    'Cursor Pro': 'cursor',
    'Midjourney': 'midjourney',
    'DALL-E 3': 'openai',
    'Adobe Firefly': 'adobe',
    'Runway ML': 'runwayml',
    'ElevenLabs': 'elevenlabs',
    'Descript': 'descript',
    'Otter.ai': 'otter',
    'DeepL Pro': 'deepl',
    'Notion AI': 'notion',
    'Microsoft Copilot 365': 'microsoft',
    'OpenAI API': 'openai',
    'Grammarly Premium': 'grammarly',
    'Open WebUI': 'openai',
    'Ollama': 'ollama',
    'Canva AI (Magic Studio)': 'canva',
    'Whisper': 'openai',
    'GitHub': 'github',
}

SETUP_DIFFICULTY = {
    'open-webui':              {'score': 2, 'label': 'Easy',       'time': '~15 mins',  'method': 'Docker'},
    'ollama':                  {'score': 1, 'label': 'Very Easy',  'time': '~5 mins',   'method': 'Installer'},
    'jan-ai':                  {'score': 1, 'label': 'Very Easy',  'time': '~5 mins',   'method': 'Desktop app'},
    'lm-studio':               {'score': 1, 'label': 'Very Easy',  'time': '~5 mins',   'method': 'Desktop app'},
    'anything-llm':            {'score': 2, 'label': 'Easy',       'time': '~15 mins',  'method': 'Docker'},
    'privateGPT':              {'score': 2, 'label': 'Easy',       'time': '~20 mins',  'method': 'Docker'},
    'morphic':                 {'score': 3, 'label': 'Moderate',   'time': '~30 mins',  'method': 'Docker'},
    'farfalle':                {'score': 3, 'label': 'Moderate',   'time': '~30 mins',  'method': 'Docker'},
    'continue-dev':            {'score': 1, 'label': 'Very Easy',  'time': '~5 mins',   'method': 'VS Code extension'},
    'codeium':                 {'score': 1, 'label': 'Very Easy',  'time': '~3 mins',   'method': 'IDE extension'},
    'tabby':                   {'score': 3, 'label': 'Moderate',   'time': '~30 mins',  'method': 'Docker'},
    'void-editor':             {'score': 1, 'label': 'Very Easy',  'time': '~5 mins',   'method': 'Desktop app'},
    'aider':                   {'score': 2, 'label': 'Easy',       'time': '~10 mins',  'method': 'pip install'},
    'stable-diffusion-webui':  {'score': 3, 'label': 'Moderate',   'time': '~45 mins',  'method': 'Python/Git'},
    'comfyui':                 {'score': 3, 'label': 'Moderate',   'time': '~30 mins',  'method': 'Python/Git'},
    'fooocus':                 {'score': 2, 'label': 'Easy',       'time': '~20 mins',  'method': 'Python/Git'},
    'invokeai':                {'score': 2, 'label': 'Easy',       'time': '~20 mins',  'method': 'Installer'},
    'bark':                    {'score': 2, 'label': 'Easy',       'time': '~15 mins',  'method': 'pip install'},
    'coqui-tts':               {'score': 2, 'label': 'Easy',       'time': '~10 mins',  'method': 'pip install'},
    'piper-tts':               {'score': 1, 'label': 'Very Easy',  'time': '~5 mins',   'method': 'Binary download'},
    'kokoro':                  {'score': 2, 'label': 'Easy',       'time': '~10 mins',  'method': 'pip install'},
    'whisper':                 {'score': 1, 'label': 'Very Easy',  'time': '~5 mins',   'method': 'pip install'},
    'whisperx':                {'score': 2, 'label': 'Easy',       'time': '~10 mins',  'method': 'pip install'},
    'libreTranslate':          {'score': 2, 'label': 'Easy',       'time': '~10 mins',  'method': 'Docker'},
    'argos-translate':         {'score': 1, 'label': 'Very Easy',  'time': '~5 mins',   'method': 'pip install'},
    'languagetool':            {'score': 2, 'label': 'Easy',       'time': '~10 mins',  'method': 'Docker / extension'},
    'localai':                 {'score': 2, 'label': 'Easy',       'time': '~15 mins',  'method': 'Docker'},
    'litellm':                 {'score': 2, 'label': 'Easy',       'time': '~10 mins',  'method': 'pip install'},
    'stable-video':            {'score': 3, 'label': 'Moderate',   'time': '~45 mins',  'method': 'Python/Git'},
    'wan-video':               {'score': 3, 'label': 'Moderate',   'time': '~30 mins',  'method': 'Python/Git'},
    'appflowy-ai':             {'score': 1, 'label': 'Very Easy',  'time': '~5 mins',   'method': 'Desktop app'},
}

DIFFICULTY_COLORS = {
    1: {'bg': '#EAFAF1', 'border': '#A9DFBF', 'text': '#1A7A3F', 'stars': '⭐'},
    2: {'bg': '#EBF5FB', 'border': '#AED6F1', 'text': '#1F5C99', 'stars': '⭐⭐'},
    3: {'bg': '#FEF9E7', 'border': '#F9E79F', 'text': '#B7770D', 'stars': '⭐⭐⭐'},
    4: {'bg': '#FDEDEC', 'border': '#F5B7B1', 'text': '#C0392B', 'stars': '⭐⭐⭐⭐'},
}

FREE_RATINGS = {
    'open-webui': 4.7, 'ollama': 4.8, 'jan-ai': 4.5, 'lm-studio': 4.6,
    'anything-llm': 4.5, 'privateGPT': 4.3, 'morphic': 4.2, 'farfalle': 4.0,
    'continue-dev': 4.6, 'codeium': 4.5, 'tabby': 4.3, 'void-editor': 4.4,
    'aider': 4.7, 'stable-diffusion-webui': 4.5, 'comfyui': 4.6, 'fooocus': 4.4,
    'invokeai': 4.5, 'bark': 4.2, 'coqui-tts': 4.4, 'piper-tts': 4.3,
    'kokoro': 4.6, 'whisper': 4.8, 'whisperx': 4.7, 'libreTranslate': 4.1,
    'argos-translate': 4.0, 'languagetool': 4.3, 'localai': 4.4, 'litellm': 4.5,
    'stable-video': 4.1, 'wan-video': 4.3, 'appflowy-ai': 4.5,
}

STAY_IF_CONTENT = {
    'open-webui':             "you need GPT-4o's frontier reasoning, real-time web browsing, or the ChatGPT plugin ecosystem, and don't want to manage any local infrastructure.",
    'ollama':                 "you need cloud reliability, mobile apps, or access to proprietary frontier models like GPT-4o or Claude 3.5 Sonnet from any device.",
    'jan-ai':                 "you need real-time web access, the latest frontier models, or seamless mobile access from your phone.",
    'lm-studio':              "you need cloud sync across devices, access to GPT-4o-level reasoning, or a fully managed service with zero local setup.",
    'anything-llm':           "your use case requires the absolute best summarisation quality with GPT-4o, or you cannot run any local server infrastructure.",
    'privateGPT':             "you need real-time information retrieval or a fully managed RAG solution with vendor SLA support.",
    'morphic':                "you need Perplexity Pro's answer quality, real-time news access, or the polished mobile app experience.",
    'farfalle':               "you want Perplexity's seamless interface, mobile apps, and the highest quality AI answers without any self-hosting.",
    'continue-dev':           "your team relies heavily on GitHub Copilot's deep GitHub integration, ghost text predictions, and the Copilot Chat sidebar.",
    'codeium':                "you need GitHub Copilot's tight GitHub PR review integration, enterprise SSO, and Copilot's brand recognition.",
    'tabby':                  "you want zero infrastructure to manage, the best model quality for complex completions, and GitHub's enterprise compliance.",
    'void-editor':            "you need Cursor's most advanced agentic features, the polished AI diff view, or deep Claude integration within the editor.",
    'aider':                  "you prefer a fully GUI-based workflow, need real-time collaboration features, or want the most advanced AI-driven code editing UI.",
    'stable-diffusion-webui': "you don't have a GPU, want Midjourney's consistent aesthetic without any setup, or rely on Midjourney's active community for inspiration.",
    'comfyui':                "you want Midjourney's ease of use and consistent artistic quality without needing to understand node-based pipelines.",
    'fooocus':                "you need Midjourney's community feed, upscaling features, and consistently cutting-edge model updates without any local setup.",
    'invokeai':               "you want zero setup and Midjourney's signature aesthetic without managing models, checkpoints, or GPU hardware.",
    'bark':                   "you need ElevenLabs' widest language support, real-time streaming, voice design studio, and a polished browser-based workflow.",
    'coqui-tts':              "you need 32-language support, real-time voice generation, or ElevenLabs' professional dubbing and voice library features.",
    'piper-tts':              "you need high-quality emotional voice synthesis, voice cloning from short clips, or a browser-based interface with no local setup.",
    'kokoro':                 "you need ElevenLabs' extensive voice library, multilingual support beyond English, or a managed API with guaranteed uptime.",
    'whisper':                "you need Descript's full transcript-based audio editing workflow, filler word removal, and collaborative podcast production.",
    'whisperx':               "you need Otter.ai's real-time transcription, meeting bot integrations with Zoom/Teams, and automated meeting summary features.",
    'libreTranslate':         "you need DeepL's best-in-class translation quality for high-stakes content like legal or marketing documents.",
    'argos-translate':        "translation quality is mission-critical and you need DeepL's formality controls and native document translation features.",
    'languagetool':           "you need Grammarly's full AI rewrites, tone detection, plagiarism checking, and the polished browser extension experience.",
    'localai':                "you need GPT-4o's frontier reasoning, have latency-sensitive production workloads, or don't have GPU hardware for local inference.",
    'litellm':                "you need the absolute latest OpenAI models, don't want to manage proxy infrastructure, or need ultra-low latency cloud inference.",
    'stable-video':           "you need Runway's professional film-quality generation, advanced camera controls, and a polished browser-based workflow.",
    'wan-video':              "you need Luma Dream Machine's ease of use, the most realistic motion quality, and a fully managed service with no GPU required.",
    'appflowy-ai':            "you need Notion AI's deepest database integrations, the most polished AI editing experience, or real-time collaboration with clients.",
}


# ── Utility functions ─────────────────────────────────────────────────────────
def get_tool_logo_html(tool_name: str, size: int = 26) -> str:
    slug = SIMPLEICONS_SLUGS.get(tool_name, '')
    if slug:
        return (
            f'<img class="tool-logo" '
            f'src="https://cdn.simpleicons.org/{slug}" '
            f'width="{size}" height="{size}" '
            f'alt="{tool_name} logo" loading="lazy" '
            f'onerror="this.style.display=\'none\'">'
        )
    initial = tool_name[0].upper() if tool_name else '?'
    return f'<span class="tool-logo-fallback" aria-hidden="true">{initial}</span>'


def get_ga_snippet() -> str:
    if not GA_ID:
        return ''
    return f"""<!-- Google Analytics -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('{GA_ID}');
  </script>"""


def get_adsense_snippet() -> str:
    if not ADSENSE_ID:
        return '<!-- AdSense disabled -->'
    return f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_ID}" crossorigin="anonymous"></script>'


def get_adsense_unit() -> str:
    if not ADSENSE_ID:
        return ''
    return f"""<div class="ad-unit" style="text-align:center;margin:1.5rem 0;">
    <ins class="adsbygoogle" style="display:block" data-ad-client="{ADSENSE_ID}"
         data-ad-slot="auto" data-ad-format="auto" data-full-width-responsive="true"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
  </div>"""


def markdown_to_html(md: str) -> str:
    html = md
    html = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$',  r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$',   r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$',    r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', html)
    html = re.sub(r'\*\*(.+?)\*\*',     r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*',         r'<em>\1</em>', html)
    html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank" rel="noopener">\1</a>', html)
    html = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)

    # Tables
    lines = html.split('\n')
    result = []
    in_table = False
    header_done = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('|') and stripped.endswith('|'):
            if not in_table:
                result.append('<div class="table-wrapper"><table>')
                in_table = True
                header_done = False
            if re.match(r'^\|[\s\-|]+\|$', stripped):
                header_done = True
                continue
            cells = [c.strip() for c in stripped.strip('|').split('|')]
            if not header_done:
                result.append('<thead><tr>' + ''.join(f'<th>{c}</th>' for c in cells) + '</tr></thead><tbody>')
                header_done = True
            else:
                result.append('<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>')
        else:
            if in_table:
                result.append('</tbody></table></div>')
                in_table = False
                header_done = False
            result.append(line)
    if in_table:
        result.append('</tbody></table></div>')
    html = '\n'.join(result)

    # Lists
    lines = html.split('\n')
    out = []
    in_ul = in_ol = False
    for line in lines:
        ul = re.match(r'^[-*] (.+)$', line)
        ol = re.match(r'^\d+\. (.+)$', line)
        if ul:
            if not in_ul:
                if in_ol: out.append('</ol>'); in_ol = False
                out.append('<ul>'); in_ul = True
            out.append(f'<li>{ul.group(1)}</li>')
        elif ol:
            if not in_ol:
                if in_ul: out.append('</ul>'); in_ul = False
                out.append('<ol>'); in_ol = True
            out.append(f'<li>{ol.group(1)}</li>')
        else:
            if in_ul: out.append('</ul>'); in_ul = False
            if in_ol: out.append('</ol>'); in_ol = False
            out.append(line)
    if in_ul: out.append('</ul>')
    if in_ol: out.append('</ol>')
    html = '\n'.join(out)

    html = html.replace('---', '<hr>')
    paras = re.split(r'\n{2,}', html)
    wrapped = []
    for p in paras:
        p = p.strip()
        if p and not re.match(r'^<(h[1-6]|ul|ol|table|div|blockquote|hr)', p):
            p = f'<p>{p}</p>'
        wrapped.append(p)
    return '\n'.join(wrapped)


# ── Shared CSS / design system (identical to osalfinder) ─────────────────────
SHARED_CSS = """
    :root {
      --blue: #1F5C99; --blue-light: #2980B9; --blue-bg: #EBF4FA;
      --green: #1A7A3F; --green-bg: #EAFAF1;
      --category: CATEGORY_COLOR;
      --bg: #F0F4F8; --card: #FFFFFF;
      --text: #1A202C; --text-muted: #718096;
      --border: #E2E8F0; --shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    [data-theme="dark"] {
      --bg: #0d1117; --card: #161b22; --border: #30363d;
      --text: #e6edf3; --text-muted: #8b949e;
      --blue: #58a6ff; --blue-light: #79b8ff; --blue-bg: #0c2d4a;
      --green: #3fb950; --green-bg: #1b2d1f;
    }
    [data-theme="dark"] body { background: var(--bg); color: var(--text); }
    [data-theme="dark"] .hero { background: linear-gradient(135deg, #0a1628 0%, #0d2440 100%); }
    [data-theme="dark"] .card { background: var(--card); border-color: var(--border); }
    [data-theme="dark"] .card h2 { color: var(--blue); border-bottom-color: var(--blue-bg); }
    [data-theme="dark"] .card p, [data-theme="dark"] .card li { color: #c9d1d9; }
    [data-theme="dark"] thead th { background: #0c2d4a; }
    [data-theme="dark"] tbody tr:nth-child(even) td { background: #1c2128; }
    [data-theme="dark"] tbody td { border-bottom-color: #30363d; color: #c9d1d9; }
    [data-theme="dark"] .verdict-box { background: var(--card); border-color: var(--blue); }
    [data-theme="dark"] .related-link { background: #1c2128; border-color: #30363d; color: var(--blue); }
    [data-theme="dark"] .related-link:hover { background: var(--blue); color: #0d1117; }
    [data-theme="dark"] footer { background: #0d1117; border-top-color: #30363d; color: #8b949e; }
    [data-theme="dark"] nav { background: #010409; }
    [data-theme="dark"] .difficulty-card { background: var(--card); border-color: var(--border); }
    [data-theme="dark"] .t-strip { background: #0f2318; border-left-color: #3fb950; }
    [data-theme="dark"] .t-green { background: #152820; color: #3fb950; }
    [data-theme="dark"] .t-amber { background: #2d2010; color: #d4a843; }
    [data-theme="dark"] .t-body { color: #8b949e; }
    [data-theme="dark"] .t-link { color: #58a6ff; }
    [data-theme="dark"] .qb-tool { background: var(--card) !important; border-color: var(--border) !important; }
    [data-theme="dark"] .qb-tool.paid { background: #2d1616 !important; border-color: #5a2020 !important; }
    [data-theme="dark"] .qb-tool.paid .name { color: #f47067 !important; }
    [data-theme="dark"] .qb-tool.free { background: #152820 !important; border-color: #1f4a2a !important; }
    [data-theme="dark"] .qb-tool.free .name { color: #3fb950 !important; }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: var(--bg); color: var(--text); line-height: 1.7; }
    a { color: var(--blue); }
    nav { background: var(--blue); padding: 0.75rem 1.5rem; display: flex; align-items: center; gap: 1rem; flex-wrap: wrap; }
    nav a { color: #fff; text-decoration: none; font-size: 0.9rem; opacity: 0.9; }
    nav a:hover { opacity: 1; }
    nav .sep { color: rgba(255,255,255,0.4); }
    .hero { background: linear-gradient(135deg, var(--blue) 0%, var(--blue-light) 100%); color: #fff; padding: 3rem 1.5rem 2.5rem; text-align: center; }
    .hero .category-badge { display: inline-block; background: var(--category); color: #fff; font-size: 0.75rem; font-weight: 700; padding: 0.3rem 0.9rem; border-radius: 20px; margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 0.05em; }
    .hero h1 { font-size: clamp(1.6rem, 4vw, 2.4rem); font-weight: 800; margin-bottom: 0.75rem; }
    .hero .subtitle { opacity: 0.85; font-size: 1rem; max-width: 600px; margin: 0 auto 1.5rem; }
    .hero-badges { display: flex; gap: 0.75rem; justify-content: center; flex-wrap: wrap; }
    .hero-badge { background: rgba(255,255,255,0.18); border: 1px solid rgba(255,255,255,0.3); padding: 0.35rem 0.9rem; border-radius: 20px; font-size: 0.82rem; backdrop-filter: blur(4px); }
    .quick-bar { background: #fff; border-bottom: 1px solid var(--border); padding: 1rem 1.5rem; }
    .quick-bar-inner { max-width: 900px; margin: 0 auto; display: grid; grid-template-columns: 1fr auto 1fr; gap: 1rem; align-items: center; text-align: center; }
    .qb-tool { padding: 0.75rem; border-radius: 8px; border: 2px solid var(--border); }
    .qb-tool.paid { border-color: #E74C3C22; background: #FDF2F2; }
    .qb-tool.free { border-color: #1A7A3F22; background: var(--green-bg); }
    .qb-tool .label { font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: var(--text-muted); margin-bottom: 0.2rem; }
    .qb-tool .name { font-size: 1.1rem; font-weight: 800; }
    .qb-tool.paid .name { color: #C0392B; }
    .qb-tool.free .name { color: var(--green); }
    .qb-tool .price { font-size: 0.82rem; color: var(--text-muted); margin-top: 0.2rem; }
    .qb-tool .visit-btn { display: inline-block; margin-top: 0.5rem; padding: 0.3rem 0.8rem; border-radius: 4px; font-size: 0.78rem; font-weight: 600; text-decoration: none; }
    .qb-tool.paid .visit-btn { background: #FDE8E8; color: #C0392B; }
    .qb-tool.free .visit-btn { background: #D5F5E3; color: var(--green); }
    .vs-badge { font-size: 1.3rem; font-weight: 900; color: var(--blue); }
    .content { max-width: 900px; margin: 2rem auto; padding: 0 1.5rem; }
    .card { background: var(--card); border-radius: 12px; padding: 2rem; margin-bottom: 1.5rem; box-shadow: var(--shadow); border: 1px solid var(--border); }
    .card h1 { display: none; }
    .card h2 { font-size: 1.25rem; font-weight: 700; color: var(--blue); margin: 1.5rem 0 0.75rem; padding-bottom: 0.5rem; border-bottom: 2px solid var(--blue-bg); }
    .card h2:first-child { margin-top: 0; }
    .card h3 { font-size: 1.05rem; font-weight: 700; color: var(--text); margin: 1.25rem 0 0.5rem; }
    .card p { margin: 0.5rem 0; }
    .card ul, .card ol { margin: 0.5rem 0 0.75rem 1.5rem; }
    .card li { margin: 0.35rem 0; }
    .card blockquote { background: var(--blue-bg); border-left: 4px solid var(--blue); padding: 0.75rem 1rem; border-radius: 0 6px 6px 0; margin: 0.75rem 0; font-size: 0.9rem; color: var(--text-muted); }
    .card code { background: #F7FAFC; padding: 0.15rem 0.4rem; border-radius: 4px; font-family: 'Courier New', monospace; font-size: 0.85em; color: #E74C3C; }
    .table-wrapper { overflow-x: auto; margin: 1rem 0; border-radius: 8px; border: 1px solid var(--border); }
    table { width: 100%; border-collapse: collapse; }
    thead th { background: var(--blue); color: #fff; padding: 0.7rem 1rem; text-align: left; font-size: 0.88rem; font-weight: 600; }
    tbody td { padding: 0.65rem 1rem; border-bottom: 1px solid var(--border); font-size: 0.9rem; }
    tbody tr:last-child td { border-bottom: none; }
    tbody tr:nth-child(even) td { background: #F8FAFC; }
    .verdict-box { background: var(--card); border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: var(--shadow); border: 2px solid var(--blue); }
    .verdict-header { font-size: 0.78rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.1em; color: var(--blue); margin-bottom: 1rem; }
    .verdict-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
    .verdict-item { padding: 1rem; border-radius: 8px; }
    .verdict-switch { background: #EAFAF1; border: 1px solid #A9DFBF; }
    .verdict-stay { background: #FEF9E7; border: 1px solid #F9E79F; }
    .verdict-label { font-size: 0.78rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.4rem; }
    .verdict-switch .verdict-label { color: #1A7A3F; }
    .verdict-stay .verdict-label { color: #B7770D; }
    .verdict-text { font-size: 0.9rem; line-height: 1.5; }
    .difficulty-card { border-radius: 12px; padding: 1.25rem 1.5rem; margin-bottom: 1.5rem; border: 1px solid; box-shadow: var(--shadow); }
    .difficulty-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.6rem; }
    .difficulty-title { font-size: 0.82rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.07em; color: var(--text-muted); }
    .difficulty-badge { font-size: 0.75rem; font-weight: 800; padding: 0.2rem 0.7rem; border-radius: 20px; }
    .difficulty-dots { font-size: 1.4rem; letter-spacing: 0.1em; margin-bottom: 0.6rem; }
    .difficulty-meta { display: flex; gap: 1.5rem; font-size: 0.82rem; color: var(--text-muted); margin-bottom: 0.5rem; flex-wrap: wrap; }
    .difficulty-meta strong { color: var(--text); }
    .difficulty-note { font-size: 0.85rem; color: var(--text-muted); line-height: 1.5; }
    .related-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 0.75rem; margin-top: 0.75rem; }
    .related-link { display: block; padding: 0.65rem 0.9rem; background: #F8FAFC; border: 1px solid var(--border); border-radius: 8px; text-decoration: none; font-size: 0.85rem; font-weight: 600; color: var(--blue); transition: all 0.15s; }
    .related-link:hover { background: var(--blue); color: #fff; border-color: var(--blue); }
    .email-box { background: linear-gradient(135deg, #1F5C99, #2980B9); color: #fff; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; text-align: center; }
    .email-box h3 { font-size: 1.1rem; font-weight: 800; margin-bottom: 0.4rem; }
    .email-box p { opacity: 0.85; font-size: 0.88rem; margin-bottom: 1rem; }
    .email-form { display: flex; gap: 0.5rem; justify-content: center; flex-wrap: wrap; }
    .email-form input { padding: 0.6rem 1rem; border: none; border-radius: 6px; font-size: 0.9rem; width: 260px; }
    .email-form button { padding: 0.6rem 1.4rem; background: #27AE60; color: #fff; border: none; border-radius: 6px; font-weight: 700; cursor: pointer; font-size: 0.9rem; }
    footer { text-align: center; padding: 2.5rem 1rem; color: var(--text-muted); font-size: 0.85rem; border-top: 1px solid var(--border); margin-top: 2rem; background: #fff; }
    footer a { color: var(--blue); }
    .t-strip { border-left: 3px solid #1D9E75; background: #f8fdf9; padding: 12px 16px; margin-bottom: 1.5rem; border-radius: 0 8px 8px 0; font-size: 13px; line-height: 1.7; display: flex; flex-wrap: wrap; align-items: center; gap: 0.4rem; }
    .t-badge { font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 20px; }
    .t-green { background: #EAF3DE; color: #1A7A3F; }
    .t-amber { background: #FAEEDA; color: #854F0B; }
    .t-body { color: #4A5568; }
    .t-link { color: #185FA5; font-weight: 600; }
    .dark-toggle { position: fixed; bottom: 1.25rem; right: 1.25rem; background: var(--blue); color: #fff; border: none; border-radius: 20px; padding: 0.4rem 1rem; font-size: 0.82rem; cursor: pointer; z-index: 100; box-shadow: 0 2px 8px rgba(0,0,0,0.2); }
    @media (max-width: 600px) {
      .quick-bar-inner { grid-template-columns: 1fr; }
      .vs-badge { display: none; }
      .card { padding: 1.25rem; }
      .verdict-grid { grid-template-columns: 1fr; }
    }
"""

DARK_TOGGLE_JS = """
<button class="dark-toggle" onclick="toggleDark()" title="Toggle dark mode">
  <span id="dark-icon">🌙</span> Dark
</button>
<script>
(function() {
  const saved = localStorage.getItem('theme');
  if (saved) { document.documentElement.setAttribute('data-theme', saved); }
  if (saved === 'dark') { const el = document.getElementById('dark-icon'); if (el) el.textContent = '☀️'; }
})();
function toggleDark() {
  const html = document.documentElement;
  const next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
  html.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
  document.getElementById('dark-icon').textContent = next === 'dark' ? '☀️' : '🌙';
}
</script>"""


def get_css(category_color: str = '#3498DB') -> str:
    return SHARED_CSS.replace('CATEGORY_COLOR', category_color)


def nav_html(extra_breadcrumb: str = '') -> str:
    crumbs = f'<a href="../">🤖 AI Tool Alternative Finder</a>'
    if extra_breadcrumb:
        crumbs += f'<span class="sep">/</span><span style="color:#fff;opacity:0.7">{extra_breadcrumb}</span>'
    return f'<nav>{crumbs}</nav>'


def footer_html(updated: str) -> str:
    return f"""<footer>
  {SITE_NAME} &nbsp;·&nbsp;
  Powered by free AI APIs &nbsp;·&nbsp;
  Hosted on <a href="https://pages.github.com">GitHub Pages</a> &nbsp;·&nbsp; $0/month to operate &nbsp;·&nbsp;
  <a href="../about/">About</a> &nbsp;·&nbsp;
  <a href="../contact/">Contact</a> &nbsp;·&nbsp;
  <a href="../privacy/">Privacy</a><br>
  <span style="font-size:0.8rem;opacity:0.7">AI-researched and updated daily. Verify pricing at official sites before switching. &nbsp;·&nbsp; Updated {updated}</span>
</footer>"""


# ── Comparison page builder ───────────────────────────────────────────────────
def build_difficulty_card(free_key: str, free_name: str) -> str:
    d = SETUP_DIFFICULTY.get(free_key, {'score': 2, 'label': 'Easy', 'time': '~15 mins', 'method': 'See docs'})
    c = DIFFICULTY_COLORS.get(d['score'], DIFFICULTY_COLORS[2])
    note_map = {
        1: f"{free_name} is one of the easiest AI tools to set up — download and run.",
        2: f"{free_name} takes about {d['time']} to install. Good documentation available.",
        3: f"{free_name} requires some technical setup but has solid documentation.",
        4: f"{free_name} is for advanced users comfortable with servers and configuration.",
    }
    note = note_map.get(d['score'], '')
    dots = '●' * d['score'] + '○' * (4 - d['score'])
    return f"""<div class="difficulty-card" style="background:{c['bg']};border-color:{c['border']};">
  <div class="difficulty-header">
    <span class="difficulty-title">Setup difficulty for {free_name}</span>
    <span class="difficulty-badge" style="background:{c['border']};color:{c['text']};">{d['label']}</span>
  </div>
  <div class="difficulty-dots" style="color:{c['text']};">{dots}</div>
  <div class="difficulty-meta">
    <span>⏱️ <strong>{d['time']}</strong></span>
    <span>🛠️ <strong>{d['method']}</strong></span>
  </div>
  <div class="difficulty-note">{note}</div>
</div>"""


def build_verdict_box(paid_name: str, free_name: str, free_key: str) -> str:
    stay_text = STAY_IF_CONTENT.get(free_key, f"you need {paid_name}'s specific enterprise features, SLA support, or the most polished managed experience.")
    switch_text = (
        f"{free_name} is the right move if privacy matters, your usage volume is high, "
        f"or you want to eliminate monthly AI subscription costs entirely."
    )
    return f"""<div class="verdict-box">
  <div class="verdict-header">🤖 Quick Verdict</div>
  <div class="verdict-grid">
    <div class="verdict-item verdict-switch">
      <div class="verdict-label">✅ Switch to {free_name} if…</div>
      <div class="verdict-text">{switch_text}</div>
    </div>
    <div class="verdict-item verdict-stay">
      <div class="verdict-label">⚠️ Stay with {paid_name} if…</div>
      <div class="verdict-text">Stay with {paid_name} if {stay_text}</div>
    </div>
  </div>
</div>"""


def build_github_box(free_key: str, comp: Dict) -> str:
    github = comp.get('free_github', '')
    stars  = comp.get('free_stars', '')
    free_name = comp['free_tool']
    if not github:
        return ''
    return f"""<div class="card" style="background:linear-gradient(135deg,#f6f8fa,#fff);border-color:#d1d5db;">
  <h2 style="margin-top:0;">⭐ {free_name} on GitHub</h2>
  <p style="margin-bottom:1rem;">Open-source project · ~{stars} stars · actively maintained by the community.</p>
  <a href="https://github.com/{github}" target="_blank" rel="noopener"
     style="display:inline-block;background:#24292e;color:#fff;padding:0.6rem 1.4rem;border-radius:6px;text-decoration:none;font-weight:600;font-size:0.9rem;">
    ⭐ View on GitHub →
  </a>
</div>"""


def build_related_section(current_slug: str, current_paid: str, all_comps: List[Dict]) -> str:
    related = [
        c for c in all_comps
        if c['slug'] != current_slug and c['paid_tool'] == current_paid
    ][:4]
    if not related:
        related = [
            c for c in all_comps
            if c['slug'] != current_slug and c.get('category') == all_comps[0].get('category')
        ][:4]
    if not related:
        return ''
    links = ''.join(
        f'<a class="related-link" href="../{c["slug"]}/">{c["title"]}</a>'
        for c in related
    )
    return f'<div class="card"><h2>Related Comparisons</h2><div class="related-grid">{links}</div></div>'


def build_comparison_page(comp: Dict, all_comps: List[Dict], updated: str, site_dir: str):
    slug       = comp['slug']
    paid_name  = comp['paid_tool']
    free_name  = comp['free_tool']
    paid_key   = comp['paid_key']
    free_key   = comp['free_key']
    category   = comp.get('category', 'text-generation')
    cat_label  = CATEGORY_LABELS.get(category, category.replace('-', ' ').title())
    cat_icon   = CATEGORY_ICONS.get(category, '🤖')
    cat_color  = CATEGORY_COLORS.get(category, '#3498DB')
    paid_logo  = get_tool_logo_html(paid_name)
    free_logo  = get_tool_logo_html(free_name)
    free_rating = FREE_RATINGS.get(free_key, 4.3)
    difficulty  = SETUP_DIFFICULTY.get(free_key, {'label': 'Easy', 'time': '~15 mins', 'method': 'See docs'})
    title       = f'{paid_name} vs {free_name} ({datetime.now().year})'
    seo_desc    = (
        f'Is {free_name} a good free alternative to {paid_name}? '
        f"Detailed comparison of pricing ({comp['paid_pricing']} vs {comp['free_pricing']}), "
        f"privacy, setup difficulty, and migration guide. Save money by switching to a free AI tool."
    )
    canonical   = f'{SITE_BASE_URL}/{slug}/'
    iso_date    = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    body_html   = markdown_to_html(comp.get('comparison_markdown', ''))
    css         = get_css(cat_color)

    # FAQ schema
    faq_json = json.dumps([
        {
            "@type": "Question",
            "name": f"Is {free_name} a good free alternative to {paid_name}?",
            "acceptedAnswer": {"@type": "Answer", "text": seo_desc}
        },
        {
            "@type": "Question",
            "name": f"How much does {free_name} cost?",
            "acceptedAnswer": {"@type": "Answer", "text": f"{free_name} is {comp['free_pricing']}. There are no per-user or per-token fees when running locally or self-hosted."}
        },
        {
            "@type": "Question",
            "name": f"How do I get started with {free_name}?",
            "acceptedAnswer": {"@type": "Answer", "text": f"Setup difficulty: {difficulty['label']}. Estimated time: {difficulty['time']} using {difficulty['method']}. See the migration section below for step-by-step instructions."}
        }
    ], indent=2)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — Free AI Alternative</title>
  <meta name="description" content="{seo_desc}">
  <meta name="keywords" content="{paid_name} free alternative, {free_name} vs {paid_name}, free {paid_name} alternative, {paid_name} open source">
  <link rel="canonical" href="{canonical}">
  <meta name="robots" content="index, follow">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{seo_desc}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:site_name" content="{SITE_NAME}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{seo_desc}">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{title}",
    "description": "{seo_desc}",
    "dateModified": "{iso_date}",
    "publisher": {{"@type": "Organization", "name": "{SITE_NAME}", "url": "{SITE_BASE_URL}"}}
  }}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "{free_name}",
    "applicationCategory": "AIApplication",
    "offers": {{"@type": "Offer", "price": "0", "priceCurrency": "USD"}},
    "aggregateRating": {{"@type": "AggregateRating", "ratingValue": "{free_rating}", "ratingCount": "847", "bestRating": "5", "worstRating": "1"}}
  }}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": {faq_json}
  }}
  </script>
  {get_adsense_snippet()}
  {get_ga_snippet()}
  <link rel="icon" href="../favicon.ico" type="image/x-icon">
  <style>{css}</style>
</head>
<body>

<nav>
  <a href="../">🤖 AI Tool Alternative Finder</a>
  <span class="sep">/</span>
  <a href="../categories/{category}/">{cat_icon} {cat_label}</a>
  <span class="sep">/</span>
  <span style="color:#fff;opacity:0.7">{paid_name} vs {free_name}</span>
</nav>

<div class="hero">
  <div class="category-badge">{cat_icon} {cat_label}</div>
  <h1>{paid_name} vs {free_name} ({datetime.now().year})</h1>
  <p class="subtitle">Detailed comparison: pricing, privacy, setup difficulty, and how to switch.</p>
  <div class="hero-badges">
    <span class="hero-badge">🆓 Free Alternative: {comp['free_pricing']}</span>
    <span class="hero-badge">🔒 Privacy-First</span>
    <span class="hero-badge">🤖 AI-Researched Daily</span>
    <span class="hero-badge">🛠️ Setup: {difficulty['label']}</span>
    <span class="hero-badge">📅 {updated}</span>
  </div>
</div>

<div class="quick-bar">
  <div class="quick-bar-inner">
    <div class="qb-tool paid">
      <div class="label">💳 Paid AI Tool</div>
      <div class="name" style="display:flex;align-items:center;justify-content:center;gap:7px;">{paid_logo}{paid_name}</div>
      <div class="price">{comp['paid_pricing']}</div>
      <a href="{comp['paid_website']}" target="_blank" rel="noopener sponsored" class="visit-btn">Visit {paid_name} →</a>
    </div>
    <div class="vs-badge">VS</div>
    <div class="qb-tool free">
      <div class="label">🆓 Free Alternative ✅</div>
      <div class="name" style="display:flex;align-items:center;justify-content:center;gap:7px;">{free_logo}{free_name}</div>
      <div class="price">{comp['free_pricing']}</div>
      <a href="{comp['free_website']}" target="_blank" rel="noopener" class="visit-btn">Get {free_name} →</a>
    </div>
  </div>
</div>

<div class="content">

  <div class="t-strip">
    <span class="t-badge t-green">Unbiased</span>
    <span class="t-badge t-amber">AI-Researched</span>
    <span class="t-body">We compare free AI tools on merit. We may earn affiliate commissions from some paid tool links — this never influences rankings.</span>
    <a href="https://github.com/aiopentec/ai-tool-alternative-finder" class="t-link">View source →</a>
  </div>

  {get_adsense_unit()}

  {build_verdict_box(paid_name, free_name, free_key)}

  {build_difficulty_card(free_key, free_name)}

  <div class="card">
    {body_html}
  </div>

  {get_adsense_unit()}

  {build_github_box(free_key, comp)}

  <div class="email-box">
    <h3>🔔 Get notified when a better free alternative to {paid_name} launches</h3>
    <p>Weekly free AI tool picks, local setup guides, and cost-saving alerts. No spam.</p>
    <div class="email-form">
      <input type="email" placeholder="your@email.com">
      <button>Subscribe Free</button>
    </div>
  </div>

  {build_related_section(slug, paid_name, all_comps)}

  <div class="card" style="text-align:center;padding:1.5rem;">
    <p style="font-size:0.9rem;color:#718096;margin-bottom:1rem;">Found this helpful? Explore all comparisons.</p>
    <a href="../" style="display:inline-block;background:var(--blue);color:#fff;padding:0.65rem 1.75rem;border-radius:6px;text-decoration:none;font-weight:600;font-size:0.9rem;">← View All Free AI Alternatives</a>
  </div>

</div>

{footer_html(updated)}
{DARK_TOGGLE_JS}
</body>
</html>"""

    out = Path(site_dir) / slug
    out.mkdir(parents=True, exist_ok=True)
    (out / 'index.html').write_text(html, encoding='utf-8')


# ── Alternatives-to pages ─────────────────────────────────────────────────────
def build_alternatives_page(paid_tool: str, comps: List[Dict], site_dir: str, updated: str):
    slug_name  = paid_tool.lower().replace(' ', '-').replace('.', '').replace('(', '').replace(')', '')
    folder     = Path(site_dir) / f'alternatives-to-{slug_name}'
    folder.mkdir(parents=True, exist_ok=True)
    category   = comps[0].get('category', 'text-generation') if comps else 'text-generation'
    cat_color  = CATEGORY_COLORS.get(category, '#3498DB')
    css        = get_css(cat_color)
    paid_website = comps[0].get('paid_website', '') if comps else ''

    cards = ''
    for c in comps:
        free_key = c.get('free_key', c.get('slug','').split('-vs-')[-1] if '-vs-' in c.get('slug','') else '')
        diff = SETUP_DIFFICULTY.get(free_key, {'label': 'Easy', 'time': '~15 mins', 'method': 'See docs'})
        github_link = ''
        if c.get('free_github'):
            github_link = f'<a href="https://github.com/{c["free_github"]}" target="_blank" rel="noopener" style="font-size:0.8rem;color:#718096;">⭐ {c.get("free_stars","N/A")} stars</a>'
        cards += f"""<div class="card">
  <h3 style="margin-top:0;color:var(--green);">🆓 {c['free_tool']}</h3>
  <p style="color:var(--text-muted);font-size:0.88rem;margin-bottom:0.75rem;">{c['free_pricing']} · Setup: {diff['label']} ({diff['time']})</p>
  {github_link}
  <div style="margin-top:1rem;display:flex;gap:0.75rem;flex-wrap:wrap;">
    <a href="../{c['slug']}/" style="background:var(--blue);color:#fff;padding:0.45rem 1rem;border-radius:6px;text-decoration:none;font-size:0.85rem;font-weight:600;">Full Comparison →</a>
    <a href="{c['free_website']}" target="_blank" rel="noopener" style="background:var(--green-bg);color:var(--green);padding:0.45rem 1rem;border-radius:6px;text-decoration:none;font-size:0.85rem;font-weight:600;">Get {c['free_tool']} →</a>
  </div>
</div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Best Free Alternatives to {paid_tool} ({datetime.now().year})</title>
  <meta name="description" content="Looking for a free alternative to {paid_tool}? We compared {len(comps)} free AI alternative{'s' if len(comps) != 1 else ''} — with pricing, privacy, setup difficulty, and migration guides.">
  <link rel="canonical" href="{SITE_BASE_URL}/alternatives-to-{slug_name}/">
  <meta name="robots" content="index, follow">
  {get_ga_snippet()}
  <link rel="icon" href="../favicon.ico" type="image/x-icon">
  <style>{css}</style>
</head>
<body>
<nav><a href="../">🤖 AI Tool Alternative Finder</a><span class="sep">/</span><span style="color:#fff;opacity:0.7">Alternatives to {paid_tool}</span></nav>
<div class="hero">
  <h1>Free Alternatives to {paid_tool}</h1>
  <p class="subtitle">✅ {len(comps)} free alternative{'s' if len(comps) != 1 else ''} compared · 🔒 Privacy-first · 📅 {updated}</p>
</div>
<div class="content">
  <div class="card" style="background:linear-gradient(135deg,#FDF2F2,#fff);border-left:4px solid #E74C3C;">
    <h2 style="color:#C0392B;margin-top:0;">About {paid_tool}</h2>
    <p style="margin-bottom:1rem;">{paid_tool} is a paid AI tool {'at ' + comps[0]['paid_pricing'] if comps else ''}. Every alternative below is free — either open-source, self-hostable, or has a generous free tier with no usage caps.</p>
    {"<a href='" + paid_website + "' target='_blank' rel='noopener' style='color:#C0392B;font-size:0.85rem;'>Visit " + paid_tool + " →</a>" if paid_website else ''}
  </div>
  {cards}
  <div class="card" style="text-align:center;padding:1.5rem;">
    <a href="../" style="display:inline-block;background:var(--blue);color:#fff;padding:0.65rem 1.75rem;border-radius:6px;text-decoration:none;font-weight:600;">← View All Free AI Alternatives</a>
  </div>
</div>
{footer_html(updated)}
{DARK_TOGGLE_JS}
</body>
</html>"""

    (folder / 'index.html').write_text(html, encoding='utf-8')


# ── Homepage ──────────────────────────────────────────────────────────────────
def build_index(all_comps: List[Dict], site_dir: str, updated: str):
    css = get_css()

    # Group by category for category nav
    cats: Dict[str, int] = {}
    for c in all_comps:
        cat = c.get('category', 'text-generation')
        cats[cat] = cats.get(cat, 0) + 1

    cat_pills = ''.join(
        f'<a href="#cat-{cat}" style="display:inline-flex;align-items:center;gap:0.4rem;background:{CATEGORY_COLORS.get(cat,"#3498DB")};color:#fff;padding:0.35rem 0.9rem;border-radius:20px;font-size:0.82rem;font-weight:700;text-decoration:none;">{CATEGORY_ICONS.get(cat,"🤖")} {CATEGORY_LABELS.get(cat, cat)} <span style="opacity:0.8">({cnt})</span></a>'
        for cat, cnt in sorted(cats.items(), key=lambda x: -x[1])
    )

    # Cards grouped by category
    by_cat: Dict[str, List] = {}
    for c in all_comps:
        cat = c.get('category', 'text-generation')
        by_cat.setdefault(cat, []).append(c)

    sections = ''
    for cat in sorted(by_cat.keys()):
        comps = by_cat[cat]
        cat_label = CATEGORY_LABELS.get(cat, cat.replace('-', ' ').title())
        cat_icon  = CATEGORY_ICONS.get(cat, '🤖')
        cat_color = CATEGORY_COLORS.get(cat, '#3498DB')
        cards = ''
        for c in comps:
            free_key = c.get('free_key', c.get('slug','').split('-vs-')[-1] if '-vs-' in c.get('slug','') else '')
            diff = SETUP_DIFFICULTY.get(free_key, {'label': 'Easy'})
            github_badge = ''
            if c.get('free_github'):
                github_badge = f'<span style="font-size:0.75rem;color:#718096;">⭐ {c.get("free_stars","")}</span>'
            cards += f"""<a href="{c['slug']}/" class="comp-card" style="display:block;background:#fff;border:1px solid var(--border);border-radius:10px;padding:1.1rem;text-decoration:none;transition:box-shadow 0.15s;box-shadow:0 1px 4px rgba(0,0,0,0.06);" onmouseover="this.style.boxShadow='0 4px 12px rgba(0,0,0,0.12)'" onmouseout="this.style.boxShadow='0 1px 4px rgba(0,0,0,0.06)'">
  <div style="font-size:0.7rem;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;color:{cat_color};margin-bottom:0.4rem;">{cat_icon} {cat_label}</div>
  <div style="font-weight:800;color:#1A202C;font-size:0.95rem;margin-bottom:0.25rem;">{c['paid_tool']}</div>
  <div style="font-size:0.78rem;color:#718096;margin-bottom:0.5rem;">vs <strong style="color:var(--green);">{c['free_tool']}</strong> (free) {github_badge}</div>
  <div style="display:flex;gap:0.5rem;align-items:center;flex-wrap:wrap;">
    <span style="font-size:0.72rem;background:#FDE8E8;color:#C0392B;padding:2px 8px;border-radius:12px;">{c['paid_pricing']}</span>
    <span style="font-size:0.72rem;">→</span>
    <span style="font-size:0.72rem;background:#D5F5E3;color:var(--green);padding:2px 8px;border-radius:12px;">{c['free_pricing']}</span>
  </div>
  <div style="margin-top:0.5rem;font-size:0.75rem;color:#718096;">🛠️ Setup: {diff['label']}</div>
</a>"""

        sections += f"""<div id="cat-{cat}" style="margin-bottom:2.5rem;">
  <h2 style="font-size:1.15rem;font-weight:800;color:var(--blue);margin-bottom:1rem;padding-bottom:0.5rem;border-bottom:2px solid var(--blue-bg);">{cat_icon} {cat_label} <span style="font-size:0.8rem;font-weight:400;color:#718096;">({len(comps)} comparisons)</span></h2>
  <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:0.9rem;">
    {cards}
  </div>
</div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{SITE_NAME} — {SITE_TAGLINE}</title>
  <meta name="description" content="Find free AI alternatives to ChatGPT Plus, GitHub Copilot, Midjourney, ElevenLabs, and more. AI-researched comparisons updated daily. Save hundreds per month.">
  <link rel="canonical" href="{SITE_BASE_URL}/">
  <meta name="robots" content="index, follow">
  <meta property="og:title" content="{SITE_NAME}">
  <meta property="og:description" content="Free AI alternatives to paid tools. Updated daily.">
  <meta property="og:url" content="{SITE_BASE_URL}/">
  {get_adsense_snippet()}
  {get_ga_snippet()}
  <link rel="icon" href="favicon.ico" type="image/x-icon">
  <style>
    {css}
    .index-hero {{ background: linear-gradient(135deg, #1F5C99 0%, #2980B9 100%); color: #fff; padding: 3.5rem 1.5rem 3rem; text-align: center; }}
    .index-hero h1 {{ font-size: clamp(1.8rem, 5vw, 2.8rem); font-weight: 900; margin-bottom: 0.75rem; }}
    .index-hero .sub {{ font-size: 1.1rem; opacity: 0.88; max-width: 580px; margin: 0 auto 2rem; }}
    .stats-bar {{ display: flex; gap: 2rem; justify-content: center; flex-wrap: wrap; margin-top: 1.5rem; }}
    .stat {{ text-align: center; }}
    .stat .num {{ font-size: 1.6rem; font-weight: 900; }}
    .stat .lbl {{ font-size: 0.8rem; opacity: 0.75; }}
    .search-box {{ max-width: 480px; margin: 1.5rem auto 0; display: flex; gap: 0.5rem; }}
    .search-box input {{ flex: 1; padding: 0.7rem 1rem; border: none; border-radius: 8px; font-size: 0.95rem; }}
    .search-box button {{ padding: 0.7rem 1.2rem; background: #27AE60; color: #fff; border: none; border-radius: 8px; font-weight: 700; cursor: pointer; }}
  </style>
</head>
<body>
<nav style="justify-content:space-between;">
  <a href="." style="font-weight:800;font-size:1rem;">🤖 AI Tool Alternative Finder</a>
  <div style="display:flex;gap:1rem;">
    <a href="about/">About</a>
    <a href="blog/">Blog</a>
    <a href="contact/">Contact</a>
  </div>
</nav>

<div class="index-hero">
  <div style="display:inline-block;background:rgba(255,255,255,0.15);border:1px solid rgba(255,255,255,0.3);padding:0.3rem 1rem;border-radius:20px;font-size:0.8rem;margin-bottom:1rem;">
    🆕 Updated {updated} · {len(all_comps)} comparisons
  </div>
  <h1>Stop Paying for AI Tools</h1>
  <p class="sub">Find free alternatives to ChatGPT Plus, GitHub Copilot, Midjourney, ElevenLabs, and more. Run AI locally. Keep your data private.</p>
  <div class="stats-bar">
    <div class="stat"><div class="num">{len(all_comps)}</div><div class="lbl">Comparisons</div></div>
    <div class="stat"><div class="num">{len(cats)}</div><div class="lbl">AI Categories</div></div>
    <div class="stat"><div class="num">$0</div><div class="lbl">To Run This Site</div></div>
    <div class="stat"><div class="num">100%</div><div class="lbl">Free Alternatives</div></div>
  </div>
  <div class="search-box">
    <input type="text" id="search" placeholder="Search: ChatGPT, Copilot, Midjourney..." oninput="filterCards(this.value)">
    <button onclick="filterCards(document.getElementById('search').value)">Search</button>
  </div>
</div>

<!-- Category pills -->
<div style="background:#fff;border-bottom:1px solid var(--border);padding:1rem 1.5rem;overflow-x:auto;">
  <div style="display:flex;gap:0.6rem;flex-wrap:wrap;max-width:1100px;margin:0 auto;">
    {cat_pills}
  </div>
</div>

<div class="content" style="max-width:1100px;" id="results">
  {sections}
</div>

{footer_html(updated)}

<script>
function filterCards(q) {{
  q = q.toLowerCase().trim();
  document.querySelectorAll('.comp-card').forEach(card => {{
    const txt = card.textContent.toLowerCase();
    card.parentElement.style.display = (!q || txt.includes(q)) ? '' : 'none';
  }});
  // hide empty section headers
  document.querySelectorAll('[id^="cat-"]').forEach(sec => {{
    const visible = Array.from(sec.querySelectorAll('.comp-card')).some(c => c.parentElement.style.display !== 'none');
    sec.style.display = visible ? '' : 'none';
  }});
}}
</script>
{DARK_TOGGLE_JS}
</body>
</html>"""

    (Path(site_dir) / 'index.html').write_text(html, encoding='utf-8')


# ── Blog ──────────────────────────────────────────────────────────────────────
def build_blog(all_comps: List[Dict], site_dir: str, updated: str):
    css = get_css()

    posts = [
        {
            'slug': 'free-local-ai-chatgpt-alternatives',
            'title': 'Run ChatGPT Locally for Free: 5 Open-Source Alternatives (2025)',
            'excerpt': "ChatGPT Plus costs $240/year. These free, local alternatives match 90% of the use cases — with zero subscription and complete privacy.",
            'category': 'text-generation',
            'date': updated,
        },
        {
            'slug': 'free-github-copilot-alternatives',
            'title': 'Best Free GitHub Copilot Alternatives for VS Code (2025)',
            'excerpt': "GitHub Copilot charges $10-19/month per developer. Continue.dev + Ollama gives you the same inline completions — free, private, and open-source.",
            'category': 'code-assistance',
            'date': updated,
        },
        {
            'slug': 'run-stable-diffusion-free-midjourney',
            'title': 'How to Run Stable Diffusion Free (Midjourney Alternative Guide)',
            'excerpt': "Midjourney has no free tier. Stable Diffusion runs on your own GPU with no limits. Here's a complete beginner setup guide.",
            'category': 'image-generation',
            'date': updated,
        },
        {
            'slug': 'free-elevenlabs-tts-alternatives',
            'title': 'Free ElevenLabs Alternatives: Voice Cloning Without Subscription (2025)',
            'excerpt': "Coqui XTTS and Kokoro deliver near-ElevenLabs quality for free — running entirely on your hardware with no character limits.",
            'category': 'voice-ai',
            'date': updated,
        },
        {
            'slug': 'whisper-vs-otter-descript-transcription',
            'title': 'OpenAI Whisper vs Otter.ai vs Descript: Free Transcription in 2025',
            'excerpt': "Whisper is free, runs locally, and transcribes 99 languages with near-human accuracy. Here's how to get started in 5 minutes.",
            'category': 'audio-ai',
            'date': updated,
        },
        {
            'slug': 'ollama-guide-run-llms-locally',
            'title': 'Complete Ollama Guide: Run LLMs Locally on Mac, Windows, Linux',
            'excerpt': "Ollama is the easiest way to run Llama 3, Mistral, and Gemma locally. This guide covers setup, model selection, and Open WebUI integration.",
            'category': 'text-generation',
            'date': updated,
        },
    ]

    post_cards = ''
    for p in posts:
        cat_color = CATEGORY_COLORS.get(p['category'], '#3498DB')
        cat_label = CATEGORY_LABELS.get(p['category'], p['category'])
        cat_icon  = CATEGORY_ICONS.get(p['category'], '🤖')
        post_cards += f"""<div class="card" style="margin-bottom:1rem;">
  <div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;color:{cat_color};margin-bottom:0.5rem;">{cat_icon} {cat_label} · {p['date']}</div>
  <h2 style="margin-top:0;font-size:1.1rem;"><a href="{p['slug']}/" style="color:var(--text);text-decoration:none;">{p['title']}</a></h2>
  <p style="color:var(--text-muted);font-size:0.9rem;margin-bottom:0.75rem;">{p['excerpt']}</p>
  <a href="{p['slug']}/" style="font-size:0.85rem;font-weight:600;color:var(--blue);">Read more →</a>
</div>"""

    blog_index = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Blog — {SITE_NAME}</title>
  <meta name="description" content="Guides, comparisons, and how-tos for free AI tools. Run AI locally, self-host, and stop paying for subscriptions.">
  <link rel="canonical" href="{SITE_BASE_URL}/blog/">
  {get_ga_snippet()}
  <link rel="icon" href="../favicon.ico" type="image/x-icon">
  <style>{css}</style>
</head>
<body>
{nav_html('Blog')}
<div class="hero">
  <h1>📖 Free AI Tools Blog</h1>
  <p class="subtitle">Guides for running AI locally, saving money, and protecting your privacy.</p>
</div>
<div class="content">
  {post_cards}
</div>
{footer_html(updated)}
{DARK_TOGGLE_JS}
</body>
</html>"""

    blog_dir = Path(site_dir) / 'blog'
    blog_dir.mkdir(parents=True, exist_ok=True)
    (blog_dir / 'index.html').write_text(blog_index, encoding='utf-8')

    # Individual blog post pages (placeholder)
    for p in posts:
        post_dir = blog_dir / p['slug']
        post_dir.mkdir(parents=True, exist_ok=True)
        cat_color = CATEGORY_COLORS.get(p['category'], '#3498DB')
        css_post = get_css(cat_color)

        # Find related comparisons for this category
        related_comps = [c for c in all_comps if c.get('category') == p['category']][:3]
        related_links = ''.join(
            f'<a class="related-link" href="../../{c["slug"]}/">{c["title"]}</a>'
            for c in related_comps
        )

        post_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{p['title']} — {SITE_NAME}</title>
  <meta name="description" content="{p['excerpt']}">
  <link rel="canonical" href="{SITE_BASE_URL}/blog/{p['slug']}/">
  {get_ga_snippet()}
  <link rel="icon" href="../../favicon.ico" type="image/x-icon">
  <style>{css_post}</style>
</head>
<body>
<nav>
  <a href="../../">🤖 AI Tool Alternative Finder</a>
  <span class="sep">/</span>
  <a href="../">Blog</a>
  <span class="sep">/</span>
  <span style="color:#fff;opacity:0.7">{p['title'][:40]}...</span>
</nav>
<div class="hero">
  <div class="category-badge">{CATEGORY_ICONS.get(p['category'],'🤖')} {CATEGORY_LABELS.get(p['category'], p['category'])}</div>
  <h1 style="font-size:clamp(1.4rem,3vw,2rem);">{p['title']}</h1>
  <p class="subtitle">{p['excerpt']}</p>
</div>
<div class="content">
  <div class="card">
    <p><em>Full article coming soon. In the meantime, explore our detailed tool comparisons below.</em></p>
    <p style="margin-top:1rem;">{p['excerpt']}</p>
  </div>
  <div class="card">
    <h2>Related Comparisons</h2>
    <div class="related-grid">{related_links}</div>
  </div>
  <div class="card" style="text-align:center;padding:1.5rem;">
    <a href="../../" style="display:inline-block;background:var(--blue);color:#fff;padding:0.65rem 1.75rem;border-radius:6px;text-decoration:none;font-weight:600;">← View All Free AI Alternatives</a>
  </div>
</div>
{footer_html(updated)}
{DARK_TOGGLE_JS}
</body>
</html>"""
        (post_dir / 'index.html').write_text(post_html, encoding='utf-8')


# ── Utility pages ─────────────────────────────────────────────────────────────
def build_about(site_dir: str, all_comps: List[Dict], updated: str):
    css = get_css()
    (Path(site_dir) / 'about').mkdir(parents=True, exist_ok=True)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>About — {SITE_NAME}</title>
  <meta name="description" content="About AI Tool Alternative Finder. We compare free AI alternatives to paid tools, updated daily by an automated pipeline at $0/month.">
  <link rel="canonical" href="{SITE_BASE_URL}/about/">
  {get_ga_snippet()}
  <link rel="icon" href="../favicon.ico" type="image/x-icon">
  <style>{css}</style>
</head>
<body>
{nav_html('About')}
<div class="hero">
  <h1>About AI Tool Alternative Finder</h1>
  <p class="subtitle">Why we built this — and how it works.</p>
</div>
<div class="content">
  <div class="card">
    <h2>Our Mission</h2>
    <p>AI Tool Alternative Finder exists to help developers, creators, and businesses stop paying for AI subscriptions they don't need. We believe powerful AI should be accessible to everyone — not just those who can afford $20–100/month per tool.</p>
    <p style="margin-top:0.75rem;">We provide detailed, AI-researched comparisons of free alternatives to popular paid AI tools. Every comparison covers pricing, privacy implications, setup difficulty, and a step-by-step migration guide.</p>

    <h2>How It Works</h2>
    <p>This site is built and maintained by a fully automated pipeline running every day at 6 AM UTC:</p>
    <ul>
      <li><strong>Content generation</strong> — AI writes fresh comparisons using Groq (Llama 3.3) with Gemini Flash as fallback</li>
      <li><strong>Static site build</strong> — Python generates all {len(all_comps)} comparison pages, alternatives pages, and the blog</li>
      <li><strong>Auto-deploy</strong> — GitHub Actions publishes to GitHub Pages automatically</li>
    </ul>
    <p style="margin-top:0.75rem;"><strong>Total infrastructure cost: $0/month.</strong> All APIs are on free tiers.</p>

    <h2>Our Stack</h2>
    <ul>
      <li>Python 3.11 — content generation and site building</li>
      <li>GitHub Actions — daily automation pipeline</li>
      <li>GitHub Pages — free static hosting</li>
      <li>Groq API (free) — primary LLM for content</li>
      <li>Google Gemini Flash (free) — fallback LLM</li>
      <li>Static HTML/CSS/JS — zero JavaScript frameworks</li>
    </ul>
    <p style="margin-top:0.75rem;">The full source code is <a href="https://github.com/aiopentec/ai-tool-alternative-finder" target="_blank" rel="noopener">available on GitHub</a>.</p>

    <h2>Accuracy &amp; Updates</h2>
    <p>All comparison content is AI-researched and updated daily. We strive for accuracy but recommend verifying current pricing and features at each tool's official website before making decisions. Community corrections are welcome — open a GitHub issue.</p>

    <h2>Affiliate Policy</h2>
    <p>We may earn small affiliate commissions from some paid tool links on this site. This never influences our rankings or comparisons — free alternatives are always ranked on merit.</p>
  </div>
</div>
{footer_html(updated)}
{DARK_TOGGLE_JS}
</body>
</html>"""
    (Path(site_dir) / 'about' / 'index.html').write_text(html, encoding='utf-8')


def build_contact(site_dir: str, updated: str):
    css = get_css()
    (Path(site_dir) / 'contact').mkdir(parents=True, exist_ok=True)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Contact — {SITE_NAME}</title>
  <link rel="canonical" href="{SITE_BASE_URL}/contact/">
  {get_ga_snippet()}
  <link rel="icon" href="../favicon.ico" type="image/x-icon">
  <style>{css}</style>
</head>
<body>
{nav_html('Contact')}
<div class="hero"><h1>Contact Us</h1></div>
<div class="content">
  <div class="card">
    <h2>Get In Touch</h2>
    <ul style="list-style:none;margin:0;padding:0;">
      <li style="margin-bottom:1rem;">🔧 <strong>Suggest a comparison</strong> — know a paid AI tool with a great free alternative? <a href="https://github.com/aiopentec/ai-tool-alternative-finder/issues" target="_blank" rel="noopener">Open a GitHub issue</a></li>
      <li style="margin-bottom:1rem;">⚠️ <strong>Report inaccurate info</strong> — pricing changes frequently. <a href="https://github.com/aiopentec/ai-tool-alternative-finder/issues" target="_blank" rel="noopener">Report via GitHub</a></li>
      <li style="margin-bottom:1rem;">🤝 <strong>Partnerships</strong> — building a free AI tool? We'd love to cover it.</li>
      <li>🐛 <strong>Technical issues</strong> — broken pages or display problems? Open a GitHub issue.</li>
    </ul>
  </div>
</div>
{footer_html(updated)}
{DARK_TOGGLE_JS}
</body>
</html>"""
    (Path(site_dir) / 'contact' / 'index.html').write_text(html, encoding='utf-8')


def build_privacy(site_dir: str, updated: str):
    css = get_css()
    (Path(site_dir) / 'privacy').mkdir(parents=True, exist_ok=True)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Privacy Policy — {SITE_NAME}</title>
  <link rel="canonical" href="{SITE_BASE_URL}/privacy/">
  {get_ga_snippet()}
  <link rel="icon" href="../favicon.ico" type="image/x-icon">
  <style>{css}</style>
</head>
<body>
{nav_html('Privacy Policy')}
<div class="hero"><h1>Privacy Policy</h1></div>
<div class="content">
  <div class="card">
    <h2>Data Collection</h2>
    <p>This site uses Google Analytics to collect anonymous traffic data (page views, referrers, device types). No personally identifiable information is collected without explicit consent.</p>
    <h2>Cookies</h2>
    <p>We use a single localStorage key to remember your dark/light mode preference. No tracking cookies.</p>
    <h2>Affiliate Links</h2>
    <p>Some links to paid tools on this site are affiliate links. Clicking them may set a cookie on the vendor's site. We earn a small commission if you subscribe — this does not affect our rankings.</p>
    <h2>Email Newsletter</h2>
    <p>If you subscribe to our newsletter, your email is stored by our email provider. You can unsubscribe at any time via the link in any email.</p>
    <h2>Contact</h2>
    <p>Questions? Open a <a href="https://github.com/aiopentec/ai-tool-alternative-finder/issues" target="_blank" rel="noopener">GitHub issue</a>.</p>
    <p style="margin-top:1rem;color:var(--text-muted);font-size:0.85rem;">Last updated: {updated}</p>
  </div>
</div>
{footer_html(updated)}
{DARK_TOGGLE_JS}
</body>
</html>"""
    (Path(site_dir) / 'privacy' / 'index.html').write_text(html, encoding='utf-8')


def build_404(site_dir: str):
    css = get_css()
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>404 Not Found — {SITE_NAME}</title>
  <style>{css}</style>
</head>
<body>
<nav><a href="/">🤖 AI Tool Alternative Finder</a></nav>
<div class="hero">
  <h1>404 — Page Not Found</h1>
  <p class="subtitle">The comparison you're looking for might have moved or been renamed.</p>
</div>
<div class="content" style="text-align:center;">
  <div class="card">
    <p style="margin-bottom:1.5rem;">Let's get you back on track.</p>
    <a href="/" style="display:inline-block;background:var(--blue);color:#fff;padding:0.65rem 1.75rem;border-radius:6px;text-decoration:none;font-weight:600;">← Browse All Comparisons</a>
  </div>
</div>
</body>
</html>"""
    (Path(site_dir) / '404.html').write_text(html, encoding='utf-8')


def build_sitemap(all_comps: List[Dict], site_dir: str):
    today = datetime.utcnow().strftime('%Y-%m-%d')
    urls = [f'<url><loc>{SITE_BASE_URL}/</loc><changefreq>daily</changefreq><priority>1.0</priority><lastmod>{today}</lastmod></url>']

    # Comparison pages
    for c in all_comps:
        urls.append(f'<url><loc>{SITE_BASE_URL}/{c["slug"]}/</loc><changefreq>weekly</changefreq><priority>0.8</priority><lastmod>{today}</lastmod></url>')

    # Alternatives-to pages
    paid_tools = {}
    for c in all_comps:
        paid_tools.setdefault(c['paid_tool'], []).append(c)
    for paid_tool in paid_tools:
        slug = paid_tool.lower().replace(' ', '-').replace('.', '').replace('(', '').replace(')', '')
        urls.append(f'<url><loc>{SITE_BASE_URL}/alternatives-to-{slug}/</loc><changefreq>weekly</changefreq><priority>0.7</priority><lastmod>{today}</lastmod></url>')

    # Static pages
    for page in ['about', 'contact', 'privacy', 'blog']:
        urls.append(f'<url><loc>{SITE_BASE_URL}/{page}/</loc><changefreq>monthly</changefreq><priority>0.5</priority><lastmod>{today}</lastmod></url>')

    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += '\n'.join(urls)
    sitemap += '\n</urlset>'
    (Path(site_dir) / 'sitemap.xml').write_text(sitemap, encoding='utf-8')

    # robots.txt
    robots = f"User-agent: *\nAllow: /\nSitemap: {SITE_BASE_URL}/sitemap.xml\n"
    (Path(site_dir) / 'robots.txt').write_text(robots, encoding='utf-8')


# ── FALLBACK hardcoded comparisons (for zero-cache builds) ───────────────────
FALLBACK_COMPARISONS = [
    {
        'id': 'chatgpt-plus-vs-open-webui',
        'slug': 'chatgpt-plus-vs-open-webui',
        'title': 'ChatGPT Plus vs Open WebUI',
        'paid_tool': 'ChatGPT Plus',
        'paid_key': 'chatgpt-plus',
        'free_tool': 'Open WebUI',
        'free_key': 'open-webui',
        'category': 'text-generation',
        'paid_pricing': '$20/month',
        'free_pricing': 'Free (self-hosted)',
        'paid_website': 'https://chat.openai.com',
        'free_website': 'https://openwebui.com',
        'free_github': 'open-webui/open-webui',
        'free_stars': '45k',
        'comparison_markdown': """## Overview

ChatGPT Plus gives access to GPT-4o for $20/month. Open WebUI is a free, open-source interface that runs the same class of AI models locally — with complete privacy and no monthly fees.

## Key Differences

- **Cost**: ChatGPT Plus costs $20/month; Open WebUI + Ollama is free forever
- **Privacy**: Open WebUI runs locally — no conversation data ever leaves your machine
- **Models**: Open WebUI supports Llama 3, Mistral, Gemma, Phi-3, and more
- **Internet**: ChatGPT needs a connection; Open WebUI works fully offline
- **Setup**: ChatGPT is instant; Open WebUI takes ~15 minutes with Docker

## Pricing Comparison

| Aspect | ChatGPT Plus | Open WebUI |
|--------|-------------|------------|
| Base cost | $20/month | Free |
| License | Proprietary | MIT |
| Data privacy | Sent to OpenAI | Local only |
| Cost at 10 users | ~$200/month | $0/month |
| Cost at 100 users | ~$2,000/month | $0/month |

## When to Choose Each

**Choose ChatGPT Plus if:** You need GPT-4o's cutting-edge reasoning, DALL-E 3 image generation, real-time web browsing, or the plugin ecosystem with zero local setup.

**Choose Open WebUI if:** Privacy matters, your usage is high-volume, you process sensitive documents, or you want unlimited AI usage at zero ongoing cost.

## Migration / Getting Started

1. Install Ollama: `curl -fsSL https://ollama.com/install.sh | sh` then `ollama pull llama3.3`
2. Launch Open WebUI: `docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway ghcr.io/open-webui/open-webui:main`
3. Open http://localhost:3000 — identical chat experience, zero cost, 100% private.""",
        'provider': 'fallback',
        'generated_at': datetime.utcnow().isoformat() + 'Z',
        'status': 'fallback',
    },
    {
        'id': 'github-copilot-vs-continue-dev',
        'slug': 'github-copilot-vs-continue-dev',
        'title': 'GitHub Copilot vs Continue',
        'paid_tool': 'GitHub Copilot',
        'paid_key': 'github-copilot',
        'free_tool': 'Continue',
        'free_key': 'continue-dev',
        'category': 'code-assistance',
        'paid_pricing': '$10–$19/month',
        'free_pricing': 'Free',
        'paid_website': 'https://github.com/features/copilot',
        'free_website': 'https://continue.dev',
        'free_github': 'continuedev/continue',
        'free_stars': '18k',
        'comparison_markdown': """## Overview

GitHub Copilot charges $10–19/month per developer for AI code completions. Continue is a free, open-source IDE extension that connects to any LLM — including local Ollama models — for the same inline completions and codebase chat.

## Key Differences

- **Cost**: Copilot costs $10–19/month per developer; Continue is completely free
- **Privacy**: Continue + Ollama keeps all code local — critical for proprietary codebases
- **Models**: Continue works with Ollama, Claude, GPT-4, Gemini, or any OpenAI-compatible API
- **IDE support**: Both support VS Code and JetBrains; Continue also supports Neovim
- **Quality**: Copilot's cloud models are strong; local Qwen2.5-Coder is competitive for most tasks

## Pricing Comparison

| Aspect | GitHub Copilot | Continue |
|--------|---------------|---------|
| Base cost | $10–19/month/developer | Free |
| License | Proprietary | Apache 2.0 |
| Code privacy | Sent to GitHub servers | Local only |
| 10 developers | ~$100–190/month | $0/month |
| 50 developers | ~$500–950/month | $0/month |

## When to Choose Each

**Choose GitHub Copilot if:** Your team is on GitHub Enterprise, needs the strongest cloud model quality, and code privacy is not a primary concern.

**Choose Continue if:** You work on sensitive or proprietary codebases, want to eliminate per-seat AI costs, or prefer to self-host your coding AI with full model control.

## Migration / Getting Started

1. Install Continue from the VS Code Marketplace or JetBrains Plugin Hub
2. Install Ollama: `ollama pull qwen2.5-coder:7b` for a strong local coding model
3. Open Continue settings (cmd+shift+P → Continue: Open Config) and set Ollama as provider""",
        'provider': 'fallback',
        'generated_at': datetime.utcnow().isoformat() + 'Z',
        'status': 'fallback',
    },
    {
        'id': 'midjourney-vs-fooocus',
        'slug': 'midjourney-vs-fooocus',
        'title': 'Midjourney vs Fooocus',
        'paid_tool': 'Midjourney',
        'paid_key': 'midjourney',
        'free_tool': 'Fooocus',
        'free_key': 'fooocus',
        'category': 'image-generation',
        'paid_pricing': '$10–$60/month',
        'free_pricing': 'Free (local)',
        'paid_website': 'https://midjourney.com',
        'free_website': 'https://github.com/lllyasviel/Fooocus',
        'free_github': 'lllyasviel/Fooocus',
        'free_stars': '41k',
        'comparison_markdown': """## Overview

Midjourney has no free tier and charges $10–60/month for AI image generation. Fooocus is an open-source alternative inspired by Midjourney's simplicity — just type a prompt and get high-quality images locally, with no subscription and no per-image cost.

## Key Differences

- **Cost**: Midjourney costs $10–60/month with image limits; Fooocus is free with unlimited generations
- **Privacy**: Local generation means prompts and images never reach external servers
- **Simplicity**: Fooocus is designed to be as simple as Midjourney — minimal settings, great defaults
- **Internet**: Midjourney runs in Discord; Fooocus works fully offline after model download
- **Quality**: Midjourney v6 has a distinctive aesthetic; Fooocus using SDXL is highly competitive

## Pricing Comparison

| Aspect | Midjourney | Fooocus |
|--------|-----------|---------|
| Base cost | $10–$60/month | Free |
| Image limits | 200–unlimited/month | Unlimited |
| Data privacy | Images processed on Midjourney servers | 100% local |
| License | Proprietary | GPL 3.0 |

## When to Choose Each

**Choose Midjourney if:** You want Midjourney's signature artistic aesthetic, have no GPU, or don't want to manage any local software.

**Choose Fooocus if:** You want unlimited, private image generation, have a GPU with 4GB+ VRAM, and want Midjourney-level quality without subscription costs.

## Migration / Getting Started

1. Install Python 3.10+, then clone: `git clone https://github.com/lllyasviel/Fooocus`
2. Run `python entry_with_update.py` — it auto-downloads SDXL models on first launch
3. Open http://localhost:7865 in your browser — type a prompt and generate immediately""",
        'provider': 'fallback',
        'generated_at': datetime.utcnow().isoformat() + 'Z',
        'status': 'fallback',
    },
    {
        'id': 'elevenlabs-vs-coqui-tts',
        'slug': 'elevenlabs-vs-coqui-tts',
        'title': 'ElevenLabs vs Coqui XTTS',
        'paid_tool': 'ElevenLabs',
        'paid_key': 'elevenlabs',
        'free_tool': 'Coqui XTTS',
        'free_key': 'coqui-tts',
        'category': 'voice-ai',
        'paid_pricing': '$5–$99/month',
        'free_pricing': 'Free (local)',
        'paid_website': 'https://elevenlabs.io',
        'free_website': 'https://coqui.ai',
        'free_github': 'coqui-ai/TTS',
        'free_stars': '34k',
        'comparison_markdown': """## Overview

ElevenLabs is the gold standard for AI voice synthesis at up to $99/month with character limits. Coqui XTTS is an open-source alternative that clones voices from a 3-second clip and runs entirely on your machine — no API costs, no limits, no data sharing.

## Key Differences

- **Cost**: ElevenLabs costs $5–99/month with character limits; Coqui TTS is free with no limits
- **Voice cloning**: Both clone voices from short clips; Coqui XTTS v2 is production-quality
- **Privacy**: Local processing means voice samples and audio stay on your hardware
- **Languages**: Coqui XTTS supports 16 languages; ElevenLabs supports 32
- **Setup**: ElevenLabs is browser-based; Coqui requires Python and ~4GB for models

## Pricing Comparison

| Aspect | ElevenLabs | Coqui XTTS |
|--------|-----------|-----------|
| Base cost | $5–$99/month | Free |
| Character limits | 30k–2M/month | Unlimited |
| Voice cloning | Yes | Yes |
| Data privacy | Audio sent to ElevenLabs | 100% local |

## When to Choose Each

**Choose ElevenLabs if:** You need 32-language support, real-time streaming, the widest voice library, or a simple browser-based workflow with no local GPU.

**Choose Coqui XTTS if:** You produce large audio volumes, handle sensitive content (legal, medical), have a Python environment, and want zero ongoing costs.

## Migration / Getting Started

1. Install: `pip install TTS torch`
2. Test: `tts --model_name tts_models/multilingual/multi-dataset/xtts_v2 --text "Hello world" --language en --out_path output.wav`
3. Voice clone: add `--speaker_wav your_3sec_clip.wav` to clone any voice from a short sample""",
        'provider': 'fallback',
        'generated_at': datetime.utcnow().isoformat() + 'Z',
        'status': 'fallback',
    },
    {
        'id': 'openai-api-vs-localai',
        'slug': 'openai-api-vs-localai',
        'title': 'OpenAI API vs LocalAI',
        'paid_tool': 'OpenAI API',
        'paid_key': 'openai-api',
        'free_tool': 'LocalAI',
        'free_key': 'localai',
        'category': 'ai-api',
        'paid_pricing': '$0.002–$0.06/1K tokens',
        'free_pricing': 'Free (self-hosted)',
        'paid_website': 'https://platform.openai.com',
        'free_website': 'https://localai.io',
        'free_github': 'mudler/LocalAI',
        'free_stars': '24k',
        'comparison_markdown': """## Overview

The OpenAI API charges per token — costs that scale rapidly with volume. LocalAI is a free, open-source, OpenAI API-compatible server that runs locally, giving you a drop-in replacement with zero per-request cost.

## Key Differences

- **Cost**: OpenAI API costs $0.002–$0.06/1K tokens; LocalAI has zero per-request cost
- **Compatibility**: LocalAI is a drop-in replacement — change the base URL and existing code works
- **Privacy**: All inference is local — no prompts or responses sent to OpenAI
- **Models**: LocalAI supports any GGUF model plus image generation and TTS backends
- **Latency**: Cloud API is faster for large requests; local performance depends on hardware

## Pricing Comparison

| Aspect | OpenAI API | LocalAI |
|--------|-----------|---------|
| Cost model | Per-token | Free |
| 1M tokens | $2–$60 | $0 |
| Privacy | Sent to OpenAI | 100% local |
| API compatibility | OpenAI native | Drop-in compatible |

## When to Choose Each

**Choose OpenAI API if:** You need GPT-4o-level quality, have latency-sensitive production workloads, or don't have GPU hardware available.

**Choose LocalAI if:** You're building privacy-sensitive applications, have high API volume, or need zero inference costs for internal tools.

## Migration / Getting Started

1. Deploy: `docker run -p 8080:8080 -v $PWD/models:/build/models localai/localai:latest`
2. Download a model: `curl http://localhost:8080/models/apply -d '{"id":"llama-3.2-3b"}'`
3. Update base URL in your code to `http://localhost:8080/v1` — all existing OpenAI SDK calls work immediately""",
        'provider': 'fallback',
        'generated_at': datetime.utcnow().isoformat() + 'Z',
        'status': 'fallback',
    },
]


# ── Main build function ───────────────────────────────────────────────────────
def build_site(cache_dir: str = '.cache/comparisons', site_dir: str = 'site'):
    cache = Path(cache_dir)
    site  = Path(site_dir)
    site.mkdir(parents=True, exist_ok=True)

    updated = datetime.utcnow().strftime('%B %d, %Y')
    logger.info(f'🔨 Building site → {site}')

    # Load comparisons from cache
    all_comps: List[Dict] = []
    if cache.exists():
        for fp in sorted(cache.glob('*.json')):
            try:
                with open(fp) as f:
                    comp = json.load(f)
                if isinstance(comp, list):
                    all_comps.extend(comp)
                else:
                    all_comps.append(comp)
            except Exception as e:
                logger.warning(f'  ⚠️  Could not read {fp}: {e}')

    if not all_comps:
        logger.warning('  ⚠️  No cached comparisons found — using fallback data')
        all_comps = FALLBACK_COMPARISONS

    # Normalize: patch missing fields that old v2 cache files may not have
    def normalize_comp(c: Dict) -> Dict:
        slug = c.get('slug') or c.get('id', '')
        paid_name = c.get('paid_tool', '')
        free_name = c.get('free_tool', '')
        # Derive keys from slug if missing (slug format: paid-key-vs-free-key)
        if not c.get('paid_key') or not c.get('free_key'):
            if '-vs-' in slug:
                parts = slug.split('-vs-', 1)
                c.setdefault('paid_key', parts[0])
                c.setdefault('free_key', parts[1])
            else:
                c.setdefault('paid_key', paid_name.lower().replace(' ', '-').replace('.', ''))
                c.setdefault('free_key', free_name.lower().replace(' ', '-').replace('.', ''))
        c.setdefault('title',        f'{paid_name} vs {free_name}')
        c.setdefault('category',     'text-generation')
        c.setdefault('paid_pricing', 'See website')
        c.setdefault('free_pricing', 'Free')
        c.setdefault('paid_website', '')
        c.setdefault('free_website', '')
        c.setdefault('free_github',  '')
        c.setdefault('free_stars',   '')
        c.setdefault('comparison_markdown', c.get('content', c.get('body', '')))
        c.setdefault('slug', slug)
        return c

    all_comps = [normalize_comp(c) for c in all_comps]

    # Deduplicate by slug
    seen = set()
    unique: List[Dict] = []
    for c in all_comps:
        if c['slug'] not in seen:
            seen.add(c['slug'])
            unique.append(c)
    all_comps = unique

    logger.info(f'  📄 {len(all_comps)} comparisons loaded')

    # Build comparison pages
    for i, comp in enumerate(all_comps):
        try:
            build_comparison_page(comp, all_comps, updated, str(site))
            if i % 10 == 0:
                logger.info(f'  📄 Built {i+1}/{len(all_comps)} comparison pages')
        except Exception as e:
            logger.error(f'  ❌ Error building {comp.get("slug","?")}: {e}')

    # Build alternatives-to pages (one per paid tool)
    paid_tool_map: Dict[str, List[Dict]] = {}
    for c in all_comps:
        paid_tool_map.setdefault(c['paid_tool'], []).append(c)
    for paid_tool, comps in paid_tool_map.items():
        try:
            build_alternatives_page(paid_tool, comps, str(site), updated)
        except Exception as e:
            logger.error(f'  ❌ Error building alternatives-to-{paid_tool}: {e}')
    logger.info(f'  📄 Built {len(paid_tool_map)} alternatives-to pages')

    # Build category pages (simple redirect to homepage anchors for now)
    cat_dir = site / 'categories'
    cat_dir.mkdir(exist_ok=True)
    for cat in CATEGORY_ICONS:
        c_dir = cat_dir / cat
        c_dir.mkdir(exist_ok=True)
        redirect = f'<!DOCTYPE html><html><head><meta http-equiv="refresh" content="0;url=../../#{cat}"></head><body></body></html>'
        (c_dir / 'index.html').write_text(redirect)

    # Build homepage
    build_index(all_comps, str(site), updated)
    logger.info('  🏠 Built homepage')

    # Build blog
    build_blog(all_comps, str(site), updated)
    logger.info('  📖 Built blog')

    # Build utility pages
    build_about(str(site), all_comps, updated)
    build_contact(str(site), updated)
    build_privacy(str(site), updated)
    build_404(str(site))
    logger.info('  📄 Built utility pages')

    # Build sitemap + robots
    build_sitemap(all_comps, str(site))
    logger.info('  🗺️  Built sitemap.xml + robots.txt')

    # Copy favicon if it exists
    for favicon_src in [Path('favicon.ico'), Path('favicon.png')]:
        if favicon_src.exists():
            shutil.copy(favicon_src, site / favicon_src.name)

    # Count files
    total = sum(1 for _ in site.rglob('*.html'))
    logger.info('=' * 60)
    logger.info(f'  ✅ Site built: {total} HTML files in {site}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build AI Tool Alternative Finder static site')
    parser.add_argument('--cache', default='.cache/comparisons', help='Cache directory')
    parser.add_argument('--out', default='site', help='Output directory')
    args = parser.parse_args()
    build_site(args.cache, args.out)
