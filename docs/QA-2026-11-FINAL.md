# Final trust, booking & production QA — 2026-11-09

Scope: the post-audit quality pass requested after PR #22. **No redesign, no new
services, no new claims, no deploy.** Everything below is either verified on this
branch with a named command, or marked **NOT VERIFIED** with the reason.

| Phase | State |
| --- | --- |
| 1 · Credential presentation removed | ✅ done, gate-enforced |
| 2 · Booking end to end | ✅ done (server + payload), UI specs written |
| 3 · Production integrity | ✅ verifier rebuilt, run locally 175/175; live domain **NOT VERIFIED** from this sandbox |
| 4 · Responsive / interaction | ⚠️ specs written; **NOT VERIFIED** — no browser binary here, CI runs them |
| 5 · Regression gates A–F | ✅ done, each proven by injecting a violation |
| 6 · `npm run check` + `npm run build` | ✅ green |
| 7 · Focused PR | ✅ opened, **not merged**, nothing deployed |

---

## 1 · Credential presentation

The audit found certification badges used as personal proof. They are gone, not
relabelled. Public pages no longer contain `CPHIMS` at all:

```sh
grep -rl CPHIMS --include=*.html . | grep -v dist      # → no output
```

| Where | Before | Now |
| --- | --- | --- |
| `/technology-services/` §03 | “CREDENTIALS”: CPHIMS *certified*, EMRAM *assessor*, TOGAF/NORA icon cards | “FRAMEWORKS IN CONTEXT” — six statements: what the method is, where it decides a decision, which service codes it applies to, plus an explicit *no personal certifications, no organisational accreditation* line |
| Founder cards (`/`, `/team/`, `/our-story/`, `/creative-services/`) | chip shelves (`.duo__creds`, `.who__creds`, `.creds`) | areas of specialisation and the service codes each founder leads |
| Founder bio | CPHIMS/EMRAM certification sentence | modelling and assessment work described as work (ArchiMate modelling, TOGAF ADM sequencing, EMRAM readiness scoring) |
| Catalogue tags / durations | `CPHIMS · …` | `EMRAM · CBAHI`, `HC · SCORED SELECTION`, `… · EMRAM-informed` — in **both** languages |
| `/healthcare/` hero + description | “CPHIMS and EMRAM readiness criteria” | “EMRAM and CBAHI readiness criteria” |
| `art-clinical-lanes.png` | framework names baked into the plate as floating labels | the processing steps they stood for: ASSESS / SCORE / GAP / ROADMAP |
| `/work/` claims register | acronym list as the item | “Framework names presented as personal certifications — Removed”. The historical entry is kept: the register exists to record what was withdrawn. |

Framework names are still allowed where they explain a decision (e.g. “CBAHI
scoping decides the evidence list”). The gate distinguishes the two cases rather
than banning the words.

## 2 · Booking — what was actually broken

Screens looked right; the scheduler was wrong underneath.

| Defect | Evidence | Fix |
| --- | --- | --- |
| Timezone selector was cosmetic | slots returned wall-clock strings only; the ICS offset was re-derived at download | slots computed from UTC, returned per requested zone, stored with `utc`, used for `DTSTART` |
| The same instant could be sold twice | `taken` keyed on `date + wall clock`, not the instant | booking identity is the UTC instant |
| Re-submitting created a second booking | no idempotency on `POST /api/booking` | same email + same instant inside 10 min → `200 {duplicate:true}` with the original id |
| One visitor could hold the day | no burst guard | third distinct booking from one email in 10 min → `429` |
| Published hours contradicted the grid | pages said 09:00–18:00, last slot 16:30 | pages, contact hours, location structured data and scheduler all say 09:00–17:00, Sun–Thu |
| Weak addresses stored as leads | `/^[^\s@]+\.[^\s@]{2,}$/`-class regex | rejects double `@`, missing TLD, trailing dot, one-letter TLD |

Verification (`npm run verify:api`, in-process, isolated temp store):

```
✓ POST /api/booking → accepted + calendar URL + normalized zone
✓ calendar invite starts at the booked UTC instant — 20261111T060000 vs 20261111T060000
✓ same wall clock ≠ same instant across zones — 2026-11-11T06:00 vs 2026-11-11T07:00
✓ offset difference is exactly one hour · AST=UTC+3, EET=UTC+2
✓ booking rejects a malformed email / unsupported timezone / off-schedule date
✓ re-submitting the same booking is idempotent, not duplicated
✓ double-booking the same slot rejected — status 409
✓ a burst of bookings from one address is refused
✓ GET /api/leads → the booking created a qualified lead linked by bookingId
smoke-api: all 33 checks passed
```

Timezone note: neither Saudi Arabia nor Egypt observes DST (Egypt suspended it
in 2025), so `AST=UTC+3` / `EET=UTC+2` are fixed offsets. The code stores the UTC
instant, so a future DST rule would change the label, not the stored time.

## 3 · Production integrity

The old verifier checked 17 hand-written routes. It could not have caught a stale
canonical, a broken hreflang pair, or an asset hash that no longer exists.
`scripts/verify-live.mjs` now:

