# Code & Canvas — site overhaul report (2026-10-14)

Branch `arena/327f43fd-codeandcanvas-native` · commits `2aab58c` → `e61fbbe` · 114 files changed (+5,082 / −953).
Companion documents: `docs/OVERHAUL-PLAN.md` (plan) · `docs/audit/GAP-REPORT.md` (live → native content audit) · `docs/audit/REVIEW.md` (cross-team review and decisions) · `docs/audit/native/*.txt` (visible text of all 42 pages, used as the QA corpus).

---

## 0. The brief

1. Remove the wordmark text next to the header logo and the disc behind it.
2. Audit the live site (codeandcanvas.net) exhaustively — any information that exists there but not on the native build must be added.
3. Treat the native site as a fresh start: reorder/reshape panels, fix the user flow, cut filler, add improvements — business, development, design, marketing, analytics and technical lenses together.
4. Plan first, then execute; deliver a report, with every analysis as a Markdown file + Google Docs + Linear.

## 1. What was done — summary

| Phase | Output | Status |
| --- | --- | --- |
| P0 Header | brand mark only; wordmark + gradient disc removed (`partials/top.html`, `erp/index.html`, `ds.css`) | done (`2aab58c`) |
| P1 Live-site audit | 20 live URLs fetched and reduced to facts; 42 native pages dumped to text; 33 findings → `GAP-REPORT.md`; 14 gaps ported | done (`c8675f8`) |
| P2 Review | 6 lenses, 10-panel home sequence, per-page orders, component list → `REVIEW.md` | done |
| P3 Execute | new home, 7 inner pages reordered, nav, SEO, analytics hooks, components | done (`ac0cdba`, `e61fbbe`) |
| P4 QA | generator + chrome sync + link check + fragment check + tag-balance + JSON-LD parse + text-loss diff — all clean | done |
| P5 Hand-over | this report + Google Docs + Linear issues | done |

## 2. Research method (P1)

* **Source of truth = the live site, not memory.** Every public route of codeandcanvas.net was fetched on 2026-10-14 (home, services, technology, creative, healthcare hub, about, our-story, methodology, team, contact, pricing-faq, case-studies, blogs + a post, books, two product pages, the Marketing-Fundamentals viewer, thank-you, login).
* Each page was reduced to **facts** — numbers, prices, durations, names, labels, bullet lists, link targets — not prose.
* `scripts/audit-text.py` dumps the visible English text of every native page to `docs/audit/native/<route>.txt`; every live fact was grep-searched there. Hits ✔, misses → ADD / FIX, deliberate differences → KEEP (with the reason), things only the owner can answer → OWNER.
* The same dump was re-run after the overhaul and diffed against the pre-overhaul dump, so nothing that existed on the native site before the restructuring was lost by accident (see §7).

### Gaps found and ported (14)
Home: three featured offers under the hero (HIS Selection Advisory $2.5K · EA Quick-Start $1K · Digital Launch Package ⭐ $3.5K) · "Why" pillar labels/tags (Mindset → Solution Makers, Risk → De-risking, Speed → 4–7× Faster, Team → Cross-functional) and the full pillar copy · "Customize your own package" panel · the sub-copy of the three closing path cards · "Review services first ↑" link · the live disciplines pills (Product Strategy · Behavioral Design · Advanced Engineering · Business Intelligence).
Technology: Ahmed "7+ years in KSA" (was 10+) · ⭐ Most Requested badge on AB-01.
Contact: "Open in Google Maps" links for the three offices.
Books: Marketing Fundamentals landing now shows the public opening part (A MODERN GUIDE · 2026 · Part 01 with its three chapters and the Arabic lead).
Thank-you: full order summary (from the local checkout), the 3 next steps with timings, and the link/WhatsApp block.
Kept out on purpose (recorded): the legacy "Industry Solutions" filler sentence, the "Full Brand Identity" 2024 product stats, empty Woo products, spam categories, duplicate pages, the `0444` landline (WhatsApp number used consistently — owner to confirm), company social links that were `#` on live.

