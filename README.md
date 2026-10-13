# Code & Canvas — native homepage

A standalone, responsive Code & Canvas homepage built with semantic HTML, CSS, and vanilla JavaScript. It is not a WordPress theme and has no runtime framework or package dependencies.

## Run locally

```sh
npm run dev
```

Open <http://localhost:3000>.

## Build

```sh
npm run build
```

The static production files are written to `dist/`. To preview that output:

```sh
python3 -m http.server 3000 --directory dist --bind 0.0.0.0
```

## Scope

This repository contains a separately developed homepage for review. It does not modify the existing WordPress website, its domain, DNS, or any production deployment. Current pricing, service details, contact methods, and destination links were taken from <https://codeandcanvas.net/>. The navigation links to the site's current service, story, and contact pages until those routes are rebuilt separately.
