# Integration contracts and launch gates

**Updated 2026-11-08 for the 2026-11 overhaul.** This describes the code that is actually on this branch. The older "no backend bundled / all endpoints empty" contract is obsolete; see the historical note at the end. Authoritative companion documents: [`docs/LEAD-PIPELINE.md`](LEAD-PIPELINE.md), [`docs/MEASUREMENT-PLAN.md`](MEASUREMENT-PLAN.md), [`docs/PUBLISH-GATE.md`](PUBLISH-GATE.md).

## 0. What runs where

| Layer | Implementation | Deployed how |
| --- | --- | --- |
| Browser | `assets/js/config.js` → `site.js`, `pages.js`, `booking.js` | Static files from `dist/` |
| Public API | `server/api.mjs` (zero runtime dependencies, Node ≥ 20) | `dev-server.mjs` locally; **must** be a same-origin Node service / serverless function in production |
| Lead Desk | `server/crm.html` served at `/crm/` by the API | Token-gated, `noindex`; `build.sh` ships only the static shell at `dist/crm/index.html` |
| Store | `.data/leads.json`, `bookings.json`, `subscribers.json`, `events.jsonl`, `notifications.log` | File-backed, single node, **gitignored**. Replace with an encrypted managed database before launch |
| Measurement | Consent-gated first-party `/api/events`; GA4 / GTM / Clarity IDs are empty | No third-party script is injected without an approved ID **and** explicit consent |

`npm run dev` starts `dev-server.mjs`, which serves the static tree, forwards `/api/*` and `/crm/` to `createApi()`, honours `_redirects` and binds `0.0.0.0`. On pure static hosting the API is absent: every form then fails **closed** with an explicit "draft prepared, not sent yet" WhatsApp/email hand-off. Nothing is silently claimed as delivered.

## 1. Public configuration (`assets/js/config.js`)

```js
window.CC_CONFIG = Object.freeze({
  contactEndpoint: '/api/contact',
  newsletterEndpoint: '/api/newsletter',
  careerEndpoint: '/api/career',
  bookingEndpoint: '/api/booking',
  slotsEndpoint: '/api/booking/slots',
  analyticsEndpoint: '/api/events',
  bookingUrl: '',          // optional approved HTTPS scheduler; empty = first-party /book/
  bookingPath: '/book/',
  requestTimeoutMs: 12000,
  measurement: Object.freeze({ ga4MeasurementId: '', gtmContainerId: '', clarityProjectId: '' }),
});
```

Only same-origin paths beginning `/api/` are accepted. Never put tokens, secrets or trusted prices in this public file. A form's non-empty `data-endpoint` overrides its configured endpoint. Third-party measurement IDs stay empty until the legal policies are signed off; loading a provider requires **both** a configured ID and `cc-analytics-consent=granted`.

Runtime secrets come from the environment only: `CC_ADMIN_TOKEN` (Lead Desk + admin API), `CC_NOTIFY_WEBHOOK` (optional notification target), `CC_DATA_DIR` (optional store location), `CC_BUILD_COMMIT` (build fingerprint). The `cc-local-admin` default is review-only and `dev-server.mjs` warns when it is unset.

## 2. Form contract

`POST /api/contact`, `/api/newsletter`, `/api/career` with `Content-Type: application/json` and same-origin credentials. `pages.js` sends the form's named fields plus `page` (pathname), `lang` (`en`/`ar`) and `kind`. The contact form uses `first_name`, `last_name`, `email`, `organization`, `inquiry`, `message`, `consent`; newsletter/career use their rendered controls. The `_hp` honeypot is checked client-side and rejected server-side. There is **no payment/order payload**.

Server-side rules (`server/api.mjs`):

- 64 KB payload cap; JSON must parse; `originOk` refuses cross-origin requests.
- Valid email, explicit `consent` (`true` / `on` / `yes`) and a name are required. Contact messages must be ≥ 5 characters and may not contain more than three URLs.
- Rate limit: 12 POSTs per IP per 60 s (429), plus 90 events per IP per 60 s.
- Idempotency: the same `kind + email + message` within 10 minutes returns the original lead with `duplicate: true` (HTTP 200) instead of creating a second one.
- Leads get an id, score (organization +2, service code +2, long message +1, phone +1), stage (`qualified` at ≥ 4, else `new`), `notes[]`, `history[]`, a hashed IP and a `createdAt`. Newsletter submissions also create a `pending_confirmation` subscriber record — frontend "request received" is **not** a confirmed subscription.
- Success is `201 {"accepted":true,"id":"lead-…", ...}` (or `200` for duplicates). The browser only confirms on 2xx + `accepted === true`; anything else keeps the inputs, emits `form-error` and shows the manual fallback.

