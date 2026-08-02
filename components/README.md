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
| `bfw-plugin-sdk` | versioned Bifrost domain, plugin, UI-manifest, and compatibility contracts | planned; repository not created |
| platform backends | native firewall, interface, and other OS-specific adapters for admitted platforms | planned; repository boundaries not yet selected |
| optional plugins | DHCP, DNS, VPN, IDS/IPS, ACME, dynamic DNS, monitoring, backup, HA, and other separately admitted capabilities | planned; repositories not created |

Names other than the settled `bfw` CLI namespace and `bfw-routing` ownership
boundary remain planning labels until their repository and public-interface
decisions are explicitly admitted.

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
