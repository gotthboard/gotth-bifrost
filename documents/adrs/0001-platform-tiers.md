# ADR-0001: Platform tiers

Status: Accepted

Date: 2026-08-08

Requirements: BFW-PRD-008, BFW-PRD-065, BFW-PRD-087, BFW-PRD-090,
BFW-PRD-209 through BFW-PRD-214, BFW-PRD-223 through BFW-PRD-228

Supersedes: none

## Context

Bifrost is cross-platform, but claiming equal first-release maturity would hide
different kernel semantics and multiply the initial admission surface.

## Decision

The v0.1 implementation profile is Linux-first. FreeBSD and Windows are
compatibility targets for the shared schemas, SDK, lifecycle substrate, and
native platform contracts; their product images are admitted in later release
profiles. Darwin is a shared-SDK build/test target until a product profile says
otherwise. Unsupported or weaker semantics fail closed.

Exact OS releases, kernels, architectures, images, and digests are release
inputs, not permanent ADR text. `governance/test-lab.toml` leaves them empty and
blocks system admission until measured images are selected.

The first Linux product image is a generic x86-64 Alpine live installation ISO
with an explicit hardware matrix. It derives normalized hardware inventory and
a deterministic machine install manifest, selects the minimal signed APK/
kernel/module/firmware/service closure, generates the exact initramfs, and
retains a signed broad generic recovery environment. The installed composition
is machine-tailored; the distributed live media remains generic.

The first BSD product image, when its later release profile is activated, is a
generic x86-64 FreeBSD live installation ISO with an explicit hardware
compatibility matrix. It derives a deterministic hardware inventory and
machine build manifest during installation, then creates a reduced
NanoBSD-style installed appliance for that machine while retaining a signed
generic recovery environment. Separately distributed prebuilt hardware-specific
media and appliance SKUs are deferred until an approved product profile
identifies exact hardware and support obligations.

## Consequences

- v0.1 has one product data-plane target and a smaller test matrix.
- Cross-platform contracts still cannot be Linux-specific shortcuts.
- No FreeBSD, Windows, or Darwin product-support claim exists yet.
- The Alpine live ISO does not promise universal x86-64 support, and its
  machine-tailored result cannot be admitted from media boot alone.
- The planned generic FreeBSD live ISO does not claim universal x86-64 support
  and cannot inherit Alpine build, hardware, performance, or admission
  evidence.
- Install-time machine tailoring is part of the generic live-installer profile;
  a separately distributed appliance-specific SKU remains out of scope until
  actual hardware and lifecycle obligations exist.

## Alternatives considered

- Admit three product platforms in v0.1: rejected as too broad for trustworthy
  first-release evidence.
- Linux-only architecture: rejected because it would corrupt shared contracts.

## Verification

- v0.1 profile partition and platform-policy validation.
- Phase 0 cross-platform substrate gates remain mandatory.
