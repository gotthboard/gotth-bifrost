# Bifrost (BFW) Product Requirements

Status: active product and governance baseline; runtime not admitted

## Product objective

Build a cross-platform Go firewall and routing system that provides a coherent
administration plane over proven native packet-processing and networking
facilities. The system must prioritize safety, deterministic behavior,
recoverability, extensibility, and clear operational evidence over feature
count.

## Product identity

- **BFW-PRD-000:** The full product name shall be **Bifrost**, its canonical
  firewall shorthand shall be **BFW** (Bifrost Firewall), and its lowercase
  public command, package, configuration, and protocol namespace shall be
  `bfw`. The repository remains named `Bifrost`.

## Repository role

- **BFW-PRD-035:** `danny/Bifrost` shall be the Bifrost meta repository. It
  shall own canonical product requirements, architecture, implementation and
  release coordination, component/dependency mapping, compatibility contracts,
  release composition, and system-level verification evidence—not product
  runtime code.
- **BFW-PRD-036:** Runtime, CLI, web, platform, and optional capability
  implementations shall live in separately versioned component repositories.
  The meta repository shall pin admitted component revisions and verify their
  compatibility without copying or forking their source trees.
- **BFW-PRD-037:** Routing shall be owned by a separately versioned
  `bfw-routing` plugin rather than the Bifrost core. Its domain shall include
  static routes, gateways, policy routing, route health, ECMP where supported,
  and admitted dynamic-routing integration.
- **BFW-PRD-038:** `bfw-routing` shall emit typed, deterministic,
  idempotent routing plans and apply/verify them only through core admission and
  supported platform adapters. It shall not own global authorization,
  credentials, executable lifecycle, interface/VLAN authority, packet-filter
  policy, or release admission.
- **BFW-PRD-039:** Every Bifrost release shall identify exact component
  revisions, contract and schema versions, platform compatibility, migration
  order, signatures/provenance, verification evidence, and rollback pairing in
  a machine-readable release composition admitted by this meta repository.
- **BFW-PRD-040:** OpenID Connect shall be a first-class web-UI authentication
  method compatible with standards-compliant providers such as Authentik,
  without making any one provider a required Bifrost dependency.
- **BFW-PRD-041:** Browser login shall use OIDC Authorization Code with PKCE,
  exact registered redirect URIs, TLS outside explicit loopback development,
  cryptographically random state and nonce, and bounded login transactions.
- **BFW-PRD-042:** OIDC validation shall fail closed on issuer, discovery,
  signature/algorithm, JWKS, audience, authorized-party, nonce, state,
  expiration, not-before, authentication-time, or required-assurance mismatch.
  Key rotation shall be supported without accepting unknown or stale trust.
- **BFW-PRD-043:** OIDC shall authenticate identity only. The Bifrost core shall
  own explicit issuer/subject and claim-to-role mapping, deny unmapped privilege
  by default, and prohibit automatic administrator access based only on a group
  or claim name supplied by an identity provider.
- **BFW-PRD-044:** OIDC client secrets, private keys, refresh tokens, and other
  reusable credential material shall be governed by `agent-keyring` and shall
  not appear in ordinary configuration, environment, command arguments, logs,
  exports, browser storage, UI manifests, or plugin inputs.
- **BFW-PRD-045:** After successful OIDC validation and core role mapping, the
  browser shall receive only a short-lived opaque Bifrost session cookie with
  Secure, HttpOnly, appropriate SameSite, rotation, inactivity, absolute-expiry,
  logout, and CSRF protections. Raw OIDC tokens shall not become browser API
  bearer credentials.
- **BFW-PRD-046:** OIDC tokens and provider sessions shall not be forwarded to
  plugins. Plugins may receive only bounded actor, authorization, assurance,
  and audit-correlation facts admitted by the core for the requested action.
- **BFW-PRD-047:** OIDC configuration shall pin allowed issuers, client ids,
  redirect origins, signing algorithms, claim mappings, assurance requirements,
  and provider-specific compatibility facts. Forwarded identity headers shall
  be denied unless a separate authenticated reverse-proxy trust contract is
  explicitly admitted.
- **BFW-PRD-048:** Identity-provider or JWKS unavailability shall fail closed
  for new logins. Existing sessions may continue only until their already
  admitted bounded expiry and shall not gain new claims or privilege while
  provider state is unavailable.
- **BFW-PRD-049:** Bifrost shall retain a separately protected local-console
  recovery identity and recovery workflow that remains usable during OIDC,
  DNS, certificate, or management-network failure. It shall not silently become
  a general remote-password fallback.
- **BFW-PRD-050:** Authentication, claim mapping, session issuance/rotation,
  logout, denial, recovery, and administrative identity-policy changes shall be
  auditable without recording tokens, secrets, unnecessary claims, or sensitive
  provider payloads.

## Capability plugin catalog

- **BFW-PRD-051:** The meta repository shall maintain a canonical catalog of
  planned Bifrost capability plugins, their ownership boundaries, typed
  dependencies and conflicts, supported platforms, permissions, health model,
  UI contribution, migration/rollback behavior, and release-admission status.
  Catalog presence alone shall grant no authority and shall not imply that a
  component repository or runtime exists.
- **BFW-PRD-052:** `bfw-firewall` shall own packet-filter, NAT, alias, schedule,
  and state-policy semantics; `bfw-network` shall own ports, interfaces, MTU,
  DHCP-client, and link-state semantics; `bfw-switching` shall own Layer-2
  VLAN, bridge, FDB, STP, and LACP semantics; and `bfw-routing` shall own
  Layer-3 routing semantics. Cross-domain changes shall use one core-admitted
  transaction without collapsing these authorities.
- **BFW-PRD-053:** DNS, DHCP, NTP, dynamic DNS, ACME, and mDNS shall be
  separately versioned plugins (`bfw-dns`, `bfw-dhcp`, `bfw-ntp`, `bfw-ddns`,
  `bfw-acme`, and `bfw-mdns`) with bounded service configuration, status,
  platform-adapter, UI, failure, and rollback contracts.
- **BFW-PRD-054:** `bfw-wireguard` shall be the first VPN plugin and shall
  support site-to-site tunnels and per-device remote access while leaving the
  common VPN contract open to later `bfw-ipsec` and `bfw-openvpn` plugins.
- **BFW-PRD-055:** WireGuard private and preshared keys shall remain governed by
  `agent-keyring`. OIDC may authenticate an enrollment actor, but every remote
  device shall receive a distinct peer identity, address, AllowedIPs,
  lifecycle, expiry/revocation state, and audit correlation; reusable private
  keys shall not be shared among users or devices.
- **BFW-PRD-056:** WireGuard activation shall validate AllowedIPs ownership,
  overlapping networks, route conflicts and loops, endpoint reachability, MTU,
  firewall/NAT and kill-switch effects, failover behavior, and rollback before
  admitting a tunnel. Routing and firewall effects remain owned by their
  respective plugins.
- **BFW-PRD-057:** `bfw-reverse-proxy` shall provide a native Go reverse proxy
  and ingress capability with a Caddy-like operator experience. It shall own
  the proxy data/control path, routes, upstreams, health checks, TLS policy,
  service publication, observed state, UI contributions, and proxy-specific
  rollback without embedding, invoking, supervising, configuring, or requiring
  Caddy at runtime.
- **BFW-PRD-058:** `bfw-reverse-proxy` shall not become firewall, DNS,
  credential, or identity authority. Certificate and provider credentials
  shall use `agent-keyring`; DNS, ACME, and firewall exposure shall use typed
  dependencies; forwarded identity headers shall remain denied unless an
  explicit authenticated reverse-proxy trust contract is admitted by the core.
- **BFW-PRD-059:** `bfw-ha` shall implement portable high-availability control
  logic natively in Go, inspired by Keepalived behavior but without embedding,
  invoking, supervising, configuring, or requiring Keepalived at runtime. It
  shall use admitted VRRP, CARP, or safe platform-equivalent mechanisms for
  virtual addresses, peer/node health, active/standby roles, state and
  configuration synchronization, failover, recovery, and HA-specific UI and
  audit evidence.
- **BFW-PRD-060:** An HA role transition shall require authenticated peer
  identity, compatible configuration and release composition, current health,
  declared quorum/fencing and priority/preemption policy, required replicated
  state, deterministic ordering, and rollback evidence. Split brain, stale
  ownership, or uncertain virtual-address ownership shall fail closed.
- **BFW-PRD-061:** Advanced networking shall remain separated into
  `bfw-frr`, `bfw-ipsec`, `bfw-openvpn`, `bfw-qos`, `bfw-multiwan`, and
  `bfw-cellular`, coordinating with but not replacing the routing, firewall,
  network, credential, or lifecycle authorities.
