# Judge pass 1 — PASS

Scope: GoKA clean-room native Go HA architecture and governance.

## Findings

- GoKA is the formal product name of `bfw-ha`; it remains one existing
  component rather than creating overlapping HA authorities.
- Public VRRP specifications and independently authored fixtures are the
  implementation authority. Keepalived source, libraries, binaries, runtime,
  configuration authority, copying, linking, wrapping, and supervision are
  all denied.
- VRRPv2/v3 IPv4/IPv6, priority 255 owner behavior, timers, preemption,
  multicast/unicast peers, protocol validation, and platform mappings are
  explicit and bounded.
- GoKA emits typed plans but cannot directly mutate addresses, routes, firewall
  roles, services, credentials, or platform state.
- Typed health checks are bounded; arbitrary shell, inherited environment, and
  ambient process access are denied.
- Keepalived import is an exact versioned subset with hard rejection of scripts,
  hooks, IPVS, unsupported directives, and ambiguity.
- Retaining last-known-good ownership requires an explicit nonempty fencing
  proof; unicast-without-peers and VRRPv2/IPv6 fixtures fail closed.

Decision: PASS. No runtime, repository, protocol claim, or release is admitted.
