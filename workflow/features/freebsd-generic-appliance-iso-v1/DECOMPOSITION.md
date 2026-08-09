# Generic FreeBSD appliance and ISO decomposition

This is the checked plan for `freebsd-generic-appliance-iso-v1`. Activation and
state remain controlled only by `workflow.toml`.

| Order | Work package | Owner | Intended source location | Dependency | Required handoff |
| --- | --- | --- | --- | --- | --- |
| 1 | Immutable FreeBSD inputs | meta/release | Bifrost `governance/` | routing/switching and shared installer boundaries | Supported FreeBSD release/source revision, build options, package snapshot, kernel/modules, firmware, bootloader, architecture, hardware matrix, licenses, digests, and support expiry |
| 2 | FreeBSD platform closure | `bfw-platform-freebsd` | separate component repository | package 1 | PF, routing, bridge/VLAN, CARP/pfsync, IPsec, interface, service, native-state oracle, unsupported-feature, and semantic-gap contract |
| 3 | Declarative reduced build | `bfw-installer` | builder subtree | packages 1–2 | `src.conf`, kernel configuration, signed private package manifest, dependency closure, retained recovery/diagnostics, reproducible NanoBSD-style ISO and installed image, SBOM/provenance |
| 4 | Generic hardware admission | platform + installer | hardware-matrix fixtures | packages 1–3 | UEFI/BIOS, NIC, storage, virtualization, firmware rows; unknown-hardware rejection before disk mutation |
| 5 | Install transaction | `bfw-installer` | installer subtree | packages 3–4 | Offline stable-disk inventory, exact destructive confirmation, journaled stages, idempotent resume or safe reset, secret-leak denial |
| 6 | Dual-slot update and recovery | `bfw-installer` + `bfw-updater` + `bfw-backup` | installer/updater handoff | package 5 | Read-only replaceable system slots, durable state separation, signed activation, boot confirmation, rollback mate, local recovery |
| 7 | Network and failure admission | platform/domain owners + meta | isolated test lab | packages 2–6 | PF/routing/bridge/CARP/FRR native-state and packet oracles, resource bounds, power loss, corrupt input, drift, rollback, and cross-distribution non-inheritance evidence |
| 8 | Independent admission | meta + independent reviewers | release/workflow evidence | packages 1–7 | Two clean reviews over one immutable revision, exact evidence digests, published limitations, and no unsupported hardware claim |

## Initial profile boundary

- One generic x86-64 FreeBSD ISO with a published, finite hardware matrix.
- UEFI and legacy BIOS are included only for admitted rows.
- The image is reduced declaratively; manual file deletion is forbidden.
- Linux and FreeBSD share product contracts but never admission evidence.
- Hardware-specific images remain deferred until an approved appliance product
  profile names exact hardware and lifecycle obligations.

## Explicit non-goals

- universal x86-64 hardware support
- a vendor appliance SKU or hardware-specific optimization
- importing Alpine packaging, drivers, or test evidence as FreeBSD proof
- allowing native package or base-system mutation outside signed Bifrost release
  transactions
- runtime implementation before workflow activation and prerequisite admission
