# «الفاتورة التانية» — Code & Canvas campaign

**The hidden cost of cheap development.** Five posts, one idea: the money you "save" at the start
comes back as a second invoice — in rebuilds, migrations, and new teams that pay to understand code
nobody designed.

This is a second, independent campaign (not a sequel post-set) built for the same brand with a
**different visual system** from `../from-idea-to-market`.

---

## The five posts

| # | Beat | Headline | Kind |
|---|---|---|---|
| 01 | الادعاء | الرخيص **مش رخيص.** | photo — receipt |
| 02 | التفصيل | 3 فواتير **بتوصل بعدين.** | type — ledger |
| 03 | السبب | كل ترقيع **بيغلي اللي بعده.** | photo — cracked wall |
| 04 | المقارنة | الأغلى إنك تعمله **مرتين.** | photo — rebuild site |
| 05 | الخطوة | قبل ما تدفع **المرة التانية.** | photo — laptop at night |

Every post ships in two formats — feed `1080×1350` and story `1080×1920` — plus an Egyptian-Arabic
caption, an English caption, hashtags, a first comment, and alt text.

---

## Files

| Path | What it is |
|---|---|
| `render.py` | The renderer. `python3 render.py [feed\|story] [1..5]` → `assets/feed`, `assets/story` |
| `typeset.py` | HarfBuzz + FreeType shaping/rasterising (Arabic joining, bidi script runs) |
| `captions.md` | **Source of truth for the copy** — AR + EN, hashtags, comments, alt text, schedule |
| `build_board.py` | Parses `captions.md` → builds `index.html` (the campaign board) |
| `index.html` | The board: idea, arc, all five posts with their captions, design system, schedule |
| `assets/photos/*.jpg` | Four conceptual photographs (AI, no people claiming to be clients) |
| `assets/feed/*.png` · `assets/story/*.png` | The ten deliverables |
| `assets/brand/` | Vendored fonts (Alexandria VF, IBM Plex Sans Arabic) + logo, OFL licences |
| `campaign-overview.png` | Contact sheet — all ten designs on one canvas |
| `campaign-kit.zip` | Everything above in one archive, for Drive / client hand-off |

---

## Design system (v1 of this campaign)

Deliberately *not* the first campaign's look:

- **Split composition.** Type lives on a quiet near-black panel on top (600px feed / 880px story),
  photography owns the band below, and a 3px brand gradient is the only thing on the seam. The
  headline never sits on the photo, so nothing is fighting the image.
- **Bigger, tighter type.** Alexandria 800 at up to **116px** (feed) / **130px** (story), leading
  **1.12** — the words are the artwork. The first campaign used 94/106 at 1.34.
- **Warm duotone.** Photos are colourised to `#09070C → #ECE0C6` (bone) instead of the earlier cool
  violet/teal, then get a 13% accent tint, 2.0σ grain, and a scrim that melts the band into the panel.
- **Chrome = two elements.** Wordmark top-right, index `01 /05` top-left. No grid, no corner ticks,
  no footer rules, no series dots.
- **One device only.** The ledger on post 02 — three rows, number as a left column, hairline rules,
  title right-aligned. Everything else is type + photograph.

Layout constants: `PAD=76`, head fit cap `116/130`, support `23/26px @ α.62`, kicker `18px @ α.48`,
`gap_sup 44/52`, seam `600/880` (post 04 uses `+62` for its three-line headline).

---

## Build

```bash
pip install --break-system-packages pillow numpy fonttools uharfbuzz freetype-py
python3 render.py                 # all ten, ~60s at S=2 supersampling
python3 render.py story 3         # one format, one post
python3 build_board.py            # regenerate index.html from captions.md
```

Photos are duotoned at render time — the JPEGs in `assets/photos/` are the raw plates.

## Schedule

22 Nov → 1 Dec 2026, every other day, 8:00–9:30 pm Cairo/Riyadh. Post 03 carries the first paid
boost. Full table in `captions.md` and on the board.
