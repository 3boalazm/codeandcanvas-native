/* ==========================================================================
   PUBLIC integration settings — no secrets, tokens or payment prices here.

   The review build ships a real first-party pipeline (server/api.mjs) served
   from the same origin by `npm run dev`. Forms are durably recorded in the CRM
   at /crm/, bookings get a calendar invite, and measurement events land in a
   consent-gated first-party collector. Everything still fails closed: if the
   API is absent on a static host, the browser keeps the explicit
   "draft prepared, not sent yet" WhatsApp/email hand-off.

   Third-party measurement IDs are intentionally EMPTY. GA4 / GTM / Clarity are
   loaded only after explicit consent, only when an ID is supplied here, and
   only after the legal policies are approved (docs/MEASUREMENT-PLAN.md).

   Contract and launch gates: docs/INTEGRATIONS.md · docs/LEAD-PIPELINE.md.
   ========================================================================== */
window.CC_CONFIG = Object.freeze({
  contactEndpoint: '/api/contact',
  newsletterEndpoint: '/api/newsletter',
  careerEndpoint: '/api/career',
  bookingEndpoint: '/api/booking',
  slotsEndpoint: '/api/booking/slots',
  analyticsEndpoint: '/api/events',
  bookingUrl: '',          // Optional approved HTTPS scheduler. Empty = first-party /book/.
  bookingPath: '/book/',   // First-party booking page (specialty → slot → confirmation).
  requestTimeoutMs: 12000,
  measurement: Object.freeze({
    ga4MeasurementId: '',  // e.g. G-XXXXXXX — consent-gated, policy approval required
    gtmContainerId: '',    // e.g. GTM-XXXXXXX
    clarityProjectId: '',  // e.g. abcd1234
  }),
});
