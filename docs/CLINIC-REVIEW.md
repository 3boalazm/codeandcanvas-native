# Dr Amro clinic review

Share `/clinic-review/` on the deployed studio domain. This is an Arabic, mobile-first client intake and prototype feedback wizard, not a patient booking engine. It is a deliberately standalone, hand-authored microsite (not a generated marketing page); edit `clinic-review/index.html` and `assets/{css,js}/clinic-review.*` directly. The existing build copies the route and assets automatically. Do not add to sitemap or public navigation.

- Prototype opens externally at https://prototype-ttxw.vercel.app/.
- All questions optional; unanswered questions appear as “نحدده معًا”. No clinic policies or prices are assumed.
- Versioned localStorage draft, capped field lengths; explicit clear action. No server submission, database, analytics, automatic notifications or patient data collection.
- Review before explicit WhatsApp handoff to the project's Egyptian WhatsApp contact (+201092500454), explicitly selected by the studio for this review. Shared site contact details are unchanged.
- WhatsApp messages above 3500 characters use a short introduction; the UI explicitly instructs downloading and attaching the text file. Copy and UTF-8 text download are always available as alternatives. Opening WhatsApp is never labelled successful delivery.
- `noindex, nofollow` reduces discoverability, but is NOT authentication. Anyone with the URL can open this page. Don't store secrets or patient data here.
- Photo/credentials can be sent separately in the studio conversation; this page does not upload files.

Suggested invitation:
> دكتور عمرو، مساء الخير 🌿 جهزنا لحضرتك مساحة صغيرة من Code & Canvas تشوف فيها نسخة التطبيق وتقول لنا رأيك، ونظبط تفاصيل الحجز على طريقة شغل العيادة. الأسئلة بسيطة، ومش لازم تجاوب عليها كلها مرة واحدة؛ الإجابات بتتحفظ على نفس الجهاز. وفي الآخر تقدر تبعتها لنا على واتساب. أي تفاصيل لسه مش جاهزة نكمّلها سوا.

## Structured choices update
- Per-weekday undecided/working/closed selectors, time pickers and optional break ranges. No preselected clinic schedule or policy. Times are same-day, clinic-local; overnight or split shifts go in schedule notes.
- Working days require start/end and a valid, ordered break inside the working period before advancing to review. Copy-hours action applies to already-selected working days only.
- Numeric service fees and patient capacity; duration, follow-up, booking-window, cancellation, administration and payment choices; multi-select reminders and necessary patient fields. Free-text notes remain for exceptions and “other”.
- Draft v1 is retained. Old combined free-text answers are shown as editable legacy notes when present, and included in review/export. Closed or undecided days do not export stale hours.

## Conditional details and optional intake
- A persistent introductory notice states that all information is optional and questions may be skipped.
- Follow-up price appears only for paid follow-ups; duration/window/notes only for available follow-ups. Online price/duration require online availability. Same-day cutoff, cancellation notice, additional branches, payment details, existing-system name, different reception hours, and age-data justification follow their relevant parent choices.
- Hidden controls are disabled and excluded from review/copy/download/WhatsApp reports. Draft values are retained locally so changing a choice back restores prior details.
- Partially filled working hours may now be skipped. Contradictory supplied ranges still show a correction message; missing times export as unspecified.

## Named doctor questionnaires
- `/amro-alahawany-review/`: دكتور عمرو الأهواني, original prototype.
- `/osama-shoier-review/`: دكتور أسامة شعير, prototype https://dr-osama-shoier.vercel.app/index.html.
- `/clinic-review/` remains an Amro alias for existing shared links and drafts.
- Shared JS uses a fixed `data-doctor` profile allowlist. Draft keys, downloaded filenames, report headings and long-message WhatsApp introductions are doctor-specific. Both use the existing studio recipient +201092500454.
- All three HTML pages are standalone, hand-authored, noindex pages; update common markup consistently. No additional clinic services, prices or policies have been assumed for Osama.
