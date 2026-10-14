# Implementation checklist — Code & Canvas native homepage

## 1. Standalone private native-code project — complete
- [x] Create the Code & Canvas rebuild as an independent private GitHub repository, separate from `3boalazm/aboalazm-os`.
- [x] Preserve the existing Code & Canvas production website and its domain; do not publish, replace, redirect, or change DNS for the live site during this task.
- [x] Implement the page as native website code, not WordPress.

## 2. Complete responsive homepage aligned to the references — in progress
- [x] Rebuild the supplied Code & Canvas homepage as a long-form, responsive page for desktop and mobile.
- [x] Follow the supplied page screenshot and the previously approved interactive presentation's visual direction: dark canvas, purple glow, luminous teal accents, restrained glass-like cards, readable typography, and controlled motion.
- [ ] Apply additional visual touches from the CanvasOne ERP presentation: use a split, dashboard-style hero panel built from existing Code & Canvas approach content; add the original brand mark, ambient violet/teal lighting, restrained floating glass callouts, scroll progress and active-section navigation, pointer-responsive light/tilt, and subtle section reveals. Respect reduced-motion settings and do not invent business metrics, clients, or claims.
- [x] Preserve Code & Canvas's existing identity and the content currently visible at `https://codeandcanvas.net/`.

## 3. Preserve accurate commercial content and navigation — complete
- [x] Include the real current content for brand, technology, data, and healthcare services and solutions, including the shown prices, timelines, metrics, advantages, and contact methods.
- [x] Use only claims, facts, numbers, prices, contact details, and destinations that already exist on the current website; do not invent testimonials, clients, or other facts.
- [x] Provide clear navigation to page sections and the genuine contact destinations already present.

## 4. Provide the full requested homepage journey — complete
- [x] Include the “Business Development By Design” opening section and primary calls to action.
- [x] Include the current metrics and featured offers, integrated services and industry solutions, customizable-package contact invitation, differentiators/how the studio works, next-step choices, and a complete footer with existing real information and links.

## 5. Accessible, usable interactions — complete
- [x] Provide keyboard navigation, visible focus states, suitable contrast, and reduced-motion support.
- [x] Ensure the page remains usable and legible on phone and desktop layouts.
- [x] Use balanced animation and clear calls to action.

## 6. Verify the build and keep the deliverable in preview — in progress
- [ ] Rebuild and verify the updated desktop and mobile layouts and interactive touches.
- [x] Deliver source in the new private repository and a preview link if available.
- [x] Do not treat a preview as production publication or change the production site/domain without a separate explicit request.

## Existing verified behavior
- The earlier static build succeeded with no install-time dependencies.
- Before the latest visual update, the homepage and `manus-routes.json` returned HTTP 200 in local and WebDev preview.
- Before the latest visual update, browser checks at 320, 360, 390, 768, 1024, and 1440 CSS pixels showed no horizontal overflow or broken on-page anchors.
- Before the latest visual update, desktop/mobile browser runs reported no page errors; the mobile menu and 6/4/5 service filters behaved as intended.
