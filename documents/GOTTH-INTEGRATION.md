# GOTTH Bifrost adoption contract

Date: 2026-10-02. Scope: BFW-PRD-229 through BFW-PRD-234.

This is the approved product-family and reuse direction, **not implementation
or dependency admission**. Bifrost remains a governance-only meta repository.
The runtime adoption feature is planned in `workflow.toml`; the existing
active feature and all alpha/Phase 0 decisions remain unchanged.

## Identity, source and compatibility

- Product: Bifrost; GOTTH display name: **GOTTH Bifrost**.
- Canonical source: private `gotthboard/gotth-bifrost` on Forgejo.
- Public one-way mirror and bug tracker: `github.com/gotthboard/gotth-bifrost`.
- Confidential security reports: the GitHub private vulnerability form in
  [SECURITY.md](../SECURITY.md), never a public issue or Forgejo ticket.
- License: MIT for this repository; dependencies keep their own notices.
- Preserve the original `danny/Bifrost` ancestry. Repository relocation is not
  a new product baseline, release, or loss of previous architectural work.
- Preserve `bfw`, `bfwd`, `bfw-web`, `BFW-PRD-*`, schema names, component IDs,
  existing ADRs and workflow identity. Repository names and protocol names are
  different contracts. Future Bifrost-specific source repositories should use
  the `gotth-bifrost-*` family; their `bfw-*` component IDs stay stable. Names
  remain proposals until component repositories are actually created.

## Reuse matrix

These are source observations on 2026-10-02, not runtime claims or approved
dependency pins. A tagged upstream version is not a Bifrost compatibility test.
The corresponding planned shared entries in `governance/components.toml` have
empty admitted revision/artifact fields. No optional candidate is added to a
required appliance composition simply by appearing here.

