#!/bin/sh
set -eu
rm -rf dist
mkdir -p dist
cp index.html favicon.svg manus-routes.json dist/
cp -R assets erp dist/
printf 'Static site built in dist/\n'
