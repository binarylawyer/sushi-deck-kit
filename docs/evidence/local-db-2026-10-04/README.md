# Compatibility kit database backfill — 2026-10-04 UTC

The authorized Mac Mini ran the previously skipped storage suite against disposable PostgreSQL 16.15 and PostgREST 12.2.3. No hosted Supabase project, provider credential, production database, public port or production migration was used.

The historical CI inputs at #16 (`d0b1da49e965c643b42a0ce02f5c092c17a556cd`) and #17 (`9d1ab72f07cefd3a6f67cdab07a790f7049920a2`) match after excluding the changed compatibility prose and agent instructions. One local Node 20.20.0 run executed `npm ci`, typecheck and the default suite: 63 passed, one opt-in database placeholder skipped. This is local CI-component evidence, not a successful original GitHub run.

## Findings and correction

1. Enabling the database suite under Node 20 failed before storage execution: locked Supabase JS/realtime 2.110.1 requires Node >=22. The workflow now pins Node 22.22.0. Dependencies and the lockfile are unchanged. [Official runtime support notice](https://github.com/orgs/supabase/discussions/45715).
2. An initial direct-PostgREST setup lacked Supabase's `/rest/v1` routing prefix. That log is a harness setup failure, not a demonstrated storage defect. The retained bounded gateway supplies the REST prefix; it does not implement Supabase Auth.
3. With correct routing and Node 22, nine storage cases passed and two failed because `"nope"` is not a valid UUID. The missing-record fixtures now use the valid absent UUID from the already accepted Sushii Deck contract. Missing-record assertions remain; no production adapter or authorization rule changed.
4. Corrected database-only suite: **11 passed, zero skipped**. Full corrected typecheck and suite: **74 passed, zero skipped**. Owner tests in that total use mocks; this receipt does not claim production RLS or real two-tenant authorization acceptance.

The local migration recreates the kit's historical `public.decks` model in a disposable database and supplies a test-only `service_role`. This does not recreate that table in any production system or replace the canonical `sushii_deck` / `sushii_deck_app` boundary. DB-DECK-01 and accepted production receipts remain intact.

## Bounds and cleanup

Internal Docker network, no published ports. PostgreSQL and REST each: 0.5 CPU, 512 MiB, no additional swap, 128 PIDs. Test runner: 1 CPU, 1.5 GiB, no additional swap, 256 PIDs. Logs: 5 MiB × 2. PostgreSQL data: 256 MiB tmpfs; no durable test volume. Outer test timeout: 300 seconds. Only synthetic short-lived JWT/configuration is created, outside Git and removed after execution. Reserved containers and network were removed.

## Reproduction

Copy `run-kit-db.py` and `kit-rest-gateway.mjs` to a private directory **outside Git**. Install the unchanged lockfile inside a matching Linux Node container first; native macOS esbuild binaries are not a substitute for Linux dependencies. Invoke the retained Mac Mini reproducer with:

```sh
python3 /private/directory/run-kit-db.py rerun node:22.22.0-bookworm-slim /absolute/path/to/sushi-deck-kit
```

Use only a disposable checkout. The helper refuses an occupied reserved namespace, injects only its synthetic local credentials, and cleans up in `finally`. Its full suite verifies the corrected fixtures and typecheck. The ordinary no-database suite intentionally retains its opt-in skip; it is now reviewed and has real local storage evidence.

Logs preserve setup failures, the first actual UUID-fixture failures, and the successful correction. `file-digests.json` records retained log hashes. This backfill does not authorize publication, traffic cutover, provider activation or retirement of the compatibility repository.
