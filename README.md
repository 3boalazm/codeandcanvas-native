# Code & Canvas — native site

Standalone, bilingual (English / Arabic, LTR / RTL) Code & Canvas site built with semantic HTML, CSS and vanilla JavaScript. It is native website code, not a WordPress theme, and has no runtime framework or package dependencies.

| Route | What it is |
| --- | --- |
| `/` | Homepage: hero, services catalogue, CanvasOne ERP teaser, why us, approach, contact |
| `/erp/` | CanvasOne ERP interactive proposal (modules, industries, compliance, timeline, package builder, FAQ, print-to-PDF) |
| `/services/` · `/technology-services/` · `/creative-services/` · `/healthcare/` | Solutions hub + the three tracks (23 services: AB-01…06, MA-01…10, HC-01…05, CC-01/02) |
| `/about/` · `/our-story/` · `/methodology/` · `/team/` | Studio, story, methodology, founders |
| `/pricing-faq/` · `/contact/` (`#book`) | Packages, payment terms, FAQ · contact form, channels, booking card |
| `/case-studies/` | Work: Pharmacy OS, Zad, Nile Pharma ERP |
| `/blog/` · `/blog/<slug>/` | Insights Hub + 8 articles (2 hub cards are "coming soon" — they never had an article on the live site) |
| `/books/` · `/books/<slug>/` · `/books/<slug>/read/` | Digital library, 4 book landings, interactive reader shell (free preview + purchase gate) |
| `/login/` `/register/` `/forgot-password/` `/reset-password/` `/account/` | Auth + Account Center UI shells (no backend yet) |
| `/cart/` `/checkout/` `/thank-you/` | localStorage cart + checkout shell (payment gateway not connected) |
| `/privacy-policy/` `/terms-of-use/` `/cookie-policy/` · `/404.html` | Legal drafts (the live site had none — pending legal review) · not-found page |

All inner pages are **generated** — edit `scripts/lib/pages_*.py` (and `scripts/lib/posts/*.py` for articles), never the HTML:

```sh
python3 scripts/gen-pages.py && node scripts/sync-chrome.mjs && node scripts/check-links.mjs
```

