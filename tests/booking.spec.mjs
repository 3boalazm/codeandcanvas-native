/* ==========================================================================
   booking.spec.mjs — the real booking journey, in both languages.

   Two layers:
     1. UI journey — specialty → day → slot → details → confirmation, driven
        against a *stubbed* /api/booking so the browser test never writes a
        production appointment. The stub asserts the exact payload the page
        sends, which is the part a UI test can prove.
     2. Server contract — the same journey against the real handler, in-process,
        so "the confirmation said yes" is checked against what was stored.

   Contact-form and calendars are stubbed at the network boundary only; nothing
   leaves 127.0.0.1 (see tests/helpers.mjs isolate()).
   ========================================================================== */
import { test, expect } from '@playwright/test';
import { createServer } from 'node:http';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { isolate, visit } from './helpers.mjs';
import { createApi } from '../server/api.mjs';

const ROOT = fileURLToPath(new URL('../', import.meta.url));

/* ------------------------------------------------------------------ stubs */
const FUTURE_DATES = ['2026-12-07', '2026-12-08', '2026-12-09'];

async function stubScheduler(page, sent = []) {
  await page.route(
    (url) => url.pathname === '/api/booking/slots',
    (route) => {
      const tz = new URL(route.request().url()).searchParams.get('timezone') || 'AST';
      const offset = tz === 'EET' ? 2 : tz === 'UTC' ? 0 : 3;
      route.fulfill({
        contentType: 'application/json',
        body: JSON.stringify({
          accepted: true, dates: FUTURE_DATES, date: FUTURE_DATES[0], timezone: tz,
          slots: [
            { time: '09:00', utc: `2026-12-07T${String(9 - offset).padStart(2, '0')}:00`, available: true },
            { time: '09:30', utc: `2026-12-07T${String(9 - offset).padStart(2, '0')}:30`, available: false },
            { time: '10:00', utc: `2026-12-07T${String(10 - offset).padStart(2, '0')}:00`, available: true },
          ],
        }),
      });
    },
  );
  await page.route(
    (url) => url.pathname === '/api/booking',
    (route) => {
      sent.push(JSON.parse(route.request().postData() || '{}'));
      route.fulfill({
        status: 201, contentType: 'application/json',
        body: JSON.stringify({
          accepted: true, id: 'book-qa-0001', leadId: 'lead-qa-0001', date: FUTURE_DATES[0],
          time: '10:00', timezone: 'AST', utc: '2026-12-07T07:00',
          calendarUrl: '/api/booking/book-qa-0001/calendar.ics',
        }),
      });
    },
  );
}

async function fillDetails(page, lang = 'en') {
  await page.locator('#b-name').fill('QA Person');
  await page.locator('#b-email').fill('qa@example.invalid');
  await page.locator('#b-consent').check();
  expect(lang).toBeTruthy();
}

/* ------------------------------------------------------------------ 1 · UI */
test.beforeEach(async ({ page }) => isolate(page));

