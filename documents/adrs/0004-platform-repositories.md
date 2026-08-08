# ADR-0004: Platform backend repositories

Status: Accepted

Date: 2026-08-08

Requirements: BFW-PRD-001, BFW-PRD-005, BFW-PRD-036, BFW-PRD-065

Supersedes: none

## Context

Linux, FreeBSD, and Windows native networking APIs have different dependency,
release, privilege, and evidence lifecycles.

## Decision

Use one backend repository per operating-system family:
`bfw-platform-linux`, `bfw-platform-freebsd`, and `bfw-platform-windows`.
Portable domain policy remains in domain-component repositories. Backends
implement only versioned platform contracts and may not redefine policy,
authorization, configuration truth, or cross-component transaction rules.

## Consequences

- Platform releases and security responses can be versioned independently.
- Shared conformance suites become mandatory to prevent semantic drift.

## Alternatives considered

- One multi-platform backend repository: rejected because it couples unrelated
  native dependencies and admission evidence.
- Backend code in the core: rejected as portability and authority collapse.

## Verification

- Catalog ownership, repository-boundary, and cross-platform conformance tests.
