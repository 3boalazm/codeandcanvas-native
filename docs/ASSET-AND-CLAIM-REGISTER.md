# Asset and claim release register

Completion sprint, 2026-10-14. Suggested reviewers below are roles, not assignments or confirmations. No client results, testimonials, photography or product screenshots were fabricated.

## What was actually supplied

Three original SVG scope diagrams in `assets/brand/work/`: `pharmacy-os.svg`, `zad.svg`, `nile-pharma-erp.svg`. They summarize the feature scope already described in this repository. Homepage alt text and case-study captions explicitly identify them as **conceptual architecture illustrations, not product screenshots or business-outcome evidence**. They are not substitutes for a genuine portfolio or an independent evaluation of these products.

The machine inventory in `completion-2026-10-14/evidence/asset-slots.json` records **37 occurrences across 29 distinct slot names**. These are review locations, not 37 unique missing images. Some existing cover/decorative treatments may be intentional. Previous audit inventory remains unchanged as a historical baseline.

## Owner-controlled publication gates

| Material / claim | Current treatment | Required before stronger publication | Suggested reviewer |
| --- | --- | --- | --- |
| Pharmacy OS / Nile Pharma ERP UI | Labeled diagrams; existing scope copy retained | Approved desktop + mobile screenshots; client permission; redact people/health/financial data; confirm author role, deployment status, access/demo restrictions | Project owner + client |
| Zad UI and offline claims | Labeled diagram and existing external project link | Actual screenshots; verify public link; demonstrate offline behavior; confirm ownership and date | Project owner |
| Creative brand work | Existing authored art/slot treatments, no fabricated client board | 2–3 permission-cleared cases: brief, constraints, personal contribution, approved visual outputs, outcome and evidence source | Creative founder + client |
| Founder portraits | Existing abstract representations / slots | Licensed high-resolution originals and written publication permission; bilingual alt text | Both founders |
| Article/OG/book imagery | Existing covers and default social card | Decide which abstract covers are final; supply licensed images and per-page OG crops where useful; verify full book content and distribution rights | Editorial owner |
| Technical results: 12%, 25%, 40%, $500K+ | Removed from homepage numeric band; technology section explicitly attributes them to prior founder portfolio, not independent audit | Baseline, date range, denominator, methodology, contribution/attribution, source document and permission; otherwise remove before release | Technical founder + source owner |
| Experience, brand/sector counts and certifications | Existing claims retained without upgrading verification; 9+ creative experience not changed to 10+ | Confirm dated CV/certificates, whether studio vs individual experience, and non-overlapping count definitions. NORA/CBAHI are frameworks/context, not automatically personal certificates | Both founders |
| HIS risk range $50K–$200K; delivery/price ranges | Existing indicative copy, not new measured results | Support risk estimate or remove; approve currencies, taxes, scope, timing and conditions | Commercial + technical owner |
| Phone/social/profile destinations | Existing published destinations retained | Confirm ownership and routing, especially Egypt contact variants; approve one canonical contact sheet | Studio owner |
| Signate Grotesk (RESOLVED 2026-11-08) | Web-embedding rights were never confirmed | Replaced by self-hosted Space Grotesk (SIL OFL, license committed); the two Signate font files were deleted and `check-claims.mjs` blocks any re-introduction | Engineering |
| Arabic SEO | Client-side AR/EN, locally hosted Arabic fonts; no `/ar/` mirror promised | Approve Arabic URL/canonical strategy, editorial translations, internal links and hreflang; then generate and test static localized pages | Editorial + engineering |
| Legal/privacy/ERP compliance claims | Legal pages explicitly marked draft; ERP claims not independently revalidated | Legal review for actual provider/retention/commerce mode; validate licensed product's compliance and availability | Legal + product owner |

## Asset delivery checklist

1. Supply original source, rights holder, usage license and consent; avoid personal/health data.
2. Identify route/slot, purpose (evidence vs illustration), caption and EN/AR alt text.
3. Record what the image proves and what it does not prove. Do not replace a diagram with an AI-generated imitation of a client product.
4. Prefer optimized AVIF/WebP or appropriate SVG, with fixed dimensions and responsive sizes; keep unneeded large originals outside Git.
5. Test cropping, contrast, layout shift and readability at 320/390/768/1440px, plus physical devices.
6. Approve exact claims and link to their source before removing the “illustration”/qualification labels.

**Release rule:** an attractive image is not evidence. A publicly reachable demo is not proof of client impact. Do not close the asset, creative-proof, certification or production gates merely because the diagrams render and the browser tests pass.

---

## 2026-11-08 · Generated artwork added this lap

