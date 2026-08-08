# ADR-0012: Distributed switching, routing, and firewall fabric

Status: Accepted

Requirements: BFW-PRD-123 through BFW-PRD-135

## Context

Bifrost must distribute switching, routing, and firewall behavior across
multiple systems while remaining one product with router, switch, and
converged roles. A monolithic fabric authority would duplicate domain logic and
turn cluster coordination into ambient network privilege. Distributed state
also introduces quorum, partition, ordering, convergence, mobility, flow-state,
and rolling-upgrade failure modes absent from a standalone appliance.

## Decision

Make `standalone` versus `fabric` an orthogonal deployment scope. Add
`bfw-fabric` to own membership topology, placement, convergence intent, and
multi-node transaction coordination. It delegates typed node-local effects to
`bfw-switching`, `bfw-routing`/`bfw-frr`, and `bfw-firewall`; it owns none of
their semantics.

Use cryptographic membership, quorum/term/generation/fencing, durable journals,
and deny-conflicting-writes partition behavior. Support admitted
VXLAN/GENEVE-class overlays and EVPN-class MAC/IP distribution, VRFs, anycast
gateways, routed VNIs, ECMP, controlled route leaking, and deterministic
distributed policy placement. Node-local last-known-good enforcement survives
control-plane loss under an explicit traffic-class safety policy.

## Consequences

- Router, switch, and converged roles can scale across multiple nodes without
  separate product editions.
- Fabric mode requires at least three nodes and multiple failure domains for
  quorum and admission evidence.
- Stateful firewall placement must solve path symmetry, steering, ownership,
  replication, mobility, and stale-state behavior explicitly.
- MTU/encapsulation/offload and BUM behavior become admission-critical.
- Fabric mode remains deferred outside v0.1 and depends on HA and dynamic
  routing foundations.

## Alternatives considered

- One fabric plugin owns all network policy: rejected due to authority collapse.
- Active/passive HA only: rejected because it does not provide a distributed
  switching/routing/firewall fabric.
- Two-node consensus: rejected because network partitions cannot provide safe
  majority decisions without an admitted external witness.
- Fail-open on control loss: rejected as a global default because it can widen
  connectivity silently.

## Verification

- authority and deterministic node-plan placement tests
- cryptographic membership, quorum, fencing, partition, and restart suites
- EVPN/VXLAN-class L2/L3, mobility, anycast, VRF/ECMP, route-leak tests
- distributed firewall placement/state symmetry/replication/failover tests
- MTU/offload/BUM, staged rollout, convergence, rollback, scale, and
  performance evidence with independent packet/state oracles
