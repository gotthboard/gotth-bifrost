# Judge pass 2 — PASS

Scope: fresh security, interoperability, failure, and evidence review of GoKA.

## Findings

- Spoofing, malformed VRRP, replay, timers, clock anomalies, partitions,
  duplicate ownership, restart, and partial transition have fail-closed tests.
- Clean-room provenance, license/dependency/source scans, packet corpora, fuzz,
  race, endurance, interoperable peers, platform parity, upgrade/rollback, and
  performance evidence are admission requirements rather than current claims.
- Linux native VRRP/netlink and FreeBSD CARP are separately admitted semantic
  mechanisms; unsupported platforms must report gaps rather than emulate
  ownership weakly.
- Observed state is bounded and authorization-filtered, with no credential,
  payload, or reusable-authority leakage.
- All 154 requirements, 41 components, 18 schemas, 14 ADRs, 20 tests,
  generated views, JSON/TOML, local links, Pyright, and diff hygiene pass.

Decision: PASS. GoKA and `bfw-ha` remain deferred outside v0.1; Phase 0 and
runtime admission remain blocked.
