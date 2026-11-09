# REF UI references — one-by-one study (2026-11-09)

> **عربية:** رفعت 63 مرجع بصري في `main/REF` (كوميت `52aeeb8b`، «Add files via upload»). قرأت كل صورة على حدة، ووصفتها، واستخرجت الفكرة القابلة للنقل، وقيّمتها مقابل هوية Code & Canvas، وقررت لكل واحد: **B** ناخد الفكرة ونبنيها بتوكيناتنا، **C** يتأجل لقرار مالك/أصل مرخّص، **D** يُرفض بسبب تعارض هوية أو ادعاءات أو أداء. مفيش **A** (تبنّي حرفي) لأن كل الملفات لقطات لأعمال غريبة مش أصولنا.

## 1. Method and source

- Source: `github.com/3boalazm/codeandcanvas-native/tree/main/REF` at commit `52aeeb8b` (2026-11-09T03:43:11Z). 63 files: 62 JPG + 1 GIF (~3.16 MB); the 1-byte `123` placeholder was excluded.

- Each file was extracted, downscaled for review and **opened individually**; the notes were written per file, not inferred from filenames. Several filenames were misleading (e.g. `Blog.jpg` is an orbit diagram, `Progress Bar.jpg` is a stat card, `Chart snippet…Layers.jpg` is a ribbon chart) — the descriptions below come from the images themselves.

- Rubric: `docs/REF-UI-STUDY.md` §4 (identity 25 / bilingual 20 / performance 20 / a11y 15 / provenance 10 / cost 10). Helper: `node scripts/ref-inventory.mjs <folder>`.

- **Important:** these are third-party screenshots (Dribbble / X / Behance / stock / AI promos). Nothing here may be republished as-is. Only the *mechanism* is a candidate; every adopted idea is rebuilt with our own tokens, our own illustrative WebP art and bilingual copy.

## 2. Result at a glance

| Decision | Count | Meaning |
| --- | --- | --- |
| **B · adapt the idea** | **28** | rebuild in our design system |
| **C · defer** | 20 | needs owner/licence/asset decision, or is a duplicate |
| **D · reject** | 15 | identity, claims, performance or licensing conflict |
| A · adopt as-is | 0 | not applicable |

### Recurring idea families (why 63 files collapse into a few themes)

| Family | Refs | What we keep |
| --- | --- | --- |

| Fanned / stacked / scroll-snap card rails | 001, 003, 009, 010, 014, 026, 036, 038, 039, 040, 044, 056, 062 | CSS-only snap rail + fanned illustrative tiles + slit/expand gallery |

| Process / layer / orbit diagrams | 005, 013, 017, 024, 025, 027, 032, 034, 037, 052, 054, 055 | three-circle pillars, numbered process rail, capability orbit |

| Footers & ghost wordmarks | 006, 011, 019, 020, 021, 022, 028, 042, 048 | grouped bilingual link columns + restrained oversized wordmark + section index |

| CTA / hero atmosphere | 002, 006, 008, 018, 028, 033, 043, 047, 063 | static violet edge-glow CTA band + announcement pill + pre-rendered gradient WebP |

| Stats, charts and dashboards | 012, 015, 035, 049, 050, 051, 053, 054, 057, 058, 059, 060, 041 | **mostly rejected** — fabricated numbers break the claims gate; keep only an honest reading-progress cue |

| Palette / token showcases | 004, 016 | defer — needs an owner-approved real token table |


## 3. Shortlist selected for implementation this pass

Chosen for identity fit + low gate risk. All are **B**, all rebuild the idea rather than copying pixels:

1. **Three-circle pillars (Brand / Product / System)** — refs 005, 025, 013. CSS-only overlapping circles, numbered bilingual labels, ghost heading.

2. **Numbered process rail** — refs 017, 037, 052, 055. Alternating glass step cards with checklists; **no week/duration claims**.

3. **Static edge-glow CTA band** — ref 018. Violet radial glows, `--grad-brand` button, bilingual copy, no animation.

4. **Footer refresh** — refs 019, 022, 048. Grouped bilingual link columns + low-opacity wordmark band; legal registration row, install button and consent rules preserved.

5. **Scroll-snap case rail** — refs 001, 038, 044. CSS-only snap rail for the case-study cards at mobile widths, with a fanned tile accent.

6. **Announcement pill + section index** — refs 002, 028. Reuse `.eyebrow` and add a lightweight numbered section marker.


### Phased plan

- **Phase 1 — done in this pass:** the six items above, rebuilt with existing tokens, bilingual copy, no new assets, no dependencies and no claims. Covers the home hero system story, the footer brand mark, the phone case rail, the pill/index motif and the light-theme contrast repairs surfaced by the new components.
- **Phase 2 — shipped in the identity-safe form (see §7):** only the *mechanisms* of 004/016 (token cards), 023/041 (bento), 026 (native `details`/`summary` slit gallery), 044 (a static grid of tilted art tiles) and 045 (label plates with monograms) were rebuilt at `/system/` using our own tokens, our own labelled illustrative WebP and real generator counts. **The `C` decisions are still pending:** no licensed photography, client screenshot, team portrait, real-data dashboard or owner asset approval was supplied or assumed. REF 060 remains rejected.
- **Phase 3 — deliberately rejected:** fabricated metrics/charts, AI/crypto/health dashboard chrome, orange/cyan/serif skins, runtime blur/WebGL, third-party portraits and logos. They conflict with identity, evidence rules or mobile performance.

