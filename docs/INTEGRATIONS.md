# Integration contracts and launch gates

Updated 2026-10-14. This is the contract for the **current completion-sprint implementation**, not the older demo checkout. No backend, payment gateway, scheduler or analytics provider is bundled or enabled.

## 1. Public configuration

Edit `assets/js/config.js`; it is loaded before `site.js` on all routes, including ERP. Do not put secrets, provider tokens or trusted commerce prices in a public script.

```js
window.CC_CONFIG = Object.freeze({
  contactEndpoint: '',        // e.g. /api/contact
  newsletterEndpoint: '',     // e.g. /api/newsletter
  careerEndpoint: '',         // e.g. /api/career
  bookingUrl: '',             // approved HTTPS scheduler URL
  analyticsEndpoint: '',      // e.g. /api/events; explicit opt-in required
  requestTimeoutMs: 12000,
});
```

All defaults deliberately remain empty. A form's nonempty `data-endpoint` overrides its configured endpoint. Only same-origin paths beginning `/api/` are accepted. Do not point the browser directly at a third-party form vendor: implement a server-side adapter. An invalid endpoint fails closed with a manual contact option, not an automatic fallback submission.

## 2. Form contract

`POST /api/<kind>` with `Content-Type: application/json`, `Accept: application/json`, same-origin credentials and a cancellable timeout.

Payload is the form's named fields, trimmed strings, plus:

- `page`: pathname, without query string;
- `lang`: `en` or `ar`;
- `kind`: `contact`, `newsletter`, `career` or `books`.

Examples of actual fields: contact uses `first_name`, `last_name`, `email`, `organization`, `inquiry`, `message`; career/newsletter use their rendered named controls. Book availability uses `name`, `email`, optional `phone`, `consent`, `inquiry` and a `message` containing catalogue IDs/titles. There is **no payment/order payload**. The `_hp` honeypot is checked locally and not included in the JSON. Backend validation remains mandatory; client validation is not a security control.

The only accepted success response is **2xx + valid JSON containing `accepted: true`**:

```json
{"accepted": true}
```

An empty 204, HTML response, malformed JSON, `accepted:false`, HTTP/network error or timeout does not confirm receipt. Failure preserves inputs, restores the submit button, offers explicit manual channels and emits `form-error`. Success clears the form and emits `form-success`. Concurrent submission from the same form is guarded. Timeout means the browser could not confirm delivery; it does **not** prove the server did no work. Implement server deduplication/idempotency before enabling production retry workflows.

With no endpoint, the browser prepares a WhatsApp/email draft. It says **not sent yet** and asks the visitor to finish in the selected app. A popup may be blocked; the status always includes clickable fallback links. This is `form-handoff`, never a confirmed lead, booking or subscription. Tests intercept `window.open` and abort external traffic; no real messages were sent.

### Backend owner must supply before activation

- Approved destination, access/retention/deletion policy, operational owner and delivery monitoring.
- Server-side validation/size limits, origin/CSRF controls, rate limiting and abuse protection.
- Secret management on the server, not in this repository or browser config.
- Durable acceptance semantics: return `accepted:true` only after durable receipt/queueing, not before.
- Newsletter consent and any required double opt-in/unsubscribe process. Frontend “request received” is not a confirmed list subscription.
- Staging tests for delivery, timeout/retry, duplicate requests and provider failure. Current tests mock this contract; they do not validate a deployed provider.

## 3. Booking

Only valid HTTPS `bookingUrl` values without embedded credentials are used. The contact page preserves a valid service code as `?service=HC-03`, etc. Empty/malformed configuration leaves the explicit manual WhatsApp link. Clicking/opening a scheduler is **not** a confirmed booking. A production booking conversion needs the scheduler's trusted confirmation/webhook integration and an approved privacy policy.

## 4. Measurement

`CC.track(name, props)` produces a bounded, in-memory diagnostic `window.dataLayer` (maximum 100 entries) and a `cc:track` DOM event. With empty `analyticsEndpoint`, no analytics network request is made.

