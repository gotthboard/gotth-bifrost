# Bifrost (BFW)

**Bifrost**, with the firewall shorthand **BFW**, is a planned open-source,
cross-platform network firewall and routing platform written in Go, in the same
broad product category as OPNsense.

The goal is a security-first appliance that combines deterministic packet and
policy control with a clear API, auditable configuration, safe upgrades, and a
web administration plane. This is the **Bifrost meta repository**: it owns the
cross-repository product definition, component map, integration contracts,
compatibility matrix, release composition, and system-level evidence. It is
not a product runtime module, firewall, router, or security boundary.

## Naming

- Full product name: **Bifrost**
- Canonical firewall shorthand: **BFW** (Bifrost Firewall)
- Lowercase command, package, configuration, and protocol namespace: `bfw`
- Repository name: `Bifrost`

The shorthand `BFW` identifies Bifrost's firewall product and is not the formal
full name, a separate component, or an edition. Future public interfaces must
use `bfw` consistently and must not
introduce competing `bfr`, `bif`, or ambiguous `bifrost` shorthand namespaces.

## Intended capabilities

- stateful firewall policy through native platform engines
- routing, VLANs, bridges, bonds, and interface management
- NAT, port forwarding, and policy-based routing
- DHCP, DNS forwarding, and network-service supervision
- site-to-site and remote-access VPN integration
- high-availability state and configuration synchronization
- versioned configuration with validation, audit history, and rollback
- metrics, structured logs, packet captures, and diagnostics
- authenticated web UI and API
- signed plugin/package repository with compatibility and permission admission
- signed, transactional upgrades with recovery support

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
  typed domain plans; `bfw-routing` owns routing-plan semantics.
- Platform plugins translate admitted plans into native OS firewall, routing,
  interface, and service transactions.
- Optional plugins may add VPN, DHCP, DNS, IDS/IPS, dynamic DNS, ACME,
  monitoring, backup, and similar capabilities.
- Plugins are separate supervised executables, not in-process libraries.
- Packages and manifests must be signed, versioned, permission-declared, and
  admitted before activation.
- A plugin crash must not remove the last known-good policy or open an
  unfiltered traffic path.

Routing is not implemented in the core. The separately versioned
`bfw-routing` plugin owns static routes, gateways, policy routing, route health,
ECMP where supported, and integration with admitted dynamic-routing services.
It produces typed routing plans under core admission and applies them through
supported native platform adapters. Interface/VLAN ownership and packet-filter
policy remain separate contracts.

The initial capability catalog is intentionally split by ownership boundary:

- `bfw-firewall`: packet-filter, NAT, aliases, schedules, and state policy
- `bfw-network`: interfaces, VLANs, bridges, bonds/LAGs, MTU, and link state
- `bfw-routing`: static and policy routing, gateways, ECMP, and route health
- `bfw-dns`, `bfw-dhcp`, `bfw-ntp`, `bfw-ddns`, `bfw-acme`, and `bfw-mdns`:
  separately supervised core network services
- `bfw-wireguard`: site-to-site and per-device remote-access WireGuard
- `bfw-reverse-proxy`: native Go reverse proxy, ingress, TLS, and service
  publication with a Caddy-like operator experience but no Caddy runtime
  dependency
- `bfw-ha`: native Go high availability inspired by Keepalived, covering
  virtual addresses, health, state/configuration synchronization, and failover
  through VRRP/CARP or safe platform-equivalent mechanisms without running
  Keepalived
- `bfw-frr`, `bfw-ipsec`, `bfw-openvpn`, `bfw-qos`, `bfw-multiwan`, and
  `bfw-cellular`: advanced routing, VPN, traffic, and uplink capabilities
- `bfw-ids`, `bfw-dns-filter`, `bfw-threat-intel`, `bfw-captive-portal`,
  `bfw-radius`, and `bfw-upnp`: separately admitted security and access
  capabilities
- `bfw-monitoring`, `bfw-logging`, `bfw-backup`, `bfw-support`,
  `bfw-notifications`, and `bfw-updater`: operational integrations

Names are planning identifiers until their repositories and public contracts
are admitted. Catalog membership grants no runtime authority. Every plugin must
declare typed dependencies and conflicts, UI contributions, platform support,
permissions, health, migration, rollback, and last-known-good consequences.

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

`bfw-ha` implements the portable HA control logic in Go rather than wrapping,
configuring, or executing Keepalived. It coordinates failover but does not
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
default. Plugins and `bifrost-web` must not read broker, VPN, DNS-provider,
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
- `bfwd` is the provisional role name for the privileged core daemon.
- `bfw-web` is the provisional role name for the independent, unprivileged web
  service.

All management clients use the same versioned, authenticated core API. They do
not edit configuration files, call platform plugins directly, run firewall
commands, or become configuration authority.

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

## Current status

Planning-only meta repository. There is no executable firewall, routing plugin,
web service, installer, image, or production deployment here.

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

Runtime implementation is also gated on completing and admitting the required
cross-platform `rpc-plugin-system` substrate. Bifrost will not create a private
fork of lifecycle, authentication, transport, generation, or supervision rules
to begin earlier.

The same gate applies to the required cross-platform `agent-keyring`
credential-authority contract. Bifrost will not create a second secret store or
fall back to ambient environment variables, command arguments, ordinary
configuration files, or plugin-owned credential databases.

Cross-platform admission of `agent-filesystem` and `agent-exec` is also a Phase
0 dependency. Bifrost will not fork their path-safety, recovery, process,
sandbox, resource-bound, or audit contracts to begin implementation early.

## Initial non-goals

- claiming feature parity with OPNsense at bootstrap
- replacing kernel packet processing with Go
- silent remote administration or undocumented telemetry
- automatic policy changes generated by an LLM
- production use before recovery, upgrade, and fail-closed behavior are proven
- loading arbitrary plugin HTML or JavaScript into the trusted web shell
- placing Bifrost runtime or plugin implementation in this meta repository
