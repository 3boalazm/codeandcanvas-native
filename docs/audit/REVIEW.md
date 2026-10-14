# Fresh-eyes review — Code & Canvas native site (2026-10-14)

Scope: the whole native site as it stood after the gap fixes (commit `c8675f8`). Six reviewer lenses, five buyer personas, one question per page: *what is the job of this page, is the panel order serving it, what is filler, what is missing?* Benchmarks (patterns only): Pentagram, Instrument, Work & Co, Huge, ustwo, Basic/Dept, Metalab, Locomotive — proof before words, services as outcomes, one primary CTA per viewport, typographic hierarchy over decoration.

Priority: **P0** = ships in this overhaul (conversion / clarity / correctness) · **P1** = ships in this overhaul if no asset is missing · **P2** = follow-up (needs an asset, a decision, or a backend).

---

## 0. Executive summary

1. **The site explains itself too slowly.** The hero says *Business Development By Design* (a slogan), the second panel says *Make the next move mean something* (a mood), and the first concrete sentence about what is sold arrives on scroll three. World-class studio homepages name the offer, the buyer and the proof in the first viewport.
2. **No proof on the homepage.** Three shipped products (Pharmacy OS, Zad, Nile Pharma ERP), five measured outcomes (85 % HIMSS Stage 6, −12 % ICU LOS, 25 % faster close, −40 % admin, $500K+ savings) and four credentials exist — none of them appear on `/`. The home shows a decorative "dashboard" instead.
3. **Duplicated panels.** The 3-step approach is rendered twice on the home (hero visual + section 05). The 8-stage methodology is on `/about/` and `/methodology/`. The founders are on `/about/`, `/team/`, `/services/`, `/technology-services/`, `/creative-services/`. Five different closing blocks ("Can't Wait To Hear From You", "Unlock the Potential of IT…", "What service appealed to you…", "The Home of Business Development", "Hope you enjoyed the journey") compete for the same job.
4. **Filler.** "Where creativity meets technology." (a 4-word section), "Growth, with intention", decorative orbit/dash visuals, repeated "Scope, timing and investment are confirmed…" notes.
5. **The buyer is never asked who they are.** Five very different personas land on one generic flow; the four tracks are listed by *our* org chart (Tech / Creative / Healthcare / Combined) instead of *their* problem.
6. **Technical gaps that cost rankings/shares:** no JSON-LD anywhere, no `og:image`, Twitter card `summary` only, no analytics hooks, single-URL bilingualism (Arabic is not indexable).
7. **The strongest assets are already there** — a 23-item fixed-price catalogue, published payment terms, real credentials, two named founders, eight long-form articles, four books. The overhaul is mostly *re-sequencing and cutting*, not writing.

---

## 1. Reviewer lenses

### 1.1 Business / strategy
| Finding | Decision | Action | Pri |
| --- | --- | --- | --- |
| Positioning sentence is buried (home scroll 3, `/about/`). | Lead with it. | New hero H1/lead: *Brand, technology and data — built around a business outcome.* + one sentence naming both practices, KSA+Egypt, 23 fixed-scope services, from $170. | P0 |
| Healthcare is the highest-ticket vertical (HIS advisory $2.5K–$8K) and has real credentials, but on the home it is one of four equal tiles. | Give healthcare its own entry point in the hero ("Start here" offers) and keep the dedicated closing line. | Featured offers panel: HIS Selection Advisory · EA Quick-Start · Digital Launch Package (live content, gap H1). | P0 |
| The "two founders, two practices" structure is the studio's real differentiator (one table, no hand-offs) but it is explained only on inner pages. | Put it on the home as panel 3. | "Two practices. One table." band with both founders + credentials, linking to the tracks. | P0 |
| CanvasOne ERP is an interactive *proposal* (package builder), not a shipped product, yet it is home section 03 with the largest visual. | Demote, keep. | Slim "Platform" band after proof; honest label "interactive proposal — configure a package". | P0 |
| Freelancer/Career form sits on the *buyer* catalogue page. | Move to `/team/` (people page), link from footer + services note. Nothing lost. | — | P0 |
| Legacy "Full Brand Identity" product stats (66 projects / 4 awards) are not used. | Keep excluded (contradict 40+ brands / 12+ sectors). | — | — |

