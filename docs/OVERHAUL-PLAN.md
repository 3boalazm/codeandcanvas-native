# Code & Canvas — Overhaul plan (2026-10-14)

Working branch: `arena/327f43fd-codeandcanvas-native`. Live preview: port 3000 (`node dev-server.mjs`).

## 0. Operating rules

1. **Nothing invented.** Every number, client, price, credential or claim must exist on codeandcanvas.net or in this repo already. Missing proof → say so (placeholder slot), never fabricate.
2. **Edit the generators, not the HTML.** Inner pages come from `scripts/lib/pages_*.py` → `python3 scripts/gen-pages.py && node scripts/sync-chrome.mjs && node scripts/check-links.mjs`. Only `index.html`, `erp/index.html`, `404.html`, partials and assets are hand-edited.
3. **Bilingual always.** Every new string ships with its Arabic twin (`data-ar`, `data-ar-html`, `data-ar-label`).
4. **Every decision is logged** in `docs/audit/*` so the final report (MD + Google Doc + Linear) is a copy, not a memory.

## 1. Flow

| Phase | What | Output |
| --- | --- | --- |
| **P0 · Header** | Remove the wordmark next to the logo and the gradient disc behind it (partials/top.html + ds.css + re-sync all pages + erp/404). | commit |
| **P1 · Live-site audit** | Crawl every live URL listed in `docs/SITEMAP.md` §2 (marketing pages, 8 posts, books, auth, cart, thank-you, 404). Save the extracted text to `docs/audit/live/`. Extract the text of every native page to `docs/audit/native/`. Diff fact-by-fact (numbers, prices, names, bullets, links, labels). | `docs/audit/GAP-REPORT.md` + fixes in generators |
| **P2 · Fresh-eyes review** | Walk the native site as six reviewers: Business/Strategy · Marketing/Conversion · UX/IA/Design · Content/Copy · Technical (SEO/perf/a11y/i18n) · Analytics. For every page: what is the job of this page → is the panel order serving it → what is filler → what is missing. Benchmark against world-class studio sites (proof-first, few words, strong hierarchy, one primary CTA per view). | `docs/audit/REVIEW.md` (findings → decision → action, P0/P1/P2) |
| **P3 · Execute** | Information architecture + nav · homepage re-sequencing · per-page panel reordering and de-cluttering · new components where the review proved a gap (proof strip, service finder, sticky CTA, comparison, FAQ, next-step rails) · technical layer (JSON-LD, OG, hreflang, perf, a11y). Regenerate after each block. | code |
| **P4 · QA** | `npm run check` (chrome sync + links + anchors), HTML/tag balance, both languages, all breakpoints by CSS review, no dead links, no console errors in the dev server log. | green checks |
| **P5 · Report** | `docs/REPORT-2026-10-14.md` (what changed, why, what is left) → mirrored to a Google Doc → Linear project with one issue per follow-up. | MD + Doc + Linear |

## 2. Research method (P1/P2)

- **Source of truth** for content: the live pages themselves, fetched today (`fetch` → markdown). Not the previous snapshot.
- **Diff unit** = a *fact*: a number, a price, a duration, a name, a credential, a bullet, a button label, a link target. Each fact is either `present`, `present-but-different` (decision needed) or `missing` (add).
- **Benchmarks** for P2 (patterns, not copy): Pentagram / Instrument / Work & Co / Huge / ustwo / Basic·Dept / Metalab / Locomotive — proof-led hero, work before words, services as outcomes, one primary CTA per viewport, generous whitespace, typographic hierarchy over decoration, honest team pages, insights as credibility.
- **Personas** used to test the user flow: (a) Hospital/clinic CIO or owner in KSA, (b) Founder launching a product (brand + web), (c) SME owner starting digital transformation, (d) Marketing lead buying brand/design retainers, (e) Reader / book buyer.

## 3. Definition of done

- Header shows only the brand mark.
- No fact from the live site is missing from the native site (or it is listed with a reason in the gap report).
- Every page has: one clear job, a primary CTA, a logical next step, no duplicate/filler panels.
- `npm run check` passes; sitemap/redirects regenerate cleanly.
- Report delivered in MD, Google Docs and Linear.
