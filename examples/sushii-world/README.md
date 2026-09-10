# Sushii World reference briefing

This directory is the canonical visual reference for the Sushii World briefing experience. `sushii-world-presentation.html` is a self-contained, offline presentation: it includes the watercolor sushi-roll illustrations, wrapper callouts, bento-box composition, stacked jubako model, connection surfaces, adapters, and the Kitchen / Legal / Deck handoffs.

## Why it lives in `sushi-deck-kit`

`@binarylawyer/sushi-deck-kit` is the reusable Deck engine and data format. The HTML file belongs here as a reference artifact and design fixture, alongside the kit's JSON examples. It is not a second presentation runtime and it does not replace the product app.

The product boundary is:

| Repository | Role |
| --- | --- |
| `sushi-deck-kit` | Portable runtime, blocks, `DeckJson`, storage/API contracts, and the canonical Sushii World reference artifact. |
| `sushi-deck-client` | Product shell: gallery, admin editor, API consumer, present/scroll/PDF routes. |
| `sushi-deck-backend` | Eventual extracted API + database service; currently the client hosts the API tier. |

## Sushii World ownership model

- **Kitchen** builds and operates systems.
- **Legal / Law** own domain workflows and substantive conclusions.
- **Deck** assembles, explains, reviews, versions, and hands off the work.

The originating workspace remains authoritative for its work. Deck owns the briefing, visual explanation, review history, and handoff—not Kitchen's system state or Legal's substantive conclusions.

## Migration path into the product

1. Keep this HTML as the visual source of truth while the native briefing is designed.
2. Add the missing asset/image primitive to the kit's `DeckJson` contract, keeping asset references separate from slide copy.
3. Express the briefing as versioned `DeckJson` and store it through the existing `/api/decks` surface.
4. Add a native client gallery entry and `/present/sushii-world` path rendered through `DeckRuntime`; use `ScrollView` for contextual review.
5. Retain this HTML as an offline review/export fixture even after the native deck is available.

Do **not** duplicate the full HTML into the client's `public/` directory. The kit owns the canonical reference artifact; the client consumes it through the package export.

## Artifact fidelity

The repository copy preserves the source presentation's 19-slide markup, CSS, JavaScript, speaker notes, interactive navigation, print mode, audience views, and offline behavior. To make the self-contained artifact practical to version and package, the four embedded PNG data images (three unique 1672×941 watercolor illustrations) are re-encoded as high-quality WebP data images without changing their dimensions or presentation structure.

For provenance, the unmodified source artifact supplied for this integration has SHA-256 `591983882d7ab2629a44a4192d077d62f95e5834727832bdf0363418062b2dc6`.