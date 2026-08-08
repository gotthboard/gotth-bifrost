# Cold review 1: role authority and isolation

Decision: PASS

Scope: BFW-PRD-100 through BFW-PRD-105, deployment-profile policy/schema,
ADR-0009, architecture, threat model, and validator changes.

Findings:

- Router, switch, and converged are profiles of one core, configuration, API,
  CLI, web, audit, release, and recovery system; no edition fork was introduced.
- Router mode explicitly denies a user Layer-2 switching domain.
- Switch mode explicitly denies Layer-3 transit and NAT; management termination
  is shared by every profile and does not imply forwarding authority.
- Converged mode requires the exact union of switching, routing, and firewall
  domains and retains core-owned cross-domain transaction authority.
- Exact required-component closure and enabled/denied effect consistency are
  machine-validated against the v0.1 composition.

No authority escalation, latent forwarding grant, runtime code, release, or
admission claim was found. Native implementations and packet-oracle evidence
remain blocked behind Phase 0.
