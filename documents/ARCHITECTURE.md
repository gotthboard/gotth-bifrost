# Bifrost (BFW) Architecture

Status: active boundary and governance architecture; runtime not admitted

## Naming boundary

**Bifrost** is the full product name; **BFW** is its canonical firewall
shorthand (Bifrost Firewall), and `bfw` is the lowercase public namespace.
Component names must compose beneath that namespace rather than inventing
another product acronym. ADR-0002 settles `bfw`, `bfwd`, and `bfw-web` as the
public executable role names; platform packages and service units preserve
those names as one compatibility contract.

## Meta-repository boundary

`danny/Bifrost` is the product meta repository. It owns:

- the canonical PRD, architecture, and implementation/release plan
- the component and external-dependency map
- cross-component API, schema, authority, lifecycle, and compatibility rules
- exact release composition and migration/rollback ordering
- system-level integration, security, recovery, and platform evidence

It does not own executable product code. The core daemon, `bfw` CLI, web
service, routing plugin, platform backends, optional service plugins, SDKs, and
installers live in separately versioned repositories. Once admitted, their
exact revisions are pinned here by release metadata or Git submodules; source
is not copied into the meta repository.

Machine-readable governance under `governance/` is authoritative for component
identity and pins, alpha and Phase 0 status, release profiles, and lab
state. Versioned shared envelope schemas live under `schemas/v1/`. Prose
remains authoritative for normative product intent, but the validator requires
matching IDs and rejects contradictory governance state.

## Control and data planes

The native operating-system networking stack is the data plane. Bifrost's
portable Go services form the control and management planes: they validate
desired configuration, compile a platform-neutral policy IR, admit plugin use,
apply deterministic runtime transactions through narrow platform adapters,
verify observed state, and preserve audit and rollback evidence.

```text
operator / API
  -> authenticated management plane
  -> versioned desired configuration
  -> validation and platform-neutral policy IR
  -> admitted platform/service plugin
  -> native transactional runtime adapter
  -> nftables/netlink, pf, WFP, or supervised network service
  -> observed-state verification and audit
```

## Proposed boundaries

- **configuration core:** canonical schemas, revisions, migrations, validation,
  and rollback
- **policy compiler:** pure desired-state conversion into reviewable,
  platform-neutral firewall and NAT plans; routing-domain compilation belongs
  to `bfw-routing`
- **platform adapters:** narrow Linux, FreeBSD, Windows, and later platform
  translation and apply/verify surfaces
- **plugin catalog:** signed manifests, package provenance, compatibility,
  declared permissions, migrations, enable/disable state, and rollback
- **plugin supervisor:** separate-process lifecycle, generation identity,
  authentication, health, failure isolation, routing, and append-only logs
- **credential authority:** `agent-keyring` stores and governs secret payloads;
  Bifrost stores only selectors, redacted metadata, opaque-reference
  fingerprints, and audit correlation
- **filesystem provider:** `agent-filesystem` performs scoped, race-safe host
  file operations after core admission; it is not canonical-state authority
- **execution provider:** `agent-exec` performs bounded local process mechanics
  after core admission; it is not shell, privilege, or policy authority
- **reconciler:** idempotent apply/verify loop with explicit drift handling
- **management API:** authenticated authorization boundary; no direct shell
  execution
- **web UI service:** independent unprivileged API client and plugin UI renderer;
  it never becomes configuration authority
- **CLI:** `bfw` uses the same API contracts and provides local recovery without
  directly mutating firewall state
- **distribution builder:** separately versioned `bfw-installer` produces the
  signed reproducible Alpine Linux and FreeBSD live installation media and
  deterministic machine-tailored installed compositions from immutable release
  inputs; it has no runtime packet-policy authority
- **evidence plane:** audit events, metrics, logs, diagnostics, and support
  bundles with secret redaction

## Safety invariants

- Configuration is not committed as current until validation and required
  runtime verification succeed.
- Runtime changes use atomic transactions where the subsystem supports them.
- A failed candidate leaves or restores the last known-good state.
- Management-access changes require a confirmation timer or local recovery
  mechanism before becoming permanent.
- Service and kernel warnings are failures when they imply incomplete policy.
- Plugin presence or capability advertisement is not permission; core admits
  each privileged operation against the declared contract.
- Plugin or supervisor failure leaves native last-known-good policy active.

## Cross-component transaction architecture

`contracts/TRANSACTION-V1.md` and
`schemas/v1/transaction.schema.json` define the shared transaction boundary.
The core alone coordinates and commits; domain, platform, and provider
participants retain their own typed authority:

```text
candidate at base generation
  -> validate without native mutation
  -> prepare immutable plan, preconditions, oracles, and rollback
  -> apply generation-bound idempotent steps
  -> verify complete observed state and packet/service oracles
  -> commit the new canonical generation
  -> or roll back and verify the recorded last-known-good pair
```

A lost reply, warning, partial result, stale generation, changed operand under
an idempotency key, or unknown participant state cannot be interpreted as
success. Coordinator restart resumes verification or rollback from its journal;
it does not issue fresh authority for an ambiguous old transaction.

## Plugin architecture

```text
Bifrost portable core
  -> admitted plugin contract
  -> cross-platform rpc-plugin-system substrate
  -> platform backend or optional service executable
  -> native OS/service API
```

The Bifrost core contract owns shared configuration and transaction envelopes,
permissions, idempotency, result framing, and rollback coordination. Each
domain contract owns its schemas, desired state, typed plan semantics, and
domain-specific rollback consequences; `bfw-switching` owns the Layer-2
switching domain and `bfw-routing` owns the Layer-3 routing domain.
The `rpc-plugin-system` substrate owns executable lifecycle and trust facts. It
must not become firewall-policy or routing authority.

Candidate plugin classes:

- platform firewall and interface backends
- `bfw-switching` Layer-2 domain plugin and its platform apply/verify adapters
- `bfw-routing` routing-domain plugin and its platform apply/verify adapters
- DHCP and DNS services
- VPN providers
- IDS/IPS and traffic-analysis services
- high-availability and configuration synchronization
- dynamic DNS, ACME, monitoring, backup, and support tooling

Core configuration, admission, audit, package verification, and recovery remain
non-optional. Plugins cannot replace or weaken them.

## Switching plugin boundary

`bfw-switching` is the Layer-2 domain plugin. It owns:

- bridge domains and VLAN membership, including access, trunk, native/PVID,
  tagged/untagged egress, and allowed VLAN sets
- learned and static forwarding-database intent, aging policy, and observations
- STP, RSTP, and MSTP policy, port roles/states, guards, and loop prevention
- LACP port-channel semantics and member eligibility/state
- port isolation, storm control, IGMP/MLD snooping, and LLDP observations
- deterministic switching-plan generation, applied-state verification,
  switching UI schemas, audit facts, health, drift, and rollback effects

It does not own physical port discovery or construction, IP addressing and
routes, packet filtering/NAT, DHCP service state, credentials, authorization,
or platform admission. Those remain `bfw-network`, `bfw-routing`,
`bfw-firewall`, service, core, and platform responsibilities.

```text
operator / bfw / web
  -> core validates and admits desired Layer-2 change
  -> bfw-switching compiles a typed deterministic switching plan
  -> admitted platform adapter applies software or admitted offloaded switching
  -> bfw-switching and core compare bounded observed state with desired state
  -> core commits, confirms, or rolls back the configuration revision
```

