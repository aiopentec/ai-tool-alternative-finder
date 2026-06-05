"""
fix_dark_final.py
  python fix_dark_final.py

fix_new_css_braces.py over-corrected — it doubled braces in all 29
[data-theme="dark"] blocks, including the original ones that live in
a REGULAR string (not an f-string). Doubling in a regular string
outputs literal {{ in the HTML, breaking those CSS selectors.

This script:
  1. Restores from scripts/build.py.bak_css2 (state after
     fix_dark_important.py but before the mass brace-doubling)
  2. Inserts ONLY the new CSS blocks (.card[style] + verdict overrides)
     with braces PRE-DOUBLED so they are safe in the f-string context
  3. Runs ast.parse() to verify
  4. Saves

After this, the rendered HTML will have:
  - Original [data-theme="dark"] rules: single { } (from regular string) ✅
  - New .card[style] + verdict rules: single { } (unescaped from f-string) ✅
  - @media dark block: single { } (unescaped from f-string) ✅
"""

import ast
import shutil
import sys
from pathlib import Path

BUILD   = Path("scripts/build.py")
BAK_SRC = Path("scripts/build.py.bak_css2")  # state after fix_dark_important, before mass doubling
BAK_OUT = Path("scripts/build.py.bak_dark_final")

if not BAK_SRC.exists():
    sys.exit(f"ERROR: {BAK_SRC} not found. Cannot restore.")

shutil.copy(BUILD, BAK_OUT)
print(f"✅ Current state saved → {BAK_OUT}")

# Restore the pre-mass-doubling state
shutil.copy(BAK_SRC, BUILD)
print(f"✅ Restored from {BAK_SRC}\n")

src = BUILD.read_text(encoding="utf-8")

# ── Verify the NameError-causing blocks are present ───────────────────────────
# fix_dark_important.py inserted two blocks with single braces into the f-string.
# We'll remove them and re-insert with doubled braces.

# ── BLOCK 1: .card[style] override ───────────────────────────────────────────
# The block starts with this comment:
CARD_COMMENT = "/* Override inline style= attributes on cards in dark mode */"

# Pre-doubled version (safe inside f-string)
CARD_STYLE_DOUBLED = """
    /* Override inline style= attributes on cards in dark mode */
    [data-theme="dark"] .card[style] {{
      background: var(--card) !important;
      border-color: var(--border) !important;
    }}
    [data-theme="dark"] .card[style] h2 {{ color: #58a6ff !important; }}
    [data-theme="dark"] .card[style] p  {{ color: #8b949e !important; }}
    [data-theme="dark"] .card[style] a  {{ color: #58a6ff !important; }}"""

# ── BLOCK 2: verdict-switch/stay overrides ────────────────────────────────────
VERDICT_COMMENT = "[data-theme=\"dark\"] .verdict-switch {"
VERDICT_STAY_COMMENT = "[data-theme=\"dark\"] .verdict-stay {"

VERDICT_DOUBLED = """
    [data-theme="dark"] .verdict-switch {{
      background: #1b2d1f !important;
      border-color: #238636 !important;
    }}
    [data-theme="dark"] .verdict-switch .verdict-label {{ color: #3fb950 !important; }}
    [data-theme="dark"] .verdict-switch .verdict-text  {{ color: #c9d1d9 !important; }}
    [data-theme="dark"] .verdict-stay {{
      background: #272115 !important;
      border-color: #9e6a03 !important;
    }}
    [data-theme="dark"] .verdict-stay .verdict-label {{ color: #d4a843 !important; }}
    [data-theme="dark"] .verdict-stay .verdict-text  {{ color: #c9d1d9 !important; }}"""

# ── Remove existing single-brace versions if present ─────────────────────────
# (fix_dark_important.py may have inserted them with single braces)

removed = []

