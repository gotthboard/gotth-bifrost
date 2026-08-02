# Bifrost (BFW) Implementation Specification

Status: meta-repository bootstrap complete; component implementation deferred

## Phase 0 dependency gate

Finish and admit the cross-platform `rpc-plugin-system` lifecycle substrate and
the `agent-keyring`, `agent-filesystem`, and `agent-exec` provider substrates
before any Bifrost runtime implementation begins.

Required exit evidence:

- Unix-domain-socket and Windows-named-pipe transports behind one documented
  compatibility contract
- Linux, BSD/macOS, and Windows peer-identity backends with fail-closed tests
- explicit protocol/capability version negotiation and compatibility matrix
- externally consumable, versioned Go SDK/module
- matching auth, generation, health, timeout, cancellation, restart, teardown,
  redaction, and append-only logging behavior on supported platforms
- crash/restart/endurance evidence proving stale generations and transports do
  not remain trusted
- clean independent review and admission decision
- cross-platform `agent-keyring` service transport and peer-identity binding
- versioned external keyring SDK with explicit compatibility negotiation
- cross-platform encrypted-payload storage and unlock/recovery contract
- lease and opaque-reference scope, expiry, revocation, rotation, restart,
  restore, and stale-generation tests
- raw-export-denied, non-loggable response, redaction, export, support-bundle,
  and audit-correlation tests
- cross-platform `agent-filesystem` scope, path normalization, symlink/reparse
  point, race safety, atomicity/durability, COW/trash recovery, bounds, SDK, and
  audit/redaction evidence
- cross-platform `agent-exec` executable identity, argv/shell separation,
  account, environment, filesystem containment, sandbox, network/resource,
  timeout/cancellation, process-tree, lifecycle-ref, SDK, and audit/redaction
  evidence
- composition tests proving keyring, filesystem, and execution authority cannot
  be exchanged, widened, inferred, or reused across provider boundaries

Bifrost design work may refine requirements and contracts during Phase 0. It
must not add runtime code, provider-local substrate forks, or host-network
mutation before this gate passes.

## Bootstrap slice

1. Create the private `danny/Bifrost` repository and `main` branch.
2. Establish it as the product meta repository with no product Go module.
3. Record product, component, architecture, safety, and recovery boundaries.
4. Define planned component/dependency ownership and pinning rules.
5. Verify clean Git state and exact local/remote ref equality.

All future public CLI commands, package/configuration keys, protocol labels,
and compatibility identifiers use the lowercase `bfw` namespace. Final daemon
and web-service executable names are selected together in the versioned public
interface design; provisional working names do not create compatibility.

## Required design work before runtime code

- pin supported OS releases, kernels/runtime APIs, Go, CPU architectures, and
  image/installer targets
- define canonical configuration schema and migration rules
- define management identity, authorization, session, and recovery contracts
- define the platform-neutral policy IR and native backend contracts
- define `nftables`/netlink, FreeBSD `pf`, and Windows Filtering Platform
  runtime-boundary behavior and hard limits for admitted targets
- define signed plugin manifests, package provenance, compatibility,
  permissions, migrations, activation, removal, and rollback
- define the required cross-platform `rpc-plugin-system` substrate evolution
- define `agent-keyring` selectors, core-admission proofs, lease and opaque-ref
  scopes, credential classes, revocation, rotation, recovery, and
  cross-platform substrate evolution
- define `agent-filesystem` scopes for generated configuration, import/export,
  backup, diagnostics, and support artifacts without exposing canonical state
  or keyring storage
- define `agent-exec` envelopes for the minimal commands that cannot use native
  APIs, including denial defaults and cross-platform process semantics
- define typed, bounded, separately admitted data transfer between keyring,
  filesystem, and execution providers
- define the independent unprivileged web-service and `bfw` CLI contracts over
  one authenticated, versioned core API
- define the signed plugin UI manifest, declarative schema/component contract,
  sanitized UI catalog, route namespace, permissions, asset digest model, and
  compatibility negotiation
- define custom-bundle separate-origin sandbox, CSP, capability-message,
  data-bound, and denial contracts
- define atomic backend/UI/schema/migration/asset activation and rollback plus
  disabled, incompatible, unhealthy, and web-failure behavior
- define the meta-repository release composition schema, immutable component
  pins, compatibility evidence, migration order, and rollback pairing
- define the `bfw-routing` domain model, typed plan, platform-adapter,
  apply/verify, ordering, failure, recovery, UI, and audit contracts without
  implementing them in this repository
- define the OIDC provider profile, Authorization Code + PKCE flow, discovery
  and token validation, key rotation, explicit claim mapping, assurance/step-up,
  keyring use, opaque local sessions, logout/revocation, outage, audit, and
  local-console recovery contracts
- define last-known-good, confirmation timer, rollback, and interrupted-upgrade
  behavior
- define independent correctness oracles for compiled and applied policy
- decompose the first narrow vertical slice

## First candidate vertical slice

The preferred first runtime slice is an offline, pure configuration validator
and platform-neutral policy compiler for a deliberately tiny firewall schema.
It must produce one canonical IR plus deterministic golden outputs for at least
two platform adapters without modifying the host network. Plugin execution,
host mutation, daemonization, and web administration remain later slices.

## Requirement-to-verification map

