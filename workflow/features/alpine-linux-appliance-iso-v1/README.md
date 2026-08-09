# Generic Alpine live installer with machine-tailored installation

Canonical state, dependencies, blockers, review, and evidence are defined only in root `workflow.toml`.

This feature makes Alpine Linux the canonical base for Bifrost's first-party
Linux appliance. Generic live installation media boots the published hardware
matrix and deterministically creates a machine-tailored installed system
without collapsing installer, updater, recovery, or packet-policy authority.

Planned scope:

- implement BFW-PRD-209 through BFW-PRD-214 only after this feature becomes the
  single active workflow
- create and admit the separately versioned `bfw-installer` repository
- pin an exact supported Alpine 3.24 patch, APK snapshot, kernel sources/
  packages, build toolchain, inventory schema, tailoring policy, recovery
  environment, firmware, boot chain, architecture, hardware matrix, and ISO
  digest
- derive a deterministic machine manifest and select only required signed APK,
  service, kernel/module, firmware, boot, and Bifrost content
- generate the exact initramfs/module-load closure without deleting APK-owned
  files; build a custom kernel/module layer only as an explicit bounded slow path
- retain a signed broad generic recovery kernel/initramfs/environment
- prove x86-64 UEFI/BIOS offline installation, exact-disk confirmation,
  interruption, inventory change, recovery, clean install, inactive-slot
  rebuild/rollback, drift, and first-boot packet/state behavior

Separately distributed prebuilt hardware-specific media and appliance SKUs are
deferred until an approved product profile names exact hardware and lifecycle/
support obligations. Install-time machine tailoring is part of this feature.

This planned record creates no installer source, ISO, disk mutation, package
fetch, process launch, release, deployment, or support claim.