- **BFW-PRD-062:** Security and access capabilities shall remain separated into
  `bfw-ids`, `bfw-dns-filter`, `bfw-threat-intel`, `bfw-captive-portal`,
  `bfw-radius`, and `bfw-upnp`. UPnP/NAT-PMP/PCP shall be disabled by default
  and constrained by explicit interface, client, protocol, port, lifetime, and
  audit policy.
- **BFW-PRD-063:** Operational capabilities shall remain separated into
  `bfw-monitoring`, `bfw-logging`, `bfw-backup`, `bfw-support`,
  `bfw-notifications`, and `bfw-updater`, with redaction, destination,
  retention, signature, compatibility, recovery, and external-side-effect
  contracts appropriate to each plugin.
- **BFW-PRD-064:** A plugin dependency shall be a typed, versioned,
  core-admitted contract rather than direct plugin-to-plugin authority. Missing,
  unhealthy, incompatible, or unauthorized dependencies shall block mutation
  and expose bounded diagnostic evidence without silently degrading safety.
- **BFW-PRD-065:** Every capability plugin shall declare exact platform support
  and platform-specific semantic gaps. Unsupported or weaker native semantics
  shall fail closed or require an explicitly admitted degraded mode; feature
  names shall not imply parity across Linux, FreeBSD, Windows, or macOS.
- **BFW-PRD-066:** Initial implementation priority shall be the bounded
  Linux-only learning alpha in BFW-PRD-215 through BFW-PRD-222. After full
  Phase 0, beta/stable priority shall be firewall, network/interfaces, routing,
  DNS, DHCP, WireGuard, ACME/DDNS, reverse proxy, monitoring/logging/backup,
  HA/multi-WAN, then IDS/IPS and dynamic routing. The sequence may change only
  through an explicit meta-repository planning and dependency decision.
- **BFW-PRD-067:** Every catalog plugin that exposes management functionality
  shall use the signed UI-contribution and typed-action contracts in
  BFW-PRD-025 through BFW-PRD-034; it shall not create a second management or
  authorization plane.
- **BFW-PRD-068:** Capability plugins shall use `agent-keyring`,
  `agent-filesystem`, and `agent-exec` only through separately admitted,
  generation-bound provider authority. A plugin category or adapter choice
  shall not widen credential, path, process, network, or privilege scope.
- **BFW-PRD-069:** The `bfw` client shall provide a Cisco IOS-style hierarchical
  command line with user EXEC, privileged EXEC, global configuration, and
  domain submodes, with stable prompts and the familiar `enable`, `disable`,
  `configure terminal`, `exit`, and `end` transitions.
- **BFW-PRD-070:** CLI mode transitions shall be presentation and workflow
  state, not authority. `enable` and configuration entry shall require the
  authenticated operator's current core authorization and any required
  step-up; a shared enable password shall not grant or widen authority.
- **BFW-PRD-071:** The interactive CLI shall provide contextual `?` help, tab
  completion, command-history navigation, and unambiguous abbreviations.
  Scripts and persisted command records shall use full canonical commands and
  versioned machine-readable output rather than ambiguous abbreviations or
  screen scraping.
- **BFW-PRD-072:** Every CLI command shall parse into a versioned typed core API
  action with schema-checked operands. The CLI shall not construct shell
  commands, edit canonical or native configuration files, invoke plugin
  sockets, or directly mutate firewall, routing, or service state.
- **BFW-PRD-073:** Configuration-mode commands shall modify a private,
  session-owned candidate bound to its operator, authorization context, base
  configuration generation, expiry, and audit correlation. They shall not
  mutate the running configuration before core admission and commit.
- **BFW-PRD-074:** The CLI shall support candidate display and diff, explicit
  validation, `commit`, bounded `commit confirmed`, and discard/abort. Commit
  shall use the normal transactional apply, verify, audit, and rollback path;
  stale generations, conflicts, disconnects, and missed confirmation shall
  fail closed or restore the last known-good state as defined by the action.
- **BFW-PRD-075:** `show` commands shall expose authorization-filtered running,
  candidate, operational, health, and audit views with stable structured-output
  forms. `show running-config` and any startup or recovery view shall be a
  deterministic rendering of canonical state, never a second configuration
  authority.
- **BFW-PRD-076:** Configuration grammar shall provide deterministic
  `no <command>` removal and `default <command>` reset semantics derived from
  the admitted schema. Absence, deletion, inheritance, and defaulting shall
  remain distinct where the domain model distinguishes them.
- **BFW-PRD-077:** A signed plugin may contribute namespaced declarative CLI
  grammar, help, schemas, and typed action bindings compatible with its admitted
  release. It shall not inject parser code, add shell escapes, bypass core
  authorization, or establish a second management plane.
- **BFW-PRD-078:** CLI history, completion, diagnostics, output, audit, and
  support artifacts shall redact or omit secrets and sensitive transient input.
  Local recovery shall use the same typed core actions and bounded recovery
  identity rather than direct host mutation.

## Executable meta-repository governance

- **BFW-PRD-079:** The meta repository shall maintain an authoritative
  machine-readable component catalog and release composition containing every
  component's repository, immutable revision or signed release, artifact
  digests, API/schema/UI versions, dependencies, conflicts, platform state,
  migration order, rollback mate, evidence hashes, and admission decision.
- **BFW-PRD-080:** Every BFW requirement shall have a machine-readable trace
  record with one owner, lifecycle status, blocking dependencies, planned or
  executable verification, evidence references, and admission decision. The
  trace ID set shall exactly match the PRD and implementation verification map.
- **BFW-PRD-081:** The meta repository shall own versioned schemas for plugin
  manifests, permissions and capabilities, compatibility, canonical
  configuration, platform-neutral plans, transaction envelopes, audit events,
  health/degradation, UI contributions, releases, and rollback records.
- **BFW-PRD-082:** Phase 0 shall have an authoritative machine-readable
  dashboard that pins each substrate revision and records required gates,
  passed gates, gaps, evidence, review, admission, and whether Bifrost runtime
  implementation is allowed. Missing evidence shall keep the gate blocked.
- **BFW-PRD-083:** Material architecture choices shall use indexed ADRs with
  explicit status, context, decision, consequences, alternatives, requirement
  links, and supersession. Open choices shall not masquerade as accepted
  compatibility contracts.
- **BFW-PRD-084:** Bifrost shall maintain a formal threat model and trust-boundary
  map covering management compromise, malicious plugins, stale generations,
  supply-chain attacks, secret leakage, rollback, split brain, lockout,
  recovery-console abuse, and fail-open packet paths, with requirement and
  verification links for every threat.
- **BFW-PRD-085:** Cross-component mutation shall use a versioned transaction
  contract defining validate, prepare, apply, verify, commit, and rollback
  phases; typed participants and effects; idempotency and generation rules;
  partial-failure behavior; and last-known-good selection.
- **BFW-PRD-086:** Meta-repository CI shall fail on naming drift, missing or
  duplicate requirement IDs, trace disagreement, product runtime source,
  invalid schemas/manifests, mutable or incomplete admitted pins, dependency
  cycles, undeclared platform state, migration/rollback mismatch, suspected
  secrets, changelog violations, stale generated views, or invalid evidence
  hashes.
- **BFW-PRD-087:** The first product profile shall remain deliberately narrow:
  core, CLI, one web shell, identity boundary, plugin SDK, one initial platform,
  firewall, network, switching, routing, DNS, DHCP, WireGuard, monitoring,
  logging, and backup/recovery. Other catalog components shall remain explicitly deferred
  until a later admitted profile.
- **BFW-PRD-088:** Every component repository shall begin from versioned
  bootstrap and admission templates covering PRD, architecture, implementation
  specification, threat model, compatibility matrix, test plan, evidence
  manifest, release manifest, and independent review.
- **BFW-PRD-089:** Release and recovery design shall define signed artifacts,
  SBOM and provenance, reproducible appliance composition, staged or atomic
  update activation, interruption recovery, local-console rollback,
  configuration migration, and verified last-known-good selection before any
  runtime release is admitted.
- **BFW-PRD-090:** System admission shall use a pinned, isolated test-lab
  topology for Linux, FreeBSD, and Windows; upgrades and recovery; HA and split
  brain; hostile management and plugin paths; and independent packet/state
  completeness oracles. Missing image or environment pins shall block evidence.
- **BFW-PRD-091:** Bifrost shall be both a managed Layer-2 switch system and a
  Layer-3 router/firewall system. Switching shall be a first-class typed domain,
  not an incidental side effect of interface configuration.
- **BFW-PRD-092:** The separately versioned `bfw-switching` component shall own
  bridge domains, VLAN membership and tagging, Layer-2 forwarding, loop-control
  policy, and switching-specific observed state. `bfw-network` shall retain port
  and interface construction, `bfw-routing` Layer-3 routing, and `bfw-firewall`
  filtering and NAT.
