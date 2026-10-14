# Code & Canvas — native site

Standalone, bilingual (English / Arabic, LTR / RTL) Code & Canvas site built with semantic HTML, CSS and vanilla JavaScript. It is native website code, not a WordPress theme, and has no runtime framework or package dependencies.

| Route | What it is |
| --- | --- |
| `/` | Homepage: hero, services catalogue (15 services, filterable), CanvasOne ERP teaser, why us, approach, contact |
| `/erp/` | CanvasOne ERP interactive proposal (modules, industries, compliance, delivery timeline, package builder, FAQ, print-to-PDF) |

Both pages share one design system — dark navy canvas, violet / teal / pink gradients, glass panels, preloader, scroll progress, cursor glow, tilt and magnetic buttons — taken from the CanvasOne ERP proposal.

## Run locally

```sh
npm run dev
```

Open <http://localhost:3000> (home) and <http://localhost:3000/erp/> (ERP). `PORT=4000 npm run dev` changes the port. The dev server is a zero-dependency Node script (`dev-server.mjs`).

## Build

```sh
npm run build
```

Static files are written to `dist/`. Preview with `node dev-server.mjs dist`.

## Structure

```
index.html               homepage (English markup; Arabic sits beside it in data-ar* attributes)
erp/index.html           ERP proposal shell (content is rendered from erp-data.js)
assets/
├── css/ds.css           shared design system (tokens, glass, buttons, nav, footer, timeline, orbit…)
├── css/home.css         homepage-only components
├── css/erp.css          ERP-only components (+ print stylesheet)
├── js/site.js           shared runtime: language, icons, preloader, reveal, tilt, nav, progress…
├── js/home.js           homepage behaviour (filters, marquee, orbit, meta per language)
├── js/erp-data.js       ALL ERP copy, bilingual { ar, en }
├── js/erp-app.js        ERP rendering and interactions
└── brand/               Code & Canvas logos (SVG)
```

## Language

- `?lang=ar` / `?lang=en` forces a language. The choice is remembered (`localStorage`, key `cc-lang`) and shared by `/` and `/erp/`. With no choice, Arabic browsers get Arabic and everything else gets English.
- **Homepage:** write English in the HTML and put the Arabic in `data-ar="…"` on the same element (`data-ar-html` when the text contains markup, `data-ar-label` / `data-ar-title` for attributes). Page title and meta description per language live in `home.js`.
- **ERP:** edit `assets/js/erp-data.js`; every text field is `{ ar: '…', en: '…' }`.
- Use CSS logical properties (`margin-inline-start`, `inset-inline-end`…) so one rule serves both directions. Wrap prices and numeric ranges in Arabic strings with LRI/PDI isolates (`⁦…⁩`) so they keep their visual order.

## Fonts

Loaded from Google Fonts in each page `<head>`: Alexandria and IBM Plex Sans Arabic (Arabic), Raleway and Fraunces Italic (English), Comfortaa (wordmark). All are SIL OFL. To self-host, download the `woff2` files, add `@font-face` rules to `ds.css` and remove the `<link>`.

## Scope

This repository contains an independently developed site for review. It does not modify the existing production website, its domain, DNS, or any production deployment. Pricing, service details, contact methods and destination links were taken from <https://codeandcanvas.net/>. Navigation links to the current service, story and contact pages point at the live site until those routes are rebuilt separately. `manus-routes.json` lists the preview routes (`/` and `/erp/`).

## Before publishing the ERP page

`assets/js/erp-data.js`: confirm that the compliance claims (KSA: ZATCA phase 2, VAT 15%, GOSI / WPS-Mudad, Hijri calendar; Egypt: ETA e-invoice / e-receipt, VAT 14%, social insurance), module features and go-live durations match the licensed product. The proposal deliberately contains no client counts, logos, testimonials or prices. The homepage teaser avoids the compliance claims on purpose.
