# ADR-0010: Layer-2/3 switching and Layer-3/4-aware routing semantics

Status: Accepted

Requirements: BFW-PRD-102, BFW-PRD-106 through BFW-PRD-110

## Context

The switch role must support both Layer 2 and Layer 3, while the router role
must support Layer 3 forwarding and Layer 4-aware edge behavior. OSI layer
labels alone do not define authority: Layer 3 switching and routing share route
mechanisms, and Layer 4-aware router behavior depends on stateful firewall/NAT
policy. Without explicit ownership, the labels could create an oversized
"network" authority or imply Layer-7 functions that were never requested.

## Decision

`bfw-switching` owns Layer-2 forwarding/control. `bfw-routing` owns all Layer-3
forwarding, including switch SVIs, routed switchports, inter-VLAN/local-fabric
routing, and router edge routes. `bfw-firewall` owns Layer-4-aware connection
state, TCP/UDP policy, NAT, port forwarding, and transport-aware steering.

Switch mode admits Layer 2 and a bounded Layer-3 switching subset while denying
WAN-edge routing, NAT, and implicit Layer-4 policy. Router mode admits Layer 3
and Layer-4-aware effects while denying a user Layer-2 switching domain.
Converged mode admits the explicit union. Management-only interfaces never
become transit paths.

Layer-4 awareness does not imply reverse proxying, TLS termination, payload
inspection, application protocols, or Layer-7 identity policy.

## Consequences

- Layer-3 switching reuses routing contracts without collapsing ownership.
- Role profiles declare data-plane layers and exact effects.
- Tests distinguish local-fabric routing from WAN-edge routing.
- Layer-4 policy remains stateful packet policy, not an application proxy.
- Unsupported or partially observed layer behavior fails closed.

## Alternatives considered

- Give Layer-3 switching to `bfw-switching`: rejected because it would duplicate
  route validation, tables, health, application, and rollback semantics.
- Call all firewall behavior "Layer-4 routing": rejected as imprecise; routing
  remains Layer 3 while the router product composes Layer-4-aware policy.
- Treat Layer-4 as Layer-7 proxying: rejected because it silently expands scope
  and authority.

## Verification

- exact profile layer/effect and component-closure validation
- SVI, routed-port, inter-VLAN, local-fabric, edge-route, TCP/UDP state, NAT,
  port-forward, management non-transit, and denied Layer-7 implication tests
