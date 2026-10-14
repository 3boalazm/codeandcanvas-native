# Acceptance log — 2026-10-14

Environment: Chromium 153.0.8010.0 headless (SwiftShader), 1 worker, local dev-server, external hosts blocked by tests/helpers.mjs.

## npm run check
```
41 page(s) carry chrome markers · 0 out of date
84 HTML files checked · 0 problem(s)
Generator parity: 91 outputs match isolated regeneration.
```

## npm run build
Static site built in dist/
`dist/`: 84 HTML files, 6.8M

## Arabic tree
`ar/`: 42 HTML files
- noindex English-only long-form: 8
- sitemap AR urls: 44

## Full Playwright run (frozen working tree)

```
Running 362 tests using 1 worker
  362 passed (12.8m)
```

| Suite | Count | What it proves |
| --- | ---: | --- |
| `matrix.spec.mjs` | 262 | every route × language × {390,1440}: one h1, no page errors, no failing local assets, no duplicate ids, ≥1 JSON-LD block, no clipped buttons, no horizontal overflow; plus 16 home-geometry viewports (320→1920) |
| `accessibility.spec.mjs` | 32 | axe wcag2a / wcag2aa / wcag21aa on 16 routes × 2 languages |
| `arabic.spec.mjs` | 42 | every `/ar/…` document: `lang=ar` + `dir=rtl`, self-canonical, reciprocal hreflang + `x-default`, zero `data-ar*` leftovers, one h1, JSON-LD, the language pill links to the English twin, that `?lang=en` cannot flip it, one no-JavaScript read of `/ar/services/`, and the language pill navigating to the Arabic twin while keeping `?inquiry=` |
| `flows.spec.mjs` | 26 | redirects, every service CTA context, registration/consent, shortlist integrity, reader gate, form API contract (accepted/rejected/http-error/invalid-json/timeout/network), analytics consent, sitemap/robots policy, no-JS fallback, preview internals 403 |

Deliberately unchanged: no test was skipped, weakened or deleted; the two a11y failures
found this round were fixed in the CSS that owns the rule (see REPORT §2).

## Measured page weights

| Page | English | Arabic |
| --- | ---: | ---: |
| `/` | 60 KB | 48 KB |
| `/services/` | 64 KB | 56 KB |

## Studio round (same day, after the four studio pages moved to v3)

```
41 page(s) carry chrome markers · 0 out of date
84 HTML files checked · 0 problem(s)
Generator parity: 91 outputs match isolated regeneration.
```

```
Running 362 tests using 1 worker
  362 passed (10.4m)
```

Pages re-shot at 1440 after the v3 pass, added to `docs/next-round/evidence/`:
`en-team-1440.png` · `en-our-story-1440.png` · `en-methodology-1440.png` · `en-books-1440.png`.

What this run re-verified after the change: the whole route matrix (including every `/ar/…`
twin of the four studio pages), axe on all 32 route/language pairs, the Arabic suite
(canonical / hreflang / no JS / language-pill navigation) and the flows suite. No test was
added, skipped or relaxed for this pass — the only new evidence is the screenshots.

## Editorial round — `/blog/`, `/books/`, `/contact/` onto v3 (same day)

```
41 page(s) carry chrome markers · 0 out of date
84 HTML files checked · 0 problem(s)
Generator parity: 91 outputs match isolated regeneration.
```

```
Running 362 tests using 1 worker
  362 passed (14.1m)
```

New screenshots in `docs/next-round/evidence/`: `en-blog-1440.png`, `en-books-1440.png`,
`en-contact-1440.png` (Arabic twins re-shot separately: see the `/ar/` captures in the
same folder). The suite run covers the rewritten routes and their Arabic twins in both
viewports, plus the 32 axe scans and the whole flows suite (newsletter/career endpoints,
book filters, reader gate, form contract) — unchanged and unskipped.

## Hero round — homepage hero restored from the owner's reference (2026-10-15)

```
41 page(s) carry chrome markers · 0 out of date
84 HTML files checked · 0 problem(s)
Generator parity: 91 outputs match isolated regeneration.
```

```
Running 362 tests using 1 worker
  362 passed (9.1m)
```

