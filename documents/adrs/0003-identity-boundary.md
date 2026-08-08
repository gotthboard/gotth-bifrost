# ADR-0003: Identity component boundary

Status: Accepted

Date: 2026-08-08

Requirements: BFW-PRD-040 through BFW-PRD-050

Supersedes: none

## Context

OIDC validation is specialized and externally facing, while Bifrost
authorization must remain core-owned.

## Decision

`bfw-identity` is a separate, unprivileged component. It performs OIDC relying-
party protocol work and returns bounded validated identity facts to the core.
It does not map roles, grant permissions, issue plugin authority, store reusable
secrets, or become a general identity provider. The core owns authorization and
opaque Bifrost sessions; `agent-keyring` owns confidential credentials.

## Consequences

- OIDC parser/network compromise is separated from authorization authority.
- Identity/core APIs require explicit versioning and hostile-input tests.

## Alternatives considered

- Put OIDC in `bfw-web`: rejected because presentation and identity validation
  should not become one trust boundary.
- Put authorization in the identity component: rejected as authority collapse.

## Verification

- Token non-propagation, deny-default role mapping, and boundary tests.
