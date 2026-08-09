# Bifrost release and recovery design

Status: architecture baseline; implementation and platform evidence absent

Requirements: BFW-PRD-006, BFW-PRD-031, BFW-PRD-039, BFW-PRD-049,
BFW-PRD-074, BFW-PRD-079, BFW-PRD-089, BFW-PRD-209 through BFW-PRD-228

## Release inputs

An admitted release is one signed composition, not a collection of latest
branches. It contains exact component commits, artifact digests, API/schema/UI/
CLI versions, platform image digests, dependency and conflict closure,
migration order, rollback mates, SBOM and provenance digests, evidence hashes,
and an admission decision. Source commits and packaged artifact digests are
both required.

For the first-party Linux appliance, release input also includes the exact
supported Alpine stable patch release, immutable APK repository snapshot and
keys, package versions/digests, kernel/modules/firmware, bootloader/initramfs,
`bfw-installer` revision, ISO digest, and installed-system manifest or image
digest. Alpine edge and moving repository indexes are not release inputs.

For the first-party BSD appliance, release input also includes the exact
supported FreeBSD release and source revision, source/object sets, `src.conf`,
build toolchain, normalized inventory schema, signed tailoring policy, generic
recovery kernel/environment, module/firmware/boot manifests, private
package-repository snapshot and keys, package versions/digests, generic x86-64
live-media hardware-matrix revision, `bfw-installer` revision, and ISO digest.
Each installation adds its content-addressed normalized hardware inventory,
machine build plan, installed-system manifest, and slot digest. Undeclared
post-install deletion and moving package inputs are not release inputs.

## Reproducible composition

Each artifact records source revision, locked dependencies, build toolchain and
target, build command, environment policy, SBOM, provenance statement, and
output digest. Two isolated builders must reproduce identical content or a
documented normalized equivalence before stable admission. Network-fetched or
mutable build inputs are forbidden unless content-addressed and declared.

## Signing and channels

ADR-0006 defines the offline root and delegated roles. ADR-0007 defines
development, alpha, beta, and stable channels. Promotion creates new signed metadata
that references already verified artifacts; it does not rebuild them. Expired,
unknown, revoked, wrong-channel, rollback, or inconsistent metadata fails
closed.

Alpha metadata uses a separate delegated role and is accepted only by systems
explicitly enrolled for the learning alpha. Alpha artifacts are visibly
non-production, may require reset/reinstall between incompatible builds, and
publish their exact scope and known limitations. Alpha metadata, evidence, and
successful operation cannot be relabelled or replayed as beta or stable. The
alpha safety gate still requires stable disk selection, fail-closed packet
state, secret custody, transactional configuration, stale-authority denial,
and local reset/recovery before installation or network mutation is allowed.
No implementation or release composition outside the exact alpha scope begins
until every Phase 0 dependency independently earns an A or A+ admission; alpha
behavior and aggregate grades cannot satisfy that prerequisite.

## Activation

1. Download into a bounded staging area without touching the active slot.
2. Verify root/delegation chain, expiry, channel, rollback counters, manifest,
   artifacts, SBOM/provenance, platform, dependencies, schemas, migrations,
   rollback mates, space, power/reboot preconditions, and recovery access.
3. Build the inactive A/B appliance slot and run offline configuration
   migration against a copy.
4. Record the prior signed release/configuration pair as last known good.
5. Atomically select the candidate slot for the next boot.
6. After boot, verify core, platform policy, management recovery, required
   services, and packet/state oracles within a bounded confirmation window.
7. Confirm the slot only after all checks pass. Otherwise boot the previous
   slot and restore its compatible configuration generation.

Platforms without safe A/B mechanics require a separately admitted equivalent;
in-place replacement is not assumed safe.

## Initial Alpine installation

The signed Bifrost Alpine ISO performs a complete offline install from the same
content-addressed composition used for release admission. Before any write it
records stable target-disk identity, shows the exact planned layout and loss
boundary, and requires explicit destructive confirmation naming that target.
It revalidates disk identity immediately before the first write and journals
destructive stages so interruption cannot be mistaken for success.

Installation ends only after boot artifacts, system content, durable-state
layout, signatures, and first-boot selection are verified. The first boot is
an unconfigured fail-closed appliance and must pass local core/platform/recovery
checks before configuration enrollment. A booted ISO, completed copy, or zero
installer exit code alone is not successful installation evidence.

## Initial FreeBSD installation

The signed Bifrost FreeBSD ISO performs the same bounded offline installation
transaction against its independently admitted FreeBSD composition. It rejects
hardware outside the published generic x86-64 matrix before disk mutation and
records normalized CPU, boot, console, NIC, storage, virtualization, and
firmware facts. It derives and displays a deterministic machine build plan from
the signed tailoring policy before destructive confirmation.

The default path assembles pinned prebuilt base/object sets and packages and
builds only machine-specific kernel/modules when required. A full on-target
source build is an explicit resource-estimated slow path, not the default. Both
paths are offline, produce a content-addressed installed-system manifest, and
retain a separately verifiable signed generic recovery kernel/environment. No
release-signing private key is present on the ISO; release signatures cover the
selectable inputs and tailoring policy rather than pretending the generated
machine manifest was signed at release time.

Installation creates independently verifiable code/root slots plus separate
durable configuration, audit/evidence, and recovery state. First boot remains
fail closed until the FreeBSD platform adapter, required services, local
recovery, native PF/routing/bridge/CARP state, and packet oracles are complete.
Alpine success, FreeBSD-native update success, or a booted generic kernel does
not substitute for this evidence.

## Configuration migration

Migrations are signed, ordered, deterministic, version-bounded, and run against
a copy. They declare reversibility, maximum resources, and compatibility with
the rollback release. Failed, interrupted, lossy, or unverifiable migration
does not overwrite current or last-known-good state. Export/import uses a
versioned signed envelope and never includes reusable secrets.

## Local-console recovery

The console can list signed release/configuration pairs, select an admitted
rollback mate, run read-only diagnostics, restore management reachability, and
export a redacted support record through typed core recovery actions. It cannot
open a shell, edit native policy files, bypass authorization/audit, or import
unsigned state. Recovery actions are rate-limited and append-only audited.

## Admission evidence

The test lab must exercise power loss or process kill at every staging,
migration, boot-selection, first-boot, confirmation, and rollback boundary;
corrupt/expired/revoked metadata; mismatched schemas and rollback mates; low
space; missing network/identity services; management lockout; and independent
packet-policy completeness before a release can be called recoverable.
