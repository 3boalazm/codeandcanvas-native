/* ==========================================================================
   Code & Canvas — app shell service worker.

   Goal: repeat visits and previously-opened pages behave like an installed app
   (instant, and usable with no connection) without ever serving stale content
   while a network is available.

   Policy
   · HTML navigation: network-first. A successful response is cached, so the
     same page reopens offline. Nothing is ever served from cache while the
     network works, so content updates are never held back.
   · Static assets (/assets/**, manifest, icons): stale-while-revalidate —
     instant from cache, refreshed in the background.
   · Never touched: /api/*, /crm/*, /_vercel/*, /build-info.json, non-GET and
     cross-origin requests. Forms, analytics and the lead pipeline always go
     straight to the network.
   · No clients.claim() and no skipWaiting(): an already-open tab is never
     hijacked by a newly installed worker.

   Bump VERSION when the cache policy or precache list changes. See docs/PWA.md.
   ========================================================================== */
'use strict';

const VERSION = 'cc-app-2026-11-10-1';
const SHELL = `${VERSION}-shell`;
const PAGES = `${VERSION}-pages`;
const ASSETS = `${VERSION}-assets`;
const ALL = new Set([SHELL, PAGES, ASSETS]);

/* A deliberately small first-install download. Everything else is learned at
   runtime, so installation never competes with the first page load. */
const CORE = [
  '/offline.html',
  '/manifest.webmanifest',
  '/',
  '/ar/',
  '/assets/css/ds.css',
  '/assets/css/fonts.css',
  '/assets/css/pages.css',
  '/assets/css/live.css',
  '/assets/css/home.css',
  '/assets/js/site.js',
  '/assets/js/home.js',
  '/assets/brand/app/icon-192.png',
];

const BYPASS = ['/api/', '/crm', '/_vercel/', '/build-info.json', '/sw.js'];

self.addEventListener('install', (event) => {
  event.waitUntil((async () => {
    const cache = await caches.open(SHELL);
    // allSettled: a single temporarily missing asset must not break installability.
    await Promise.allSettled(CORE.map((url) => cache.add(new Request(url, { cache: 'reload' }))));
  })());
});

self.addEventListener('activate', (event) => {
  event.waitUntil((async () => {
    for (const key of await caches.keys()) if (!ALL.has(key)) await caches.delete(key);
  })());
});

const cacheable = (response) =>
  response && response.ok && response.status === 200 && response.type === 'basic';

async function networkFirst(request, cacheName, offlineFallback) {
  const cache = await caches.open(cacheName);
  try {
    const response = await fetch(request);
    if (cacheable(response)) cache.put(request, response.clone()).catch(() => {});
    return response;
  } catch {
    const hit = await cache.match(request, { ignoreSearch: false });
    if (hit) return hit;
    if (offlineFallback) {
      const fallback = await caches.match(offlineFallback);
      if (fallback) return fallback;
    }
    return new Response('Offline', { status: 503, headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
  }
}

async function staleWhileRevalidate(request, event) {
  const cache = await caches.open(ASSETS);
  const hit = await cache.match(request);
  const update = fetch(request).then((response) => {
    if (cacheable(response)) cache.put(request, response.clone()).catch(() => {});
    return response;
  }).catch(() => null);
  if (hit) {
    // Refresh in the background; do not make the visitor wait for it, but keep
    // the worker alive long enough for the update to actually land in the cache.
    event.waitUntil(update);
    return hit;
  }
  return (await update) || new Response('Offline', { status: 503, headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
}

self.addEventListener('fetch', (event) => {
  const request = event.request;
  if (request.method !== 'GET') return;
  let url;
  try { url = new URL(request.url); } catch { return; }
  if (url.origin !== self.location.origin) return;
  if (BYPASS.some((prefix) => url.pathname.startsWith(prefix))) return;

  const wantsHtml = request.mode === 'navigate' ||
    (request.headers.get('accept') || '').includes('text/html');
  if (wantsHtml) {
    event.respondWith(networkFirst(request, PAGES, '/offline.html'));
    return;
  }
  if (url.pathname.startsWith('/assets/') ||
      url.pathname === '/manifest.webmanifest' ||
      /\.(?:png|jpe?g|webp|avif|svg|ico|woff2?|css|js)$/i.test(url.pathname)) {
    event.respondWith(staleWhileRevalidate(request, event));
  }
});