for (const lang of ['en', 'ar']) {
  test(`booking journey completes in ${lang} and sends a complete payload`, async ({ page }) => {
    const sent = [];
    await stubScheduler(page, sent);
    await visit(page, lang === 'ar' ? '/ar/book/' : '/book/', lang);

    // Specialty is a real choice, not a hidden default.
    const specialty = page.locator('#b-specialty');
    await expect(specialty.locator('option').nth(1)).toBeAttached();
    await specialty.selectOption({ index: 1 });

    // Days arrive from the scheduler, not from hard-coded markup.
    await expect(page.locator(`#b-date option[value="${FUTURE_DATES[0]}"]`)).toBeAttached();
    await expect(page.locator('#b-date option[value=""]')).toHaveCount(1);

    // A taken slot is visible but not selectable.
    const taken = page.locator('.slot[data-time="09:30"]');
    await expect(taken).toBeDisabled();
    await expect(taken).toContainText('09:30');

    // Slots carry their timezone so the time read is the time stored.
    await expect(page.locator('.slot[data-time="10:00"] small')).toHaveText('AST');

    await page.locator('.slot[data-time="10:00"]').click();
    await expect(page.locator('.slot[data-time="10:00"]')).toHaveAttribute('aria-pressed', 'true');
    await expect(page.locator('#b-time')).toHaveValue('10:00');

    // Consent is mandatory and the submit is refused without it.
    await page.locator('#b-name').fill('QA Person');
    await page.locator('#b-email').fill('qa@example.invalid');
    await page.locator('form button[type="submit"]').click();
    await expect(page.locator('#b-confirm')).toBeHidden();
    expect(sent).toHaveLength(0);

    await page.locator('#b-consent').check();
    await page.locator('form button[type="submit"]').click();

    await expect(page.locator('#b-confirm')).toBeVisible();
    await expect(page.locator('#b-ref')).toContainText('book-qa-0001');
    await expect(page.locator('#b-ics')).toHaveAttribute('href', /calendar\.ics$/);

    expect(sent).toHaveLength(1);
    const body = sent[0];
    expect(body).toMatchObject({ time: '10:00', date: FUTURE_DATES[0], timezone: 'AST', email: 'qa@example.invalid', lang });
    expect(body.specialty).toBeTruthy();
    expect(body.consent).toBeTruthy();
    // The summary the visitor reads is the record the server returned.
    await expect(page.locator('#b-summary')).toContainText('10:00');
  });
}

test('changing timezone re-reads the schedule instead of relabelling stale slots', async ({ page }) => {
  const calls = [];
  await page.route(
    (url) => url.pathname === '/api/booking/slots',
    (route) => {
      const tz = new URL(route.request().url()).searchParams.get('timezone') || 'AST';
      calls.push(tz);
      route.fulfill({
        contentType: 'application/json',
        body: JSON.stringify({
          accepted: true, dates: FUTURE_DATES, date: FUTURE_DATES[0], timezone: tz,
          slots: [{ time: tz === 'EET' ? '08:00' : '09:00', available: true }],
        }),
      });
    },
  );
  await visit(page, '/book/');
  await expect(page.locator('.slot').first()).toContainText('09:00');
  await page.locator('#b-tz').selectOption('EET');
  await expect(page.locator('#b-tz')).toHaveValue('EET');
  await expect(page.locator('.slot').first()).toContainText('EET');
  expect(calls).toContain('EET');
});

test('scheduler outage falls back to a manual request and never claims a booking', async ({ page }) => {
  await page.route((url) => url.pathname === '/api/booking/slots', (r) => r.fulfill({ status: 503, body: 'down' }));
  await visit(page, '/book/');
  const status = page.locator('#b-status');
  await expect(status).toContainText(/could not confirm|لم نتمكن/i);
  await expect(page.locator('#b-confirm')).toBeHidden();
  await expect(status.locator('a[href^="mailto:"]')).toBeVisible();
});

test('a slot taken between load and submit asks for another slot', async ({ page }) => {
  await page.route((url) => url.pathname === '/api/booking/slots', (route) => route.fulfill({
    contentType: 'application/json',
    body: JSON.stringify({ accepted: true, dates: FUTURE_DATES, date: FUTURE_DATES[0], timezone: 'AST', slots: [{ time: '10:00', available: true }] }),
  }));
  await page.route((url) => url.pathname === '/api/booking', (route) => route.fulfill({
    status: 409, contentType: 'application/json', body: JSON.stringify({ accepted: false, error: 'slot unavailable' }),
  }));
  await visit(page, '/book/');
  await page.locator('#b-specialty').selectOption({ index: 1 });
  await page.locator('.slot[data-time="10:00"]').click();
  await fillDetails(page);
  await page.locator('form button[type="submit"]').click();
  await expect(page.locator('#b-status')).toContainText(/just taken|حُجز للتو/i);
  await expect(page.locator('#b-confirm')).toBeHidden();
});

