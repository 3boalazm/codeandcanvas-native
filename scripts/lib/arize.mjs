/* ==========================================================================
   arize.mjs — turns a finished English page into its standalone Arabic twin.

   The English HTML already carries the Arabic copy in `data-ar*` attributes
   (that is how the runtime language switch works). This module performs the
   same swap at build time, on the committed file, so `/ar/<route>/` is a real
   Arabic document: it reads and indexes correctly with JavaScript disabled.

   Rules kept deliberately literal to the runtime behaviour in assets/js/site.js:
     data-ar            → element text        (attribute value is already escaped)
     data-ar-html       → element markup      (entity-decoded, injected as HTML)
     data-ar-label      → aria-label / optgroup label
     data-ar-title      → title
     data-ar-alt        → alt
     data-ar-placeholder→ placeholder
   `.split` elements keep the word-by-word animation by rebuilding `.w` spans.
   ========================================================================== */

export const SITE = 'https://codeandcanvas.net';
const VOID = new Set(['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr']);
const ENTITIES = { '&lt;': '<', '&gt;': '>', '&quot;': '"', '&#39;': "'", '&apos;': "'", '&nbsp;': '\u00a0' };

const unescapeHtml = (s) => s.replace(/&(?:lt|gt|quot|apos|#39|nbsp);/gi, (m) => ENTITIES[m.toLowerCase()] ?? m).replace(/&amp;/gi, '&');

/** Absolute URL of the Arabic twin of an English route. */
export function arPathOf(path) {
  const clean = path === '/' ? '/' : path;
  return clean === '/' ? '/ar/' : `/ar${clean}`;
}

/** Share of Arabic letters among all letters in the page's main content (0–1). */
export function arabicShare(html) {
  const main = html.match(/<main[\s\S]*?<\/main>/) ?? [html];
  const text = main[0].replace(/<(script|style)[\s\S]*?<\/\1>/g, ' ').replace(/<[^>]+>/g, ' ');
  const ar = (text.match(/[\u0600-\u06FF]/g) ?? []).length;
  const lat = (text.match(/[A-Za-z]/g) ?? []).length;
  return ar + lat === 0 ? 0 : ar / (ar + lat);
}

/** Walk forward from `from` and return the index just past the element's close tag. */
function findClose(html, from, tag) {
  const re = new RegExp(`<(/?)${tag}(?=[\\s/>])([^>]*)>`, 'gi');
  re.lastIndex = from;
  let depth = 1;
  let m;
  while ((m = re.exec(html))) {
    if (m[1] === '/') {
      depth -= 1;
      if (depth === 0) return re.lastIndex;
    } else if (!/\/\s*$/.test(m[2]) && !VOID.has(tag.toLowerCase())) {
      depth += 1;
    }
  }
  return -1;
}

/** First opening tag after `from` that carries `attr="…"`, with its value. */
function findAttrTag(html, attr, from = 0) {
  const needle = `${attr}="`;
  let i = html.indexOf(needle, from);
  while (i !== -1) {
    if (/\s/.test(html[i - 1])) {
      const start = html.lastIndexOf('<', i);
      if (start !== -1 && start >= from && /^[a-zA-Z]/.test(html[start + 1])) {
        const tagName = html.slice(start + 1).match(/^[a-zA-Z][\w:-]*/)[0];
        let k = i + needle.length;
        const q = html.indexOf('"', k);
        if (q === -1) return null;
        const value = html.slice(k, q);
        k = q + 1;
        while (k < html.length && html[k] !== '>') {
          if (html[k] === '"') {
            const q2 = html.indexOf('"', k + 1);
            if (q2 === -1) break;
            k = q2 + 1;
            continue;
          }
          k += 1;
        }
        if (k >= html.length) return null;
        return { start, end: k + 1, tagName, value, openTag: html.slice(start, k + 1) };
      }
    }
    i = html.indexOf(needle, i + 1);
  }
  return null;
}

/** Replace the text (or markup) of every element carrying `attr`. */
function swapContent(html, attr, asHtml) {
  let out = html;
  let guard = 0;
  while (guard++ < 40000) {
    const hit = findAttrTag(out, attr);
    if (!hit) break;
    const tag = hit.tagName.toLowerCase();
    const value = asHtml ? unescapeHtml(hit.value) : hit.value;
    const openTag = hit.openTag.replace(new RegExp(`\\s${attr}="[^"]*"`), '');
    if (VOID.has(tag)) {
      out = out.slice(0, hit.start) + openTag + out.slice(hit.end);
      continue;
    }
    const close = findClose(out, hit.end, hit.tagName);
    if (close === -1) {
      out = out.slice(0, hit.start) + openTag + out.slice(hit.end);
      continue;
    }
    const inner = out.slice(hit.end, close);
    const closeTag = inner.slice(inner.lastIndexOf('</'));
    let body;
    if (asHtml) {
      body = value;
    } else if (/\bsplit\b/.test(openTag)) {
      body = value
        .split(/\s+/)
        .filter(Boolean)
        .map((w, i) => `<span class="w" style="--i:${i}">${w}</span>`)
        .join(' ');
    } else {
      body = value;
    }
    out = out.slice(0, hit.start) + openTag + body + closeTag + out.slice(close);
  }
  return out;
}

/** Copy an attribute's Arabic value onto its runtime destination attribute. */
function swapAttr(html, src, dst) {
  let out = html;
  let guard = 0;
  while (guard++ < 40000) {
    const hit = findAttrTag(out, src);
    if (!hit) break;
    let openTag = hit.openTag.replace(new RegExp(`\\s${src}="[^"]*"`), '');
    const value = hit.value;
    if (new RegExp(`\\s${dst}="`).test(openTag)) openTag = openTag.replace(new RegExp(`\\s${dst}="[^"]*"`), ` ${dst}="${value}"`);
    else openTag = openTag.replace(/>$/, ` ${dst}="${value}">`);
    if (hit.tagName.toLowerCase() === 'optgroup' && src === 'data-ar-label') openTag = openTag.replace(/\slabel="[^"]*"/, ` label="${value}"`);
    out = out.slice(0, hit.start) + openTag + out.slice(hit.end);
  }
  return out;
}

/** Text bound at runtime from a JS dictionary (the ERP proposal sheet). */
function resolveDict(html, dict) {
  const lookup = (path) => path.split('.').reduce((o, k) => (o ? o[k] : undefined), dict);
  const textOf = (raw) => (typeof raw === 'string' ? raw : raw && typeof raw === 'object' ? raw.ar ?? raw.en ?? '' : '');

  let out = html;
  for (let guard = 0; guard < 20000; guard += 1) {
    const hit = findAttrTag(out, 'data-t-title');
    if (!hit) break;
    const value = textOf(lookup(hit.value)).replace(/"/g, '&quot;');
    let openTag = hit.openTag.replace(/\sdata-t-title="[^"]*"/, '');
    openTag = /\stitle="/.test(openTag) ? openTag.replace(/\stitle="[^"]*"/, ` title="${value}"`) : openTag.replace(/>$/, ` title="${value}">`);
    openTag = /\saria-label="/.test(openTag) ? openTag.replace(/\saria-label="[^"]*"/, ` aria-label="${value}"`) : openTag.replace(/>$/, ` aria-label="${value}">`);
    out = out.slice(0, hit.start) + openTag + out.slice(hit.end);
  }

  for (let guard = 0; guard < 20000; guard += 1) {
    const hit = findAttrTag(out, 'data-t');
    if (!hit) break;
    const value = textOf(lookup(hit.value));
    const openTag = hit.openTag.replace(/\sdata-t="[^"]*"/, '');
    const tag = hit.tagName.toLowerCase();
    const close = VOID.has(tag) ? -1 : findClose(out, hit.end, hit.tagName);
    if (close === -1) {
      out = out.slice(0, hit.start) + openTag + out.slice(hit.end);
      continue;
    }
    const inner = out.slice(hit.end, close);
    const closeTag = inner.slice(inner.lastIndexOf('</'));
    const body = /\bsplit\b/.test(openTag)
      ? value.split(/\s+/).filter(Boolean).map((w, i) => `<span class="w" style="--i:${i}">${w}</span>`).join(' ')
      : value;
    out = out.slice(0, hit.start) + openTag + body + closeTag + out.slice(close);
  }
  return out;
}

const strip = (html, attr) => {
  let out = html;
  let guard = 0;
  while (guard++ < 40000) {
    const hit = findAttrTag(out, attr);
    if (!hit) break;
    out = out.slice(0, hit.start) + hit.openTag.replace(new RegExp(`\\s${attr}="[^"]*"`), '') + out.slice(hit.end);
  }
  return out;
};

/** `/pricing-faq/` → `/ar/pricing-faq/`; assets, API calls, anchors and externals are untouched. */
function arHref(ref) {
  if (!ref.startsWith('/') || ref.startsWith('//')) return ref;
  if (/^\/(assets|api)\//.test(ref)) return ref;
  if (/\.(svg|png|jpe?g|webp|avif|gif|ico|xml|txt|json|pdf|webmanifest|woff2?)$/i.test(ref)) return ref;
  const [base, ...rest] = ref.split('#');
  const [path, query] = base.split('?');
  if (path === '/ar/' || path.startsWith('/ar/')) return ref;
  const target = path === '/' || path === '' ? '/ar/' : `/ar${path}`;
  return `${target}${query ? `?${query}` : ''}${rest.length ? `#${rest.join('#')}` : ''}`;
}

function rewriteLinks(html) {
  return html.replace(/\s(href|action)="(\/[^"]*)"/g, (m, name, ref) => ` ${name}="${arHref(ref)}"`);
}

function localizeJsonLd(graph, enPath, arPath) {
  const enUrl = SITE + enPath;
  const arUrl = SITE + arPath;
  const walk = (node) => {
    if (Array.isArray(node)) return node.map(walk);
    if (!node || typeof node !== 'object') return node;
    const out = {};
    for (const [k, v] of Object.entries(node)) {
      if (k === 'inLanguage' && (v === 'en' || (Array.isArray(v) && v.length === 1 && v[0] === 'en'))) out[k] = 'ar';
      else if (node['@type'] === 'WebPage' && k === 'name' && titleArRef) out[k] = titleArRef;
      else if (node['@type'] === 'WebPage' && k === 'description' && descArRef) out[k] = descArRef;
      else if (typeof v === 'string' && v.startsWith(enUrl)) out[k] = arUrl + v.slice(enUrl.length);
      else out[k] = walk(v);
    }
    return out;
  };
  return walk(graph);
}

function localizeLd(chunk) {
  return chunk.replace(/(<script type="application\/ld\+json">)([\s\S]*?)(<\/script>)/g, (block, open, json, close) => {
    try {
      return open + JSON.stringify(localizeJsonLd(JSON.parse(json), enPathRef, arPathRef)) + close;
    } catch {
      return block;
    }
  });
}

const LOCKED_SCRIPT = `<script>
    /* Arabic document: language and direction are fixed in the markup, not chosen at runtime. */
    (function () {
      try {
        var d = document.documentElement;
        d.lang = 'ar'; d.dir = 'rtl';
        try { if (sessionStorage.getItem('cc-pre')) d.classList.add('no-pre'); } catch (e) {}
      } catch (e) {}
    })();
    </script>`;

/**
 * @param {string} html   finished English page
 * @param {{enPath: string, arPath: string}} opts
 * @returns {string}      standalone Arabic page
 */
let enPathRef = '/';
let arPathRef = '/ar/';
let titleArRef = '';
let descArRef = '';

export function arize(html, { enPath, arPath, dict = null, untranslated = false }) {
  enPathRef = enPath;
  arPathRef = arPath;
  let out = html;
  const arUrl = SITE + arPath;
  const enUrl = SITE + enPath;

  // ── document element ────────────────────────────────────────────────────
  const titleAr = out.match(/<html[^>]*\sdata-title-ar="([^"]*)"/)?.[1] ?? '';
  const descAr = out.match(/<html[^>]*\sdata-desc-ar="([^"]*)"/)?.[1] ?? '';
  titleArRef = unescapeHtml(titleAr);
  descArRef = unescapeHtml(descAr);
  out = out.replace(/<html\b[^>]*>/, (tag) =>
    tag
      .replace(/\slang="[^"]*"/, ' lang="ar"')
      .replace(/\sdir="[^"]*"/, ' dir="rtl"')
      .replace(/\sdata-title-ar="[^"]*"/, '')
      .replace(/\sdata-desc-ar="[^"]*"/, '')
      .replace(/<html/, '<html data-lang-lock="ar"'));

  // ── head: title, description, social, canonical, alternates ─────────────
  if (titleAr) {
    out = out.replace(/<title>[\s\S]*?<\/title>/, `<title>${titleAr}</title>`);
    out = out.replace(/(<meta property="og:title" content=")[^"]*(")/, `$1${titleAr}$2`);
    out = out.replace(/(<meta name="twitter:title" content=")[^"]*(")/, `$1${titleAr}$2`);
  }
  if (descAr) {
    out = out.replace(/(<meta name="description" content=")[^"]*(")/, `$1${descAr}$2`);
    out = out.replace(/(<meta property="og:description" content=")[^"]*(")/, `$1${descAr}$2`);
    out = out.replace(/(<meta name="twitter:description" content=")[^"]*(")/, `$1${descAr}$2`);
  }
  out = out.replace(/(<meta property="og:url" content=")[^"]*(")/, `$1${arUrl}$2`);
  out = out.replace(/(<meta property="og:locale" content=")[^"]*(")/, '$1ar_AR$2');
  out = out.replace(/(<link rel="canonical" href=")[^"]*(")/, `$1${arUrl}$2`);
  const alternates = [
    `    <link rel="alternate" hreflang="en" href="${enUrl}" />`,
    `    <link rel="alternate" hreflang="ar" href="${arUrl}" />`,
    `    <link rel="alternate" hreflang="x-default" href="${enUrl}" />`,
  ].join('\n');
  out = out.replace(/\n\s*<link rel="alternate" hreflang="[^"]*" href="[^"]*" \/>/g, '');
  out = out.replace(/(\n\s*<link rel="canonical" href="[^"]*" \/>)/, `$1\n${alternates}`);
  out = out.replace(/<script>\s*\/\* Sets language\/direction[\s\S]*?<\/script>/, LOCKED_SCRIPT);

  // ── body copy ───────────────────────────────────────────────────────────
  const bodyStart = out.indexOf('<body');
  let head = localizeLd(out.slice(0, bodyStart));
  let body = localizeLd(out.slice(bodyStart));
  body = body.replace(/<script type="application\/ld\+json">[\s\S]*?<\/script>/g, () => '');

  if (dict) {
    body = resolveDict(body, dict);
  }
  body = swapContent(body, 'data-ar-html', true);
  body = swapContent(body, 'data-ar', false);
  body = swapAttr(body, 'data-ar-label', 'aria-label');
  body = swapAttr(body, 'data-ar-title', 'title');
  body = swapAttr(body, 'data-ar-alt', 'alt');
  body = swapAttr(body, 'data-ar-placeholder', 'placeholder');
  for (const attr of ['data-ar-html', 'data-ar', 'data-ar-label', 'data-ar-title', 'data-ar-alt', 'data-ar-placeholder']) {
    body = strip(body, attr);
  }
  body = rewriteLinks(body);
  // the language pill becomes a real link back to the English twin (after link rewriting)
  body = body.replace(/<a class="nav__round lang-btn" id="langBtn" href="[^"]*"[^>]*>EN<\/a>/, `<a class="nav__round lang-btn" id="langBtn" href="${enPath}" hreflang="en" title="Switch to English" aria-label="Switch to English">EN</a>`)
    .replace(/<button class="nav__round lang-btn" id="langBtn" type="button"><\/button>/, `<a class="nav__round lang-btn" id="langBtn" href="${enPath}" hreflang="en" title="Switch to English" aria-label="Switch to English">EN</a>`);

  if (untranslated) {
    // Long-form article not translated yet: keep the Arabic chrome, say so in the page,
    // and keep search engines on the English original instead of indexing a near-duplicate.
    if (!/<meta name="robots"/.test(head)) head = head.replace('</head>', '    <meta name="robots" content="noindex, follow" />\n  </head>');
    body = body.replace(/(<main[^>]*>)/, `$1
    <div class="notice container" style="margin-top:16px" role="note"><p>هذا المحتوى الطويل متاح باللغة الإنجليزية حاليًا. <a href="${enPath}">اقرأ الصفحة الأصلية</a>.</p></div>`);
  }
  return head + body;
}
