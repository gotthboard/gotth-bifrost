# Bifrost Product Requirements

Status: initial planning baseline

## Product objective

Build a cross-platform Go firewall and routing system that provides a coherent
administration plane over proven native packet-processing and networking
facilities. The system must prioritize safety, deterministic behavior,
recoverability, extensibility, and clear operational evidence over feature
count.

## Initial requirements

- **BFR-PRD-001:** Bifrost shall compile one canonical policy model into
  deterministic, platform-native transactions and verify the applied result.
- **BFR-PRD-002:** Configuration changes shall be schema-validated, versioned,
  audited, and recoverable through rollback.
- **BFR-PRD-003:** Failed validation, partial configuration, and uncertain
  runtime state shall fail closed without silently discarding the last
  known-good configuration.
- **BFR-PRD-004:** The management plane shall support explicit network exposure
  controls and a local recovery path.
- **BFR-PRD-005:** Routing, interface, NAT, firewall, DHCP, DNS, and VPN
  integrations shall have explicit ownership boundaries and health evidence.
- **BFR-PRD-006:** Upgrades shall be signed, preflighted, transactional where
  practical, and recoverable after interruption.
- **BFR-PRD-007:** Secrets shall be stored separately from ordinary
  configuration and excluded from logs, exports, and source control.
- **BFR-PRD-008:** Supported operating system, release, kernel/runtime,
  architecture, and appliance-image targets shall be pinned before
  implementation admission.
- **BFR-PRD-009:** Bifrost shall support independently versioned, separately
  supervised plugins without allowing them to redefine core authorization,
  configuration authority, lifecycle identity, or audit rules.
- **BFR-PRD-010:** Plugin packages, manifests, migrations, and declared
  permissions shall be signed, compatibility-checked, and admitted before
  activation.
- **BFR-PRD-011:** Plugin APIs shall be stable, version-negotiated, additive by
  default, and fail closed on unsupported required behavior.
- **BFR-PRD-012:** Plugin failure, restart, removal, or upgrade shall not erase
  the last known-good network policy or create an unintended open path.
- **BFR-PRD-013:** Bifrost runtime implementation shall not begin until the
  required cross-platform `rpc-plugin-system` lifecycle substrate has passed
  its compatibility, security, failure, and platform admission gates.
- **BFR-PRD-014:** `agent-keyring` shall be Bifrost's credential authority.
  Bifrost configuration, databases, logs, exports, support bundles, web UI,
  and plugins shall not retain reusable secret payloads.
- **BFR-PRD-015:** Core action admission shall precede credential access.
  Credential possession, keyring reachability, process identity, or plugin
  capability shall not independently authorize a Bifrost action.
- **BFR-PRD-016:** Credential access shall use short-lived leases or
  non-exporting opaque references bound to the caller, plugin and provider
  generations, admitted action, credential usage, access mode, target,
  audience, policy version, credential generation, keyring authority
  generation, and expiry. Raw export shall be denied by default.
- **BFR-PRD-017:** Credential revocation, rotation, keyring restore, authority
  restart, policy change, or relevant runtime-generation change shall make
  stale leases and references unusable and auditable.
- **BFR-PRD-018:** Bifrost runtime credential integration shall not begin until
  `agent-keyring` has passed cross-platform transport, peer-identity,
  encrypted-storage/unlock, lease, revocation, recovery, SDK, and redaction
  admission gates for the supported Bifrost platforms.
- **BFR-PRD-019:** Host-file operations outside Bifrost's private canonical
  state shall use `agent-filesystem` with a core-admitted scope containing
  explicit roots, operations, bounds, link/special-file policy, mutation
  preconditions, recovery behavior, generation, expiry, and audit correlation.
- **BFR-PRD-020:** Bifrost shall treat paths and filesystem results as operands,
  not authority. Filesystem operations shall not expose keyring payloads,
  provider-private state, or reusable handles, and destructive operations shall
  require an explicit destructive admission and recoverable behavior where the
  platform contract supports it.
- **BFR-PRD-021:** Local process execution shall use `agent-exec` only after
  core admission of the executable identity, argv or separately allowed shell,
  cwd, environment, stdio, timeout, process-tree, resource, network,
  filesystem-containment, side-effect, retry, and audit policies.
- **BFR-PRD-022:** Bifrost process execution shall deny shells, ambient PATH and
  environment, inherited credentials, unrestricted network access, privilege
  fallback, and reusable raw process/session handles by default. Native
  platform APIs shall remain preferred for firewall and routing mutation.
- **BFR-PRD-023:** A workflow combining credentials, files, and processes shall
  require one sealed core-admitted plan and separate, matching, short-lived
  authority for every keyring, filesystem, and execution use. Outputs or
  handles from one provider shall not expand another provider's authority.
- **BFR-PRD-024:** Bifrost runtime integration shall not begin until
  `agent-filesystem` and `agent-exec` have passed their supported-platform
  transport, identity, path/process safety, sandbox/containment, recovery,
  lifecycle, SDK, audit/redaction, and independent admission gates.

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