### 1.2 Marketing / conversion
| Finding | Decision | Action | Pri |
| --- | --- | --- | --- |
| Hero primary CTA is an anchor to "Our services"; the money action (book a call) is secondary. | Swap. | Primary: *Book a free 30-min call* · Secondary: *See 23 services*. | P0 |
| Closing section has three equal buttons and no sub-copy; live had three *cards* with reasons ("Free · Video call · 30 min", "respond within the business day"). | Restore the 3-path cards (gap H5). | `paths` component on home; reused as compact closing on inner pages. | P0 |
| Trust strip (4 promises) sits only at the bottom. | Also under the hero offers. | "Clear scope · Milestone payment · We'll say no · KSA+Egypt" micro-strip. | P1 |
| No "best for" hooks — a founder cannot tell in 2 s which track is theirs. | Add one line per track. | *For CIOs & transformation leads / For founders & marketing leads / For clinics & hospitals / For launches that need both.* | P0 |
| "Customize your own package" exists only as a text link. | Panel. | 5th tile in the tracks grid → `/contact/?inquiry=custom`. | P0 |
| Insights and Books are invisible from the home (only nav/footer). Content is a credibility and SEO asset; books are revenue. | Add a "Learn" band. | 3 latest articles + 2 books. | P1 |
| WhatsApp is the fastest channel for the region but only a nav icon on desktop. | Keep nav icon, add to path cards and footer. | — | P1 |
| Pricing is a differentiator (fixed, published) but not in the primary nav. | Add *Pricing* to the nav. | Nav: Services · Healthcare · Work · Pricing · About · Insights · Books. | P0 |

### 1.3 UX / IA / design
| Finding | Decision | Action | Pri |
| --- | --- | --- | --- |
| Nav label "Solutions" is vaguer than the page (`/services/`, 23 services). | Rename to *Services*. | — | P0 |
| Home panel order: hero → stats → mood intro → tracks → ERP → why → statement → approach (dup) → closing. | Re-sequence (see §3). | Rebuild `index.html`. | P0 |
| Hero visual = decorative dashboard duplicating section 05. | Replace with informational panel (featured offers). | — | P0 |
| "Where creativity meets technology." statement section. | Cut. The phrase survives as the Why kicker. | — | P0 |
| `/services/`: 23 cards, no in-page navigation. | Sticky anchor pills (Technology · Creative · Healthcare · Combined · Pricing). | `subnav` component (reused on technology/creative/pricing). | P0 |
| `/technology-services/`, `/creative-services/`, `/healthcare/`: founder bio before proof and before services. | Proof first: hero → proof band (credentials + numbers) → services → method/capabilities → founder → CTA. | Reorder generators. | P0 |
| `/about/` repeats the 8 stages and both founder bios. | Keep a 1-line summary + link to `/methodology/` and `/team/`; keep the positioning, why-us, values. | — | P1 |
| `/contact/`: cards → form; form is the job. | Form + booking first, contact cards as aside; remove the duplicate closing ("Can't wait to hear from you" twice). | — | P0 |
| Five different closing blocks. | One `closing` component, page-specific lead line (the live phrases are kept as the lead lines so no copy is lost). | — | P0 |
| Blog/Books hubs are fine. Book landings: fine. Account: fine. 404: fine. | — | — | — |
| Decorative `orbit` on ERP band and `dash` in hero are heavy for what they say. | Remove `dash`; keep `orbit` only on `/erp/`. | — | P1 |

