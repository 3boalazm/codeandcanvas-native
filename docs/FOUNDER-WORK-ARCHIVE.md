# Founder work archive — source & evidence register

Added 2026-11-08 to `/work/` (and its generated `/ar/work/` twin) on branch `arena/2072977a-codeandcanvas-native`.

## What was asked for, and what was done

The owner asked for **everything on Mustafa Aboalazm's work page** to be added to our work page «بما يتناسب مع ترتيبنا واستايلنا» — in a way that fits our order and style. The sources were:

| Source | What it contributed |
| --- | --- |
| `https://aboalazm-os.vercel.app/work` | Landing index, the two-track counts (Identity 8 / Digital Products 17), three featured identity projects, the "more projects" index wall |
| `https://aboalazm-os.vercel.app/work/design` | All 8 identity projects: title, year, description, tags, case-study link |
| `https://aboalazm-os.vercel.app/work/development` | All 17 digital products: title, year, description, tags, case-study link, live-preview link, status |
| `https://github.com/3boalazm?tab=repositories` | Public repository links used as third-party source pointers in the cards |

**Result:** 25 compact bilingual entries (`scripts/lib/data_founder_work.py`), rendered by `scripts/lib/pages_portfolio.py::archive_section()` as **section 02** of `/work/`, between the four labelled concept studies (01) and the publication gate (03) / claims register (04). Our numbering, `sec_head` pattern, gradient headings, filter chips, glass panels, `data-ar` translation mechanism, and `live-media-note` / `work-disclaimer` components are reused. Nothing was copied as raw HTML, CSS or imagery from his site.

## Order and style decisions

| His order | Our order | Why |
| --- | --- | --- |
| Featured 3 identity cards, then a separate "more" table, then a separate development track | One archive section, **Track 01 · Identity (8)** then **Track 02 · Digital products (17)**, with an All / Identity / Products filter | Matches our two-track studio positioning and our existing `.work-filters` behaviour; keeps one scannable index |
| Image-led cards with a large cover per project | Typographic index cards: number, year, status, title, one-line description, stack chips, source links | We do not hotlink or republish his imagery without permission; keeps the archive light on mobile and consistent with our evidence-first voice |
| External case-study links only | Case study + live deployment + public GitHub repo + our own case notes where a project overlaps `/case-studies/` | Uses the GitHub source the owner supplied and connects the archive to our existing routes |
| No disclaimer on the index | An explicit gold/teal `work-disclaimer` above the cards | Required by our claims discipline: an attractive image/link is not evidence |

Four entries explicitly link back into our own site: **Code & Canvas** and **Code & Canvas — Platform** → `/`, and **Zad** / **Nile Pharma ERP** → `/case-studies/` (where their evidence limits are already published).

## Honesty / claims contract

- These are **the co-founder's own published projects**, documented and linked. They are **not** presented as verified Code & Canvas client engagements, are not paired with measured outcomes, and are not captioned as our deliverables.
- Descriptions are **adapted**, not always verbatim. Stale counts in his case studies were removed rather than asserted against our real build (e.g. the older "82 pages" figure for the Code & Canvas platform; our generated site currently has 123 HTML pages). Numbers that describe *his* project scope (64 screens, 21 views, 69 items, 5 languages, 23 routes, 15 modules) are retained as quotes from his documentation and remain attributable via the case-study link.
- Project statuses (`In progress`, `Live product`, `Demo`) are carried over from his index and translated; they are not silent upgrades to "shipped" claims.
- No client permission, no screenshot, no testimonial and no outcome metric was invented. The existing four concept studies keep their `CONCEPT STUDY · NOT CLIENT WORK` labels and the `/work/` honesty paragraph stays intact.
- A **real client case** still requires the permission → evidence → attribution gate shown on the page and recorded in `docs/ASSET-AND-CLAIM-REGISTER.md`; adding a founder project to this archive does not bypass it.

## Inventory (25)

`✓` = source link carried over. `GH` = public repository pointer.

### Track 01 · Identity (8)

| # | Project | Year | Case | GH | Our notes |
| --- | --- | --- | --- | --- | --- |
| 01 | GAD Heart & Lungs Institute | 2023 | ✓ | — | — |
| 02 | Ahmed Bedeer | 2025 | ✓ | — | — |
| 03 | Nile Pharma Food | 2020–25 | ✓ | — | — |
| 04 | Code & Canvas | 2024 → | ✓ | ✓ | `/` |
| 05 | Reflection | 2022 | ✓ | — | — |
| 06 | Egypt SEG Field Camp | 2020 | ✓ | — | — |
| 07 | Learn in Arabic | 2020–21 | ✓ | — | — |
| 08 | Youth Scope | 2019–21 | ✓ | — | — |

