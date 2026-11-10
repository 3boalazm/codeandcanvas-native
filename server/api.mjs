/* ==========================================================================
   Code & Canvas — first-party lead / booking / measurement API
   Zero runtime dependencies. Node >= 20.

   This is the reference implementation of docs/INTEGRATIONS.md. It is a REAL
   pipeline (durable records, validation, spam controls, consent, CRM stages,
   notifications, calendar sync) but it is a SINGLE-NODE, FILE-BACKED service for
   review and staging. Before a production launch, move the store to a managed
   database, put it behind TLS + authentication + backups, and replace the
   webhook/log notifier with an approved mail provider. See docs/LEAD-PIPELINE.md.

   No secrets are committed: CC_ADMIN_TOKEN and CC_NOTIFY_WEBHOOK come from env.
   ========================================================================== */
import { readFileSync, writeFileSync, existsSync, mkdirSync, appendFileSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { createHash, randomUUID } from 'node:crypto';

const STAGES = ['new', 'qualified', 'proposal', 'won', 'lost'];
const SPECIALTIES = new Set(['brand', 'product', 'technology', 'healthcare', 'general']);
const KINDS = new Set(['contact', 'newsletter', 'career', 'books']);
/* Strict enough to reject what a buyer would call a broken address:
   no whitespace, angle brackets, double @, leading/trailing dot, or a TLD
   shorter than two characters. Deliberately not RFC-complete — the goal is to
   catch typos before a lead is stored, not to police exotic mailboxes. */
const EMAIL_RE = /^[^\s@<>.][^\s@<>]*@[^\s@<>.]+(?:\.[^\s@<>.]+)*\.[A-Za-z]{2,}$/;
const CODE_RE = /^(AB|MA|HC|CC)-\d{2}$/i;
const EVENT_KEYS = new Set(['id', 'service', 'from', 'form', 'channel', 'filter', 'to']);

const json = (res, status, body, headers = {}) => {
  const text = JSON.stringify(body);
  res.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff', ...headers });
  res.end(text);
};
const text = (res, status, body, type = 'text/plain; charset=utf-8', headers = {}) => {
  res.writeHead(status, { 'Content-Type': type, 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff', ...headers });
  res.end(body);
};
const clean = (v, max = 2000) => (typeof v === 'string' ? v.trim().slice(0, max) : '');
const safe = (s) => String(s).replace(/[^\w./@-]/g, '').slice(0, 80);

function readJson(req) {
  return new Promise((resolve, reject) => {
    let size = 0; const chunks = [];
    req.on('data', (c) => {
      size += c.length;
      if (size > 64 * 1024) { reject(new Error('payload too large')); req.destroy(); return; }
      chunks.push(c);
    });
    req.on('end', () => {
      try { resolve(chunks.length ? JSON.parse(Buffer.concat(chunks).toString('utf8')) : {}); }
      catch { reject(new Error('invalid JSON')); }
    });
    req.on('error', reject);
  });
}

export function createApi({ root, env = process.env } = {}) {
  const dataDir = resolve(env.CC_DATA_DIR || join(root, '.data'));
  mkdirSync(dataDir, { recursive: true });
  const token = env.CC_ADMIN_TOKEN || 'cc-local-admin';
  const webhook = env.CC_NOTIFY_WEBHOOK || '';
  const commit = (env.CC_BUILD_COMMIT || 'dev').slice(0, 40);
  const files = {
    leads: join(dataDir, 'leads.json'),
    bookings: join(dataDir, 'bookings.json'),
    subscribers: join(dataDir, 'subscribers.json'),
    events: join(dataDir, 'events.jsonl'),
    log: join(dataDir, 'notifications.log'),
  };
  for (const key of ['leads', 'bookings', 'subscribers']) if (!existsSync(files[key])) writeFileSync(files[key], '[]');
  if (!existsSync(files.events)) writeFileSync(files.events, '');
  const load = (key) => { try { return JSON.parse(readFileSync(files[key], 'utf8')); } catch { return []; } };
  const save = (key, value) => {
    const tmp = `${files[key]}.tmp`;
    writeFileSync(tmp, JSON.stringify(value, null, 2));
    writeFileSync(files[key], readFileSync(tmp)); // atomic-ish rename-free write for static hosts
  };
  const id = (prefix) => `${prefix}-${Date.now().toString(36)}-${randomUUID().slice(0, 8)}`;

  /* ---------------- Rate limiting / origin ---------------- */
  const hits = new Map();
  const rateLimited = (key, limit, windowMs) => {
    const now = Date.now();
    const list = (hits.get(key) || []).filter((t) => now - t < windowMs);
    list.push(now); hits.set(key, list);
    return list.length > limit;
  };
  const clientIp = (req) => clean(req.headers['x-forwarded-for']?.split(',')[0] || req.socket.remoteAddress || 'unknown', 80);
  const originOk = (req) => {
    const origin = req.headers.origin;
    if (!origin) return true;
    try {
      const host = req.headers.host || '';
      return new URL(origin).host === host;
    } catch { return false; }
  };
  const authorized = (req, url) => {
    const bearer = (req.headers.authorization || '').replace(/^Bearer\s+/i, '');
    const supplied = bearer || req.headers['x-cc-token'] || url.searchParams.get('token') || '';
    return supplied && supplied === token;
  };

  /* ---------------- Events / notifications ---------------- */
  function event(name, props = {}) {
    const row = { at: new Date().toISOString(), name: String(name).slice(0, 50), lang: clean(props.lang, 5), path: safe(props.path || '') };
    for (const [k, v] of Object.entries(props)) if (EVENT_KEYS.has(k) && /^[a-zA-Z0-9_./-]{1,80}$/.test(String(v))) row[k] = String(v);
    try { appendFileSync(files.events, JSON.stringify(row) + '\n'); } catch { /* diagnostics only */ }
    return row;
  }
  function notify(kind, record) {
    const line = `${new Date().toISOString()} ${kind} ${record.id} ${record.email || ''} ${record.stage || record.status || ''}\n`;
    try { appendFileSync(files.log, line); } catch { /* best effort */ }
    if (webhook && /^https:\/\//.test(webhook)) {
      const payload = JSON.stringify({ kind, id: record.id, name: record.name, email: record.email, inquiry: record.inquiry || record.specialty, stage: record.stage, createdAt: record.createdAt });
      fetch(webhook, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: payload }).catch(() => {});
    }
  }
  /* Deliberately conservative: no third-party script is loaded by the browser.
     A real mail provider is configured server-side via CC_NOTIFY_WEBHOOK. */

  /* ---------------- Lead qualification ---------------- */
  function qualify(data) {
    let score = 0;
    if (clean(data.organization)) score += 2;
    if (CODE_RE.test(clean(data.inquiry, 120))) score += 2;
    if (clean(data.message, 4000).length > 120) score += 1;
    if (clean(data.phone)) score += 1;
    return { score, stage: score >= 4 ? 'qualified' : 'new' };
  }

  function makeLead(data, kind, req) {
    const q = qualify(data);
    const now = new Date().toISOString();
    return {
      id: id('lead'), createdAt: now, updatedAt: now, kind,
      name: [clean(data.first_name, 120), clean(data.last_name, 120)].filter(Boolean).join(' ') || clean(data.name, 160),
      email: clean(data.email, 200).toLowerCase(),
      phone: clean(data.phone, 60), organization: clean(data.organization, 200),
      inquiry: clean(data.inquiry, 200), message: clean(data.message, 4000),
      specialty: SPECIALTIES.has(clean(data.specialty, 40)) ? clean(data.specialty, 40) : '',
      service: CODE_RE.test(clean(data.inquiry, 200)) ? clean(data.inquiry, 200).slice(0, 5).toUpperCase() : '',
      page: safe(data.page || ''), lang: clean(data.lang, 5) === 'ar' ? 'ar' : 'en',
      consent: data.consent === true || data.consent === 'on' || data.consent === 'yes',
      source: clean(data.source, 60) || 'website',
      score: q.score, stage: q.stage, notes: [], history: [{ at: now, action: 'created', detail: `website inquiry (${kind})` }],
      ipHash: createHash('sha256').update(clientIp(req) + commit).digest('hex').slice(0, 16),
    };
  }

  /* ---------------- Booking slots ---------------- */
  const TZ_OFFSET = { AST: 3, EET: 2, UTC: 0 };
  // Accept both the short labels used by the booking form and IANA zones sent by
  // older clients; normalize to a label so the ICS offset is never guessed.
  const TZ_ALIAS = { 'Asia/Riyadh': 'AST', 'Africa/Cairo': 'EET', 'Etc/UTC': 'UTC', 'Etc/GMT': 'UTC' };
  const SLOTS = ['09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:00', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30'];
  function businessDates(count = 30) {
    const out = []; const d = new Date(); d.setUTCHours(0, 0, 0, 0);
    for (let i = 1; out.length < count && i < 90; i++) {
      const day = new Date(d.getTime() + i * 86400000);
      const wd = day.getUTCDay(); // 0 Sun … 4 Thu are the published office days
      if (wd >= 0 && wd <= 4) out.push(day.toISOString().slice(0, 10));
    }
    return out;
  }
  /* Office hours are published wall-clock times: 09:00–17:00 AST (UTC+3) and
     09:00–17:00 EET (UTC+2). A slot is therefore defined in UTC and rendered per
     visitor timezone — storing the wall clock alone made the timezone picker
     cosmetic and let two visitors book the same UTC instant. */
  function slots(date, tz = 'AST') {
    if (!businessDates().includes(date)) return [];
    const off = TZ_OFFSET[tz] ?? TZ_OFFSET.AST;
    const taken = new Set(load('bookings').filter((b) => b.date === date && b.status !== 'cancelled').map((b) => slotUtc(b)));
    return SLOTS.map((time) => {
      const utc = wallToUtc(date, time, off);
      return { time, utc, label: utcToWall(utc, off), available: !taken.has(utc) };
    });
  }
  /* Booking identity is the UTC instant, so AST 09:00 and EET 09:00 never clash
     with each other and the same instant can only be sold once. */
  function wallToUtc(date, time, off) {
    const [y, m, d] = date.split('-').map(Number);
    const [hh, mm] = time.split(':').map(Number);
    return new Date(Date.UTC(y, m - 1, d, hh - off, mm, 0)).toISOString().slice(0, 16);
  }
  function slotUtc(b) {
    const off = TZ_OFFSET[b.timezone] ?? 3;
    return b.utc || wallToUtc(b.date, b.time, off);
  }
  function utcToWall(utc, off) {
    const d = new Date(utc + ':00Z');
    const local = new Date(d.getTime() + off * 3600000);
    return local.toISOString().slice(11, 16);
  }
  function ics(booking) {
    /* Prefer the stored UTC instant; fall back to the wall clock + offset for
       bookings created before the utc field existed. */
    const start = booking.utc
      ? new Date(booking.utc + ':00Z')
      : (() => {
          const off = TZ_OFFSET[booking.timezone] ?? 3;
          const [y, m, d] = booking.date.split('-').map(Number);
          const [hh, mm] = booking.time.split(':').map(Number);
          return new Date(Date.UTC(y, m - 1, d, hh - off, mm, 0));
        })();
    const end = new Date(start.getTime() + 30 * 60000);
    const fmt = (x) => x.toISOString().replace(/[-:]/g, '').replace(/\.\d{3}/, '');
    const esc = (s) => String(s).replace(/([,;\\])/g, '\\$1').replace(/\n/g, '\\n').slice(0, 500);
    return ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Code and Canvas//Booking//EN', 'CALSCALE:GREGORIAN', 'METHOD:PUBLISH',
      'BEGIN:VEVENT', `UID:${booking.id}@codeandcanvas.net`, `DTSTAMP:${fmt(new Date())}`, `DTSTART:${fmt(start)}`, `DTEND:${fmt(end)}`,
      `SUMMARY:${esc('Code & Canvas — 30-min discovery call')}`,
      `DESCRIPTION:${esc(`Specialty: ${booking.specialty}\nReference: ${booking.id}\nNotes: ${booking.notes || '—'}\nRemote call · ${booking.timezone}`)}`,
      'LOCATION:Remote (link confirmed by email)', 'STATUS:CONFIRMED', 'BEGIN:VALARM', 'TRIGGER:-PT60M', 'ACTION:DISPLAY',
      'DESCRIPTION:Discovery call in one hour', 'END:VALARM', 'END:VEVENT', 'END:VCALENDAR'].join('\r\n') + '\r\n';
  }

  /* ---------------- Public routes ---------------- */
  async function handle(req, res, url) {
    const path = url.pathname;
    if (!path.startsWith('/api/') && path !== '/crm' && path !== '/crm/') return false;

    if (path === '/api/health') return json(res, 200, { ok: true, service: 'cc-lead-pipeline', commit, time: new Date().toISOString(), store: 'file' });

    if (path === '/crm' || path === '/crm/') {
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store', 'X-Robots-Tag': 'noindex' });
      return res.end(readFileSync(join(root, 'server/crm.html'), 'utf8'));
    }

    /* Admin-only reads / writes */
    if (path === '/api/leads' || path === '/api/bookings' || path === '/api/stats' || path === '/api/export.csv' || path.startsWith('/api/leads/')) {
      if (!authorized(req, url)) return json(res, 401, { accepted: false, error: 'admin token required' });
      if (path === '/api/leads' && req.method === 'GET') return json(res, 200, { accepted: true, leads: load('leads') });
      if (path === '/api/bookings' && req.method === 'GET') return json(res, 200, { accepted: true, bookings: load('bookings') });
      if (path === '/api/stats' && req.method === 'GET') {
        const leads = load('leads'), bookings = load('bookings');
        let events = 0; try { events = readFileSync(files.events, 'utf8').trim().split('\n').filter(Boolean).length; } catch { /* none yet */ }
        return json(res, 200, { accepted: true, leads: leads.length, byStage: Object.fromEntries(STAGES.map((s) => [s, leads.filter((l) => l.stage === s).length])), bookings: bookings.length, events });
      }
      if (path === '/api/export.csv' && req.method === 'GET') {
        const rows = [['id', 'createdAt', 'kind', 'name', 'email', 'organization', 'inquiry', 'stage', 'score']];
        for (const l of load('leads')) rows.push([l.id, l.createdAt, l.kind, l.name, l.email, l.organization, l.inquiry, l.stage, l.score]);
        const csv = rows.map((r) => r.map((v) => `"${String(v ?? '').replace(/"/g, '""')}"`).join(',')).join('\r\n');
        return text(res, 200, csv, 'text/csv; charset=utf-8', { 'Content-Disposition': 'attachment; filename="cc-leads.csv"' });
      }
      const match = path.match(/^\/api\/leads\/(lead-[\w-]+)$/);
      if (match && req.method === 'PATCH') {
        const body = await readJson(req).catch(() => ({}));
        const leads = load('leads'); const lead = leads.find((l) => l.id === match[1]);
        if (!lead) return json(res, 404, { accepted: false, error: 'not found' });
        const stage = String(body.stage || '').toLowerCase();
        if (STAGES.includes(stage)) {
          lead.stage = stage;
          lead.history.push({ at: new Date().toISOString(), action: 'stage', detail: stage });
          if (stage === 'qualified' || stage === 'won') event(`lead_${stage === 'won' ? 'converted' : 'qualified'}`, { id: lead.id });
        }
        if (typeof body.note === 'string' && body.note.trim()) lead.notes.push({ at: new Date().toISOString(), text: clean(body.note, 1000) });
        lead.updatedAt = new Date().toISOString(); save('leads', leads);
        return json(res, 200, { accepted: true, lead });
      }
      return json(res, 405, { accepted: false, error: 'method not allowed' });
    }

    /* Calendar download (reference id is unguessable enough for a review build) */
    const icsMatch = path.match(/^\/api\/booking\/(book-[\w-]+)\/calendar\.ics$/);
    if (icsMatch && req.method === 'GET') {
      const booking = load('bookings').find((b) => b.id === icsMatch[1]);
      if (!booking) return json(res, 404, { accepted: false, error: 'not found' });
      return text(res, 200, ics(booking), 'text/calendar; charset=utf-8', { 'Content-Disposition': `attachment; filename="${booking.id}.ics"` });
    }
    if (path === '/api/booking/slots' && req.method === 'GET') {
      const date = clean(url.searchParams.get('date'), 10);
      const tzIn = clean(url.searchParams.get('timezone'), 64);
      const timezone = TZ_OFFSET[tzIn] !== undefined ? tzIn : (TZ_ALIAS[tzIn] || 'AST');
      return json(res, 200, {
        accepted: true, dates: businessDates(), date, timezone,
        offsets: TZ_OFFSET, slots: slots(date, timezone),
      });
    }

    if (req.method !== 'POST') return json(res, 405, { accepted: false, error: 'method not allowed' });
    if (!originOk(req)) return json(res, 403, { accepted: false, error: 'cross-origin request refused' });
    const ip = clientIp(req);
    if (rateLimited(`post:${ip}`, 30, 60000)) return json(res, 429, { accepted: false, error: 'too many requests' });
    let body;
    try { body = await readJson(req); } catch (e) { return json(res, 400, { accepted: false, error: e.message }); }
    if (body._hp) return json(res, 400, { accepted: false, error: 'rejected' });

    /* First-party measurement collector: allowlisted identifiers only, no PII. */
    if (path === '/api/events') {
      if (rateLimited(`events:${ip}`, 90, 60000)) return json(res, 429, { accepted: false });
      const name = clean(body.name, 50);
      if (!name || !/^[a-z0-9_.-]+$/i.test(name)) return json(res, 400, { accepted: false });
      event(name, body);
      return json(res, 202, { accepted: true });
    }

    /* Forms */
    if (path === '/api/contact' || path === '/api/newsletter' || path === '/api/career') {
      const kind = path.slice(5);
      if (!KINDS.has(kind) && kind !== 'contact') return json(res, 400, { accepted: false });
      const email = clean(body.email, 200).toLowerCase();
      const consent = body.consent === true || body.consent === 'on' || body.consent === 'yes';
      const nameOk = kind === 'newsletter' || clean(body.first_name, 120) || clean(body.name, 160);
      const message = clean(body.message, 4000);
      if (!EMAIL_RE.test(email) || email.length > 200) return json(res, 422, { accepted: false, error: 'valid email required' });
      if (!consent) return json(res, 422, { accepted: false, error: 'consent required' });
      if (!nameOk) return json(res, 422, { accepted: false, error: 'name required' });
      if (kind !== 'newsletter' && message && (message.match(/https?:\/\//g) || []).length > 3) return json(res, 422, { accepted: false, error: 'too many links' });
      if (kind === 'contact' && message.length < 5) return json(res, 422, { accepted: false, error: 'message too short' });

      /* Idempotency: the same email/kind/message inside 10 minutes is one lead. */
      const leads = load('leads');
      const fingerprint = createHash('sha256').update([kind, email, message].join('|')).digest('hex').slice(0, 20);
      const dup = leads.find((l) => l.fingerprint === fingerprint && Date.now() - Date.parse(l.createdAt) < 600000);
      if (dup) return json(res, 200, { accepted: true, id: dup.id, duplicate: true });

      const lead = makeLead(body, kind, req);
      lead.fingerprint = fingerprint;
      leads.push(lead); save('leads', leads);
      if (kind === 'newsletter') {
        const subs = load('subscribers');
        subs.push({ id: id('sub'), leadId: lead.id, email, lang: lead.lang, consentAt: lead.createdAt, status: 'pending_confirmation' });
        save('subscribers', subs);
      }
      event('form_submit', { form: kind, lang: lead.lang, path: lead.page });
      if (lead.stage === 'qualified') event('lead_qualified', { id: lead.id });
      notify(kind, lead);
      return json(res, 201, { accepted: true, id: lead.id, stage: lead.stage });
    }

    /* Booking */
    if (path === '/api/booking') {
      const email = clean(body.email, 200).toLowerCase();
      const name = clean(body.name, 160);
      const date = clean(body.date, 10), time = clean(body.time, 5);
      const specialty = clean(body.specialty, 40);
      const tzIn = clean(body.timezone, 64);
      const timezone = TZ_OFFSET[tzIn] !== undefined ? tzIn : (TZ_ALIAS[tzIn] || '');
      if (!timezone) return json(res, 422, { accepted: false, error: 'unsupported timezone' });
      const consent = body.consent === true || body.consent === 'on' || body.consent === 'yes';
      if (!EMAIL_RE.test(email) || !name || !consent) return json(res, 422, { accepted: false, error: 'name, valid email and consent required' });
      if (!SPECIALTIES.has(specialty)) return json(res, 422, { accepted: false, error: 'unknown specialty' });
      if (!/^\d{4}-\d{2}-\d{2}$/.test(date) || !businessDates().includes(date)) return json(res, 422, { accepted: false, error: 'date outside the published schedule' });
      /* Replay-safe: the same person booking the same slot twice inside 10
         minutes gets the first booking back instead of a second record. */
      const requestedUtc = wallToUtc(date, time, TZ_OFFSET[timezone] ?? 3);
      const duplicate = load('bookings').find((b) => b.status !== 'cancelled'
        && b.email === email && slotUtc(b) === requestedUtc
        && Date.now() - Date.parse(b.createdAt) < 600000);
      if (duplicate) {
        return json(res, 200, { accepted: true, duplicate: true, id: duplicate.id, leadId: duplicate.leadId || '',
          date: duplicate.date, time: duplicate.time, timezone: duplicate.timezone, calendarUrl: duplicate.calendarUrl });
      }
      /* One address cannot hold the whole day: a second *different* slot within
         ten minutes is treated as a burst, not a real second appointment. */
      const recent = load('bookings').filter((b) => b.email === email && Date.now() - Date.parse(b.createdAt) < 600000);
      if (recent.length >= 2) return json(res, 429, { accepted: false, error: 'too many bookings from this address' });
      const free = slots(date, timezone).find((s) => s.time === time && s.available);
      if (!free) return json(res, 409, { accepted: false, error: 'slot unavailable' });
      const booking = {
        id: id('book'), createdAt: new Date().toISOString(), name, email,
        phone: clean(body.phone, 60), organization: clean(body.organization, 200),
        specialty, timezone, date, time, utc: requestedUtc, durationMinutes: 30,
        notes: clean(body.notes, 2000), service: CODE_RE.test(clean(body.service, 5)) ? clean(body.service, 5).toUpperCase() : '',
        inquiry: clean(body.inquiry, 200), lang: clean(body.lang, 5) === 'ar' ? 'ar' : 'en',
        calendarUrl: '', status: 'confirmed', source: 'website',
      };
      booking.calendarUrl = `/api/booking/${booking.id}/calendar.ics`;
      const bookings = load('bookings'); bookings.push(booking); save('bookings', bookings);
      /* Every confirmed booking creates / links a CRM record. */
      const leads = load('leads');
      const lead = makeLead({ first_name: name.split(' ')[0], last_name: name.split(' ').slice(1).join(' '), email, organization: booking.organization,
        inquiry: booking.inquiry || `Discovery call · ${specialty}`, message: booking.notes || `Booked ${date} ${time} ${timezone}`,
        consent: true, specialty, lang: booking.lang, page: '/book/', source: 'booking' }, 'contact', req);
      lead.stage = 'qualified'; lead.score = Math.max(lead.score, 5); lead.bookingId = booking.id;
      lead.history.push({ at: lead.createdAt, action: 'booking', detail: `${date} ${time} ${timezone}` });
      leads.push(lead); save('leads', leads); booking.leadId = lead.id; save('bookings', bookings);
      event('booking_confirmed', { id: booking.id, service: booking.service });
      event('lead_qualified', { id: lead.id });
      notify('booking', booking);
      return json(res, 201, { accepted: true, id: booking.id, leadId: lead.id, date, time, timezone, utc: booking.utc, calendarUrl: booking.calendarUrl });
    }

    return json(res, 404, { accepted: false, error: 'unknown endpoint' });
  }

  return { handle, dataDir, commit, stages: STAGES };
}
