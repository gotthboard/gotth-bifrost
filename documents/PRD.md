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
- Go module identity is established without executable firewall code.

## Non-goals for this slice

- packet-filter implementation
- web UI or API implementation
- installer or bootable appliance image
- production deployment
- feature-parity claim against OPNsense