Deferred/rejected items still have value: they document what *not* to import (fake metrics, third-party portraits, orange/blue palettes, runtime blur, WebGL, AI-product positioning).


## 4. Per-file assessment (all 63)

| # | Source file | What it actually shows | Idea worth taking | Decision | Where it could land | Adaptation / reason |
| --- | --- | --- | --- | --- | --- | --- |

| 001 | `(1) Charlie J on X_ _One of the most underrated CSS props is d…` | CSS scroll-snap carousel of overlapping destination photo cards; centre card enlarged, side cards smaller/opaque, circular arrows + dot pagination + caption below | CSS-only scroll-snap rail with centre emphasis, no JS library | **B** | work/case cards on mobile | Rebuild in navy glass + our WebP illustrative art; RTL-safe logical scroll; reduced-motion fallback; dots/arrows need AR labels |

| 002 | `(1) Home _ X.jpg` | AgentBoost dark SaaS hero: black page, huge centred headline, small "New" pill, blue→cyan gradient glow band behind a rounded hero panel, outlined pill CTA, trust-logo strip | Announcement pill + controlled gradient wash behind hero + trust strip | **B** | hero / navbar eyebrow | Use our indigo→violet→teal gradient at low opacity, NOT bright cyan; keep one H1 and our existing CTA; trust strip must contain only real, evidenced names |

| 003 | `(3) Instagram.jpg` | Taski light-blue gradient page with 3 translucent rounded gradient cards stacked behind a front card (title, time, description), avatars + caption | Layered "card stack" depth behind a main panel | **B** | case-study / pillar cards | Recolour to violet/teal/pink glass; static layers (no heavy shadow), disabled on mobile if jank; decorative layers aria-hidden |

| 004 | `12343` | "UI Color Set" palette showcase: glass photo card, floating "Colors"/"Copy" pills, circular swatches, hex-code palette strip, gold circle | Interactive brand-token / palette card | **C** | design-system page or /about/ (defer) | Needs an owner decision + a real token table; no fabricated palette copy; not core business journey |

| 005 | `3 layer stack diagram template with space for your text - glas…` | "3 LAYER DIAGRAM" glassmorphism slide: three stacked elliptical discs (blue), numbered 01/02/03 pill labels with connector lines + description boxes | Three-layer process diagram — maps perfectly to brand / product / system | **B** | methodology or services "how we work" section | Rebuild as CSS-only stacked glass discs with our tokens; numbered bilingual labels; connector lines must flip in RTL; no stock vector |

| 006 | `A modern cybersecurity landing page designed for SaaS business…` | Cybersecurity landing: giant ghost outline word behind hero, framed hero panel with portrait, thin uppercase nav, floating numeric stat card, vertical SCROLL DOWN marker, play button, logos | Ghost oversized brand word + framed hero + vertical scroll cue | **B** | homepage hero background | Use low-opacity "CANVAS" wordmark only; REJECT the numeric stat card (claims gate bans unevidenced numbers); no portrait/stock photo; vertical marker needs dir-aware writing-mode |

| 007 | `ABDUL W_ _ Web calendar interface, My screen, Pinterest interf…` | Frosted calendar widget: Weekly/Monthly segmented pill, gear circle, huge "August 23", weekday row with gradient selected-day circle, "Add a note" + "New Event" button | Segmented control + active-state gradient circle + big display numeral | **B** | book/ scheduler or filters | We already have .seg/.chips; add our violet→pink active circle and a large --f-num display value; no invented availability |

| 008 | `AI APP BUILDER HERO PAGE.jpg` | AI app-builder hero: dark panel over blue gradient, centred headline, glass "Type something to generate" input card with platform chips and a Generate button, wave lines | Glass input card with chip row + one action | **D** | — | Fake "AI generates an app" product contradicts our honest-service positioning; keep only the glass-input styling cue for the real newsletter form |

| 009 | `Anyway.jpg` | Mobile story-card carousel: centre photo card with small category tag, bright rounded title label, "16 MINUTES", blurred side cards | Card carousel with category badge + title pill + reading time | **B** | blog / resources cards | Recolour tag/label to our violet/teal (not yellow); drop the numeric reading-time claim; blurred side cards are decorative only |

| 010 | `Athens Explorer App – Cultural Travel UX Concept.jpg` | Athens Explorer: glass browser toolbar pill, fanned translucent photo cards, centre card with Expand pill + title/description + "1/7" + location, bottom mini-nav pill with thumbnail and arrows | Fanned glass card stack with expand control + counter + bottom pager | **B** | work / case-study gallery | Simplify to CSS-only fanned layers (no WebGL/blur), bilingual counter, keyboard-operable Expand, aria-hidden decorative cards |

