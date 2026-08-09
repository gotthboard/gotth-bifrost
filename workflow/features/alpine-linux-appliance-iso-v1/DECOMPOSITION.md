# Generic Alpine live installer and machine-tailoring decomposition

This is a checked work plan, not implementation evidence. Root `workflow.toml`
owns state and dependency order.

| Order | Work package | Owner | Repository / path | Depends on | Required handoff |
| --- | --- | --- | --- | --- | --- |
| 1 | Immutable distribution inputs | meta/release | Bifrost `governance/` | routing/switching completion | Exact Alpine patch/APK snapshot, kernel sources/packages, build toolchain, inventory schema, tailoring policy, generic recovery environment, firmware, bootloader, architecture, live-media hardware matrix, source digests, licenses, and expiry policy |
| 2 | Installer authority | `bfw-installer` | separate component repository, not yet created | package 1 | Typed machine/disk inventory APIs, stable identity, no packet-policy, secret-custody, or release-signing-key authority |
| 3 | Reproducible generic live media | `bfw-installer` | builder subtree | packages 1–2 | Offline inputs only, two clean media-build digest match, signed ISO/recovery artifacts, SBOM/provenance |
| 4 | Hardware inventory and admission | platform + installer | hardware-matrix and inventory fixtures | packages 1–3 | Normalized CPU, UEFI/BIOS, console, NIC, storage, virtualization, and firmware facts; ambiguity, change, and unknown-hardware denial before disk mutation |
| 5 | Deterministic machine tailoring | `bfw-installer` | planner/builder subtree | packages 3–4 | Signed selection policy, content-addressed manifest, exact APK/service/kernel/initramfs/module/firmware/boot closure, APK ownership preservation, optional bounded custom kernel/module layer, no mutable fetches |
| 6 | Install transaction | `bfw-installer` | installer subtree | packages 4–5 | Displayed machine/disk plan, exact destructive confirmation, write-ahead state, interruption/power-loss recovery, idempotent resume or safe reset, sealed manifest, secret/signing-key denial |
| 7 | Boot, first boot, and recovery | `bfw-installer` + platform | installer/platform handoff | package 6 | UEFI/BIOS evidence, verified machine manifest, deny-by-default packet state, signed generic recovery kernel/initramfs/environment, bounded recovery console |
| 8 | Upgrade and rollback | updater/recovery owners | component handoffs | packages 5–7 | Inventory-aware inactive-slot rebuild, signed activation, boot confirmation, corrupt-input and failed-upgrade recovery, rollback-mate identity, drift detection |
| 9 | Appliance admission | meta/release | Bifrost evidence and release records | packages 1–8 | Inventory/build-plan reproducibility, APK ownership, wrong-disk, offline install, clean reinstall, interruption, rollback, recovery, first boot, provenance, resource bounds, and independent review |

## Fixed initial platform

- Alpine Linux 3.24 stable family; the exact patch remains deliberately
  unselected until workflow activation.
- x86-64 only, UEFI and legacy BIOS, one explicitly pinned VM/hardware profile.
- The live ISO is generic for the admitted matrix; each installed composition is
  machine-tailored and retains the signed generic recovery environment.
- Moving repositories, Alpine edge, network-dependent installation, ambiguous
  hardware/disk identity, APK-owned-file deletion, best-effort rollback, and
  unsigned release inputs are denied.

## Activation boundary

Workflow activation may select immutable inputs and create component-owned
implementation tasks. It does not authorize host disk writes, artifact
distribution, or production use. Those effects remain blocked until the exact
`BFW-ALPHA-0` gates applicable to them pass.