| Shared project | Observed availability | Intended Bifrost consumer and boundary |
| --- | --- | --- |
| [gotth-oidc](https://github.com/gotthboard/gotth-oidc) | Implemented, `v0.1.0` tag | First identity-library candidate for `bfw-identity`; storage-neutral protocol validation. Core retains role mapping and opaque sessions; keyring retains secrets. |
| [gotth-authentik](https://github.com/gotthboard/gotth-authentik) | Implemented, unreleased | Optional OIDC provider configuration/validation. Blueprint rendering is not remote application; generic OIDC remains supported. |
| [gotth-scim](https://github.com/gotthboard/gotth-scim) | Implemented, `v0.1.0` tag | Optional later provisioning adapter with a Bifrost-owned durable store, authenticated scope and revocation policy; no implicit network privilege. |
| [gotth-extensions](https://github.com/gotthboard/gotth-extensions) | Implemented control/compatibility foundation, unreleased | Reuse applicable manifest, capability and negotiation mechanisms behind an explicit mapping. Not an invocation bus, supervisor or replacement for signed BFW packages. |
| [gotth-jobs](https://github.com/gotthboard/gotth-jobs) | Implemented, PostgreSQL 17, unreleased | Optional controller background jobs. At-least-once execution requires product idempotency and unknown-outcome reconciliation; never the forwarding/fast-failover loop. |
| [gotth-webhooks](https://github.com/gotthboard/gotth-webhooks) | Implemented, unreleased; consumer evidence still required | Authorized outbound event delivery. Current contract is public HTTPS port 443, not private-LAN endpoints or inbound hooks. Bifrost owns destinations, event semantics, keys and receipts. |
| [gotth-portability](https://github.com/gotthboard/gotth-portability) | Implemented, unreleased | Bounded export/import mechanics for configuration and diagnostics. Bifrost owns authorization, redaction, schema, authentication/encryption, staged application and rollback. A hash is not authentication. |
| [gotth-release](https://github.com/gotthboard/gotth-release) | Implemented, unreleased | Deterministic archive and exact Git/SemVer mechanisms. Not a signer, appliance installer, boot verifier or updater; Bifrost retains those contracts. |
| [gotth-infrastructure](https://github.com/gotthboard/gotth-infrastructure) | Implemented, unreleased | Optional management-service container contracts; current one-container/port, nonprivileged model is not privileged appliance deployment or network orchestration. |
| [gotth-pg-migrate](https://github.com/gotthboard/gotth-pg-migrate) | Implemented, PostgreSQL 17, unreleased | Only for an explicitly selected PostgreSQL management service. Forward-only, application-owned migration history; schema/backup/rollback remain product-owned. Not a mandate to add PostgreSQL to nodes. |
| [gotth-stack](https://github.com/gotthboard/gotth-stack) | Non-mutating planning/journal foundation; no `apply` command | Future optional scoped management adapter. No existing Bifrost adapter, direct native network access, credential access or forwarding/recovery dependency is implied. |
| [gotth-sdk](https://github.com/gotthboard/gotth-sdk) | Placeholder, no importable module | Future shared public client/UI contracts, after real APIs exist. Not today's BFW domain SDK or `rpc-plugin-system` SDK. |
| [gotth-notify](https://github.com/gotthboard/gotth-notify) | Placeholder | Future channel-neutral notification mechanics; no dispatcher to consume today. |
| [gotth-media](https://github.com/gotthboard/gotth-media) | Placeholder | Optional future upload/object mechanics. Packet-capture authorization, quotas, retention and redaction remain Bifrost-specific. |
| [gotth-search](https://github.com/gotthboard/gotth-search) | Placeholder | Optional future search mechanics; access must be enforced before counts/results expose data. |
| [gotth-extension-markdown](https://github.com/gotthboard/gotth-extension-markdown) | Design only, no renderer/container | Optional future help/operator content: one Markdown/Mermaid/math extension. Host validates output and content access; local recovery never depends on it. |

Other GOTTH products are not automatic dependencies. Reuse is driven by a
concrete consumer contract, not by importing the entire family. Existing Go
modules inspected for this matrix declare Go 1.26.6; implementation must select
and verify an exact compatible toolchain rather than inherit a moving default.

## Authority and availability

```text
bfw CLI / GOTTH-style bfw-web / optional GOTTH Stack adapter
    -> Bifrost core API: actor, authorization, generation, preview, confirmation
    -> Bifrost typed domain plan and transaction coordinator
    -> rpc-plugin-system supervised BFW component
    -> admitted native OS adapter; verify / commit / rollback
```

1. Use the existing Go/templ + HTMX + Tailwind presentation approach in the
   unprivileged `bfw-web` component. Server-rendered essential workflows remain
   usable without JavaScript; progressive enhancement cannot bypass core
   authorization, confirmation, validation, output escaping or asset policy.
   Follow shared contracts where implemented; do not pretend `gotth-sdk` already
   provides an editor or reusable widget library.
2. `bfw-identity` owns the protocol boundary, not authorization. `gotth-oidc`
   can implement that boundary; Bifrost must still supply one-use login state,
   bounded caches, issuer/subject mapping, core-issued sessions, revocation,
   credential references and local-console recovery. Optional Authentik/SCIM
   integration must prove those same boundaries rather than auto-grant admin.
3. One supervisor owns executable identity, generations, liveness, teardown
   and recovery: `rpc-plugin-system`. Before using `gotth-extensions`, map the
   exact contracts, authentication/capability facts and failure states. No
   second supervisor, container runtime requirement, compatibility fiction or
   provider-local lifecycle fork is admitted by this document.
4. `agent-keyring` remains the credential authority. Shared code must not
   introduce environment-variable secrets, ordinary configuration payloads or
   plugin-owned stores. Host-file and process effects still require scoped
   `agent-filesystem`/`agent-exec` authority after core admission.
5. Management-service failure must not erase last-known-good packet policy,
   defeat commit-confirmed rollback, or disable local-console recovery.
   Remote OIDC, PostgreSQL, Stack, jobs, catalogs and optional renderers are
   outside the established forwarding path. Unavailable required management
   dependencies deny affected new mutations with explicit diagnostics.
6. Keep product-specific network compilation, routing/switching/firewall,
   native Go reverse proxy, GoKA, appliance installation, signed composition,
   image/boot rollback and packet/state oracles in their owning BFW components.
   GOTTH Stack's Caddy direction does not override Bifrost's no-Caddy proxy or
   no-Keepalived GoKA decisions.

## Adoption sequence and admission

1. Finish required existing design work and activate the applicable bounded
   component workflow. Choose a real upstream API and immutable source, review
   licenses and target/toolchain support, and map any missing mechanism.
2. Start with an offline identity integration slice using `gotth-oidc` inside
   `bfw-identity`; prove hostile-token, replay, secret isolation, core mapping,
   session expiry and provider-outage behavior. Do not create a duplicate OIDC
   library or place runtime code in this meta repository.
3. Build the minimal `bfw-web`/CLI-to-core slice with independently checked
   server-rendered requests, authorization and local recovery. Shared assets
   and contracts must be selected explicitly, not copied from Mail internals.
4. Add bounded portability/release mechanics, then optional controller jobs,
   notifications and Stack adapters only when their consumer scope is admitted.
   Missing generic mechanisms belong upstream; Bifrost adapters own only the
   domain-specific boundary and must not become permanent copied forks.
5. For each adopted candidate, update the authoritative component graph and
   release composition with the actual dependency edges, immutable revisions,
   artifact digests where applicable, platforms, compatibility, migration and
   rollback evidence. Record Bifrost consumer tests and independent admission.

BFW-ALPHA-0 and BFW-PHASE-0 remain blocked until their existing evidence gates
pass. This migration creates no runtime artifact, admitted dependency,
installer, release, deployment, broad feature activation or performance claim.

## Verification for this repository update

Run the existing governance validator, deterministic renderer check, governance
unit tests and patch/link checks. Review the new trace, dependency candidates
and exact preserved safety states independently. Repository history and mirror
parity are publication checks, not runtime proof. Current tests do not measure
shared-library correctness or automatically validate upstream API availability.
