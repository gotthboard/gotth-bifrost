# Bifrost component map

This directory belongs to the Bifrost meta repository. It records component
ownership and, after admission, exact immutable component pins. It does not
contain copied component source.

## Planned Bifrost-owned components

| Component | Responsibility | Status |
| --- | --- | --- |
| `bfw-core` | canonical configuration, admission, transaction coordination, audit, reconciliation, and recovery | planned; repository not created |
| `bfw-cli` | unprivileged `bfw` command-line and local-recovery client | planned; repository not created |
| `bfw-web` | independent unprivileged web/API presentation service and trusted UI shell | planned; repository not created |
| `bfw-routing` | routing domain, deterministic route plans, platform apply/verify adapters, routing UI contribution, and routing rollback effects | planned; repository not created |
| `bfw-firewall` | packet-filter, NAT, aliases, schedules, state policy, deterministic policy plans, and native apply/verify adapters | planned; repository not created |
| `bfw-network` | interfaces, VLANs, bridges, bonds/LAGs, MTU, DHCP client, and link-state ownership | planned; repository not created |
| `bfw-wireguard` | WireGuard site-to-site tunnels, per-device remote access, enrollment, peer state, key rotation, and VPN UI | planned; repository not created |
| `bfw-reverse-proxy` | native Go reverse proxy, ingress, upstream health, TLS policy, service publication, and proxy UI with no Caddy runtime dependency | planned; repository not created |
| `bfw-ha` | native Go HA control logic, virtual-address ownership, health, failover, state/configuration synchronization, and VRRP/CARP/equivalent platform mechanisms with no Keepalived runtime dependency | planned; repository not created |
| `bfw-plugin-sdk` | versioned Bifrost domain, plugin, UI-manifest, and compatibility contracts | planned; repository not created |
| identity/authentication component | generic OIDC relying-party integration, claim mapping inputs, and opaque Bifrost session exchange; final repository boundary/name not selected | planned; repository not created |
| platform backends | native firewall, interface, and other OS-specific adapters for admitted platforms | planned; repository boundaries not yet selected |
| network-service plugins | `bfw-dns`, `bfw-dhcp`, `bfw-ntp`, `bfw-ddns`, `bfw-acme`, and `bfw-mdns` | planned; repositories not created |
| advanced-network plugins | `bfw-frr`, `bfw-ipsec`, `bfw-openvpn`, `bfw-qos`, `bfw-multiwan`, and `bfw-cellular` | planned; repositories not created |
| security plugins | `bfw-ids`, `bfw-dns-filter`, `bfw-threat-intel`, `bfw-captive-portal`, `bfw-radius`, and `bfw-upnp` | planned; repositories not created |
| operations plugins | `bfw-monitoring`, `bfw-logging`, `bfw-backup`, `bfw-support`, `bfw-notifications`, and `bfw-updater` | planned; repositories not created |

Names other than the settled `bfw` CLI namespace and `bfw-routing` ownership
boundary remain planning labels until their repository and public-interface
decisions are explicitly admitted.

## Catalog ownership rules

- `bfw-firewall` owns packet filtering and NAT; `bfw-network` owns link and
  interface construction; `bfw-routing` owns route semantics. No one plugin may
  collapse those authorities into an ambient network-administrator capability.
- `bfw-wireguard` owns tunnel and peer semantics. It requests separately
  admitted routing and firewall/NAT effects and never stores reusable private
  or preshared keys outside `agent-keyring`.
- `bfw-reverse-proxy` owns proxy configuration and observed proxy health. DNS,
  ACME credentials, firewall exposure, and identity-header trust remain typed
  dependencies owned by their respective authorities. It is a native Bifrost
  implementation and does not embed, invoke, supervise, or configure Caddy.
- `bfw-ha` owns failover intent and active/standby evidence. It coordinates
  virtual-address, routing, firewall, service, and replicated-state changes
  through typed plans; it does not seize those domains directly. Its portable
  control logic is implemented in Go and does not embed, invoke, supervise, or
  configure Keepalived.
- Every plugin declares compatible platforms, dependencies, conflicts,
  permissions, schemas, UI contracts, health, migration/rollback behavior,
  and release evidence before it can be pinned here.

## Existing external substrate dependencies

| Repository | Bifrost use |
| --- | --- |
| `agents/rpc-plugin-system` | cross-platform executable lifecycle, transport, identity/generation, supervision, and diagnostics substrate |
| `agents/agent-keyring` | credential authority and scoped/non-exporting credential use |
| `agents/agent-filesystem` | scoped host-file operations outside core private state |
| `agents/agent-exec` | bounded admitted local process execution when native APIs are insufficient |

These dependencies are not vendored here. Bifrost runtime remains gated on
their cross-platform contracts and independent admission.

## Pinning rule

When a component repository is created and admitted, this meta repository shall
record:

- canonical repository owner/name and immutable commit or signed release
- contract, schema, and UI-manifest versions
- supported Bifrost and platform ranges
- signature/provenance and artifact digests
- migration order and rollback-compatible revision
- verification and independent review evidence

Git submodules may represent exact source revisions, but the machine-readable
release composition is authoritative for packaged artifacts and compatibility.
