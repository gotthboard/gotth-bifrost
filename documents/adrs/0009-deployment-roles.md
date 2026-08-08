# ADR-0009: Router, switch, and converged deployment roles

Status: Accepted

Requirements: BFW-PRD-100 through BFW-PRD-105

## Context

Bifrost is intended to be full-featured router and switch software, but a given
installation may need only routing, only switching, or both. Treating those as
separate products would duplicate configuration, authorization, management,
release, and recovery machinery. Treating every installation as converged
would unnecessarily expose forwarding domains and confuse a management address
with transit routing.

## Decision

Define `router`, `switch`, and `converged` as machine-readable deployment
profiles of one Bifrost product. They share the core, configuration, APIs, CLI,
web shell, audit, release, and recovery model. Each profile declares required
components plus enabled and denied forwarding effects. A switch management
address is non-transit; separately configured SVIs and routed switchports may
provide the switch role's bounded Layer-3 switching. Role changes use commit-confirmed transactions and
verified last-known-good rollback.

"Full-featured" describes the governed catalog and long-term product surface,
not universal availability. Runtime exposure is the admitted intersection of
the selected profile, release, platform, drivers, and hardware.

## Consequences

- Operators choose an appliance role without choosing a different edition.
- Disabled forwarding domains grant no latent authority or mutation surface.
- Role transition and recovery become explicit admission-test classes.
- v0.1 can test all three roles within its deliberately narrow feature set.
- Platform gaps remain visible and cannot be papered over by a profile name.

## Alternatives considered

- Separate router and switch editions: rejected due to governance and
  configuration drift.
- Always-converged runtime: rejected due to unnecessary authority and exposure.
- Infer role from configured interfaces: rejected because implicit role changes
  are difficult to authorize, audit, verify, and roll back safely.

## Verification

- exact machine-readable profile and component-closure validation
- denied-effect tests for router and switch profiles
- converged cross-domain transaction and packet-oracle tests
- role-transition, lost-management, restart, and rollback exercises