- **BFW-PRD-093:** The switching contract shall cover VLAN access, trunk,
  native/PVID and allowed-list behavior; software bridges; learned and static
  FDB entries; STP/RSTP/MSTP; LACP port channels; port isolation; storm control;
  IGMP/MLD snooping; and LLDP observations, with explicit per-platform support.
- **BFW-PRD-094:** Loop risk, contradictory VLAN ownership, tag leakage,
  duplicate bridge membership, uncertain STP state, and unsupported required
  switching behavior shall fail closed without exposing a wider broadcast
  domain or bypassing the last known-good configuration.
- **BFW-PRD-095:** Changes spanning ports, Layer-2 switching, Layer-3 routing,
  firewall/NAT, DHCP, or management reachability shall be validated, ordered,
  applied, observed, verified, and rolled back as one core-coordinated typed
  transaction.
- **BFW-PRD-096:** Platform adapters shall map switching plans to admitted native
  facilities and declare semantic gaps. Linux software bridge/VLAN and
  applicable switchdev/DSA/devlink, FreeBSD bridge/VLAN, Windows Hyper-V
  vSwitch or an admitted equivalent, and vendor ASIC SDKs shall not be treated
  as interchangeable or universally available.
- **BFW-PRD-097:** Switching observed state shall expose authorized, bounded
  views of VLAN membership, FDB learning/aging, STP role and state, LACP member
  state, counters, offload state, health, and desired-versus-observed drift.
- **BFW-PRD-098:** A change to a management VLAN, bridge, switch uplink, native
  VLAN, or port channel that can remove the active management path shall require
  commit-confirmed or an admitted local/OOB recovery path and shall roll back
  before operator lockout when confirmation or verification fails.
- **BFW-PRD-099:** The v0.1 profile shall include `bfw-switching` with a Linux
  software-switching baseline. Hardware offload may be admitted only when its
  platform adapter proves equivalent plan, observation, verification, failure,
  and rollback semantics; absence of offload shall not block the baseline.
- **BFW-PRD-100:** Bifrost shall be one full-featured network operating system
  deployable in `router`, `switch`, or `converged` router-switch roles. The
  roles shall be profiles of one product and configuration model, not separate
  editions, forks, or mutually incompatible management planes.
- **BFW-PRD-101:** The router role shall require admitted port/interface,
  Layer-3 routing, and firewall policy capabilities while permitting
  switching to remain disabled for user traffic. Internal implementation
  bridges shall not silently create a managed switching domain.
- **BFW-PRD-102:** The switch role shall require admitted port/interface and
  Layer-2 switching capabilities and may enable admitted Layer-3 switching for
  SVIs, routed switchports, and inter-VLAN/local-fabric routing. WAN-edge
  routing and NAT shall remain denied by default. A bounded management address
  shall not become a transit forwarding path.
- **BFW-PRD-103:** The converged role shall enable admitted switching, routing,
  and firewall domains under one canonical configuration and shall coordinate
  inter-VLAN routing, routed ports, switched virtual interfaces, policy, DHCP,
  and management reachability through core-owned typed transactions.
- **BFW-PRD-104:** Role selection and transition shall validate component and
  platform admission, configuration compatibility, management reachability,
  forwarding isolation, and last-known-good recovery. A transition shall be a
  candidate/commit-confirmed transaction and shall roll back on incomplete
  verification or lost confirmation.
- **BFW-PRD-105:** "Full-featured" shall mean the governed product capability
  catalog is the intended product surface; it shall not imply that v0.1, every
  platform, or every hardware target supports every capability. Unsupported or
  unadmitted features shall be reported explicitly and fail closed when
  required by a selected configuration or deployment role.
- **BFW-PRD-106:** The switch role shall support Layer-2 access/trunk VLAN,
  bridge, FDB, loop-control, and aggregation behavior plus Layer-3 switched
  virtual interfaces, routed switchports, inter-VLAN routing, and local fabric
  route domains where the selected platform admits them.
- **BFW-PRD-107:** Layer-3 switching shall use `bfw-routing` plans and shall not
  grant WAN-edge routing, NAT, or Layer-4 policy implicitly. Management-only
  addresses and interfaces shall remain excluded from transit forwarding.
- **BFW-PRD-108:** The router role shall support Layer-3 route forwarding and
  Layer-4-aware stateful TCP/UDP policy, NAT, port forwarding, connection-state
  handling, and transport-aware steering through separately owned routing and
  firewall plans.
- **BFW-PRD-109:** `bfw-routing` shall remain the Layer-3 forwarding authority;
  `bfw-firewall` shall remain the Layer-4-aware state, policy, and NAT authority.
  Neither ownership label shall imply application payload inspection, reverse
  proxying, TLS termination, or Layer-7 identity policy.
- **BFW-PRD-110:** Deployment profiles and observed capability reports shall
  state their admitted data-plane layers and effects explicitly. Missing,
  unsupported, or only partially observed required Layer-2, Layer-3, or
  Layer-4-aware behavior shall reject activation and preserve last-known-good.
- **BFW-PRD-111:** `bfw-ids` shall be a clean-room native Go implementation of
  Snort-class IDS/IPS behavior. It shall not embed, invoke, supervise, require,
  or copy the Snort runtime, executable, source tree, or private implementation.
- **BFW-PRD-112:** The engine shall support passive IDS and separately admitted
  inline IPS modes through explicit capture/injection adapters and capture-point
  identities. Enabling prevention shall never be an implicit consequence of
  installing rules or enabling observation.
- **BFW-PRD-113:** Detection shall include bounded IP fragmentation and TCP
  stream reassembly, flow tracking, direction/state semantics, protocol
  normalization/decoding, content and safe regular-expression matching,
  thresholds, suppression, references/classification, and evasion-resistant
  overlap/checksum/truncation policy.
- **BFW-PRD-114:** Bifrost shall own a canonical versioned IDS rule model. A
  clean-room Snort-rule importer shall declare the exact supported dialect,
  keywords, actions, protocol decoders, and option semantics. Unsupported or
  ambiguous rules, PCRE constructs, preprocessors, or actions shall be rejected
  with diagnostics rather than accepted with weaker behavior.
- **BFW-PRD-115:** Packet, flow, stream, decoder, decompression, file-metadata,
  rule, match, alert, and evidence work shall have explicit CPU, memory, byte,
  depth, time, cardinality, and retention bounds. Exhaustion or incomplete
  inspection shall be observable and shall never be reported as complete.
- **BFW-PRD-116:** Rulesets and feeds shall be signed, provenance-bound,
  content-addressed, compatibility-checked, staged, compiled deterministically,
  activated atomically, versioned, auditable, expirable, and rollback-capable.
- **BFW-PRD-117:** Alerts shall use a stable typed schema with rule/revision,
  flow, capture point, timestamps, classification, confidence, action,
  truncation/incompleteness, and bounded evidence references. Payload and PCAP
  retention shall be explicit, access-controlled, redacted, and disabled by
  default where not required.
- **BFW-PRD-118:** IDS detections may propose drop, reject, rate-limit,
  quarantine, or temporary-block effects, but only the core may authorize and
  dispatch a typed `bfw-firewall` transaction. `bfw-ids` shall not mutate native
  firewall, routing, switching, interface, or process state directly.
- **BFW-PRD-119:** Inline IPS shall declare per-zone fail-open/fail-closed policy,
  bypass availability, queue/backlog bounds, overload behavior, watchdogs,
  health, confirmation, and recovery. A mode or failure-policy change shall be
  transactional and shall never silently change enforcement behavior.
- **BFW-PRD-120:** Platform adapters shall declare exact capture, injection,
  timestamp, checksum/offload, VLAN-tag, multi-queue, zero-copy, and packet-loss
  semantics. Linux, FreeBSD, and Windows mechanisms shall not be presumed
  equivalent, and unmeasured loss or normalization gaps shall block admission.
- **BFW-PRD-121:** Admission shall include canonical packet/flow corpora,
  differential rule fixtures, fragmentation/stream/evasion suites, malformed
  packet and rule fuzzing, deterministic alert oracles, restart/upgrade/rollback,
  overload/loss accounting, race tests, and representative performance/resource
  evidence for every supported platform and mode.
- **BFW-PRD-122:** Bifrost shall not claim complete Snort rule, preprocessor,
  decoder, performance, or detection parity. Compatibility claims shall name a
  tested dialect/version and feature matrix, and Snort names/marks shall be used
  only descriptively without implying endorsement.
- **BFW-PRD-123:** Distributed operation shall be an orthogonal fabric scope:
  any admitted router, switch, or converged node may be standalone or a fabric
  member without creating a separate product edition or management authority.
- **BFW-PRD-124:** `bfw-fabric` shall own cluster topology, node placement,
  convergence, and multi-node transaction coordination. It shall not own
  Layer-2 switching, Layer-3 routing, or firewall policy semantics, which remain
  with `bfw-switching`, `bfw-routing`, and `bfw-firewall` on every node.