Linux software bridge/VLAN is the v0.1 baseline. Linux switchdev/DSA/devlink,
FreeBSD bridge/VLAN, Windows Hyper-V vSwitch or another native equivalent, and
vendor ASIC SDKs are distinct adapter profiles with declared semantic gaps.
Hardware offload is never inferred from a device name and never bypasses the
typed plan, observation, verification, audit, failure, or rollback contract.

Potential loops, conflicting VLAN ownership, tag leakage, duplicate bridge
membership, uncertain STP convergence, or unsupported required behavior fail
closed. A management VLAN, bridge, uplink, native-VLAN, or port-channel change
uses commit-confirmed unless an admitted local or out-of-band recovery path can
prove continued access.

## Routing plugin boundary

`bfw-routing` is the routing-domain plugin. It owns:

- static route and gateway desired state
- route selection, metrics, tables/VRFs, and policy-routing domain validation
- gateway and route-health observations
- ECMP modeling where the admitted platform supports it
- integration contracts for separately supervised dynamic-routing services
- deterministic route-plan generation and applied-state verification
- routing-specific UI schemas, typed actions, audit facts, and rollback effects

It does not own interface or VLAN/bridge creation, DNS or DHCP,
packet-filter/NAT policy,
credentials, process execution, global authorization, plugin lifecycle, or
release admission. Those remain separate Bifrost or provider boundaries.

```text
operator / bfw / web
  -> core validates and admits desired routing change
  -> bfw-routing compiles a typed deterministic routing plan
  -> admitted platform adapter applies native route operations
  -> bfw-routing and core verify observed state
  -> core commits or rolls back the configuration revision
```

The core may coordinate a transaction containing firewall, port, switching,
routing, and DHCP steps, but it does not reimplement those domains. Each owner
must declare ordering, preconditions, reversibility, partial-failure semantics,
and last-known-good consequences so the core can admit the whole transaction.

### Comprehensive BGP suite boundary

`bfw-frr` is the separately supervised BGP protocol adapter. The admitted FRR
build owns wire-protocol parsing, capability negotiation, BGP session state,
Adj-RIB-In/Out, BGP policy evaluation, and its protocol-local Loc-RIB. It runs
with ambient forwarding mutation disabled or contained: selected BGP routes
cross a typed, generation-bound boundary into `bfw-routing`, which validates
route ownership, next-hop reachability, VRF/table scope, loops, policy, and
platform support before compiling the canonical route plan. FRR, its CLI, and
its configuration files never become an alternate route authority.

```text
operator / bfw / web
  -> core admits typed BGP intent
  -> bfw-routing validates route-domain ownership and dependencies
  -> bfw-frr compiles provider configuration for one pinned FRR capability set
  -> admitted FRR instance negotiates peers and computes protocol-local state
  -> bfw-frr emits typed candidate routes and complete protocol observations
  -> bfw-routing compiles/admits the canonical platform route plan
  -> independent protocol, native-route, and packet oracles verify convergence
  -> core commits or rolls back the configuration generation
```

The BGP contract is a matrix, not a boolean. It records peer topology modes;
IPv4/IPv6 transport; every enabled AFI/SAFI; negotiated capabilities; import,
export, and leak-prevention policy; authentication and routing-security
mechanisms; platform/provider support; limits; and interoperability evidence.
The required family surface includes unicast, multicast, labeled-unicast,
VPNv4/VPNv6, EVPN, FlowSpec, route-target constraints, MVPN, BGP-LS, and SR
Policy. A release may admit these independently, but it must publish every gap
and cannot use one family's success as evidence for another.

Peer modes include eBGP, iBGP, route-reflector client/server, confederation,
route-server, multihop, numbered/unnumbered, dynamic-neighbor/listen, peer-group,
and VRF-scoped operation. Route reflection, confederation, route-server, VPN,
EVPN, and FlowSpec policies retain distinct typed semantics; they are not
flattened into a generic text route-map whose evaluation order is hidden.

Authentication material for TCP MD5, TCP-AO, or later admitted mechanisms is
owned by `agent-keyring` and delivered only through a bounded endpoint-
specific use. RPKI origin validation, ASPA, BGPsec, BGP Roles/OTC, GTSM,
prefix/attribute limits, and own-prefix/own-AS leak controls are explicit
capability/policy states. If a required validator, trust anchor, key, peer
identity, or current validation generation is unavailable, the affected
session/family follows its declared fail-closed or last-known-good policy and
cannot silently become unvalidated.

Configuration lifecycle uses a candidate generation, semantic validation,
peer-impact and route-delta preview, provider syntax preflight, staged apply,
bounded convergence observation, and commit or rollback. Management-path
risk requires commit-confirmed. Timeout, process loss, partial family
activation, RIB/FIB disagreement, cursor gaps, and incomplete telemetry are
unknown/degraded states requiring reconciliation, never proof of success.

Protocol telemetry is bounded and typed. `bfw-frr` may expose authorized peer,
family, capability, route-decision, policy, validation, restart, BFD, and
convergence facts; BMP and MRT destinations require separate authority and
retention/redaction limits. Raw daemon text, unbounded route dumps, and
provider-private state do not become canonical audit evidence.

The BGP suite remains deferred outside v0.1. No BGP session, FRR process,
component repository, route mutation, or support claim exists merely because
this architecture is specified.

### Comprehensive routing-protocol suite

`bfw-routing` owns one canonical protocol-independent route model and the
installed-route plan. Protocol engines remain separately supervised adapters.
The first provider is `bfw-frr`, whose documented suite includes BGP, OSPFv2,
OSPFv3, RIPv1/RIPv2/RIPng, IS-IS, PIM/MSDP, LDP, BFD, Babel, VRRP, and alpha
EIGRP/NHRP support. Provider documentation is inventory, not admission: every
protocol/version/feature/platform row still requires a typed contract and
evidence. GoKA retains Bifrost HA/VRRP ownership; FRR's VRRP implementation
cannot create a second HA authority.

```text
typed protocol intent
  -> core admission
  -> bfw-routing ownership, recursion, redistribution, and route-policy checks
  -> one admitted protocol-provider adapter
  -> protocol-local adjacency/database/RIB computation
  -> typed candidate routes, withdrawals, and completeness observations
  -> bfw-routing canonical selection and platform route plan
  -> independent native-state and packet oracle
```

The routing matrix separates BGP; OSPFv2/v3; IS-IS; RIP/RIPng; Babel; EIGRP;
NHRP; IGMP/MLD/PIM/MSDP multicast routing; LDP/MPLS; SR-MPLS/SRv6; RSVP-TE;
PCEP; and BFD. It also keeps named unsupported rows for protocols not supplied
by the admitted provider, including mesh/IoT, deprecated, experimental, and
vendor fabrics. A new provider is a new supervised component boundary, not a
reason to add protocol parsing or daemon control to core.

Redistribution is an explicit typed edge between two protocol domains. It
preserves source protocol, route identity, policy generation, tags/communities,
metric mapping, scope, validation state, and loop-prevention provenance. The
default graph contains no redistribution edges. A candidate graph is rejected
if feedback, unbounded amplification, ambiguous preference, or incomplete
withdrawal cannot be excluded.

BFD is a shared liveness service keyed by endpoint, interface/VRF, mode,
authentication, timers, and generation. Consumers subscribe to typed liveness
facts and apply their own dampened transition policy; they do not launch
duplicate sessions or reinterpret an old discriminator after restart.

