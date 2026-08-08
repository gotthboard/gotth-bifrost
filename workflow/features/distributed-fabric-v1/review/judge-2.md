# Cold review 2: data plane, convergence, and recovery completeness

Decision: PASS

Scope: EVPN/VXLAN-class L2/L3, VRF/anycast/ECMP, distributed firewall state,
MTU/offload/BUM, staged rollout, observations, lab topology, and v0.1 boundary.

Findings:

- L2 contracts cover VNI/bridge identity, split horizon, designated forwarding,
  bounded BUM, ARP/ND suppression, mobility sequence, duplicates, and aging.
- L3 contracts cover VRF, routed VNI, anycast gateway, ECMP, route targets,
  controlled leaking, next-hop reachability, and typed dynamic routing.
- Distributed firewall policy uses one canonical generation and deterministic
  node placement with explicit symmetry, steering, state owner, replication,
  failover, mobility, and stale-state behavior.
- Underlay/overlay tests include MTU/PMTU, encapsulation, fragmentation,
  QoS/ECN, entropy, loops/BUM, offload parity, loss, and ordering.
- Multi-node transactions use readiness barriers, failure-domain staging,
  canaries, independent node/end-to-end oracles, convergence deadlines, and
  coordinated rollback or explicit isolation.
- The lab requires three nodes, failure domains, asymmetric partitions,
  mobility/churn, rolling upgrade/rollback, scale, and resource/performance
  evidence. Fabric remains deferred outside v0.1.

No blocking design defect was found. Protocol, packet-path, and performance
behavior remains unimplemented and unclaimed.