- **BFW-PRD-125:** Fabric membership shall require cryptographic node identity,
  explicit enrollment/revocation, current liveness/generation, compatible
  release/schema/capability sets, authorized roles, and encrypted authenticated
  control channels. Node reachability alone shall grant no fabric authority.
- **BFW-PRD-126:** Canonical fabric intent shall use quorum/consensus, monotonic
  generations, leader/term identity, fencing, idempotency, durable journals, and
  deterministic reconciliation. Minority, stale, split-brain, or ambiguous
  ownership partitions shall not accept conflicting mutations.
- **BFW-PRD-127:** Distributed Layer-2 switching shall support admitted
  VXLAN/GENEVE-class overlays and EVPN-class MAC/IP distribution, VNI/bridge
  domains, split horizon, designated forwarding, BUM replication, ARP/ND
  suppression, MAC mobility/duplication controls, and bounded learning/aging.
- **BFW-PRD-128:** Distributed Layer-3 routing shall support VRFs, distributed
  anycast gateways, routed VNIs, ECMP, route-target import/export, controlled
  route leaking, next-hop reachability, and graceful convergence through typed
  routing and dynamic-control-plane contracts.
- **BFW-PRD-129:** Distributed firewall policy shall compile one canonical
  generation into deterministic node-local enforcement placements. Ingress,
  egress, transit, workload, and service policy shall preserve identity and
  zone semantics across mobility; stateful flows shall declare symmetry,
  steering, ownership, replication, failover, and stale-state behavior.
- **BFW-PRD-130:** Fabric partition, node loss, control-plane loss, delayed or
  reordered update, stale generation, topology loop, duplicate endpoint, route
  conflict, policy-placement gap, or incomplete observation shall follow an
  explicit safety policy and shall never silently widen connectivity.
- **BFW-PRD-131:** Underlay and overlay plans shall validate encapsulation
  overhead, MTU/PMTU, fragmentation policy, QoS markings, ECN, hashing, entropy,
  loop prevention, multicast/BUM behavior, and hardware/offload semantic gaps
  for every admitted path.
- **BFW-PRD-132:** Fabric changes shall be staged and committed as generation-
  bound multi-node transactions with dependency order, readiness barriers,
  canaries where appropriate, independent per-node and end-to-end oracles,
  bounded convergence deadlines, interruption recovery, and coordinated or
  safely isolated rollback.
- **BFW-PRD-133:** Node-local enforcement shall retain the last verified policy
  during control-plane loss. Any fail-static, fail-isolated, fail-open, or
  fail-closed exception shall be explicit per traffic class, bounded in time,
  visible, audited, and incapable of overriding a stricter local safety floor.
- **BFW-PRD-134:** Fabric observed state shall expose authorized topology,
  membership, terms/generations, overlay peers, MAC/IP and route distribution,
  policy placement, flow-state ownership, loss, convergence, drift, degraded
  isolation, and rollback status without leaking credentials or payloads.
- **BFW-PRD-135:** Admission shall cover at least three nodes, multiple failure
  domains, asymmetric partitions, node/control-plane restart, endpoint mobility,
  duplicate MAC/IP, route and policy churn, ECMP member loss, rolling upgrade,
  rollback, scale/resource boundaries, deterministic packet/state oracles, and
  latency/throughput/convergence distributions on every supported platform.
- **BFW-PRD-136:** Bifrost shall offer a first-party Kubernetes-managed HA scope
  in which a dedicated controller deployment coordinates canonical intent,
  inventory, rollout, observation, and recovery for native managed nodes. It
  shall not create a separate product edition or configuration authority.
- **BFW-PRD-137:** A single dedicated controller may be admitted only as a
  non-HA small-site profile whose loss freezes management. The HA controller
  profile shall use at least three odd-numbered control-plane members across
  separately identified failure domains and quorum-backed durable state.
- **BFW-PRD-138:** Kubernetes, its API server, scheduler, CNI, service network,
  overlay, and storage shall never be required for node-local packet forwarding,
  fast failover, last-known-good enforcement, or local recovery.
- **BFW-PRD-139:** Routers and switches shall run native signed Bifrost services
  and an authenticated management agent. They shall not be required to join the
  Kubernetes cluster as worker nodes or expose a container runtime.
- **BFW-PRD-140:** Controller loss or partition shall deny new mutations while
  managed nodes retain their last verified configuration and continue native
  BFD, routing/EVPN, ECMP, gateway ownership, and firewall-state behavior.
- **BFW-PRD-141:** Controller-to-node operations shall use mutually authenticated,
  authorization-checked, signed, generation-bound typed plans with expiry,
  idempotency, readiness, verification, audit, and deterministic rollback.
- **BFW-PRD-142:** Production controller reachability shall use a separately
  admitted dedicated management VLAN or out-of-band path where available.
  Shared-path use shall require explicit risk acceptance, commit-confirmed
  protection, local recovery, and a tested bootstrap/rebuild procedure.
- **BFW-PRD-143:** Kubernetes integration shall pin and admit exact Kubernetes or
  K3s, container-runtime, CNI, storage, image, chart/manifest, CRD, API, RBAC,
  NetworkPolicy, Pod Security, provenance, upgrade, backup, and rollback contracts.
- **BFW-PRD-144:** Admission shall test controller quorum/member loss, total
  controller loss, API/etcd/CNI/storage failure, asymmetric management partition,
  stale/replayed plans, node restart, autonomous forwarding, controller rebuild,
  rolling upgrade/rollback, secret isolation, and recovery without widening
  connectivity or interrupting an already verified forwarding state.
- **BFW-PRD-145:** The native Go HA engine behind `bfw-ha` shall be named
  **GoKA** and developed clean-room from public protocol specifications and
  independently authored tests. It shall not embed, copy, link, invoke,
  supervise, configure, or require Keepalived source, libraries, binaries, or
  runtime behavior as implementation authority.
- **BFW-PRD-146:** GoKA shall implement admitted VRRPv2/VRRPv3 IPv4/IPv6 virtual
  router election semantics, priorities, advertisement/skew/master-down timers,
  preemption policy, owner behavior, multicast or explicit unicast peers, and
  protocol validation without silently extending authority.
- **BFW-PRD-147:** GoKA shall emit typed generation-bound virtual-address,
  neighbor-announcement, route, firewall-role, and service-role transition plans.
  Only the core and owning network/routing/firewall/platform components may
  authorize, apply, verify, or roll back those effects.
- **BFW-PRD-148:** GoKA health tracking shall use bounded typed checks and
  admitted plugin observations with explicit interval, timeout, rise/fall,
  weight, dependency, freshness, and incomplete-health semantics. Arbitrary
  shell commands, inherited environment, or ambient process access are denied.
- **BFW-PRD-149:** Duplicate ownership, split brain, replay, stale generation,
  peer ambiguity, timer exhaustion, clock anomaly, partial transition, restart,
  and lost observation shall follow explicit fencing/quorum and fail-closed or
  bounded last-known-good policy without silently widening connectivity.
- **BFW-PRD-150:** Any Keepalived configuration importer shall name an exact
  tested dialect and translate only a documented subset into canonical GoKA
  intent. Unsupported directives, scripts, notification hooks, IPVS behavior,
  ambiguous ordering, or incompatible semantics shall be hard errors.
- **BFW-PRD-151:** Linux may use native Go VRRP packet handling and admitted
  netlink effects; FreeBSD may map to separately admitted CARP mechanics; other
  platforms shall publish exact semantic gaps and report unsupported behavior
  rather than weakly emulate ownership or fencing.
- **BFW-PRD-152:** GoKA observed state shall expose authorized instance, role,
  peer, priority, timers, health, generation, transition, duplicate-owner,
  degraded, and rollback facts with bounded cardinality and no credential,
  packet-payload, or reusable authority leakage.
- **BFW-PRD-153:** Admission shall include clean-room provenance/source scans,
  protocol conformance and interoperable-peer matrices, deterministic state-
  machine tests, packet corpus/fuzz/race/endurance tests, partitions/restarts,
  hostile inputs, platform parity, upgrade/rollback, and latency/CPU/memory/
  allocation evidence for every supported mode and platform.
- **BFW-PRD-154:** Bifrost shall have exactly two first-party out-of-the-box HA
  deployment profiles: `goka-native` and `kubernetes-managed`. They shall ship
  as supported Bifrost composition choices rather than third-party add-ons.
- **BFW-PRD-155:** Both HA profiles shall use the same canonical configuration,
  core authorization, CLI, web/API, audit, transaction, compatibility,
  observation, release, backup, and recovery contracts.
- **BFW-PRD-156:** `goka-native` shall require no external orchestrator and shall
  use GoKA/native Bifrost peers for management coordination, election, health,
  fencing, and failover intent.
- **BFW-PRD-157:** `kubernetes-managed` shall ship the Bifrost controller,
  manifests/charts, CRDs, policies, and compatibility metadata out of the box,
  while requiring an admitted Kubernetes/K3s environment as its selected
  controller substrate.
