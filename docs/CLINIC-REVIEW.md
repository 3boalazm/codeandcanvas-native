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
