// Zero-dependency combined server for local development and the Arena live preview:
// static site (`npm run dev`) + first-party lead/booking/measurement API + Lead Desk.
// Production static hosting keeps the same HTML; deploy server/api.mjs behind the
// same origin (see docs/LEAD-PIPELINE.md). Binds 0.0.0.0 so the preview proxy works.
import { createServer } from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import { extname, join, normalize, resolve, sep } from 'node:path';
import { execFileSync } from 'node:child_process';
import { createApi } from './server/api.mjs';

const root = resolve(process.argv[2] || '.');
const port = Number(process.env.PORT) || 3000;
const types = {
  '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.mjs': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.avif': 'image/avif',
  '.woff2': 'font/woff2', '.ttf': 'font/ttf', '.ico': 'image/x-icon', '.xml': 'application/xml; charset=utf-8', '.txt': 'text/plain; charset=utf-8',
  '.ics': 'text/calendar; charset=utf-8', '.pdf': 'application/pdf',
};

const commit = (() => { try { return execFileSync('git', ['rev-parse', '--short', 'HEAD'], { cwd: root, stdio: ['ignore', 'pipe', 'ignore'] }).toString().trim(); } catch { return 'dev'; } })();
const api = createApi({ root, env: { ...process.env, CC_BUILD_COMMIT: commit } });
console.log(`[cc] lead pipeline: ${api.dataDir} · /crm/ · commit ${api.commit}`);
if (!process.env.CC_ADMIN_TOKEN) console.warn('[cc] CC_ADMIN_TOKEN is unset — using the review-only default. Set it before exposing this service.');

// `_redirects` (Netlify/Cloudflare syntax) is honoured so legacy WordPress URLs behave like production.
async function loadRedirects() {
  const text = await readFile(join(root, '_redirects'), 'utf8').catch(() => '');
  return text.split('\n').map((l) => l.trim()).filter((l) => l && !l.startsWith('#')).map((l) => l.split(/\s+/)).filter((p) => p.length >= 2 && p[0] !== '/*');
}
const redirects = await loadRedirects();
const matchRedirect = (path) => redirects.find(([from]) => (from.endsWith('/*') ? path.startsWith(from.slice(0, -1)) : from === path || decodeURIComponent(from) === path));

createServer(async (req, res) => {
  try {
    const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
    const path = decodeURIComponent(url.pathname);

    // Build fingerprint: lets scripts/production-verify.mjs prove which commit the host serves.
    if (path === '/build-info.json') {
      res.writeHead(200, { 'Content-Type': types['.json'], 'Cache-Control': 'no-store' });
      return res.end(JSON.stringify({ commit, service: 'codeandcanvas-native', generatedAt: new Date().toISOString(), mode: 'dev-preview' }));
    }

    if (path.startsWith('/api/') || path === '/crm' || path === '/crm/') {
      // createApi writes the response itself. Its helpers resolve to undefined,
      // so test the response state rather than a truthy return value; otherwise
      // a handled /api/ request would fall through to the static 404 handler and
      // crash the process with ERR_HTTP_HEADERS_SENT.
      await api.handle(req, res, url);
      if (res.headersSent || res.writableEnded) return;
    }

    if (path.split('/').some(part => part.startsWith('.')) ||
        /^\/(?:node_modules|scripts|tests|docs|partials|server|\.data|test-results|playwright-report)(?:\/|$)/.test(path)) {
      res.writeHead(403, { 'Content-Type': 'text/plain' }); return res.end('Forbidden');
    }
    const r = matchRedirect(path);
    if (r && r[1] !== path) {
      res.writeHead(Number(r[2]) || 301, { Location: (() => { const u = new URL(r[1], 'http://x'); url.searchParams.forEach((v, k) => { if (!u.searchParams.has(k)) u.searchParams.append(k, v); }); return u.pathname + u.search + u.hash; })() });
      return res.end();
    }
    let file = normalize(join(root, path));
    if (file !== root && !file.startsWith(root + sep)) throw new Error('outside root');
    if ((await stat(file).catch(() => null))?.isDirectory()) {
      if (!path.endsWith('/')) { res.writeHead(301, { Location: `${path}/${url.search}` }); return res.end(); }
      file = join(file, 'index.html');
    }
    const body = await readFile(file);
    res.writeHead(200, { 'Content-Type': types[extname(file)] || 'application/octet-stream', 'Cache-Control': 'no-cache' });
    res.end(body);
  } catch (err) {
    // Never attempt a second response after one has already been written.
    if (res.headersSent || res.writableEnded) return;
    if (/api|crm/.test(req.url || '')) {
      res.writeHead(500, { 'Content-Type': types['.json'] }); return res.end(JSON.stringify({ accepted: false, error: 'internal error' }));
    }
    const body = await readFile(join(root, '404.html')).catch(() => 'Not found');
    res.writeHead(404, { 'Content-Type': typeof body === 'string' ? 'text/plain; charset=utf-8' : 'text/html; charset=utf-8' });
    res.end(body);
  }
}).listen(port, '0.0.0.0', () => console.log(`Serving ${root} at http://localhost:${port}`));
