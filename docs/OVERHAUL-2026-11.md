# Audit overhaul — staged closure (branch `arena/f3440ff7-codeandcanvas-native`, 2026-11-08)

User request: implement every audit item, generate section-appropriate design so the site feels alive, keep the native static architecture, work in staged phases, do **not** merge or deploy before tests and approval.

## P0 — closed in code, awaiting approved deployment

| Item | Implementation | Verification |
| --- | --- | --- |
| Live domain response for `/`, `/ar/`, `/services/`, `/case-studies/`, `/contact/`, `/blog/` | Direct fetches; all six answer with real HTML (old build) | `docs/PRODUCTION-VERIFICATION.md`, `scripts/verify-live.mjs` |
| Real Lead Management Pipeline | `server/api.mjs` (validation, honeypot, rate limit, idempotency, consent, durable leads, scoring, stages, notifications, admin token, CSV), `server/crm.html` (`New · Qualified · Proposal · Won · Lost`), `dev-server.mjs` combined server | `npm run verify:api` → 23 checks pass; `docs/LEAD-PIPELINE.md` |
| Real Booking | `/book/` + `assets/js/booking.js`: 5 specialties, published slots, timezone, consent, server confirmation, CRM lead, `.ics` calendar sync, request details attached. Failure = explicit manual hand-off, never a fake confirmation | `npm run verify:api`, `tests/flows.spec.mjs`, `tests/visual.spec.mjs` |
| Real visual Portfolio | `/work/` hub + 4 concept studies (Brand Identity, Packaging & Print, Digital Products, Web Experiences) with problem / strategy / studio role / execution / deliverables / evidence gate. Explicitly labelled "not client work"; published client cases stay at `/case-studies/` | `scripts/lib/pages_portfolio.py`, `data_growth.py`, `/claims/` |
| Claim cleanup | `10+ years / 40+ brands / 12+ sectors / 4–7× / $50K–$200K / active credentials` removed or qualified everywhere; `9+ years` removed from homepage, about, creative, story, author bio. Public `/claims/` register with 9 rows and statuses | `scripts/check-claims.mjs` gate + `docs/ASSET-AND-CLAIM-REGISTER.md` |
| Legal policies | `/privacy-policy/`, `/terms-of-use/`, `/cookie-policy/` rewritten to describe the actual first-party API, data store, retention, consent, nine events, DNT/GPC, no accounts/payments. "Draft — pending legal review" removed; owner legal sign-off remains an explicit gate | `scripts/check-claims.mjs` rejects the draft badge |

## P1 — closed in code

- **Positioning:** `Code & Canvas — Strategy. Design. Technology.` with four pillars `01 Brand Systems · 02 Digital Products & Platforms · 03 Technology & Automation · 04 Specialist Solutions`, all 23 services intact, flagship services linked from `/services/` to their standalone pages.
- **Homepage:** `Positioning · Hero · Selected Work · Main Offers · Process · CTA` — value-first hero, generated artwork with a visible disclaimer, one primary CTA (`/book/`), secondary Work CTA, verifiable trust strip (`/claims/`), four-pillar section, local-market and content-funnel cross-links.
- **Visual Portfolio:** `/work/` with filters + 4 labelled case pages, evidence table and intake steps.
- **7 standalone landing pages:** `brand-identity-design`, `brand-strategy-systems`, `packaging-design`, `website-design-development`, `product-design-ux`, `healthcare-digital-solutions`, `ai-workflow-automation` — original copy, scope, deliverables, steps, FAQ, `Service` + `FAQPage` JSON-LD, scoped inquiry/booking CTAs.
- **Team / Story imagery:** labelled illustrative studio artwork on `/about/`, `/our-story/`, `/team/`; real licensed founder photography documented as an owner gate rather than invented.
- **Commerce/account flows:** hidden from header/footer, `/resources/` explains the honest status, legacy screens carry a visible notice, all are noindex and out of the main journey.
- **Content funnel:** all 10 articles (including the two previously "Coming soon": `from-brand-identity-to-brand-systems`, `creative-strategy-in-the-age-of-generative-ai`) are full bilingual articles with a shared `article → service → case study → CTA → lead` section. Both have real Arabic URLs and per-route OG cards.
- **Measurement plan:** nine canonical events, consent-gated `/api/events`, DNT/GPC, PII exclusions, GA4/GTM/Clarity IDs empty by default with double opt-in. `docs/MEASUREMENT-PLAN.md`, `tests/flows.spec.mjs`.
- **Local SEO:** `/saudi-arabia/` + `/egypt/` (and Arabic twins), unified NAP, `ProfessionalService` schema, no invented street address / map pin / GBP / reviews. `docs/LOCAL-SEO.md`.

