# Implementation checklist — Code & Canvas native site

> **Status: 2026-11-08.** The 2026-11 audit overhaul is implemented and verified on `arena/f3440ff7-codeandcanvas-native`. Full closure by phase: [`docs/OVERHAUL-2026-11.md`](docs/OVERHAUL-2026-11.md). Open items below are **owner / legal / production** gates, not remaining code work. Nothing has been merged or deployed.

## 1. Standalone native project — complete
- [x] Independent repository, no WordPress, no runtime framework.
- [x] Preserve the existing production site, domain and DNS; no deployment during this task.
- [x] Semantic HTML + one CSS design system + vanilla JS; Node service only for the first-party API.

## 2. Homepage — complete
- [x] Value-first hero, selected work, four positioning pillars, trust strip, markets/content funnel.
- [x] One primary `/book/` CTA, secondary `/work/` CTA, no unevidenced `9+ years` claim.
- [x] Keyboard navigation, visible focus, reduced-motion, 320 → 1920 px layouts (Playwright matrix).
- [x] Generated illustrative artwork with visible "not client work" captions.

## 3. CanvasOne ERP / shared design system — complete
- [x] `/erp/` and `/ar/erp/` share nav, brand, footer and language preference with `/`.
- [x] ERP timeline a11y fixed (decorative rail is an `aria-hidden` sibling, `<ol>` contains only `<li>`).
- [x] Compliance claims and go-live durations remain subject to product-owner approval in `assets/js/erp-data.js`.

## 4. Bilingual — complete
- [x] EN/AR, RTL, persisted `?lang=`, per-language title/description.
- [x] **Real Arabic URLs** under `/ar/…` for every route including `/ar/book/`, `/ar/work/`, `/ar/erp/`, the 7 service landings, the 2 new articles and the local/claims/resources pages.
- [x] Arabic axe, matrix and screenshot-regression coverage.

## 5. Content and claims — complete
- [x] All 10 articles published (the two "coming soon" placeholders are gone), bilingual with per-route OG cards.
- [x] `/work/` + 4 labelled concept studies; published client cases stay at `/case-studies/`.
- [x] `/claims/` evidence register; unevidenced numeric/credential claims removed or qualified; `check-claims.mjs` gate.
- [x] Legal policies rewritten (Nov 2026 v2.0) to the real first-party data flow; draft badge removed.
- [x] `/saudi-arabia/` + `/egypt/` with honest city-level NAP; `/resources/` explains the commerce/account status.
- [x] 35 per-route OG cards, 10 WebP illustrations, Space Grotesk (OFL) replacing unlicensed Signate.

## 6. First-party pipeline — complete in code
- [x] `/api/contact`, `/api/newsletter`, `/api/career`, `/api/booking`, `/api/booking/slots`, `/api/events`, ICS, admin reads/PATCH/CSV.
- [x] Consent, honeypot, origin check, size cap, rate limits, idempotency, lead scoring/stages/history, notifications, `.ics`.
- [x] `/crm/` noindex Lead Desk with `New · Qualified · Proposal · Won · Lost`.
- [x] `/book/` real scheduler with published slots, timezone normalization, server confirmation, manual fallback.
- [x] Nine canonical measurement events, DNT/GPC/consent gating, no PII, no third-party script loaded by default.
- [x] 23 API smoke checks + 566 Playwright tests + generator/claim/link/media gates.

## 7. Open owner / production gates
- [ ] Human preview approval, then merge to `main`.
- [ ] Configure `environment: production` required reviewers (repository owner).
- [ ] Deploy `server/api.mjs` same-origin as a Node service; replace `.data/` with an encrypted managed database; set a real `CC_ADMIN_TOKEN` and an approved mail provider.
- [ ] Qualified legal sign-off on jurisdiction-specific policy wording and newsletter double opt-in.
- [ ] Licensed founder/team photography to replace the labelled illustrative artwork.
- [ ] Verified Google Business Profiles, street addresses and permissioned local references before strengthening `/saudi-arabia/` / `/egypt/`.
- [ ] Permissioned real client screenshots/outcomes before any concept study becomes a client case.
- [ ] Real company social URLs and confirmation of the Egypt landline (`0444` vs `0454`).
- [ ] `npm run verify:live` on `https://codeandcanvas.net` **after** deployment (currently the live domain serves the older build; see [`docs/PRODUCTION-VERIFICATION.md`](docs/PRODUCTION-VERIFICATION.md)).
- [ ] Product-owner verification of ERP compliance claims, module features and go-live durations.

## 8. Deliberately not implemented
- Accounts, sign-in, reset, orders, payments, receipts or paid book content. The legacy screens are noindex UI shells with visible "unavailable" notices; there is no fake auth, entitlement or success state.
- Third-party analytics/trackers by default. Provider IDs are empty and require explicit consent plus legal approval.
- Any change to the live domain, DNS, Hostinger or the WordPress install.