# Remove card[style] block (single-brace version)
if CARD_COMMENT in src:
    # Find start of the comment block
    start = src.index(CARD_COMMENT)
    # Walk back to find the newline before the comment
    while start > 0 and src[start-1] in " \t\n":
        start -= 1
    # Find end: next </style> occurrence or next blank line after rules
    # The block ends after the last rule in the inserted section
    # Look for the next CSS comment or </style> after the block
    search_from = src.index(CARD_COMMENT) + len(CARD_COMMENT)
    # Find closing of last rule in this block (4 rules, each ending with } or ;)
    # Simpler: find the end by looking for the next \n\n or </style>
    end_markers = ["</style>", "\n\n    [data-theme", "\n\n    @media", "\n    </style>"]
    end = len(src)
    for marker in end_markers:
        pos = src.find(marker, search_from)
        if pos != -1 and pos < end:
            end = pos
    removed_block = src[start:end]
    src = src[:start] + src[end:]
    removed.append(".card[style] block")
    print(f"  Removed single-brace .card[style] block ({len(removed_block)} chars)")

# Remove verdict-switch/stay block (single-brace version, if separate from original)
# Only remove if it was added by fix_dark_important (check for doubled rules)
# The original verdict-box rule is [data-theme="dark"] .verdict-box { ... }
# The new ones are verdict-switch and verdict-stay sub-rules
# Look for the pattern added by fix_dark_important:
VERDICT_MARKER = '    [data-theme="dark"] .verdict-switch {\n      background: #1b2d1f !important;'
if VERDICT_MARKER in src:
    start = src.index(VERDICT_MARKER)
    while start > 0 and src[start-1] in " \t\n":
        start -= 1
    search_from = src.index(VERDICT_MARKER)
    end = len(src)
    for marker in ["</style>", "\n\n    [data-theme", "\n    </style>"]:
        pos = src.find(marker, search_from)
        if pos != -1 and pos < end:
            end = pos
    removed_block = src[start:end]
    src = src[:start] + src[end:]
    removed.append("verdict-switch/stay block")
    print(f"  Removed single-brace verdict block ({len(removed_block)} chars)")

if not removed:
    print("  ℹ️  No single-brace blocks found to remove (may already be clean)")

# ── Insert pre-doubled versions before </style> ───────────────────────────────
print("\n── Inserting pre-doubled CSS blocks ────────────────────────────")

if "</style>" in src:
    insert_point = src.index("</style>")
    insertion = CARD_STYLE_DOUBLED + VERDICT_DOUBLED + "\n    "
    src = src[:insert_point] + insertion + src[insert_point:]
    print("  ✅ Inserted .card[style] block (pre-doubled braces)")
    print("  ✅ Inserted verdict-switch/stay block (pre-doubled braces)")
else:
    sys.exit("ERROR: No </style> found in build.py. Cannot insert CSS.")

# ── Syntax check ─────────────────────────────────────────────────────────────
print("\n── Syntax check ────────────────────────────────────────────────")
try:
    ast.parse(src)
    print("  ✅ Passed")
    BUILD.write_text(src, encoding="utf-8")
    print("  ✅ build.py saved\n")
except SyntaxError as e:
    shutil.copy(BAK_OUT, BUILD)
    print(f"  ❌ SyntaxError at line {e.lineno}: {e.msg}")
    print(f"     Text: {(e.text or '').strip()!r}")
    print("  build.py restored from backup.")
    sys.exit(1)

print("""── WHAT THIS FIXES ─────────────────────────────────────────────

  Original [data-theme="dark"] rules: in a REGULAR string → single
  braces render correctly as { } in HTML output. We do NOT touch these.

  New .card[style] + verdict rules: in the F-STRING template → braces
  must be {{ }} which Python unescapes to { } in the rendered HTML.

  @media (prefers-color-scheme: dark): also in f-string, already {{ }}.

── NEXT ────────────────────────────────────────────────────────

  1. Build and verify NO errors:
       python scripts/build.py

  2. Open site/openai-api-vs-localai/index.html in Chrome
     Click Dark — difficulty card, GitHub card, verdict boxes
     should all go dark.

  3. Commit:
       git add scripts/build.py
       git commit -m "fix: dark mode CSS pre-doubled braces for f-string safety"
       git push

  4. Actions → Run workflow → Force regenerate: false
""")