Cross-protocol convergence is complete only when protocol databases, candidate
routes, the canonical RIB, the native FIB, dependent policy, and independent
packet paths agree for one generation. Missing database pages, provider loss,
partial redistribution, unknown withdrawal, or RIB/FIB drift is degraded and
blocks commit or triggers the admitted conservative recovery policy.

Dynamic routing beyond the already defined static/local v0.1 route scope is
deferred. This architecture creates no protocol daemon or route.

### Comprehensive switching-protocol suite

`bfw-switching` owns canonical Layer-2 topology and protocol intent. Native
kernel/bridge mechanisms, switch daemons, ASIC SDKs, and vendor agents are
platform/provider adapters; none may bypass the typed plan, observed-state,
verification, audit, or rollback boundary. `bfw-routing`, `bfw-fabric`,
`bfw-qos`, `bfw-identity`, `bfw-dhcp`, `bfw-firewall`, and `agent-keyring`
retain their respective Layer-3, fabric, queue, identity, lease, enforcement,
and secret authorities.

The switching matrix has independent rows for VLAN/802.1Q and provider
bridging/Q-in-Q; MVRP/GVRP/VTP; STP/RSTP/MSTP and vendor PVST profiles; static
LAG/LACP and multi-chassis variants; LLDP/LLDP-MED and vendor discovery;
IGMP/MLD snooping and MVR; 802.1X/EAPOL, MACsec/MKA, and port protections;
VXLAN/GENEVE/NVGRE overlays; SPB/TRILL/ERPS/REP/vendor fabrics; DCB/TSN/QoS;
and Ethernet OAM. Standards-track, legacy, vendor, hardware, and deprecated
profiles remain distinct. Similar names or packet formats do not establish
semantic parity.

```text
typed switching intent
  -> core admission and cross-domain dependency resolution
  -> bfw-switching topology/protocol compiler
  -> admitted software, daemon, or hardware adapter
  -> protocol and native-state convergence
  -> independent control-frame and packet-path oracle
  -> commit or rollback
```

Peer control frames are untrusted. BPDU, LACPDU, LLDP, EAPOL, OAM, discovery,
multicast, and overlay inputs are parsed with exact dialects and byte,
cardinality, timer, rate, topology, and retained-state bounds. A peer's claim
about identity, root/role, aggregation, VLAN, management address, endpoint, or
health is an observation subject to policy; it is never configuration
authority.

Management-risking VLAN, STP, LAG, overlay, multi-chassis, or port-security
changes require independent path preflight and commit-confirmed rollback. A
loop, duplicate owner, split brain, ambiguous native VLAN, cross-tenant leak,
partial offload, incomplete observation, or unsupported semantic gap fails
closed or isolates the affected scope according to an explicit policy.

The v0.1 software-switch baseline remains limited to its already declared
VLAN, FDB, STP, LACP, snooping, and local Layer-3 subset. The broader switching
matrix is deferred and cannot be inferred from this architecture.

### Sticky endpoint-binding architecture

Sticky ports are two explicit endpoint-security mechanisms under one operator
contract; they are not multi-WAN flow affinity and are not one fake abstraction
over incompatible data structures.

For a switched port, `bfw-switching` owns a sticky binding whose key contains
the physical or logical port generation, bridge domain, VLAN/PVID, source MAC,
and optional authenticated endpoint identity. Dynamic learning creates a
bounded `pending` observation. Only the configured enrollment policy and core
admission can promote it to persistent canonical state. Static FDB entries,
sticky entries, ordinary learned entries, LAG membership, overlays, and
hardware-offloaded entries remain distinct and cannot silently replace one
another.

For a routed port, `bfw-network` identifies the interface and link generation;
`bfw-routing` owns VRF, encapsulation, address-family, and neighbor scope; and
`bfw-firewall` owns source enforcement. The sticky key includes interface
generation, VRF, VLAN or other encapsulation, address family, MAC when the link
has one, and admitted IP address or prefix. ARP, NDP, DHCP, authenticated
access, and configured facts are typed evidence inputs, not independent
authority. A routed endpoint binding does not manufacture an FDB entry or a
route.

```text
bounded endpoint observation
  -> pending binding with exact port/interface generation and scope
  -> policy validation and operator/automatic-enrollment admission
  -> cross-domain prepare and independent conflict check
  -> provider enforcement plus observed-state/packet verification
  -> active persistent binding or rollback
```

Unknown, excess, moved, duplicated, stale, or provider-disputed identities
default to drop and alarm. Explicit profiles may restrict, quarantine, or
disable the affected port, but a violation never causes automatic relearning
or replacement. Clearing or replacing a binding is a new authorized audited
transaction. Reboot, upgrade, failover, interface recreation, LAG change, and
rollback bind to generations so a stale port identity cannot inherit access.

## Deployment-role architecture

`governance/deployment-profiles.toml` defines three roles over the same core,
API, CLI, web shell, canonical configuration, audit history, and release:

| Role | Required data-plane domains | Denied by default |
| --- | --- | --- |
| `router` | network, routing, firewall | user-traffic Layer-2 bridge forwarding |
| `switch` | network, switching, routing | WAN-edge routing, NAT, and implicit Layer-4 policy |
| `converged` | network, switching, routing, firewall | no admitted domain; all cross-domain effects remain explicitly configured |

A management-only address is outside the user forwarding role. In switch mode
it terminates authorized management traffic but cannot become a transit
interface. Separately configured switch SVIs and routed switchports may use
`bfw-routing` for inter-VLAN and local-fabric Layer-3 switching without
enabling WAN-edge routing, NAT, or Layer-4-aware policy. Likewise, incidental
OS bridges in router mode do not create a configurable switching domain or
appear as switch authority.

Layer terminology describes admitted packet effects, not component privilege:

- Layer 2 switch effects—VLAN forwarding, FDB, STP-family control, and LACP—are
  owned by `bfw-switching`.
- Layer 3 switch and router effects—SVIs, routed ports, route tables/VRFs,
  inter-VLAN, local-fabric, and edge routes—are owned by `bfw-routing`.
- Layer 4-aware router effects—stateful TCP/UDP policy, NAT, port forwarding,
  connection tracking, and transport-aware steering—are owned by
  `bfw-firewall`.

Layer 4 awareness does not silently grant reverse-proxy, TLS termination,
payload inspection, application identity, or other Layer-7 authority. Those
remain separately admitted components and contracts.

Profiles are evaluated against the exact release composition and platform
capability report. Required missing, unhealthy, incompatible, or unadmitted
capabilities reject selection. Optional features remain absent rather than
being emulated with weaker semantics. "Full-featured" describes the governed
product direction; the selected profile exposes the admitted intersection of
catalog, release, platform, driver, and hardware support.

A role transition starts from a private candidate and computes removed,
retained, and added forwarding effects. The core validates configuration
compatibility, isolation, management reachability, dependencies, and rollback;
orders domain withdrawal and activation; verifies native state and independent
packet oracles; and commits only after confirmation. Restart, timeout, lost
management, partial apply, or incomplete observation restores the verified
last-known-good role and configuration or enters a conservative failed-closed
state.

## Distributed fabric architecture

Fabric scope is orthogonal to deployment role: every router, switch, or
converged node is either `standalone` or a member of one admitted fabric. The
same canonical configuration, identity, API, CLI, audit, transaction, and
release contracts apply. Fabric membership does not create a second management
plane.

`bfw-fabric` owns cluster topology, node capability/placement decisions,
convergence intent, and the generation-bound multi-node transaction. It asks
the existing domain owners to compile node-local plans:

