# Code & Canvas as a mobile app (PWA)

Added 2026-11-09. The site is now **installable**: it opens in its own window with
no browser toolbar, has a home-screen icon and splash colours, and reopens the
pages a visitor has already seen even with no connection. It is still the same
static bilingual site — no framework, no native binary, no app-store listing.

## What ships

| File | Purpose |
| --- | --- |
| `manifest.webmanifest` | `display: standalone`, `start_url: /`, `scope: /`, navy `theme_color` / `background_color`, 4 PNG icons (`any` + `maskable`), 3 shortcuts (Work, Book a call, العربية). |
| `sw.js` | App-shell service worker, registered from `assets/js/site.js` **after `load`** so it never competes with the first paint. |
| `offline.html` | Self-contained bilingual fallback for a page that was never visited. |
| `assets/brand/app/*.png` | 192/512 `any` + 192/512 `maskable` + 180 `apple-touch-icon`, all rendered by `scripts/generate-app-icons.mjs` from `assets/brand/icon-white.svg`. |
| `partials/head.html` | `manifest`, `mobile-web-app-capable`, `apple-mobile-web-app-*`, `apple-touch-icon`. `arize.mjs` localises the iOS home-screen title on `/ar/` twins. |
| `partials/bottom.html` + `#installApp` | Hidden footer button, revealed only when the browser fires a real `beforeinstallprompt`. |
| `vercel.json` headers (generated in `scripts/gen-pages.py::meta_files()`) | `/sw.js` is `no-cache` with `Service-Worker-Allowed: /`; manifest gets the correct MIME type; `/offline.html` is `must-revalidate`. |
| `scripts/make-htaccess.mjs` → `dist/.htaccess` | The **Hostinger/Apache** deploy is the live one, so it also sets `AddType application/manifest+json .webmanifest`, a no-cache `sw.js` override with `Service-Worker-Allowed: /`, and a one-hour manifest cache. Without the override the generic `css\|js` rule would cache the worker for an hour and delay updates. |
| `dev-server.mjs`, `build.sh` | `.webmanifest` MIME type; root PWA files copied into `dist/`. |

## Install on a phone

- **Android / Chrome, Edge, Samsung Internet:** open `https://codeandcanvas.net/`, then use the browser's *Install app* / *Add to Home screen* menu, or the **Install app** button that appears in the footer once the browser confirms installability.
- **iOS / iPadOS / Safari:** tap Share → **Add to Home Screen**. iOS does not fire `beforeinstallprompt`, so the footer button stays hidden there; the `apple-touch-icon` and `apple-mobile-web-app-title` supply the icon and label.
- Desktop Chromium also supports installation; the same manifest is used.

## Caching policy (why it is safe)

- **HTML navigation → network-first.** While online, content is *always* fetched fresh; a copy is stored. A newly generated page is therefore visible immediately — no stale content is ever served from cache when the network works.
- **`/assets/**`, manifest and icons → stale-while-revalidate.** Instant from cache, refreshed in the background.
- **Never intercepted:** `/api/*`, `/crm/*`, `/_vercel/*`, `/build-info.json`, `/sw.js`, non-GET and cross-origin requests. Forms, consented analytics, booking and the lead pipeline always hit the network. **Nothing is cached from a form submission.**
- **Offline:** a visited page is served from the pages cache; an unvisited one shows `offline.html`. The install precache is deliberately tiny (~12 small files, added with `Promise.allSettled`, so one missing asset cannot break installation).
- No `clients.claim()` and no `skipWaiting()`: an already-open tab is never taken over by a newly activated worker.
- Bump `VERSION` in `sw.js` when the cache policy or precache list changes; `activate` deletes every cache from older versions.
- **CSS/JS are content-hashed (`?v=<sha256[:10]>`).** Asset URLs are stable by design, and this worker caches them by URL with stale-while-revalidate on top of a 1-hour CDN window. A stylesheet edit that kept its URL therefore reached returning visitors *after* the new markup — which is exactly how the home `/system/` band once rendered as unstyled text. `scripts/version-assets.mjs` now rewrites every CSS/JS reference in the partials and on every page after `sync-chrome.mjs`, so a changed file gets a new URL, a new cache entry and an immediate fetch. It is part of `npm run sync`, `npm run check` (as `version-assets --check`) and `scripts/check-generated.mjs`, and `scripts/check-asset-versioning.mjs` fails the build on any unversioned or stale-hash reference plus any drift between the `/system/` markup and its stylesheet.

## Verification

- `tests/pwa.spec.mjs` opts into `serviceWorkers: 'allow'` (the rest of the suite blocks workers to keep its assertions deterministic) and checks: manifest link + iOS chrome on EN and AR, Arabic home-screen title, valid manifest JSON, all icon URLs served, install button behaviour, worker activation, and **a real offline reload of a visited page**.
- `scripts/check-claims.mjs` fails the publish gate if any of the **150 pages that load `site.js`** loses the manifest/apple-icon links, or if a PWA asset is missing or the manifest is invalid. The three `noindex` private review surveys have standalone heads and never load the runtime, so they are intentionally not app pages.
- `/erp/` and `/ar/erp/` have their own head rather than `partials/head.html`. Adding the app chrome there also exposed a gap from the previous lap: their inline bootstrap set language/direction but **not the persisted light/dark choice**. It now sets `data-theme` and `theme-color` before first paint like the rest of the site.
- `npm run check` (157 HTML files, 0 problems; generator parity 159 outputs; claims ok on 153 pages), `npm run gate` (**680 passed / 17.6 m**, 4 of them new PWA tests), `npm run verify:api` (23/23) and `npm run audit:content` (0 blockers) are green; `dist/` contains the manifest, worker, offline page and all five icons.

## Limits / decisions still open

1. **First visit needs a connection.** Only `/`, `/ar/`, the offline page and a small core shell are precached; other pages become available offline after they are opened once.
2. **`theme_color` is dark navy** even when the visitor has chosen the light theme, because the manifest is a static file. A native-accurate status bar for light-mode users would need either a generated per-theme manifest or an owner decision to keep the branded navy splash.
3. **Lighthouse / real-device installability** (Android + iOS) has not been run on physical hardware in this environment; the checks above are browser-automation and static checks.
4. **No push notifications, background sync, or native wrapper (Capacitor/APK)** were added. If an actual store app is wanted, that is a separate project requiring an app-store account, signing keys and review.
5. **The install prompt is a measurement event** (`app-install-prompt`), emitted only through the existing first-party, consent-gated `CC.track` path. No new third-party script or identifier is introduced.
6. Release blockers in `docs/PUBLISH-GATE.md` are unchanged: installing the site as an app does not supply legal sign-off, licensed photography, permissioned client screenshots, or a production API/database.
