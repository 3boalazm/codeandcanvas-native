// Zero-dependency static server for local development: `npm run dev` → http://localhost:3000
// Mirrors the production host: `/path/` → `/path/index.html`, unknown paths → `/404.html` (HTTP 404).
import { createServer } from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import { extname, join, normalize, resolve } from 'node:path';

const root = resolve(process.argv[2] || '.');
const port = Number(process.env.PORT) || 3000;
const types = {
  '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.mjs': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp',
  '.woff2': 'font/woff2', '.ttf': 'font/ttf', '.ico': 'image/x-icon', '.xml': 'application/xml; charset=utf-8', '.txt': 'text/plain; charset=utf-8',
};

createServer(async (req, res) => {
  try {
    const path = decodeURIComponent(new URL(req.url, 'http://x').pathname);
    let file = normalize(join(root, path));
    if (!file.startsWith(root)) throw new Error('outside root');
    if ((await stat(file).catch(() => null))?.isDirectory()) {
      if (!path.endsWith('/')) { res.writeHead(301, { Location: `${path}/` }); return res.end(); }
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
