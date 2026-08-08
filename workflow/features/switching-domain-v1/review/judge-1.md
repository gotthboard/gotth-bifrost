# Cold review 1: authority and security boundaries

Decision: PASS

Scope: BFW-PRD-091 through BFW-PRD-099, `bfw-switching`, switching schema,
ADR-0008, transaction integration, and threat-model additions.

Findings:

- No direct domain-authority collapse found. Ports/interfaces, Layer-2
  forwarding, Layer-3 routing, and firewall/NAT remain separately owned.
- The core remains the sole admission and transaction authority; the switching
  plugin proposes typed plans and cannot call peer plugins as authority.
- Loop, VLAN leakage, FDB manipulation, uncertain STP, unsupported required
  semantics, partial apply, and offload drift fail closed or roll back.
- Hardware offload is optional and requires separate platform admission; the
  text makes no universal ASIC or vendor-SDK support claim.
- No runtime code, executable authority, secret, release admission, or product
  artifact was introduced.

Residual blockers are explicit: Phase 0, native adapter implementations,
pinned lab images, conformance evidence, artifacts, and independent runtime
admission.
