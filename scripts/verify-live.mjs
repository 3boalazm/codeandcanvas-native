#!/usr/bin/env node
/* ==========================================================================
   verify-live.mjs — production acceptance check against the LIVE DOMAIN.

   A green GitHub Actions run or a successful `hostinger` branch push is NOT
   evidence that the site answers. This script requests the real public URLs,
   checks status/content and a few page-level invariants, and fails loudly.

     npm run verify:live
     CC_BASE_URL=https://codeandcanvas.net npm run verify:live
     node scripts/verify-live.mjs --json

   Network-restricted sandboxes may not be able to reach the domain; in that
   case the script reports SKIPPED with the network error and exits 2 so CI can
   treat "no answer" as a failure rather than a pass.
   ========================================================================== */
const BASE = (process.env.CC_BASE_URL || 'https://codeandcanvas.net').replace(/\/$/, '');
const AS_JSON = process.argv.includes('--json');

const ROUTES = [
  ['/', ['Code & Canvas', 'og:image']],
  ['/ar/', ['Code & Canvas', 'dir="rtl"']],
  ['/services/', ['Services', 'og:image']],
  ['/case-studies/', ['Case', 'og:image']],
  ['/contact/', ['Contact', 'name="consent"']],
  ['/blog/', ['Insights', 'from-brand-identity-to-brand-systems']],
  ['/work/', ['Selected', 'work/']],
  ['/book/', ['Book a 30-Minute', 'book-form']],
  ['/saudi-arabia/', ['Saudi Arabia']],
  ['/egypt/', ['Egypt']],
  ['/privacy-policy/', ['Privacy Policy', 'first-party']],
  ['/terms-of-use/', ['Terms of Use']],
  ['/cookie-policy/', ['Cookie Policy']],
  ['/resources/', ['Resources']],
  ['/claims/', ['Claims']],
];

const out = [];
let networkError = null;
for (const [route, needles] of ROUTES) {
  const url = BASE + route;
  try {
    const res = await fetch(url, { redirect: 'follow', headers: { 'User-Agent': 'cc-live-verify/2.0' } });
    const html = await res.text();
    const missing = needles.filter((n) => !html.includes(n));
    const problems = [];
    if (res.status !== 200) problems.push(`HTTP ${res.status}`);
    if (!/text\/html/i.test(res.headers.get('content-type') || '')) problems.push('not text/html');
    if (/Lost in the void|404 — Lost/.test(html)) problems.push('404 page body');
    if (/{{OG_IMAGE}}/.test(html)) problems.push('unresolved shared-head placeholder');
    if (missing.length) problems.push(`missing markers: ${missing.join(', ')}`);
    out.push({ route, url, status: res.status, ok: problems.length === 0, problems });
  } catch (e) {
    networkError = e.message;
    out.push({ route, url, status: 0, ok: false, problems: ['network error: ' + e.message] });
  }
}

if (AS_JSON) {
  console.log(JSON.stringify({ base: BASE, networkError, results: out }, null, 2));
} else {
  console.log(`Live domain verification — ${BASE}`);
  for (const r of out) console.log(`${r.ok ? '✓' : '✗'} ${r.route}  [${r.status}]${r.problems.length ? '  ' + r.problems.join('; ') : ''}`);
}

const failed = out.filter((r) => !r.ok);
if (networkError) {
  console.error(`\nCould not reach ${BASE}: ${networkError}. Live verification is REQUIRED; do not treat a green build as deployment.`);
  process.exit(2);
}
if (failed.length) {
  console.error(`\n${failed.length}/${out.length} live route(s) failed. Production deployment is NOT approved.`);
  process.exit(1);
}
console.log(`\nAll ${out.length} live routes answered correctly.`);