| 011 | `Azentos – Branding Studio Website Design.jpg` | Azentos orange branding-studio hero: giant outline BRANDING ghost word, silhouette portrait, thin uppercase nav, "472+/597+" stat cards, partner logos | Ghost word + bold colour field + stat cards | **D** | — | Orange field and unlicensed portrait clash with navy identity; numeric stat cards violate the unevidenced-claims gate; ghost-word idea already captured in 006 |

| 012 | `Battery Charging UI with Dynamic Island _ iOS Energy Status De…` | Battery/Dynamic Island status pills: black pill with green bolt + 76, larger pill with green progress bar and inline value + "~15m" | Compact status pill with inline progress bar | **B** | blog reading progress / scroll progress | Recolour green to our teal/violet; reuse existing .scroll-progress rather than adding a second progress listener; no fake percentage |

| 013 | `Blog.jpg` | Radial "continuous loop" diagram: blue glow core with a sentence, surrounded by 7 small white pill labels (Signals flows in, Insights emerge, …) | Orbit of pill labels around a glowing core | **B** | methodology / services capability loop | We already have .orbit__node (70s spin); replace with a static, reduced-motion-safe bilingual loop; no "AI innovation engine" claim |

| 014 | `Cards.jpg` | Three tilted fanned card decks (dark cards with bright covers), captions below and tag pills (ML, ChatGPT, UX, UI, YC, Startups) | Fanned deck as a collection/category visual + tag chips | **B** | resources / blog category groups | Use our own illustrative art and our .pill tokens; static rotation (transform only), no hover jank on mobile |

| 015 | `Chart snippet by Mohammed Kabir Hussaini _ Layers.jpg` | Orange layered-ribbon line chart with dotted crosshair, highlighted node and a "127.01au" tooltip pill | Data-viz ribbon motif + value tooltip | **C** | decorative section divider (defer) | No real dataset exists; a numeric tooltip would be an unevidenced claim. Only the layered-ribbon shape could be reused as pure CSS decoration after owner approval |

| 016 | `Color set.jpg` | Second "UI Color Set" palette card (green/pink/orange), glass photo, floating Colors pill, Copy swatch card, hex strip | Duplicate palette-showcase concept | **C** | duplicate of 004 | Same owner decision; no new idea to implement |

| 017 | `Crypto Swap (4) _ Images __ Behance.jpg` | "Design Phases" infographic: vertical numbered 1–5 timeline, alternating rounded cards with checklists and coloured duration pills | Alternating numbered process timeline with checklists | **B** | methodology page / services process | Strong fit; rebuild with our glass panels, numbered nodes, bilingual checklists; DROP the "2 weeks/3 weeks" duration pills (claims gate); RTL-safe connector lines; decorative rail aria-hidden |

| 018 | `Dataly - SaaS & Tech _ CTA Website Design Ideas.jpg` | Wide dark CTA banner with two violet glowing arcs at both edges, small eyebrow, centred headline + subtext + violet gradient pill button | Edge-glow CTA band | **B** | homepage / services CTA band | Very close to our identity: static violet radial gradients, --grad-brand button, bilingual copy; reject "free trial" and any numeric claim; no animation on mobile |

| 019 | `Faizur Rehman (@fazurrehman) on X (1).jpg` | Faizur footer: rounded white panel, giant cropped lowercase "faizur" wordmark, compact Explore/Follow/Call/Courses link columns, tiny bottom meta row | Oversized cropped wordmark as footer hero + compact link columns | **B** | footer | Subtle low-opacity CODE & CANVAS band + grouped links; must remain bilingual and keep the legal registration row + install button; drop the fake clock/weather widget |

| 020 | `Faizur Rehman (@fazurrehman) on X.jpg` | Exact duplicate of 019 (same Faizur footer screenshot) | Duplicate | **C** | — | No new idea; recorded so the count stays honest |

| 021 | `Footer UI Design.jpg` | Acme footer: full-bleed green grass photo with torn-paper white top edge, logo+tagline left, 4 link columns, centred copyright | Photo footer + link columns | **C** | — | No licensed photography; dark navy footer is identity. Only the link-column grouping is reused (see 019) |

| 022 | `Footer Website UI design.jpg` | Krafft: upper CTA ("Built for brands that mean business" + Get Quote), lower blue gradient footer with 4 link columns, newsletter field, social icons, huge Krafft wordmark + squircle logo | CTA-then-footer composition with big wordmark and newsletter | **B** | footer + CTA band | Combine with 018: a violet static-gradient footer, grouped bilingual links, our real newsletter form and a restrained oversized wordmark; no blue, no fabricated claims |

