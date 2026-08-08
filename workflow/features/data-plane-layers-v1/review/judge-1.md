# Cold review 1: data-plane authority and layer semantics

Decision: PASS

Scope: revised BFW-PRD-102, BFW-PRD-106 through BFW-PRD-110, ADR-0010,
deployment profiles/schema, architecture, threat model, and validator.

Findings:

- Layer-2 switch effects remain owned by `bfw-switching`.
- Layer-3 effects, whether called switching or routing, remain owned by
  `bfw-routing`; no duplicate route authority was created.
- Layer-4-aware connection state, TCP/UDP policy, NAT, and port forwarding
  remain owned by `bfw-firewall`; "Layer 4 router" does not create a second
  firewall or routing authority.
- Switch mode requires routing for SVIs/routed ports/local fabric but explicitly
  denies WAN-edge routing, NAT, and implicit stateful transport policy.
- Router mode denies a user Layer-2 switching domain and declares Layer 3 plus
  Layer-4-aware effects.
- No Layer-7 proxy, TLS, payload inspection, or application-identity authority
  is implied.

No authority collapse, latent capability grant, runtime code, or admission
overclaim was found.
