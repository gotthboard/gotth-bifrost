# Judge pass 1 — PASS

Scope: exactly two first-party out-of-the-box Bifrost HA profiles.

## Findings

- The authoritative profile set is exactly `goka-native` and
  `kubernetes-managed`; both are first-party and packaged out of the box once
  an HA-ready release is admitted.
- GoKA-native needs no external orchestrator. Kubernetes-managed ships Bifrost
  controller assets but honestly requires an admitted Kubernetes/K3s substrate.
- Both profiles share the canonical core configuration, authorization, CLI,
  web/API, audit, transaction, release, backup, and recovery contracts.
- Exactly one management coordinator may own an HA domain. Kubernetes may
  coordinate native mechanisms but cannot replace node-local fast failover or
  become a competing writer.
- Profile changes are commit-confirmed authority-handoff transactions with
  continuity or conservative isolation, independent verification, and rollback.
- Both components are planned first-party product features but remain deferred
  from v0.1 until Phase 0 and runtime admission evidence exist.

Decision: PASS. No runtime or release claim is created.
