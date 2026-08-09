# ADR-0016: Linux learning-alpha admission path

Status: Accepted

Date: 2026-08-09

Requirements: BFW-PRD-013, BFW-PRD-066, BFW-PRD-215, BFW-PRD-216, BFW-PRD-217, BFW-PRD-218, BFW-PRD-219, BFW-PRD-220, BFW-PRD-221, BFW-PRD-222

Supersedes: none

## Context

Requiring the complete cross-platform substrate before any implementation
prevents a usable appliance from producing the evidence needed to settle
product and interface decisions. Dropping safety gates to get a demo would be
worse: network and installer effects can damage systems even in an alpha.

## Decision

Bifrost adds a Linux-only, non-production learning-alpha path. Source work,
unit tests, offline simulation, network namespaces, and disposable VMs may
start after normal workflow activation and before full Phase 0 admission.
Phase 0 exemption does not itself activate work. Designated host-network mutation,
installer-disk mutation, and alpha distribution require the independent
`BFW-ALPHA-0` minimum safety and dependency gate.

The first alpha is single-node Alpine Linux x86-64, software-data-plane only,
and uses `rpc-plugin-system` v2 plus selected Linux-compatible authority
providers. It implements only the explicit alpha scope. It may be incomplete,
rough, slow, reset-oriented, and incompatible between builds. Destructive
selection, packet-policy defaults, secret custody, configuration integrity,
generation/liveness authority, recovery, truthful state, and channel isolation
are not relaxed.

Full `BFW-PHASE-0` admission remains mandatory for beta and stable. Alpha
artifacts, evidence, and successful demos cannot be promoted or laundered into
that decision. It is also mandatory before implementation expands beyond the
exact learning-alpha scope: every Phase 0 dependency must independently earn
an A or A+ grade with fresh evidence and review. Grades cannot be averaged or
inherited from end-to-end behavior.

## Consequences

- Product decisions can be tested against a usable appliance before broad
  compatibility, polishing, optimization, and hardening are frozen.
- Alpha installations require explicit limitation labels and disposable or
  designated non-production targets.
- Alpha compatibility is provisional; reset/reinstall is an acceptable
  migration policy when documented.
- Two gates must stay mechanically distinct; a single ambiguous runtime flag
  is forbidden.
- Requirements and design may continue while Phase 0 is blocked, but all
  out-of-alpha runtime implementation waits for four independent A-grade
  dependency admissions.

## Alternatives considered

- Wait for full Phase 0 before any implementation: rejected because it delays
  the evidence needed to make sound product decisions.
- Permit an unrestricted prototype: rejected because installer and packet
  effects can cause real damage regardless of release label.
- Treat alpha as a weak beta: rejected because it invites accidental promotion
  and dishonest support claims.

## Verification

- Governance tests prove source/offline permission cannot authorize host,
  disk, distribution, beta, stable, or production effects.
- Alpha lab tests cover installation, packet policy, authority loss,
  configuration recovery, reset, channel isolation, and published limits.
