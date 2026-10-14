# Verification evidence — 2026-10-14

This directory records an independent verification of the **unchanged application snapshot** `4b0e854ae3f90cecd56d8f75e8e7fd29c0a5a41f`. See [the Arabic report](../REPORT.md) for interpretation and limitations.

## Files

- `browser-results.json`: 108 route/viewport/language observations, panel order/position, uncaught page errors, failed local responses, 16 axe scans (violations **and incomplete checks**).
- `flow-results.json`: interaction tests, ten prefill scenarios, 16 hero viewport measurements, intercepted contact hand-off, local demo purchase, unchecked consent, account counters, reader buttons, query redirect. Language toggle observations wait for the asynchronous state change.
- `targeted-results.json`: 320px Arabic CTA clipping, registration consent-validation observation, local HTTP status/redirect samples, sticky-anchor alignment, default-motion smoke.
- `i18n-results.json`: rendered literal HTML-tag text in Arabic after visiting all 42 routes.
- `static-results.json`: 42-page schema/metadata/link/form inventory. `trackedLinks` only counts tagged anchors; dynamic form/cart events are evaluated separately in the flow tests.
- PNGs: viewport screenshots, not design proposals. `home-1440-en.png` shows the hero fold; `home-320-ar.png` shows clipping. Google-hosted fonts were unavailable in this environment; do not treat these as final Arabic typography approval.
- `*-audit.mjs`, `static-audit.py`: scripts used to collect the evidence. These are **observation harnesses**, not a passing regression suite: they intentionally record current failures without fixing the site.

## Conditions

- Chromium 153.0.8010.0 via `@sparticuz/chromium@153.0.0`.
- `playwright@1.64.1`, `@axe-core/playwright@4.13.0`, axe-core 4.13.0.
- Local Node dev server, `0.0.0.0:3000`; browser requests to `localhost` are local test automation, not browser-facing application code.
- External page requests intentionally blocked; no live-site crawl, real contact submission or real payment.
- Primary scans use reduced motion. A separate smoke uses normal motion.
- Browser viewport emulation is not physical-device testing. No Safari/Firefox, full screen-reader evaluation, production Lighthouse/CrUX or security certification is claimed.
- Synthetic checkout data uses `audit@example.test`; the order is local/session-only.
- A missing manifest returns 404 and activates the existing public reader fallback. It is recorded, not treated as an unexpected route failure.
- Contrast occurrences are not deduplicated across viewports/languages. `excess` may include intentionally off-screen honeypots; do not equate every entry with a UI defect.

## Re-run without changing application dependencies

Run the existing dev server in a separate terminal/process. From the repository root:

```sh
node dev-server.mjs
```

In another terminal, still with the repository root as the working directory:

```sh
AUDIT_ENV="$(mktemp -d /home/user/.cache/cc-audit-repro.XXXXXX)"
export AUDIT_ENV
npm install --prefix "$AUDIT_ENV" \
  playwright@1.64.1 @axe-core/playwright@4.13.0 @sparticuz/chromium@153.0.0
cp docs/audit/verification-2026-10-14/evidence/*-audit.mjs "$AUDIT_ENV/"

# The sandbox lacked NSS/NSPR. Extract the runtime libraries bundled with
# Sparticuz rather than installing or modifying application dependencies.
node --input-type=module -e '
import fs from "node:fs"; import z from "node:zlib";
const d=process.env.AUDIT_ENV;
fs.writeFileSync(d+"/libs.tar",z.brotliDecompressSync(fs.readFileSync(d+"/node_modules/@sparticuz/chromium/bin/al2023.tar.br")));
'
mkdir -p "$AUDIT_ENV/libs"
tar xf "$AUDIT_ENV/libs.tar" -C "$AUDIT_ENV/libs"
export LD_LIBRARY_PATH="$AUDIT_ENV/libs/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"

node "$AUDIT_ENV/browser-audit.mjs"
node "$AUDIT_ENV/flow-audit.mjs"
node "$AUDIT_ENV/targeted-audit.mjs"
node "$AUDIT_ENV/i18n-audit.mjs"
python3 docs/audit/verification-2026-10-14/evidence/static-audit.py
npm run check
npm run build
```

The observation scripts overwrite their corresponding evidence JSON/screenshots. Runtime/browser support can differ by OS; the commands above describe the Linux sandbox used for this review, not universal installation instructions. Dependencies and browser binaries were kept outside the repository and are not committed.

## Historical verification

Read-only GitHub inspection:

```sh
gh pr view 2 --json title,body,commits,mergedAt,mergeCommit,url
gh api 'repos/3boalazm/codeandcanvas-native/git/trees/45b6985e4618ddaf6b13f25d53af4c151930263d?recursive=1'
git ls-tree -r 4b0e854ae3f90cecd56d8f75e8e7fd29c0a5a41f
```

All 169 blobs in the prior PR's final tree match the corresponding paths in the reviewed snapshot. PR #2 was already merged at `2026-10-14T18:58:49Z`. This audit performed no merge or deployment.