| 023 | `High Conversion Landing Page Design Ideas.jpg` | Purple lavender/sky landing page: floating bento cards of mixed sizes (write a story, story cards, "1,682,122" stat, collaborate, search pill), vertical icon toolbar | Bento grid of mixed-size glass cards | **C** | resources / insights (defer) | Needs licensed atmosphere imagery, drops the unevidenced stat, and requires owner approval; keep only the bento sizing idea |

| 024 | `How To Setup Ollama With N8n_ A Beginner's Guide To Workflow A…` | n8n/Ollama workflow diagram: pastel gradient, 3 white "Private" node cards joined by curved lines to a glowing orb | Node/flow diagram with curved connectors | **C** | services integration diagram (defer) | No real workflow product to document; would be decorative. Curved-connector motif could be reused inside the 017 timeline |

| 025 | `How to create a great Design System for your brand.jpg` | "Brand Thinking" Venn: three overlapping thin circles labelled 01 Strategy / 02 Design / 03 Growth, ghost title, dotted rings | Three-circle Venn for the three pillars | **B** | homepage positioning / methodology | Excellent conceptual fit for Brand / Product / System; CSS-only circles, numbered bilingual labels, ghost heading, RTL-safe; no stock vector |

| 026 | `Image Gallery Stacked as Narrow Slits and Expands to Show The …` | GIF: image gallery as narrow vertical slits; clicking a slit expands it to a full rounded image, circular icon buttons at each strip base | Slit/accordion gallery expanding on click | **B** | work / case-study art gallery | Simplify to a 3-slit CSS+small-JS accessible accordion using our own illustrative WebP; keyboard + aria-expanded; reduced-motion; no autoplay GIF |

| 027 | `Keep It Clean and Beautiful with Free Minimalist PowerPoint Te…` | Golden-circle diagram: cyan concentric glow, WHY / HOW / WHAT labels with thin connector lines, "Sets the golden circle" headline | Concentric-circle narrative with labelled callouts | **B** | about / methodology | Rebuild with our violet/teal static gradients, bilingual Why/How/What copy, logical connector lines; no fabricated metrics |

| 028 | `Lomen Ai Glass landing page.jpg` | Lomen AI Glass hero: three-tone headline (VISION. REIMAGINED. FUTURE.), thin nav, right-side vertical 01/02/03 section index, robot portrait, bottom floating 4-item feature bar | Right-side numbered section index + floating capability strip | **B** | long pages / services | Take the numeric section index and the glass feature strip; reject the AI-product copy and unlicensed robot render |

| 029 | `Meditation Mobile App by Bogdan Nikitin for Nixtio on Dribbble…` | Meditation app: two tilted phone mockups, warm orange gradients, portrait photos, "Tell us about yourself" checklist, circular progress slider | Onboarding checklist + curved slider | **C** | booking form (defer) | Health-app context and licensed portrait photography are off-identity; only the curved-progress control is a possible future cue |

| 030 | `Meeting App UI Design 📱✨_📝 Designed by_ @gautham_ui__👉 Follow …` | Meeting app cards: tall photo cards with gradient overlay caption and paired white primary / outlined ghost pill buttons | Full-bleed art card with overlay caption + paired CTAs | **B** | case-study cards | Use our illustrative WebP (no stock people), our --grad-brand primary + .btn--glass secondary, bilingual overlay copy |

| 031 | `MorniX - Online City Guide.jpg` | MorniX city guide: scattered floating cards (travel timeline, weather, book cover, audio waveform, best places, coordinates) over beige with giant ghost text | Scattered bento collage + ghost typography | **C** | — | Same family as 023; needs licensed photography and owner approval; no new mechanism |

| 032 | `Nike Year in Review _ Instrument.jpg` | Nike Year in Review: dark blurred blue field, horizontal flow of pill nodes with arrows and small green status dots | System/flow diagram with pill nodes | **C** | services "system" section (defer) | No verified architecture to document; decorative flow would imply a technical claim. Keep the curved connector cue for 017 |

| 033 | `OP (@openpurpose) on X.jpg` | Popcorn/OP minimal page: centred serif headline, tiny pill nav, Legal/Blogroom/Detail segmented micro-nav, three gradient-blur region cards with Get Plan links | Centred editorial headline + gradient-blur region cards | **B** | saudi-arabia / egypt market cards | Use our own WebP market art and .pill tokens; reject the serif (not in our font stack) and any "Get Plan" commerce link |

| 034 | `OpenAI launches professional services business with $4B invest…` | Coral/pink gradient: concentric ring lines with glass panels "Using skill / Summarize", "working…", "evaluating…", "Output Results.pdf" | Glass process panels over concentric rings | **C** | — | AI-agent workflow metaphor; decorative only. The concentric-ring motif is already covered by 013/027 |

| 035 | `Progress Bar.jpg` | "Total Project 374" stat card: +4,5% delta, blue gradient progress bar at 67% with marker, tick scale, bottom pill with counts | Gradient progress bar with tick scale | **D** | — | Every figure is fabricated; check-claims bans unevidenced numbers. The progress-bar visual is captured in 012 with honest usage |

