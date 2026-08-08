# Cold review 1: distributed authority, consensus, and partitions

Decision: PASS

Scope: BFW-PRD-123 through BFW-PRD-135, `bfw-fabric`, fabric-plan schema,
ADR-0012, architecture, requirements, threats, and validators.

Findings:

- Fabric is orthogonal to router/switch/converged role and does not create a
  separate product, configuration authority, or management plane.
- `bfw-fabric` owns membership topology, placement, convergence intent, and
  multi-node transactions but cannot create switching, routing, or firewall
  semantics; node-local plans come from their owning domains.
- Membership requires cryptographic identity, explicit enrollment/revocation,
  compatible release/capabilities, liveness/generation, and authenticated
  encrypted channels.
- Quorum, leader term, monotonic generation, fencing, journals, idempotency,
  and minority mutation denial cover stale-leader and split-brain paths.
- Control loss retains last-known-good node-local enforcement; unknown policy
  placement denies rather than widens connectivity.
- Per-traffic-class exceptions cannot override a stricter local safety floor.

No ambient cluster authority, two-node-consensus claim, silent fail-open,
runtime cluster, or admission overclaim was found.