```text
canonical signed fabric generation
  -> bfw-fabric validates membership, topology, placement, and barriers
  -> bfw-switching compiles node-local Layer-2/overlay effects
  -> bfw-routing / bfw-frr compile routes and EVPN-class advertisements
  -> bfw-firewall compiles node-local distributed policy placement
  -> core coordinates staged apply, independent verification, commit/rollback
```

The fabric component cannot manufacture a bridge, route, or firewall rule and
cannot call peer plugins as authority. Every node binds the plan to the same
configuration generation, release/capability set, leader term, membership
epoch, participant generations, and transaction identity.

The Layer-2 fabric supports admitted VXLAN/GENEVE-class overlays and
EVPN-class MAC/IP distribution with VNI/bridge-domain identity, split horizon,
designated forwarding, bounded BUM replication, ARP/ND suppression, mobility
sequence, duplicate endpoint detection, and bounded learning/aging. The Layer-3
fabric supports VRFs, routed VNIs, distributed anycast gateways, ECMP,
route-target import/export, explicitly authorized route leaking, and next-hop
reachability. Dynamic protocol behavior is supplied through the typed
`bfw-frr` contract; `bfw-fabric` does not become a BGP implementation.

Distributed firewall policy is compiled from one canonical policy generation
into deterministic node-local ingress, egress, transit, workload, and service
placements. Mobility preserves endpoint/zone identity. Stateful flows declare
whether symmetry is required, how paths are steered, which node owns state,
whether state is replicated, and how stale or unavailable state behaves.
Unknown placement or state ownership never widens connectivity.

Membership uses cryptographic node identity and current liveness/generation
proved by the admitted `rpc-plugin-system` substrate, with durable control
credentials and rotation/revocation material held by `agent-keyring`.
`bfw-identity` remains the generic human OIDC relying-party component and is
not a node trust root. Enrollment/revocation, encrypted authenticated control
channels, and compatible release/schema/capabilities are mandatory. Canonical
mutations require quorum,
monotonic generations, leader/term identity, fencing, durable journaling, and
idempotent reconciliation. Minority or ambiguous partitions retain last-known-
good local enforcement and cannot accept conflicting writes.

Every fabric member has exactly one placement record for a generation, and a
placement names at least one typed switch, route, or firewall plan. Duplicate,
missing, non-member, or all-null placements fail validation rather than
silently leaving a policy or forwarding gap.

### First-party Kubernetes-managed HA

A dedicated Kubernetes or K3s deployment may host `bfw-kubernetes-controller`
as a first-party out-of-the-box management and orchestration plane. It holds no independent
configuration authority: the canonical Bifrost API, authorization, audit,
generation, transaction, and rollback contracts remain authoritative. Managed
routers and switches run native signed Bifrost services plus an authenticated
agent; they are not required to be Kubernetes workers or expose a container
runtime.

The small-site profile permits one controller and labels it non-HA. Its loss
freezes new management mutations while nodes continue forwarding. The HA
profile requires an odd quorum of at least three controller members across
declared failure domains, with pinned durable storage and tested backup,
restore, upgrade, and quorum-recovery procedures. Controller replicas do not
replace native `bfw-ha` or `bfw-fabric` consensus, BFD, BGP/EVPN, ECMP,
gateway ownership, state replication, fencing, or node-local rollback.

The selected controller list is authoritative: its unique member count must
match the declared profile, be odd for HA, and map every controller to a
distinct admitted failure domain. Missing, duplicate, or unassigned members
fail validation. The controller may manage standalone or fabric-scoped nodes;
`bfw-fabric` is an integration, not a hard dependency of fleet management.

The controller distributes mutually authenticated, signed, generation-bound
typed plans. Each node independently authorizes, validates, applies, observes,
and either confirms or rolls back its own native effects. Kubernetes API,
scheduler, etcd, CNI, service network, overlay, storage, or controller failure
denies new mutations but cannot be a dependency of packet forwarding or local
recovery. A dedicated management VLAN or out-of-band path is preferred;
shared-path deployments require explicit admission and commit-confirmed local
recovery evidence.

Underlay/overlay admission includes MTU and encapsulation overhead, PMTU,
fragmentation, QoS/ECN preservation, hashing/entropy, loop prevention, BUM,
and hardware-offload semantics. A fabric change stages by dependency and
failure domain, uses readiness barriers/canaries and independent node/end-to-end
oracles, and either converges within a bound or rolls back/islands nodes under
an explicit safety policy. Control-plane loss never silently removes the last
verified node-local policy.

## Capability plugin catalog

The catalog is an ownership and planning map, not an ambient service bus. A
plugin calls no peer plugin as an authority. It proposes typed effects to the
core; the core validates the actor, dependency graph, permissions, generations,
ordering, failure behavior, and whole-transaction rollback before dispatching
each step to its owning component.

| Class | Planned plugins | Ownership summary |
| --- | --- | --- |
| Foundation | `bfw-firewall`, `bfw-network`, `bfw-switching`, `bfw-routing`, `bfw-wireguard`, `bfw-reverse-proxy`, `bfw-ha` | packet/NAT policy; ports/interfaces; Layer-2 switching; Layer-3 routes; WireGuard peers/tunnels; proxy ingress; failover coordination |
| Network services | `bfw-dns`, `bfw-dhcp`, `bfw-ntp`, `bfw-ddns`, `bfw-acme`, `bfw-mdns` | separately supervised core network services and their bounded configuration/status |
| Advanced network | `bfw-fabric`, `bfw-frr`, `bfw-ipsec`, `bfw-openvpn`, `bfw-qos`, `bfw-multiwan`, `bfw-cellular` | distributed fabrics, dynamic routing, alternate VPNs, shaping, uplink policy/failover, and modem integration |
| Security/access | `bfw-ids`, `bfw-dns-filter`, `bfw-threat-intel`, `bfw-captive-portal`, `bfw-radius`, `bfw-upnp` | inspection, filtering, signed feeds, guest access, AAA integration, and constrained dynamic mappings |
| Operations | `bfw-monitoring`, `bfw-logging`, `bfw-backup`, `bfw-support`, `bfw-notifications`, `bfw-updater` | metrics, event export, protected recovery artifacts, diagnostics, alert delivery, and signed updates |

Every entry declares plugin id and version, supported platforms, dependencies
and conflicts, permissions, schemas, UI/API versions, health and degradation,
migrations, activation and rollback, last-known-good effects, artifacts and
signatures, and verification evidence. A missing or unhealthy dependency blocks
mutation. Read-only bounded diagnostics may remain visible under the normal UI
catalog rules.

### WireGuard plugin boundary

`bfw-wireguard` owns WireGuard interface and peer desired state, endpoints,
public keys, AllowedIPs, persistent keepalive, handshake and transfer status,
per-device enrollment and revocation, key-rotation workflow, VPN-specific UI,
and VPN rollback consequences. It supports site-to-site and per-device remote
access; the common VPN contract remains open to later IPsec and OpenVPN plugins.

WireGuard authenticates devices by key rather than human users. OIDC can prove
the identity and assurance of an enrollment actor, but the core records a
separate device identity and approval. Each device has a unique key, address,
AllowedIPs, owner/audit link, creation and expiry, and revocation state. Private
and preshared keys are `agent-keyring` material and do not enter ordinary
configuration, QR-code caches, logs, UI state, plugin state, or support bundles.
One-time delivery must be bounded and non-replayable.

Activation is a coordinated transaction:

