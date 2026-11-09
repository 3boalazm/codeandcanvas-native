# Content audit — 2026-11-08

Scope: the whole generated static site, **123 HTML pages** (EN + `/ar/` twins), 14 source artworks / 28 WebP derivatives / 35 OG cards, generated chrome, claims, links, metadata, and responsive payload. This lap ran after the owner's **PR #14 (Vercel Web Analytics)** was synced into this branch as `a16d322`.

This is a diagnostic + remediation report, **not a production release approval**. No merge, deploy, or live-domain pass was performed for this branch. See `docs/PUBLISH-GATE.md` and the release blockers at the end.

## 1. Method

| Layer | Command / tool | What it checks |
| --- | --- | --- |
| Content inventory | `npm run audit:content` (`scripts/audit-content.mjs`, new, read-only, exit 0) | 123 pages: claims, dates, placeholders, thin/dynamic copy, duplicate titles/descriptions/bodies, image alt/dimensions/loading/AR alt, `srcset` existence, media/OG usage, metadata, heading structure, homepage payload |
| Generator integrity | `npm run check` | chrome sync, internal links, isolated-regeneration parity of 129 outputs, claims/consent/OG/routes, media variants |
| Full publish gate | `npm run gate` | generate + check + 566 Playwright assertions + static build |
| First-party API | `npm run verify:api` | 23 booking/CRM/event contract checks |
| Browser tour | 22 visits: 11 routes × 390×844 and 1440×900 | console/page errors, 404s, broken images, horizontal overflow, H1 count, decoded hero, real asset requests, screenshots |

The audit script deliberately **classifies** rather than hides. Its first pass produced **619 raw hits**; most were false positives from hidden `<template data-ar-swap>` blocks, decorative brand SVGs, quoted *removed* claims, guarantee-FAQ questions, sample invoice numbers, intentional "Coming soon" copy, and 14 OG cards that were genuinely unused. Each class was fixed in the site or explicitly exempted with a reason in the script comments.

## 2. Baseline → after

