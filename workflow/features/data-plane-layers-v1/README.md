# Data-plane layers v1 workflow

Status: completed

This feature defines Layer-2 and Layer-3 switch behavior plus Layer-3 routing
and Layer-4-aware router policy without collapsing component authority or
implying Layer-7 functions.

Scope:

- revise BFW-PRD-102 and add BFW-PRD-106 through BFW-PRD-110
- add exact data-plane layer and effect declarations to deployment profiles
- define SVI, routed-switchport, inter-VLAN, local-fabric, edge-route,
  stateful transport policy, NAT, and port-forward boundaries
- deny implicit WAN/NAT/Layer-4 effects in switch mode and implicit Layer-7
  behavior in every mode

No runtime code, repository, release, deployment, or admission is authorized.