With a same-origin collector configured, events are sent only after the visitor chooses **Allow**. **Decline** is equally available; settings in the footer allow withdrawal. Do Not Track (`1`) and Global Privacy Control suppress transmission even if consent was previously stored. The collector uses POST JSON; it must not depend on a browser secret. Do not attach an unconsented GTM/third-party listener to the diagnostic event and bypass this contract.

Payload: `{event:'cc', name, lang, path}` plus allowlisted identifiers only: `id`, `service`, `from`, `form`, `channel`, `filter`, `to`. Identifiers are length/character restricted. Automatic events exclude form values, email, notes, full URLs and URL queries. No visitor fingerprint, user ID, transaction or order ID is generated. Collectors/hosting still see network metadata; minimize logging and approve retention independently.

Current event families:

| Family | Meaning |
| --- | --- |
| `page-view` | Initial view with prior consent, or landing view when consent is granted; local-only if not allowed |
| `book-call`, `contact`, `whatsapp`, `email`, `phone` | Intent/click, not confirmed conversion |
| `service-inquiry`, `service-detail`, `service-finder`, `offer`, `track` | Service interest; valid context carried where available |
| `navigation`, `work`, `post`, `book`, `portfolio`, `erp`, `duo`, `see-services` | Navigation/editorial interest |
| `filter`, `lang-toggle` | Interface use |
| `form-attempt` | Passed client validation; not receipt |
| `form-handoff` | Manual draft prepared; not sent |
| `form-success` | Configured backend returned the accepted contract |
| `form-error` | Receipt could not be confirmed |
| `save-book`, `remove-book` | Local shortlist operations, not add-to-cart revenue/purchase |

Do not use click, handoff or shortlist events as purchase/lead totals. There is no `purchase` conversion in this build. Provider deployment, dashboards, retention and production privacy acceptance remain release gates.

## 5. Books and accounts

- `cc-cart` is a **single-copy local shortlist** of known catalogue IDs, not a shopping transaction. `assets/js/book-catalog.js` is generated from `scripts/lib/pages_books.py`.
- Stored titles/prices/quantities/unknown IDs are not trusted. Display values come from the generated catalogue, which itself is **not server payment authority**.
- `/account/` shows saved previews and a live local count, not an authenticated library. Cross-tab storage changes refresh it.
- `/checkout/` is an availability inquiry. It neither charges nor creates an order or grants paid access. `/thank-you/` is not a receipt.
- Auth/reset/2FA forms are explicitly unavailable UI; no login, reset, redirect-success or token is fabricated. Google login is disabled. Legacy `cc-library` values grant no access.
- Public reader content comes from inline public previews. No nonexistent manifest is requested. Position/notes are local only. Any optional future manifest HTML must be trusted and sanitized before publication; the current runtime is not a paid-content protection boundary.

A commerce release requires server authentication, secure sessions, authorization, server prices, order state, verified signed payment webhooks, idempotency, refund/access policy and protected content delivery. Do not reintroduce localStorage ownership or serve full paid manifests from public static assets.

## 6. Storage / index / deployment

Local keys: `cc-lang`, `cc-cart`, `cc-reader-*`, `cc-notes-*`, optional `cc-analytics-consent`; session key `cc-pre`. Clear in browser settings. Storage-denied/malformed states fail safely and do not claim a book was saved.

Auth, shortlist, checkout, status and reader routes have `noindex, follow` and are excluded from the sitemap. Crawling is allowed so robots can read `noindex`; robots rules are not access control. Arabic remains a client-side language on the same URL. No dedicated `/ar/` URLs or hreflang are claimed.

Generate: `npm run generate`; check: `npm run check`; build: `npm run build`; browser tests: `npm test` after `npm ci && npx playwright install chromium`. `npm run check` verifies 48 generated outputs in a temporary directory without rewriting the workspace. `build.sh` ships route directories/assets only, not tests/docs/tooling.

No merge, production deployment, DNS change or real external submission was performed in this sprint. Production headers/redirects, actual form/measurement delivery, physical devices, Safari/Firefox, assistive technology and production performance remain separately required checks.
