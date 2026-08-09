# Bifrost system admission lab

Status: specified but unprovisioned

Authority: `governance/test-lab.toml`

The lab is isolated from production and has separate management, inside,
outside, HA-sync, and hostile-client networks. It contains an unprivileged
operator host, two HA-capable appliance nodes, two independent traffic
generator/observer endpoints, four independent switch-port fixtures, service
fixtures, and an independent witness.

Linux is the v0.1 product target. FreeBSD and Windows nodes exist to test shared
substrates, platform contracts, and later profiles. Exact OS releases, kernels,
architectures, and image digests are intentionally empty today; evidence is
blocked until they are pinned.

The switch-port fixtures provide access endpoints and redundant trunk/LACP
paths. They exercise VLAN isolation and tagging, native/PVID behavior,
learned/aged/static FDB entries, STP-family convergence under physical and
logical loops, LACP member loss, storm control, IGMP/MLD snooping,
management-VLAN rollback, and software/offload parity where an offload adapter
is admitted. Packet capture and native state inspection remain independent of
`bfw-switching` success reports.

The same admitted image is exercised as router, switch, and converged.
Independent packet oracles prove that router mode exposes no user-traffic
switching domain; switch mode performs admitted SVI, routed-switchport,
inter-VLAN, and local-fabric Layer-3 switching but denies WAN-edge routing, NAT,
and Layer-4 state policy; its management address remains non-transit. Router
mode separately proves Layer-3 edge forwarding, TCP/UDP state policy, NAT, and
port forwarding without implying Layer-7 proxy or payload authority. Converged
mode performs only the configured union. Every pairwise role transition is
tested for partial apply, lost management, lost confirmation, process restart,
and last-known-good rollback.

IDS/IPS admission uses immutable packet/flow corpora and independent alert
oracles across passive observation and separately admitted inline fail-open and
fail-closed modes. Fixtures cover IP fragments, TCP retransmission/overlap,
segmentation, VLAN/offload/checksum normalization, malformed protocols,
evasion, unsupported Snort-rule constructs, hostile rules, overload, capture
loss, queue saturation, crash/restart, ruleset interruption/rollback, and
payload/PCAP redaction. Traffic generation and packet capture are independent
of `bfw-ids`; known injected cardinality and sequence markers prove loss and
completeness. Performance evidence records p50/p95/p99 latency, throughput,
packet loss, CPU, memory, allocations, flow/stream occupancy, queue depth, and
alert/evidence volume for every admitted platform and mode.

Fabric admission uses at least three independently identified nodes across
multiple logical failure domains plus independent underlay/overlay traffic
generators and observers. It covers enrollment/revocation, quorum/term/fencing,
asymmetric partitions, delayed/reordered control messages, leader/node restart,
EVPN/VXLAN-class MAC/IP distribution and mobility, duplicate endpoints,
VRF/route-target isolation, anycast gateways, ECMP member loss, distributed
firewall placement and state-owner failover, MTU/PMTU/encapsulation boundaries,
BUM/loop/offload behavior, staged rolling upgrade, island/rollback, churn, and
scale convergence. Oracles compare the canonical generation, every node's
native switching/routing/firewall state, and end-to-end allowed/denied packet
matrices; fabric self-reporting alone cannot prove completeness.

Kubernetes-managed HA admission adds three controller members in
separate declared failure domains and at least one native managed router or
switch. Managed nodes are not required to be Kubernetes workers. Continuous
packet/state oracles cover controller quorum and total loss, API server, etcd,
CNI, storage, asymmetric management partitions, stale-plan replay, controller
rebuild, rolling upgrade/rollback, RBAC and secret isolation, and autonomous
node forwarding throughout controller failure.

GoKA admission adds independent VRRPv2/v3 peers and packet capture/injection
oracles. It covers clean-room provenance, IPv4/IPv6 multicast and unicast
election, owner/priority/preemption/timer boundaries, malformed/spoofed/replayed
packets, partitions and duplicate ownership, typed health and shell denial,
Keepalived-subset rejection, Linux/CARP semantic parity, restart, upgrade,
rollback, fuzz/race/endurance, and latency/CPU/memory/allocation boundaries.

Out-of-the-box HA profile admission proves exactly `goka-native` and
`kubernetes-managed` are packaged first-party choices with identical canonical
policy semantics. It covers competing-coordinator denial, profile selection,
interrupted cross-profile authority handoff, continuous forwarding or
conservative isolation, commit-confirmed rollback, recovery assets, and release
composition without treating an unadmitted v0.1 profile as HA-ready.

