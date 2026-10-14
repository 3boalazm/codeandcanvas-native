# -*- coding: utf-8 -*-
"""Dump the visible English text of every native page to docs/audit/native/<route>.txt (audit helper)."""
import os, re, html, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'docs', 'audit', 'native')
SKIP = {'node_modules', 'dist', '.git', 'partials', 'docs', 'scripts', 'assets'}

def text_of(src):
    # keep only <main>…</main> when present (drop shared chrome)
    m = re.search(r'<main[^>]*>([\s\S]*?)</main>', src)
    body = m.group(1) if m else src
    body = re.sub(r'<script[\s\S]*?</script>|<style[\s\S]*?</style>', ' ', body)
    body = re.sub(r'<(br|/p|/h[1-6]|/li|/div|/section|/article|/tr|/summary|/dt|/dd|/blockquote)[^>]*>', '\n', body)
    body = re.sub(r'<[^>]+>', ' ', body)
    body = html.unescape(body)
    lines = [re.sub(r'[ \t\u00a0]+', ' ', l).strip() for l in body.split('\n')]
    out, prev = [], None
    for l in lines:
        if l and l != prev:
            out.append(l)
        prev = l
    return '\n'.join(out)

for dirpath, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in SKIP]
    for f in files:
        if not f.endswith('.html'):
            continue
        p = os.path.join(dirpath, f)
        rel = os.path.relpath(p, ROOT)
        name = rel.replace('/index.html', '').replace('.html', '').replace('/', '__') or 'home'
        with open(p, encoding='utf-8') as fh:
            txt = text_of(fh.read())
        with open(os.path.join(OUT, name + '.txt'), 'w', encoding='utf-8') as fh:
            fh.write(txt)
print('ok', len(os.listdir(OUT)))