Four new pieces of **illustrative studio artwork** were generated for this repository. They are abstract, AI-generated compositions in the site's navy / violet / teal / pink glass-panel language. **None of them is a photograph, a client deliverable, a product screenshot, a testimonial, or evidence of an outcome.** Every visible placement keeps an EN/AR `alt` (via `data-ar-alt`) and an on-page qualifier such as `ILLUSTRATIVE · NOT CLIENT WORK`, `ILLUSTRATIVE STUDIO ARTWORK · NOT A PEOPLE OR CLIENT PHOTO`, or `STUDIO VISUAL STUDY`. They must not be captioned or re-used as proof of work.

| Source PNG (kept in Git) | Derived WebP | Visible placement | Purpose | What it does **not** prove |
| --- | --- | --- | --- | --- |
| `assets/media/blog-product-strategy.png` | `blog-product-strategy.webp` (1600w) + `blog-product-strategy-sm.webp` (780w) | Cover for four product-thinking / product-strategy articles and their AR twins, via `pages_blog.py::COVERS_BY_SLUG` | Editorial atmosphere for an article | No product, no client, no measured result |
| `assets/media/blog-design-systems.png` | `blog-design-systems.webp` + `-sm.webp` | Cover for the design-systems article + AR twin | Editorial atmosphere | No design system was shipped by this image |
| `assets/media/blog-experience-design.png` | `blog-experience-design.webp` + `-sm.webp` | Cover for two experience-design / digital-transformation articles + AR twins | Editorial atmosphere | No UX research or outcome |
| `assets/media/studio-method.png` | `studio-method.webp` + `-sm.webp` | Labelled bilingual figure in `/methodology/` (and `/ar/methodology/`) via `pages_methodology.py::studio_figure()`; desktop-only background for the homepage "How we work" band in `assets/css/home.css` | Explains the *shape* of the process, not a real engagement | No milestone, invoice, client, or deployment evidence |

All eight WebP derivatives are produced by `scripts/optimize-media.mjs`: 1600px q82 for desktop and 780px q72 for phone, with `srcset`/`sizes` emitted by `scripts/lib/h.py::media_img()`. The `<figure>` carries its own bilingual label and disclaimer. The smaller variants are deliberately not loaded on mobile for the desktop-only background, so the artwork adds **zero** phone bytes there.

### Other asset/SEO resolutions recorded this lap

- The 14 previously orphaned OG cards in `assets/brand/og/` are now routed to their matching pages by `scripts/lib/h.py::OG_BY_PATH` (16 routes); an explicit `og_image=` argument still wins. `/erp/` also uses `og/erp.png`, and `/claims/` uses `og/claims.png`.
- `/index.html` and `/erp/index.html` now carry EN / AR / x-default `hreflang`; `ar/erp/index.html` is generated with Arabic `<title>` and description from `data-title-ar` / `data-desc-ar`. `/clinic-review/index.html` (noindex) has its own title/description so it no longer duplicates `amro-alahawany-review`.
- These are **technical** resolutions. The editorial/legal approval rows above remain open: Arabic translations, licensed photography, permission-cleared client screenshots, and claim sources still require owner sign-off.

**Still true:** the generated art makes the site feel alive; it does not close any claim, creative-proof, certification, legal, or production gate.

---

## 2026-11-08 · Founder work archive (text index, no imagery added)

The owner's own portfolio (`https://aboalazm-os.vercel.app/work`, `/work/design`, `/work/development`) and public GitHub repositories were re-indexed into `/work/` as 25 bilingual text cards — 8 identity projects and 17 digital products. Full source/evidence mapping: `docs/FOUNDER-WORK-ARCHIVE.md`.

**No image was copied, hotlinked, or regenerated for these entries.** Each card carries the project's year, a one-line description, stack/discipline chips, and links back to the founder's case study, live deployment and public repository. Four entries also cross-link to our own `/` or `/case-studies/`.

| Material / claim | Current treatment | Required before stronger publication | Suggested reviewer |
| --- | --- | --- | --- |
| 25 founder projects | Text index explicitly labelled «Founder work, documented — not verified studio client claims» | Client permission, approved screenshots/photography, written attribution of role/team/date, and evidence source before any is reclassified as a studio client case | Project owner + client |
| Project imagery on his portfolio | Not republished here; reached only via outbound links | Written publication permission and licensed originals if we ever host them | Founder + rights holder |
| Numbers quoted from his case studies (64 screens, 21 views, 69 items, 5 languages, 23 routes, 15 modules) | Retained as attributed quotes with a link to the source case study; stale counts about our own build were removed | Dated source, denominator and methodology before any marketing reuse | Editorial + technical founder |
| Overlap with `/case-studies/` (Zad, Nile Pharma ERP) | Linked to the existing pages with their published evidence limits | Unchanged — see the rows above | Engineering |

The four labelled concept studies, the `/work/` honesty paragraph, the permission → evidence → attribution gate, and the claims/evidence register stay in place. **An archive of links is not a portfolio of proven outcomes.**

---

## 2026-11-08 · Legal registration numbers in the shared footer

