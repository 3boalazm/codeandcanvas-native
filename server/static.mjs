/* ==========================================================================
   static.mjs — serve the built site the way the host serves it.

   `npm run dev` serves the source tree, which is convenient but different from
   production: no trailing-slash directory resolution, no .htaccess rewrites, no
   /404.html fallback. That difference is exactly where a post-deploy verification
   can disagree with a local run, so this server serves dist/ with the
   production rules (LiteSpeed/Apache semantics from dist/.htaccess):

     • /path  → /path/ (301) when a directory exists
     • /path/ → /path/index.html
     • legacy redirects from _redirects
     • unknown path → 404.html with status 404
     • .git is never served

     node server/static.mjs            # http://localhost:8080
     CC_STATIC_PORT=9000 node server/static.mjs

   No compression, no caching layer: this is a verification target, not a CDN.
   ========================================================================== */
import { createServer } from 'node:http';
import { readFileSync, existsSync, statSync } from 'node:fs';
import { join, extname, normalize } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(fileURLToPath(new URL('../', import.meta.url)), 'dist');
const PORT = Number(process.env.CC_STATIC_PORT || 8080);

const TYPES = {
  '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8', '.mjs': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8', '.webmanifest': 'application/manifest+json',
  '.webp': 'image/webp', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
  '.svg': 'image/svg+xml', '.ico': 'image/x-icon', '.woff2': 'font/woff2', '.woff': 'font/woff',
  '.txt': 'text/plain; charset=utf-8', '.xml': 'application/xml', '.ics': 'text/calendar',
};

/* dist/_redirects lines: "from  to  status" — the same rules build.sh turns into
   .htaccess. Only literal rules are used here (patterns with :params or * are the
   host's job and are not part of this verification target). */
const REDIRECTS = (() => {
  const file = join(ROOT, '_redirects');
  if (!existsSync(file)) return [];
  return readFileSync(file, 'utf8').split('\n')
    .map((l) => l.trim()).filter((l) => l && !l.startsWith('#'))
    .map((l) => l.split(/\s+/))
    .filter((p) => p.length >= 2 && !/[:*]/.test(p[0]))
    .map(([from, to, status]) => ({ from, to, status: Number(status) || 301 }));
})();

const NOT_FOUND = join(ROOT, '404.html');

function send(res, status, body, type, extra = {}) {
  res.writeHead(status, { 'Content-Type': type, 'Cache-Control': 'no-cache', ...extra });
  res.end(body);
}

createServer((req, res) => {
  const url = new URL(req.url, 'http://localhost');
  let path = decodeURIComponent(url.pathname);
  if (path.includes('..') || /(^|\/)\.git(\/|$)/.test(path)) return send(res, 404, 'not found', 'text/plain');

  // /api/* belongs to the Node service; make the static target say so loudly
  // instead of answering with the SPA-ish 404 page.
  if (path.startsWith('/api/')) return send(res, 501, JSON.stringify({ ok: false, error: 'static target has no API' }), TYPES['.json']);

  /* _redirects is generated with both spellings, but Hostinger's Apache rules
     are written as ^slug/?$ — i.e. either spelling matches. Mirror that. */
  const bare = path.replace(/\/$/, '') || '/';
  const hit = REDIRECTS.find((r) => r.from === path || r.from === bare || r.from === bare + '/');
  if (hit) return send(res, hit.status, '', 'text/plain', { Location: hit.to });

  const file = normalize(join(ROOT, path));
  if (!file.startsWith(ROOT)) return send(res, 404, 'not found', 'text/plain');

  if (existsSync(file)) {
    const st = statSync(file);
    if (st.isDirectory()) {
      if (!path.endsWith('/')) return send(res, 301, '', 'text/plain', { Location: path + '/' });
      const index = join(file, 'index.html');
      if (existsSync(index)) return send(res, 200, readFileSync(index), TYPES['.html']);
    } else if (!path.endsWith('/')) {
      const type = TYPES[extname(file).toLowerCase()] || 'application/octet-stream';
      return send(res, 200, readFileSync(file), type);
    }
  }
  return send(res, 404, existsSync(NOT_FOUND) ? readFileSync(NOT_FOUND) : 'not found', TYPES['.html']);
}).listen(PORT, '0.0.0.0', () => {
  console.log(`static target: ${ROOT} on http://localhost:${PORT} · ${REDIRECTS.length} literal redirect rule(s)`);
});
