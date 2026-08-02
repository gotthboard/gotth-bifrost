# Bifrost (BFW) Architecture

Status: initial boundary architecture

## Naming boundary

**Bifrost** is the full product name; **BFW** is its canonical firewall
shorthand (Bifrost Firewall), and `bfw` is the lowercase public namespace.
Component names must compose beneath that namespace rather than inventing
another product acronym. Internal working names such as `bifrostd` or
`bifrost-web` remain provisional until executable, service, API, package, and
upgrade naming is admitted as one compatibility contract.

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
domain-specific rollback consequences; `bfw-routing` owns the routing domain.
The `rpc-plugin-system` substrate owns executable lifecycle and trust facts. It
must not become firewall-policy or routing authority.

Candidate plugin classes:

- platform firewall and interface backends
- `bfw-routing` routing-domain plugin and its platform apply/verify adapters
- DHCP and DNS services
- VPN providers
- IDS/IPS and traffic-analysis services
- high-availability and configuration synchronization
- dynamic DNS, ACME, monitoring, backup, and support tooling

Core configuration, admission, audit, package verification, and recovery remain
non-optional. Plugins cannot replace or weaken them.

## Routing plugin boundary

`bfw-routing` is the routing-domain plugin. It owns:

- static route and gateway desired state
- route selection, metrics, tables/VRFs, and policy-routing domain validation
- gateway and route-health observations
- ECMP modeling where the admitted platform supports it
- integration contracts for separately supervised dynamic-routing services
- deterministic route-plan generation and applied-state verification
- routing-specific UI schemas, typed actions, audit facts, and rollback effects

It does not own interface/VLAN creation, DNS or DHCP, packet-filter/NAT policy,
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

The core may coordinate a transaction containing firewall, interface, and
routing steps, but it does not reimplement the routing domain. `bfw-routing`
must declare ordering, preconditions, reversibility, partial-failure semantics,
and last-known-good consequences so the core can admit the whole transaction.

## Capability plugin catalog

The catalog is an ownership and planning map, not an ambient service bus. A
plugin calls no peer plugin as an authority. It proposes typed effects to the
core; the core validates the actor, dependency graph, permissions, generations,
ordering, failure behavior, and whole-transaction rollback before dispatching
each step to its owning component.

| Class | Planned plugins | Ownership summary |
| --- | --- | --- |
| Foundation | `bfw-firewall`, `bfw-network`, `bfw-routing`, `bfw-wireguard`, `bfw-reverse-proxy`, `bfw-ha` | packet/NAT policy; links/interfaces; routes; WireGuard peers/tunnels; proxy ingress; failover coordination |
| Network services | `bfw-dns`, `bfw-dhcp`, `bfw-ntp`, `bfw-ddns`, `bfw-acme`, `bfw-mdns` | separately supervised core network services and their bounded configuration/status |
| Advanced network | `bfw-frr`, `bfw-ipsec`, `bfw-openvpn`, `bfw-qos`, `bfw-multiwan`, `bfw-cellular` | dynamic routing, alternate VPNs, shaping, uplink policy/failover, and modem integration |
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

`bfw-reverse-proxy` provides a Caddy-style ingress and reverse-proxy domain.
Caddy is the preferred first service adapter because it offers a useful secure
configuration model and automatic certificate workflows, but the Bifrost
contract describes proxy routes, listeners, upstreams, health, TLS policy,
service publication, observations, and rollback rather than exposing Caddy's
configuration as the canonical product API.

The proxy plugin may request typed effects from `bfw-dns`, `bfw-acme`, and
`bfw-firewall`. It does not modify their state directly. Account keys, DNS API
tokens, private keys, and upstream credentials remain in `agent-keyring`.
Generated adapter configuration uses `agent-filesystem`; admitted adapter
execution uses `agent-exec` only where a native/service API is insufficient.

Forwarded identity is a separate trust contract. The proxy strips
client-supplied identity headers by default and may add authenticated identity
facts only for an exact admitted upstream, protected path, header set, network
path, key/certificate generation, and expiry. Merely installing or enabling the
proxy does not satisfy the OIDC forwarded-header exception in BFW-PRD-047.

TLS issuance failure, upstream-health uncertainty, partial route publication,
or incompatible Caddy/adapter behavior fails closed for the affected route
without weakening unrelated last-known-good routes. Firewall exposure and DNS
publication are committed only with verified proxy readiness or rolled back.

### High-availability plugin boundary

`bfw-ha` supplies Keepalived-style high availability without making
Keepalived the portable product contract. Linux may use an admitted
Keepalived/VRRP adapter; FreeBSD may use CARP; other platforms require an
equivalent adapter whose semantics are explicitly mapped and tested. A platform
without safe address-ownership and fencing semantics reports the feature as
unsupported rather than emulating it weakly.

The plugin owns cluster membership intent, authenticated peer observations,
virtual-address role intent, priority/preemption policy, health inputs,
configuration/state synchronization plans, transition ordering, HA UI, and
failover audit facts. The network, routing, firewall, service, keyring, and
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

`bfwd` and `bfw-web` are provisional role names until public executable and
service naming is admitted. The architectural boundary is not provisional: the
web service is unprivileged, separately restartable, and incapable of direct
firewall, filesystem, keyring, execution-provider, or plugin-socket access.

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
  -> unprivileged bifrost-web
  -> bifrostd validates and admits the exact action
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

## Cross-platform substrate prerequisite

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

This substrate is a predecessor project, not a parallel convenience task.
Bifrost design and interface planning may continue, but runtime implementation
is blocked until the cross-platform substrate is complete and independently
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

## Recovery

The detailed recovery model is not yet selected. Implementation is blocked
until the project defines local-console recovery, last-known-good selection,
interrupted-upgrade behavior, configuration export/import, and appliance-image
rollback.