## P2 — closed in code, owner gates remain

- **Publish gate:** `npm run gate` = generate → `npm run check` (chrome parity, links, generator parity, claims/consent/OG/routes, WebP/OG assets) → `npm test` (Playwright matrix, Arabic, flows, accessibility, layout, screenshot regression) → `npm run build`. `npm run verify:api` in CI. `.github/workflows/pr-gate.yml` and a rewritten `deploy-hostinger.yml` with `gate → deploy (environment: production) → verify-live`. `docs/PUBLISH-GATE.md`.
- **Arabic coverage:** `/ar/` and `/ar/erp/` added to `manus-routes.json`, Arabic matrix, accessibility matrix, screenshot regression and all new routes.
- **Per-page OG:** 35 generated 1200×630 cards (`scripts/optimize-media.mjs`), per-route `data-og`, `{{OG_IMAGE}}` substitution, `primaryImageOfPage` JSON-LD. `home.png` visually reviewed.
- **Font licence:** Signate Grotesk replaced by self-hosted Space Grotesk (SIL OFL, licence committed); the two Signate font files were deleted; a claim gate blocks re-introduction.
- **Stale patch:** reviewed `01a13976-…-d60ae74be3b3.patch` (1.9 MB, an already-applied historical full-repo diff) and deleted it.
- **Restructure:** Homepage + Work + Services + Studio + Contact rebuilt as one system.

## Visual system added (section-appropriate, never fake client work)

10 abstract 16:9 illustrations → 10 WebP (1600px, q82) + 35 OG cards. Used on: homepage hero/selected work, `/work/` hub and 4 cases, 7 service landings, `/resources/`, both local pages, article covers, `/about/`, `/our-story/`, `/team/`. Every visible use carries an "illustrative — not client work/screenshot/photo" caption. `assets/css/live.css` is an additive RTL-safe layer (value hero, pillars, work grid, evidence table, funnel, booking slots, local NAP, responsive + reduced-motion rules).

## Verification run on this branch

```
npm run gate            ✅ EXIT 0 (full publish gate, 2026-11-08)
  ├ generate           ✅ 60 chrome-marked pages · 61 Arabic pages · 129 outputs
  ├ check              ✅ 126 HTML files, 0 link/tag problems · parity 129 outputs
  │                      ✅ check-claims 123 pages · media 10 WebP + 35 OG cards
  ├ test               ✅ 566 Playwright tests passed (9.6m) · no failures
  └ build              ✅ Static site built in dist/ · dist/crm/index.html present
npm run verify:api      ✅ 23/23 first-party pipeline checks
node --check           ✅ server/api.mjs, assets/js/booking.js, dev-server.mjs
preview /crm/          ✅ noindex · 5 stage columns · token auth gate verified in Chromium
```

A review preview runs on port 3000 with `CC_ADMIN_TOKEN=cc-review-token`; the Lead Desk
token field accepts that value. Runtime lead records live in `.data/`, which is now
gitignored so personal data can never be committed.

> Chromium was unavailable in the sandbox (`cdn.playwright.dev` blocked), so browser QA used an npm-hosted Chromium binary via `PW_EXECUTABLE_PATH` / `PW_LD_LIBRARY_PATH`. CI installs Chromium normally with `npx playwright install --with-deps chromium`.

## Still open — owner / production gates (do NOT deploy yet)

1. Human preview approval and merge to `main` (not done; this branch is the review artifact).
2. `environment: production` protection rule configured by the repository owner.
3. Node API deployed same-origin + encrypted managed database + real `CC_ADMIN_TOKEN` + notification provider.
4. Qualified legal sign-off on jurisdiction-specific policy wording.
5. Licensed founder/team photos, verified Google Business Profiles, street addresses and permissioned local references.
6. Permissioned real client screenshots/outcomes before any concept study is upgraded to a client case.
7. `npm run verify:live` against the live domain **after** deployment; currently the live domain serves the old build (see `docs/PRODUCTION-VERIFICATION.md`).