| 036 | `Random designs - Collection Social Media - Pham Ngoc Anh.jpg` | "2023–2025 Random designs": three overlapping coloured cards fanned behind a front card with a screenshot collage | Fanned coloured card stack | **C** | — | Duplicate of the card-stack family (003/014); no new mechanism |

| 037 | `Smart Book Rental App – Design Process & Workflow.jpg` | "Behind the Design" process infographic: organic clover shape linking 4 circles (Research / Idea Sprint / Design Core / Design), each with a week pill and tag pills | Connected-circle process map | **B** | methodology process | Combine with 017: use our glass circles + numbered nodes, bilingual tags, DROP the "Week 01/02" duration claims; RTL-safe connectors |

| 038 | `Stunning Framer Template for Agencies (Free Portfolio Framer t…` | Framer agency template: centred "Curious What Else I've Created?" + See more Project pill, then a curved fan of 5 image tiles with tiny #01–#04 captions | Curved/fanned panorama of numbered project tiles | **B** | work / case studies | Strong fit: fan our own illustrative WebP tiles, numbered bilingual captions, static transforms only; no stock product photography |

| 039 | `Typography Music.jpg` | Spotify-style amber player: fanned album cover cards + glass playback control pill | Fanned media card stack | **D** | — | Third-party branding and licensed album art; fanned-stack idea already captured in 003/010/014 |

| 040 | `Week on Journal - summary card.jpg` | "Week on Journal" stacked summary cards: deck of white cards, app icon + avatar, big display numerals with up/down arrows and writing-time metrics | Stacked summary deck + large display numerals | **D** | — | All figures are fabricated metrics; claims gate would reject. The plain deck motif is already in 003 |

| 041 | `Wellness_ All-in-One UI Kit ( Components) by Kawsar Ahmed on D…` | Wellness UI kit: 3x4 bento grid of small white widget cards (trackers, circular charts, colour grids, audio, stats) | Bento widget grid / component gallery | **C** | defer | Marketing site has no dashboard to document; bento motif already logged in 023 |

| 042 | `X.jpg` | FORESS 1.0: blue-sky photo hero with huge "Disconnect to Connect.", white door rectangle, thin nav, bottom dark glass footer with 5 link columns | Atmospheric hero + dark glass footer columns | **C** | — | Requires licensed photography and a palette change; footer-column idea is covered by 019/022 |

| 043 | `download (1).jpg` | AUTONIX AI-agent hero: left headline + orange pill + black Book a Demo, centre sculpture portrait, floating "Discover" card and "98.4% Tasks Automated" stat, avatar rating, logo strip | Asymmetric hero with floating info cards | **D** | — | Fabricated 98.4% / 5000+ / 4.9 rating claims and an AI-product position we do not sell; floating-card cue already in 010 |

| 044 | `download (10).jpg` | AI-photo hero: a ring of rotated rounded-square image tiles around a centred headline, dark pill CTA, three feature columns | Circular orbit of tilted art tiles around centred copy | **B** | work / homepage intro | Great match for our existing .orbit__node: static (no 70s spin), our own illustrative WebP tiles, bilingual centre copy, reduced-motion safe |

| 045 | `download (11).jpg` | Two team profile cards with portrait photos, white bottom label plate (role + name), square icon button and circular + button | Profile card with label plate | **C** | team page (defer) | Needs licensed team photography; no verified people to publish yet |

| 046 | `download (12).jpg` | Dark AI chat bar with orange/blue glow border, "Ask anything…", mode chips (Normal / DeepThink / Voice) and gradient send button | Glowing command bar with mode chips | **D** | — | Fake AI assistant; chip-row styling already captured in 008 |

| 047 | `download (13).jpg` | Orchid page: upper band of blurred abstract gradient blobs, lower white area with "Meet Orchid, your personal exec.", small copy, dark pill CTA + text link | Static blurred-gradient hero band + clean copy block | **B** | hero background | Pre-render ONE static gradient WebP from our tokens (no runtime CSS blur, no mobile jank); reject the product copy |

| 048 | `download (14).jpg` | Kresna footer: rounded split card — blue gradient left (logo, tagline, socials) and light right (Navigation/Company columns, newsletter field), floating 3D app icon, giant ghost wordmark | Two-tone split footer card + newsletter + ghost wordmark | **B** | footer | Combine with 019/022 into one restrained dark-glass footer with grouped bilingual links, our real newsletter form and a low-opacity wordmark; no 3D app icon |

| 049 | `download (2).jpg` | Dark glass "Project Progress 65%" card: green→cyan gradient bar, due-date pill, collaborator avatars, More details button | Dark stat card with gradient progress bar | **D** | — | Fabricated percentage/date/people; licensing for avatars unavailable. Visual already covered by 012/035 |

| 050 | `download (3).jpg` | "Comfort / Home" white card: orange line chart with dashed crosshair and "11.3 kW" value pill | Line chart with tooltip pill | **D** | — | No real dataset; numeric value would be an unevidenced claim (same as 015) |

