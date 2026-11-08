# Local SEO — KSA & Egypt (November 2026)

## What is published

| Market | Route | NAP record |
| --- | --- | --- |
| Saudi Arabia | `/saudi-arabia/` and `/ar/saudi-arabia/` | Al Khobar, KSA · +966 54 552 0750 · info@codeandcanvas.net · Sun–Thu 09:00–18:00 AST |
| Egypt | `/egypt/` and `/ar/egypt/` | Al Obour City, Egypt · +20 109 250 0454 · info@codeandcanvas.net · Sun–Thu 09:00–18:00 |

The same phone numbers, email, hours and language statement appear in the header, footer, `/contact/`, `/book/`, both market pages and the Organization JSON-LD. Each market page emits `ProfessionalService` schema with `areaServed`, `openingHoursSpecification` and a `parentOrganization` reference.

## What is deliberately NOT published

- **No street address.** The live WordPress content contained conflicting addresses (Riyadh / Al Khobar / Al Obour). Publishing one without owner confirmation would create an inconsistent NAP, which is worse than a city-level record.
- **No map pin, no embedded map, no Google Business Profile link** until the owner confirms the profile exists and matches these contact details.
- **No local reviews, testimonials or "clients in KSA" counts** without dated, permissioned evidence. `/claims/` lists what is required before any such claim can be added.
- **No fake branch photography.** `location-ksa.webp` and `location-eg.webp` are labelled abstract illustrations.

## Why this still helps

- Two crawlable, bilingual, internally linked market pages with unique copy about the actual briefs we see in each market.
- Consistent NAP across every page of the site.
- Structured data that names the cities and countries without inventing an address.
- Links from the homepage, footer, resources hub and both pages to each other and to the flagship service pages.

## Owner gates to complete local SEO

1. Confirm the legal entity name per country and the exact office city/address, if any.
2. Verify or create the Google Business Profile(s) and provide the URLs; then we add `sameAs` and a real map link.
3. Supply two permissioned local references or reviews with dates; then we add them with `Review`/`AggregateRating` only if eligible.
4. Confirm the working-hours timezone and holiday policy for each market.
5. Run `npm run verify:live` after deployment and re-check the two market URLs in Google Search Console.
