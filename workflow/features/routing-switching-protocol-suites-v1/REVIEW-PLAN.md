# Routing and switching review plan

This is a gate plan, not a review verdict. Root `workflow.toml` owns state.

## Immutable target

Both reviewers must inspect the same committed revision. Each verdict must name
that revision, the relevant requirement range (`BFW-PRD-162` through
`BFW-PRD-208`), every file inspected, the reviewer identity, and the review
time. A later change invalidates both verdicts.

## Architecture review

An independent architecture reviewer must verify:

- every advertised protocol/profile has an exact provider, platform,
  maturity, limitation, evidence, and admission row;
- `bfw-routing` remains canonical L3 authority and `bfw-switching` remains
  canonical L2 authority;
- FRR, platform, and hardware adapters cannot bypass planning, authorization,
  transaction, reconciliation, rollback, or audit boundaries;
- protocol interaction, redistribution, convergence, restart, upgrade, and
  rollback semantics have bounded ownership and failure behavior;
- deferred, legacy, proprietary, experimental, and unsupported behavior is
  named instead of implied.

## Security review

A different independent reviewer must verify:

- fail-closed defaults, peer and endpoint identity, key custody, replay and
  stale-generation denial, route-leak controls, resource limits, and audit;
- sticky routed and switched bindings cannot silently relearn or cross VLAN,
  VRF, interface-generation, or port-generation boundaries;
- management, discovery, telemetry, packet capture, and export do not become
  hidden control planes;
- negative and adversarial admission-lab cases cover malformed input,
  conflicting authority, partition, restart, rollback, and provider drift.

## Completion record

Completion requires two passing verdicts over the same revision, governance
render and validation, all governance unit tests, whitespace checks, and a
`workflow/features/routing-switching-protocol-suites-v1/evidence/verification.toml`
record whose digest is entered in `workflow.toml` and the append-only event log.
Any real finding is repaired before both reviews are rerun from a fresh target.

No runtime protocol process, route, switch state, release, or support claim is
authorized by this review.