| 051 | `download (4).jpg` | Health weight chart: "118 lbs ↓32 lbs", green area chart, date marker, treatment options list, Continue button | Area chart with big value and CTA | **D** | — | Health/medical claims plus invented metrics; off-identity and unsafe to republish |

| 052 | `download (5).jpg` | Orange gradient "Step 4" journey: wavy vertical path with icon nodes on the left and a glass checklist panel on the right | Curved-path step timeline with side info panel | **B** | methodology process | Combine with 017/037: a static SVG curve (aria-hidden) plus numbered glass step cards; bilingual, RTL-mirrored path, no week/date claims |

| 053 | `download (6).jpg` | "Ensuring Your Peace of Mind" bento grid: mixed-size cards with 95% / $100M / 500K+ / 45% big numerals, photo and gradient panels | Bento grid with oversized display numerals | **C** | defer | All figures are fabricated; bento layout motif already logged in 023/041 |

| 054 | `download (7).jpg` | "03 Problem" infographic: radial sunburst semicircle, three labelled percentages on the left, four icon callout pills on the right | Radial sunburst with callout labels | **C** | decorative motif (defer) | Percentages claim unverified research; only the pure radial-sunburst shape could be reused as CSS decoration |

| 055 | `download (8).jpg` | "Unlock the power of your inventory": 2x2 explainer grid — glowing orb with 3 node circles, glass data card, "CURRENT PROCESS" step bar (Receive/Store/Fulfill/Ship) and a floating card | 2x2 explainer grid with a compact numbered step bar | **B** | services / methodology | Rebuild as our glass panels with bilingual steps; no invented inventory data; step bar uses logical inline flow for RTL |

| 056 | `download (9).jpg` | Ajrol Design System: three stacked browser sheets (Description / Date Picker / Spotlight) over a pastel gradient, black pill demo widget, feature list | Stacked documentation sheets | **C** | — | Design-system documentation page we do not publish; stacked-card motif already in 003/040 |

| 057 | `download.jpg` | Brak Instagram post: orange/red hero with "VISUALIZE YOUR MIND IN MOTION", 3 glass stat cards with charts and percentages, social post chrome (2/6, likes, comments) | Glass stat cards over a bold gradient | **D** | — | Fabricated cognitive metrics, unlicensed portrait and third-party social chrome |

| 058 | `hehe.jpg` | Growth chart card: orange curve Aug→Nov, glowing endpoint node and "+320% Monthly revenue" tooltip | Growth curve with tooltip pill | **D** | — | Invented revenue figure; claims gate would reject outright |

| 059 | `ui component.jpg` | Team dashboard: greeting, All/Active/Enrolled segmented control, "1,930 Total Members", gradient chart with 632 tooltip, bottom tab bar with + button | Dashboard with segmented control and bottom nav | **D** | — | No dashboard product; all numbers fabricated |

| 060 | `ui.jpg` | Two dark profile cards with portrait, name + verified badge, bio, follower counts and Follow button; right one has a gradient fade over the photo | Profile card with gradient overlay | **D** | — | Licensed portrait unavailable and follower counts are invented |

| 061 | `visual inspo AI idea.jpg` | Creativestyle minimal social card: rounded portrait card with "Connecting", avatar + 33m ago, "+ More Info" pill, a Minimalism Style tag and a promo QR code | Minimal social card with More Info pill | **D** | — | Third-party promo/QR + licensed portrait; no reusable honest idea |

| 062 | `Жми на ссылку и переходи на доску с промптами для нейросетей.j…` | Russian "PROMPTS" graphic: fanned photo cards with white outlines, frosted front plate with circular arrow, big word + 2025 pill | Fanned cards with frosted front plate | **C** | — | Duplicate of the card-stack family (003/010/014/038) with third-party photography |

| 063 | `Магия AI_ Читай в профиле.jpg` | Blue blurred gradient banner with tiny centred "20 Global Design Leader Summit 19" serif text | Blurred gradient banner + centred small type | **C** | — | Duplicate of 047; blue is off-palette and the year/award claim is unverified |


## 5. Guardrails applied to every B decision

- Rebuild with `--navy/--violet/--teal/--pink/--grad-brand`, 999px pills, `--r`/`--r-lg` and `--glass`; no orange, no bright cyan, no serif.

- `data-ar` / `data-ar-label` / `data-ar-html` for every visible string; logical properties; RTL connectors mirror; zero `data-ar*` leftovers.

- No runtime `filter: blur`, `backdrop-filter` heaviness, `will-change` or always-on animation at ≤720px; `prefers-reduced-motion` respected.

- No unevidenced number, percentage, date, rating, client name or outcome. No third-party portrait, logo, screenshot, font or CDN.

- Changes go through `partials/` + generator helpers, then `npm run generate`; **no hand-edited generated HTML**.

- Proof: `npm run gate` (**706 tests** after Phase 2), `npm run verify:api` (23/23), `npm run audit:content` (0 blockers), EN/AR 320/390/1440 dark/light visual QA, no-reduced-motion pass and mobile jank check.

