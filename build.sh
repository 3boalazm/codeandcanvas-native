#!/bin/sh
set -eu
rm -rf dist
mkdir -p dist/assets/brand
cp index.html styles.css canvasone-touch.css script.js canvasone-touch.js favicon.svg manus-routes.json dist/
cp assets/brand/icon-white.svg assets/brand/logo-white-horizontal.svg dist/assets/brand/
printf 'Static site built in dist/\n'
