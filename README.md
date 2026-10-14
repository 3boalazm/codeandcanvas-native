# Code & Canvas — native homepage

A standalone, responsive Code & Canvas homepage built with semantic HTML, CSS, and vanilla JavaScript. It is native website code, not a WordPress theme, and has no runtime framework or package dependencies.

The design follows the supplied Code & Canvas page reference and borrows selected visual cues from the CanvasOne ERP presentation: a split, glass-panel hero; soft violet/teal atmosphere; connected workflow cards; gradient scroll progress; active section navigation; restrained pointer tilt and card light; and subtle section reveals. The hero workflow uses the actual Listen / Shape / Deliver approach already shown on the live site, rather than invented metrics or client data. Motion is disabled or reduced for `prefers-reduced-motion`.

## Run locally

```sh
npm run dev
```

Open <http://localhost:3000>.

## Build

```sh
npm run build
```

The static production files are written to `dist/`, including the original Code & Canvas wordmark and icon under `dist/assets/brand/`. To preview that output:

```sh
python3 -m http.server 3000 --directory dist --bind 0.0.0.0
```

## Scope

This repository contains an independently developed homepage for review. It does not modify the existing production website, its domain, DNS, or any production deployment. Current pricing, service details, contact methods, and destination links were taken from <https://codeandcanvas.net/>. Navigation links to the current service, story, and contact pages remain until those routes are rebuilt separately. The root project also includes `manus-routes.json` for the single-page preview route.
