# REF / UI-reference study — framework and current status

> **عربية مختصرة:** الفولدر كان فاضي في أول فحص، وبعدين **الملفات نزلت فعلاً** في كوميت `52aeeb8b` («Add files via upload») الساعة 03:43 UTC من 2026-11-09: **63 مرجع بصري** (62 JPG + GIF). اتقرأوا واحد واحد، واتكتبت دراستهم الكاملة في **[`docs/REF-UI-STUDY-2026-11.md`](REF-UI-STUDY-2026-11.md)** — كل ملف بوصفه والفكرة اللي تستاهل النقل وقرار `B/C/D` ومكانه في السايت. الملف ده فاضل كـ **مرجع المنهجية**: الهوية، الـ rubric، خريطة الإدماج، قائمة الممنوعات وقالب الدراسة.

## 1. What was checked (2026-11-09 — updated after the upload)

| Check | Result |
| --- | --- |
| Working branch | `arena/e9a49e14-codeandcanvas-native` (active); `origin/main` = `596124ff8fa5f69ae8060ccb04b8074f2fe29459` (PR #18 merge) |
| `main` HEAD | `596124f` — «Merge pull request #18 …», 2026-11-09T09:27:38Z, on top of `52aeeb8b` («Add files via upload») |
| `REF` at `origin/main` | **64 entries = 63 real visual sources** (62 JPG + 1 GIF, 3,157,261 bytes) + the 1-byte `REF/123` newline placeholder |
| Local extraction | ignored `.qa-ref/originals/001.jpg`–`063.gif`, `.qa-ref/manifest.json` (original long filenames + blob sha + size + dimensions), 63 review thumbnails and `.qa-ref/notes.tsv` |
| One-by-one study | **complete**: 63 rows in [`docs/REF-UI-STUDY-2026-11.md`](REF-UI-STUDY-2026-11.md) §4; descriptions come from the opened images, not filenames |
| Decisions | **B 28** (adapt the idea) · **C 20** (defer) · **D 15** (reject) · **A 0** (adopt as-is) |
| Implementation | Phase 1 shortlist (§6), identity-safe Phase 2 `/system/` (§7) and Phase 3 no-go guardrails (§8) rebuilt and QA'd. No REF pixels, fonts, portraits, logos, licensed photos, client screenshots, CDN scripts, dashboards or numeric claims were published |
| Verification | `npm run gate` **711 passed / 0 failed**; `verify:api` 23/23; `audit:content` 155 pages / 110 findings / 0 blockers / `[claims] 0`; `check-phase3` 0 no-go signatures; light-theme axe matrix 38 pages / 0 violations |

The earlier pass found only `REF/123`; that conclusion applied **only to `fbe3fbc3`** and is superseded. `docs/REF-INVENTORY.md` was not generated from the numbered local copies because the dated study's per-file table already carries the original filenames, descriptions, decisions and placements; `scripts/ref-inventory.mjs` remains the helper for any **future** reference drop.

## 2. Study protocol (one item at a time)

1. **Inventory** — `node scripts/ref-inventory.mjs REF` (or any folder path). Produces a numbered row per file: kind, size, external dependencies, colours, class hints, heavy-effect flags, RTL hints, short hash. `--write` also saves `docs/REF-INVENTORY.md`.
2. **Read** — open every file, not just the filenames. For HTML/CSS/JS extracts, identify the actual UI idea (layout, interaction, motion, state), and for images identify what the element *does* rather than copying its pixels.
3. **Classify** — component / pattern / micro-interaction / layout / asset. Note the source licence and whether it is a snippet, a CodePen export, a library demo, a screenshot or a font.
4. **Evaluate** — score against the rubric in §4.
5. **Decide** — `A` adopt as-is (rare), `B` adapt the idea into our own tokens/markup (expected for most), `C` defer (needs an owner/legal/asset decision), `D` reject (conflicts with identity, performance, a11y, bilingual or claims rules).
6. **Map** — pick the exact home in the site (§5) and the existing class/partial/generator to extend.
7. **Implement, if approved** — change `partials/`, `assets/css/`, `assets/js/`, `scripts/lib/*.py` / generator helpers; then `npm run generate` (**never hand-edit generated HTML**).
8. **Prove** — `npm run gate` (711 Playwright tests after Phase 3), `npm run verify:api` (23/23), `npm run audit:content` (0 blockers), `npm run check:phase3` (0 no-go signatures), visual QA at 320/390/1440 in EN+AR, dark+light, a no-reduced-motion pass and a mobile jank check. Any new element must be `data-ar`-complete and present in both language twins.

The real pass delivered the **per-file table** (`# · source file · what it shows · idea · decision · placement · adaptation`), a **prioritised shortlist**, a **phased plan**, the Phase 1 code, the identity-safe Phase 2 `/system/` route and the Phase 3 no-go guardrails — all in `docs/REF-UI-STUDY-2026-11.md` §6/§7/§8. Phase 2 adapted mechanisms only; Phase 3 locked the rejection list; the `C` owner/legal/asset decisions remain pending.

## 3. Identity baseline (read from the source, not guessed)

Source of truth: `assets/css/ds.css`, `assets/css/fonts.css`, `assets/css/home.css`, `assets/css/live.css`, `partials/head.html`, `partials/top.html`, `partials/bottom.html`, `assets/js/site.js`, `scripts/lib/arize.mjs`, `docs/PUBLISH-GATE.md`, `docs/PWA.md`, `docs/ASSET-AND-CLAIM-REGISTER.md`.

### 3.1 Visual language
- Stated in `ds.css`: **“Modern-classic · glassmorphism · violet / teal / pink on deep navy.”**
- Dark is the brand default (`--navy: #00001e`, `--bg: #07071c`, `--panel: #0d0d28`); `--ink: #f5f4ff`, `--hi: #fff` is the bright emphasis token that flips in light mode.
- Accents: `--indigo #4f3fd8`, `--violet #8b6cff`, `--purple #7a55e0`, `--teal #3fd6c4`, `--pink #ee5ba3`, `--gold #f3c77a`.
- `--grad` = teal → violet → pink; `--grad-brand` = indigo → purple → violet. The **only** warm element is the amber/orange header CTA (`#ffc877 → #ff8f45`) with dark ink `#241206`.
- Glass: `--glass rgba(255,255,255,.04)`, `--glass-2 .07`, border `.1`, `--blur: 16px`; panels are `--panel` with `--line rgba(255,255,255,.08)`.
- Radii: `--r-sm 10px`, `--r 16px`, `--r-lg 22px`; **999px pills** for buttons, nav, chips, eyebrows. The header is a 64px-high full-width **glass capsule** with five `nav__ring` circular controls.
- Motion: `--ease cubic-bezier(.22,1,.36,1)`, `--ease-in-out`, `--shadow` deep/soft, `[data-reveal]` = opacity + 28px translate + 6px blur, sheen sweep on `.btn--primary`, magnetic buttons, scroll-progress bar, marquee, orbit nodes, ambient blobs/grain.

### 3.2 Typography (self-hosted, all OFL)
- EN: **Space Grotesk** (headings), **Raleway** (titles/numerals), **Poppins** (body). AR: **Alexandria** (headings/titles), **IBM Plex Sans Arabic** (body).
- Strict `unicode-range` per face; Latin-only range is deliberately limited to keep mobile font bytes low. No Arabic face is loaded for a Latin glyph, and `/ar/` pages do not preload the EN heading font.
- **Hard rule:** Raleway's OFL declares a *Reserved Font Name*. No modified/subset font binary may ship without a rename plus legal sign-off; Poppins' local licence text is still missing. Any new typeface needs `assets/fonts/SOURCES.md` + provenance.

### 3.3 Signature components already in the site
`nav__pill` / `nav__ring` / `nav__brand` / `nav__links` / `nav__round` / `nav__cta` / `burger`, `.btn` `.btn--primary` `.btn--glass` `.btn--sm` `.btn--lg`, `.glass` `.glass--deep`, `.panel` `.panel--deep`, `.card` (+ cursor-radial hover via `--mx/--my`), `.card__icon`, `.pill`, `.eyebrow`, `.kicker`, `.sec-head`, filter chips, `.toast`, `.to-top`, `.scroll-progress`, `.preloader`, `.ambient`/`.blob`/`.grain`, `.orbit__node`, `.footer__bottom` + `.footer__reg` + `#installApp`.

### 3.4 Non-visual rules that every imported idea must survive
- **Bilingual, real pages:** `/ar/…` twins generated by `gen-ar.mjs` + `arize.mjs`; `data-ar`, `data-ar-label`, `data-ar-html`, `data-ar-alt` swaps; zero `data-ar*` leftovers; RTL brand far right / burger far left; logical CSS properties; one H1; no overflow 320→1920 px.
- **Themes:** persisted `cc-theme` (dark default, explicit light), applied before first paint in `partials/head.html` and the ERP standalone head; `theme-color` follows; 73 light overrides; everything must use `var(--hi, #fff)` rather than hard-coded `#fff`.
- **Performance:** the last mobile pass reduced readiness to ~3.3 s and jank to **0 frames > 50 ms / 17.2 ms average** at 390 px; blurred drifting blobs, grain, cursor glow, heavy `backdrop-filter`, `will-change` and blur reveals are **disabled on phones**. Any always-on animation, large library, WebGL canvas or scroll listener is a regression risk, not a feature.
- **Accessibility:** axe WCAG2 A/AA + 2.1 AA in EN and AR, visible focus, Escape-to-close, `aria-expanded` / `aria-pressed` translated, `prefers-reduced-motion: reduce` respected, decorative effects `aria-hidden`.
- **Content / claims gate:** no unevidenced numbers, no client names or outcomes without evidence, `check-claims.mjs` bans guarantee language, all illustrative art stays labelled **ILLUSTRATIVE / NOT CLIENT WORK**, per-route OG images, consent on every lead form, no fake auth/commerce success states.
- **Assets:** `scripts/check-media.mjs` does not exist; `optimize-media.mjs` expects WebP + `-sm.webp` + OG variants. No hotlinked third-party images/CDNs. New imagery must be recorded in `docs/ASSET-AND-CLAIM-REGISTER.md`.
- **PWA:** `manifest.webmanifest` (standalone), `sw.js` (network-first HTML, stale-while-revalidate assets, `/api/*` + `/crm/*` excluded), `offline.html`, no-cache worker headers on both Vercel and Hostinger/Apache. No third-party script is loaded by default; analytics is consent-gated and first-party.
- **Build discipline:** `npm run generate` → `npm run check` (sync-chrome parity, links, generator parity, claims, media) → `npm test` → `npm run build`; `npm run gate` is the local equivalent of the required CI check. `check-generated.mjs` regenerates in an isolated temp from `scripts`, `partials`, `index.html`, `erp/index.html`, `assets/js/erp-data.js` — anything generated must be reproducible from those sources. Current green baseline: **711 passed (11.8 m)**, `verify:api` 23/23, `audit:content` 110 findings / 0 blockers on 155 pages, 159 HTML files / 0 problems, parity 161 outputs, `check-phase3` 0 no-go signatures.

## 4. Evaluation rubric (per item)

| Criterion | Weight | Pass condition |
| --- | --- | --- |
| Identity fit | 25 | Uses our navy/violet/teal/pink palette, 999px pills or 16–22px radii, glass borders, our fonts and our easing. Does not import a foreign visual language (neon brutalism, neumorphism, corporate flat blue, etc.). |
| Bilingual / RTL | 20 | Works with `data-ar*`, logical properties, Arabic line-height and glyphs, and the `arize.mjs` swap. No absolute left/right positioning that breaks RTL. |
| Performance / jank | 20 | No new dependency, no always-on rAF/WebGL/blur on phones, no layout thrash. Adds < ~10 KB CSS/JS and no extra font or large image to the first load. |
| Accessibility | 15 | Keyboard, focus, reduced motion, one H1, correct roles/labels in both languages, axe clean. |
| Content / legal / provenance | 10 | No fabricated claim, client screenshot, unlicensed font, third-party CDN or tracking. Licence recorded. |
| Implementation cost / gate risk | 10 | Fits the generator/partial model; does not require hand-editing 150+ generated pages or weakening a check. |

**Decision scale:** `A` adopt as-is · `B` adapt the idea (rebuild in our tokens) · `C` defer pending owner/legal/asset decision · `D` reject with reason. Most external UI snippets should be `B`: take the *interaction*, not the CSS.

## 5. Integration map — where an idea can land

| Surface | Existing home | Good candidate ideas | Watch out for |
| --- | --- | --- | --- |
| Header capsule | `partials/top.html`, `.nav__pill`, `.nav__ring` | active-link indicator, compact command/search, theme transition | five rings already fixed; RTL order; CTA hidden on mobile |
| Hero | `index.html` + `home.css` | typographic reveals, gradient mesh, stat strips, scroll cue | mobile jank budget; no blurred drifting blobs on phones |
| Section headers / eyebrows | `scripts/lib/h.py`, `.sec-head`, `.eyebrow` | numbered section markers, kicker lines | must work in AR and be generator-driven |
| Work / case cards | `scripts/lib/pages_case_studies.py`, `assets/css/case-study.css`, `.card` | hover tilt, reveal, tag chips, image treatment | every card stays labelled illustrative; no client proof |
| Filters / chips | `pages_portfolio.py`, `.chips button` | segmented filters, animated active pill | `data-ar`, keyboard, no layout shift |
| Buttons / CTAs | `.btn*` in `ds.css` | sheen, magnetic hover, loading/success state | `data-track` CTA analytics, no fake success |
| Forms / booking | `/book/`, `.form`, consent bar | inline validation, step progress, field focus | consent checkbox mandatory, no fake API success |
| Footer | `partials/bottom.html`, `.footer__bottom`, `.footer__reg` | link groups, back-to-top, install button | legal registration row must stay |
| Global micro-interactions | `assets/js/site.js` | scroll progress, toasts, cursor effects | disabled on mobile; `window.CC` and `body.is-ready` contract |
| Ambient / background | `partials/top.html`, `.ambient` | static gradients, grid, grain | heavy effects already cut on phones |
| Transitions / reveals | `[data-reveal]` in `ds.css` | staggered reveal, reduced-motion fallback | `playwright.config.mjs` runs with `reducedMotion:'reduce'` |
| PWA / install | `manifest.webmanifest`, `sw.js`, `#installApp` | install prompt UI, offline state indicator | only show on a real `beforeinstallprompt`; no push notifications |
| ERP standalone page | `erp/index.html`, `erp.css` | timeline, module cards, builder | it has its own head: theme/lang bootstrap must be kept in sync |

## 6. Hard “never” list for imported references

1. No external CSS/JS from a CDN, no `@import url(http…)`, no npm library added without review.
2. No font binary without licence text, provenance and Raleway-RFN legal sign-off.
3. No client photography, logo or screenshot without permission; no relabelling a concept study as client work.
4. No unevidenced number, percentage, testimonial or guarantee.
5. No hand-edited generated HTML — all shared chrome goes through `partials/` + `npm run generate`.
6. No `data-ar*` leftover, no absolute `left/right` for directional UI, no broken `/ar/` twin.
7. No always-on animation, `filter: blur`, `backdrop-filter` or scroll listener on phones.
8. No weakening of `check-claims.mjs`, `check-generated.mjs` or the publish gate to make an element pass.
9. No breakage of the theme bootstrap, the PWA cache policy, the first-party API/consent flow, or the footer legal row.
10. No new tracker or third-party identifier; measurement stays first-party and consent-gated.

## 7. Per-item study template (copy for every file)

```md
### N · `path/to/source.ext`
- **Kind / licence:** HTML snippet · CSS · JS · image · font · archive · unknown · licence: …
- **What it actually is:** one or two sentences describing the UI element and its interaction.
- **The idea worth taking:** the mechanism, not the pixels.
- **External dependencies:** CDN / library / font / none; size.
- **Fit score (§4):** identity /5 · bilingual /5 · perf /5 · a11y /5 · provenance /5 · cost /5 → weighted __/100.
- **Decision:** A · B · C · D — reason.
- **Where it lands:** exact file(s) + existing class/partial/generator helper.
- **Adaptation required:** tokens, RTL, reduced motion, AR copy, image provenance, claims wording.
- **Work / risk:** S · M · L · risk to `npm run gate`.
- **Verification:** EN+AR 390/1440, dark+light, axe, jank, `verify:api`, `audit:content`.
```

## 8. What I need from the owner

- For a **new** reference drop: push into `main/REF` (subfolders are fine), send a zip/attachments, or give the correct link.
- If a licence/attribution file exists, include it — it changes the `provenance` score and may turn a `B` into a `D`.
- Optional: say whether this pass should end with **a written study only**, or **study + implement the shortlist**. The default here is the study first; implementation waits for approval, because every adopted element has to pass the 680-test gate and the bilingual/claims rules.