```text
admitted WireGuard peer/tunnel intent
  -> bfw-wireguard validates peer and tunnel semantics
  -> bfw-routing validates route ownership, overlap, loops, and reachability
  -> bfw-firewall validates forwarding, exposure, NAT, and kill-switch effects
  -> platform adapters stage/apply their owned native changes
  -> core verifies all observed state and commits, or rolls back the whole plan
```

Endpoint reachability, AllowedIPs ownership, overlapping prefixes, MTU,
failover, partial activation, and rollback are explicit. A tunnel becoming
healthy cannot silently authorize forwarded traffic.

### Reverse-proxy plugin boundary

`bfw-reverse-proxy` is a Bifrost-native Go ingress and reverse-proxy
implementation. Its operator experience may learn from Caddy's clear route,
automatic-certificate, and secure-default model, but Caddy is neither an
adapter nor a runtime dependency. The plugin does not embed Caddy packages,
invoke or supervise a Caddy process, generate Caddy configuration, or expose
Caddy's API/configuration as a Bifrost compatibility contract.

The plugin owns the bounded HTTP reverse-proxy data path and its control
domain: listeners, routes, upstream selection and health, header policy,
timeouts and body/stream bounds, TLS termination, service publication,
observations, and rollback. Protocol implementation may use the Go standard
library and separately admitted libraries, but every dependency and supported
HTTP/TLS feature requires its own provenance, compatibility, security, limit,
and conformance evidence.

The proxy plugin may request typed effects from `bfw-dns`, `bfw-acme`, and
`bfw-firewall`. It does not modify their state directly. Account keys, DNS API
tokens, private keys, and upstream credentials remain in `agent-keyring`.
Generated auxiliary artifacts use `agent-filesystem`; separately admitted
helper execution uses `agent-exec` only where a native API is insufficient.
Neither provider turns the native plugin into a wrapper around another proxy.

Forwarded identity is a separate trust contract. The proxy strips
client-supplied identity headers by default and may add authenticated identity
facts only for an exact admitted upstream, protected path, header set, network
path, key/certificate generation, and expiry. Merely installing or enabling the
proxy does not satisfy the OIDC forwarded-header exception in BFW-PRD-047.

TLS issuance failure, upstream-health uncertainty, protocol-limit uncertainty,
or partial route publication fails closed for the affected route without
weakening unrelated last-known-good routes. Firewall exposure and DNS
publication are committed only with verified proxy readiness or rolled back.

### High-availability plugin boundary

`bfw-ha` is formally named **GoKA** and implements the portable HA control
plane as a clean-room native Go engine. Keepalived is
a behavioral reference, not an embedded library, configured service, wrapped
executable, adapter, or runtime dependency. On platforms where Bifrost owns the
VRRP implementation, the plugin creates and validates protocol messages and
state transitions itself through admitted network APIs. FreeBSD may use the
kernel's native CARP facility through a narrow platform mechanism; other
platforms require an equivalent mechanism whose semantics are explicitly
mapped and tested. A platform without safe address-ownership and fencing
semantics reports the feature as unsupported rather than emulating it weakly.

Protocol compatibility is proved independently against the applicable VRRP or
platform specification and interoperable peers. Bifrost does not promise
Keepalived configuration-file, CLI, API, extension, or bug compatibility, and
no copied Keepalived implementation becomes a Bifrost public contract. GoKA is
implemented from public VRRP specifications, independently authored state-
machine and packet fixtures, and separately documented interoperability tests.
Clean-room provenance, dependency/source scans, and license review are release
evidence.

An optional importer may translate only an exact documented Keepalived dialect
subset into canonical GoKA intent. Unsupported directives, scripts,
notification hooks, IPVS/load-balancer behavior, include/order ambiguity, and
unknown semantics are hard errors. Imported text is never executed and does
not become a continuing configuration authority.

The plugin owns cluster membership intent, authenticated peer observations,
virtual-address role intent, priority/preemption and VRRP timer policy, bounded
typed health inputs,
configuration/state synchronization plans, transition ordering, HA UI, and
failover audit facts. Health checks declare interval, timeout, rise/fall,
weight, dependency, freshness, and incomplete behavior; arbitrary shell,
inherited environment, and ambient process access are denied. The network,
routing, firewall, service, keyring, and
release authorities retain their domains. `bfw-ha` cannot seize an address,
route, firewall role, or credential by calling a native command directly.

Before an active-role transition the core proves:

- peer and node identity plus current generation
- compatible Bifrost release composition and configuration revision
- declared quorum/witness or fencing policy and peer-loss behavior
- required replicated configuration and state checkpoints
- virtual-address ownership preconditions and duplicate-owner detection
- dependent routing, firewall, proxy/VPN/service readiness
- deterministic step order, confirmation where needed, and rollback/recovery

Split brain, stale state, ambiguous ownership, or loss of required fencing is a
fail-closed condition. The system preserves local packet safety even when it
cannot provide service availability. State synchronization must be typed and
bounded; it must not become general filesystem replication or a credential
export channel.

### Remaining plugin boundaries

- DNS, DHCP, NTP, DDNS, ACME, and mDNS are separate services so failure,
  upgrade, and platform support remain independently bounded.
- FRR contributes dynamic routes through the routing contract; it never writes
  canonical routes around `bfw-routing`.
- QoS and multi-WAN coordinate with firewall and routing through typed plans;
  sticky-connection state and health are explicit rather than hidden coupling.
- IDS/IPS and threat feeds propose signed/versioned observations or policy
  inputs; they cannot silently mutate firewall policy.
- UPnP/NAT-PMP/PCP is disabled by default and constrained by interface, client,
  protocol, port, lifetime, and audit policy.
- Monitoring, logging, backup, support, notifications, and updates must redact
  secrets and require explicit authority for external destinations or state
  changes.

### Native Go IDS/IPS boundary

`bfw-ids` is a native Go Snort-class detection engine, not a Snort process
adapter. Its data path is:

```text
admitted capture point / platform capture adapter
  -> packet and offload normalization
  -> bounded fragment/stream/flow reconstruction
  -> protocol decoders and canonical rule evaluation
  -> typed alert plus bounded evidence reference
  -> optional core-admitted bfw-firewall enforcement transaction
```

The engine owns packet normalization, flow/stream state, protocol decoding,
signature evaluation, threshold/suppression state, alert formation, and
detection health. It does not own interfaces, routes, firewall mutation,
credentials, evidence-file authority, external feeds, or process execution.
Feed credentials use `agent-keyring`; bounded PCAP/evidence artifacts use
`agent-filesystem`; enforcement is a typed proposal admitted by the core and
applied only by `bfw-firewall`.

Passive IDS and inline IPS are distinct admitted modes. Installing a rule never
enables inline enforcement. Each inline zone declares fail-open or fail-closed,
bypass behavior, backlog/resource limits, watchdogs, and recovery. Unknown
mode, packet loss, incomplete normalization, queue overflow, stream truncation,
or decoder exhaustion is explicit health/evidence and never a successful claim
of complete inspection.

Bifrost owns a canonical rule IR. A clean-room Snort-rule importer targets an
explicit dialect and feature matrix. Unsupported actions, keywords,
preprocessors, PCRE constructs, decoder assumptions, or ambiguous semantics are
hard errors. Safe matching uses bounded operators; a compatibility label never
waives resource limits or completeness oracles.