## 6. Implementation results (this pass)

Six adapted ideas were rebuilt from scratch with our own tokens and copy. **No reference image, third-party portrait, logo, font, CDN or stock vector was published.** The 63 REF screenshots stay in `main/REF` as reference material only.

| # | Implemented | Refs | Files |
| --- | --- | --- | --- |
| 1 | **Studio-system section on `/`** — clipped ghost `CANVAS` wordmark, announcement pill, three overlapping glass circles (Brand / Product / System) with bilingual numbered labels, a four-step delivery rail and a static edge-glow CTA band | 002, 005, 006, 011, 013, 018, 019, 025, 028, 037, 052, 055 | `index.html`, `assets/css/home.css` |
| 2 | **Footer ghost wordmark** — restrained, clipped, decorative, dark/light variants; the grouped link columns, legal registration row and install button are preserved | 019, 022, 048 | `partials/bottom.html`, `assets/css/ds.css` |
| 3 | **CSS-only scroll-snap rail** for the 15 case-study cards at ≤720px — keyboard-reachable `role="region"` with a bilingual label, visible focus ring, SWIPE hint, no library and no scroll listener | 001, 038, 044 | `scripts/lib/pages_case_studies.py`, `assets/css/case-study.css` |
| 4 | **Announcement pill variant** (`.eyebrow--new` with a teal status dot) | 002 | `assets/css/home.css` |
| 5 | **Site-wide light-theme WCAG pass** — dark accent inks for teal/pink/gold/violet labels on light panels, a solid active-filter background, and dark teal for `/work/` disclaimers, status pills, case labels/CTAs and the new system accents. Bright brand tokens are untouched on dark surfaces | side effect of refs 019/022 light variants | `assets/css/ds.css`, `assets/css/home.css`, `assets/css/live.css`, `assets/css/case-study.css` |
| 6 | **Keyboard-focusable scrollable tables** found by the same sweep: the service-tracks and traceability-matrix wrappers are now named `role="region"` regions with `tabindex="0"` and bilingual labels | a11y sweep | `scripts/lib/pages_services.py`, `scripts/lib/pages_methodology.py`, `assets/css/ds.css` |
| 7 | **Acceptance tests** — 320/390/1440 × EN/AR × dark/light, one H1, no overflow, zero `data-ar*` leftovers in the AR twin, snap-rail contract, 4 home axe variants, plus a 36-page light-theme axe matrix | — | `tests/ref-system.spec.mjs`, `tests/light-contrast.spec.mjs` |

### Deliberately not implemented (and why)
- **Phase 1:** slit/expand gallery (026), orbit art tiles (044), bento grids (023/041), palette showcases (004/016) and profile cards (045/060) were not shipped because they appeared to need licensed imagery or an owner decision. **Phase 2 revisited the mechanisms only** on `/system/` — see §7 — without promoting any `C` source to an asset: no licensed photo, client screenshot, team portrait or dashboard dataset was added. AI/crypto/health dashboards (008/029/043/046/059), every numeric stat/chart (035/049–054/057/058), runtime blur/WebGL and third-party portraits/logos remain rejected.
- **No A decisions:** zero files were adopted as-is. Phase 1's six shipped items and Phase 2's five adapted mechanisms are `B`-style rebuilds — the idea, never the pixels.

### Verification (Phase 1 final; Phase 2 results in §7)
- `npm run generate` → `npm run check`: 157 HTML files · 0 problems · generator parity 159 outputs · `check-claims` ok on 153 pages · media 29/58/50.
- **`npm run gate`: 688 passed (15.9 m), 0 failed**, including the 8 new REF/light-theme tests and `npm run build` (47 redirects + PWA headers in `dist/`).
- `npm run verify:api`: **23/23** checks passed. `npm run audit:content`: **153 pages / 110 findings / 0 blockers / `[claims] 0` / `[provenance] 32`**; 444 `<img>` / 74 eager / 0 missing alt, dimensions, loading or AR alt.
- Custom browser QA: 8 EN/AR × dark/light × 390/1440 combinations → **0 problems**; `/work/` at 390 → `display:flex`, `scroll-snap-type: inline mandatory`, 15 cards, `role=region`, `tabindex=0`, no overflow.
- No-reduced-motion QA at 390px EN/AR × dark/light on `/` and `/work/`: **0 problems** — no infinite animation, no always-on blur/`backdrop-filter` on the new components.
- Light-theme axe matrix: **36 pages (18 EN + 18 AR) · 0 violations** across WCAG 2 A/AA and 2.1 AA.
- Visual review: EN dark and light at 1440/390, AR light 390, footer wordmark, `/work/` snap rail in both themes — all read correctly in LTR and RTL. Fixed floating nav/skip-link overlays at the top of scrolled section crops are expected, not layout regressions.
- Full Phase 1 gate/API/audit results are also recorded in `docs/CONTENT-AUDIT-2026-11.md` §F. Phase 2 supersedes the *counts* in §7.

