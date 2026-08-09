# Generic FreeBSD live installer and machine-tailoring decomposition

This is the checked plan for `freebsd-generic-appliance-iso-v1`. Activation and
state remain controlled only by `workflow.toml`.

| Order | Work package | Owner | Intended source location | Dependency | Required handoff |
| --- | --- | --- | --- | --- | --- |
| 1 | Immutable FreeBSD inputs | meta/release | Bifrost `governance/` | routing/switching and shared installer boundaries | Supported FreeBSD release/source revision, source/object sets, build toolchain, inventory schema, tailoring policy, package snapshot, generic recovery environment, firmware, bootloader, architecture, live-media hardware matrix, licenses, digests, and support expiry |
| 2 | FreeBSD platform closure | `bfw-platform-freebsd` | separate component repository | package 1 | PF, routing, bridge/VLAN, CARP/pfsync, IPsec, interface, service, native-state oracle, unsupported-feature, and semantic-gap contract |
| 3 | Reproducible generic live media | `bfw-installer` | builder subtree | packages 1–2 | Declarative `src.conf`, signed base/object/package inputs, broad boot drivers, generic recovery environment, dependency closure, reproducible live ISO, SBOM/provenance |
| 4 | Hardware inventory and admission | platform + installer | hardware-matrix and inventory fixtures | packages 1–3 | Normalized CPU, UEFI/BIOS, console, NIC, storage, virtualization, and firmware facts; ambiguity, change, and unknown-hardware rejection before disk mutation |
| 5 | Deterministic machine tailoring | `bfw-installer` | planner/builder subtree | packages 3–4 | Signed selection policy, content-addressed machine manifest, exact kernel/module/firmware/package closure, default prebuilt-set path, optional resource-estimated full-source path, no mutable fetches |
| 6 | Install transaction | `bfw-installer` | installer subtree | packages 4–5 | Offline stable-disk inventory, displayed machine plan, exact destructive confirmation, journaled stages, idempotent resume or safe reset, sealed manifest, secret/signing-key leak denial |
| 7 | Dual-slot update and recovery | `bfw-installer` + `bfw-updater` + `bfw-backup` | installer/updater handoff | package 6 | Read-only replaceable machine-tailored slots, durable state separation, retained generic recovery environment, signed activation, boot confirmation, inventory-aware rebuild, rollback mate, local recovery |
| 8 | Network and failure admission | platform/domain owners + meta | isolated test lab | packages 2–7 | PF/routing/bridge/CARP/FRR native-state and packet oracles, build/resource bounds, inventory change, recovery boot, power loss, corrupt input, drift, rollback, and cross-distribution non-inheritance evidence |
| 9 | Independent admission | meta + independent reviewers | release/workflow evidence | packages 1–8 | Two clean reviews over one immutable revision, exact evidence digests, published limitations, and no unsupported hardware claim |

## Initial profile boundary

- One generic x86-64 FreeBSD live ISO with a published, finite hardware matrix.
- Each install deterministically creates a machine-tailored system from signed
  offline inputs and retains a signed generic recovery environment.
- UEFI and legacy BIOS are included only for admitted rows.
- The image is reduced declaratively; manual file deletion is forbidden.
- Linux and FreeBSD share product contracts but never admission evidence.
- Separately distributed prebuilt hardware-specific media and appliance SKUs
  remain deferred until an approved product profile names exact hardware and
  lifecycle obligations.

## Explicit non-goals

- universal x86-64 hardware support
- a vendor appliance SKU or separately distributed hardware-specific medium
- importing Alpine packaging, drivers, or test evidence as FreeBSD proof
- allowing native package or base-system mutation outside signed Bifrost release
  transactions
- runtime implementation before workflow activation and prerequisite admission