## 3. Review findings (P2) — why the site was rebuilt

Six lenses were applied to all 42 pages (business, development, design, marketing, analytics, technical). Head-line problems:

1. **The site explained itself too slowly** — slogan hero, mood headline, first concrete sentence about what is sold three panels down.
2. **Proof came last** — results (85% HIMSS Stage 6, −12% ICU LOS, $500K+) sat at the end of the technology page; the home had no results at all.
3. **Four CTAs competed** (Profile, Services, Learn more, Book) with no primary path.
4. **Filler** — four-word sections, abstract kickers, decorative orbit/dashboard visuals, repeated notes.
5. **Flow defects** — service pages mixed bio → method → services; the career form lived on the buyers' services page; the contact page put the form after three cards and repeated the hero as a closing.
6. **Technical gaps** — no `og:image`, no JSON-LD, no analytics hooks, no sticky in-page navigation on 60-screen pages.

## 4. What changed — page by page (P3)

### 4.1 Home (`index.html`, `home.css`, `home.js`) — rebuilt
Old: hero + dashboard visual → "Make the next move mean something" → services → ERP → why → approach → contact (orbit visual).
New, outcome-first, 10 sections:

| # | Section | Purpose |
| --- | --- | --- |
| 1 | Hero — "Brand, technology and data — built around a business outcome." + 1 primary CTA (Book a free 30-min call) + 1 secondary (See all 23 services) + trust chips | say what is sold in one sentence |
| 2 | **Start here** — the three fixed-scope offers from the live home | fastest path to a purchase decision |
| 3 | Proof strip — 10+ years · 40+ brands · 12+ sectors · 23 services | credibility |
| 4 | **The studio** — two founder cards (The Code / The Canvas) with credentials and the live disciplines pills | who you buy from |
| 5 | **What we do** — four tracks as an editorial list with "for whom", service count, floor price + "Customize your own package" | route visitors |
| 6 | **Selected work** — 3 case tiles + verified results numbers (sourced: Ahmed's KSA engagements) | proof of delivery |
| 7 | **Why** — the four live pillars with before → after, label and closing line | differentiation |
| 8 | **How we work** — Listen → Shape → Deliver + links to the 8-stage methodology and payment terms | reduce risk |
| 9 | **Insights & books** — 3 articles + 2 books | authority |
| 10 | **Platform** — CanvasOne ERP band | secondary product |
| 11 | **Choose your next move** — 3 path cards (call / catalogue / WhatsApp), healthcare line, contact details, trust strip | convert |

Removed: hero dashboard, orbit visual, hero parallax, "Growth, with intention", "Make the next move mean something", "Where creativity meets technology" as a standalone section (now the Why kicker), duplicated scope notes. All removed CSS/JS was deleted (`home.css` rewritten; `home.js` is now meta + boot only).

### 4.2 Inner pages — reordered with `scripts/lib/_reorder.py`
| Page | Before | After |
| --- | --- | --- |
| `/technology-services/` | hero → bio → services → capabilities → credentials → outcomes → model → CTA | hero → **sticky section nav** → credentials → **results** → services → capabilities → engagement model → who delivers → CTA |
| `/creative-services/` | hero → bio → method → services → à-la-carte → CTA | hero → sticky nav → **proof band** (20+ brands · 4 acts/38 days · AR+EN · Nile Pharma Food · Behance) → services → à-la-carte → method → who delivers → CTA |
| `/healthcare/` | hero → who leads → services → credentials | hero → **clinical context** (credentials + outcomes) → services → who leads what → CTA |
| `/services/` | hero (anchor pills inside) → … → **career form** | hero → **sticky scroll-spy track nav** (Technology 6 · Creative 10 · Healthcare 5 · Combined 2 · Not sure?) → stats → tracks → Not sure? (career form moved) |
| `/about/` | hero → stats → glance → why → tracks → 8-stage tiles → position | hero → stats → **position** → why → tracks → glance → methodology as a compact **stage rail** (same text, ¼ of the height) → CTA |
| `/team/` | hero → founders → together → CTA | hero → founders → together → **Join us** (career form, moved here) → CTA |
| `/contact/` | hero → 3 cards → form → duplicate closing | hero → **form + booking** → channels; redundant closing removed |

Every reorder renumbers the kickers automatically; anchors referenced from the home (`#credentials`, `#results`, `#who`, `#proof`, `#not-sure`, `#career`, `#model`, `#position`, `#glance`) exist and are link-checked.

### 4.3 Navigation
Header: **Services · Healthcare · Work · Pricing · About · Insights · Books** (+ Contact on mobile), replacing Solutions / CanvasOne ERP / Why us / Our approach / Contact. Rationale: top-level items are now the things people search for; the ERP (a proposal) is reachable from the home band and the footer; "Pricing" is the single most requested page for a productized studio and was unreachable from the header.

### 4.4 Components added (`pages.css`, `home.css`)
`offers` · `duo` · `tracks` (5th "custom" tile) · `work-strip` + `numbers` · `pillars-x` · `learn` · `platform-band` · `paths` + `closing-foot` · `proof-band` · `stage-rail` · `subnav--sticky` (scroll-spy, horizontal scroll on mobile) · `btn-row` · `tstep` (thank-you steps). All responsive at 1180 / 1024 / 860 / 720 / 560 px; reduced-motion respected by the existing reveal system.

### 4.5 Marketing / analytics plumbing
* `CC.track(name, props)` in `site.js`: pushes to `window.dataLayer` and dispatches a `cc:track` DOM event. Delegated handler for `[data-track]` with `data-track-*` props and the href. 17 event names are live (book-call, see-services, offer, duo, track, work, post, book, erp, whatsapp, phone, email, portfolio, lang-toggle, form-submit, add-to-cart, checkout). No provider is bundled — GTM/GA4/Plausible just listen.
* `/contact/?inquiry=<CODE>` pre-selects the matching service in the form (custom / book-<slug> fall back to General Inquiry + a pre-filled message) and scrolls to it. Every service link that ends in a sale now lands on a pre-filled form.

### 4.6 SEO / sharing
* `assets/brand/og-default.png` (1200×630) rendered from the brand SVG + Poppins by `scripts/make-og.mjs` (reproducible). `og:image`, `og:image:alt`, `og:site_name`, `twitter:card=summary_large_image`, `twitter:image` on all 42 pages (shared head partial; ERP page patched by hand).
* JSON-LD on every page: `WebPage` + `BreadcrumbList` (generated from the breadcrumb trail); `Organization` + `WebSite` + two `Person` nodes on the home; `Article` on the 8 posts; `Book` + `Offer` (SAR) on the book landings; `ItemList` of `Service` nodes on `/services/` and the three track pages; `SoftwareApplication` on `/erp/`. All blocks parse; `</` is escaped.
* Canonical + `og:url` added to `/erp/`.

### 4.7 Content decisions taken (from `SITEMAP.md` §7 — these were live-site contradictions)
| Conflict | Decision |
| --- | --- |
| Studio stats 10+/40+/12+ vs 7+/20+/6 | Studio-level figures (10+ · 40+ · 12+) on the home/about/services stats; **personal** figures on the founder cards (Ahmed 7+ yrs KSA; Mustafa 9+ yrs · 20+ brands · 6 sectors). The creative proof band uses Mustafa's personal numbers. |
| Service count 6 / 9 / 14 / 15 / 16 | 23 everywhere (AB 6 + MA 10 + HC 5 + CC 2). |
| Egypt phone 0444 vs 0454 | 0454 (every WhatsApp link) — **owner to confirm** the landline. |
| Typos "Cteativity", "Order Executers", "Our Sotory" | corrected. |
| Career form location | moved from `/services/` to `/team/#career` (text unchanged). |
| Duplicate closing on `/contact/` | removed (hero already says it; footer follows). |

## 5. QA (P4)

| Check | Result |
| --- | --- |
| `python3 scripts/gen-pages.py` | 41 pages + `_redirects`, `sitemap.xml`, `robots.txt`, `manus-routes.json`, `vercel.json` |
| `node scripts/sync-chrome.mjs --check` | 41 pages, 0 out of date |
| `node scripts/check-links.mjs` | 42 files, 0 problems |
| Fragment check (every `href="…#id"` across 42 files) | 0 missing targets |
| Tag balance (HTML parser, 42 files) | 0 errors |
| JSON-LD parse (42 files) | 0 invalid blocks |
| CSS class coverage (classes used in HTML but undefined) | 0 (after adding `track--tech`, `duo__card--code`, `learn__cover--violet`, `btn-row`) |
| `data-icon` coverage | 57 icons defined, 0 undefined |
| `node --check` on all JS | clean |
| Text-loss diff (pre- vs post-overhaul dumps) | only renumbered kickers, replaced paraphrases and the deliberately cut filler — every live fact still present (`grep` on `docs/audit/native/*.txt`) |
| Dev server (`node dev-server.mjs`) | all routes 200 |

Not possible in this sandbox: a real browser run (no Chromium/Playwright). Visual QA of the new home and the sticky navs on real devices is the first thing to do after pull.

## 6. How to work with the result

```sh
npm run dev                                   # http://localhost:3000
python3 scripts/gen-pages.py && npm run sync  # after editing scripts/lib/*.py or partials/
npm run check                                 # chrome sync + links
python3 scripts/audit-text.py                 # refresh docs/audit/native/*.txt (content QA)
python3 scripts/lib/_reorder.py scripts/lib/pages_X.py "Hero,Proof,Services,CTA"  # reorder blocks
npx -y -p @resvg/resvg-js node scripts/make-og.mjs                                # re-render the OG card
```
Rules that still hold: inner pages are generated — edit `scripts/lib/*.py`, never the HTML; the home is hand-written in `index.html`; `erp/index.html` carries its own chrome; the live site, domain and DNS were not touched.

## 7. Text-loss diff — what disappeared and why
Lines from the pre-overhaul native pages that no longer appear anywhere:
* Home: "MENA · Brand · Technology · Transformation · Data" (→ "KSA + Egypt · Brand · Technology · Transformation · Data"), "The core discipline behind every engagement" (→ the live wording "BD Business Development, By Design — the discipline behind every engagement"), "C&C / ENGAGEMENT FLOW", "BUSINESS-FIRST", "THE C&C APPROACH", "Start with the outcome.", "Strategy, design, and engineering — around one business goal." — all labels of the removed dashboard visual. "Growth, with intention", "Make the next move mean something", "A clear way forward" — native-draft kickers (not live content). Shortened pillar paraphrases were replaced with the **longer live pillar copy**. "Unified core" + the three ERP bullet variants → same facts, tighter wording in the platform band.
* Creative / healthcare / services: kicker numbers only (renumbered); "05 Freelancer? Connect to our development" now lives on `/team/`.
* Contact: "Book an appointment, start with our story, or browse the services." + the three buttons — the duplicate closing; the same three destinations are in the hero, the form aside and the footer.

## 8. Follow-ups (owner decisions / later sprints) → Linear
1. Visual QA on devices (home, sticky navs, RTL) — first task after pull.
2. Analytics provider: listen to `CC.track()`; define the conversion events in GA4/GTM.
3. Per-page OG images (all pages share `og-default.png`); founder/office photography; case-study screenshots (`.art[data-slot]`).
4. Confirm the Egypt landline (0444 vs 0454) and supply company social URLs (Facebook / Instagram / LinkedIn page).
5. Backend hooks: contact `data-endpoint`, booking URL, newsletter, auth API, payment gateway, book manifests (unchanged from the previous hand-over list).
6. Arabic URL mirror (`/ar/` + `hreflang`) if Arabic SEO matters; self-hosted fonts.
7. Case-study metrics for the creative track (today only the technology track has numbers).
8. Clean the WordPress install before the switch-over (spam categories, duplicate pages, "– Copy" posts).