- **BFW-PRD-158:** Exactly one management-coordinator profile may own a given HA
  domain. Kubernetes may coordinate GoKA or other admitted node-local mechanisms
  but shall not become a competing writer or replace native fast failover.
- **BFW-PRD-159:** Selecting or migrating HA profiles shall be an explicit
  generation-bound, commit-confirmed transaction with compatibility preflight,
  authority handoff, continuous forwarding or conservative isolation,
  independent verification, and automatic rollback.
- **BFW-PRD-160:** Capability negotiation shall distinguish packaged,
  configured, controller-available, forwarding-ready, degraded, unsupported,
  and admitted states. Merely shipping either profile shall grant no authority.
- **BFW-PRD-161:** A release claiming out-of-the-box HA support shall package and
  verify both first-party profiles, their schemas and recovery assets, cross-
  profile migration, controller/node failure matrices, and identical policy
  semantics without claiming that v0.1 or an unadmitted platform is HA-ready.
- **BFW-PRD-162:** Bifrost shall provide a comprehensive BGP suite through the
  separately supervised `bfw-frr` component and the typed `bfw-routing`
  contract. `bfw-frr` shall own BGP protocol/session behavior but shall not
  become canonical route, interface, credential, authorization, process,
  release, or platform-mutation authority.
- **BFW-PRD-163:** Every admitted release shall publish a machine-readable BGP
  capability matrix keyed by exact FRR build, platform, transport, peer mode,
  AFI/SAFI, extension, security mechanism, scale bound, interoperability
  result, and admission state. “All BGP” shall mean the complete declared
  matrix, never an unqualified promise about every historical, proprietary,
  experimental, or future extension.
- **BFW-PRD-164:** BGP peer and topology contracts shall cover IPv4 and IPv6
  eBGP and iBGP, full-mesh and route-reflector client/server operation,
  confederations, route-server policy, multihop, numbered and admitted
  unnumbered sessions, dynamic-neighbor/listen ranges, peer groups, VRFs, and
  independently bounded per-peer/per-family activation.
- **BFW-PRD-165:** The minimum multiprotocol matrix shall explicitly address
  IPv4/IPv6 unicast and multicast, IPv4/IPv6 labeled-unicast, VPNv4/VPNv6,
  L2VPN EVPN, IPv4/IPv6 and VPN FlowSpec, route-target constraints, multicast
  VPN, BGP-LS, and SR Policy families. Each family is independently admitted;
  a missing provider/platform mechanism is `unsupported`, not silently
  omitted, translated, or weakened.
- **BFW-PRD-166:** Capability negotiation shall explicitly model four-octet
  ASNs, multiprotocol capability, route refresh and enhanced route refresh,
  graceful and long-lived graceful restart, Add-Path, extended next hop,
  extended messages, multiple labels, BGP Roles/Only-to-Customer, and any
  family-specific capability required by the declared matrix. A capability
  mismatch shall degrade or deny only according to explicit policy.
- **BFW-PRD-167:** BGP import/export policy shall be typed, ordered,
  deterministic, direction- and family-specific, default-deny where required,
  and capable of matching and setting prefixes, next hops, AS paths, origins,
  local preference, MED, weights, tags, route targets, and standard, extended,
  large, and well-known communities without accepting ambiguous text order.
- **BFW-PRD-168:** BGP security shall include explicit peer identity, local and
  remote AS, source/interface/VRF binding, GTSM/TTL policy, max-prefix and
  prefix/attribute limits, TCP MD5 and TCP-AO capability states, keyring-owned
  authentication material, RPKI origin validation, ASPA and BGPsec capability
  states, BGP Roles/OTC leak prevention, bogon/own-prefix/own-AS controls, and
  fail-closed handling of unavailable required validation data.
- **BFW-PRD-169:** BGP convergence shall model BFD, graceful shutdown, graceful
  restart, long-lived graceful restart, End-of-RIB, stale-route handling,
  route dampening, minimum advertisement behavior, Add-Path withdrawal,
  next-hop tracking, ECMP, restart, upgrade, and control-plane loss without
  retaining routes beyond their admitted lifetime or completeness proof.
- **BFW-PRD-170:** BGP selection and export shall be deterministic for a fixed
  input generation and shall preserve all decision inputs and rejection
  reasons needed to reproduce best-path, multipath, route-reflection,
  confederation, route-server, VPN/EVPN, FlowSpec, and leak-prevention results.
- **BFW-PRD-171:** BGP configuration and lifecycle changes shall use staged,
  generation-bound, idempotent transactions with syntax/semantic preflight,
  peer-impact and route-delta preview, dependency order, bounded convergence,
  commit-confirmed for management-risking changes, independent observation,
  interruption recovery, and verified rollback. A timeout is an unknown
  outcome requiring reconciliation, not success.
- **BFW-PRD-172:** BGP observed state shall expose bounded authorized peer,
  capability, AFI/SAFI, Adj-RIB-In/Out, Loc-RIB, accepted/rejected route,
  best-path, policy, RPKI/ASPA/BGPsec, BFD, graceful-restart, convergence,
  generation, and drift facts. BMP and MRT export shall be explicit,
  destination-scoped, bounded, redacted, and never an ambient data-exfiltration
  channel.
- **BFW-PRD-173:** The CLI and web contribution shall provide typed BGP
  configuration, neighbor/family/policy status, received/advertised route
  inspection, capability and validation evidence, route refresh/clear actions,
  preview, confirmation, rollback, and degraded diagnostics through core
  authorization. UI or CLI reachability shall grant no protocol or route
  authority.
- **BFW-PRD-174:** BGP work shall have explicit peer, prefix, path, attribute,
  community, update-rate, message-size, queue, CPU, memory, time, telemetry,
  and retained-history bounds. Admission shall include malformed OPEN/UPDATE/
  NOTIFICATION/ROUTE-REFRESH fuzzing, attribute/error-handling corpora, churn,
  route leaks/hijacks, restart, partition, scale, endurance, and resource-
  exhaustion evidence.
- **BFW-PRD-175:** BGP admission shall pin standards/RFC interpretations and an
  interoperability matrix including at least independent FRR, BIRD, and GoBGP
  peers plus available vendor implementations. Every unsupported, partial,
  experimental, vendor-specific, or semantic-gap entry shall be visible; no
  release may claim universal BGP support from configuration parsing or a
  single successful session.
- **BFW-PRD-176:** Bifrost shall publish a comprehensive routing-protocol
  matrix owned by `bfw-routing`. `bfw-frr` may provide protocols implemented by
  the exact admitted FRR build; a protocol absent from that provider requires
  a separately admitted adapter or an explicit `unsupported` state rather than
  a weak emulation or hidden omission.
- **BFW-PRD-177:** OSPF contracts shall cover OSPFv2 and OSPFv3, IPv4/IPv6
  address families, areas and interface/network types, DR/BDR election,
  stub/totally-stubby/NSSA behavior, virtual links where admitted, ABR/ASBR,
  summarization, external routes, authentication, graceful restart, opaque/
  extended LSAs, traffic-engineering and segment-routing capability states,
  and exact LSA/flooding/SPF limits.
- **BFW-PRD-178:** IS-IS contracts shall cover Level 1, Level 2, and L1/L2,
  point-to-point and broadcast adjacencies, DIS election, areas/NET/system ID,
  wide metrics, multi-topology IPv4/IPv6, authentication, overload/attached
  bits, graceful restart, route leaking, TE, SR-MPLS/SRv6 capability states,
  and bounded LSP/TLV/flooding/SPF behavior.
- **BFW-PRD-179:** Distance-vector, mesh, and legacy profiles shall explicitly
  cover RIPv1, RIPv2, RIPng, Babel, EIGRP, and NHRP capability states. RIPv1,
  alpha provider features, unauthenticated modes, and vendor-specific behavior
  are disabled by default and require isolated compatibility admission; parser
  presence shall not imply production support.
- **BFW-PRD-180:** Multicast-routing contracts shall cover IGMPv2/v3, MLDv1/v2,
  PIM-SM/SSM/DM for IPv4/IPv6 where implemented, RP/BSR and static-RP policy,
  MSDP, source/group policy, RPF, joins/prunes/registers, assert/DR state,
  anycast-RP capability, boundary/scoping, and bounded multicast-route and
  replication state without collapsing Layer-2 snooping ownership.
- **BFW-PRD-181:** Label and path-control profiles shall explicitly model LDP,
  targeted LDP, MPLS label allocation/retention, BGP labeled routes, SR-MPLS,
  SRv6, RSVP-TE, PCEP, and traffic-engineering capability states. Only rows
  backed by an admitted provider and platform forwarding contract may install
  labels, SIDs, tunnels, or programmed paths.
