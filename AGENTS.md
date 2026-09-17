# Sushi Deck Kit — Repository Agent Instructions

These instructions apply to the entire `binarylawyer/sushi-deck-kit` repository.

## 1. Repository role

This repository is a portable Deck behavior-contract and compatibility/source repository during consolidation into `binarylawyer/sushii-deck`.

The exact commit exercised by the accepted ARCH-10 runtime was:

```text
d49546d800ae0afe35c9672d7624f503811da94c
```

ARCH-10 / SUSHII-DL is CLOSED at 52/52 in `binarylawyer/sushii-world`.

This proof binds the exact commit above. It does not automatically prove every later `main` commit.

Read `README.md`, `docs/SUSHII-DL-COMPATIBILITY-STATUS-2026-09-17.md`, current `main`, open PRs, and relevant Sushii Deck architecture before changing public behavior contracts.

## 2. Compatibility preservation

Do not delete/archive this repository or silently replace its public contracts merely because `sushii-deck` passed ARCH-10 runtime acceptance.

Behavior remains evidence-bearing until the Deck consolidation audit proves required public/open-core capability has been migrated, intentionally retained or retired.

Changes to `DeckStore`, API handlers, `DeckJson`, generation interfaces, tenancy/owner scoping or portable behavior may affect the first-party Deck subject and must be reviewed as compatibility-contract changes.

## 3. CI classification

Classify CI from actual execution:

- `CI_PASS`: required relevant steps executed and passed.
- `CI_FAIL`: a required relevant build/test/check step actually executed and failed.
- `CI_DEFERRED`: CI could not exercise the source.

A job with:

```text
runner_id=0
runner_name empty
steps=[]
```

is `CI_DEFERRED` even when the GitHub conclusion string is `failure`. No test ran.

Likewise `startup_failure` with zero jobs is `CI_DEFERRED`.

Deferred is never PASS. Preserve exact merged SHAs for later backfill; a later real FAIL requires a corrective PR.

## 4. Fresh cost approval

Stop for fresh explicit product-owner approval immediately before creating or purchasing any new billable, recurring or usage-charged resource, including hosted services, domains, cloud resources, paid DBs/branches, subscriptions or metered provider activation.

Repository implementation authority does not imply cost authority.

## 5. Exact-SHA evidence

When claiming compatibility/runtime acceptance, state the exact commit and any downstream subject pin. Do not represent later `main` as accepted unless the relevant gate actually ran against that basis.

Terminal cross-repo receipts are:

```text
DL-08D  92a10ac06049a4253ebd6be1f9c9295b175d9ad972c84841d627376b3895a1cf
DL-08F  98794d4827196c6c2f2d61a6dbe9b57983e573aa02344ac83dd20e94d57db3a4
```

## 6. Runtime acceptance when this kit changes an aggregate

For Sushii Bento/Jubako/whole-stack work, use the accepted A0-A14 aggregate acceptance model unless superseded.

A healthy stack is not enough. Exercise direct/transitive workflow, persistence, isolation, repeatability, cleanup and receipt correlation as applicable.

Preserve the first failed stage and rerun the smallest necessary stage chain after a bounded fix.

## 7. Secrets

Never commit or paste `.env` contents, decrypted secret values, credential-bearing DB URLs, secret/service-role keys, private keys, bearer tokens/Authorization headers or generated passwords.

Use opaque secret references and sanitized evidence.

## 8. Public ingress / deployment

This kit is portable source, not authority to deploy a customer-facing service. ARCH-10 did not authorize a public hostname, DNS/TLS, Traefik, Keycloak/OIDC, CORS or customer traffic for this repository.

Permanent namespace/OPS decisions remain separate.

## 9. Documentation

Preserve dated evidence as historical snapshots. Keep README/current compatibility docs accurate when repository role or migration status changes.