### 1.4 Content / copy
| Finding | Decision | Action | Pri |
| --- | --- | --- | --- |
| Why-us pillars lost their labels, tags and closing lines in the port (gap H2/H3). | Restore full live copy, 4 cards. | — | P0 |
| Section kickers are abstract ("Growth, with intention", "A clear way forward"). | Replace with functional kickers ("What we do", "Selected work", "How we work"). | — | P0 |
| Closing copy on About/Methodology: "Unlock the Potential of IT to Streamline Operations and Boost Productivity" — generic, Elementor-era. | Keep the sentence as the lead line of the unified closing (it is live content), headline becomes the studio's own. | — | P1 |
| "Scope, timing, and investment are confirmed around the engagement." appears on every service page. | Keep once per page, inside the price area. | — | P1 |
| Arabic twins exist for all strings; a few `data-ar` values are longer than EN and break pills on mobile (track meta). | Shorten the Arabic meta strings. | — | P1 |

### 1.5 Technical (SEO / performance / accessibility / i18n)
| Finding | Decision | Action | Pri |
| --- | --- | --- | --- |
| No structured data on any page. | Add JSON-LD from the generator. | `Organization` + `WebSite` (home), `BreadcrumbList` (all inner), `Service`/`OfferCatalog` (services, pricing), `Article` (posts), `Book`/`Product` (book landings), `FAQPage` (pricing FAQ). | P0 |
| No `og:image`; `twitter:card=summary`. | Ship a default 1200×630 OG image (brand mark on navy) and `summary_large_image`. | `assets/brand/og-default.png` via ImageMagick from SVG. | P0 |
| Single-URL bilingualism — Arabic is swapped client-side; Google indexes English only. | Out of scope for a static swap; document. | P2: build-time `/ar/` mirror from `data-ar` attributes (generator already has every string). | P2 |
| Google Fonts loaded from fonts.googleapis.com (3 families) + a local TTF. | Fine for now; self-host P2. | — | P2 |
| Reduced-motion handled globally; skip-link present; nav has aria. Focus rings exist on `.btn`. | Keep. Verify new components get `:focus-visible`. | — | P0 |
| `sitemap.xml` + `robots.txt` regenerate from the registry. | Keep; ensure the new home anchors are not listed as pages. | — | — |
| Dev server has no caching headers (not production). `vercel.json` carries redirects. | Keep. | — | — |

### 1.6 Analytics / measurement
| Finding | Decision | Action | Pri |
| --- | --- | --- | --- |
| No event hooks: nothing tells the owners which CTA converts. | Add a provider-agnostic `CC.track(name, props)` that pushes to `window.dataLayer` (GTM/GA4-ready) and fires a `cc:track` DOM event; no third-party script shipped (cookie policy stays true). | `data-track` on: book-call, whatsapp, email, add-to-cart, checkout, contact-submit, lang-toggle, service-filter. | P0 |
| Forms post to a demo handler; no backend. | Document; the hook makes any provider a one-line change. | — | P2 |

---

## 2. Persona walks (before → after)

| Persona | Before | After |
| --- | --- | --- |
| (a) Hospital/clinic CIO, KSA | Lands on a slogan; healthcare is tile 3 of 4; credentials appear only on `/technology-services/` scroll 3. | Hero offers show *HIS Selection Advisory — $2.5K · 3–5 weeks · CPHIMS-delivered, CBAHI + NORA aligned*; *Healthcare* in nav; proof band first on `/healthcare/`; closing has the healthcare discovery line. |
| (b) Founder launching brand + web | Must discover "Combined Engagements" (tile 4) to find the Digital Launch Package. | Hero offers show *Digital Launch Package ⭐ $3.5K · 6–8 weeks*; tracks carry "for founders & marketing leads"; path cards explain *fixed scope · from $170*. |
| (c) SME owner starting transformation | No cheap entry point visible. | *EA Quick-Start Assessment $1K · 2 weeks* in the hero offers; "Build your own package" tile; ERP proposal band for operations needs. |
| (d) Marketing lead buying retainers | Creative track → 10 services, retainers at the bottom; no proof of brand work. | Creative page proof band (40+ brands · Behance · Nile Pharma Food); subnav jumps to *Retainers*; "Most Popular" badge on the Full Brand System. |
| (e) Reader / book buyer | Books reachable only via nav; hub fine. | "Learn" band on home with the two available books; thank-you page now shows the order and the library link. |

