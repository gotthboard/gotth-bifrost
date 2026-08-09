# Release composition plan

This is a release gate plan, not a release record. Canonical composition state
remains in `governance/releases/` and cannot outrun component admission.

## Alpha composition

An alpha composition may be created only after the learning-alpha workflow,
Alpine appliance artifacts, applicable `BFW-ALPHA-0` safety gates, and every
included component handoff pass. It must pin:

- every repository revision, artifact digest, dependency lock, schema/API
  version, Alpine/APK snapshot, inventory schema, tailoring policy, recovery
  environment, live-media hardware matrix, and ISO digest;
- every build/distribution component revision and artifact digest separately
  from the installed runtime composition;
- each target's normalized hardware inventory, machine plan, selected APK/
  service/kernel/initramfs/module/firmware manifest, installed-file manifest,
  and slot digest;
- signed SBOM and provenance, builder identity, reproducibility result,
  channel/signing identity, rollback mates, and expiration/support limits;
- clean install, first boot, configuration, reset, clean reinstall, upgrade,
  interrupted upgrade, rollback, recovery, and deny-by-default packet evidence;
- exact supported hardware/VM profile and a published limitation matrix.

Alpha artifacts and evidence cannot be relabeled or promoted into beta or
stable. A beta/stable composition is rebuilt from independently admitted inputs
after full `BFW-PHASE-0` passes.

## Admission sequence

1. Validate every installed runtime component, build/distribution component,
   and dependency is admitted for the target channel and exact revision.
2. Build twice from immutable offline inputs and compare content identities.
3. Run composition, installation, lifecycle, rollback, recovery, security, and
   channel-isolation harnesses.
4. Obtain an independent cold review over the exact composition manifest and
   evidence set.
5. Sign only after all gates pass; publish manifest, SBOM, provenance,
   limitations, rollback instructions, and support status together.
6. If any input, artifact, or evidence changes, invalidate the verdict and
   repeat the gate. Unknown or partial state is `not_admitted`.