The owner supplied two identifiers and asked for them in the footer. They are now rendered on every EN page and its generated `/ar/` twin from `partials/bottom.html` (styled by `.footer__reg` in `assets/css/ds.css`):

| Identifier | Value as published | Status | Required before legal sign-off | Suggested reviewer |
| --- | --- | --- | --- | --- |
| Commercial Register | `311891` EN / `٣١١٨٩١` AR | Owner-supplied, published verbatim | Match against the official commercial-register certificate: exact legal entity name, number, issue date and jurisdiction | Legal + studio owner |
| Tax Registration | `774235055` EN / `٧٧٤٢٣٥٠٥٥` AR | Owner-supplied, published verbatim | Match against the official tax card / VAT registration: exact entity, number and jurisdiction | Legal + studio owner |

The Arabic digits are a locale rendering of the **same** numbers, not different identifiers. These are identifiers, **not** a claim of certification, verification, tax filing status, or legal opinion, and they do **not** close the legal sign-off blocker in `docs/PUBLISH-GATE.md`. No certificate, tax card, or registry lookup was performed in this repository — the figures are published exactly as supplied by the owner and should be checked against the source documents before production.

---

## 2026-11-09 · Project case studies (illustrative art, no new outcome claims)

Fifteen bilingual `/work/<slug>/` detail pages and a 15-card `/work/#project-cases` index were added from `scripts/lib/data_case_studies.py` + `scripts/lib/pages_case_studies.py`. **These are documented co-founder work, not verified studio client engagements and not measured business outcomes.** Each page carries the problem/approach/role, the concrete build and stack, verification/source links, a source note, and an explicit evidence-limits paragraph; each index card carries an `ILLUSTRATIVE` badge and the founder-work / not-client-claim disclaimer.

| Material / claim | Current treatment | Required before stronger publication | Suggested reviewer |
| --- | --- | --- | --- |
| 15 detail-page figures | Labelled **illustrative studio artwork**; figure captions state it is not a product screenshot, real interface, client photo or proof of an outcome | Permission-cleared real screenshots, dated evidence and written role attribution | Project owner + client |
| 10 AI-generated sources (`case-maqloop`, `case-packbox`, `case-ummah`, `case-zad`, `case-axiom`, `case-nile-bed`, `case-craft-egypt`, `case-stt`, `case-pharmacy`, `case-farm`; 1672×941) | Abstract composition only: no text, logo, UI mock, photograph, person or client mark | Same as above; the images are not evidence of any build | Editorial owner |
| 5 locally generated composites (`case-sakanwave`, `case-oltre`, `case-continuum`, `case-npf`, `case-evolve`; 1600×900) | Built by `scripts/generate-case-art.mjs` from the site's own SVG geometry plus `sharp` / `@resvg`, composited over one of the ten abstract sources; **no third-party imagery was copied or hotlinked** | Same as above | Engineering + editorial |
| `case-evolve` | Represents **source access pending**, not a claimed live product. The three inaccessible repositories (`evolve-system`, `NPF`, `craft-egypt`) are recorded as such, not published as public code evidence | Confirm access / ownership before any live-product claim | Technical founder |
| Source links | Only links that were actually fetched are published; login-only screens and inaccessible GitHub repos are described in source notes rather than quoted as evidence | Recheck availability and permission at publication time | Technical founder |

`node scripts/optimize-media.mjs` now registers **29 PNG sources / 58 WebP variants / 50 OG cards** (up from 14/28/35). Fifteen `assets/media/case-*.png` sources, thirty `-sm`/1600w WebP derivatives and sixteen `assets/brand/og/case-*.png` cards were produced (15 per-route detail cards plus `case-studies.png` for the `/work/` index); `scripts/lib/case_study_cards.json` describes the fifteen OG descriptors. No founder-portfolio image, `/_next/image` response, client photo or screenshot was copied, hotlinked or regenerated.

**Still true:** an illustrated, attributed work archive is not a portfolio of proven outcomes. The permission → evidence → attribution gate in the rows above is unchanged.

---

## 2026-11-09 · PWA / home-screen icons (own brand mark only)

Five `assets/brand/app/*.png` files were added for the installable app (192/512 `any`, 192/512 `maskable`, 180 `apple-touch-icon`). They are **rendered locally by `scripts/generate-app-icons.mjs` from `assets/brand/icon-white.svg`** — the same committed brand squircle already used in the header — onto a navy radial-gradient field. No photography, client mark, third-party artwork, app-store asset or AI-generated image was used, and no new claim of any kind is attached to them. See `docs/PWA.md`.

`manifest.webmanifest`, `sw.js` and `offline.html` contain no client names, outcomes, numbers, testimonials or screenshots. The offline page is a bilingual connection notice pointing back to `/` and `/ar/`. The service worker explicitly excludes `/api/*`, `/crm/*`, `/_vercel/*` and all non-GET requests, so no lead, form or analytics payload is ever stored in a cache. The permission → evidence → attribution gate above is unchanged.
