# Generic x86-64 FreeBSD appliance installation ISO

This planned feature makes FreeBSD the canonical base for Bifrost's first-party
BSD appliance and initial generic x86-64 installation ISO. `workflow.toml` is
the authority for state, dependencies, review, blockers, and evidence.

The feature shall:

- implement BFW-PRD-223 through BFW-PRD-228 only after its dependencies and
  workflow activation permit work
- reuse the separately versioned `bfw-installer` authority boundary without
  giving the installer packet-policy or post-install configuration authority
- pin one supported FreeBSD release/source revision, source-build options,
  kernel, packages, firmware, boot artifacts, hardware matrix, and image inputs
- build a reduced NanoBSD-style dual-slot appliance from declarative manifests
- prove complete offline installation, exact-disk confirmation, interruption,
  recovery, first boot, update, rollback, and native network-state behavior
- keep every FreeBSD admission result independent from Alpine evidence

Hardware-specific appliance images are not part of this feature. They require
a later approved product profile naming exact hardware, firmware, lifecycle,
replacement, and support obligations.

No runtime implementation, ISO build, package fetch, disk mutation, release,
or distribution is authorized by this planning record.