- **BFW-PRD-182:** BFD shall be one shared, typed liveness service for admitted
  routing, HA, and fabric consumers with asynchronous and demand capability
  states, single/multihop and echo profiles, explicit timers/multipliers,
  authentication, discriminator/generation identity, resource bounds, and
  dampened consumer reactions. No protocol may create an untracked competing
  BFD session for the same ownership key.
- **BFW-PRD-183:** Redistribution among connected, static, BGP, OSPF, IS-IS,
  RIP/RIPng, Babel, EIGRP, multicast, label, and provider-specific domains shall
  be explicit, directional, tagged, metric-mapped, loop-prevented, bounded, and
  previewable. No protocol shall redistribute every learned route by default or
  erase source/provenance needed to prevent feedback.
- **BFW-PRD-184:** Every routing adjacency shall bind protocol, peer/router
  identity, interface/VRF, address family, local identity, authentication
  reference, expected capabilities, timers, limits, generation, and policy.
  Protocol authentication material remains in `agent-keyring`; missing current
  trust or validation state follows explicit fail-closed/last-known-good policy.
- **BFW-PRD-185:** Cross-protocol convergence shall model adjacency changes,
  election/SPF/distance-vector/path-vector updates, recursive next hops,
  redistribution, route preference/administrative distance, ECMP, BFD,
  graceful restart, stale state, FIB programming, rollback, and control-plane
  loss with deterministic event and completeness boundaries.
- **BFW-PRD-186:** CLI, web, API, audit, and observation surfaces shall expose
  typed protocol-specific configuration, adjacency/database/RIB state,
  decisions, rejects, timers, authentication/validation status, convergence,
  redistribution provenance, and drift through bounded pages and actions. Raw
  provider CLI/configuration remains diagnostic input, not authority.
- **BFW-PRD-187:** Routing-protocol admission shall include exact provider and
  platform versions, standards interpretations, independent peers, malformed
  packet/TLV/LSA/LSP/update fuzzing, topology/partition/restart/upgrade cases,
  redistribution-loop and route-leak tests, convergence, scale, endurance,
  CPU/memory/queue bounds, native-route state, and end-to-end packet oracles.
- **BFW-PRD-188:** Deprecated, experimental, alpha, proprietary, or unavailable
  routing protocols and extensions shall remain named matrix rows with exact
  denial or gap reasons. Bifrost shall not claim support for IGRP, OLSR/OLSRv2,
  BATMAN, RPL, vendor fabrics, or a future protocol unless a separate provider,
  ownership, security, failure, interop, and admission contract proves it.
- **BFW-PRD-189:** A release claiming comprehensive routing support shall prove
  every advertised protocol row and every enabled redistribution pair under
  the same pinned component composition, recovery assets, and cross-protocol
  failure matrix. Unadvertised or unsupported rows cannot be inferred from FRR
  branding or another protocol's success.
- **BFW-PRD-190:** Bifrost shall publish a comprehensive switching-protocol and
  mechanism matrix owned by `bfw-switching`, keyed by standard/dialect,
  provider/platform/hardware path, deployment role, topology, limits,
  interoperability evidence, and admission state. Switching protocol support
  is not inferred from a Linux bridge, ASIC name, or vendor-compatible CLI.
- **BFW-PRD-191:** VLAN and provider-bridging profiles shall cover 802.1Q access,
  trunk, native/PVID, priority-tagged, allowed-VLAN and VLAN translation
  semantics; 802.1ad/Q-in-Q; MVRP and legacy GVRP capability states; and VTP or
  other vendor propagation only as isolated explicit compatibility profiles.
- **BFW-PRD-192:** Loop-prevention profiles shall cover STP, RSTP, and MSTP,
  bridge/region identity, timer/root/path-cost/port-role/state semantics,
  topology changes, BPDU handling, edge/PortFast, BPDU/root/loop guards, and
  PVST+/Rapid-PVST+ only as explicit vendor interoperability profiles.
- **BFW-PRD-193:** Link-aggregation profiles shall cover static LAG and LACP,
  actor/partner/system/key/port state, active/passive mode, timers, selection,
  min-links, hashing, member churn, and fallback. MLAG/MC-LAG, ICCP, vPC/VSS,
  chassis stacking, and vendor multi-chassis mechanisms require separately
  matrixed peer/state/fencing/split-brain contracts.
- **BFW-PRD-194:** Discovery and topology profiles shall cover LLDP and LLDP-MED
  with bounded typed TLVs, age/expiry, identity, management-address filtering,
  and authorization; CDP, EDP, FDP, NDP, and other vendor discovery protocols
  are explicit compatibility rows and never trusted configuration authority.
- **BFW-PRD-195:** Layer-2 multicast profiles shall cover IGMP and MLD snooping,
  querier/proxy capability states, router-port discovery, fast leave, unknown-
  multicast policy, MVR, group/source limits, aging, and control/data-plane
  completeness while coordinating rather than duplicating Layer-3 multicast
  routing.
- **BFW-PRD-196:** Port-access and link-protection profiles shall cover 802.1X/
  EAPOL authenticator behavior, MAC Authentication Bypass capability, dynamic
  VLAN/ACL inputs, MACsec/802.1AE and MKA capability, DHCP snooping, Dynamic ARP
  Inspection, IP Source Guard, RA Guard, and storm/loop protection through
  typed identity, keyring, DHCP, firewall, and switching dependencies.
- **BFW-PRD-197:** Overlay switching profiles shall cover VXLAN, GENEVE, and
  explicitly admitted NVGRE compatibility; VTEP, VNI/bridge-domain, split-
  horizon, BUM, ARP/ND suppression, endpoint mobility/duplication, and MTU
  semantics; and EVPN control only through the routing/fabric BGP contract.
- **BFW-PRD-198:** Advanced resiliency/fabric rows shall explicitly address
  SPB/802.1aq, TRILL, G.8032 ERPS, REP, FabricPath, Shortest Path Bridging,
  proprietary ring/stack/fabric systems, and provider deprecation state. No
  unsupported mechanism shall be approximated by STP or MLAG while retaining
  its name.
- **BFW-PRD-199:** Data-center bridging, QoS, and TSN rows shall explicitly
  address 802.1p priority, PFC/802.1Qbb, ETS/DCBX/802.1Qaz, congestion
  notification, 802.1AS/gPTP, Qav/Qbv/Qbu/Qci/Qcc capability states, timing,
  queue/class/resource bounds, and the separate `bfw-qos` authority boundary.
- **BFW-PRD-200:** Ethernet OAM rows shall cover 802.3ah link OAM, 802.1ag CFM,
  ITU-T Y.1731 capability, maintenance domains/associations/endpoints,
  continuity/loopback/linktrace/loss/delay observations, rate limits, and
  strict separation between diagnostics and mutation authority.
- **BFW-PRD-201:** Switching protocol changes shall use deterministic candidate
  topology validation, protocol/provider preflight, management-path analysis,
  staged ordering, bounded convergence, independent BPDU/LACP/LLDP/OAM/native-
  state and packet observation, commit-confirmed where lockout or loops are
  possible, interruption recovery, and verified rollback.
- **BFW-PRD-202:** Switching observed state and UI/CLI shall expose bounded
  bridge/VLAN, port role/state, protocol peer, timer, LAG/member, discovery,
  multicast, access-security, overlay, OAM, offload, convergence, loss, drift,
  and rollback facts without trusting peer advertisements or hardware self-
  report as complete evidence.
- **BFW-PRD-203:** Switching admission shall include standards/dialect fixtures,
  Linux software and admitted hardware paths, independent bridge/vendor peers,
  malformed BPDU/LACPDU/LLDP/EAPOL/OAM fuzzing, loops/storms/partitions/member
  churn, cross-VLAN/tenant leakage, management rollback, scale/endurance/
  resource evidence, and a claim matrix that leaves every unsupported,
  partial, proprietary, or deprecated row visible.
- **BFW-PRD-204:** Bifrost shall support persistent sticky endpoint bindings on
  ports in switch, router, and converged appliance roles. This is endpoint
  identity enforcement, not `bfw-multiwan` sticky-flow selection, and each
  role shall use its owning Layer-2 or Layer-3 mechanism rather than pretending
  that a bridge FDB exists on a routed port.
- **BFW-PRD-205:** A switched sticky binding shall bind an admitted source MAC
  to an exact physical or logical port generation, bridge domain, VLAN/PVID,
  and optional authenticated endpoint identity. Learning shall use an explicit
  bounded enrollment policy, persist only after admission, enforce per-port and
  per-VLAN limits, coexist deterministically with static FDB entries, and deny
  ambiguous LAG, overlay, or hardware-offload semantics.
- **BFW-PRD-206:** A routed sticky binding shall bind an admitted endpoint to an
  exact interface generation, VRF, encapsulation/VLAN, address family, MAC when
  present, and IP address or prefix using bounded ARP, NDP, DHCP, or configured
  evidence. `bfw-network`, `bfw-routing`, and `bfw-firewall` shall coordinate
  neighbor and source enforcement without turning the binding into route,
  credential, or general firewall authority.
