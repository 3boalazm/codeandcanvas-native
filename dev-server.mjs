// Zero-dependency static server for local development: `npm run dev` → http://localhost:3000
// Mirrors the production host: `/path/` → `/path/index.html`, unknown paths → `/404.html` (HTTP 404).
import { createServer } from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import { extname, join, normalize, resolve, sep } from 'node:path';

const root = resolve(process.argv[2] || '.');
const port = Number(process.env.PORT) || 3000;
const types = {
  '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.mjs': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp',
  '.woff2': 'font/woff2', '.ttf': 'font/ttf', '.ico': 'image/x-icon', '.xml': 'application/xml; charset=utf-8', '.txt': 'text/plain; charset=utf-8',
};

// `_redirects` (Netlify/Cloudflare syntax) is honoured so legacy WordPress URLs behave like production.
async function loadRedirects() {
  const text = await readFile(join(root, '_redirects'), 'utf8').catch(() => '');
  return text.split('\n').map((l) => l.trim()).filter((l) => l && !l.startsWith('#')).map((l) => l.split(/\s+/)).filter((p) => p.length >= 2 && p[0] !== '/*');
}
const redirects = await loadRedirects();
const matchRedirect = (path) => redirects.find(([from]) => (from.endsWith('/*') ? path.startsWith(from.slice(0, -1)) : from === path || decodeURIComponent(from) === path));

createServer(async (req, res) => {
  try {
    const url = new URL(req.url, 'http://x');
    const path = decodeURIComponent(url.pathname);
    if (path.split('/').some(part => part.startsWith('.')) || /^\/(?:node_modules|scripts|tests|docs|partials|test-results|playwright-report)(?:\/|$)/.test(path)) { res.writeHead(403, { 'Content-Type': 'text/plain' }); return res.end('Forbidden'); }
    const r = matchRedirect(path);
    if (r && r[1] !== path) { res.writeHead(Number(r[2]) || 301, { Location: (() => { const u = new URL(r[1], 'http://x'); url.searchParams.forEach((v, k) => { if (!u.searchParams.has(k)) u.searchParams.append(k, v); }); return u.pathname + u.search + u.hash; })() }); return res.end(); }
    let file = normalize(join(root, path));
    if (file !== root && !file.startsWith(root + sep)) throw new Error('outside root');
    if ((await stat(file).catch(() => null))?.isDirectory()) {
      if (!path.endsWith('/')) { res.writeHead(301, { Location: `${path}/${url.search}` }); return res.end(); }
      file = join(file, 'index.html');
    }
    const body = await readFile(file);
    res.writeHead(200, { 'Content-Type': types[extname(file)] || 'application/octet-stream', 'Cache-Control': 'no-cache' });
    res.end(body);
  } catch {
    const body = await readFile(join(root, '404.html')).catch(() => 'Not found');
    res.writeHead(404, { 'Content-Type': typeof body === 'string' ? 'text/plain; charset=utf-8' : 'text/html; charset=utf-8' });
    res.end(body);
  }
}).listen(port, '0.0.0.0', () => console.log(`Serving ${root} at http://localhost:${port}`));
