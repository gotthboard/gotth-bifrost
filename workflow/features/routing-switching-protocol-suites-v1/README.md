# Comprehensive routing and switching protocol suites workflow

Canonical state, dependencies, blockers, review, and evidence are defined only in root `workflow.toml`.

This feature replaces vague broad-protocol claims with exact, machine-readable
capability matrices. BGP is one routing family within the larger contract.
`bfw-routing` remains canonical L3 route authority, and `bfw-switching` remains
canonical L2 switching authority.

Scope:

- add BFW-PRD-162 through BFW-PRD-208
- define BGP peer topology, AFI/SAFI, capability, policy, security,
  convergence, transaction, observation, scale, fuzz, and interoperability
- define provider-neutral routing contracts for OSPF, IS-IS, RIP, RIPng,
  Babel, EIGRP, NHRP, multicast routing, MPLS, segment routing, traffic
  engineering, BFD, and redistribution
- define switching contracts for VLAN registration, spanning tree, link
  aggregation, discovery, multicast snooping, access protection, overlays,
  fabric and ring protocols, DCB/TSN, and Ethernet OAM
- define distinct switched MAC/port/VLAN and routed
  interface/VRF/MAC/IP sticky endpoint bindings with fail-closed violations
- require each protocol/profile row to state provider, platform, maturity,
  limitations, evidence, and admission state
- add routing and switching threats and isolated admission-lab scenarios
- preserve v0.1's explicit dynamic-routing and advanced-switching exclusions
- run governance validation and independent cold architecture/security review
  before completing the workflow

No runtime code, component repository, routing daemon, switch process, peer
session, route or forwarding-state mutation, release, deployment, or support
claim is authorized by this feature.