`docs/MEASUREMENT-PLAN.md` lists the nine canonical funnel events: `page_view`, `service_view`, `case_study_view`, `cta_click`, `form_start`, `form_submit`, `booking_confirmed`, `lead_qualified`, `lead_converted`. Legacy short names (`form-success`, `form-error`, `form-handoff`, `page-view`) still work for existing dashboards.

## 3. Booking

`GET /api/booking/slots` returns `{ accepted, dates, date, slots, timezone: 'AST' }`; `GET /api/booking/slots?date=YYYY-MM-DD` returns that day's 30-minute slots with `available` flags. Only published business dates are accepted.

`POST /api/booking` requires `name`, valid `email`, `consent`, a `specialty` (`brand`, `product`, `technology`, `healthcare`, `general`), a published `date` and an available `time`. `timezone` accepts the published labels `AST` (UTC+3), `EET` (UTC+2), `UTC` and the IANA aliases `Asia/Riyadh`, `Africa/Cairo`, `Etc/UTC`, `Etc/GMT`; unsupported zones are rejected with 422 rather than silently relabelled. `assets/js/booking.js` preselects `AST`/`EET` from `Intl.DateTimeFormat().resolvedOptions().timeZone`.

A confirmed booking returns `201 {"accepted":true,"id":"book-…","leadId":"lead-…","date","time","timezone","calendarUrl"}`; the same slot cannot be booked twice (409). `GET /api/booking/<id>/calendar.ics` serves a `VEVENT` with the correct UTC offset. Every confirmed booking also creates/links a qualified CRM lead and emits `booking_confirmed` + `lead_qualified`. Clicking a scheduler link or opening `/book/` is **never** by itself a confirmed booking.

## 4. Measurement

`CC.track(name, props)` writes a bounded `window.dataLayer` (max 100 entries), dispatches `cc:track`, and — only with consent + no DNT/GPC + a same-origin `/api/` endpoint — POSTs a **single event object** `{ event:'cc', name, lang, path, ...allowlisted props }` to `/api/events`. The collector accepts `202` for a valid `[a-z0-9_.-]+` name and `400` for anything else; it never receives form values, message bodies, emails, phone numbers or URL query strings. `EVENT_KEYS` allowlists `id, service, from, form, channel, filter, to`. DNT, GPC and consent withdrawal are honoured; the footer "Measurement settings" link lets a visitor change their choice.

## 5. Lead Desk / admin API

All admin routes require `Authorization: Bearer <CC_ADMIN_TOKEN>`, header `x-cc-token` or `?token=…`; missing/incorrect values return 401.

| Route | Method | Result |
| --- | --- | --- |
| `/api/health` | GET | `200 {ok:true, service, commit, store:'file'}` |
| `/crm/` | GET | noindex Lead Desk HTML |
| `/api/leads` | GET | `{accepted:true, leads:[…]}` |
| `/api/bookings` | GET | `{accepted:true, bookings:[…]}` |
| `/api/stats` | GET | counts + `byStage` |
| `/api/export.csv` | GET | CSV of id, createdAt, kind, name, email, organization, inquiry, stage, score |
| `/api/leads/<id>` | PATCH | `{stage, note}` → stage transition (case-insensitive) + history entry |

Stages are lower-case internally: `new · qualified · proposal · won · lost`; the Lead Desk labels them `New · Qualified · Proposal · Won · Lost`.

## 6. Static-host fallback

With no API available, `pages.js` prepares a WhatsApp/email draft, says **not sent yet**, and provides clickable fallback links. `booking.js` says "We could not confirm the booking" and offers the same manual channels; it never displays a fake confirmation. Tests intercept `window.open` and abort external traffic — no real messages are sent during QA.

## 7. Gates before production activation

- Deploy the API same-origin behind TLS; replace `.data/` with an encrypted managed store with backups, retention/deletion policy and access control.
- Set a real `CC_ADMIN_TOKEN`; configure an approved mail/notification provider instead of the log/webhook stub.
- Qualified legal sign-off on the jurisdiction-specific policy wording; confirm retention (24 months leads / 90 days events) and the double opt-in process for newsletters.
- Staging delivery, timeout/retry, duplicate and provider-failure tests. `npm run verify:api` (23 checks) validates the local reference implementation, not a deployed provider.
- `npm run verify:live` against the real domain **after** an approved release. A green build is not deployment proof.

## Historical note

The 2026-10-14 version of this file documented a backend-less site with all endpoints empty and a purely manual hand-off. That contract was superseded on 2026-11-08 by the first-party pipeline above. The old behaviour is retained **only** as the static-host fallback. `docs/audit/*` and `docs/completion-2026-10-14/*` are historical evidence, not current instructions.