- **BFW-PRD-207:** Sticky-binding violations, including unknown endpoints,
  excess cardinality, MAC/IP movement, duplicate identity, stale interface
  generation, spoofed neighbor state, or provider disagreement, shall default
  to drop and alarm. Explicit profiles may restrict, quarantine, or disable a
  port, but shall never silently permit, relearn, or overwrite the admitted
  binding; recovery requires an authorized audited action.
- **BFW-PRD-208:** Sticky enrollment, activation, clearing, replacement,
  migration, expiration, and rollback shall be typed, idempotent,
  generation-bound transactions. UI/CLI and audit shall distinguish learned,
  pending, admitted, active, violating, quarantined, stale, and unsupported
  states, and reboot, upgrade, failover, interface recreation, LAG membership
  change, and last-known-good recovery shall preserve or conservatively reject
  bindings without widening access.
- **BFW-PRD-209:** Alpine Linux shall be the canonical base distribution for
  Bifrost's first-party Linux appliance and bootable installation ISO. The
  initial design baseline is the supported Alpine 3.24 stable branch; every
  Bifrost release shall pin an exact Alpine patch release, repository snapshot,
  package set, kernel, firmware, architecture, and image digest. Alpine edge or
  an unpinned moving repository shall never be a release input.
- **BFW-PRD-210:** The separately versioned `bfw-installer` component shall
  build the Bifrost Alpine installation ISO and installed appliance image from
  a declarative, content-addressed release composition. ISO, boot artifacts,
  packages, configuration defaults, SBOM, provenance, and signatures shall be
  reproducible and independently verifiable; the installer shall have no
  packet-policy or post-install configuration authority.
- **BFW-PRD-211:** The initial Linux ISO shall support x86-64 UEFI and legacy
  BIOS installation, local-console recovery, and a complete offline install.
  It shall identify hardware and target disks before mutation, require an
  explicit destructive confirmation naming the exact target, never select a
  disk by unstable enumeration alone, and preserve no installation secrets in
  media, logs, command lines, or reusable answer files.
- **BFW-PRD-212:** The installed Alpine appliance shall use a minimal declared
  package and service set, a pinned boot chain and init contract, read-only or
  integrity-verified system content where supported, separate durable Bifrost
  configuration/evidence state, least-privilege service identities, and
  fail-closed startup. Ad-hoc package installation or repository drift is not
  part of the supported appliance contract and shall be detected as release
  drift rather than normalized as healthy state.
- **BFW-PRD-213:** Alpine appliance updates shall follow the signed staged or
  A/B release, bounded boot-confirmation, configuration migration,
  last-known-good, and local recovery contracts. A Bifrost release shall not be
  built from an unsupported Alpine branch, and loss of upstream security
  support shall trigger a blocked release or an admitted base-version
  migration rather than silent continued distribution.
- **BFW-PRD-214:** Alpine ISO and installed-image admission shall cover
  reproducible rebuilds, signature/SBOM/provenance verification, UEFI and BIOS
  boot, offline installation, exact-disk confirmation, interruption at every
  destructive stage, power loss, corrupt media/package databases, unsupported
  hardware, clean install, upgrade, migration, rollback, recovery-console use,
  resource bounds, and independent post-boot packet/state completeness on each
  admitted architecture and hardware profile.
- **BFW-PRD-215:** Bifrost release channels shall be `development`, `alpha`,
  `beta`, and `stable`, with separate delegated signing scope, explicit
  audience and support claims, and no automatic promotion. Alpha exists to
  produce a usable decision build before final interfaces, architecture,
  feature breadth, or optimization choices are frozen.
- **BFW-PRD-216:** The first alpha shall be a narrow Linux-only, single-node,
  non-production vertical slice: Alpine Linux x86-64 installation ISO; one
  pinned VM/hardware profile; `rpc-plugin-system` v2; Linux software
  nftables/netlink/bridge data plane; install, boot, persistence, diagnostics,
  reset and local recovery; basic router interfaces/static routes/firewall/NAT/
  DHCP/DNS; basic switched bridge/access/trunk VLAN/FDB/loop protection; and a
  minimal CLI/web path. HA, fabric, hardware offload, dynamic routing breadth,
  broad switching protocols, secondary platforms, and production support are
  explicitly outside the first alpha.
- **BFW-PRD-217:** Alpha source repositories, component implementation, unit
  tests, offline simulation, and isolated namespace/VM integration may begin,
  after normal workflow activation, before BFW-PHASE-0. Host-network mutation,
  installer disk writes, or alpha
  artifact distribution shall remain denied until BFW-ALPHA-0 has passed its
  pinned dependency, destructive-safety, authority-boundary, recovery,
  observation, and review gates.
- **BFW-PRD-218:** The alpha shall pin a v2 `rpc-plugin-system` build and exact
  Linux-compatible `agent-keyring`, `agent-filesystem`, and `agent-exec`
  revisions for only the capabilities it uses. Alpha dependencies may be
  incomplete outside that declared Linux slice, but unknown generation,
  unauthenticated peers, unbounded transport/work, unsafe teardown, reusable
  secret export, uncontained paths/processes, or ambiguous side effects shall
  block use rather than become accepted alpha debt.
- **BFW-PRD-219:** Alpha may be incomplete, visually rough, slow, disposable,
  and contract-unstable, but it shall not erase an unintended disk, expose an
  unintended packet path, leak reusable credentials, corrupt canonical
  configuration silently, accept stale authority, or report unknown runtime
  state as success. These minimum safety properties require focused negative
  tests and recovery evidence before anyone uses the alpha for decisions.
- **BFW-PRD-220:** Alpha shall maximize decision evidence: typed event and
  diagnostic capture, bounded packet/native-state observations, install and
  recovery timings, resource measurements, operator task friction, explicit
  known limitations, provisional contract markers, and a decision log linking
  observed use to retained, changed, or rejected product choices. Telemetry
  shall not contain secrets or silently become production surveillance.
- **BFW-PRD-221:** Alpha evidence shall not be laundered into beta admission.
  Beta requires the full BFW-PHASE-0 cross-platform dependency gate, admitted
  beta-scope components and immutable release composition, B+ or better overall
  grade with A-level critical boundaries, clean install/upgrade/rollback/
  recovery and independent packet/state evidence, no open P0/P1 correctness or
  security defects, published limitations, and fresh independent review.
- **BFW-PRD-222:** Every BFW-PHASE-0 dependency—`rpc-plugin-system`,
  `agent-keyring`, `agent-filesystem`, and `agent-exec`—shall independently
  earn an A or A+ grade with fresh evidence and independent admission before
  Bifrost starts runtime implementation outside the exact BFW-PRD-216 learning-
  alpha scope. Grades shall not be averaged, inherited, self-asserted, or
  substituted by an end-to-end alpha demo. Requirements, architecture,
  decomposition, and review may continue; additional product implementation,
  protocol breadth, secondary platforms, and beta/stable work remain blocked.
- **BFW-PRD-223:** FreeBSD shall be the canonical base distribution for
  Bifrost's first-party BSD appliance and bootable installation ISO. The
  initial BSD profile shall target generic x86-64 systems rather than one
  vendor appliance; every release shall pin an exact supported FreeBSD
  release and source revision, package repository snapshot, package set,
  kernel, modules, firmware, boot artifacts, architecture, and image digest.
- **BFW-PRD-224:** `bfw-installer` shall build the FreeBSD installation ISO and
  installed appliance image from a declarative content-addressed composition
  using supported FreeBSD source-build and NanoBSD-style appliance-image
  mechanisms. Independent builds, signatures, SBOM, provenance, and input and
  output digests are mandatory; the installer gains no packet-policy or
  post-install configuration authority.
- **BFW-PRD-225:** The initial BSD ISO shall support an explicitly bounded
  generic x86-64 UEFI and legacy-BIOS hardware profile, complete offline
  installation, stable target-disk identity, exact destructive confirmation,
  first-boot verification, and local-console recovery. Generic means the
  published compatibility matrix, not every x86-64 machine. Hardware-specific
  appliance images are deferred until a separately approved product profile
  names exact hardware, firmware, lifecycle, and support obligations.
- **BFW-PRD-226:** The installed FreeBSD appliance shall be reduced only by a
  declarative `src.conf`, kernel configuration, package manifest, and signed
  private package repository. It shall retain every admitted firewall,
  routing, switching, HA, IPsec, audit, cryptographic, signature-verification,
  console/SSH recovery, filesystem-repair, observability, firmware, and driver
  dependency. Manual post-install deletion is unsupported release drift.
- **BFW-PRD-227:** The initial FreeBSD appliance shall use replaceable
  read-only or integrity-verified system content, two independently verifiable
  code/root slots or a separately admitted equivalent, and separate durable
  configuration, audit/evidence, and recovery state. Signed update, bounded
  boot confirmation, migration, rollback, and recovery shall reuse the common
  Bifrost release transaction rather than FreeBSD-native in-place mutation.
