#!/bin/sh
# Copies the deployable static site into dist/ (no transforms — the committed HTML is already final).
set -eu
rm -rf dist
mkdir -p dist
# Root files
for f in index.html 404.html favicon.svg manus-routes.json robots.txt sitemap.xml _redirects google59d6c1a82a1cce60.html; do
  [ -f "$f" ] && cp "$f" dist/
done
# Shared assets
cp -R assets dist/
# Every route folder (anything that contains an index.html, except tooling folders)
for d in */; do
  d="${d%/}"
  case "$d" in assets|dist|docs|node_modules|partials|scripts) continue ;; esac
  if [ -f "$d/index.html" ]; then cp -R "$d" dist/; fi
done
# Apache / LiteSpeed rules for Hostinger (Vercel ignores this file)
node scripts/make-htaccess.mjs _redirects dist/.htaccess
printf 'Static site built in dist/\n'
