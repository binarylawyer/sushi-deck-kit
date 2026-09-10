# Sushii World reference briefing

This directory is the canonical visual reference for the Sushii World briefing experience. `sushii-world-presentation.html` contains the complete 19-slide presentation markup, interaction model, speaker notes, print mode, and audience views. Its three watercolor illustrations live beside it in `assets/` so the reference can be versioned cleanly and consumed by the Sushi Deck client without duplicating a 12 MB data-URI file.

The directory remains offline-capable: the HTML uses only relative, repository-owned assets and does not depend on GitHub, Vercel, a CDN, or another network service to render the presentation.

## Why it lives in `sushi-deck-kit`

`@binarylawyer/sushi-deck-kit` is the reusable Deck engine and data format. The Sushii World reference belongs here as a design fixture and canonical artifact, alongside the kit's JSON examples. It is not a second presentation runtime and it does not replace the product app.

The product boundary is:

| Repository | Role |
| --- | --- |
| `sushi-deck-kit` | Portable runtime, blocks, `DeckJson`, storage/API contracts, and the canonical Sushii World reference artifact and artwork. |
| `sushi-deck-client` | Product shell: gallery, admin editor, API consumer, present/scroll/PDF routes, and the Vercel route that serves the installed reference. |
| `sushi-deck-backend` | Eventual extracted API + database service; currently the client hosts the API tier. |

## Sushii World ownership model

- **Kitchen** builds and operates systems.
- **Legal / Law** own domain workflows and substantive conclusions.
- **Deck** assembles, explains, reviews, versions, and hands off the work.

The originating workspace remains authoritative for its work. Deck owns the briefing, visual explanation, review history, and handoff—not Kitchen's system state or Legal's substantive conclusions.

## Migration path into the product

1. Keep this reference as the visual source of truth while the native briefing is designed.
2. Add a first-class asset/image primitive to the kit's `DeckJson` contract, keeping asset references separate from slide copy.
3. Express the briefing as versioned `DeckJson` and store it through the existing `/api/decks` surface.
4. Add a native client gallery entry and `/present/sushii-world` path rendered through `DeckRuntime`; use `ScrollView` for contextual review.
5. Retain this HTML directory as an offline review/export fixture and regression reference even after the native deck is available. A single-file export can inline the same package-owned assets when needed.

Do **not** duplicate the full HTML or the artwork into the client's `public/` directory. The kit owns the canonical reference; the client consumes package exports and serves them through its Node/Vercel routes.

## Artifact fidelity

The repository copy preserves the supplied presentation's 19 slide sections (`s1` through `s19`), CSS, JavaScript, speaker notes, interactive navigation, print mode, audience views, wrapper callouts, bento composition, jubako model, adapters, and connection surfaces.

The only media refactor is storage: the source's four inline PNG data references contain three unique 1672×941 watercolor images, one of which is used twice. Those three unique images are re-encoded as high-quality WebP files at the same dimensions and referenced relatively from the HTML. No external asset URL is introduced.

For provenance, the unmodified source artifact supplied for this integration has SHA-256 `591983882d7ab2629a44a4192d077d62f95e5834727832bdf0363418062b2dc6`.
