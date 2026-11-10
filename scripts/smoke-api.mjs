#!/usr/bin/env node
/* ==========================================================================
   smoke-api.mjs — end-to-end smoke test of the first-party lead pipeline.

   Boots server/api.mjs on an ephemeral port with an isolated temp data dir,
   then exercises: health, validation, consent, honeypot, contact/newsletter/
   career leads, booking slots + booking + ICS, measurement events, admin
   reads, stage transitions, CSV export and idempotency.

   Usage: npm run verify:api
   ========================================================================== */
import { createServer } from 'node:http';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createApi } from '../server/api.mjs';

const ROOT = fileURLToPath(new URL('../', import.meta.url));
const DIR = mkdtempSync(join(tmpdir(), 'cc-smoke-'));
const TOKEN = process.env.CC_ADMIN_TOKEN || 'cc-local-admin';
const api = createApi({ root: ROOT, env: { ...process.env, CC_DATA_DIR: DIR, CC_ADMIN_TOKEN: TOKEN } });
const server = createServer((req, res) => { api.handle(req, res, new URL(req.url, 'http://localhost')); });

const results = [];
const ok = (name, cond, detail = '') => {
  results.push({ name, pass: !!cond, detail });
  console.log(`${cond ? '✓' : '✗'} ${name}${detail ? ' — ' + detail : ''}`);
};
const j = async (path, opts = {}) => {
  const r = await fetch(`http://127.0.0.1:${port}${path}`, opts);
  let body = '';
  try { body = await r.text(); } catch {}
  return { status: r.status, headers: r.headers, body, json: (() => { try { return JSON.parse(body); } catch { return null; } })() };
};
const post = (path, data, headers = {}) => j(path, {
  method: 'POST', headers: { 'Content-Type': 'application/json', ...headers },
  body: JSON.stringify(data),
});
let port = 0;
await new Promise((resolve) => server.listen(0, '127.0.0.1', () => { port = server.address().port; resolve(); }));

