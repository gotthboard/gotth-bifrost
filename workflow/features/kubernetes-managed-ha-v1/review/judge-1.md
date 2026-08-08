# Judge pass 1 — PASS

Scope: optional dedicated Kubernetes/K3s-managed HA controller architecture.

## Findings

- One controller is explicitly non-HA; the HA profile requires an odd quorum
  of at least three members across distinct failure domains.
- Managed routers and switches remain native Bifrost nodes and need not be
  Kubernetes workers or expose a container runtime.
- Kubernetes has no independent configuration, forwarding, switching, routing,
  firewall, fast-failover, or local-recovery authority.
- Controller/API/etcd/CNI/storage loss freezes new mutations while preserving
  last-known-good forwarding and native network HA.
- Controller plans remain mutually authenticated, signed, authorized,
  generation-bound, expiring, idempotent, verified, audited, and rollback-safe.
- The component is optional, deferred outside v0.1, and has no hard dependency
  on `bfw-ha` or `bfw-fabric`; those are node/fabric integrations.
- Requirements, ADR, threat entries, strict schema, positive/negative fixtures,
  lab scenarios, catalog/profile partition, and validators reconcile.

Decision: PASS. No Kubernetes cluster, runtime, release, or admission exists.
