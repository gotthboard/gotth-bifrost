# Bifrost (BFW) Product Requirements

Status: initial planning baseline

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
  and state-policy semantics; `bfw-network` shall own interfaces, VLANs,
  bridges, bonds/LAGs, MTU, DHCP-client, and link-state semantics; and
  `bfw-routing` shall own routing semantics. Cross-domain changes shall use one
  core-admitted transaction without collapsing these authorities.
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
- **BFW-PRD-057:** `bfw-reverse-proxy` shall provide a Caddy-style reverse
  proxy and ingress capability with Caddy as the preferred first adapter. It
  shall own proxy routes, upstreams, health checks, TLS policy, service
  publication, observed state, UI contributions, and proxy-specific rollback.
- **BFW-PRD-058:** `bfw-reverse-proxy` shall not become firewall, DNS,
  credential, or identity authority. Certificate and provider credentials
  shall use `agent-keyring`; DNS, ACME, and firewall exposure shall use typed
  dependencies; forwarded identity headers shall remain denied unless an
  explicit authenticated reverse-proxy trust contract is admitted by the core.
- **BFW-PRD-059:** `bfw-ha` shall provide Keepalived-style high availability
  using admitted VRRP, CARP, or platform-equivalent adapters for virtual
  addresses, peer/node health, active/standby roles, state and configuration
  synchronization, failover, recovery, and HA-specific UI and audit evidence.
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
  plugin model, and planning-only status.
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
