# Bifrost Implementation Specification

Status: repository bootstrap complete; implementation deferred

## Bootstrap slice

1. Create the private `danny/Bifrost` repository and `main` branch.
2. Establish the Go module path.
3. Record product, architecture, safety, and recovery boundaries.
4. Verify clean Git state and exact local/remote ref equality.

## Required design work before runtime code

- pin supported distribution, kernel, Go, CPU architecture, and image targets
- define canonical configuration schema and migration rules
- define management identity, authorization, session, and recovery contracts
- define `nftables` and netlink runtime-boundary behavior and hard limits
- define last-known-good, confirmation timer, rollback, and interrupted-upgrade
  behavior
- define independent correctness oracles for compiled and applied policy
- decompose the first narrow vertical slice

## First candidate vertical slice

The preferred first runtime slice is an offline, pure configuration validator
and deterministic policy compiler for a deliberately tiny firewall schema. It
must produce reviewable output and golden tests without modifying the host
network. Host mutation, daemonization, and web administration remain later
slices.

## Requirement-to-verification map

| Requirement | Planned verification |
| --- | --- |
| BFR-PRD-001 | compiler golden tests plus isolated network-namespace apply/oracle tests |
| BFR-PRD-002 | schema, migration, audit, and rollback tests |
| BFR-PRD-003 | partial-failure and last-known-good recovery tests |
| BFR-PRD-004 | authorization, exposure, confirmation-timer, and console-recovery tests |
| BFR-PRD-005 | adapter contracts, integration tests, and health-state tests |
| BFR-PRD-006 | signature, preflight, interruption, and rollback tests |
| BFR-PRD-007 | secret-storage, export, logging, and redaction tests |
| BFR-PRD-008 | pinned build and integration matrix |
