# Bifrost Implementation Specification

Status: repository bootstrap complete; implementation deferred

## Phase 0 dependency gate

Finish and admit the cross-platform `rpc-plugin-system` substrate before any
Bifrost runtime implementation begins.

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

Bifrost design work may refine requirements and contracts during Phase 0. It
must not add runtime code, provider-local substrate forks, or host-network
mutation before this gate passes.

## Bootstrap slice

1. Create the private `danny/Bifrost` repository and `main` branch.
2. Establish the Go module path.
3. Record product, architecture, safety, and recovery boundaries.
4. Verify clean Git state and exact local/remote ref equality.

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
| BFR-PRD-001 | canonical IR golden tests plus per-platform compiler and isolated apply/oracle tests |
| BFR-PRD-002 | schema, migration, audit, and rollback tests |
| BFR-PRD-003 | partial-failure and last-known-good recovery tests |
| BFR-PRD-004 | authorization, exposure, confirmation-timer, and console-recovery tests |
| BFR-PRD-005 | adapter contracts, integration tests, and health-state tests |
| BFR-PRD-006 | signature, preflight, interruption, and rollback tests |
| BFR-PRD-007 | secret-storage, export, logging, and redaction tests |
| BFR-PRD-008 | pinned build and integration matrix |
| BFR-PRD-009 | process isolation, generation, authority-boundary, and failure-isolation tests |
| BFR-PRD-010 | signature, provenance, permission, migration, activation, and rollback tests |
| BFR-PRD-011 | protocol negotiation and backward/forward compatibility matrix |
| BFR-PRD-012 | crash/restart/upgrade tests proving last-known-good policy remains active |
| BFR-PRD-013 | cross-platform substrate admission record and independent review |