### Track 02 · Digital products (17)

| # | Project | Year | Case | Live | GH | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | Code & Canvas — Platform | 2026 | ✓ | ✓ | ✓ | `/` |
| 02 | Nile Pharma ERP | 2025–26 | ✓ | — | — | `/case-studies/` |
| 03 | Nile Pharma Food — Storefront | 2026 | ✓ | ✓ | ✓ | — |
| 04 | OLTRÈ Collective | 2026 | ✓ | ✓ | ✓ | — |
| 05 | Zad | 2025–26 | ✓ | ✓ | ✓ | `/case-studies/` |
| 06 | Farm Console | 2025–26 | ✓ | ✓ | ✓ | — |
| 07 | Speech to Text Studio | 2026 | ✓ | ✓ | ✓ | — |
| 08 | Mini Exam | 2026 | ✓ | ✓ | ✓ | — |
| 09 | Ahmed Kamar | 2026 | ✓ | ✓ | ✓ | — |
| 10 | Continuum | 2026 | ✓ | ✓ | ✓ | — |
| 11 | Pharmacy Web | 2026 | ✓ | ✓ | ✓ | — |
| 12 | Youssef Guba | 2026 | ✓ | ✓ | ✓ | — |
| 13 | Ummah Academy | 2026 | ✓ | ✓ | ✓ | In progress |
| 14 | StemForge | 2026 | ✓ | ✓ | ✓ | — |
| 15 | Nile Bed | 2026 | — | ✓ | ✓ | Live product |
| 16 | Craft Egypt | 2026 | — | ✓ | — | Live product |
| 17 | Clinic Appointment System | 2026 | — | ✓ | — | Demo · request walkthrough |

Repository pointers are only attached where the public repo name unambiguously matches the project. Unmapped repos on the profile (`AZM-Box`, `Erfa3ly`, `DR-Osama-Shoier`, `Dr-Amro-Alahawany`, `Mohamed-Ahmed-Al-Rifai`, `-Ibrahim-Taha-Axiom`, `-Hobby-Digital-Wallet`, `ccna-Wezzah`, `mini-AI-Dos`) were **not** guessed into projects.

## Related fix

`scripts/verify-live.mjs` expected the word `Selected` on `/work/`, a marker left over from the pre-overhaul page. That stale expectation was the sole reason the post-merge Hostinger deploy run `42522043649` failed `Verify the LIVE domain` (14 of 15 route marker sets passed). The marker now checks for `CONCEPT STUDY` and `FOUNDER WORK ARCHIVE`, both emitted by the current generator. This is a test-expectation correction, not a relaxation: it still requires the live `/work/` body and rejects 404/unresolved-placeholder pages.

## Verification

`npm run generate` → `npm run check` → `npm run gate` (566 Playwright assertions + static build) → `npm run verify:api` → `npm run audit:content`, plus a 390px / 1440px EN+AR browser tour of `/work/`. No merge, deployment, or live-domain approval is implied by this document.

---

## 2026-11-09 · Detail pages for overlapping archive rows

The text index stays as described above. Archive rows whose subject matches one of the fifteen documented projects now link through to a bilingual `/work/<slug>/` detail page (`ARCHIVE_CASE_BY_URL` / `ARCHIVE_CASE_BY_TITLE` in `scripts/lib/data_case_studies.py`). One detail page may serve two archive rows (`nile-pharma` + `nile-pharma-storefront` → `nile-pharma-food`); this is a mapping decision, not an additional project or claim.

The `/work/` index now also carries a `Project cases · 15` CTA and a `#project-cases` card grid. `scripts/verify-live.mjs` therefore expects three markers on `/work/`: `CONCEPT STUDY`, `FOUNDER WORK ARCHIVE` and `PROJECT CASE STUDIES`. The older `Selected` expectation remains retired; no verifier check was relaxed.

The new pages add **no** client, screenshot, outcome, certification or deployment claim. They publish role/approach/build detail, source links, source notes and evidence limits; the three inaccessible repositories and the login-only live sites are still described as source-access-pending. See `docs/ASSET-AND-CLAIM-REGISTER.md` (2026-11-09 section) for the art provenance and the publication gates that remain open.