Rulesets are signed, provenance-bound, content-addressed, deterministically
compiled, staged, atomically activated, expirable, and rollback-capable. Alerts
carry rule/revision, capture point, normalized flow identity, classification,
confidence, action, timestamps, and incompleteness facts. Raw payload or PCAP
retention is opt-in, bounded, access-controlled, and separately audited.

Platform capture adapters must expose timestamp, checksum/offload, VLAN-tag,
multi-queue, zero-copy, injection, loss, and ordering semantics. Linux,
FreeBSD, and Windows implementations are admitted independently; a Snort-class
product goal is not a claim of complete Snort parity or endorsement.

## Management and plugin UI architecture

The management path is intentionally one-way through the core:

```text
browser
  -> HTTPS bfw-web role
  -> versioned authenticated core API
  -> core validation, authorization, confirmation, audit, and admission
  -> supervised plugin
  -> native OS or service API

local operator
  -> bfw CLI
  -> the same core API and admission path
```

ADR-0002 admits `bfwd` and `bfw-web` as public role names. The web service is
unprivileged, separately restartable, and incapable of direct
firewall, filesystem, keyring, execution-provider, or plugin-socket access.

### Cisco IOS-style CLI architecture

The `bfw` client deliberately adopts Cisco IOS command-line ergonomics while
retaining Bifrost's transactional authority boundary:

| Mode | Example prompt | Purpose |
| --- | --- | --- |
| user EXEC | `edge-1>` | bounded status and discovery |
| privileged EXEC | `edge-1#` | authorized operational actions and configuration entry |
| global configuration | `edge-1(config)#` | edit a private candidate configuration |
| domain configuration | `edge-1(config-if)#`, `edge-1(config-router)#`, `edge-1(config-firewall)#` | edit one typed domain within that candidate |

`enable` changes mode only after the core confirms current role and any required
step-up. It is not a shared-password authority path. Contextual help,
completion, and abbreviations come from one versioned grammar catalog filtered
by operator permissions and admitted plugin state. Plugin additions are signed,
declarative, namespaced grammar fragments bound to typed actions; executable
parser extensions and shell escapes are forbidden.

Configuration-mode input is parsed into a typed edit against a session-owned
candidate and its base generation. A typical safe flow is:

```text
edge-1# configure terminal
edge-1(config)# ...
edge-1(config)# show configuration diff
edge-1(config)# validate
edge-1(config)# commit confirmed 300
edge-1(config)# end
edge-1# confirm
```

The core performs authorization, schema and cross-domain validation, conflict
detection, deterministic planning, apply, verification, audit, and rollback.
An expired candidate, stale base generation, conflicting commit, lost required
confirmation, or failed verification cannot silently become current state.
`abort`/`discard` removes the candidate without changing live state.

`show running-config` is a deterministic, authorization-filtered rendering of
canonical structured state. It is useful for operators, diffs, and migration,
but is not a writable source of truth. Automation uses complete canonical
commands or versioned structured output, never interactive abbreviation or
terminal screen scraping. Sensitive input is excluded from history and all
rendering and audit paths apply field-aware redaction.

### UI contribution package

A signed plugin release may contain a UI contribution manifest with:

- plugin id, plugin version, UI contract version, and compatible core API range
- namespaced navigation groups and routes
- declarative configuration and result schemas
- forms, tables, status panels, validation, confirmation, and error mappings
- typed core action identifiers and required display/action permissions
- localization and accessibility metadata
- content-addressed asset names, digests, sizes, media types, and CSP class
- optional custom-bundle declaration and sandbox capability request

The core verifies the same package signature, provenance, compatibility,
permissions, migrations, and asset digests used for backend admission. It then
publishes a sanitized UI catalog filtered by the authenticated operator's
display permissions and the admitted plugin state. The web service never asks a
plugin executable which pages or scripts to load.

Declarative UI is the default. Shared BFW components render ordinary DNS, DHCP,
VPN, monitoring, and package pages consistently and keep validation,
confirmation, accessibility, localization, and error behavior in the trusted
shell. For example, a DHCP package can contribute Leases, Pools, Reservations,
and Options views whose forms bind to typed actions such as
`dhcp.pool.update`; the browser cannot edit a daemon configuration file or call
the DHCP process.

### Rich extension isolation

A feature such as a topology viewer, high-rate graph, or packet-capture viewer
may require custom frontend code. Such code is never inserted into the trusted
DOM or granted the web application's origin. Its signed, content-addressed
bundle runs in a separate-origin sandboxed frame with a restrictive CSP and a
versioned capability-based message channel.

The sandbox denies BFW cookies and tokens, keyring access, canonical state,
filesystem paths, plugin sockets, top navigation, trusted-DOM access, arbitrary
network requests, and undeclared browser capabilities. The host sends only
typed, bounded, authorization-filtered data and accepts only typed action
proposals, which still pass through the core API. A bundle signature proves
provenance; it does not grant permissions.

### Lifecycle and degradation

The plugin backend, UI manifest, schemas, migrations, and assets form one
versioned release unit. Staging verifies all parts before activation; activation
publishes the new backend generation and UI catalog atomically; rollback restores
the last compatible pair. Content-addressed assets prevent path substitution
and make cached content verifiable.

Disabled, removed, incompatible, or untrusted plugins have no active UI routes.
An unhealthy but admitted plugin may retain a clearly degraded read-only status
and diagnostic page so operators can repair it; mutating actions are denied.
Web or UI failure never affects native packet policy. The `bfw` CLI and local
console recovery remain available when the web service is down.

## OIDC identity architecture

OIDC is the primary federated authentication contract for the web UI. Authentik
is an intended integration target, but Bifrost depends on the OIDC standard and
an explicit compatibility profile rather than Authentik-specific APIs.

```text
browser
  -> bfw-web begins Authorization Code + PKCE transaction
  -> configured OIDC provider authenticates the user
  -> bfw-web receives the exact registered callback
  -> identity boundary validates code/token response and trust facts
  -> core maps issuer + subject + admitted claims to Bifrost roles
  -> core issues a short-lived opaque Bifrost session
  -> browser calls the core API through bfw-web
```

The identity boundary validates discovery metadata, exact issuer, signed ID
token algorithm and key, JWKS rotation, audience, authorized party where
required, nonce, state, expiry, not-before, authentication time, and configured
assurance requirements. Redirect origins and client ids are exact allowlists.
TLS is mandatory outside explicit loopback development.

OIDC proves identity; it does not grant Bifrost authority. Role mapping is a
versioned core policy keyed by allowed issuer and stable subject, with explicit
claim transforms and deny-by-default behavior. A provider group named `admin`
does not create a Bifrost administrator unless an operator has admitted that
exact mapping. High-risk actions may require a configured authentication age or
assurance level and still pass normal Bifrost confirmation.

`agent-keyring` owns confidential-client secrets, private keys, refresh tokens,
and any reusable provider credential. The web and identity components use
scoped opaque keyring authority; secrets never appear in configuration,
environment, argv, logs, exports, browser storage, UI manifests, or plugins.
OIDC tokens are consumed at the identity boundary and are never forwarded to
plugins or used as Bifrost API bearer tokens.

After validation, the core issues an opaque Bifrost session bound to issuer,
subject, client, authentication time/assurance, role-policy generation,
session generation, and expiry. The browser receives a Secure, HttpOnly,
appropriately SameSite cookie. Sessions have inactivity and absolute expiry,
rotation, CSRF protection, explicit logout, and revocation behavior. Plugins see
only the admitted actor id, authorization/assurance facts required for the
action, and audit correlation.

