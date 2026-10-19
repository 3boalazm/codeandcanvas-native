#!/usr/bin/env node
/* ==========================================================================
   make-htaccess.mjs — writes an Apache / LiteSpeed .htaccess (Hostinger)
   from _redirects, mirroring what vercel.json does on Vercel: legacy 301s,
   404 page, HTTPS + apex, security and cache headers.

   Usage (called by build.sh):
     node scripts/make-htaccess.mjs _redirects dist/.htaccess
   ========================================================================== */
import { readFileSync, writeFileSync } from 'node:fs';

const [src, out] = process.argv.slice(2);
const esc = (s) => s.replace(/[.+?^${}()|[\]\\]/g, '\\$&');
const seen = new Set();
const rules = [];

for (const raw of readFileSync(src, 'utf8').split(/\r?\n/)) {
  const line = raw.trim();
  if (!line || line.startsWith('#')) continue;
  const [from, to, status = '301'] = line.split(/\s+/);
  if (from === '/*' || from === '/index.html') continue; // handled separately
  let path = decodeURIComponent(from).replace(/^\//, '');
  let pattern;
  if (path.endsWith('/*')) pattern = '^' + esc(path.slice(0, -2)) + '(/.*)?$';
  else pattern = '^' + esc(path.replace(/\/$/, '')) + '/?$';
  if (seen.has(pattern)) continue;
  seen.add(pattern);
  rules.push(`RewriteRule ${pattern} ${to} [R=${status},L,NE]`);
}

const htaccess = `# Generated from _redirects for Hostinger (LiteSpeed/Apache)
Options -Indexes
DirectoryIndex index.html
DirectorySlash On
ErrorDocument 404 /404.html
AddDefaultCharset UTF-8
AddType image/svg+xml .svg
AddType font/woff2 .woff2
AddType application/manifest+json .webmanifest

<IfModule mod_rewrite.c>
RewriteEngine On

# Force HTTPS
RewriteCond %{HTTPS} !=on
RewriteCond %{HTTP:X-Forwarded-Proto} !https
RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [R=301,L,NE]

# www -> apex
RewriteCond %{HTTP_HOST} ^www\\.(.+)$ [NC]
RewriteRule ^ https://%1%{REQUEST_URI} [R=301,L,NE]

# Hide the Git checkout that Hostinger's Git deploy leaves in public_html
RewriteRule (^|/)\\.git(/|$) - [R=404,L]

# /index.html -> /
RewriteCond %{THE_REQUEST} \\s/index\\.html[\\s?]
RewriteRule ^index\\.html$ / [R=301,L]

# Legacy WordPress URLs -> native routes
${rules.join('\n')}
</IfModule>

<IfModule mod_headers.c>
Header always set X-Content-Type-Options "nosniff"
Header always set X-Frame-Options "SAMEORIGIN"
Header always set Referrer-Policy "strict-origin-when-cross-origin"
Header always set Permissions-Policy "camera=(), microphone=(), geolocation=()"
<FilesMatch "\\.html$">
Header set Cache-Control "public, max-age=0, must-revalidate"
</FilesMatch>
<FilesMatch "\\.(woff2?|ttf|otf)$">
Header set Cache-Control "public, max-age=31536000, immutable"
</FilesMatch>
<FilesMatch "\\.(css|js|svg|png|jpe?g|webp)$">
Header set Cache-Control "public, max-age=3600, stale-while-revalidate=86400"
</FilesMatch>
</IfModule>

<IfModule mod_deflate.c>
AddOutputFilterByType DEFLATE text/html text/css application/javascript text/javascript application/json image/svg+xml text/xml application/xml text/plain
</IfModule>
`;
writeFileSync(out, htaccess);
console.log(`${rules.length} redirect rules written to ${out}`);
