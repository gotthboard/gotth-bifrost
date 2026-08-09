# Generic FreeBSD live installer with machine-tailored installation

This planned feature makes FreeBSD the canonical base for Bifrost's first-party
BSD appliance. Its initial generic x86-64 live installation ISO boots the
published hardware matrix and creates a machine-tailored installed system.
`workflow.toml` is the authority for state, dependencies, review, blockers,
and evidence.

The feature shall:

- implement BFW-PRD-223 through BFW-PRD-228 only after its dependencies and
  workflow activation permit work
- reuse the separately versioned `bfw-installer` authority boundary without
  giving the installer packet-policy or post-install configuration authority
- pin one supported FreeBSD release/source revision, source/object sets,
  build toolchain, inventory schema, tailoring policy, packages, firmware,
  boot/recovery artifacts, hardware matrix, and ISO inputs
- derive a deterministic machine build manifest from normalized hardware facts
- assemble pinned prebuilt base sets and build machine-specific kernel/modules
  by default, with full on-target source compilation only as an explicit slow
  path
- build a reduced NanoBSD-style dual-slot appliance while retaining a signed
  generic recovery kernel/environment
- prove complete offline installation, exact-disk confirmation, interruption,
  inventory change, recovery, first boot, update, rollback, and native
  network-state behavior
- keep every FreeBSD admission result independent from Alpine evidence

Separately distributed prebuilt hardware-specific media and appliance SKUs are
not part of this feature. They require a later approved product profile naming
exact hardware, firmware, lifecycle, replacement, and support obligations.
That exclusion does not apply to install-time machine tailoring.

No runtime implementation, ISO build, package fetch, disk mutation, release,
or distribution is authorized by this planning record.
