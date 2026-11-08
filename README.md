# Code & Canvas — native site

> **Current state (2026-11-08):** the 2026-11 audit overhaul is implemented and verified on `arena/f3440ff7-codeandcanvas-native`. Start with [`docs/OVERHAUL-2026-11.md`](docs/OVERHAUL-2026-11.md) for the staged closure, [`docs/PRODUCTION-VERIFICATION.md`](docs/PRODUCTION-VERIFICATION.md) for what the live domain actually serves, and [`docs/PUBLISH-GATE.md`](docs/PUBLISH-GATE.md) before any release. **Nothing on this branch has been merged or deployed.** Older `docs/*-2026-10-14` files are historical snapshots, not current instructions.

A standalone, bilingual (English / Arabic, LTR / RTL) Code & Canvas site: semantic HTML, one CSS design system and vanilla JavaScript for the browser, plus a zero-dependency Node service for the first-party lead pipeline. No runtime framework, no WordPress, no third-party tracker loaded by default.

| Route | What it is |
| --- | --- |
| `/` | Value-first homepage: positioning, selected work, four pillars, trust strip (`/claims/`), markets and content funnel |
| `/work/` · `/work/<slug>/` | Visual portfolio hub + 4 **labelled concept studies** (brand system, packaging, product UI, web experience) with an evidence gate |
| `/case-studies/` | The three documented shipped systems (unchanged evidence caveats) |
| `/services/` · 7 `/services/<slug>/` | 23-service catalogue, four positioning pillars, plus standalone landings with `Service` + `FAQPage` JSON-LD |
| `/technology-services/` · `/creative-services/` · `/healthcare/` · `/methodology/` · `/pricing-faq/` | Existing track, methodology and pricing pages |
| `/book/` | First-party 30-minute booking: specialty → published slots → timezone → consent → server confirmation → `.ics` |
| `/contact/` | Consent-aware contact form posting to `/api/contact`; explicit manual hand-off only when the API cannot confirm |
| `/claims/` | Public evidence register for every removed / qualified claim |
| `/saudi-arabia/` · `/egypt/` | City-level local pages, unified NAP, `ProfessionalService` schema; no invented addresses or reviews |
| `/resources/` | Honest status of the books / accounts / checkout flows |
| `/blog/` · 10 `/blog/<slug>/` | Insights hub with **all 10 articles published** (including the two previously "coming soon"), article → service → work → CTA → book funnel |
| `/about/` · `/our-story/` · `/team/` | Studio, story and founders — labelled illustrative artwork, real photography is an owner gate |
| `/erp/` · `/clinic-review/` | CanvasOne ERP proposal and the standalone Arabic clinic intake review |
| `/privacy-policy/` · `/terms-of-use/` · `/cookie-policy/` · `/404.html` | November 2026 v2.0 policies describing the real API and consent flow |
| `/crm/` | Token-gated, `noindex` Lead Desk: `New · Qualified · Proposal · Won · Lost` |
| `/books/` · `/login/` · `/register/` · `/account/` · `/cart/` · `/checkout/` · `/thank-you/` | Legacy screens kept out of the main journey, noindex, with visible "unavailable" notices and no fake auth/payment/entitlement |

Every route above has a real Arabic twin under `/ar/…` (and `/ar/erp/`), generated from the same source at build time — not a JavaScript translation shell.

## Quick start

```sh
npm ci                 # Node >= 20; devDependencies are QA/build tooling only
npm run dev            # static site + /api/* + /crm/ on 0.0.0.0:3000
```

Open <http://localhost:3000/>, `/ar/`, `/book/`, `/work/` and `/crm/`. Set `CC_ADMIN_TOKEN` before exposing the service anywhere; the built-in `cc-local-admin` is review-only. The Lead Desk token field takes that value. Lead data is written to `.data/` (gitignored — it contains personal data).

`PORT=4000 npm run dev` changes the port; `node dev-server.mjs dist` serves the built `dist/` tree instead.

## Architecture

```
index.html · erp/index.html · partials/{head,top,bottom}.html
assets/
├── css/ds.css · home.css · pages.css · erp.css · live.css   (live.css = additive RTL-safe growth layer)
├── js/config.js · site.js · home.js · pages.js · booking.js · erp-app.js · shop.js · reader.js
├── fonts/             self-hosted OFL fonts (Space Grotesk, Alexandria, IBM Plex Sans Arabic, Comfortaa)
├── media/*.webp       10 generated illustrations, always captioned as illustrative
└── brand/og/*.png     35 per-route 1200×630 social cards
scripts/
├── gen-pages.py       writes every inner page + _redirects / sitemap.xml / robots.txt / manus-routes.json / vercel.json
├── sync-chrome.mjs    injects shared head/nav/footer between <!-- cc:head/top/bottom --> markers
├── gen-ar.mjs         builds /ar/ twins (scripts/lib/arize.mjs swaps data-ar* attributes)
├── check-links.mjs · check-generated.mjs · check-claims.mjs · optimize-media.mjs   static QA gates
├── smoke-api.mjs · verify-live.mjs                                                runtime + live-domain QA
└── lib/               catalog.py, data_growth.py, h.py, pages_*.py, posts/*.py
server/api.mjs         zero-dependency first-party API (leads, bookings, events, ICS, CRM)
server/crm.html        noindex Lead Desk UI
dev-server.mjs         combined static + API + CRM server for local preview
build.sh               copies the deployable static tree to dist/ (incl. dist/.htaccess, dist/crm/)
tests/                 566 Playwright tests (matrix, Arabic, flows, a11y, layout, visual)
```