test('every booking CTA across the site points at /book/, never an external scheduler', async ({ page }) => {
  const routes = ['/', '/services/', '/technology-services/', '/creative-services/', '/healthcare/', '/pricing-faq/', '/contact/', '/team/', '/about/', '/work/', '/ar/', '/ar/healthcare/'];
  for (const route of routes) {
    await visit(page, route, route.startsWith('/ar/') ? 'ar' : 'en');
    const hrefs = await page.locator('main a[href]').evaluateAll((els) => els.map((e) => e.getAttribute('href')));
    const booking = hrefs.filter((h) => /#book|\/book\//.test(h));
    expect(booking.length, `${route} has no booking CTA`).toBeGreaterThan(0);
    for (const href of booking) {
      expect(href, `${route} books somewhere else`).not.toMatch(/calendly|cal\.com|savvycal|hubspot|wa\.me|whatsapp/i);
    }
  }
});

/* ------------------------------------------------------- 2 · server truth */
test('server: a confirmed booking is a stored booking, a CRM record and a calendar file', async () => {
  const dir = mkdtempSync(join(tmpdir(), 'cc-booking-'));
  const api = createApi({ root: ROOT, env: { ...process.env, CC_DATA_DIR: dir, CC_ADMIN_TOKEN: 'qa-token' } });
  const server = createServer((req, res) => api.handle(req, res, new URL(req.url, 'http://127.0.0.1')));
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
  const base = `http://127.0.0.1:${server.address().port}`;
  const post = async (path, body) => {
    const res = await fetch(base + path, {
      method: 'POST', headers: { 'Content-Type': 'application/json', Origin: base, 'Sec-Fetch-Site': 'same-origin' },
      body: JSON.stringify(body),
    });
    return { status: res.status, json: await res.json().catch(() => null) };
  };
  try {
    const schedule = await (await fetch(`${base}/api/booking/slots?timezone=AST`)).json();
    const date = schedule.dates[0];
    const slot = schedule.slots.find((s) => s.available);

    const booked = await post('/api/booking', {
      name: 'QA Person', email: 'qa@example.invalid', specialty: 'brand',
      date, time: slot.time, timezone: 'AST', consent: 'on', lang: 'en', notes: 'Automated QA, not a real appointment.',
    });
    expect(booked.status).toBe(201);
    expect(booked.json.accepted).toBe(true);
    expect(booked.json.id).toMatch(/^book-/);

    // The instant is UTC and matches the wall clock the visitor chose.
    expect(booked.json.utc).toBe(slot.utc);

    // The slot is gone for the next visitor.
    const after = await (await fetch(`${base}/api/booking/slots?timezone=AST&date=${date}`)).json();
    expect(after.slots.find((s) => s.time === slot.time).available).toBe(false);

    // The calendar file starts at the booked instant.
    const ics = await (await fetch(base + booked.json.calendarUrl)).text();
    const utcStamp = slot.utc.replace(/[-:]/g, '') + '00';
    expect(ics).toContain(`DTSTART:${utcStamp}Z`);
    expect(ics).toContain('BEGIN:VALARM');

    // A CRM record exists, is qualified, and links back to the booking.
    const leads = await (await fetch(`${base}/api/leads`, { headers: { Authorization: 'Bearer qa-token' } })).json();
    const lead = (leads.leads || leads).find((l) => l.email === 'qa@example.invalid');
    expect(lead).toBeTruthy();
    expect(lead.stage).toBe('qualified');
    expect(lead.bookingId).toBe(booked.json.id);

    // And the booking itself is stored with its reference.
    const bookings = await (await fetch(`${base}/api/bookings`, { headers: { Authorization: 'Bearer qa-token' } })).json();
    const stored = (bookings.bookings || []).find((b) => b.id === booked.json.id);
    expect(stored).toMatchObject({ date, time: slot.time, timezone: 'AST', durationMinutes: 30 });
    expect(stored.leadId).toBe(lead.id);
  } finally {
    await new Promise((resolve) => server.close(resolve));
    rmSync(dir, { recursive: true, force: true });
  }
});
