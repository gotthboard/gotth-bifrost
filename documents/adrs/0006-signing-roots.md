# ADR-0006: Signing roots and delegated roles

Status: Accepted

Date: 2026-08-08

Requirements: BFW-PRD-006, BFW-PRD-010, BFW-PRD-026, BFW-PRD-039, BFW-PRD-089

Supersedes: none

## Context

One online signing key would turn a build or repository compromise into product
authority and make rotation/recovery ambiguous.

## Decision

Bifrost uses an offline product root with threshold-controlled rotation and
separately scoped online delegated roles for release targets, metadata
freshness, plugin packages, and update channels. Release composition binds
artifact, SBOM, provenance, schema, migration, rollback, and evidence digests.
The core trusts only explicitly configured root generations and enforces expiry,
scope, rollback protection, and revocation. Private signing material is never
stored in this repository and runtime verification keys are not signing keys.

The design is TUF-inspired but makes no TUF conformance claim until an exact
implementation and interoperability profile is admitted.

## Consequences

- Offline-root ceremonies and delegated-key rotation need documented evidence.
- Development, beta, and stable channels cannot share ambient signing authority.

## Alternatives considered

- One repository/build key: rejected for excessive blast radius.
- Unsigned development artifacts accepted by production: rejected.

## Verification

- Threshold, expiry, scope, rotation, revocation, rollback, channel-isolation,
  and compromised-delegation tests.
