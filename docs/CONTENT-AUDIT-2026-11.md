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
