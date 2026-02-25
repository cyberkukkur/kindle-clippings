#!/usr/bin/env python3
"""
Kindle Clippings Updater
------------------------
1. Connect your Kindle via USB
2. Copy 'My Clippings.txt' from your Kindle into this folder
3. Run:  python update.py
4. Wait ~30 seconds, then refresh the app on your phone

The script parses your clippings, injects them into index.html,
and pushes to GitHub Pages so your phone always has the latest data.
"""

import re
import json
import os
import sys
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, 'My Clippings.txt')
HTML_FILE  = os.path.join(SCRIPT_DIR, 'index.html')


def parse_clippings(text):
    entries = text.split('==========')
    clippings = []
    seen = set()
    for entry in entries:
        entry = entry.strip()
        if not entry:
            continue
        lines = entry.split('\n')
        if len(lines) < 2:
            continue
        title_raw = lines[0].lstrip('\ufeff').strip()
        meta      = lines[1].strip()
        body      = '\n'.join(lines[2:]).strip()
        m      = re.match(r'^(.*?)\s*\(([^)]+)\)\s*$', title_raw)
        title  = m.group(1).strip() if m else title_raw
        author = m.group(2).strip() if m else ''
        tm   = re.search(r'Your (Highlight|Note|Bookmark)', meta)
        typ  = tm.group(1) if tm else 'Unknown'
        if typ == 'Bookmark' and not body:
            continue
        dm   = re.search(r'Added on (.+)$', meta)
        date = dm.group(1).strip() if dm else ''
        pm   = re.search(r'[Pp]age (\d+)', meta)
        page = int(pm.group(1)) if pm else None
        lm       = re.search(r'[Ll]ocation[s]? ([\d-]+)', meta)
        location = lm.group(1) if lm else None
        key = title + '|||' + body
        if key in seen:
            continue
        seen.add(key)
        clippings.append({
            'title': title, 'author': author, 'type': typ,
            'date': date, 'page': page, 'location': location, 'text': body,
        })
    return clippings


def run(cmd, cwd=None):
    result = subprocess.run(cmd, shell=True, cwd=cwd or SCRIPT_DIR,
                            capture_output=True, text=True)
    if result.returncode != 0:
        print(f'ERROR running: {cmd}')
        print(result.stderr.strip())
        sys.exit(1)
    return result.stdout.strip()


def main():
    # ── Check input file ──
    if not os.path.exists(INPUT_FILE):
        print('ERROR: "My Clippings.txt" not found in this folder.')
        print(f'       Expected: {INPUT_FILE}')
        print()
        print('Steps:')
        print('  1. Connect your Kindle via USB')
        print('  2. Copy "My Clippings.txt" from your Kindle into this folder')
        print('  3. Run this script again')
        sys.exit(1)

    if not os.path.exists(HTML_FILE):
        print('ERROR: "index.html" not found in this folder.')
        sys.exit(1)

    # ── Parse ──
    print('Reading My Clippings.txt ...')
    with open(INPUT_FILE, 'r', encoding='utf-8-sig') as f:
        raw = f.read()

    print('Parsing...')
    clippings = parse_clippings(raw)
    books = len(set(c['title'] for c in clippings))
    print(f'  {len(clippings):,} clippings across {books:,} books')

    # ── Inject into HTML ──
    print('Updating index.html...')
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html = f.read()

    if '// DATA_START' not in html:
        print('ERROR: index.html is missing data markers. Please re-download it.')
        sys.exit(1)

    data_json = json.dumps(clippings, ensure_ascii=False)
    new_block  = f'// DATA_START\nconst EMBEDDED_DATA = {data_json};\n// DATA_END'
    html = re.sub(r'// DATA_START.*?// DATA_END', new_block, html, flags=re.DOTALL)

    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  Done ({os.path.getsize(HTML_FILE)/1_000_000:.1f} MB)')

    # ── Push to GitHub ──
    print('Pushing to GitHub...')

    # Check git is available
    try:
        subprocess.run('git --version', shell=True, check=True,
                       capture_output=True)
    except subprocess.CalledProcessError:
        print()
        print('NOTE: git is not installed, so the app was not pushed to GitHub.')
        print('      Install git from https://git-scm.com and run this script again.')
        print('      Your index.html has been updated locally.')
        sys.exit(0)

    # Check we're in a git repo
    result = subprocess.run('git rev-parse --is-inside-work-tree', shell=True,
                            cwd=SCRIPT_DIR, capture_output=True, text=True)
    if result.returncode != 0:
        print()
        print('NOTE: This folder is not a git repository.')
        print('      Follow the setup instructions in SETUP.md to connect to GitHub.')
        sys.exit(0)

    run('git add index.html')
    run('git commit -m "Update clippings data"')
    run('git push')

    print()
    print('✓ Done! Your app will update in ~30 seconds.')
    print('  Open: https://cyberkukkur.github.io/kindle-clippings')


if __name__ == '__main__':
    main()