---

## 3. Target homepage sequence

| # | Panel | Job | Source of content |
| --- | --- | --- | --- |
| 1 | **Hero** — concrete H1, one-sentence lead, primary *Book a free 30-min call*, secondary *See 23 services*; right: **Start here** — 3 featured offers | Say what/for whom/how priced; route the three biggest personas | live home (gap H1), catalogue |
| 2 | **Proof strip** — 10+ years · 40+ brands · 12+ sectors · 23 services + promises micro-strip | Credibility in one glance | existing |
| 3 | **Two practices, one table** — Ahmed (EA/healthcare, CPHIMS·TOGAF·NORA·EMRAM) · Mustafa (brand systems, 40+ brands) | Explain the studio's shape | `/team/`, `/about/` |
| 4 | **Services** — 4 tracks with "best for" + *Build your own package* tile | Route | existing + gap H4 |
| 5 | **Selected work + numbers** — Pharmacy OS · Zad · Nile Pharma ERP; 85 % · −12 % · 25 % · −40 % · $500K+ | Proof | `/case-studies/`, `/technology-services/` |
| 6 | **Why Code & Canvas** — 4 pillars, full live copy | Differentiate | live home (gap H2/H3) |
| 7 | **How we work** — Listen · Shape · Deliver + link to methodology | Reduce risk | existing (single copy) |
| 8 | **Learn** — 3 latest articles · 2 books | Credibility + revenue | `/blog/`, `/books/` |
| 9 | **CanvasOne ERP** — slim band | Secondary offer | existing, demoted |
| 10 | **Choose your next move** — 3 path cards (call / catalogue / WhatsApp) + healthcare line + contact details | Convert | live home (gap H5/H6) |

Cut from the home: "Make the next move mean something" header (its paragraph moves into panel 3), "Where creativity meets technology" statement (becomes the Why kicker), the hero dashboard, the orbit visual.

---

## 4. Per-page panel orders (inner pages)

| Page | New order |
| --- | --- |
| `/services/` | hero → stats → **subnav** → Technology → Creative → Healthcare → Combined (+ how we charge) → Not sure? → closing. Career form moves to `/team/`. |
| `/technology-services/` | hero → **proof band** (credentials + 4 numbers) → subnav → services → capabilities → engagement model → **who delivers** (Ahmed) → CTA → closing |
| `/creative-services/` | hero → **proof band** (40+ brands · 12+ sectors · Behance · method in 4 acts) → subnav → services → à-la-carte → who delivers (Mustafa) → CTA → closing |
| `/healthcare/` | hero → **clinical context** (credentials + numbers) → services → who leads → CTA → closing |
| `/about/` | hero → stats → positioning → why (6) → founders (short, link to team) → methodology summary (link) → closing. 8-stage block removed (lives on `/methodology/`). |
| `/team/` | hero → founders → together (5 engagements) → **work with us** (career/freelancer form, moved) → closing |
| `/contact/` | hero → **form + booking** (main) with contact/location/WhatsApp cards as aside → no duplicate closing |
| others | unchanged except the unified closing |

---

## 5. Component additions
`offers` (hero featured offers) · `duo` (two practices) · `tracks` 5th tile · `work-strip` (3 case tiles) · `numbers` (results) · `pillars` (4 why cards, before→after + label + closing line) · `learn` (articles + books) · `paths` (3 closing cards) · `subnav` (sticky anchor pills) · `proof-band` · unified `closing` · `CC.track` + `data-track`.

## 6. Out of scope / follow-ups (→ Linear)
Arabic URL mirror (`/ar/`), self-hosted fonts, payment provider, form backend, analytics provider choice, real social URLs, Egypt landline confirmation, OG images per page, photography for founders/offices, case-study metrics for the creative track.
