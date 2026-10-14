/* Public integration settings. Never put API keys, secrets or payment prices here.
   Endpoints must be same-origin /api/... routes supplied by your backend.
   Empty endpoints keep the explicit WhatsApp/email hand-off (no simulated success).
   Contract and launch gates: docs/INTEGRATIONS.md. */
window.CC_CONFIG = Object.freeze({
  contactEndpoint: '',
  newsletterEndpoint: '',
  careerEndpoint: '',
  bookingUrl: '', // HTTPS scheduler URL, after owner approval
  analyticsEndpoint: '', // same-origin collector; requires explicit consent
  requestTimeoutMs: 12000,
});
