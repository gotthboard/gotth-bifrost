# Linux learning-alpha decomposition

This is a decision-oriented, non-production work plan. Root `workflow.toml`
owns state and dependency order. It cannot weaken `BFW-ALPHA-0` or
`BFW-PHASE-0`.

| Order | Work package | Owner | Repository / path | Depends on | Required handoff |
| --- | --- | --- | --- | --- | --- |
| 1 | Dependency selection | meta | Bifrost `governance/alpha.toml` | routing/switching review | Immutable rpc-plugin-system v2, keyring, filesystem, and exec revisions with Linux-alpha gate evidence |
| 2 | Core transaction and state | `bfw-core` | component repository | package 1 | Typed desired state, idempotency, commit-confirmed transaction, durable recovery, audit, unknown-as-failure |
| 3 | Linux software data plane | platform/network/firewall/switching/routing owners | component repositories | packages 1–2 | nftables, netlink, and software-bridge plans; reconciliation, rollback, namespace tests, no adapter bypass |
| 4 | Basic services | DHCP/DNS owners | component repositories | packages 1–3 | Bounded DHCP and DNS behavior, persistent configuration, deterministic restart and recovery |
| 5 | Management and diagnostics | CLI/web/observability owners | component repositories | packages 2–4 | Minimal CLI/web flows, exact state/provenance, no hidden mutation path, stale/disconnected mutation denial |
| 6 | Appliance integration | installer/release owners | Alpine ISO workflow and packages 1–5 | completed ISO decomposition | Install, boot, configure, reset, clean reinstall, local recovery, and first-boot deny evidence on one profile |
| 7 | Alpha admission | meta + independent reviewers | Bifrost evidence and release records | packages 1–6 | All `BFW-ALPHA-0` safety gates, limitation matrix, signed artifacts, decision log, no beta/stable promotion claim |

## Supported learning surface

- Alpine x86-64, single node, one pinned VM/hardware profile;
- interfaces, addresses, static routes, firewall, NAT, bounded DHCP/DNS;
- software bridge, access/trunk VLANs, FDB visibility, basic loop protection;
- configuration persistence, clean reinstall, reset, local recovery;
- minimal CLI/web management and strong decision diagnostics.

## Explicitly denied in the first alpha

- production use, HA, distributed fabric, clustering, and remote scheduling;
- dynamic routing, comprehensive protocol suites, hardware offload, and broad
  vendor/hardware support;
- automatic upgrade, unattended destructive actions, arbitrary package or URL
  fetches, and moving dependency revisions;
- promotion of alpha artifacts or evidence into beta or stable;
- any out-of-alpha implementation until rpc-plugin-system, agent-keyring,
  agent-filesystem, and agent-exec each independently earn A or A+ Phase 0
  admission.

## Decisions the alpha must inform

The evidence packet must record operator friction, component boundary changes,
failure and recovery behavior, observability gaps, resource cost, data-plane
mechanism choices, and which plugin surfaces deserve beta hardening. Popularity
or demo success is not an admission signal.
