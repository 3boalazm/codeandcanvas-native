# Implementation checklist — Code & Canvas native site

## 1. Standalone private native-code project — complete
- [x] Independent private GitHub repository, separate from `3boalazm/aboalazm-os`.
- [x] Preserve the existing production website and domain; do not publish, replace, redirect, or change DNS during this task.
- [x] Native website code, not WordPress.

## 2. Homepage — complete
- [x] Long-form responsive homepage with the content currently visible at `https://codeandcanvas.net/` (services, prices, timelines, metrics, contact details).
- [x] Do not invent testimonials, clients, claims or metrics.
- [x] Keyboard navigation, visible focus, reduced-motion support, phone and desktop layouts.

## 3. CanvasOne ERP style merged into the site — complete
- [x] One shared design system (`assets/css/ds.css`) used by `/` and `/erp/`: fonts, glass panels, gradient buttons, preloader, ambient background, nav, timeline, orbit, footer.
- [x] Homepage rebuilt in the CanvasOne ERP visual language (hero with glass board, stats bar, marquee, tilt cards, gradient accents).
- [x] ERP proposal moved to `/erp/`, sharing nav, brand, footer and language preference with the homepage.
- [x] CanvasOne ERP teaser section on the homepage + nav and footer links.
- [x] ERP contact details switched to the real ones from the live site (info@, KSA WhatsApp, booking page).

## 4. Bilingual site — complete
- [x] English / Arabic with RTL on both pages, persisted choice, `?lang=` override, per-language title and description.
- [x] Arabic translation of all homepage copy (review wording with a native copywriter before launch).

## 5. Open items
- [ ] Self-host the fonts (`woff2`) instead of Google Fonts if "no third-party requests" is required.
- [ ] Verify ERP compliance claims and module features against the licensed product (`// VERIFY` in `assets/js/erp-data.js`).
- [ ] Decide whether the homepage should default to Arabic for Saudi / Egypt visitors regardless of browser language.
- [ ] Add `hreflang` / separate Arabic URLs if SEO for Arabic is needed (currently `?lang=ar`).
- [ ] Rebuild the remaining pages (services, our story, contact) — links still point to the live site.
