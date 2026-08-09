# Alpine appliance and ISO decomposition

This is a checked work plan, not implementation evidence. Root `workflow.toml`
owns state and dependency order.

| Order | Work package | Owner | Repository / path | Depends on | Required handoff |
| --- | --- | --- | --- | --- | --- |
| 1 | Immutable distribution inputs | meta/release | Bifrost `governance/` | routing/switching completion | Exact Alpine patch, immutable APK snapshot, kernel, packages, firmware, bootloader, architecture, source digests, licenses, and expiry policy |
| 2 | Installer authority | `bfw-installer` | separate component repository, not yet created | package 1 | Typed disk inventory and selection API, stable hardware identity, no packet-policy or secret-custody authority |
| 3 | Reproducible image builder | `bfw-installer` | builder subtree | packages 1–2 | Offline inputs only, two clean-build digest match, signed ISO and installed-image provenance, SBOM |
| 4 | Install transaction | `bfw-installer` | installer subtree | packages 2–3 | Explicit destructive confirmation, write-ahead state, interruption and power-loss recovery, idempotent resume or safe reset |
| 5 | Boot and first boot | `bfw-installer` + platform | installer/platform handoff | package 4 | UEFI and legacy BIOS evidence, verified configuration identity, deny-by-default packet state, bounded recovery console |
| 6 | Upgrade, rollback, recovery | updater/recovery owners | component handoffs | packages 3–5 | Signed A/B or equivalent rollback, corrupt-media and failed-upgrade recovery, rollback-mate identity, drift detection |
| 7 | Appliance admission | meta/release | Bifrost evidence and release records | packages 1–6 | Wrong-disk, offline-install, clean-reinstall, interruption, rollback, recovery, first-boot, provenance, and independent-review evidence |

## Fixed initial platform

- Alpine Linux 3.24 stable family; the exact patch remains deliberately
  unselected until workflow activation.
- x86-64 only, UEFI and legacy BIOS, one explicitly pinned VM/hardware profile.
- Moving repositories, Alpine edge, network-dependent installation, ambiguous
  disk names, best-effort rollback, and unsigned artifacts are denied.

## Activation boundary

Workflow activation may select immutable inputs and create component-owned
implementation tasks. It does not authorize host disk writes, artifact
distribution, or production use. Those effects remain blocked until the exact
`BFW-ALPHA-0` gates applicable to them pass.