---

## 7. Phase 2 — `/system/` (identity-safe adaptation, 2026-11-09)

The owner said **"Phase 2 يلا"** without supplying licensed photography, client screenshots, real dashboard data or an explicit `C`-item approval. Phase 2 therefore stayed on the safe path: a new bilingual documentation route that adapts **only mechanisms** from the deferred references, using first-party content that already exists in this repository. No owner decision was invented, and no `C` item was silently reclassified as approved.

### 7.1 What shipped

| # | Mechanism | Refs | Rebuild | Evidence rule |
| --- | --- | --- | --- | --- |
| 1 | Palette / token cards | 004, 016 | Six cards showing `ds.css` values (`#00001e`, `#8b6cff`, `#3fd6c4`, `#ee5ba3`, `#f3c77a`, `--grad`) with a copy button and a live status | Values are read from our own stylesheet, not the references' hex palettes; the page says so explicitly |
| 2 | Bento component gallery | 023, 041 | Six cards documenting glass, buttons, ring, numbered rail, CSS ghost type and labelled status | Real site components, no foreign headline, no oversized fabricated numerals |
| 3 | Real-data inventory | 041 | Six counts computed **at generation time**: `len(SERVICES)=23`, `len(TRACKS)=4`, `len(CASE_STUDIES)=15`, `len(FOUNDER_WORK)=25`, 2 founders, 2 local market pages | No percentages, growth, revenue, chart, tooltip or business KPI. A caption states the source of every number |
| 4 | Slit / accordion gallery | 026 | Four native `<details name="sys-slit">` panels, keyboard-operable, each showing one existing labelled illustrative WebP | CSS-only; no scroll listener, no animation, no library; every caption repeats `ILLUSTRATIVE / NOT CLIENT WORK` |
| 5 | Static orbit of tilted art tiles | 044 | Eight existing first-party case-study WebP tiles around a central bilingual statement, tilted with CSS `rotate()` only | No runtime orbit animation, WebGL, AI-photo claim or product positioning; at ≤720px it becomes a plain 2-column grid |
| 6 | Founder label plates | 045 | Two monogram plates (`AB`, `MA`) with real bilingual names, roles and leads from `pages_team.py` | No stock portrait, follower count, verified badge or gradient-over-photo effect; **REF 060 stays rejected** |

Supporting changes: `/system/` + `/ar/system/` generated from `scripts/lib/pages_system.py`; `assets/css/system.css`; `assets/js/system.js` (clipboard with a synchronous fallback and an AR/EN live region); a home `#system` cross-link; a footer link; `/design-system/` → `/system/` redirects; sitemap / `manus-routes.json` / `vercel.json` / `.htaccess` entries; `tests/phase2.spec.mjs`; `/system/` added to `check-claims`, `verify-live`, the accessibility, light-contrast and visual matrices. The OG card is the existing `resources.png` — no new OG bitmap.

### 7.2 Still pending (owner decisions, unchanged)

- Licensed photography or **client screenshots** for the fanned/slit gallery (026) and orbit tiles (044) — the shipped versions deliberately use our own labelled illustrative art.
- **Real team portraits** for profile cards (045) — the shipped plates use monograms and real roles.
- A **real-data dashboard** (008/029/043/046/059) — none was built; the inventory counts are generator-derived documentation, not a dashboard or a KPI claim.
- Any palette/token showcase tied to the references' own colour sets (004/016) — we document our own tokens only.
- REF 060 (portrait + follower counts + verification badge) and every fabricated metric remain rejected.

### 7.3 Verification (Phase 2)

- `npm run generate` + `npm run check` → 159 HTML / 0 problems / parity 161 / claims 155 pages / media 29-58-50.
- `npm run gate` → **706 passed, 0 failed (12.2 m)**, including 6 new `/system/` tests and `npm run build` (48 redirect rules, 52 `RewriteRule` lines, PWA headers).
- `npm run verify:api` → 23/23. `npm run audit:content` → 155 pages / 110 findings / **0 blockers** / `[claims] 0` / `[provenance] 32` / 472 `<img>` / 74 eager / 0 missing alt-dim-loading-AR-alt.
- Browser QA: 12 EN/AR × dark/light × 320/390/1440 `/system/` combinations → one H1, no overflow, 6/6/6/4/8/2 component counts, zero AR `data-ar*` leftovers, zero external images/CSS/JS, zero infinite animation, zero runtime blur; 10 no-reduced-motion route/theme combinations → 0 problems; 38-page light axe matrix + 4 `/system/` axe variants → 0 violations.
- Visual review of tokens, bento, inventory, slit gallery, orbit, founder plates, EN dark 1440, EN/AR light/dark 390 — read correctly in LTR and RTL. Screenshots remain in ignored `.qa-ref/p2-*.png`.
- No PR, merge or deploy was performed; publication remains approval-gated by `docs/PUBLISH-GATE.md`.