New logins fail closed when provider discovery or keys cannot be validated.
Already admitted sessions may continue only to their bounded expiry without
claim or privilege refresh. A separate local-console recovery identity remains
available for OIDC, DNS, certificate, or management-network failure; it is
strongly protected, audited, and never exposed as an automatic remote-login
fallback.

## Credential authority

Credential management is a separate trust boundary from action authorization:

```text
browser or operator
  -> unprivileged bfw-web
  -> bfwd validates and admits the exact action
  -> agent-keyring issues a scoped, short-lived lease or opaque reference
  -> admitted plugin or host-mediated executor performs the exact use
  -> Bifrost and agent-keyring record correlated, redacted audit evidence
```

`agent-keyring` is the sole credential authority. Bifrost's canonical state may
contain a credential selector and non-secret binding metadata, but never the
secret payload, an exportable private key, a reusable token, or an ambient
credential path. The web UI and ordinary plugins cannot request raw secrets or
talk around core admission.

The core's admission record must exist before keyring access. Every lease or
non-exporting reference is bound to the admitted caller and action, runtime and
provider generations, target and audience, usage and access mode, policy and
credential generations, keyring authority generation, and a short expiry.
Rotation, revocation, restore, restart, or a relevant generation change
invalidates stale authority. Credential possession never substitutes for core
authorization.

Provider operations should prefer non-exporting references. For example, an
ACME or VPN plugin receives authority for one admitted operation without
receiving a reusable account key. Secret-bearing response types, if a future
contract admits them at all, must remain distinct, non-loggable, narrowly
scoped, and unavailable to the web UI.

## Filesystem and execution providers

Bifrost uses `agent-filesystem` for admitted host-file work outside the core's
private canonical state: generated service configuration, bounded imports and
exports, backup artifacts, diagnostics, and support bundles. The core remains
responsible for its own private transactional state and migrations; neither a
plugin nor the web UI receives ambient access to it.

Every file operation carries an admitted root and operation set, byte and
recursion bounds, link and special-file policy, mutation preconditions,
generation/expiry, recovery requirements, and audit correlation. Paths, file
descriptors, trash/COW records, rollback references, and provider-private
storage are never reusable authority. Secret-denied scopes must cover keyring
payload and authority storage.

Bifrost uses `agent-exec` only when an admitted operation genuinely requires a
local process. Native OS APIs remain the preferred path for firewall, routing,
and interface mutations. The execution envelope binds executable identity and
resolution, argv or an explicitly admitted shell payload, cwd, environment,
stdio, timeout/cancellation, process tree, resources, network policy,
filesystem containment, side-effect class, idempotency, generation/expiry, and
audit rules. Cwd is not containment; process reachability is not permission.

Shell execution, PATH lookup, inherited environment, network access, and
privilege transitions are denied unless separately and explicitly admitted.
Credentials are never placed in argv, environment, stdin, output, transcripts,
or diagnostics. If an operation needs credential use, `agent-keyring` supplies
an opaque, scoped authority reference through the admitted mediation contract;
`agent-exec` does not read the keyring or collect passwords.

Multi-provider composition is fail-closed:

```text
one sealed Bifrost action plan
  -> distinct keyring authority use, if required
  -> distinct filesystem authority use, if required
  -> distinct execution authority use, if required
  -> correlated redacted result and audit evidence
```

Each use is bound to the same action, target/audience, policy, correlation, and
current provider/plugin generations. File content does not become a command,
a command result does not become a path, and a provider-owned reference does
not cross a boundary unless the sealed plan explicitly types, bounds, and
admits that transfer.

## Linux learning-alpha boundary

The learning alpha is a disposable, single-node Alpine Linux x86-64 appliance,
not a smaller claim of the final product. It uses only the Linux software data
plane (`nftables`, netlink, and software bridge), one pinned machine/VM profile,
and a pinned `rpc-plugin-system` v2 plus Linux-compatible keyring, filesystem,
and execution providers. The canonical core remains the sole configuration and
action authority; narrowing the platform does not create a second control
plane inside adapters or the UI.

Source implementation and offline simulation are low-effect work exempt from
Phase 0 only after normal workflow activation. Designated host-network
mutation, installer-disk mutation, and distributable alpha media
are separate effects and stay disabled until `BFW-ALPHA-0` passes. The gate
binds each effect to an immutable dependency set, safety evidence, and
independent review. No gate is inferred from a demo working once.

```text
source + unit + deterministic offline tests
  -> disposable namespace/VM tests
  -> BFW-ALPHA-0 safety and dependency admission
  -> designated non-production host/network/disk execution
  -> signed alpha artifact with explicit limitations
  -X-> beta, stable, production, or cross-platform admission
```

The alpha retains hard authority invariants: stable disk identity before
destruction, fail-closed packet state, opaque secret custody, transactional
configuration, stale-generation denial, bounded recovery/reset, and unknown
state reported as unknown. It may omit features, optimization, polish, broad
hardware coverage, seamless upgrades, and long-term compatibility. Alpha state
and media are visibly channel-bound and cannot be accepted by beta or stable
trust roots.

The alpha is the only runtime implementation lane before full Phase 0. Product
requirements, architecture, decomposition, and hostile review may continue,
but no implementation outside its exact scope begins until every Phase 0
dependency independently holds an A or A+ admission. One excellent dependency
cannot compensate for a weaker one, and a successful integrated demo proves
nothing about a substrate's independent grade.

## Beta and stable cross-platform substrate prerequisite

The current `rpc-plugin-system` v1 contract uses Unix-domain sockets, Go
`net/rpc`/gob, and Linux `SO_PEERCRED` hardening. Bifrost must not fork that
contract inside provider plugins. Before Bifrost depends on it across platforms,
the substrate must define and test:

- Unix-domain-socket and Windows-named-pipe transports behind one standard
- Linux, BSD/macOS, and Windows peer-identity adapters
- explicit protocol and capability-version negotiation
- an externally consumable, versioned SDK/module
- matching generation, auth, timeout, cancellation, logging, and teardown
  behavior on every supported platform

This substrate is a predecessor to beta and stable admission, not a parallel
convenience task. Bifrost design and bounded Linux-alpha implementation may
continue under `BFW-ALPHA-0`, but beta, stable, production, and cross-platform
claims remain blocked until the full substrate is complete and independently
admitted. Bifrost must not carry provider-local transport, authentication,
generation, lifecycle, or supervision forks as a shortcut.

The current `agent-keyring` v1 service also uses a local Unix-domain socket.
Before Bifrost integrates credentials across platforms, the credential
substrate must preserve the same authority semantics across Unix sockets and
Windows named pipes, platform peer identity, encrypted payload storage and
unlock, SDK compatibility, redaction, lease/ref invalidation, backup/restore,
and recovery. Platform storage adapters may protect keyring material, but they
must not become competing sources of credential truth.

The current `agent-filesystem` v1 is a local POSIX provider, and the current
`agent-exec` contract is centered on local Linux/dedicated-account execution.
Before Bifrost depends on them across platforms, their contracts must define
and test Windows and supported BSD/macOS path/process semantics, race-safe path
containment, symlink/reparse-point behavior, atomicity and durability,
trash/recovery semantics, executable identity, account/sandbox/resource
controls, cancellation/process-tree behavior, opaque lifecycle references,
and consistent audit redaction. Unsupported security semantics fail closed;
provider-local compatibility shortcuts are forbidden.

## Alpine Linux appliance and installer architecture

