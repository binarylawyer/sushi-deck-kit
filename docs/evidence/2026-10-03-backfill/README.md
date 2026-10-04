# Kit historical backfill and fixture correction — 2026-10-03

Basis: `9d1ab72f07cefd3a6f67cdab07a790f7049920a2` (PR #17). PR #16 at
`d0b1da49e965c643b42a0ce02f5c092c17a556cd` differs only in AGENTS.md;
source, dependency lock and CI inputs are identical.

The original Node 20.19.0 `npm ci`, typecheck and unit suite passed: 63 tests,
with the optional database suite skipped. Enabling that suite produced 11
failures before database access: the locked Supabase client requires native
WebSocket support absent from Node 20. CI now selects Node 22. The fixture
also uses a valid, absent UUID for missing-record update/delete assertions;
Postgres must reach the not-found behavior rather than reject invalid UUID
syntax. This is the same bounded correction already merged in Deck #55.
No storage implementation, public contract, owner boundary or accepted
ARCH-10 subject pin changed.

With both corrections, all 74 tests passed (9 files, zero skips) using Node
22.17.1 on the Mac Mini and disposable Linux/arm64 Postgres 16.15 plus
PostgREST 12.2.3. Existing repository migrations were applied. A loopback
path proxy adapts `/rest/v1` and strips dummy authentication headers. The
fixture exercises service-role database transport, not production JWT, RLS,
Realtime, hosted Supabase or deployment acceptance. No production service
was contacted. Native macOS Node is not a claim of Linux/x86 parity.

First failures are retained: the initial internal Docker network did not
publish the port; a private bridge with loopback-only publishing corrected
that setup. The subsequent Node 20 execution failure is retained separately.
Containers, network and proxy were removed after every run (cleanup JSON).
Only task-owned images are eligible for final cleanup.

Reproduction: use the locked dependencies (`npm ci`), Node 22, a disposable
Postgres/PostgREST instance with these migrations, and supply the two test
variables above before `npm test`. Ordinary CI intentionally still reports
the optional suite skipped without a database. These local receipts supply
that missing coverage; they do not relabel the original skipped CI run.
