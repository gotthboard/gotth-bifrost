# Alpine Linux appliance installation ISO

Status: planned; blocked behind the active routing/switching design workflow

This feature makes Alpine Linux the canonical base for Bifrost's first-party
Linux appliance and bootable installation ISO without collapsing installer,
updater, recovery, or packet-policy authority.

Planned scope:

- implement BFW-PRD-209 through BFW-PRD-214 only after this feature becomes the
  single active workflow
- create and admit the separately versioned `bfw-installer` repository
- pin an exact supported Alpine 3.24 patch release, repository snapshot,
  package/kernel/firmware set, boot chain, architecture, and every image digest
- build signed content-addressed reproducible ISO and installed-image artifacts
- support x86-64 UEFI and legacy BIOS, complete offline installation, stable
  target-disk identity, explicit destructive confirmation, and local recovery
- prove interruption, power-loss, corrupt-media, clean-install,
  upgrade/rollback, recovery, drift, and first-boot packet/state behavior

This planned record creates no installer source, ISO, disk mutation, package
fetch, process launch, release, deployment, or support claim.