- **BFW-PRD-228:** FreeBSD ISO admission shall independently cover reproducible
  builds, signatures/SBOM/provenance, UEFI and BIOS boot, offline installation,
  wrong-disk and interruption safety, package and base-system drift, A/B
  upgrade and rollback, recovery, resource bounds, and native PF, routing,
  bridge/VLAN, CARP/pfsync, FRR, and packet/state-oracle behavior across every
  supported hardware row. Linux evidence shall not admit FreeBSD or imply
  cross-platform parity.

## Initial requirements

- **BFW-PRD-001:** Bifrost shall compile one canonical policy model into
  deterministic, platform-native transactions and verify the applied result.
- **BFW-PRD-002:** Configuration changes shall be schema-validated, versioned,
  audited, and recoverable through rollback.
- **BFW-PRD-003:** Failed validation, partial configuration, and uncertain
  runtime state shall fail closed without silently discarding the last
  known-good configuration.
- **BFW-PRD-004:** The management plane shall support explicit network exposure
  controls and a local recovery path.
- **BFW-PRD-005:** Routing, interface, NAT, firewall, DHCP, DNS, and VPN
  integrations shall have explicit ownership boundaries and health evidence.
- **BFW-PRD-006:** Upgrades shall be signed, preflighted, transactional where
  practical, and recoverable after interruption.
- **BFW-PRD-007:** Secrets shall be stored separately from ordinary
  configuration and excluded from logs, exports, and source control.
- **BFW-PRD-008:** Supported operating system, release, kernel/runtime,
  architecture, and appliance-image targets shall be pinned before
  implementation admission.
- **BFW-PRD-009:** Bifrost shall support independently versioned, separately
  supervised plugins without allowing them to redefine core authorization,
  configuration authority, lifecycle identity, or audit rules.
- **BFW-PRD-010:** Plugin packages, manifests, migrations, and declared
  permissions shall be signed, compatibility-checked, and admitted before
  activation.
- **BFW-PRD-011:** Plugin APIs shall be stable, version-negotiated, additive by
  default, and fail closed on unsupported required behavior.
- **BFW-PRD-012:** Plugin failure, restart, removal, or upgrade shall not erase
  the last known-good network policy or create an unintended open path.
- **BFW-PRD-013:** Beta, stable, and production-capable Bifrost runtime releases
  shall not begin admission until the required cross-platform
  `rpc-plugin-system` lifecycle substrate has passed its compatibility,
  security, failure, and platform gates. A separately bounded Linux-only
  learning alpha may begin source implementation and, after BFW-ALPHA-0 passes,
  designated non-production execution without satisfying the broader
  cross-platform BFW-PHASE-0 gate.
- **BFW-PRD-014:** `agent-keyring` shall be Bifrost's credential authority.
  Bifrost configuration, databases, logs, exports, support bundles, web UI,
  and plugins shall not retain reusable secret payloads.
- **BFW-PRD-015:** Core action admission shall precede credential access.
  Credential possession, keyring reachability, process identity, or plugin
  capability shall not independently authorize a Bifrost action.
- **BFW-PRD-016:** Credential access shall use short-lived leases or
  non-exporting opaque references bound to the caller, plugin and provider
  generations, admitted action, credential usage, access mode, target,
  audience, policy version, credential generation, keyring authority
  generation, and expiry. Raw export shall be denied by default.
- **BFW-PRD-017:** Credential revocation, rotation, keyring restore, authority
  restart, policy change, or relevant runtime-generation change shall make
  stale leases and references unusable and auditable.
- **BFW-PRD-018:** Bifrost beta and stable credential integration shall not
  begin until `agent-keyring` has passed cross-platform transport,
  peer-identity, encrypted-storage/unlock, lease, revocation, recovery, SDK,
  and redaction admission gates for the supported Bifrost platforms. The Linux
  learning alpha may use only the immutable keyring revision and capabilities
  separately admitted by BFW-ALPHA-0.
- **BFW-PRD-019:** Host-file operations outside Bifrost's private canonical
  state shall use `agent-filesystem` with a core-admitted scope containing
  explicit roots, operations, bounds, link/special-file policy, mutation
  preconditions, recovery behavior, generation, expiry, and audit correlation.
- **BFW-PRD-020:** Bifrost shall treat paths and filesystem results as operands,
  not authority. Filesystem operations shall not expose keyring payloads,
  provider-private state, or reusable handles, and destructive operations shall
  require an explicit destructive admission and recoverable behavior where the
  platform contract supports it.
- **BFW-PRD-021:** Local process execution shall use `agent-exec` only after
  core admission of the executable identity, argv or separately allowed shell,
  cwd, environment, stdio, timeout, process-tree, resource, network,
  filesystem-containment, side-effect, retry, and audit policies.
- **BFW-PRD-022:** Bifrost process execution shall deny shells, ambient PATH and
  environment, inherited credentials, unrestricted network access, privilege
  fallback, and reusable raw process/session handles by default. Native
  platform APIs shall remain preferred for firewall and routing mutation.
- **BFW-PRD-023:** A workflow combining credentials, files, and processes shall
  require one sealed core-admitted plan and separate, matching, short-lived
  authority for every keyring, filesystem, and execution use. Outputs or
  handles from one provider shall not expand another provider's authority.
- **BFW-PRD-024:** Bifrost beta and stable runtime integration shall not begin
  until `agent-filesystem` and `agent-exec` have passed their
  supported-platform transport, identity, path/process safety,
  sandbox/containment, recovery, lifecycle, SDK, audit/redaction, and
  independent admission gates. The Linux learning alpha may use only the
  immutable provider revisions and capabilities separately admitted by
  BFW-ALPHA-0.
- **BFW-PRD-025:** The web UI shall run as an independent unprivileged service
  and shall use the same versioned, authenticated core API as the `bfw` CLI. It
  shall not edit configuration files, invoke platform plugins directly, run
  firewall commands, hold platform/root privilege, or become configuration
  authority.
- **BFW-PRD-026:** A plugin UI contribution shall be part of its signed package
  and shall declare its plugin/version identity, UI/API compatibility,
  routes/navigation, schemas/views, typed action bindings, required
  permissions, localization metadata, and content-addressed asset digests.
- **BFW-PRD-027:** The core shall verify signature, provenance, compatibility,
  permissions, schemas, migrations, and asset digests before publishing a
  sanitized, authorization-filtered UI catalog. `bfw-web` shall never discover
  pages directly from a running plugin process.
- **BFW-PRD-028:** Common plugin pages shall use a versioned declarative UI
  contract and shared BFW components for forms, tables, status panels,
  validation, confirmation, accessibility, and error presentation.
- **BFW-PRD-029:** Every plugin UI action shall bind to a typed core API action
  and pass normal identity, authorization, validation, confirmation, audit,
  idempotency, generation, and rollback admission. Browser reachability or UI
  visibility shall not grant action authority.
- **BFW-PRD-030:** A custom frontend bundle, when declarative UI is insufficient,
  shall be signed, content-addressed, permission-declared, and isolated in a
  separate-origin sandbox with strict CSP and a narrow capability-based message
  protocol. It shall have no direct access to BFW credentials, cookies,
  canonical state, host files, plugin sockets, privileged APIs, the trusted DOM,
  or arbitrary network requests.
- **BFW-PRD-031:** Plugin backend, UI manifest, schemas, migrations, and assets
  shall be compatibility-checked and activated, upgraded, or rolled back as one
  versioned release. A partially activated UI/backend pair shall fail closed.
- **BFW-PRD-032:** Disabled, removed, incompatible, or untrusted plugins shall
  contribute no active UI routes. An unhealthy admitted plugin may expose only
  a clearly degraded, read-only diagnostic surface while mutating actions are
  denied.
- **BFW-PRD-033:** The `bfw` CLI shall provide a local recovery path through the
  same core contracts when the web service or plugin UI is unavailable. The CLI
  shall be a client, not a direct firewall-state editor.
- **BFW-PRD-034:** Web-service, UI-renderer, or plugin-UI failure, restart, or
  upgrade shall not interrupt packet processing, erase last-known-good policy,
  or weaken core admission and audit behavior.

## Bootstrap acceptance criteria

- Private `danny/Bifrost` repository exists on Forgejo with default branch
  `main`.
- README states the cross-platform Go/native-engine architecture boundary,
  plugin model, governance-only meta-repository status, and absence of product
  runtime code.
- Canonical PRD, architecture, and implementation specification exist under
  `documents/` in the required order.
- Meta-repository role and component map are explicit without a product Go
  module or executable firewall code.

## Non-goals for this slice

- packet-filter implementation
- web UI or API implementation
- installer or bootable appliance image
- production deployment
- feature-parity claim against OPNsense
