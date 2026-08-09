# Distributed fabric v1 workflow

Canonical state, dependencies, blockers, review, and evidence are defined only in root `workflow.toml`.

This feature defines distributed Layer-2 switching, Layer-3 routing, and
firewall enforcement as an orthogonal Bifrost fabric scope.

Scope:

- add BFW-PRD-123 through BFW-PRD-135 and `bfw-fabric`
- define cryptographic membership, quorum/term/generation/fencing, and
  partition-safe reconciliation
- define EVPN/VXLAN-class overlays, VRFs, anycast gateways, routed VNIs, ECMP,
  mobility, BUM, and controlled route leaking
- define deterministic distributed firewall placement and flow-state
  symmetry/steering/ownership/replication/failover
- define MTU/offload semantics, staged rollout, convergence, node-local
  last-known-good enforcement, observability, rollback, scale, and admission

Fabric scope remains deferred outside v0.1. No runtime, cluster, peer,
repository, release, deployment, or admission is created.