`gen-pages.py` also rewrites `_redirects`, `sitemap.xml`, `robots.txt` and `manus-routes.json` from the page registry. `sync-chrome.mjs` injects the shared `<head>` / nav / footer from `partials/` between the `<!-- cc:head/top/bottom -->` markers of every page (`--check` to verify in CI). `check-links.mjs` validates tag balance, internal links (honouring `_redirects`) and anchors.

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
├── js/pages.js          inner pages: tabs, FAQ, filters, forms (contact / demo), booking hook, TOC, account panels
├── js/shop.js           localStorage cart, checkout shell, account library
├── js/reader.js         interactive book reader (manifest or free preview, notes, fullscreen)
├── css/pages.css        inner-page components (hero, tiles, tiers, forms, prose, reader, cart, auth…)
├── js/erp-data.js       ALL ERP copy, bilingual { ar, en }
├── js/erp-app.js        ERP rendering and interactions
└── brand/               Code & Canvas logos (SVG)
scripts/
├── gen-pages.py         builds every inner page + _redirects / sitemap.xml / robots.txt / manus-routes.json
├── sync-chrome.mjs      injects partials/{head,top,bottom}.html into all pages (--check in CI)
├── check-links.mjs      static QA: tag balance, internal links, anchors
└── lib/                 catalog.py (23 services), h.py (HTML helpers), pages_*.py (one per page), posts/ (articles)
partials/                shared head / nav / footer chrome
docs/
├── SITEMAP.md           map of the live codeandcanvas.net (every URL, page blueprints, redirects, build phases)
└── sitemap.json         the same route list, machine-readable
```

## Language

- `?lang=ar` / `?lang=en` forces a language. The choice is remembered (`localStorage`, key `cc-lang`) and shared by `/` and `/erp/`. With no choice, Arabic browsers get Arabic and everything else gets English.
- **Homepage:** write English in the HTML and put the Arabic in `data-ar="…"` on the same element (`data-ar-html` when the text contains markup, `data-ar-label` / `data-ar-title` for attributes). Page title and meta description per language live in `home.js`.
- **ERP:** edit `assets/js/erp-data.js`; every text field is `{ ar: '…', en: '…' }`.
- Use CSS logical properties (`margin-inline-start`, `inset-inline-end`…) so one rule serves both directions. Wrap prices and numeric ranges in Arabic strings with LRI/PDI isolates (`⁦…⁩`) so they keep their visual order.

## Fonts

Typography roles (English): **Signate Grotesk** (Black) for headings, **Raleway** for titles (card titles, kickers, buttons, nav, italic accent words) and **Poppins** for subtitles and body copy. The files are self-hosted from `assets/fonts/` (TTF, declared in `assets/css/ds.css`). Arabic uses Alexandria (headings / titles) and IBM Plex Sans Arabic (body), and the wordmark uses Comfortaa — those three still load from Google Fonts in each page `<head>`. Check the Signate Grotesk licence covers web embedding before going public; converting the TTFs to WOFF2 would cut their size.

## Integration points (no backend is bundled)

| Hook | Where | What to do |
| --- | --- | --- |
| **Contact form** | `/contact/` → `form[data-form="contact"]` (`scripts/lib/pages_contact.py`) | Set `data-endpoint="https://…"` to POST the form as JSON (`{name,email,phone,company,inquiry,budget,message,lang,page}`); a 2xx response shows the success state. Empty endpoint = hand-off to WhatsApp (`data-whatsapp`) or `mailto:` (`data-mail`) with the message pre-filled. Honeypot field `_hp`. |
| **Booking** | `/contact/#book` → `section#book[data-booking-url]` | Put your Calendly / Cal.com / TidyCal URL in `data-booking-url`; every `[data-book]` button then opens it. Empty = WhatsApp + form fallback. Legacy `/about#book` links hop client-side. |
| **Newsletter** | `/blog/` subscribe form (`data-form="contact"`, `data-subject`) | Same contract as the contact form: set `data-endpoint` to your list provider's JSON endpoint (Mailchimp/Brevo/Buttondown…). |
| **Auth** | `/login/`, `/register/`, `/forgot-password/`, `/reset-password/`, `/account/` (`pages_shop.py`) | Forms are `data-form="demo"` (`data-next` = where to go after "success"). Replace with real `fetch()` calls in `assets/js/pages.js › submitDemo` or point the forms at your auth API. The Google button is a plain link to `/login/?provider=google` — wire your OAuth start URL there. The live site's 2FA step (6-digit / recovery code) is kept as a collapsible block. |
| **Cart & payment** | `assets/js/shop.js` | Cart = `localStorage["cc-cart"]`; purchases unlock books via `localStorage["cc-library"]` (demo). Implement `checkout(cart, data)` with Moyasar / Tap / Paymob / Stripe and persist entitlements server-side. `[data-add]` buttons carry `data-title/-price/-currency`. |
| **Book content** | `assets/js/reader.js` → `/assets/books/<slug>/manifest.json` | Publish `{ "parts":[{ "title", "slides":[{ "kicker","title","html" }] }], "free_parts": n }` (serve it behind your entitlement check). Without a manifest the reader shows the free preview generated from the landing page copy + the purchase gate. Reading position and notes are stored locally (`cc-reader-*`, `cc-notes-*`). |
| **Imagery** | every `.art[data-slot="…"]` | CSS/SVG art tiles stand in for the WordPress stock images; replace by slot name (`blog/<slug>/cover`, `work/pharmacy-os`, `books/<slug>/cover`, …). |
| **Hosting** | `_redirects`, `404.html`, `manus-routes.json` | Netlify / Cloudflare Pages read `_redirects` natively; for Vercel convert to `vercel.json` rewrites. The dev server honours `_redirects` too. |

## Scope

This repository contains an independently developed site for review. It does not modify the existing production website, its domain, DNS, or any production deployment. Pricing, service details, contact methods and destination links were taken from <https://codeandcanvas.net/>. Every public route of the live site now has a native twin (see `docs/SITEMAP.md` §6 for the URL map and `_redirects` for the legacy URLs). `manus-routes.json` lists all routes and redirects.

## Before publishing the ERP page

`assets/js/erp-data.js`: confirm that the compliance claims (KSA: ZATCA phase 2, VAT 15%, GOSI / WPS-Mudad, Hijri calendar; Egypt: ETA e-invoice / e-receipt, VAT 14%, social insurance), module features and go-live durations match the licensed product. The proposal deliberately contains no client counts, logos, testimonials or prices. The homepage teaser avoids the compliance claims on purpose.
