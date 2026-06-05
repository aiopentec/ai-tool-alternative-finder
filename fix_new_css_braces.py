"""
fix_new_css_braces.py
  python fix_new_css_braces.py

fix_dark_important.py inserted CSS blocks with single { } braces
into the f-string template. Python tries to evaluate {background
as an f-string expression → NameError: name 'background' is not defined.

This script finds every CSS rule block that still has single braces
(i.e. NOT already doubled to {{ }}) and doubles them.

Safe: skips Python f-string expressions like {comp['slug']} by only
targeting text that looks like CSS selector { property: value } blocks.

Creates scripts/build.py.bak_css2 first.
"""

import ast
import re
import shutil
import sys
from pathlib import Path

BUILD = Path("scripts/build.py")
BAK   = Path("scripts/build.py.bak_css2")

if not BUILD.exists():
    sys.exit("ERROR: scripts/build.py not found.")

shutil.copy(BUILD, BAK)
print(f"✅ Backup → {BAK}\n")

src = BUILD.read_text(encoding="utf-8")

def double_braces_in_block(text: str) -> str:
    """Doubles single { } in CSS text. Idempotent: skips already-doubled {{ }}."""
    out = []
    i = 0
    while i < len(text):
        ch = text[i]
        if ch in "{}":
            nxt = text[i + 1] if i + 1 < len(text) else ""
            if nxt == ch:          # already {{ or }} — keep and skip both
                out.append(ch * 2)
                i += 2
            else:                  # single — double it
                out.append(ch * 2)
                i += 1
        else:
            out.append(ch)
            i += 1
    return "".join(out)

# ─────────────────────────────────────────────────────────────────────────────
# Strategy: find all CSS selector blocks that have single { } braces
# by scanning for [data-theme="dark"] selectors followed by a single {
# (not {{).  These are the ones we need to fix.
#
# Pattern: [data-theme="dark"] .something { ... } with single braces
# We find the { character that starts the rule body and track depth
# to find the matching }, then double all braces in that span.
# ─────────────────────────────────────────────────────────────────────────────

print("── Finding CSS blocks with single braces ───────────────────────")

# Find all positions of [data-theme="dark"] in the source
selector_pattern = re.compile(r'\[data-theme="dark"\][^{]*(?<!\{)\{(?!\{)')

fixed_count = 0
offset = 0  # track position shifts as we modify src

while True:
    # Re-search from scratch each iteration (src changes)
    m = selector_pattern.search(src, offset)
    if not m:
        break

    # The { that ends the match is the opening brace of the CSS rule
    open_brace_pos = m.end() - 1  # position of the {

    # Verify it's actually a single { (not {{)
    if open_brace_pos + 1 < len(src) and src[open_brace_pos + 1] == "{":
        # Already doubled — skip past this match
        offset = m.end()
        continue

    # Find the matching closing } by tracking depth
    depth = 0
    close_brace_pos = open_brace_pos
    for i in range(open_brace_pos, min(open_brace_pos + 5000, len(src))):
        if src[i] == "{" and (i + 1 >= len(src) or src[i + 1] != "{"):
            depth += 1
        elif src[i] == "{" and i + 1 < len(src) and src[i + 1] == "{":
            depth += 1  # count {{ as one
            # skip the second { in the depth tracking
        elif src[i] == "}" and (i == 0 or src[i - 1] != "}"):
            depth -= 1
            if depth == 0:
                close_brace_pos = i
                break

    if close_brace_pos == open_brace_pos:
        # Couldn't find closing brace — skip
        offset = m.end()
        continue

    # Extract the CSS block (from selector start to closing })
    block_start = m.start()
    block_end   = close_brace_pos + 1
    raw_block   = src[block_start:block_end]

    # Double all braces in this block
    fixed_block = double_braces_in_block(raw_block)

    if fixed_block != raw_block:
        src = src[:block_start] + fixed_block + src[block_end:]
        fixed_count += 1
        selector_text = raw_block[:60].replace("\n", " ").strip()
        print(f"  ✅ Fixed: {selector_text}...")
        # Don't advance offset — re-scan from same position since src changed
        # but use block_start + len(fixed_block) to avoid re-processing
        offset = block_start + len(fixed_block)
    else:
        offset = m.end()

print(f"\n  Total blocks fixed: {fixed_count}")

# ─────────────────────────────────────────────────────────────────────────────
# Also fix the @media block's newly-added nested rules if any slipped through
# ─────────────────────────────────────────────────────────────────────────────

# Find any remaining single { that appear after CSS property patterns
# like "background: " or "border-color: " — these are definitely CSS
remaining = re.findall(r'(?<!\{)\{(?!\{)\s*\n\s+(?:background|border|color|margin|padding|font)', src)
if remaining:
    print(f"\n  ⚠️  {len(remaining)} possible remaining single-brace CSS blocks found.")
    print("     These may need manual review.")
else:
    print("\n  ✅ No remaining single-brace CSS blocks detected.")

# ─────────────────────────────────────────────────────────────────────────────
# SYNTAX CHECK
# ─────────────────────────────────────────────────────────────────────────────
print("\n── Syntax check ────────────────────────────────────────────────")
try:
    ast.parse(src)
    print("  ✅ Passed")
    BUILD.write_text(src, encoding="utf-8")
    print("  ✅ build.py saved\n")
except SyntaxError as e:
    shutil.copy(BAK, BUILD)
    print(f"  ❌ SyntaxError at line {e.lineno}: {e.msg}")
    print(f"     Text: {(e.text or '').strip()!r}")
    print("  build.py restored from backup.")
    sys.exit(1)

print("""── NEXT ────────────────────────────────────────────────────────

  1. Build:
       python scripts/build.py

  2. Confirm no errors (should see 'Built 1/5 comparison pages'):
       Look for:  ❌ Error building  ← should be gone

  3. Commit and push:
       git add scripts/build.py
       git commit -m "fix: double CSS braces in dark mode !important blocks"
       git push

  4. Trigger Actions → Run workflow → Force regenerate: false
""")