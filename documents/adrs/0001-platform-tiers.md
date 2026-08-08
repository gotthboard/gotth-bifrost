# ADR-0001: Platform tiers

Status: Accepted

Date: 2026-08-08

Requirements: BFW-PRD-008, BFW-PRD-065, BFW-PRD-087, BFW-PRD-090

Supersedes: none

## Context

Bifrost is cross-platform, but claiming equal first-release maturity would hide
different kernel semantics and multiply the initial admission surface.

## Decision

The v0.1 implementation profile is Linux-first. FreeBSD and Windows are
compatibility targets for the shared schemas, SDK, lifecycle substrate, and
native platform contracts; their product images are admitted in later release
profiles. Darwin is a shared-SDK build/test target until a product profile says
otherwise. Unsupported or weaker semantics fail closed.

Exact OS releases, kernels, architectures, images, and digests are release
inputs, not permanent ADR text. `governance/test-lab.toml` leaves them empty and
blocks system admission until measured images are selected.

## Consequences

- v0.1 has one product data-plane target and a smaller test matrix.
- Cross-platform contracts still cannot be Linux-specific shortcuts.
- No FreeBSD, Windows, or Darwin product-support claim exists yet.

## Alternatives considered

- Admit three product platforms in v0.1: rejected as too broad for trustworthy
  first-release evidence.
- Linux-only architecture: rejected because it would corrupt shared contracts.

## Verification

- v0.1 profile partition and platform-policy validation.
- Phase 0 cross-platform substrate gates remain mandatory.