BGP admission adds at least six independent peers capable of FRR, BIRD,
GoBGP, and available vendor implementations. The lab crosses eBGP/iBGP,
reflector, confederation, route-server, multihop, numbered/unnumbered, dynamic,
peer-group, and VRF topologies with every declared AFI/SAFI and negotiated
capability. Independent route and packet oracles cover policy order,
route-target/VRF isolation, leak/hijack prevention, RPKI/ASPA/BGPsec capability
state, FlowSpec/EVPN/VPN behavior, Add-Path, BFD, GR/LLGR, restart, upgrade,
RIB/FIB disagreement, malformed-message fuzzing, churn, scale, BMP/MRT bounds,
redaction, convergence, and rollback. Provider self-reporting and one
established session are not completeness evidence.

The routing-peer pool additionally covers OSPFv2/v3, IS-IS, RIP/RIPng, Babel,
EIGRP/NHRP status, IGMP/MLD/PIM/MSDP, LDP/MPLS/SR/TE, and shared BFD. Tests
cross adjacency/election/database/flooding, authentication, malformed control
traffic, partitions, recursive next hops, every enabled redistribution edge,
withdrawal, restart/upgrade, convergence, resource bounds, canonical RIB/native
FIB agreement, and packet reachability. Legacy, alpha, and unavailable provider
rows must demonstrate denial rather than fake compatibility.

Switching-protocol peers cover VLAN/Q-in-Q/registration, STP/RSTP/MSTP and
vendor dialects, LACP and multi-chassis failure, LLDP/vendor discovery,
IGMP/MLD snooping/MVR, 802.1X/MACsec and port protections, overlays, ring/fabric
profiles, DCB/TSN, and Ethernet OAM. Hostile control-frame injection, loops,
storms, partitions, duplicate ownership, cross-VLAN/tenant leakage, hardware
offload drift, management lockout, upgrade, convergence, and rollback are
observed independently from the device/provider under test.

Sticky-binding admission uses independent endpoint generators on switched and
routed ports. It covers bounded observation and explicit enrollment, persisted
MAC/port/VLAN binding, routed interface/VRF/MAC/IP neighbor binding, duplicate
and moved endpoints, limit overflow, spoofed ARP/NDP/DHCP evidence, LAG/VLAN
and interface-generation changes, hardware/provider disagreement, reboot,
failover, upgrade, clear/replace, quarantine, last-known-good rollback, and
packet-oracle proof that a violation never widens access or silently relearns.

The primary Linux image target is Alpine Linux 3.24.1 on x86-64, but remains
unpinned and unadmitted until an exact repository snapshot, kernel, package,
firmware, installer, ISO, and installed-image digest exist. Installer admission
performs independent reproducible rebuilds and covers UEFI and legacy BIOS,
offline install, stable target-disk identity and destructive confirmation,
wrong/removed/renumbered disk, interruption and power loss at every write
stage, corrupt media and APK database, unsupported hardware, first-boot
fail-closed state, package drift, upgrade, boot confirmation, rollback, and
local-console recovery. A booted live ISO or successful installer exit is not
installed-appliance evidence.

The learning-alpha lane is a smaller matrix, not a weaker safety oracle. It
uses one pinned disposable VM/hardware profile and proves install/boot/reset,
the basic router path, the basic switch path, configuration persistence,
authority-loss/unknown-state recovery, and explicit unsupported-capability
denial. Before `BFW-ALPHA-0`, tests remain offline, namespace-contained, or in
disposable VMs; attempts to mutate a designated host network, write an
installer target, or distribute media must be denied. Alpha signing and trust
fixtures also prove that alpha metadata and evidence cannot be replayed,
relabelled, or promoted into beta or stable.

Every run records immutable image/artifact/release digests, host and topology
facts, commands, time bounds, configuration and participant generations,
packet/state completeness oracles, redacted logs, rollback result, and review.
Required scenarios cover clean install, upgrade interruption, migration,
last-known-good rollback, management lockout, local-console recovery, plugin
crash/restart, stale generation, malicious plugins, warnings/partial results,
HA failover/split brain/duplicate ownership, identity-provider outage, and
secret-seeded redaction scans, plus the complete switching scenario set above.

Passing metadata validation proves only that the lab specification is complete.
It does not prove that the lab exists or that any runtime behavior passed.
