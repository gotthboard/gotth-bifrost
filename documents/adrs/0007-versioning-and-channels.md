# ADR-0007: Versioning, compatibility, and update channels

Status: Accepted

Date: 2026-08-08

Requirements: BFW-PRD-011, BFW-PRD-031, BFW-PRD-039, BFW-PRD-089, BFW-PRD-215, BFW-PRD-221

Supersedes: none

## Context

Independently released components need predictable compatibility without an
unbounded promise to accept old or unknown wire behavior.

## Decision

Public API, schema, UI, CLI, and plugin contracts use semantic versions.
Compatible minor releases are additive; removals or semantic changes require a
major version and migration. An admitted core supports its own contract minor
and the immediately preceding minor unless a release manifest narrows that
window for a documented security reason. Required unknown behavior fails
closed; optional unknown fields are accepted only where the schema explicitly
allows extensions.

Update channels are `development`, `alpha`, `beta`, and `stable`, with separate
delegated signing scope and no automatic promotion. Alpha is a provisional
learning channel governed by ADR-0016; its artifacts and evidence cannot be
relabelled or promoted into beta or stable admission. Downgrade is denied
except to the exact signed rollback mate recorded in the active release.

## Consequences

- Compatibility suites must cover both supported minors and reject older,
  newer-required, or ambiguous behavior.
- Pre-1.0 draft contracts may change, but every change still updates schemas,
  fixtures, traceability, and release composition.

## Alternatives considered

- Indefinite backward compatibility: rejected as unsafe and untestable.
- Lockstep repository versions: rejected because components are independent.

## Verification

- Version-negotiation, supported-window, unknown-required-field, channel,
  promotion, downgrade, and rollback-mate tests.
