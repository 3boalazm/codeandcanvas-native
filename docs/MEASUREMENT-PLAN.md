# Measurement Plan — v2.0 (November 2026)

## Canonical events

| Event | Fired from | Required properties |
| --- | --- | --- |
| `page_view` | `assets/js/site.js` boot, and `viewEvent()` from `data-view-track` | `path`, `lang` |
| `service_view` | service pages + `/book/` via `data-view-track` | `path`, optional `service` |
| `case_study_view` | work cards / case pages via `data-view-track` and `data-track` | `path`, `id` |
| `cta_click` | `data-track="cta_click"` | `id`, optional `service` |
| `form_start` | first focus/input in any lead form | `form` |
| `form_submit` | server accepted a contact/newsletter/career/booking request | `form`, `id` |
| `booking_confirmed` | server accepted a booking | `id`, `service` |
| `lead_qualified` | server moved a lead to `Qualified` | `id` |
| `lead_converted` | admin PATCH sets stage to `Won` | `id`, `stage` |

Server-side stage events are recorded in `.data/events.json` by `server/api.mjs`. Client events are batched to `/api/events` by `assets/js/site.js`.

## Consent rules

- `cc-analytics-consent=granted` is required before any provider loads or any client event is sent.
- `navigator.doNotTrack === '1'` and `navigator.globalPrivacyControl === true` suppress measurement and hide the consent bar.
- Without consent, `CC.track()` only keeps a bounded in-memory `dataLayer`/`cc:track` queue for other first-party logic; no network request leaves the browser.
- Withdrawal is available through **Measurement settings** in the footer.
- The queue is bounded (see `site.js`), contains no form values, no email addresses and no URL query strings.

## Third-party providers

GA4, Google Tag Manager and Microsoft Clarity IDs are empty in `assets/js/config.js`. `site.js` loads a provider only when **both** an approved ID is present and consent is granted. This makes the default release privacy-safe and makes adding a provider an explicit, reviewable configuration change. No advertising pixels, session replay or cross-site identifiers are enabled by default.

## What we do not measure

- No personal data in event payloads.
- No keystrokes, no form content, no scroll heatmaps.
- No fingerprinting and no cross-site tracking.
- No purchase or revenue events, because there is no commerce in this release.

## Verification

- `tests/flows.spec.mjs` — consent, DNT/GPC, PII exclusion, queue bound and withdrawal.
- `npm run verify:api` — `/api/events` acceptance and event store.
- `/claims/` — public evidence register for every published number.
