# Code & Canvas — native site

> **Next chat / استكمال المشروع:** اقرأ [`docs/NEXT-CHAT-HANDOFF.md`](docs/NEXT-CHAT-HANDOFF.md) أولًا. إصلاحات الجولة السابقة اندمجت عبر [PR #3](https://github.com/3boalazm/codeandcanvas-native/pull/3)، لكن التفوير الشامل وقبول الإنتاج لم يكتملَا. [إيصال الدمج وحدود النشر](docs/completion-2026-10-14/MERGE-RECEIPT.md).

Standalone, bilingual (English / Arabic, LTR / RTL) Code & Canvas site built with semantic HTML, CSS and vanilla JavaScript. It is native website code, not a WordPress theme, and has no runtime framework or package dependencies.

| Route | What it is |
| --- | --- |
| `/` | Homepage (editorial sections and purposeful cards): compact hero → selected work → studio → service tracks → approach, resources and contact paths |
| `/erp/` | CanvasOne ERP interactive proposal (modules, industries, compliance, timeline, package builder, FAQ, print-to-PDF) |
| `/services/` · `/technology-services/` · `/creative-services/` · `/healthcare/` | Solutions hub + the three tracks (23 services: AB-01…06, MA-01…10, HC-01…05, CC-01/02) |
| `/about/` · `/our-story/` · `/methodology/` · `/team/` | Studio, story, methodology, founders |
| `/pricing-faq/` · `/contact/` (`#book`) | Packages, payment terms, FAQ · contact form, channels, booking card |
| `/case-studies/` | Work: Pharmacy OS, Zad, Nile Pharma ERP |
| `/blog/` · `/blog/<slug>/` | Insights Hub + 8 articles (2 hub cards are "coming soon" — they never had an article on the live site) |
| `/books/` · `/books/<slug>/` · `/books/<slug>/read/` | Digital library, 4 book landings, public-preview readers; no online purchase or paid access |
| `/login/` `/register/` `/forgot-password/` `/reset-password/` `/account/` | Explicitly unavailable auth UI + local saved-book previews |
| `/cart/` `/checkout/` `/thank-you/` | Single-copy local shortlist + availability inquiry; no checkout success/receipt simulation |
| `/privacy-policy/` `/terms-of-use/` `/cookie-policy/` · `/404.html` | Legal drafts (the live site had none — pending legal review) · not-found page |

The header is a floating pill (`partials/top.html`): round brand mark + wordmark, uppercase links, language + WhatsApp round buttons, Contact CTA; the burger takes over below 1024px.

All inner pages are **generated** — edit `scripts/lib/pages_*.py` (and `scripts/lib/posts/*.py` for articles), never the HTML:

```sh
python3 scripts/gen-pages.py && node scripts/sync-chrome.mjs && node scripts/check-links.mjs
```

`gen-pages.py` also rewrites `_redirects`, `sitemap.xml`, `robots.txt` and `manus-routes.json` from the page registry. `sync-chrome.mjs` injects the shared `<head>` / nav / footer from `partials/` between the `<!-- cc:head/top/bottom -->` markers of every page (`--check` to verify in CI). `check-links.mjs` validates tag balance, internal links (honouring `_redirects`) and anchors.

The routes share one design system — dark navy canvas, violet / teal / pink gradients, glass panels, preloader, scroll progress, cursor glow, tilt and magnetic buttons — taken from the CanvasOne ERP proposal.

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
├── css/ds.css           shared design system (tokens, glass, buttons, nav, footer, timeline…)
├── css/home.css         homepage-only components
├── css/erp.css          ERP-only components (+ print stylesheet)
├── js/site.js           shared runtime: language, icons, preloader, reveal, tilt, nav, progress, CC.track() analytics hook…
├── js/home.js           homepage behaviour (meta per language; sections are plain CSS/HTML)
├── js/pages.js          inner pages: tabs, FAQ, filters, forms (contact / demo), booking hook, TOC, account panels
├── js/shop.js           trusted-ID shortlist, availability inquiry, saved previews
├── js/reader.js         interactive book reader (manifest or free preview, notes, fullscreen)
├── css/pages.css        inner-page components (hero, tiles, tiers, forms, prose, reader, cart, auth…)
├── js/erp-data.js       ALL ERP copy, bilingual { ar, en }
├── js/erp-app.js        ERP rendering and interactions
└── brand/               Code & Canvas logos (SVG) + og-default.png (1200×630 social card)
scripts/
├── gen-pages.py         builds every inner page + _redirects / sitemap.xml / robots.txt / manus-routes.json
├── sync-chrome.mjs      injects partials/{head,top,bottom}.html into all pages (--check in CI)
├── check-links.mjs      static QA: tag balance, internal links, anchors
├── audit-text.py        dumps the visible English text of every page to docs/audit/native/ (content QA)
├── make-og.mjs          renders assets/brand/og-default.png (needs @resvg/resvg-js, see file header)
└── lib/                 catalog.py (23 services), h.py (HTML helpers + JSON-LD), pages_*.py (one per page), posts/ (articles), _reorder.py (dev helper: reorder page blocks)
partials/                shared head / nav / footer chrome
docs/
├── SITEMAP.md           map of the live codeandcanvas.net (every URL, page blueprints, redirects, build phases)
├── sitemap.json         the same route list, machine-readable
├── OVERHAUL-PLAN.md     work plan of the 2026-10 overhaul (phases, research method)
├── OVERHAUL-REPORT.md   what the overhaul changed and why (final report)
└── audit/               GAP-REPORT.md (live → native content gaps), REVIEW.md (cross-team site review), native/*.txt (text dumps)
```

## Language

- `?lang=ar` / `?lang=en` forces a language. The choice is remembered (`localStorage`, key `cc-lang`) and shared by `/` and `/erp/`. With no choice, Arabic browsers get Arabic and everything else gets English.
- **Homepage:** write English in the HTML and put the Arabic in `data-ar="…"` on the same element (`data-ar-html` when the text contains markup, `data-ar-label` / `data-ar-title` for attributes). Page title and meta description per language live in `home.js`.
- **ERP:** edit `assets/js/erp-data.js`; every text field is `{ ar: '…', en: '…' }`.
- Use CSS logical properties (`margin-inline-start`, `inset-inline-end`…) so one rule serves both directions. Wrap prices and numeric ranges in Arabic strings with LRI/PDI isolates (`⁦…⁩`) so they keep their visual order.

## Fonts

English roles remain Signate Grotesk (headings), Raleway (titles/buttons) and Poppins (body). Existing TTF files now have lossless WOFF2 web versions, used by `ds.css`. Alexandria, IBM Plex Sans Arabic and Comfortaa are self-hosted WOFF2 with adjacent OFL licenses; no Google Fonts request is needed. Provenance: [`assets/fonts/SOURCES.md`](assets/fonts/SOURCES.md). **Signate web-embedding permission still needs owner approval.**

## Deploy to Vercel

The repo is Vercel-ready — `vercel.json` is generated by `scripts/gen-pages.py` (build command, output dir, 301 redirects for every legacy WordPress URL, cache + security headers), so it always matches `_redirects`.

**One-time setup (dashboard):** Vercel → *Add New → Project* → import `3boalazm/codeandcanvas-native` → Framework Preset **Other** → leave Build Command / Output Directory as detected from `vercel.json` (`sh build.sh` → `dist`) → *Deploy*. Every push to the production branch redeploys; other branches get preview URLs.

**Or from the terminal:**

```sh
npm i -g vercel
vercel login
vercel          # first run links the folder to a project and creates a preview
vercel --prod   # production deploy
```

**Custom domain:** Project → *Settings → Domains* → add `codeandcanvas.net` + `www.codeandcanvas.net` (redirect www → apex). At the registrar point `A @ → 76.76.21.21` and `CNAME www → cname.vercel-dns.com`. Keep the WordPress host alive until the Vercel deployment is verified, then switch DNS — the legacy URLs keep working through the redirects. HTTPS is automatic.

What the config does: `trailingSlash: true` (`/services` → `/services/`), `cleanUrls: true`, `404.html` served for unknown paths, `/assets/fonts/*` cached for a year, CSS/JS for an hour with stale-while-revalidate, HTML always revalidated, plus `X-Content-Type-Options` / `X-Frame-Options` / `Referrer-Policy` / `Permissions-Policy` headers. Static preview needs no environment variables. Optional real integrations require a separately implemented backend and approved public configuration in `assets/js/config.js`; never put secrets there. See *Integration points*.

## Integration points (no backend is bundled)

The authoritative contract is [`docs/INTEGRATIONS.md`](docs/INTEGRATIONS.md). The previous localStorage purchase/auth simulation has been removed.

| Feature | Current behavior |
| --- | --- |
| Contact / newsletter / careers | Manual WhatsApp/email drafts by default, explicitly **not sent**. Optional same-origin `/api/` endpoint succeeds only on 2xx JSON `{accepted:true}`. Timeout/error keeps inputs. |
| Booking | Manual link by default; approved HTTPS scheduler can be set in public config, preserving service context. Click ≠ confirmed booking. |
| Accounts / payments | Unavailable; no fake sign-in, reset, order, receipt or entitlement. Google login disabled. Real commerce needs a server-led release. |
| Books | Single-copy saved IDs in `cc-cart`, catalogue-generated display data, local preview list/count, public reader content. `cc-library` is not ownership. |
| Measurement | Bounded local diagnostics; configured first-party collector sends only after consent, respecting DNT/GPC. Footer permits withdrawal. No personal form values or URL queries in events. |
| Artwork / evidence | Three labeled scope diagrams, not screenshots. Real client proof/portraits/permissions remain gates in [`docs/ASSET-AND-CLAIM-REGISTER.md`](docs/ASSET-AND-CLAIM-REGISTER.md). |
| Hosting | Generated `_redirects` and `vercel.json`. Local slash redirects preserve query strings. Production cutover remains unperformed. |

## Regression and source consistency

```sh
npm ci
npx playwright install chromium
npm run generate         # Python 3 + shared chrome sync
npm run check            # links/anchors/tag balance + isolated generator parity
npm test                 # Chromium flows, bilingual route matrix, geometry and axe
npm run build
```

`npm run test:flows`, `npm run test:matrix`, and `npm run test:a11y` run subsets. `PW_EXECUTABLE_PATH`, optional JSON `PW_BROWSER_ARGS`, and `TEST_BASE_URL` support an existing browser/local server. Tests abort external traffic and mock API responses: no message or payment is sent. They do not certify a live provider, physical devices, screen readers, Safari/Firefox or production Lighthouse/CrUX.

`check-links.mjs` is lightweight static validation, not a full HTML validator, CSS audit, icon audit or browser accessibility test. `check-generated.mjs` regenerates 48 outputs in a temporary directory and compares bytes without overwriting the workspace. The sitemap no longer claims a fresh last-modified date simply because the generator ran. Update generators first, then regenerate—never fix generated inner HTML alone.

Latest implementation report: [`docs/completion-2026-10-14/REPORT.md`](docs/completion-2026-10-14/REPORT.md). Historical audit: [`docs/audit/verification-2026-10-14/REPORT.md`](docs/audit/verification-2026-10-14/REPORT.md). These are deliberately separate; audit screenshots/results do not validate later code.

## Scope

This repository contains an independently developed site for review. It does not modify the existing production website, its domain, DNS, or any production deployment. Pricing, service details, contact methods and destination links were taken from <https://codeandcanvas.net/>. Every public route of the live site now has a native twin (see `docs/SITEMAP.md` §6 for the URL map and `_redirects` for the legacy URLs). `manus-routes.json` lists all routes and redirects.

## Before publishing the ERP page

`assets/js/erp-data.js`: confirm that the compliance claims (KSA: ZATCA phase 2, VAT 15%, GOSI / WPS-Mudad, Hijri calendar; Egypt: ETA e-invoice / e-receipt, VAT 14%, social insurance), module features and go-live durations match the licensed product. The proposal deliberately contains no client counts, logos, testimonials or prices. The homepage teaser avoids the compliance claims on purpose.