| Metric | Before this lap | After |
| --- | --- | --- |
| Raw audit hits | 619 | 78 (all advisory / intentional; **0 blockers**) |
| `<img>` missing `alt` | 242 | **0** |
| `<img>` missing `loading` | 246 | **0** |
| `<img>` missing dimensions | counted as a risk | **0** |
| EN images missing `data-ar-alt` | 122 | **0** |
| Unused OG cards | 14 | **0** (16 routes mapped) |
| Duplicate/weak metadata | 11 | **0** |
| Hard claim / placeholder / media / link failures | 7 claims, 5 placeholders, 14 media | **0** |
| Homepage HTML | 70,477 B | 71,801 B (+1.9%: hreflang, `srcset`, swipe hints) |
| Homepage `<img>` tags (across 123 pages) | 322 | 324 (+2 new figures) |
| Mobile homepage height @390px | 8,182 px (after PR #13) | **7,563 px EN / 7,425 px AR** |
| Original mobile height before PR #13 | 17,327 px | **−56% cumulative** |

Remaining 78 informational groups: `[dates] 18` (historical citations, "Est. 2024", Vision 2030 policy context), `[structure] 54` (advisory heading-level jumps where axe WCAG2 A/AA and 2.1 AA pass), `[roadmap] 5` (one book deliberately labelled "Coming soon"), `[dynamic] 1` (`/erp/` copy injected by JS, verified in the browser). No `[claims]`, `[placeholders]`, `[images]`, `[media]`, `[metadata]`, `[links]`, `[duplicates]`, `[arabic]`, or `[thin]` findings remain.

## 3. Homepage payload — the mobile load reduction

The homepage previously sent 1600px WebPs to a 390px phone. Now `scripts/lib/h.py::media_img()` emits `srcset` with 780w (`-sm.webp`) and 1600w candidates plus real `sizes`, and the phone preloads only the small hero.

| Static inventory (`npm run audit:content`) | Bytes |
| --- | --- |
| Full-size artwork referenced by homepage `srcset` (old behaviour) | **242,566 B** (237 KiB) |
| 780w artwork a 390px phone actually selects | **53,014 B** (52 KiB) |
| **Saving on homepage artwork** | **78%** |

Browser-tour confirmation at 390×844: the homepage requested **37,012 B of artwork** (the hero plus the work cards reached while scrolling); the desktop run requested 108,704 B. `hero-system-sm.webp` was the chosen `currentSrc` on both EN and `/ar/` at 390px; at 1440px the same `srcset` still selects the smaller candidate where the layout slot is small, and `studio-method.webp` is loaded **only above 720px** as a desktop background, so it costs the phone nothing. `eagerImages` rose 0 → 1 intentionally: the hero is now eager with `fetchpriority="high"` and is verified decoded by the gate; all other imagery stays lazy.

Note: `referencedAssetBytes` (534,864 B) is a **static sum of every referenced candidate**, not network transfer — it counts both `srcset` sizes and therefore grew slightly. It must not be read as "the phone downloads more". The measurement above is the one that matters.

**Where the remaining mobile bytes are.** The 390px browser tour requested ~804 KiB of assets on the homepage, of which **~505 KiB (61%) is 12 self-hosted `woff2` files** (Space Grotesk, four Raleway weights, three Poppins weights, Alexandria Latin, IBM Plex Arabic, Comfortaa) and only ~36 KiB is artwork. All of them are genuinely referenced by the current typography system in `assets/css/ds.css`, and `font-display: swap` plus the Space Grotesk preload are already in place. Consolidating to variable Raleway/Poppins faces or to two families would be the single biggest further win, but it changes the site's typography and therefore needs a design decision — it was **not** done unilaterally in this lap.

Content-height reduction on mobile came from a second `MOBILE LITE · pass 2` layer in `assets/css/home.css`: 2-column compact service tracks instead of four tall cards, compact books/markets chips, hidden long track/platform details and step detail rows, and a horizontal `m-rail` for the three "how we work" steps — while keeping the image-led hero, the violet CTA, EN/AR copy, disclaimers, evidence links, and tracking attributes intact. Nothing was removed from the desktop layout.

## 4. Changes made from the findings

**New generated imagery (4 sources, 8 WebPs).** `blog-product-strategy`, `blog-design-systems`, `blog-experience-design`, `studio-method`. All are labelled illustrative artwork with bilingual alt text; mapped to seven article covers via `COVERS_BY_SLUG`, to a labelled bilingual `<figure>` in `/methodology/`, and to a desktop-only homepage background. Registered in `docs/ASSET-AND-CLAIM-REGISTER.md`.

**Responsive media pipeline.** `scripts/optimize-media.mjs` now emits 1600px q82 + 780px q72 for all 14 sources (28 WebPs) and regenerates 35 OG cards; `--check` is part of `npm run check`.

**OG / metadata / SEO.** `h.py::OG_BY_PATH` routes 16 pages to their own OG card; `/erp/` uses `og/erp.png`; `/claims/` uses `og/claims.png`; EN/AR/x-default `hreflang` on `/` and `/erp/`; Arabic `<title>`/description generated for `ar/erp/`; distinct title/description for the noindex `/clinic-review/`.

**Claims discipline.** Preserved the claims/evidence register, "NOT CLIENT WORK" qualifiers, legal draft markers, the ERP compliance caveat, `/book/` as the primary first-party CTA, and the removed-claims table. The audit script excludes quoted removed claims and guarantee-FAQ *questions* from claim matching, but still flags guarantee language, superlatives, unverified years/brand/sector counts, and unquantified outcome percentages in real copy: **0 hits**.

**Architecture unchanged.** Native static HTML + generated EN/AR twins, no framework, no client-side routing. All HTML edits went through the source + `npm run generate`, so generator parity holds.

## 5. Known issues / owner decisions (not fixed by this branch)

1. **Vercel analytics script 404s off Vercel.** The 22 browser visits each logged one `404 /_vercel/insights/script.js` plus its console error, and nothing else. That path is injected by Vercel's platform; the local dev server and the Hostinger-hosted `https://codeandcanvas.net` cannot serve it. Analytics will therefore only work on Vercel-hosted previews. This also broke two `flows.spec.mjs` assertions that require zero 404 responses; the test now excludes `/_vercel/` exactly as PR #14 already taught `scripts/check-links.mjs` to do, while staying strict for every first-party asset. Owner decision: either serve analytics from the installed `@vercel/analytics` package via a bundled `inject()`, or accept a no-op/404 on non-Vercel hosts — the owner's PR #14 update was **not** removed or rewritten.
2. **The live domain is still stale.** After PR #13, Hostinger deploy run `42479352407` succeeded at Gate + Deploy but failed `Verify the LIVE domain`: `https://codeandcanvas.net/` and `/ar/` still serve the pre-overhaul content and `/work/` returns 404. This is a deployment-target/publishing issue, not a code failure here; `npm run verify:live` cannot pass until the built `dist/` is actually published.
3. **`/erp/` is 19,698 px tall on mobile** (JS-injected copy) and its compliance/deployment claims remain pending product-owner approval before public release, as labelled on the homepage.
4. **Typography is the next load-reduction decision.** ~505 KiB of self-hosted `woff2` on a 390px homepage, versus ~36 KiB of artwork. Replacing the eight static Raleway/Poppins files with two variable faces (or dropping to two families) would cut roughly 300 KiB, but needs visual sign-off.
5. **54 advisory heading jumps** (mostly `h1 → h3` on utility pages and `h2 → h4` inside article card grids). Axe WCAG2 A/AA + 2.1 AA passes on EN/AR; cosmetic cleanup is optional and would require generator-wide heading changes.
6. **Release blockers unchanged:** required reviewers for `environment: production`; same-origin Node API with encrypted managed DB, real `CC_ADMIN_TOKEN` and approved mail provider (pure static hosting cannot execute `/api/*`); legal sign-off; licensed photography; verified GBP/addresses/local references; permissioned client screenshots/outcomes; post-deploy `npm run verify:live` on the live domain.

## 6. Verification

All commands below were run after the final `npm run generate` on this branch (2026-11-08).

| Command | Result |
| --- | --- |
| `npm run gate` (= generate + check + test + build) | **EXIT 0** · `566 passed (9.0m)` / 0 failed · `Static site built in dist/` |
| `npm run check` (inside gate) | `60 page(s) carry chrome markers · 0 out of date`; `126 HTML files checked · 0 problem(s)`; `Generator parity: 129 outputs match isolated regeneration`; `check-claims: ok — 123 HTML pages, claims/consent/OG/routes verified`; `media check: 14 source(s), 28 WebP variant(s), 35 OG card(s)` |
| `npm run verify:api` | `smoke-api: all 23 checks passed` |
| `npm run audit:content` | 123 pages · 78 findings, all advisory/intentional · `324 <img> · 44 eager · 0 missing alt · 0 missing dimensions · 0 missing loading · 0 EN images missing data-ar-alt` · homepage `mobileImageBytes 53,014 / desktopImageBytes 242,566 / saving 78%` |
| Browser tour (11 routes × 390×844 + 1440×900) | 0 console/page errors other than the known Vercel analytics 404 · 0 broken images · 0 horizontal overflow · exactly one H1 per page · hero decodes · EN + AR visually verified, including the new article covers and the labelled methodology figure |
| `npm run verify:live` | **Not run as a pass** — the live domain still serves pre-overhaul content (see §5.2) |

The gate initially reported `564 passed / 2 failed`; both failures were the PR #14 `/_vercel/insights/script.js` 404 counted by the reader-flow "no 404 responses" assertion. The test now excludes that platform URL (§5.1) and the full gate was re-run green.

---

# 2026-11-09 addendum · case studies, header, theme and mobile responsiveness

Sections 1–6 above are the **2026-11-08 historical snapshot**; their page counts and byte figures describe that lap's build. This addendum records the following lap. Nothing above was rewritten.

## A. What changed

**15 bilingual project case studies.** `scripts/lib/pages_case_studies.py` generates 15 EN + 15 AR `/work/<slug>/` detail pages and a 15-card `/work/#project-cases` grid; overlapping founder-archive cards now open the matching detail page. `assets/css/case-study.css` is linked by the case and portfolio builders. Art provenance, evidence limits and the still-open publication gates: `docs/ASSET-AND-CLAIM-REGISTER.md` (2026-11-09) and `docs/FOUNDER-WORK-ARCHIVE.md` (2026-11-09).

**Header.** `partials/top.html` now renders a deep-navy glass capsule with a thin outline and five ringed circular controls (brand, language, theme, WhatsApp, burger) plus the warm amber CTA on desktop/tablet. The pre-1024px layout uses `justify-content: space-between` with a flexible action group, so in Arabic the logo sits at the far right and the burger at the far left (measured at 390px: brand `x=325`, burger `x=23`, pill `[16,10,358,60]`). Previously the fixed `.nav__links` left no spacer and all controls clustered right-of-centre (burger `x=166`).

**Real light/dark theme.** Dark remains the default; light is an explicit, persisted (`cc-theme`) opt-in. A pre-paint bootstrap in `partials/head.html` and the matching `scripts/lib/arize.mjs::LOCKED_SCRIPT` set `data-theme` and `theme-color` on EN and `/ar/` twins before first paint, so there is no flash. `assets/css/ds.css` introduces a `--hi` emphasis token and scoped `html[data-theme='light']` overrides derived from every plain white-alpha / near-black panel declaration across the seven stylesheets; dark artwork wells and the header capsule deliberately stay dark in both themes. `assets/js/site.js` owns the toggle, `aria-pressed`, localized label and sun/moon icon. The language button is now a tolerant id/class match in `arize.mjs`, so header decoration classes cannot silently break the `/ar/ → EN` link again.

**Mobile load + jank.** `startPreloader()` no longer waits for `document.fonts.ready`; it races a 350 ms font cap, uses a 420 ms minimum on phones / 850 ms on desktop, and has a 1.8 s hard ceiling instead of 1.7 s minimum + 4 s safety. A mobile/coarse-pointer budget in `ds.css` replaces four `blur(96px)` drifting blobs with a static radial gradient, disables the full-viewport SVG-turbulence grain and cursor glow, lowers the fixed header's `backdrop-filter` from `blur(22px) saturate(160%)` to `blur(10px)`, drops `will-change` on every button, and removes `filter: blur()` from reveal transitions. Desktop rendering is unchanged. Latin-only `@font-face` declarations in `ds.css` gained `unicode-range`, the `ع` glyph no longer pulls an IBM Plex Arabic webfont onto English pages, and `/ar/` twins no longer preload the EN-only Space Grotesk face.

## B. Measurements (same 390×844 / 4× CPU / 1.6 Mbps · 150 ms synthetic profile)

| Metric | Before | After | Note |
| --- | --- | --- | --- |
| Interactive (`body.is-ready`) | ≈ 5.4 s (derived, not directly sampled: `document.fonts.ready` resolved ≈ 5.3 s; the 1.7 s minimum had already elapsed) | **3.3 s** | `load` still 5.3 s because non-blocking fonts finish later; the scroll lock is gone ~2 s earlier |
| Startup long tasks | 5 tasks / 967 ms | **2 tasks / 619–810 ms** | varies by run |
| Resources / bytes | 26 / 827,319 B | **25 / 806,511 B** | uncompressed local dev server; Vercel brotli reduces the 264 KiB of CSS in production |
| Grain animation | `grain 1.2s steps(6) infinite` | **none** | mobile only |
| Frames in a 3.1 s idle + rapid-scroll window | 113 frames, **27 over 50 ms**, worst 83 ms, avg 48.7 ms (≈20 fps) | **322 frames, 0 over 50 ms**, worst 50 ms, avg 17.2 ms (≈58 fps) | A/B on the same build, re-enabling the old effects via injected CSS |

The byte saving is deliberately modest: **no font binary was modified**. Subsetting the Raleway/Poppins files was evaluated (a 425-character subset cuts one 51 KiB face to ~29 KiB) but **not done** — Raleway's OFL declares a Reserved Font Name, so a modified/subset build would require renaming and legal sign-off. Poppins has no RFN. This joins the typography decision below rather than silently changing licensed assets.

## C. Verification on this lap

| Command / check | Result |
| --- | --- |
| `npm run generate` | EXIT 0 · `75 page(s) carry chrome markers · 74 rewritten` · `Arabic pages: 76 written` |
| `npm run check` | EXIT 0 · `75 · 0 out of date` · `156 HTML files checked · 0 problem(s)` · `Generator parity: 159 outputs` · `check-claims: ok — 153 HTML pages` · `media check: 29 source(s), 58 WebP variant(s), 50 OG card(s)` |
| Custom case-study QA (browser script) | 15 case pages × 2 languages × 2 widths + `/work/` twins → **0 problems** (H1, overflow, AR leftovers/dir/lang, case CSS/OG, evidence/build structure, eager images, local 404s, 15 index cards, archive detail links) |
| Header/theme QA (browser script) | 390/1440 × EN/AR → **0 problems**: RTL order, no overflow at 390 and 1440, five rings, circular brand, sun/moon, theme flip + `aria-pressed` + `theme-color` + persistence + pre-paint restore on reload, burger open/Escape, reciprocal language navigation, 0 page errors |
| `npm run gate` (before PWA lap) | **EXIT 0** · `676 passed (17.5m)` / 0 failed · `47 redirect rules written to dist/.htaccess` · `Static site built in dist/`; includes 320→1920px geometry for EN/AR |
| `npm run verify:api` | EXIT 0 · `smoke-api: all 23 checks passed` |
| `npm run audit:content` | EXIT 0 · **110 findings, 0 blockers** (`[dates] 18`, `[provenance] 32`, `[roadmap] 5`, `[structure] 54`, `[dynamic] 1`, `[claims] 0`) · `444 <img> · 74 eager · 0 missing alt / dimensions / loading / AR alt`. The 32 provenance advisories are the case-study/archive year labels that each link to their source; the earlier `[claims] 1` was a negated sentence («without implying guaranteed outcomes») and was reworded in the source copy rather than by relaxing the checker. |
| Mobile jank A/B (same build, old effects re-enabled via injected CSS) | old effects re-enabled on the same build → 113 frames / 27 over 50 ms / avg 48.7 ms; new budget → 322 frames / 0 over 50 ms / avg 17.2 ms |
| Visual | Dark/light EN+AR mobile/desktop header crops and light-mode frames for `/`, `/ar/`, `/work/`, `/work/zad/`, `/ar/work/zad/` reviewed; illustrative badges and disclaimers remain visible |

## D. Owner decisions still open

1. **Typography is still the largest remaining mobile transfer.** ~460 KiB of `woff2` was requested in the 390px profile (the 2026-11-08 figure of ~505 KiB covered 12 files incl. Arabic faces). Replacing the eight static Raleway/Poppins faces with two variable families, or consolidating to two families, remains the single biggest win (~300 KiB), but needs visual sign-off. If subsetting is chosen instead, rename the Raleway subset per its OFL Reserved Font Name and add the missing Raleway/Poppins license texts to `assets/fonts/` first.
2. **Light theme is opt-in.** If the owner wants OS-preference auto-detection or light as the default, change both the head bootstrap and `LOCKED_SCRIPT` together; the current default keeps every existing dark screenshot valid.
3. Release blockers from §5.6 are unchanged: production reviewers, same-origin Node API with encrypted managed DB / real `CC_ADMIN_TOKEN` / approved mail provider, legal sign-off on the registration numbers, licensed photography, verified GBP/addresses/local references, permissioned client screenshots/outcomes, and post-deploy CI live verification.

## E. 2026-11-09 · Installable app shell (PWA)

The site is now installable on mobile: `manifest.webmanifest` (`display: standalone`), a deferred service worker, a self-contained bilingual `offline.html`, five locally rendered home-screen icons, iOS/Chrome meta chrome in `partials/head.html`, and a footer install button that appears only on a real `beforeinstallprompt`. Full policy, install steps, limits and verification: **`docs/PWA.md`**.

Performance is protected deliberately: registration happens **after `load`**, the precache is ~12 small files added with `Promise.allSettled`, HTML is network-first (so no stale content is ever served while online), and static assets are stale-while-revalidate. This makes repeat visits instant and visited pages available offline without adding a byte to the first-load critical path. `tests/pwa.spec.mjs` opts into `serviceWorkers: 'allow'` while the rest of the suite blocks workers for determinism, and `scripts/check-claims.mjs` now fails the publish gate if any EN/AR page loses the manifest or apple-icon link, or if a PWA asset/manifest field is missing.

No font binary was modified for this lap (see §D.1). No push notifications, background sync, native wrapper or app-store asset was added. The final gate after §E was **680 passed (17.6m)**, including 4 PWA tests with `verify:api` 23/23 and `audit:content` 0 blockers.

## F. 2026-11-09 · REF UI-reference study and adapted components

63 owner-supplied UI-reference screenshots in `main/REF` (`52aeeb8b`) were read one by one; the full per-file assessment is in **`docs/REF-UI-STUDY-2026-11.md`** and the rubric/identity baseline in `docs/REF-UI-STUDY.md`. Result: 28 `B` (adapt the idea), 20 `C` (defer), 15 `D` (reject), 0 `A` (adopt as-is). Six `B` themes were rebuilt with our own tokens: a three-circle Brand/Product/System section with a ghost wordmark and edge-glow CTA band, a footer ghost wordmark, a CSS-only snap rail for the 15 case cards on phones, an announcement-pill variant, light-theme contrast repairs, and `tests/ref-system.spec.mjs`.

No reference pixels, fonts, portraits, logos, CDN scripts or numeric claims were published. The new section states explicitly that no measured outcomes are claimed. The light-theme sweep that started with the new components became a site-wide WCAG pass: dark accent inks for light panels, a solid active-filter surface, and keyboard-focusable named scrollable-table regions. Eight acceptance tests were added (`tests/ref-system.spec.mjs`, `tests/light-contrast.spec.mjs`).

**Phase 1 final verification:** `npm run generate` + `npm run check` → 157 HTML / 0 problems / parity 159 / claims ok on 153 pages / media 29-58-50. **`npm run gate` → 688 passed, 0 failed (15.9 m)**, including the 8 new tests and `npm run build` (47 redirects, PWA headers). `npm run verify:api` → 23/23. `npm run audit:content` → 153 pages, 110 findings, **0 blockers**, `[claims] 0`, `[provenance] 32`, 444 `<img>` / 74 eager / 0 missing alt-dim-loading-AR-alt. Custom browser QA: 8 EN/AR × dark/light × 390/1440 → 0 problems; no-reduced-motion QA → 0 problems; light-theme axe matrix → 36 pages (18 EN + 18 AR) / 0 WCAG 2 A-AA / 2.1 AA violations. Visual review of EN dark/light 1440/390, AR light 390, the footer wordmark and the `/work/` snap rail in both themes passed.

## G. 2026-11-09 · Phase 2 `/system/` (identity-safe REF adaptations)

Phase 2 of `docs/REF-UI-STUDY-2026-11.md` §7 added `/system/` + `/ar/system/` as a bilingual documentation route. Only the *mechanisms* of REF 004/016 (token cards), 023/041 (bento), 026 (native slit accordion), 044 (static tilted art tiles) and 045 (label plates) were rebuilt: six `ds.css` token values, six real site components, six generator-derived counts (23 services / 4 tracks / 15 case studies / 25 founder archive entries / 2 founders / 2 local market pages), four `<details>` panels, eight tiles and two monogram plates. Every image is an existing labelled illustrative WebP; every number comes from `SERVICES`, `TRACKS`, `CASE_STUDIES`, `FOUNDER_WORK`, `AHMED` and `MUSTAFA` at generation time. No licensed photo, client screenshot, team portrait, dashboard dataset, percentage, growth chart, tooltip, follower count, verification badge, new font, new WebP, new OG card, CDN or library was introduced. REF 060 stays rejected. The `C` owner/legal/asset decisions are still pending; the page says so in both languages.

**Final verification after Phase 2:** `npm run generate` + `npm run check` → 159 HTML / 0 problems / parity 161 / claims ok on 155 pages / media 29-58-50. **`npm run gate` → 706 passed, 0 failed (12.2 m)**, including 6 new `/system/` tests, the 38-page light axe matrix and `npm run build` (48 redirect rules, 52 `RewriteRule` lines, PWA headers). `npm run verify:api` → 23/23. `npm run audit:content` → **155 pages / 110 findings / 0 blockers / `[claims] 0` / `[provenance] 32`**, 472 `<img>` / 74 eager / 0 missing alt-dim-loading-AR-alt. Custom browser QA → 0 problems on 8 home/work combinations and 12 `/system/` EN/AR × dark/light × 320/390/1440 combinations; no-reduced-motion QA → 10 route/theme combinations / 0 problems; light-theme axe matrix → **38 pages (19 EN + 19 AR) / 0 violations**; four extra `/system/` axe variants → 0 violations. Visual review of all six new sections in EN dark 1440, EN/AR light 390 and the AR orbit passed.