Alpine Linux is the canonical base distribution for Bifrost's first-party
Linux appliance. The initial design baseline is Alpine 3.24 stable. Each
released composition pins an exact patch release and immutable repository
snapshot, package set, signing keys, kernel sources/packages, build toolchain,
normalized inventory schema, signed tailoring policy, generic recovery kernel/
initramfs/environment, modules, firmware, bootloader, CPU architecture,
installer source revision, and ISO digest. Alpine edge and live repository
resolution are build inputs only for development experiments and are forbidden
in admitted release composition.

`bfw-installer` is a separately versioned distribution component. It consumes
the signed Bifrost release composition and produces a generic bootable live ISO
that deterministically creates a machine-tailored installed appliance; it does
not own policy, credentials, interfaces, routes, switching, or post-install
configuration. The meta repository pins the installer revision and every media
input/output digest. Independent rebuilds compare the ISO, boot artifacts,
packages, SBOM, and provenance rather than trusting installer exit status.

After boot, the live installer records normalized CPU, boot, console, NIC,
storage, virtualization, and firmware facts and matches them to the signed
hardware matrix. It derives the machine install manifest before destructive
confirmation. The normal offline path selects only required signed APKs,
services, kernel flavor/modules, firmware, boot files, and Bifrost components,
then generates the exact initramfs and module-load closure. It never trims an
installed package by deleting APK-owned files.

If no admitted prebuilt kernel/module set satisfies the machine, an explicit
resource-estimated slow path may build only the required kernel/module layer
from pinned sources and toolchain. Rebuilding Alpine as a whole on the target is
unsupported. The content-addressed machine inventory, plan, APK/file manifest,
custom layer if any, and slot digest are sealed into installed and durable
evidence. Release signatures cover selectable inputs and policy; the ISO does
not carry a release-signing private key. A signed broad generic recovery kernel,
initramfs, and environment remain separately bootable.

```text
immutable Alpine and Bifrost release composition
  -> isolated reproducible generic live-ISO and APK/input build
  -> signed live ISO, recovery environment, SBOM, provenance, and checksums
  -> UEFI or legacy-BIOS boot on an admitted x86-64 profile
  -> normalized hardware inventory and deterministic machine install manifest
  -> stable target-disk identity
  -> explicit destructive confirmation naming that disk
  -> offline machine-tailored build/install into inactive system content
  -> retain signed generic recovery kernel/initramfs/environment
  -> first boot into an unconfigured fail-closed appliance
  -> local recovery/bootstrap or authenticated configuration enrollment
```

The installer never chooses a target from `/dev` enumeration order alone and
never performs a destructive write before showing stable device identity,
capacity, model/serial when available, planned layout, and the exact data-loss
boundary. Cancellation, power loss, media corruption, or package verification
failure leaves the target either recognizably uninstalled or recoverable; it
cannot report partial installation as bootable success. Secrets are entered at
the local console or enrolled after boot and are not embedded in media, logs,
kernel arguments, environment, or reusable answer files.

The installed system is a declared appliance, not a general-purpose Alpine
host with an undocumented pile of packages. Its package/service set, boot and
init behavior, writable state, service identities, network defaults, and
kernel/runtime features are release artifacts. Bifrost configuration,
evidence, and recovery state are separated from replaceable system content.
Ad-hoc `apk` changes and repository drift are unsupported release drift and
must be surfaced; they do not silently become the new normal.

Separately distributed prebuilt Alpine hardware-specific media and appliance
SKUs require a later approved product profile naming exact hardware, firmware,
lifecycle, replacement, and support obligations. That deferral does not apply
to the generic live installer's deterministic machine tailoring.

FreeBSD and Windows remain separately admitted compatibility targets. They are
not alternate bases for the Bifrost Linux ISO, and Alpine-specific packaging
does not weaken Bifrost's provider-neutral domain contracts.

## FreeBSD appliance and installer architecture

FreeBSD is the canonical base for Bifrost's first-party BSD appliance. Its
initial distribution profile is a generic x86-64 live installation ISO that
builds a machine-tailored installed system, not a vendor-appliance image and
not a promise to boot every x86-64 machine. Each released composition pins the
supported FreeBSD release and source revision, source/object sets, source-build
options, build toolchain, inventory schema, tailoring policy, recovery
kernel/environment, firmware, boot artifacts, private package-repository
snapshot, packages, builder, installer revision, and ISO digest. The published
live-media hardware matrix is part of the signed release claim.

`bfw-installer` uses supported FreeBSD source-build controls and a NanoBSD-style
appliance layout to produce read-only or integrity-verified system content,
two independently verifiable code/root slots, and separate durable
configuration, audit/evidence, and recovery state. Reduction is declarative:
`src.conf`, kernel configuration, and the signed package manifest define every
omission. Deleting files from an installed system is drift, not an image-build
method. PF, routing, bridge/VLAN, CARP/pfsync, IPsec, audit, cryptographic and
signature-verification support, local recovery, filesystem repair,
observability, promised firmware, and promised drivers remain present whenever
the admitted profile requires them.

After the live environment boots, the installer records normalized CPU, boot,
console, NIC, storage, virtualization, and firmware facts and matches them to
the signed hardware matrix. It deterministically derives a machine build
manifest before destructive confirmation. The default path installs pinned
prebuilt base sets and packages, then builds only the kernel/modules that must
be machine-specific. A full on-target source build is an explicit slower mode,
never an accidental consequence of installation. Both paths are offline and
use the same signed inputs, dependency-closure rules, and resource bounds.

The machine build manifest is content-addressed and sealed into both the
installed slot and durable evidence; it is not falsely represented as a
vendor-signed artifact created with a private key embedded in the ISO. Release
signatures cover every selectable input and the deterministic selection policy.
A signed generic recovery kernel/environment with the admitted broad driver set
remains available so a bad inventory or over-reduced primary kernel cannot
destroy local recovery.

```text
immutable FreeBSD source, package, and Bifrost composition
  -> isolated base/object/package and generic live-ISO build
  -> reproducible generic x86-64 live ISO, SBOM, and provenance
  -> UEFI or legacy-BIOS boot on a published hardware-matrix row
  -> normalized hardware inventory and deterministic machine build manifest
  -> stable target-disk inventory and explicit destructive confirmation
  -> offline machine-tailored build/install into inactive system slots
  -> retain signed generic recovery kernel/environment plus durable state
  -> first boot into an unconfigured fail-closed appliance
  -> independent native-state and packet verification before enrollment
```

The FreeBSD and Alpine artifacts share Bifrost schemas, authority boundaries,
release semantics, UI/CLI behavior, and audit contracts. They do not share
platform admission by implication. Each has independent platform adapters,
native-state oracles, installers, update mechanics, package/firmware manifests,
hardware matrices, performance bounds, and verification evidence.

Separately distributed prebuilt hardware-specific media and appliance SKUs are
deferred. They require a later product profile naming exact boards, NICs,
storage, firmware, boot path, lifecycle, replacement policy, and support
obligations. This does not prohibit the generic live installer from producing
the machine-tailored installed composition defined above.

## Recovery

ADR-0005 and `documents/RELEASE-RECOVERY.md` define the recovery baseline:
verified last-known-good release/configuration pairs, A/B image activation where
the platform supports it, bounded boot confirmation, rollback-compatible
configuration migration, `commit confirmed` for management-risk changes, and a
typed audited local-console recovery path. Exact boot selection and durability
mechanics remain platform contracts and block each platform until tested.
