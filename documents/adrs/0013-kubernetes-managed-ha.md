# ADR-0013: First-party Kubernetes-managed high availability

Status: Accepted

Requirements: BFW-PRD-136 through BFW-PRD-144

## Context

A dedicated local controller can centralize management for many Bifrost routers
and switches. Kubernetes provides mature scheduling, API reconciliation,
rollout, and observability, but it depends on networking and therefore cannot
safely become the forwarding or fast-failover substrate it is managing.

## Decision

Support Kubernetes or K3s as a first-party controller deployment for management,
inventory, signed plan distribution, rollout, observation, and recovery. Keep
router and switch services native and autonomous. One controller is an explicit
non-HA profile; controller HA requires an odd quorum of at least three members
across declared failure domains. Loss of the controller freezes new mutations
but preserves last-known-good forwarding and native network HA.

## Consequences

- Small sites may use one dedicated controller with honest availability limits.
- Production controller HA consumes at least three failure-separated members.
- Kubernetes components, versions, images, CNI, storage, RBAC, and recovery
  become separately pinned admission inputs.
- Routers are managed nodes, not required Kubernetes workers.
- Native Bifrost HA and local recovery remain mandatory.

## Alternatives considered

- Run every router as a Kubernetes worker: rejected because CNI, scheduler, and
  container-runtime failure would become forwarding dependencies.
- One controller marketed as HA: rejected because it is a single failure domain.
- Kubernetes owns packet failover: rejected because network recovery would
  depend on the failed network and reconciliation latency is not a fast path.
- No centralized controller option: rejected because it discards useful fleet
  management, rollout, inventory, and observability capabilities.

## Verification

- single-controller labeling and three-controller quorum tests
- controller/API/etcd/CNI/storage loss with continuous packet/state oracles
- signed typed plan, stale/replay, node-local authorization, and rollback tests
- RBAC, NetworkPolicy, Pod Security, image/provenance, secret, and recovery audits
- management partition, controller rebuild, rolling upgrade, and rollback tests
