# ADR-0002: Public executable role names

Status: Accepted

Date: 2026-08-08

Requirements: BFW-PRD-000, BFW-PRD-025, BFW-PRD-033, BFW-PRD-069

Supersedes: none

## Context

Provisional daemon and web names would otherwise leak into packages and service
units inconsistently.

## Decision

The public command is `bfw`, the privileged core-daemon role is `bfwd`, and the
independent web-service role is `bfw-web`. Platform packaging may add native
service-unit labels, but it must preserve these public role names and the
lowercase `bfw` namespace.

## Consequences

- Documentation, packages, service definitions, diagnostics, and upgrades have
  one naming contract.
- Renaming after a public release requires a compatibility and migration ADR.

## Alternatives considered

- `bifrostd` and `bifrost-web`: rejected because `bfw` is the settled namespace.

## Verification

- Naming validator and package/service compatibility tests.
