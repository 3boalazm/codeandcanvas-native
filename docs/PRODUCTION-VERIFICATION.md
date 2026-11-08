# Production verification — 2026-11-08 (UTC)

The audit explicitly rejected "GitHub Actions succeeded / `hostinger` branch is green" as proof. This record is a **direct request to the live domain** `https://codeandcanvas.net`, not a build log.

## Core route response (P0 requirement)

| Route | Result | What was actually served |
| --- | --- | --- |
| `/` | ✅ real HTML 200 | Old homepage: "Business Development, By Design", `.flow` hero, three SVG scope diagrams, `9+ years` / `7+ years` claims |
| `/ar/` | ✅ real HTML 200 | Old Arabic homepage, RTL, translated shell |
| `/services/` | ✅ real HTML 200 | Old 23-service index, four legacy tracks, `#ab-01`… anchors |
| `/case-studies/` | ✅ real HTML 200 | Three documented product cases with evidence caveats |
| `/contact/` | ✅ real HTML 200 | Old contact form, **no consent checkbox**, WhatsApp/e-mail draft hand-off |
| `/blog/` | ✅ real HTML 200 | 8 published articles + **two "Coming soon" cards** |
| `/book/` | ⚠️ 301 → `/contact/#book` | Old `_redirects` rule; no booking page exists in production |
| `/work/` | ⚠️ 404 page (`Lost in the void`) | New visual portfolio is not deployed |

**Conclusion:** the live domain does answer on all six audited routes, so hosting/DNS/SSL are functional. But the deployed content is the **pre-overhaul build**. This is expected: none of the work on `arena/f3440ff7-codeandcanvas-native` has been merged or deployed, per the instruction not to deploy before approval and tests.

Consequently:

- A green GitHub Actions run is **not** evidence that the new portfolio, booking, CRM, legal pages, claims register, local pages or licensed font are live.
- `/work/`, `/book/`, `/resources/`, `/claims/`, `/saudi-arabia/`, `/egypt/`, the seven service landings and the two new articles will remain 404/redirected on the live domain until an approved deployment.
- The live `/contact/` form currently does **not** collect consent and does **not** create a lead record. The new form exists only in this branch's generated HTML and in the preview.
- The live homepage still displays `9+ years` / `7+ years` claims that this branch removed. `/claims/` documents their status as `Removed`.

## After an approved production release

Run the real check, not a build check:

```sh
npm run verify:live
# or CC_BASE_URL=https://your-preview-host npm run verify:live
```

`scripts/verify-live.mjs` requests 15 public routes, rejects 404 bodies, unresolved `{{OG_IMAGE}}` placeholders, missing consent controls and missing article slugs, and exits non-zero if any route fails. The deploy workflow runs it as a **post-deploy job** (`.github/workflows/deploy-hostinger.yml → verify-live`). A failure there means rollback or hotfix — never "ship anyway".

## Static-host limitation (must be resolved before CRM is live)

Hostinger `public_html` is static. The generated HTML is deployable there as-is, but `server/api.mjs` cannot run on pure static hosting. On such a host the site correctly falls back to a manual WhatsApp/email hand-off and says the request was not sent. For a real lead pipeline in production, deploy `server/api.mjs` as a same-origin Node service (or an equivalent serverless function) and replace the file-backed `.data/` store with an encrypted managed database. See `docs/LEAD-PIPELINE.md`.

## `npm run verify:live` in this sandbox

`node scripts/verify-live.mjs` was executed here and exited **2**: all 15 routes reported `network error: fetch failed`. The sandbox permits outbound HTTP only to GitHub and package registries; Node's `fetch` cannot reach `https://codeandcanvas.net`. This is a **tooling/network limitation, not a site failure** — the direct content fetches above did reach the domain through the browser tool.

Therefore:

- The live-domain check **must run in CI after deployment** (`.github/workflows/deploy-hostinger.yml → verify-live`), where outbound HTTPS is available.
- A local `verify:live` exit 2 is correctly treated as "not verified", never as a pass.
- On the current live build the script would also fail its content markers: `/work/` returns a 404 body, `/book/` redirects to `/contact/#book`, `/contact/` has no `name="consent"` field and `/blog/` lacks the two new article slugs.
