# Mandatory Publish Gate

**Rule: no deployment happens unless every core gate passes.** A successful GitHub Actions build or a green `hostinger` branch push is not approval.

```
Pull Request
   │
   ├─ 1. npm ci + npx playwright install chromium
   ├─ 2. npm run generate            (generate ALL pages, incl. Arabic twins)
   ├─ 3. npm run check               ├─ sync–chrome --check (shared head/top/bottom parity)
   │                                 ├─ check-links (all href/src/action + anchors)
   │                                 ├─ check-generated (generator ↔ committed output parity)
   │                                 ├─ check-claims (claims, consent, OG, required routes, legal)
   │                                 ├─ optimize-media --check (WebP + 50 OG cards present)
   │                                 ├─ check-phase3 (Phase 3 no-go guard: CDN/canvas/WebGL/blur/skins/AR leftovers)
   │                                 ├─ check-phase4 (Phase 4 residual-B section counts + no CDN/canvas in new markup)
   │                                 ├─ check-art (first-party plates: both WebP variants, labelled placement, no hotlinked images)
   │                                 ├─ version-assets --check (every CSS/JS ref carries a current ?v=<hash>)
   │                                 └─ check-asset-versioning (no stale/unversioned refs; /system/ band ↔ stylesheet agree)
   ├─ 4. npm test                    (Playwright: matrix, Arabic, flows, a11y, layout)
   ├─ 5. npm run verify:api          (first-party lead/booking/CRM smoke test)
   ├─ 6. npm run build               (dist/)
   ├─ 7. Preview approval            (human sign-off on the live preview)
   └─ 8. Production deployment       (only after 1–7 are green)
           │
           └─ 9. npm run verify:live  (REAL live domain, all core routes)
```

Any failure in steps 2–6 stops the pipeline. Step 7 is a required GitHub Environment protection rule (`production`), configured by the repository owner — code cannot self-approve. Step 9 runs after deployment; a failure there must trigger a rollback or a hotfix, never a "ship anyway" decision.

## Local equivalent

```sh
npm ci
npx playwright install chromium
npm run gate          # generate → check → test → build
npm run verify:api
npm run dev           # human preview on 0.0.0.0
npm run verify:live   # after an approved production release
```

## CI implementation

- `.github/workflows/deploy-hostinger.yml` — `gate` job (steps 1–6), `deploy` job (`needs: gate`, `environment: production`, only on `main`), `verify-live` job (step 9).
- `.github/workflows/pr-gate.yml` — runs the same `gate` job on every pull request into `main`; no deployment.

## Preview approval checklist

- [ ] Homepage hero, selected work and four pillars render at 1440 / 768 / 390.
- [ ] `/ar/` and `/ar/book/` are real RTL pages, not a translated shell.
- [ ] `/crm/` is noindex and token-gated; no lead data is public.
- [ ] Booking shows a confirmation only after a real 200 from `/api/booking`.
- [ ] Commerce/account screens are out of the main journey and say they are unavailable.
- [ ] Every illustrative image has a visible "not client work" caption.
- [ ] No `Draft — pending legal review` badge remains on legal pages.
- [ ] `npm run verify:live` reports all core routes answering on the **live domain**.

## Runtime secrets and data (must not ship in Git)

- `.data/` holds the file-backed leads, bookings, subscribers and event log. It is gitignored because it contains personal data. In production replace it with an encrypted managed store (see `docs/LEAD-PIPELINE.md`).
- `CC_ADMIN_TOKEN` must be set in the production environment. The `cc-local-admin` default is review-only; `dev-server.mjs` prints a warning when it is unset.
- `CC_NOTIFY_WEBHOOK`, if used, is an environment secret, never a committed value.

## Sandbox note

`cdn.playwright.dev` is unreachable in some sandboxes, so browser QA here used an npm-hosted Chromium via `PW_EXECUTABLE_PATH` / `PW_LD_LIBRARY_PATH` (`playwright.config.mjs` supports both). CI uses `npx playwright install --with-deps chromium` as normal. `scripts/optimize-media.mjs --check` deliberately lazy-loads `sharp` / `@resvg/resvg-js` so the static check gate also works on a minimal runner.

### 3 · Playwright + accessibility matrix

Failures inside this step are republished as GitHub **error annotations** by
`tests/github-annotations.mjs` (wired in `playwright.config.mjs`, only active
under `GITHUB_ACTIONS`). Each annotation names the spec file, line and test
title, and an `::notice` line summarises the failing count. This exists because
job logs are not always retrievable from outside CI; annotations are, through
`GET /repos/:owner/:repo/check-runs/:id/annotations`.

```sh
gh api repos/3boalazm/codeandcanvas-native/commits/<sha>/check-runs \
  --jq '.check_runs[] | select(.conclusion=="failure") | .id' \
| while read id; do gh api repos/3boalazm/codeandcanvas-native/check-runs/$id/annotations; done
```

## 2026-11 buyer-audit locks (added after the client-side review)

The following are now enforced by `scripts/check-claims.mjs` and
`scripts/check-asset-versioning.mjs`, and exercised by `tests/evidence.spec.mjs`:

| Rule | Why it exists |
| --- | --- |
| No `owner gate` / `بانتظار المالك` wording in public HTML | A buyer read internal delivery state as an unfinished studio. |
| No `Are your credentials active?` FAQ | The site answered "Active." while `/claims/` called the same items unverified. The question is removed until dated certificates exist. |
| No booking CTA pointing at `/contact/#book` | "Book a call" landed on a WhatsApp draft, not a schedule. Every booking CTA now resolves to `/book/`, which is a real slot picker. |
| `/evidence/` exists in EN + AR with 4 decision blocks and the tiers section | The trust path must not silently disappear. |
| `tests/helpers.mjs › configure()` matches on `url.pathname` | A `**/config.js` glob stops matching once the URL carries `?v=<hash>`, which silently disabled the stubbed config and hid the booking mismatch. |

`/evidence/` ("how we decide") is built from `scripts/lib/pages_evidence.py`: four
situations, each with the decision we would recommend, what we refuse to do, and
the published service codes that carry it — plus the evidence-status table
(published vs. stated limit) and four engagement tiers so a low entry price is
not read as the price of the studio.