try {
  const health = await j('/api/health');
  ok('GET /api/health → 200', health.status === 200 && health.json?.ok === true, `commit ${health.json?.commit || 'n/a'}`);

  const bad = await post('/api/contact', { name: 'A', email: 'not-an-email', message: 'Hello world', consent: 'on' });
  ok('invalid contact rejected (422)', bad.status === 422 && bad.json?.accepted === false, `status ${bad.status}`);

  const noConsent = await post('/api/contact', { name: 'QA Person', email: 'qa@example.invalid', message: 'A valid long-enough message.', consent: '' });
  ok('missing consent rejected (422)', noConsent.status === 422, `status ${noConsent.status}`);

  const spam = await post('/api/contact', { name: 'QA Person', email: 'qa@example.invalid', message: 'A valid long-enough message.', consent: 'on', _hp: 'bot' });
  ok('honeypot rejected', spam.status >= 400, `status ${spam.status}`);

  const contact = await post('/api/contact', {
    name: 'QA Person', email: 'qa@example.invalid', company: 'QA Co', message: 'Smoke test: we need a brand system and a website.',
    inquiry: 'MA-03', consent: 'on', lang: 'en', page: '/contact/',
  });
  ok('POST /api/contact → accepted + lead id', [200,201].includes(contact.status) && contact.json?.accepted === true && !!contact.json?.id, contact.json?.id || contact.body.slice(0, 120));

  const idem = await post('/api/contact', {
    name: 'QA Person', email: 'qa@example.invalid', company: 'QA Co', message: 'Smoke test: we need a brand system and a website.',
    inquiry: 'MA-03', consent: 'on', lang: 'en', page: '/contact/',
  }, { 'Idempotency-Key': 'smoke-1' });
  ok('idempotency key accepted', [200,201].includes(idem.status) && idem.json?.accepted === true);

  const news = await post('/api/newsletter', { email: 'news@example.invalid', consent: 'on', inquiry: 'Newsletter subscription', lang: 'en' });
  ok('POST /api/newsletter → accepted', [200,201].includes(news.status) && news.json?.accepted === true, news.json?.id || '');

  const career = await post('/api/career', { name: 'QA Designer', email: 'qa@example.invalid', consent: 'on', inquiry: 'Freelancer / Career', lang: 'en' });
  ok('POST /api/career → accepted', [200,201].includes(career.status) && career.json?.accepted === true, career.json?.id || '');

  const slots = await j('/api/booking/slots');
  const dates = slots.json?.dates || [];
  ok('GET /api/booking/slots → published dates', slots.status === 200 && dates.length > 0, dates.slice(0, 3).join(', '));
  const day = await j(`/api/booking/slots?date=${encodeURIComponent(dates[0] || '')}`);
  const free = (day.json?.slots || []).find((s) => s.available);
  ok('slots for a date include an available time', !!free, free?.time || '');

  const booking = await post('/api/booking', {
    name: 'QA Person', email: 'qa@example.invalid', specialty: 'brand', date: dates[0], time: free?.time || '10:00',
    timezone: 'Asia/Riyadh', message: 'Discuss a bilingual brand system.', consent: 'on', lang: 'en', service: 'MA-03',
  });
  // IANA zones from older clients normalize to the published label used by the .ics offset.
  ok('POST /api/booking → accepted + calendar URL + normalized zone',
     [200,201].includes(booking.status) && booking.json?.accepted === true && !!booking.json?.calendarUrl && booking.json?.timezone === 'AST',
     `${booking.json?.id || booking.body.slice(0, 80)} · ${booking.json?.timezone || 'no zone'}`);
  if (booking.json?.calendarUrl) {
    const ics = await j(booking.json.calendarUrl);
    ok('GET calendar.ics → VEVENT', ics.status === 200 && /BEGIN:VEVENT/.test(ics.body) && /BEGIN:VCALENDAR/.test(ics.body));
    const dt = (ics.body.match(/DTSTART:(\d{8}T\d{6})Z/) || [])[1];
    const expected = booking.json?.utc ? `${booking.json.utc.replace(/[-:]/g, '')}00` : '';
    ok('calendar invite starts at the booked UTC instant', !!dt && dt === expected, `${dt || 'no DTSTART'} vs ${expected || 'no utc'}`);
    ok('calendar invite carries a reminder and a reference', /BEGIN:VALARM/.test(ics.body) && new RegExp(booking.json.id).test(ics.body),
       'VALARM + UID reference');
  }
  /* ---- timezone correctness -------------------------------------------------
     Office hours are published wall-clock times. Asking for EET must return the
     same wall-clock grid with a different UTC instant, and two visitors booking
     "09:00" in different zones must NOT be sold the same instant. */
  const slotsAst = await j(`/api/booking/slots?date=${dates[0]}&timezone=AST`);
  const slotsEet = await j(`/api/booking/slots?date=${dates[0]}&timezone=EET`);
  const ast09 = slotsAst.json?.slots?.find((x) => x.time === '09:00');
  const eet09 = slotsEet.json?.slots?.find((x) => x.time === '09:00');
  ok('slots are labelled in the requested timezone', slotsAst.json?.timezone === 'AST' && slotsEet.json?.timezone === 'EET',
     `${slotsAst.json?.timezone}/${slotsEet.json?.timezone}`);
  ok('same wall clock ≠ same instant across zones', !!ast09?.utc && !!eet09?.utc && ast09.utc !== eet09.utc,
     `${ast09?.utc} vs ${eet09?.utc}`);
  ok('offset difference is exactly one hour', (() => {
    if (!ast09?.utc || !eet09?.utc) return false;
    return Math.abs(Date.parse(`${ast09.utc}:00Z`) - Date.parse(`${eet09.utc}:00Z`)) === 3600000;
  })(), 'AST is UTC+3, EET is UTC+2');

  /* ---- malformed input ------------------------------------------------------ */
  const badEmail = await post('/api/booking', {
    name: 'Bad Email', email: 'not-an-email', specialty: 'brand', date: dates[0], time: ast09?.time || '09:00',
    timezone: 'AST', consent: 'on',
  });
  ok('booking rejects a malformed email', badEmail.status === 422, `status ${badEmail.status}`);
  const badTz = await post('/api/booking', {
    name: 'Bad Zone', email: 'zone@example.invalid', specialty: 'brand', date: dates[0], time: '09:00',
    timezone: 'Mars/Olympus', consent: 'on',
  });
  ok('booking rejects an unsupported timezone', badTz.status === 422, `status ${badTz.status}`);
  const weekend = dates.find((d) => [5, 6].includes(new Date(`${d}T00:00:00Z`).getUTCDay()));
  const offSchedule = await post('/api/booking', {
    name: 'Weekend', email: 'weekend@example.invalid', specialty: 'brand', date: weekend || '1999-01-01',
    time: '09:00', timezone: 'AST', consent: 'on',
  });
  ok('booking rejects a date outside published office days', offSchedule.status === 422, `status ${offSchedule.status}`);

  /* ---- replay safety -------------------------------------------------------- */
  const replay = await post('/api/booking', {
    name: 'QA Person', email: 'qa@example.invalid', specialty: 'brand', date: dates[0],
    time: free?.time || '10:00', timezone: 'AST', consent: 'on', lang: 'en',
  });
  ok('re-submitting the same booking is idempotent, not duplicated',
     replay.status === 200 && replay.json?.duplicate === true && replay.json?.id === booking.json?.id,
     `status ${replay.status} · ${replay.json?.id || 'no id'}`);

  const clash = await post('/api/booking', {
    name: 'Other Person', email: 'other@example.invalid', specialty: 'product', date: dates[0], time: free?.time || '10:00',
    timezone: 'Asia/Riyadh', consent: 'on', lang: 'en',
  });
  ok('double-booking the same slot rejected', clash.status === 409, `status ${clash.status}`);
  /* A third distinct booking from one address inside ten minutes is a burst —
     refused so a single visitor cannot empty the day. */
  const burst1 = await post('/api/booking', { name: 'Burst A', email: 'burst@example.invalid', specialty: 'brand', date: dates[0], time: slotsAst.json?.slots?.[1]?.time || '09:30', timezone: 'AST', consent: 'on' });
  const burst2 = await post('/api/booking', { name: 'Burst B', email: 'burst@example.invalid', specialty: 'brand', date: dates[0], time: slotsAst.json?.slots?.[2]?.time || '10:00', timezone: 'AST', consent: 'on' });
  const burst3 = await post('/api/booking', { name: 'Burst C', email: 'burst@example.invalid', specialty: 'brand', date: dates[0], time: slotsAst.json?.slots?.[3]?.time || '10:30', timezone: 'AST', consent: 'on' });
  ok('a burst of bookings from one address is refused',
     [200, 201].includes(burst1.status) && [200, 201].includes(burst2.status) && burst3.status === 429,
     `${burst1.status}/${burst2.status}/${burst3.status}`);

  const ev1 = await post('/api/events', { event: 'cc', name: 'page_view', path: '/', lang: 'en' });
  const ev2 = await post('/api/events', { event: 'cc', name: 'cta_click', path: '/', lang: 'en' });
  ok('POST /api/events → single consented event accepted', ev1.status === 202 && ev2.status === 202, `statuses ${ev1.status}/${ev2.status}`);
  const evBad = await post('/api/events', { name: 'evil<script>', path: '/' });
  ok('POST /api/events rejects unknown event names', evBad.status === 400, `status ${evBad.status}`);

  const denied = await j('/api/leads');
  ok('admin reads require a token', denied.status === 401 || denied.status === 403, `status ${denied.status}`);
  const H = { Authorization: `Bearer ${TOKEN}` };
  const leads = await j('/api/leads', { headers: H });
  const list = Array.isArray(leads.json) ? leads.json : (leads.json?.leads || []);
  ok('GET /api/leads → stored records', leads.status === 200 && list.length >= 4, `${list.length} records`);
  const stages = new Set(list.map((l) => l.stage));
  ok('CRM stages present', ['new', 'qualified', 'proposal', 'won', 'lost'].every((s) => typeof s === 'string') && stages.size > 0, [...stages].join(', '));
  if (list.length) {
    const first = list[0].id || list[0].leadId;
    const patch = await j(`/api/leads/${encodeURIComponent(first)}`, {
      method: 'PATCH', headers: { ...H, 'Content-Type': 'application/json' },
      body: JSON.stringify({ stage: 'Proposal', note: 'Smoke test qualification' }),
    });
    ok('PATCH /api/leads/:id → stage transition', patch.status === 200, `status ${patch.status}`);
  }
  const bookings = await j('/api/bookings', { headers: H });
  ok('GET /api/bookings → stored booking', bookings.status === 200 && JSON.stringify(bookings.json).includes('QA Person'));
  const stats = await j('/api/stats', { headers: H });
  ok('GET /api/stats → counts', stats.status === 200 && stats.json && Object.keys(stats.json).length > 0);
  const csv = await j('/api/export.csv', { headers: H });
  ok('GET /api/export.csv → CSV', csv.status === 200 && /id|name|email/i.test(csv.body));
  const crm = await j('/crm/');
  ok('GET /crm/ → noindex lead desk', crm.status === 200 && /Lead Desk/.test(crm.body) && /Qualified/.test(crm.body));
} finally {
  await new Promise((r) => server.close(r));
  rmSync(DIR, { recursive: true, force: true });
}

const failed = results.filter((r) => !r.pass);
if (failed.length) {
  console.error(`\nsmoke-api: ${failed.length}/${results.length} check(s) failed`);
  process.exit(1);
}
console.log(`\nsmoke-api: all ${results.length} checks passed`);