| Requirement | Planned verification |
| --- | --- |
| BFW-PRD-000 | naming lint for full name Bifrost, `BFW` firewall shorthand, `bfw` public namespace, and absence of competing shorthand |
| BFW-PRD-001 | canonical IR golden tests plus per-platform compiler and isolated apply/oracle tests |
| BFW-PRD-002 | schema, migration, audit, and rollback tests |
| BFW-PRD-003 | partial-failure and last-known-good recovery tests |
| BFW-PRD-004 | authorization, exposure, confirmation-timer, and console-recovery tests |
| BFW-PRD-005 | adapter contracts, integration tests, and health-state tests |
| BFW-PRD-006 | signature, preflight, interruption, and rollback tests |
| BFW-PRD-007 | secret-storage, export, logging, and redaction tests |
| BFW-PRD-008 | pinned build and integration matrix |
| BFW-PRD-009 | process isolation, generation, authority-boundary, and failure-isolation tests |
| BFW-PRD-010 | signature, provenance, permission, migration, activation, and rollback tests |
| BFW-PRD-011 | protocol negotiation and backward/forward compatibility matrix |
| BFW-PRD-012 | crash/restart/upgrade tests proving last-known-good policy remains active |
| BFW-PRD-013 | cross-platform substrate admission record and independent review |
| BFW-PRD-014 | secret-location scan plus configuration, database, log, export, UI, plugin, and support-bundle redaction tests |
| BFW-PRD-015 | negative tests proving no credential or caller identity bypasses core action admission |
| BFW-PRD-016 | lease/ref scope, generation, target, audience, expiry, and raw-export-denied tests |
| BFW-PRD-017 | rotation, revocation, restore, restart, policy-change, and stale-generation invalidation tests |
| BFW-PRD-018 | cross-platform keyring compatibility, storage/unlock, recovery, SDK, and independent admission record |
| BFW-PRD-019 | filesystem scope, path, bounds, link/special-file, mutation-precondition, generation, expiry, and audit tests |
| BFW-PRD-020 | secret/provider-state denial plus destructive-class and recoverability tests |
| BFW-PRD-021 | complete process-envelope validation and negative spawn tests |
| BFW-PRD-022 | shell, PATH/env, credential, network, privilege, raw-handle denial and native-API boundary tests |
| BFW-PRD-023 | cross-provider confused-deputy, stale-generation, type/bounds, ref-reuse, and correlation tests |
| BFW-PRD-024 | cross-platform filesystem/exec compatibility, safety, lifecycle, SDK, and independent admission record |
| BFW-PRD-025 | privilege, direct-access, restart-isolation, and shared-core-API tests for web and CLI clients |
| BFW-PRD-026 | signed UI-manifest schema, compatibility, namespace, permission, localization, and asset-digest tests |
| BFW-PRD-027 | provenance/schema/migration/asset verification plus sanitized authorization-filtered catalog tests |
| BFW-PRD-028 | declarative form/table/status/validation/confirmation/accessibility/error golden tests |
| BFW-PRD-029 | typed-action admission, identity, confirmation, audit, idempotency, generation, and rollback tests |
| BFW-PRD-030 | hostile custom-bundle tests for origin, CSP, cookie/token, DOM, network, filesystem, socket, and capability escape |
| BFW-PRD-031 | staged activation, crash interruption, version skew, cache integrity, atomic publish, and rollback tests |
| BFW-PRD-032 | disabled/removed/incompatible/untrusted route denial and unhealthy read-only diagnostic tests |
| BFW-PRD-033 | web-down local CLI recovery tests proving the same core admission path is used |
| BFW-PRD-034 | web/UI crash, restart, and upgrade tests proving packet policy and core authority remain intact |
| BFW-PRD-035 | repository-content and release-governance checks proving the meta repo contains no product runtime |
| BFW-PRD-036 | component ownership, immutable pin, no-source-copy, and independent-versioning checks |
| BFW-PRD-037 | routing ownership tests proving no routing implementation or domain policy resides in core |
| BFW-PRD-038 | routing plan determinism, admission, idempotency, platform apply/oracle, boundary, and rollback tests |
| BFW-PRD-039 | signed release composition, exact revision, compatibility, migration-order, evidence, and rollback-pair checks |
| BFW-PRD-040 | generic OIDC conformance plus Authentik integration tests without provider-specific authority |
| BFW-PRD-041 | authorization-code/PKCE, redirect, TLS, state, nonce, and bounded-transaction tests |
| BFW-PRD-042 | hostile issuer/JWKS/algorithm/audience/azp/nonce/time/assurance and key-rotation tests |
| BFW-PRD-043 | issuer-subject role mapping, deny-default, claim-change, and no-auto-admin tests |
| BFW-PRD-044 | keyring mediation and secret/token absence scans across config, env, argv, logs, exports, browser, UI, and plugin surfaces |
| BFW-PRD-045 | opaque-cookie, Secure/HttpOnly/SameSite, rotation, inactivity, absolute-expiry, logout, and CSRF tests |
| BFW-PRD-046 | plugin-boundary tests proving no raw OIDC token or provider session crosses the core |
| BFW-PRD-047 | issuer/client/origin/algorithm/claim/assurance pinning and forwarded-header denial tests |
| BFW-PRD-048 | provider/JWKS outage tests for new-login denial and bounded existing-session behavior |
| BFW-PRD-049 | isolated local-console recovery and no-remote-fallback tests during identity/network failures |
| BFW-PRD-050 | redacted authentication, mapping, session, logout, denial, recovery, and policy-change audit tests |
