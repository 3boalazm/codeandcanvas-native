# Lead Management Pipeline — v2.0 (November 2026)

This document describes the pipeline **as implemented**, not an integration wish-list. Every claim below maps to code you can read.

## The flow

```
Visitor fills a form / books a call
        │  explicit consent checkbox (per form)
        ▼
Browser: assets/js/pages.js  ·  assets/js/booking.js
        │  same-origin POST, JSON, 12 s timeout, no third-party endpoint
        ▼
First-party API: server/api.mjs
        │  server-side validation · honeypot · rate limit · idempotency
        │  consent must be truthy · email syntax · timezone/slot checks
        ▼
Durable record: .data/leads.json · .data/bookings.json · .data/events.json
        │  (CC_DATA_DIR; outside the public static tree)
        ▼
CRM lead: New → Qualified → Proposal → Won / Lost
        │  scored on kind + service code + message length
        ▼
Notification: .data/notifications.log + optional CC_NOTIFY_WEBHOOK
        │  minimal payload: id, kind, timestamp — no raw message body
        ▼
Lead Desk: /crm/ (noindex, token-gated) — stages, notes, stats, CSV
```

## Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/api/health` | Liveness + build commit |
| POST | `/api/contact` | Website inquiry → lead |
| POST | `/api/newsletter` | Consented subscription → lead |
| POST | `/api/career` | Freelancer application → lead |
| GET | `/api/booking/slots` | Published business dates and 30-minute slots |
| POST | `/api/booking` | Validated reservation → booking + qualified lead |
| GET | `/api/booking/:id/calendar.ics` | Calendar sync with specialty, reference and reminder |
| POST | `/api/events` | Nine consent-gated measurement events only |
| GET | `/api/leads` | Admin: list/search leads |
| PATCH | `/api/leads/:id` | Admin: stage + note |
| GET | `/api/bookings` | Admin: booking list |
| GET | `/api/stats` | Admin: stage/event counts |
| GET | `/api/export.csv` | Admin: CSV export |

Admin routes require `Authorization: Bearer $CC_ADMIN_TOKEN`. The built-in `cc-local-admin` token is for local review only and **must** be replaced in production (`dev-server.mjs` prints a warning when unset).

## Stages

`New` (contact), `Qualified` (scored inquiry or booking), `Proposal`, `Won`, `Lost`. Stage changes are appended to the lead's timeline with an actor and timestamp; they never rewrite the original record.

## Privacy and honesty rules

- No lead is created without a truthy `consent` field; the browser shows a checkbox beside each form.
- `Do Not Track` / `Global Privacy Control` suppress measurement entirely.
- Only nine event names are accepted; form values, emails and URL query strings are never sent to `/api/events`.
- GA4 / GTM / Clarity IDs are empty by default and load only with an approved ID **and** granted consent.
- If the API is unreachable, the UI says the request **was not sent** and offers WhatsApp/email drafts. A click is never reported as a submitted lead or a confirmed booking.
- No account, payment, entitlement, receipt or purchase is implied anywhere in the flow.

See `/privacy-policy/`, `/terms-of-use/`, `/cookie-policy/` and `/claims/` for the public wording.

## Operational gates before production

1. Replace `CC_ADMIN_TOKEN` with a secret, and put `/crm/` behind host-level authentication as well.
2. Replace the file-based `.data/` store with an encrypted, access-controlled database; the current store is deliberately unencrypted at rest.
3. Configure a real email/WhatsApp notification provider if automatic notification is required. Today only the local log and an operator-controlled webhook exist.
4. Confirm retention (24 months leads / 90 days events) with a qualified legal adviser.
5. Deploy `server/api.mjs` as a Node service. Pure static hosting (Hostinger `public_html`, Vercel static) cannot execute it; on such a host the site correctly falls back to manual hand-off.

## Verification

```sh
npm run verify:api     # boots an isolated API and exercises the whole flow
npm run dev            # combined static + API + /crm/ on 0.0.0.0
npm run verify:live    # production acceptance against the live domain
```