- crawls **every** page in `dist/` (175 routes) plus the booking API;
- asserts the canonical is self-referential and `en`/`ar`/`x-default` alternates
  exist and point at the twin **in the other language**;
- rejects HTML that references a hashed asset the fresh build does not have —
  the signature of stale HTML served from a cache;
- rejects unresolved build placeholders and HTML served with a long `max-age`;
- follows every static redirect in `vercel.json` to a destination that exists;
- probes `/api/health`, because the published site is static and `/book/` silently
  degrades to “request a manual call”. A dead API is a warning by default and a
  failure when `CC_REQUIRE_API=1` (use that once the Node service is mounted).

Local run against the dev server:

```
175/175 routes answered · 1207 hashed asset reference(s) in the build
All 175 live routes answered correctly.
```

**NOT VERIFIED — production domain.** This sandbox has no outbound network to
`codeandcanvas.net` (`fetch failed`), so the release cannot be signed off from
here. The state of the pipeline, read from GitHub, is:

- `main` = `30d8ea3` (PR #22 merged); run `42746531399` (Deploy to Hostinger):
  **Gate ✓ · Deploy ✓ · Verify the LIVE domain ✓**;
- `hostinger` branch head message: `Deploy 30d8ea3` — i.e. production serves the
  pre-pass build, which is correct: **this pass is not deployed**.

Run after approval: `npm run verify:live` (the deploy workflow already does it as
a post-deploy job and fails the release if any route answers wrong).

**Vercel — NOT APPLICABLE / NOT VERIFIED.** `vercel.json` is maintained in the
repo (build, `cleanUrls`, `trailingSlash`, cache headers, 47 redirect rules), but
the live host is Hostinger via the `hostinger` branch. The connected Vercel
account has no project or domain for this site (`list_projects` and
`list_domains` both return empty), so there is no deployment, alias or domain to
verify there. No Vercel or DNS setting was changed.

## 4 · Responsive and interaction

There is no Chromium in this sandbox and the Playwright download is blocked
(`npx playwright install chromium` → `Download failure, code=1`), so browser
tests are written but **NOT VERIFIED here**. CI runs them (`npm test`, the gate
installs Playwright with deps).

`tests/responsive.spec.mjs` (new, 14 tests): every page changed in this pass at
**320px**, in both languages — no horizontal scroll, no clipped text node, plus
booking slot targets ≥36×60px and a slot click filling the hidden time field.
It exists because the new two-column rows (`fw`, `person__scope`, `who__list`)
are exactly the shape that used to clip at 320.

`tests/booking.spec.mjs` (new, 7 tests): both languages through the full
journey against a stubbed API (never a production appointment), timezone change
re-reading the schedule, scheduler outage falling back to a manual request,
slot taken between load and submit, every booking CTA sitewide (and none pointing
at Calendly/Cal.com/WhatsApp), plus an in-process contract test that the
confirmation, stored booking, CRM lead and `.ics` are the same booking.

## 5 · Regression gates

Added to `scripts/check-claims.mjs` (runs in `npm run check`, so in CI):

| Gate | Rule | Proven |
| --- | --- | --- |
| A | `CPHIMS` anywhere in public HTML; framework + certified/accredited/assessor; `certified in <framework>`; credential chip shelves | injected `CPHIMS certified` → **caught** |
| A | chip shelf class reintroduced | injected `class="who__creds"` → **caught** |
| B | booking CTA to `/contact/#book`; third-party scheduler; “30-minute call” page that never links `/book/` | injected Calendly link → **caught** |
| C | existing: owner-gate wording, credential FAQ, unlicensed font, unresolved placeholder, missing OG asset | unchanged, still green |
| D | EN/AR twins: same section/`h2`/`article` counts, `lang`, self-referential Arabic canonical | removed a section from `/ar/team/` → **caught** |
| E | generated parity (`check-generated.mjs`), asset versioning, art, phase3/4 guards | green |
| F | 320px overflow sweep | `tests/responsive.spec.mjs` (CI) |

Every injected violation was reverted; the tree is clean afterwards.

## 6 · Green gates at the time of writing

```
sync-chrome        77 pages carry chrome markers · 0 out of date
version-assets     21 hashed assets · 0 pages out of date
check-links        161 HTML files · 0 problems
check-generated    Generator parity: 161 outputs match isolated regeneration
check-claims       ok — 157 HTML pages
optimize-media     44 sources, 88 WebP, 50 OG cards
phase3 / phase4    0 no-go · 0 problems
check-art          20 plates · 27 placements · 0 hotlinked
asset-versioning   1219 hashed refs current · sw cc-app-2026-11-10-1
verify:api         33/33
build              dist/ + 47 redirect rules
```

## 7 · Release decision

Nothing is merged and nothing is deployed. Before the owner approves:

1. Let CI run `npm test` (browser suite, including the two new specs).
2. After the approved deploy, read the `Verify the LIVE domain` job: it must print
   `All … live routes answered correctly`.
3. Then, and only then, re-run `npm run verify:live` against production and paste
   the output into this file.

Open item carried over from earlier rounds: founder photographs for `/team/` and
`/about/` must be supplied and licensed by the owner — no synthetic portraits.
