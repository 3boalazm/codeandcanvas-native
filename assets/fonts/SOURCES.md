# Font provenance

- **Space Grotesk** (display headings): `@fontsource/space-grotesk`, unmodified Latin WOFF2, SIL Open Font License 1.1 — `space-grotesk-OFL.txt`. Replaced Signate Grotesk on 2026-11-08 because its web-embedding permission was never confirmed. **This resolves the open font-licensing launch gate.**
- Alexandria: `@fontsource-variable/alexandria@5.3.0`, unmodified Arabic/Latin WOFF2 subsets, SIL OFL (`alexandria-OFL.txt`).
- IBM Plex Sans Arabic: `@fontsource/ibm-plex-sans-arabic@5.3.0`, unmodified WOFF2 subsets, SIL OFL (`ibm-plex-sans-arabic-OFL.txt`).
- Comfortaa: `@fontsource-variable/comfortaa@5.3.0`, unmodified Latin WOFF2 subset, SIL OFL (`comfortaa-OFL.txt`).
- Poppins and Raleway TTF/WOFF2 files predate this sprint and are distributed under the SIL OFL; the WOFF2 files are lossless web-compressed versions of the same font data. A formal license file copy is kept with the original asset pack by the brand owner.
- The unlicensed `signategrotesk-*` files were removed from the repository on 2026-11-08. No stylesheet, preload or generator references them; `scripts/check-claims.mjs` fails the publish gate if any HTML mentions Signate again.

No Google Fonts request is made at runtime. All faces are served from `/assets/fonts/`.
