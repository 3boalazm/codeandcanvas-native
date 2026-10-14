# Live-site gap report — codeandcanvas.net → native site (2026-10-14)

Method: every public live URL was fetched today and reduced to *facts* (numbers, prices, durations, names, bullets, labels, link targets). Each fact was searched in the visible text of the native page (`scripts/audit-text.py` → `docs/audit/native/*.txt`). Only differences are listed; everything else matched.

Legend — **ADD** = missing, added in this pass · **FIX** = present but wrong · **KEEP** = intentionally different (decision recorded) · **OWNER** = needs a decision/asset from Code & Canvas.

## 1. Homepage `/`

| # | Live fact | Native state | Action |
| --- | --- | --- | --- |
| H1 | Three featured offers under the hero: **HIS Selection Advisory** "$2.5K starting from · 3–5 weeks · Objective, evidence-based vendor selection — CPHIMS-delivered, CBAHI + NORA aligned. Wrong HIS: $50K–$200K exposure." · **EA Quick-Start Assessment** "$1K · 2 weeks · 2-week TOGAF-anchored architecture assessment — current state, capability gaps, 90-day action plan." · **Digital Launch Package ⭐** "$3.5K · 6–8 weeks · Brand identity + bilingual website + digital launch system with scalable positioning." | missing | **ADD** — "Start here" featured-offers rail (home rebuild) |
| H2 | "Why" pillars carry a label + tag each: 01 · Mindset → *Solution Makers* · 02 · Risk → *De-risking* · 03 · Speed → *4–7× Faster* · 04 · Team → *Cross-functional* | labels/tags dropped | **ADD** |
| H3 | Pillar detail copy: "higher conversions, stronger retention, measurable growth" · "A digital product is a means to a business goal — not just code." · "The biggest startup risk: building a product the market doesn't want … lean MVPs that gather data, not just ship features." · "Save time, save money — and ensure product-market fit from day one." · "accumulated playbook … modern No-code and AI tooling to launch digital assets **4–7× faster** than traditional methods." · "Speed is a competitive advantage. We build it in from day one." · "every design decision serves a strategic purpose, and every line of code supports the user experience" · "No handoff gaps. No lost context. One team, one outcome." | shortened, facts lost | **ADD** (full pillar copy + closing line per pillar) |
| H4 | "Customize your own package — Each brand has unique requirements and distinct details that set it apart from others. → Start now" | text link only | **ADD** as a proper panel next to the tracks |
| H5 | Closing paths carry sub-copy: "Free · Video call · 30 min" · catalogue card "Fixed scope … milestone-based payment, and a traceable business outcome. No open-ended retainers. From $500 · 1 week → 8 weeks" · WhatsApp card "Prefer a quick chat before committing to a call? … we'll respond within the business day. KSA +966 545 520 750" | plain buttons | **ADD** — 3 path cards (figures updated to the unified catalogue: from $22 · 3 days → 8 weeks) |
| H6 | Healthcare block secondary link "Review Services First ↑" | missing | **ADD** |
| H7 | "Industry Solutions — offering comprehensive IT solutions, Creative designs, and strategic marketing services to empower businesses of all sizes." | missing | **KEEP out** — legacy Elementor filler sentence, contradicts the positioning copy; its meaning is covered by the intro |
| H8 | 15 service cards S01–S10 + HC-01…05 rendered twice (desktop/mobile) | 4 track panels + catalogue on `/services/` | **KEEP** — catalogue lives on `/services/`; home shows tracks + featured offers |
| H9 | Stats "6 productized services" / CTA "9 Services" | 23 | **KEEP** — unified catalogue count |
| H10 | Typos "Where Cteativity meets Technology", "Order Executers" | fixed | KEEP |

## 2. `/services/` — all facts present (hero, stats, both founder cards, AB-01…06, MA-01…10, "Not sure which service", Freelancer/Career form, closing). Prices for MA-01…03 follow the Creative Services page (decision §7.3 of SITEMAP). ✔

## 3. `/technology-services/`

