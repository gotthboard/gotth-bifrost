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
- **BFW-PRD-066:** Initial implementation priority after Phase 0 shall be
  firewall, network/interfaces, routing, DNS, DHCP, WireGuard, ACME/DDNS,
  reverse proxy, monitoring/logging/backup, HA/multi-WAN, then IDS/IPS and
  dynamic routing. The sequence may change only through an explicit
  meta-repository planning and dependency decision.
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
- **BFW-PRD-013:** Bifrost runtime implementation shall not begin until the
  required cross-platform `rpc-plugin-system` lifecycle substrate has passed
  its compatibility, security, failure, and platform admission gates.
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
- **BFW-PRD-018:** Bifrost runtime credential integration shall not begin until
  `agent-keyring` has passed cross-platform transport, peer-identity,
  encrypted-storage/unlock, lease, revocation, recovery, SDK, and redaction
  admission gates for the supported Bifrost platforms.
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
- **BFW-PRD-024:** Bifrost runtime integration shall not begin until
  `agent-filesystem` and `agent-exec` have passed their supported-platform
  transport, identity, path/process safety, sandbox/containment, recovery,
  lifecycle, SDK, audit/redaction, and independent admission gates.
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