`/` no longer carries the v3 hero. The section is the one in the owner's screenshot:
the eyebrow strip, the three-line display title with the gradient italic “By Design” and
its brush stroke, the `BD` discipline pill, the original lead paragraph, the three CTAs
(`Our services` → `#solutions`, `Our profile` → `/our-story/`, `Learn more` → `#fit`),
the four discipline chips, and the `C&C / ENGAGEMENT FLOW` window with
`01 LISTEN / 02 SHAPE / 03 DELIVER` plus the two floating chips. Every new string carries
its `data-ar` twin, so the Arabic site was regenerated (`node scripts/gen-ar.mjs` → 42
pages written).

Screenshots: `en-home-1440.png` (new), `ar-home-1440.png` and `ar-home-390.png` (re-shot —
they previously showed the v3 hero).

Honest notes: the floating chips overlap the window corners by design at ≥1025px and become
static below the card at ≤1024px so they can never widen the document; the hero itself
carries no booking button (matching the reference) — booking stays in `#contact` and in the
section CTAs. The dead `.hero__card* / .ways / .way` rules and the dead `.thesis` RTL
selector were deleted rather than left behind.

## v3 round — `/erp/` and the account/shop shells (2026-10-15)

```
41 page(s) carry chrome markers · 0 out of date
84 HTML files checked · 0 problem(s)
Generator parity: 91 outputs match isolated regeneration.
```

```
npx playwright test tests/matrix.spec.mjs --grep "route /(login|register|forgot-password|reset-password|account|cart|checkout|thank-you)/"
  32 passed (34.4s)
npx playwright test tests/flows.spec.mjs tests/accessibility.spec.mjs
  58 passed (2.8m)
npx playwright test --workers=1        # full suite, same frozen tree
  362 passed (8.5m)
```

`/erp/` now uses the same numbered section heads as every v3 page (`.sec-head` +
`.sec-head__no`: teal number, uppercase kicker), with `--stack` on the platform and
compliance sections. The three status chips that used to float over the dashboard mock —
covering the KPI row, the sales chart and the invoice list, and colliding with each other
once the Arabic labels ran longer — are now a static three-up row under the mock at every
width (`grid-template-columns: repeat(3, …)`, two columns ≤720px). A new honesty line
(`hero.dash.note`, AR + EN) states that the interface shown is illustrative sample data,
not a customer screenshot and not a promised result. Two decorative blobs were deleted and
nine gradient/glow accents flattened, so the page stops competing with its own content.

`.sec-head--center` was fixed in `ds.css`: it centred inside the left column of a
two-column grid, so a "centred" head never actually sat on the page axis. It now stacks and
centres (verified: the three centred heads on `/erp/` sit at the container axis at 1440).

The eight account/shop shells moved from the legacy `.section__title` / `.section__lead` /
`.oops` heads to the same `.phero` component every other inner page uses (crumbs, `.eyebrow`,
`.phero__title`, `.hero__lead`), plus a `--tight` variant for the auth pages. The
"accounts are not available yet" notice moved out of the form card to page level, and the
card is now only the form container. Contracts kept verbatim: `data-form="demo"` +
`data-next`, `_hp` honeypot, `data-match="#f-password"`, `data-checkout` /
`data-integration="books"` / `data-whatsapp` / `data-mail` / `data-subject`, `[data-pay]`,
`[data-cart-total]`, `[data-cart-empty]`, `[data-library*]`, `.cart-table` markup, and every
field id/name. Dead CSS (`auth__head`, `auth__alt`, `auth__foot`, `auth__brand`,
`auth__title`, `auth__card--wide`) was deleted rather than left behind; `pages.css` went from
85855 to 85016 bytes.

Geometry: no horizontal overflow on `/erp/` and `/ar/erp/` at 360/390/1024/1440
(`documentElement.scrollWidth === clientWidth` in both languages), verified with a
per-element overflow sweep.

Screenshots: `v3-erp-hero-1440-2026-10-15.png`, `v3-erp-hero-ar-1440-2026-10-15.png`,
`v3-shell-login-1440-2026-10-15.png`, `v3-shell-login-390-2026-10-15.png`,
`v3-shell-login-ar-1440-2026-10-15.png`, `v3-shell-cart-1440-2026-10-15.png`,
`v3-shell-cart-ar-1440-2026-10-15.png`.

Still v2 (unchanged this round): the eight long-form articles, the two book detail pages,
`cookie-policy` / `pricing-faq` / `privacy-policy` / `terms-of-use`, and `/404.html`.
