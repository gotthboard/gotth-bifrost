# ADR-0005: Recovery model

Status: Accepted

Date: 2026-08-08

Requirements: BFW-PRD-002 through BFW-PRD-006, BFW-PRD-049, BFW-PRD-074, BFW-PRD-089

Supersedes: none

## Context

A firewall appliance must recover from bad policy, management lockout, failed
migration, power loss, and interrupted software activation without silently
opening traffic.

## Decision

Bifrost keeps verified last-known-good configuration and release records,
stages appliance updates into inactive A/B image slots where the platform
supports them, and activates only after preflight. Boot success is confirmed
within a bounded window; otherwise the prior slot is selected. Configuration
migrations retain a rollback-compatible snapshot and do not overwrite the last
known-good generation.

The local console can select the prior release/configuration pair, inspect
redacted diagnostics, and restore management access through typed recovery
actions. It cannot edit native firewall files or bypass audit. Network-sensitive
configuration uses `commit confirmed` and rolls back when confirmation is lost.

## Consequences

- Release storage must reserve two complete image slots plus bounded evidence.
- Platform boot-selection mechanics remain adapter-specific and require exact
  interruption tests before a platform is admitted.

## Alternatives considered

- In-place package upgrades: rejected because interruption recovery is weak.
- Configuration-only rollback: rejected because binary/schema skew remains.

## Verification

- Power-loss, failed-boot, failed-migration, lockout, console, and last-known-
  good selection exercises in the pinned test lab.
