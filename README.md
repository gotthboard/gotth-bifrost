# GOTTH Bifrost (BFW)

**Bifrost**, with the firewall shorthand **BFW**, is a planned open-source,
cross-platform network firewall, managed-switch, and routing platform written in Go, in the same
broad product category as OPNsense.

Bifrost is now a **GOTTH product**, developed in `gotthboard/gotth-bifrost`.
The private [Forgejo repository](https://git.dannyhunn.com/gotthboard/gotth-bifrost)
is canonical; [GitHub](https://github.com/gotthboard/gotth-bifrost) is its public
one-way mirror and [bug tracker](https://github.com/gotthboard/gotth-bifrost/issues).
Report vulnerabilities privately using [SECURITY.md](SECURITY.md).

**This repository still contains design and governance, not a usable appliance.**
The [GOTTH adoption contract](documents/GOTTH-INTEGRATION.md) defines how shared
GOTTH code will be used to build Bifrost. No runtime integration is claimed.

The goal is a security-first appliance that combines deterministic packet and
policy control with a clear API, auditable configuration, safe upgrades, and a
web administration plane. This is the **Bifrost meta repository**: it owns the
cross-repository product definition, component map, integration contracts,
compatibility matrix, release composition, and system-level evidence. It is
not a product runtime module, firewall, router, or security boundary.

Bifrost is one full-featured network operating system with three supported
deployment roles: **router**, **switch**, and **converged router-switch**. The
switch role provides Layer-2 switching and Layer-3 switching through SVIs,
routed switchports, and inter-VLAN/local-fabric routing. The router role
provides Layer-3 routing plus Layer-4-aware stateful policy, NAT, port
forwarding, and transport-aware steering. A router deployment does not require
a user-traffic Layer-2 switching domain; a switch management address does not
become a transit path; a converged deployment coordinates all domains through the same
candidate, authorization, transaction, audit, and recovery model. These are
profiles of one product, not separate editions or forks.

## Naming

- Full product name: **Bifrost**
- Canonical firewall shorthand: **BFW** (Bifrost Firewall)
- Lowercase command, package, configuration, and protocol namespace: `bfw`
- GOTTH family/display name: **GOTTH Bifrost**
- Repository name: `gotth-bifrost` (formerly `danny/Bifrost`)

The shorthand `BFW` identifies Bifrost's firewall product and is not the formal
full name, a separate component, or an edition. Future public interfaces must
use `bfw` consistently and must not
introduce competing `bfr`, `bif`, or ambiguous `bifrost` shorthand namespaces.
Repository branding does not rename `bfw`, `bfwd`, `bfw-web`, `BFW-PRD-*`,
schema identifiers, or the canonical workflow project key `Bifrost`.

## Build on GOTTH

Prefer the existing GOTTH implementations for identity (`gotth-oidc`, optional
`gotth-authentik` and `gotth-scim`), jobs, portability, webhooks, release and
infrastructure tooling. Evaluate `gotth-extensions` for its shared package and
capability contracts, not as a replacement for `rpc-plugin-system` supervision.
Use Go/templ, HTMX and Tailwind for the independent management UI, following
GOTTH conventions; `gotth-sdk` is a planned shared surface, not an available UI
library today. Optional Stack integration is a client of Bifrost's core API.

The adoption matrix records existing code versus placeholders, proposed
consumers, version/admission work and failure boundaries. Bifrost retains its
network semantics, local recovery, credential custody and native data plane.
No shared web service, PostgreSQL server, identity provider or GOTTH Stack
instance becomes a prerequisite for established packet forwarding.

## Current governance status

- [Workflow status](docs/WORKFLOW.md) — generated from canonical
  `workflow.toml`
- [Global coverage](workflow/COVERAGE.md) — evidence, gaps, checked plans, and
  next increments
- [Phase 0](docs/PHASE0.md) — independent A/A+ substrate admission
- [Learning alpha](docs/ALPHA.md) — bounded Linux-alpha effect gates
- [Requirement trace](docs/REQUIREMENTS.md) — requirement ownership and
  admission state

These are governance views, not runtime-support claims. Generated files must be
regenerated from their canonical TOML sources and must not be edited by hand.

## Intended capabilities

- stateful firewall policy through native platform engines
- Layer-2 switching with VLAN access/trunk ports, bridges, STP, LACP, FDB,
  isolation, storm control, and multicast snooping
- Layer-3 routing, bonds, and physical/logical interface management
- NAT, port forwarding, and policy-based routing
- DHCP, DNS forwarding, and network-service supervision
- site-to-site and remote-access VPN integration
- high-availability state and configuration synchronization
- versioned configuration with validation, audit history, and rollback
- metrics, structured logs, packet captures, and diagnostics
- authenticated web UI and API
- signed plugin/package repository with compatibility and permission admission
- signed, transactional upgrades with recovery support
- native Go intrusion detection and separately admitted prevention with a
  Snort-class rule/flow operating model and bounded compatibility imports
- distributed switching, routing, and firewall fabrics with node-local
  enforcement, convergence evidence, and partition-safe recovery
- first-party Kubernetes/K3s-hosted controller HA for centralized management,
  without making node forwarding or fast failover depend on Kubernetes

The catalog is the full-featured product direction, not a claim that every
platform or the first release implements every item. Profiles expose only
admitted capabilities supported by the selected OS, drivers, and hardware.

## Learning-alpha path

The first usable build is a non-production learning alpha, not a miniature
promise of the final cross-platform product. It is single-node Alpine Linux
x86-64 on one pinned VM/hardware profile, uses the Linux software data plane
and `rpc-plugin-system` v2, and implements only basic install/boot/recovery,
configuration persistence, router, switch, management, and diagnostic paths.
Its purpose is to test product decisions before APIs, workflows, compatibility,
polish, optimization, and hardening are frozen.

Phase 0 does not block source work and offline simulation after the alpha
workflow is activated. Host-network mutation, installer-disk mutation, and
alpha distribution stay blocked behind the separate `BFW-ALPHA-0` safety gate.
Alpha may be incomplete, rough, slow,
and reset-oriented; it may not choose the wrong disk, expose traffic by
default, leak reusable credentials, corrupt configuration silently, trust
stale authority, or call unknown state success. Full cross-platform Phase 0
remains mandatory for beta and stable, and alpha evidence cannot be promoted
into that decision.

The alpha is also the only implementation lane before Phase 0 completes.
`rpc-plugin-system`, `agent-keyring`, `agent-filesystem`, and `agent-exec` must
each independently earn an A or A+ admission before implementation expands
beyond the exact alpha scope. The grades are not averaged, and a working demo
does not excuse a weak substrate. Planning and review may continue meanwhile.

## Design posture

- Go owns orchestration, validation, APIs, state reconciliation, and service
  supervision.
- The host operating system remains the packet-processing authority; Bifrost
  will use established facilities such as Linux `nftables`, FreeBSD `pf`, and
  Windows Filtering Platform rather than inventing a userspace packet path.
- Generated firewall rules must be deterministic, reviewable, and applied
  transactionally.
- Invalid or incomplete configuration fails closed.
- The management plane must be separable from routed traffic and recoverable
  from local console access.
- Secrets must be isolated from ordinary configuration and never written to
  logs or Git.
- `agent-keyring` is the credential authority. Bifrost configuration, the web
  UI, and plugins retain only non-secret credential selectors, redacted
  metadata, and opaque reference fingerprints—not reusable secret material.
- Upgrades and migrations require preflight validation and a tested rollback
  path.

## Plugin model

Bifrost is intended to be extensible in the style of OPNsense: a small trusted
core coordinates independently versioned platform backends and optional
service plugins.

- The portable core owns canonical configuration, shared transaction envelopes,
  authorization, audit, compatibility, and rollback. Domain plugins own their
  typed domain plans; `bfw-switching` owns switching-plan semantics and
  `bfw-routing` owns routing-plan semantics.
- Platform plugins translate admitted plans into native OS firewall, routing,
  interface, and service transactions.
- Optional plugins may add VPN, DHCP, DNS, IDS/IPS, dynamic DNS, ACME,
  monitoring, backup, and similar capabilities.
- Plugins are separate supervised executables, not in-process libraries.
- Packages and manifests must be signed, versioned, permission-declared, and
  admitted before activation.
- A plugin crash must not remove the last known-good policy or open an
  unfiltered traffic path.

Switching and routing are not implemented in the core. The separately versioned
`bfw-switching` plugin owns bridge domains, VLAN membership, access/trunk and
native/PVID behavior, MAC learning and static FDB entries, STP-family loop
prevention, LACP port channels, isolation, storm control, and multicast
snooping. The separately versioned
`bfw-routing` plugin owns static routes, gateways, policy routing, route health,
ECMP where supported, and integration with admitted dynamic-routing services.
It produces typed routing plans under core admission and applies them through
supported native platform adapters. Physical interface ownership and
packet-filter policy remain separate contracts. Platform adapters may use
software switching or separately admitted hardware offload; catalog membership
does not claim universal ASIC or vendor-SDK support.

Comprehensive routing and switching are matrix claims, not product adjectives.
Routing rows cover BGP, OSPFv2/v3, IS-IS, RIP/RIPng, Babel, EIGRP, NHRP,
multicast routing, LDP/MPLS/SR/TE, and BFD. Switching rows cover VLAN/provider
bridging, STP-family, LACP/multi-chassis, discovery, multicast snooping,
port-access/link security, overlays, ring/fabric protocols, DCB/TSN, and OAM.
Every row names its standard or dialect, exact provider/platform/hardware path,
limits, semantic gaps, interoperability evidence, and admission state.

The initial capability catalog is intentionally split by ownership boundary:

- `bfw-firewall`: packet-filter, NAT, aliases, schedules, and state policy
- `bfw-network`: physical/logical ports, interface construction, MTU, and link state
- `bfw-switching`: bridges, VLAN access/trunk membership, FDB, STP, LACP,
  switched sticky endpoint bindings, isolation, storm control, snooping, and
  LLDP observations
- `bfw-routing`: canonical static, policy, and dynamic-route semantics,
  routed sticky endpoint scope, redistribution, gateways, ECMP, route health,
  and comprehensive protocol matrix ownership
- `bfw-dns`, `bfw-dhcp`, `bfw-ntp`, `bfw-ddns`, `bfw-acme`, and `bfw-mdns`:
  separately supervised core network services
- `bfw-wireguard`: site-to-site and per-device remote-access WireGuard
- `bfw-reverse-proxy`: native Go reverse proxy, ingress, TLS, and service
  publication with a Caddy-like operator experience but no Caddy runtime
  dependency
- `bfw-ha` (**GoKA**): clean-room native Go VRRP-class high availability,
  covering
  virtual addresses, health, state/configuration synchronization, and failover
  through VRRP/CARP or safe platform-equivalent mechanisms without running
  Keepalived code, binaries, configuration authority, or runtime
- `bfw-frr`: comprehensive BGP protocol/session integration with an exact
  peer-mode, AFI/SAFI, capability, security, scale, and interoperability matrix;
  all candidate routes still cross the typed `bfw-routing` authority boundary
- `bfw-ipsec`, `bfw-openvpn`, `bfw-qos`, `bfw-multiwan`, and `bfw-cellular`:
  advanced VPN, traffic, and uplink capabilities
- `bfw-fabric`: distributed Layer-2 overlays, Layer-3/anycast routing, policy
  placement, node convergence, and fabric transaction coordination
- `bfw-kubernetes-controller`: first-party dedicated Kubernetes/K3s management,
  rollout, observation, and recovery for autonomous native managed nodes
- `bfw-ids`, `bfw-dns-filter`, `bfw-threat-intel`, `bfw-captive-portal`,
  `bfw-radius`, and `bfw-upnp`: separately admitted security and access
  capabilities
- `bfw-monitoring`, `bfw-logging`, `bfw-backup`, `bfw-support`,
  `bfw-notifications`, and `bfw-updater`: operational integrations
- `bfw-installer`: reproducible signed Alpine Linux and FreeBSD appliance
  installation ISOs, exact-disk installation, first-boot verification, and
  recovery media

Names are planning identifiers until their repositories and public contracts
are admitted. Catalog membership grants no runtime authority. Every plugin must
declare typed dependencies and conflicts, UI contributions, platform support,
permissions, health, migration, rollback, and last-known-good consequences.

`bfw-ids` is intended as a clean-room native Go implementation of Snort-class
IDS/IPS behavior, not a wrapper, embedded Snort runtime, or copy of Snort
source. It owns capture normalization, flow/stream state, protocol decoding,
signature evaluation, alert evidence, and prevention proposals. A versioned
Snort-rule compatibility importer may accept only the semantics it proves;
unsupported keywords, PCRE behavior, preprocessors, or actions fail explicitly.
Only the core and `bfw-firewall` may turn a detection into packet enforcement.

Distribution is orthogonal to appliance role. A router, switch, or converged
node may run standalone or join an admitted Bifrost fabric. `bfw-fabric` owns
topology, placement, convergence, and multi-node transaction intent; it does
not own Layer-2 semantics, routes, or firewall policy. Those remain compiled by
`bfw-switching`, `bfw-routing`, and `bfw-firewall` and enforced locally on each
node under one signed configuration generation.

The first-party Bifrost Linux appliance is based on Alpine Linux and is
distributed as a generic x86-64 live installation ISO. The initial design
target is Alpine 3.24 stable; every released ISO pins the exact patch,
repository snapshot, APK/kernel/firmware inputs, inventory schema, tailoring
policy, recovery environment, installer revision, hardware matrix, and ISO
digest. The installer inventories the machine and deterministically selects the
required signed APK/service/kernel/module/firmware/boot closure, generates its
initramfs, and retains a signed broad generic recovery environment. Alpine edge,
moving repositories, APK-owned-file deletion, and a successful installer exit
without independent first-boot verification are not admissible.

The planned first-party BSD appliance uses a reduced NanoBSD-style FreeBSD
composition and is distributed initially as one generic x86-64 live installer
ISO with a published hardware matrix. The live installer inventories the
machine and deterministically creates a reduced machine-tailored installed
system while retaining a signed generic recovery environment. It is not a
universal x86-64 promise. Separately distributed prebuilt hardware-specific
media and appliance SKUs are deferred until an approved product profile names
exact hardware, firmware, lifecycle, and support obligations.
FreeBSD and Alpine share product contracts but require independent images,
platform adapters, hardware evidence, and admission decisions.

Sticky endpoint binding is available by contract in router, switch, and
converged roles. Switched ports persist an admitted MAC/port/VLAN binding under
`bfw-switching`; routed ports persist an admitted interface/VRF/MAC/IP neighbor
binding coordinated by `bfw-network`, `bfw-routing`, and `bfw-firewall`.
Unknown, moved, excessive, stale, or disputed endpoints default to drop and
alarm rather than silent relearning.

WireGuard enrollment may use OIDC to authenticate an operator or user, but a
WireGuard peer remains a per-device cryptographic identity. Private and
preshared keys remain in `agent-keyring`; routing and firewall/NAT effects are
separately admitted through their owning plugins.

`bfw-reverse-proxy` owns a Bifrost-native Go proxy engine, proxy routes,
upstreams, health, TLS policy, and service-publication UI. It does not embed,
configure, supervise, or invoke Caddy, and does not become Bifrost identity
authority, firewall authority, DNS authority, or credential storage. Forwarded
identity headers remain denied unless the core admits an explicit authenticated
proxy trust contract.

`bfw-ha`, formally named **GoKA**, implements the portable HA control logic as
a clean-room Go engine rather than copying, linking, wrapping, configuring, or
executing Keepalived. It coordinates failover but does not
silently grant itself ownership of firewall, routing, interface, service, or
credential state. A node may assume a virtual address or active role only after
peer identity, configuration and release compatibility, health, quorum/fencing
policy, and required replicated state are proven. Split brain and uncertain
ownership fail closed.

`rpc-plugin-system` is the intended lifecycle and isolation substrate, but its
current v1 Unix-socket/Linux-hardening contract is not yet a cross-platform
Bifrost dependency. Bifrost keeps its domain contracts transport-neutral while
the substrate gains Unix and Windows transports, platform peer identity,
protocol negotiation, and an externally consumable SDK.

`agent-keyring` is the intended credential substrate. The portable core must
first admit an action; only then may it request a short-lived credential-use
lease or non-exporting opaque reference scoped to the caller, plugin and
provider generations, action, target, usage, policy version, and expiry. A
credential never grants authority by itself, and raw export is denied by
default. Plugins and `bfw-web` must not read broker, VPN, DNS-provider,
ACME, API, or administrative credentials directly.

The current `agent-keyring` v1 service is Unix-socket based. Its transport,
peer-identity, encrypted-storage/unlock, lease, revocation, and recovery
contracts must be admitted on every supported Bifrost platform before runtime
integration begins.

`agent-filesystem` is the intended provider for admitted host-file operations
outside Bifrost's private canonical state. Plugin configuration artifacts,
imports/exports, backups, support bundles, and other host-file work must use
explicit path roots, operations, byte/recursion bounds, symlink and special-file
policy, mutation preconditions, and recovery evidence. A path is an operand,
not authority, and filesystem access must never become a route to keyring
payloads.

`agent-exec` is the intended provider for admitted local process execution.
Bifrost must prefer native platform APIs, but may use bounded argv execution for
separately admitted service or tooling operations. Shells, ambient PATH and
environment, inherited credentials, unrestricted network access, privilege
fallback, and reusable process handles are denied by default. Command
reachability never grants firewall or administrative authority.

Any operation combining keyring, filesystem, and process capabilities requires
one core-admitted plan plus separate, generation-bound authority for each use.
Data or handles returned by one provider never silently expand another
provider's authority.

## Management surfaces and plugin UI

Bifrost separates the privileged core from presentation:

- `bfw` is the unprivileged command-line and local-recovery client.
- `bfwd` is the public role name for the privileged core daemon.
- `bfw-web` is the public role name for the independent, unprivileged web
  service. ADR-0002 owns this naming decision.

All management clients use the same versioned, authenticated core API. They do
not edit configuration files, call platform plugins directly, run firewall
commands, or become configuration authority.

The `bfw` client presents a Cisco IOS-style command line with hierarchical
EXEC and configuration modes, familiar prompts, `show`, `configure terminal`,
`no`, `default`, `exit`, `end`, contextual `?` help, and tab completion. The
similarity is an operator interface, not an authority model: `enable` is an
authorized mode transition rather than a shared-password bypass, and
configuration commands update a session-owned candidate at a known base
generation. Operators inspect the candidate and diff, validate it, and use
`commit` or `commit confirmed` before the core may apply anything. Stale or
conflicting candidates fail closed, and an unconfirmed commit rolls back.

The command parser resolves input to versioned typed core actions; it never
constructs shell commands or edits native service configuration. Canonical
structured state remains the source of truth, while `show running-config` is a
deterministic rendering for operators and automation. Interactive command
abbreviations are allowed only when unambiguous; scripts use full canonical
commands and machine-readable output.

Plugin packages may contribute signed UI manifests containing versioned route
and navigation declarations, configuration/data schemas, declarative forms,
tables, status panels, typed action bindings, permissions, and content-addressed
asset digests. The core verifies and sanitizes those contributions before
publishing a UI catalog to `bfw-web`. Ordinary DNS, DHCP, VPN, and similar pages
are rendered from shared BFW components rather than arbitrary plugin code.

Rich extensions are exceptional. A signed custom bundle must run in a
separate-origin sandboxed frame with a strict content security policy and a
narrow capability-based message API. It receives no BFW cookies, credentials,
filesystem access, plugin sockets, top-level DOM access, or arbitrary network
access. UI and backend compatibility is checked and activated or rolled back as
one plugin release.

## Executable product governance

The meta repository has a machine-readable development control plane under
`governance/`. It owns component and external-dependency identity, release
profiles and exact admitted composition, requirement lifecycle and evidence
traces, the learning-alpha gate, the beta/stable Phase 0 gate, and test-lab requirements. Versioned JSON Schemas
under `schemas/v1/` define shared contract envelopes. ADRs, the threat model,
transaction contract, release/recovery design, v0.1 profile, and component
templates turn open architecture work into reviewable state.

Local and Forgejo checks run `python tools/governance.py validate` and
`python tools/governance.py render --check`. These checks reject inconsistent
metadata and stale generated views; they never turn missing runtime evidence
into admission. Empty component, image, artifact, rollback, signature, or
evidence pins remain blockers.

## First-class OIDC login

The Bifrost web UI treats OpenID Connect as a first-class authentication path
so standards-compliant providers such as Authentik can supply user identity.
OIDC authentication does not replace Bifrost authorization: the core explicitly
maps trusted issuer/subject and admitted claims to local roles and permissions,
denying unmapped privilege by default.

The browser flow uses Authorization Code with PKCE, exact redirect URIs, state,
nonce, TLS, discovery, and signed-token validation. OIDC client credentials are
held by `agent-keyring`; tokens and secrets are never stored in ordinary
configuration, logs, browser storage, plugins, or UI manifests. The web service
exchanges validated identity for a short-lived opaque Bifrost session, and
plugins receive only the minimum authorized actor/audit facts—not OIDC tokens.

A bounded local-console recovery identity remains available when the identity
provider, DNS, certificates, or network path is unavailable. It is not a normal
remote-login fallback and cannot be disabled solely by an OIDC configuration
change.

## Contributors

- **Linus** — product architecture, governance, installer/recovery contracts,
  and technical review.

## Current status

Governance-only meta repository. It contains executable validation/rendering
tooling, but no firewall, routing plugin, web service, installer, appliance
image, or production deployment.

The component and dependency map is maintained in
[`components/README.md`](components/README.md). Component repositories will be
pinned by immutable revision in a release manifest or Git submodule only after
their ownership and public contracts are admitted. The meta repository does
not absorb component source code.

Canonical design work proceeds in this order:

1. [`documents/PRD.md`](documents/PRD.md)
2. [`documents/ARCHITECTURE.md`](documents/ARCHITECTURE.md)
3. [`documents/IMPLEMENTATION-SPEC.md`](documents/IMPLEMENTATION-SPEC.md)

Implementation begins only after the supported platform matrix, plugin and
userspace contracts, recovery design, and acceptance tests are explicit.

Runtime implementation outside the exact learning-alpha lane is gated on
completing and admitting the required cross-platform `rpc-plugin-system`
substrate. The bounded source/offline alpha exception remains the one path
defined above; it does not permit a private fork of lifecycle, authentication,
transport, generation, or supervision rules.

The same out-of-alpha gate applies to the required cross-platform
`agent-keyring` credential-authority contract. The alpha must still use an
explicitly selected Linux-compatible keyring release and may not create a
second secret store or fall back to ambient environment variables, command
arguments, ordinary configuration files, or plugin-owned credential databases.

Cross-platform admission of `agent-filesystem` and `agent-exec` is also a Phase
0 dependency for out-of-alpha work. The alpha may use only selected
Linux-compatible releases inside `BFW-ALPHA-0`; it may not fork their path-
safety, recovery, process, sandbox, resource-bound, or audit contracts.

## Initial non-goals

- claiming feature parity with OPNsense at bootstrap
- replacing kernel packet processing with Go
- silent remote administration or undocumented telemetry
- automatic policy changes generated by an LLM
- production use before recovery, upgrade, and fail-closed behavior are proven
- loading arbitrary plugin HTML or JavaScript into the trusted web shell
- placing Bifrost runtime or plugin implementation in this meta repository

## License

MIT; see [LICENSE](LICENSE). Shared dependencies and third-party appliance
inputs retain their own licenses and require composition-level notice review.
