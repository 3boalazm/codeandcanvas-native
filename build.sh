#!/bin/sh
set -eu
rm -rf dist
mkdir -p dist
cp index.html styles.css script.js favicon.svg manus-routes.json dist/
printf 'Static site built in dist/\n'