**Generated output is committed and never hand-edited.** Edit `scripts/lib/pages_*.py` / `scripts/lib/posts/*.py` / `scripts/lib/data_growth.py`, then `npm run generate`. `npm run check` verifies chrome parity, internal links/anchors, generator↔output parity, claim/consent/OG/route gates and media assets. The generator refuses to emit a redirect source with two different destinations.

## First-party pipeline (what replaced the old manual hand-off)

`assets/js/config.js` points at same-origin `/api/*` endpoints by default. `server/api.mjs` validates consent, honeypot, origin, payload size and rate limits; deduplicates submissions; stores leads durably; scores and stages them; publishes booking slots; blocks double-booking; emits `.ics`; records consent-gated measurement events; and exposes token-protected reads, stage PATCH, CSV export and a notification log/webhook. See [`docs/INTEGRATIONS.md`](docs/INTEGRATIONS.md) and [`docs/LEAD-PIPELINE.md`](docs/LEAD-PIPELINE.md).

On **pure static hosting** (Hostinger `public_html`, Vercel static output) `server/api.mjs` cannot run. The site then fails closed: forms keep the user's input and show an explicit WhatsApp/email draft saying **nothing was sent**. A real production lead pipeline therefore requires `server/api.mjs` deployed as a same-origin Node service (or an equivalent serverless function) plus an encrypted managed database, a real `CC_ADMIN_TOKEN`, mail delivery and backups.

## Verification / publish gate

```sh
npm run gate           # generate → check → 566 Playwright tests → build
npm run verify:api     # 23 first-party pipeline checks
npm run dev            # human preview approval
npm run verify:live    # AFTER an approved production release, against the real domain
```

`npm run gate` currently exits 0. A green GitHub Actions run is **not** proof of deployment: `.github/workflows/deploy-hostinger.yml` runs `gate → deploy (environment: production) → verify-live`, and the production environment requires a human reviewer configured by the repository owner. See [`docs/PUBLISH-GATE.md`](docs/PUBLISH-GATE.md).

Chromium is installed normally in CI. In restricted sandboxes `playwright.config.mjs` also accepts `PW_EXECUTABLE_PATH` / `PW_LD_LIBRARY_PATH` for an npm-hosted Chromium.

## Language

`?lang=ar` / `?lang=en` forces a language, remembered in `localStorage` (`cc-lang`). English lives in the HTML; Arabic sits in `data-ar` on the same element (`data-ar-html` for markup, `data-ar-label` / `data-ar-title` for attributes). `scripts/lib/arize.mjs` produces standalone Arabic HTML files under `/ar/` and rewrites root links except `/assets/` and `/api/`. Use CSS logical properties (`margin-inline-start`, `inset-inline-end`) so one rule serves both directions.

## Fonts and artwork

All faces are self-hosted and served from `/assets/fonts/`; no Google Fonts request is made. Signate Grotesk was replaced by **Space Grotesk** (SIL OFL, licence committed at `assets/fonts/space-grotesk-OFL.txt`) on 2026-11-08 because web-embedding permission was never confirmed; the two Signate files were deleted. Provenance: [`assets/fonts/SOURCES.md`](assets/fonts/SOURCES.md). Ten abstract 16:9 illustrations were generated, converted to 1600px WebP (q82) and used with visible "illustrative — not client work / screenshot / photo" captions. Real licensed founder photography and permissioned client screenshots remain owner gates.

## Deployment

- **Hostinger (current live host):** `npm run build` → upload `dist/` to `public_html`. `build.sh` generates `dist/.htaccess` from `_redirects` (47 rules), ships `dist/crm/index.html` (static shell only) and copies every route folder. The API must be deployed separately as described above.
- **Vercel:** `vercel.json` is generated by `scripts/gen-pages.py` from the same redirect table (build `sh build.sh`, output `dist`). It is a static-only deployment unless a serverless API is added.
- **Custom domain:** the live domain is `https://codeandcanvas.net`; do not switch DNS until `npm run verify:live` passes after deployment.

As of 2026-11-08 the live domain still serves the **pre-overhaul build**: `/book/` redirects to `/contact/#book`, `/work/` is a 404 body, `/blog/` still marks two articles "Coming soon" and `/contact/` has no consent field. Full details: [`docs/PRODUCTION-VERIFICATION.md`](docs/PRODUCTION-VERIFICATION.md).

## Remaining owner / legal gates (not code work)

1. Human preview approval, then merge to `main`.
2. Configure `environment: production` required reviewers.
3. Deploy the Node API same-origin with an encrypted managed database, real `CC_ADMIN_TOKEN` and an approved mail provider.
4. Qualified legal sign-off on jurisdiction-specific policy wording.
5. Licensed founder/team photos, verified Google Business Profiles, street addresses and permissioned local references.
6. Permissioned real client screenshots/outcomes before upgrading any concept study to a client case.
7. `npm run verify:live` on the live domain after deployment.

## Historical documents

`docs/OVERHAUL-PLAN.md`, `docs/OVERHAUL-REPORT.md`, `docs/NEXT-CHAT-HANDOFF.md`, `docs/SITEMAP.md`, `docs/audit/*` and `docs/completion-2026-10-14/*` describe the 2026-10 baseline and the audit that motivated this work. They are kept as evidence, not as current operating instructions.