| # | Live fact | Native state | Action |
| --- | --- | --- | --- |
| T1 | Ahmed: "**7+ years** in KSA" (bio) and stat "7+ Years across KSA & MENA" | "10+ years in KSA" / "10+" | **FIX** → 7+ (live value; "10+ years" on the homepage is the studio's combined figure, not Ahmed's KSA tenure). Same fix on `/healthcare/` lead card. |
| T2 | AB-01 badge "⭐ Most Requested" | tag "TOGAF · NORA" only | **ADD** badge on the featured card |
| T3 | Everything else (85 % HIMSS Stage 6, 12 % ICU LOS, 25 % close, 40 % admin, $500K+, 4 credentials, 9 capabilities, engagement model, extended advisory $3,000–$8,000, trust strip) | present | ✔ |

## 4. `/creative-services/` — all facts present (4-act method with day ranges, à-la-carte price list, policy strip, Nile Pharma Food, Behance, Webflow). ✔

## 5. `/about/`, `/our-story/`, `/methodology/`, `/team/` — all facts present (incl. +40 % / +25 %, Services-led lists, 8 stages, two diagnostic layers, alignment matrix, five joint engagements). ✔

## 6. `/contact/`

| # | Live fact | Native state | Action |
| --- | --- | --- | --- |
| C1 | Static Google map of the offices | none | **ADD** "Open in Google Maps" links on both office cards (no API key needed) |
| C2 | Egypt phone "+20 109 250 0444" (contact page) vs "…0454" (every WhatsApp link) | 0454 everywhere | **OWNER** — confirm the landline; native uses the WhatsApp number consistently |
| C3 | Follow-us: Facebook / Instagram / LinkedIn company = `#` | omitted (only real links kept) | **OWNER** — supply URLs, slots exist in `pages_contact.py` |
| C4 | Form service list S01…HC-05 + "General Inquiry / Not Sure Yet" | present (mapped to unified codes) | ✔ |

## 7. `/pricing-faq/` — all facts present (payment splits, 3 policy cards, every service bullet list incl. .NET discovery, 10 FAQ answers, closing). ✔

## 8. `/case-studies/` — all facts present (EN copy + Arabic twins, stacks, module counts, live link, NDA note). ✔

## 9. `/blogs/` + 8 posts — hub stats recalculated from the 8 real articles (8 · 8 topics · ~58 min); the two "coming soon" cards are kept as teasers. All 8 bodies ported in full (1.4k–2.0k words each, stat tiles, frameworks, case tiles, takeaways, FAQ where present). ✔

## 10. Books

| # | Live fact | Native state | Action |
| --- | --- | --- | --- |
| B1 | Marketing Fundamentals viewer opens publicly on **Part 01 — Introduction to Marketing** ("A MODERN GUIDE · 2026"; chapters 01 What Is Marketing? · 02 The Evolution · 03 The Ecosystem; Arabic lead "مقدمة في التسويق — الأساس الذي يبدأ منه كل شيء قبل الإعلانات والمحتوى والعلامة التجارية.") | landing says "TOC shown after purchase" | **ADD** — opening-part preview on the landing (public on live, so not paid content) |
| B2 | Basics of Visual Identity landing: 16 chapters / 3 journeys, every chapter teaser, "next book" link | present | ✔ |
| B3 | Woo product pages for Graphic Design / UI-UX: placeholder image, "Uncategorized", 0 reviews | native landings | KEEP (no content to port) |

## 11. `/thank-you/`

| # | Live fact | Native state | Action |
| --- | --- | --- | --- |
| K1 | Order summary (order #, date, e-mail, payment method, subtotal, total) | single sentence | **ADD** — summary card fed from the local checkout (`cc-last-order`) |
| K2 | Next steps: 1 E-mail confirmation (now) · 2 Team review (within 24 h) · 3 Kickoff session (within 48–72 h) | missing | **ADD** |
| K3 | Links: Account Center · Browse books · Explore services · Home · WhatsApp KSA 🇸🇦 / Egypt 🇪🇬 | partial | **ADD** |

## 12. Auth, cart, 404 — all facts present (Google button, 2FA step, remember-me, reset-token states, empty cart, "Lost in the void"). ✔

## 13. Not carried over on purpose (unchanged decisions)
Legacy 2024 product "Full Brand Identity" (66 projects / 4 awards / 2 years / 20 clients — contradicts every other stat on the site), empty Woo products (IT Solutions, Data Analysis), 22 spam categories, duplicate pages (`/our-team/`, `/elementor-6205/`, `/healthcare-hub/` = copy of Creative), the Freelancer form's broken "Daytime/Daytime" select, image placeholders ("YOUR_IMAGE_URL_HERE" ×16).
