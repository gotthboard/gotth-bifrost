# Bifrost (BFW)

**Bifrost**, with the firewall shorthand **BFW**, is a planned open-source,
cross-platform network firewall and routing platform written in Go, in the same
broad product category as OPNsense.

The goal is a security-first appliance that combines deterministic packet and
policy control with a clear API, auditable configuration, safe upgrades, and a
web administration plane. This repository is an architectural bootstrap—not a
working firewall, router, or security boundary yet.

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

- The portable core owns configuration, validation, policy IR, authorization,
  audit, compatibility, and rollback.
- Platform plugins translate admitted plans into native OS firewall, routing,
  interface, and service transactions.
- Optional plugins may add VPN, DHCP, DNS, IDS/IPS, dynamic DNS, ACME,
  monitoring, backup, and similar capabilities.
- Plugins are separate supervised executables, not in-process libraries.
- Packages and manifests must be signed, versioned, permission-declared, and
  admitted before activation.
- A plugin crash must not remove the last known-good policy or open an
  unfiltered traffic path.

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

## Current status

Planning only. There is no executable firewall, web service, installer, image,
or production deployment in this repository.

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
