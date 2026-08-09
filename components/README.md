# Bifrost component map

This directory belongs to the Bifrost meta repository. It records component
ownership and, after admission, exact immutable component pins. It does not
contain copied component source.

`governance/components.toml` is authoritative for component identity,
dependencies, platform status, pins, and admission. This file explains the map
for humans and must not override the machine-readable catalog.

## Planned Bifrost-owned components

| Component | Responsibility | Status |
| --- | --- | --- |
| `bfw-core` | canonical configuration, admission, transaction coordination, audit, reconciliation, and recovery | planned; repository not created |
| `bfw-cli` | unprivileged Cisco IOS-style `bfw` command-line and local-recovery client; modal grammar maps to typed core actions and candidate transactions | planned; repository not created |
| `bfw-web` | independent unprivileged web/API presentation service and trusted UI shell | planned; repository not created |
| `bfw-switching` | canonical Layer-2 topology plus comprehensive switching-protocol/mechanism matrix, switched sticky endpoint bindings, deterministic plans, provider/platform apply/verify, UI, observation, and rollback | planned; repository not created |
| `bfw-routing` | canonical Layer-3 route semantics plus comprehensive routing-protocol matrix, routed sticky endpoint scope, redistribution, deterministic plans, provider/platform apply/verify, UI, observation, and rollback | planned; repository not created |
| `bfw-firewall` | packet-filter, NAT, aliases, schedules, state policy, deterministic policy plans, and native apply/verify adapters | planned; repository not created |
| `bfw-network` | physical/logical ports, interface construction, MTU, DHCP client, and link-state ownership | planned; repository not created |
| `bfw-wireguard` | WireGuard site-to-site tunnels, per-device remote access, enrollment, peer state, key rotation, and VPN UI | planned; repository not created |
| `bfw-reverse-proxy` | native Go reverse proxy, ingress, upstream health, TLS policy, service publication, and proxy UI with no Caddy runtime dependency | planned; repository not created |
| `bfw-ha` (**GoKA**) | clean-room native Go VRRP-class HA control, virtual-address role intent, typed health, failover, state/configuration synchronization, and admitted CARP/equivalent adapters with no Keepalived code or runtime dependency | planned; repository not created |
| `bfw-fabric` | distributed topology, overlay/underlay placement, convergence, multi-node transactions, and coordination of switching/routing/firewall plans without owning those domains | deferred; repository not created |
| `bfw-kubernetes-controller` | first-party out-of-the-box Kubernetes/K3s-hosted management, inventory, rollout, observation, and recovery coordination for autonomous native Bifrost nodes | planned; repository not created |
| `bfw-plugin-sdk` | versioned Bifrost domain, plugin, UI-manifest, and compatibility contracts | planned; repository not created |
| `bfw-identity` | generic OIDC relying-party validation and opaque identity facts without core authorization ownership | planned; repository not created |
| `bfw-platform-linux` | Linux nftables/netlink, bridge/VLAN, optional admitted switch offload, interface, routing, and service adapters | planned; repository not created |
| `bfw-platform-freebsd` | FreeBSD pf, bridge/VLAN, routing, interface, CARP, and service adapters | planned; repository not created |
| `bfw-platform-windows` | Windows Filtering Platform, admitted Hyper-V vSwitch/equivalent, IP Helper, interface, routing, and service adapters | planned; repository not created |
| network-service plugins | `bfw-dns`, `bfw-dhcp`, `bfw-ntp`, `bfw-ddns`, `bfw-acme`, and `bfw-mdns` | planned; repositories not created |
| `bfw-frr` | comprehensive BGP protocol/session adapter with an exact capability matrix and typed candidate-route handoff to `bfw-routing`; no direct canonical route authority | deferred; repository not created |
| other advanced-network plugins | `bfw-ipsec`, `bfw-openvpn`, `bfw-qos`, `bfw-multiwan`, and `bfw-cellular` | planned; repositories not created |
| `bfw-ids` | native Go Snort-class IDS/IPS engine: capture normalization, flow/stream state, protocol decoding, rules, alerts/evidence, and typed enforcement proposals | deferred; repository not created |
| other security plugins | `bfw-dns-filter`, `bfw-threat-intel`, `bfw-captive-portal`, `bfw-radius`, and `bfw-upnp` | planned; repositories not created |
| operations plugins | `bfw-monitoring`, `bfw-logging`, `bfw-backup`, `bfw-support`, `bfw-notifications`, and `bfw-updater` | planned; repositories not created |
| `bfw-installer` | separately versioned reproducible signed Alpine Linux appliance installation ISO, exact-disk installation, first-boot verification, and recovery media with no packet-policy authority | deferred; repository not created |

Catalog names are settled planning identifiers. They create no runtime or
release authority until their repositories, public contracts, exact revisions,
artifacts, rollback mates, evidence, and admission are recorded here.

## Catalog ownership rules

- `bfw-firewall` owns packet filtering and NAT; `bfw-network` owns ports and
  interface construction; `bfw-switching` owns Layer-2 forwarding and loop
  control; `bfw-routing` owns Layer-3 route semantics. No one plugin may
  collapse those authorities into an ambient network-administrator capability.
- `bfw-switching` coordinates cross-domain changes through the core. It never
  writes routes or firewall policy, and hardware offload requires a separately
  admitted platform adapter with equivalent apply, observe, verify, and
  rollback behavior.
- `bfw-wireguard` owns tunnel and peer semantics. It requests separately
  admitted routing and firewall/NAT effects and never stores reusable private
  or preshared keys outside `agent-keyring`.
- `bfw-reverse-proxy` owns proxy configuration and observed proxy health. DNS,
  ACME credentials, firewall exposure, and identity-header trust remain typed
  dependencies owned by their respective authorities. It is a native Bifrost
  implementation and does not embed, invoke, supervise, or configure Caddy.
- `bfw-ha`/GoKA owns failover intent and active/standby evidence. It coordinates
  virtual-address, routing, firewall, service, and replicated-state changes
  through typed plans; it does not seize those domains directly. Its portable
  control logic is clean-room Go and does not copy, embed, invoke, supervise,
  configure, or require Keepalived.
- `bfw-frr` owns BGP wire/session behavior for one exact admitted FRR build. It
  exports typed candidate routes and observations to `bfw-routing`; it cannot
  write canonical routes, hold ambient peer keys, or treat provider CLI/config
  text as Bifrost authority.
- `bfw-installer` owns image-build and installation mechanics only. It consumes
  an immutable release composition and cannot configure post-install packet
  policy, retain installer secrets, choose a disk by unstable enumeration, or
  create an updater path outside the signed release/recovery contract.
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
