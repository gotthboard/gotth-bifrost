# Bifrost (BFW) Implementation Specification

Status: executable meta-governance active; bounded Linux learning-alpha source implementation permitted

## Linux learning-alpha gate

The first implementation target is a deliberately narrow, non-production
Linux learning alpha. Source implementation, unit tests, deterministic offline
simulation, network-namespace tests, and disposable-VM tests may begin before
full cross-platform Phase 0 admission after the alpha workflow is activated.
Phase 0 exemption alone does not activate work. These activities do not authorize mutation of a
developer workstation, production network, or unconfirmed disk.

The alpha target is one pinned Alpine Linux x86-64 appliance profile using
`rpc-plugin-system` v2 and selected Linux-compatible `agent-keyring`,
`agent-filesystem`, and `agent-exec` releases. It is single-node, software-data-
plane only, and limited to installation/boot/recovery, configuration
persistence, interfaces, static routes, firewall/NAT, DHCP/DNS, bridge,
access/trunk VLANs, FDB inspection, basic loop protection, minimal CLI/web
management, and diagnostic evidence. HA, fabric, broad dynamic routing,
comprehensive switching protocols, hardware offload, secondary operating
systems, polish, performance tuning, and production hardening remain outside
this alpha.

`governance/alpha.toml` is the authoritative `BFW-ALPHA-0` gate. Before any
designated non-production host-network mutation, installer-disk mutation, or
alpha artifact distribution, stable disk selection, fail-closed packet policy,
opaque secret custody, transactional configuration, connection-bound identity,
non-repeating generation identity, enforced liveness, bounded work, safe
teardown, stale-authority denial, local recovery/reset, channel isolation, and
independent review must be admitted with immutable evidence.

The alpha may be incomplete, rough, slow, and reset-oriented. It may not erase
an unconfirmed disk, expose unintended traffic, leak reusable credentials,
silently corrupt configuration, trust stale authority, or report success while
authoritative state is unknown. Alpha observations and operator decisions are
design evidence, not promotion evidence.

## Beta and stable Phase 0 dependency gate

Finish and admit the cross-platform `rpc-plugin-system` lifecycle substrate and
the `agent-keyring`, `agent-filesystem`, and `agent-exec` provider substrates
before any Bifrost beta, stable, or production runtime admission begins.
Each dependency must independently earn an A or A+ grade from fresh evidence
and independent review. Averages, transitive trust, self-grading, and a working
alpha are not substitutes. Until all four meet that bar, runtime source work is
limited to the exact BFW-PRD-216 alpha slice; broader plugins, protocols,
platforms, product features, and beta/stable implementation must not start.
Requirements, architecture, decomposition, and review may continue.

Required exit evidence:

- Unix-domain-socket and Windows-named-pipe transports behind one documented
  compatibility contract
- Linux, BSD/macOS, and Windows peer-identity backends with fail-closed tests
- explicit protocol/capability version negotiation and compatibility matrix
- externally consumable, versioned Go SDK/module
- matching auth, generation, health, timeout, cancellation, restart, teardown,
  redaction, and append-only logging behavior on supported platforms
- crash/restart/endurance evidence proving stale generations and transports do
  not remain trusted
- clean independent review and admission decision
- cross-platform `agent-keyring` service transport and peer-identity binding
- versioned external keyring SDK with explicit compatibility negotiation
- cross-platform encrypted-payload storage and unlock/recovery contract
- lease and opaque-reference scope, expiry, revocation, rotation, restart,
  restore, and stale-generation tests
- raw-export-denied, non-loggable response, redaction, export, support-bundle,
  and audit-correlation tests
- cross-platform `agent-filesystem` scope, path normalization, symlink/reparse
  point, race safety, atomicity/durability, COW/trash recovery, bounds, SDK, and
  audit/redaction evidence
- cross-platform `agent-exec` executable identity, argv/shell separation,
  account, environment, filesystem containment, sandbox, network/resource,
  timeout/cancellation, process-tree, lifecycle-ref, SDK, and audit/redaction
  evidence
- composition tests proving keyring, filesystem, and execution authority cannot
  be exchanged, widened, inferred, or reused across provider boundaries

Bifrost design and bounded alpha work may continue during Phase 0 under
`BFW-ALPHA-0`. It must not add provider-local substrate forks or claim beta,
stable, production, or cross-platform admission before Phase 0 passes.

## Bootstrap slice

1. Maintain private `gotthboard/gotth-bifrost` on Forgejo and `main`, preserving
   the original `danny/Bifrost` history; mirror approved public source to GitHub.
2. Establish it as the product meta repository with no product Go module.
3. Record product, component, architecture, safety, and recovery boundaries.
4. Define planned component/dependency ownership and pinning rules.
5. Verify clean Git state and exact local/remote ref equality.

All future public CLI commands, package/configuration keys, protocol labels,
and compatibility identifiers use the lowercase `bfw` namespace. ADR-0002
settles `bfw`, `bfwd`, and `bfw-web` as the public executable role names.

## GOTTH implementation adoption

Follow [GOTTH-INTEGRATION.md](GOTTH-INTEGRATION.md) and the ordered
[adoption plan](../workflow/features/gotth-foundation-adoption/PLAN.md).
This records BFW-PRD-229 through BFW-PRD-234; it does not activate the planned
runtime feature or relax the preceding alpha/Phase 0 gates. Shared repositories
are reused through versioned dependencies in their consuming component repos,
not copied into this meta repository. Empty component revision/artifact fields
continue to mean unadmitted, including for GOTTH entries.

## Router-hosted service implementation

[EDGE-SERVICES.md](EDGE-SERVICES.md) defines BFW-PRD-235 through BFW-PRD-240.
Follow its profile -> scoped placement -> Caddy read-only/one-route -> credential
and resource admission -> other services sequence. Implementation remains in
separate component repositories. No new runtime feature is activated here.

## Required design work before beta or stable admission

The Linux learning alpha may implement only the narrower surface named above.
Everything below remains required before beta or stable admission even when an
alpha experiment appears successful.

- pin supported OS releases, kernels/runtime APIs, Go, CPU architectures, and
  image/installer targets
- define canonical configuration schema and migration rules
- define management identity, authorization, session, and recovery contracts
- define the platform-neutral policy IR and native backend contracts
- define `nftables`/netlink, FreeBSD `pf`, and Windows Filtering Platform
  runtime-boundary behavior and hard limits for admitted targets
- define signed plugin manifests, package provenance, compatibility,
  permissions, migrations, activation, removal, and rollback
- define the required cross-platform `rpc-plugin-system` substrate evolution
- define `agent-keyring` selectors, core-admission proofs, lease and opaque-ref
  scopes, credential classes, revocation, rotation, recovery, and
  cross-platform substrate evolution
- define `agent-filesystem` scopes for generated configuration, import/export,
  backup, diagnostics, and support artifacts without exposing canonical state
  or keyring storage
- define `agent-exec` envelopes for the minimal commands that cannot use native
  APIs, including denial defaults and cross-platform process semantics
- define typed, bounded, separately admitted data transfer between keyring,
  filesystem, and execution providers
- define the independent unprivileged web-service and `bfw` CLI contracts over
  one authenticated, versioned core API
- define the Cisco IOS-style CLI mode grammar, prompt and transition rules,
  contextual help/completion, canonical scripting form, typed-action mapping,
  session-owned candidate lifecycle, diff/validation, commit-confirmed, and
  redacted history/output contracts
- define the signed plugin UI manifest, declarative schema/component contract,
  sanitized UI catalog, route namespace, permissions, asset digest model, and
  compatibility negotiation
- define custom-bundle separate-origin sandbox, CSP, capability-message,
  data-bound, and denial contracts
- define atomic backend/UI/schema/migration/asset activation and rollback plus
  disabled, incompatible, unhealthy, and web-failure behavior
- define the meta-repository release composition schema, immutable component
  pins, compatibility evidence, migration order, and rollback pairing
- define the `bfw-routing` domain model, typed plan, platform-adapter,
  apply/verify, ordering, failure, recovery, UI, and audit contracts without
  implementing them in this repository
- define `bfw-frr` as the comprehensive BGP protocol adapter with an exact
  provider/platform/peer-mode/AFI-SAFI/capability/security/scale/interoperability
  matrix, typed candidate-route boundary, staged lifecycle, bounded telemetry,
  and no direct canonical route authority
- define the OIDC provider profile, Authorization Code + PKCE flow, discovery
  and token validation, key rotation, explicit claim mapping, assurance/step-up,
  keyring use, opaque local sessions, logout/revocation, outage, audit, and
  local-console recovery contracts
- define the canonical capability-plugin catalog schema, typed dependency and
  conflict graph, platform-support declarations, degradation rules, health,
  migration, rollback, UI, evidence, and release-admission states
- define `bfw-firewall`, `bfw-network`, `bfw-switching`, and `bfw-routing` as separate domain
  authorities and specify atomic cross-domain transaction coordination
- define `bfw-switching` as the Layer-2 authority for bridge domains, VLAN
  membership, FDB, STP, LACP, isolation, storm control, multicast snooping,
  LLDP observations, platform semantic gaps, and management-path recovery
- define switched and routed sticky endpoint-binding variants, bounded
  enrollment, generation-bound persistence, violation behavior, cross-domain
  enforcement, observation, clearing/replacement, and rollback
- define machine-readable router, switch, and converged deployment profiles,
  role-specific enabled/denied forwarding effects, management-only addressing,
  capability admission, and transactional role transitions
- define Layer-2/Layer-3 switch effects and Layer-3/Layer-4-aware router effects
  while retaining separate routing and firewall plan ownership and excluding
  implied Layer-7 behavior
- define `bfw-wireguard` peer/tunnel, per-device enrollment, keyring,
  routing/firewall coordination, site-to-site validation, status, and rollback
  contracts while retaining a generic later-VPN extension contract
- define the native Go `bfw-reverse-proxy` HTTP/TLS data path, routes,
  listeners, upstream health, limits, DNS/ACME/firewall dependencies,
  forwarded-identity trust, UI, staged publication, conformance, verification,
  and rollback contracts without a Caddy runtime dependency
- define the native Go `bfw-ha` control plane, cluster identity, VRRP protocol
  and CARP/platform mechanism boundaries, virtual-address ownership,
  quorum/fencing, priority/preemption, state/config synchronization,
  dependent-service readiness, split-brain handling, UI, transition,
  interoperability, and recovery contracts without a Keepalived runtime
  dependency
- define bounded ownership contracts for every network-service,
  advanced-network, security/access, and operations plugin in the catalog
- define the native Go `bfw-ids` capture, normalization, flow/stream,
  decoder/rule, Snort-import, resource-bound, alert/evidence, signed-ruleset,
  passive/inline, enforcement-proposal, platform, and admission contracts
- define `bfw-fabric` membership/identity, quorum/fencing, EVPN-class
  Layer-2/3 overlays, anycast/VRF/ECMP routing, distributed policy placement,
  flow-state ownership, partitions, MTU/offload, staged rollout, convergence,
  observability, rollback, scale, and admission contracts
- define last-known-good, confirmation timer, rollback, and interrupted-upgrade
  behavior
- define the separately versioned `bfw-installer`, exact Alpine Linux and
  FreeBSD inputs, reproducible signed offline ISO/image builds, deterministic
  machine tailoring, destructive-disk confirmation, first-boot verification,
  package-drift, and recovery contracts
- define independent correctness oracles for compiled and applied policy
- decompose the first narrow vertical slice
- maintain the authoritative component/release catalog, requirement registry,
  alpha and Phase 0 dashboards, versioned schemas, ADR index, threat model,
  cross-component transaction contract, v0.1 profile, component templates,
  release/recovery plan, test-lab specification, and governance CI

## Planned capability sequence

This is a dependency order, not permission to create every repository at once:

1. `bfw-firewall`
2. `bfw-network`
3. `bfw-switching`
4. `bfw-routing`
5. `bfw-dns`
6. `bfw-dhcp`
7. `bfw-wireguard`
8. `bfw-acme` and `bfw-ddns`, followed by `bfw-reverse-proxy`
9. `bfw-monitoring`, `bfw-logging`, `bfw-backup`, and `bfw-updater`
10. `bfw-ha` and `bfw-multiwan`
11. `bfw-installer` after the release-schema and recovery contracts, and before
    the first complete Alpine release composition; FreeBSD output admission
    remains a later independent platform workflow
12. `bfw-ids`, `bfw-frr`, and the remaining catalog plugins as their contracts
    and user need justify them

Each component begins with its own PRD, architecture, implementation spec,
contract tests, platform matrix, and narrow vertical slice. The meta repository
admits and pins it only after independent verification. This sequence does not
override the Phase 0 substrate gate for beta or stable admission. Alpha work
must instead remain inside `BFW-ALPHA-0`.

### BGP suite implementation contract

Before `bfw-frr` runtime work, its component repository shall define and
version these public artifacts:

- BGP desired-state, policy, peer, peer-group, family, capability, validation,
  limit, and authentication-reference schemas
- an exact FRR build/platform capability matrix with `unsupported`, `partial`,
  `experimental`, `supported`, and `admitted` states
- candidate-route and withdrawal records crossing from `bfw-frr` to
  `bfw-routing`, bound to peer, family, VRF, policy, validation, source FRR
  generation, and immutable route identity
- bounded peer, Adj-RIB-In/Out, Loc-RIB, decision, rejection, graceful-restart,
  BFD, convergence, BMP/MRT, health, and drift observations
- candidate/preflight/apply/converge/commit/rollback transaction records with
  immutable request and generation identities

The minimum matrix has distinct rows for eBGP, iBGP, route reflection,
confederations, route-server mode, multihop, numbered/unnumbered peers, dynamic
neighbors, and VRF-scoped sessions. AFI/SAFI rows cover IPv4/IPv6 unicast and
multicast, labeled-unicast, VPNv4/VPNv6, EVPN, IPv4/IPv6 and VPN FlowSpec,
route-target constraints, MVPN, BGP-LS, and SR Policy. Negotiated capabilities,
security mechanisms, policy/attribute coverage, limits, and interop peers are
cross-products where semantics differ; a blanket family-level pass is invalid.

Provider configuration shall be generated deterministically from typed intent,
never accepted as an unbounded raw FRR/vtysh fragment. The implementation may
use only the management and observation interfaces admitted for the pinned FRR
build. Shell parsing, scraping human output as authority, inherited daemon
configuration, ambient sockets, and direct operator access to provider mutation
interfaces are denied.

The apply sequence is candidate validation, route-domain dependency validation,
keyring-use admission, provider syntax/semantic preflight, route-delta and peer-
reset preview, staged provider activation, session/family convergence,
candidate-route handoff to `bfw-routing`, native route and packet verification,
and commit. Failure or interruption before verified commit restores the prior
provider and canonical-route generation or enters a visible conservative
degraded state when rollback completeness cannot be proven.

The first implementation slice is IPv4/IPv6 unicast eBGP/iBGP in an isolated
lab with deny-default policy, no direct FIB mutation, typed candidate routes,
RPKI-state plumbing, bounded observations, restart/rollback, and independent
FRR/BIRD/GoBGP peers. That slice proves the boundary; it does not authorize a
universal-support claim. Later slices admit matrix rows independently.

### Routing-protocol suite implementation contract

The `bfw-routing` contract shall define one provider-neutral adjacency,
protocol database, candidate-route, withdrawal, redistribution, liveness,
selection, canonical-RIB, native-FIB, convergence, and observation vocabulary.
Provider adapters may add typed extensions but cannot replace common identity,
generation, bounds, failure, audit, or rollback fields with raw daemon text.

The machine-readable matrix shall include separate rows for BGP; OSPFv2/v3;
IS-IS; RIPv1/v2/RIPng; Babel; EIGRP; NHRP; IGMP/MLD/PIM-SM/SSM/DM/MSDP;
LDP/MPLS; SR-MPLS/SRv6; RSVP-TE; PCEP; and BFD, plus explicit unsupported rows
for named mesh, IoT, deprecated, and vendor protocols. Each row pins standards
interpretations, provider version/status, platform data-plane requirements,
authentication, topology, features, limits, interop peers, and admission.

Redistribution is represented as a directed graph whose edges name exact
source/destination protocols and families, match/set policy, metric mapping,
tag/provenance encoding, maximum route cardinality, loop-prevention rule,
withdrawal behavior, and generation. Static/connected origination uses the
same explicit edge model. An absent edge means deny.

Routing rollout proceeds protocol by protocol: isolated parser/model tests,
provider dry-run, independent-peer adjacency, candidate-route completeness,
canonical RIB/FIB application, packet oracle, restart/withdrawal, then bounded
multi-protocol redistribution. Alpha or legacy provider features remain
unsupported until their own hostile-input, failure, and interop evidence passes.

### Switching-protocol suite implementation contract

The `bfw-switching` component shall maintain a machine-readable matrix for:

- 802.1Q VLAN/access/trunk/native/translation, 802.1ad/Q-in-Q, MVRP/GVRP, and
  explicit vendor VTP compatibility
- STP/RSTP/MSTP and explicit PVST+/Rapid-PVST+ compatibility
- static LAG/LACP and separate MLAG/MC-LAG/ICCP/vendor multi-chassis profiles
- LLDP/LLDP-MED and separately identified vendor discovery protocols
- IGMP/MLD snooping, querier/proxy capability, MVR, and multicast bounds
- 802.1X/EAPOL, MAB, MACsec/MKA, DHCP snooping, DAI, IP Source Guard, RA Guard,
  and typed dependencies on identity/DHCP/firewall/keyring authorities
- VXLAN/GENEVE/NVGRE data planes with EVPN control delegated to routing/fabric
- SPB, TRILL, ERPS, REP, FabricPath, and other ring/fabric compatibility rows
- DCB/PFC/ETS/DCBX, TSN/gPTP/shaping/preemption/filtering, and QoS ownership
- 802.3ah, 802.1ag CFM, and Y.1731 OAM

Each row pins standard/dialect, provider/platform/hardware identity, topology,
frame/TLV semantics, timers, state machine, bounds, dependency effects,
observation completeness, interop fixtures, recovery, and admission. Provider
configuration fragments, vendor CLI, and hardware self-report are never the
canonical model.

The first broader switching slice remains the v0.1 Linux software baseline.
Every additional protocol row begins in an isolated namespace/lab with hostile
control frames and an independent control-frame/native-state/packet oracle.
Hardware and multi-chassis rows additionally require semantic-parity, fencing,
partition, upgrade, and rollback evidence before they can replace or augment a
software path.

### Sticky endpoint-binding implementation contract

The public model shall expose a discriminated `sticky_endpoint_binding` with
`switched` and `routed` variants. Common fields include binding identity,
configuration and participant generations, port/interface identity, enrollment
policy, endpoint identity/provenance, cardinality limit, violation profile,
created/confirmed/expiry times, state, last observation, and audit correlation.
Unknown fields or a variant missing a required scope fail validation.

The switched variant additionally requires bridge domain, VLAN/PVID, source
MAC, learning source, FDB class, and hardware/offload state. The routed variant
requires VRF, encapsulation/VLAN, address family, IP address or prefix, MAC when
the link supplies one, neighbor-evidence type/generation, and the exact
`bfw-network`, `bfw-routing`, and `bfw-firewall` enforcement participants.

Lifecycle is `observed -> pending -> admitted -> active`, with explicit
`violating`, `quarantined`, `stale`, `unsupported`, `clearing`, and `removed`
states. Learning never writes canonical configuration by itself. Promotion,
replacement, clearing, migration, and expiration require typed idempotent
requests and compare-and-swap generations. The default violation result is
drop plus bounded alert/audit; automatic relearn and permit-on-provider-error
are forbidden.

The first implementation slice uses Linux software bridge/nftables/netlink
fixtures with one switched access port and one routed Ethernet port. It covers
first observation, explicit admission, persistence, reboot, MAC/IP move,
duplicate endpoint, limit overflow, stale interface generation, LAG/VLAN
change, provider disagreement, clearing, and rollback before any hardware
offload or automatic-enrollment row is admitted.

### Alpine appliance and installer implementation contract

`bfw-installer` shall consume a release manifest containing the exact Alpine
release, repository snapshot and keys, APK package names/versions/digests,
kernel sources/packages, build toolchain, normalized inventory schema, signed
tailoring policy, generic recovery kernel/initramfs/environment, modules,
firmware, bootloader, architecture, Bifrost component artifacts, defaults,
filesystem layout, service identities, migrations, rollback mates, SBOM,
provenance, and builder identity. Media outputs are the ISO, boot/recovery
artifacts, checksums, signatures, SBOM, provenance, and reproducibility record.
Each installation additionally emits a content-addressed normalized machine
inventory, plan, selected APK/service/kernel/module/firmware manifest,
installed-file manifest, slot digest, and verification record.

The initial design/test target is Alpine Linux 3.24.1 on x86-64 with both UEFI
and legacy BIOS boot. That version is a starting pin, not admission: repository
snapshot, input, and ISO digests remain required. A later patch or stable-branch
migration changes the release composition and reruns the full image,
installation, boot, network, upgrade, and rollback matrix. Alpine edge is
rejected by schema and build policy.

The build runs in an isolated environment against content-addressed inputs;
network resolution during the reproducible phase is denied. The installer
state machine is `inspect-machine -> derive-tailored-plan -> inspect-disk ->
confirm-destruction -> stage -> verify -> activate-boot -> verify-first-boot`.
It normalizes CPU, boot, console, NIC, storage, virtualization, and firmware
facts, rejects incomplete, ambiguous, changed, or unsupported inventory, and
derives the plan only from signed policy. Target identity uses stable hardware
facts and revalidates immediately before the first write. Every destructive
stage is journaled sufficiently to distinguish untouched, resumable,
rollbackable, and manual-recovery outcomes after interruption.

The normal path selects only required signed APKs, services, firmware packages,
kernel flavor/modules, boot files, and Bifrost components and generates the
exact initramfs/module-load closure. It shall not delete or modify APK-owned
files to fake minimality. When prebuilt inputs cannot satisfy an admitted
profile, an explicit resource-estimated slow path may build only a custom
kernel/module layer from pinned sources/toolchain. Rebuilding all of Alpine on
the target is unsupported. The custom layer and generated manifest are
content-addressed and sealed, not falsely vendor-signed; the ISO contains no
release-signing private key.

The machine-tailored installed slot boots with no forwarding or management
exposure beyond the explicit bootstrap/recovery contract. It separates
replaceable system content from durable Bifrost configuration, audit/evidence,
and recovery state;
enforces the declared package/service set; and reports local package or
repository mutation as drift. Installer media and unattended inputs contain no
reusable secrets. A signed broad generic recovery kernel/initramfs/environment
remains separately bootable. Signed staged/A-B update rebuilds the inactive
slot against current verified inventory, performs bounded boot confirmation,
and preserves the last-known-good and recovery paths. Alpine support-lifecycle
checks and rollback reuse the canonical release/recovery transaction rather
than adding an installer-owned update path.

### FreeBSD appliance and installer implementation contract

The first BSD distribution target is a generic x86-64 FreeBSD live installation
ISO that produces a machine-tailored installed system. `bfw-installer` shall
consume an exact FreeBSD release/source revision, source/object sets,
`src.conf`, build toolchain, normalized inventory schema, signed tailoring
policy, generic recovery kernel/environment, module/firmware/boot manifests,
signed private-package repository snapshot, package names/versions/digests,
Bifrost artifacts, filesystem/slot layout, service identities, migrations,
rollback mates, hardware-matrix rows, SBOM, provenance, and builder identity.
Media outputs shall include the ISO, boot and recovery artifacts, checksums,
signatures, SBOM, provenance, and independent rebuild comparison. Each install
shall additionally produce a content-addressed machine inventory, build plan,
installed file manifest, slot digest, and verification record.

The build shall use supported source-build controls and a NanoBSD-style
appliance layout. The release manifest, not cleanup scripts, defines omissions.
A dependency-closure check shall prove that retained PF, routing, bridge/VLAN,
CARP/pfsync, IPsec, audit, crypto/signature, console/SSH recovery,
filesystem-repair, observability, firmware, and driver capabilities match each
admitted hardware row. Package installation shall come only from the pinned
signed repository produced in an isolated builder.

The live installer shall normalize CPU, boot, console, NIC, storage,
virtualization, and firmware facts, reject incomplete, ambiguous, changed, or
unsupported inventory, and derive the machine build plan deterministically
from the signed tailoring policy before confirmation or disk mutation. The
default path shall install pinned prebuilt base/object sets and packages and
build only machine-specific kernel/modules when required. Full on-target
`buildworld`/`buildkernel` is permitted only as an explicit resource-estimated
slow path using the same offline inputs. Neither path may fetch mutable inputs.

The primary kernel/module closure shall contain only the detected and required
hardware plus platform and recovery-independent runtime dependencies. A signed
generic recovery kernel/environment shall retain the admitted broad driver set,
remain separately verifiable, and be bootable without widening packet-policy
authority. The generated machine manifest is sealed into the installed slot
and durable evidence; the ISO shall contain no release-signing private key.

The installed system shall expose two independently verifiable code/root slots
or an admitted equivalent, keep replaceable system content read-only or
integrity verified, and separate durable configuration, audit/evidence, and
recovery state. Install and update use the canonical inspect, plan,
confirm-destruction, stage, verify, activate, boot-confirm, and rollback
transactions. Native in-place update success is not Bifrost admission evidence.

The generic live-media profile shall publish exact supported CPU, NIC, storage,
boot, console, virtualization, and firmware rows. Unknown hardware and hardware
changes that invalidate the sealed machine manifest fail before disk mutation
or activation. Upgrade rebuilds the inactive slot against the current verified
inventory and retains the last-known-good slot and generic recovery path.
Separately distributed prebuilt hardware-specific media and appliance SKUs are
outside this feature and require a distinct product profile and workflow.

## First learning-alpha vertical slice

The preferred first runtime slice is an offline, pure configuration validator
and platform-neutral policy compiler for a deliberately tiny firewall schema.
It includes a pure `bfw` grammar/parser slice that maps a small set of EXEC and
configuration commands into typed candidate edits and read actions. It must
produce one canonical IR plus deterministic golden output for the Linux
platform adapter without modifying the host network. A second adapter remains
a beta/stable requirement. Plugin execution, daemonization, designated host
mutation, installer execution, and web administration remain later alpha
slices and cannot cross the specific `BFW-ALPHA-0` effect gate that applies.

## Requirement-to-verification map

| Requirement | Planned verification |
| --- | --- |
| BFW-PRD-000 | naming lint for full name Bifrost, `BFW` firewall shorthand, `bfw` public namespace, and absence of competing shorthand |
| BFW-PRD-001 | canonical IR golden tests plus per-platform compiler and isolated apply/oracle tests |
| BFW-PRD-002 | schema, migration, audit, and rollback tests |
| BFW-PRD-003 | partial-failure and last-known-good recovery tests |
| BFW-PRD-004 | authorization, exposure, confirmation-timer, and console-recovery tests |
| BFW-PRD-005 | adapter contracts, integration tests, and health-state tests |
| BFW-PRD-006 | signature, preflight, interruption, and rollback tests |
| BFW-PRD-007 | secret-storage, export, logging, and redaction tests |
| BFW-PRD-008 | pinned build and integration matrix |
| BFW-PRD-009 | process isolation, generation, authority-boundary, and failure-isolation tests |
| BFW-PRD-010 | signature, provenance, permission, migration, activation, and rollback tests |
| BFW-PRD-011 | protocol negotiation and backward/forward compatibility matrix |
| BFW-PRD-012 | crash/restart/upgrade tests proving last-known-good policy remains active |
| BFW-PRD-013 | alpha/Phase-0 channel separation plus cross-platform beta/stable substrate admission record and independent review |
| BFW-PRD-014 | secret-location scan plus configuration, database, log, export, UI, plugin, and support-bundle redaction tests |
| BFW-PRD-015 | negative tests proving no credential or caller identity bypasses core action admission |
| BFW-PRD-016 | lease/ref scope, generation, target, audience, expiry, and raw-export-denied tests |
| BFW-PRD-017 | rotation, revocation, restore, restart, policy-change, and stale-generation invalidation tests |
| BFW-PRD-018 | cross-platform keyring compatibility, storage/unlock, recovery, SDK, and independent admission record |
| BFW-PRD-019 | filesystem scope, path, bounds, link/special-file, mutation-precondition, generation, expiry, and audit tests |
| BFW-PRD-020 | secret/provider-state denial plus destructive-class and recoverability tests |
| BFW-PRD-021 | complete process-envelope validation and negative spawn tests |
| BFW-PRD-022 | shell, PATH/env, credential, network, privilege, raw-handle denial and native-API boundary tests |
| BFW-PRD-023 | cross-provider confused-deputy, stale-generation, type/bounds, ref-reuse, and correlation tests |
| BFW-PRD-024 | cross-platform filesystem/exec compatibility, safety, lifecycle, SDK, and independent admission record |
| BFW-PRD-025 | privilege, direct-access, restart-isolation, and shared-core-API tests for web and CLI clients |
| BFW-PRD-026 | signed UI-manifest schema, compatibility, namespace, permission, localization, and asset-digest tests |
| BFW-PRD-027 | provenance/schema/migration/asset verification plus sanitized authorization-filtered catalog tests |
| BFW-PRD-028 | declarative form/table/status/validation/confirmation/accessibility/error golden tests |
| BFW-PRD-029 | typed-action admission, identity, confirmation, audit, idempotency, generation, and rollback tests |
| BFW-PRD-030 | hostile custom-bundle tests for origin, CSP, cookie/token, DOM, network, filesystem, socket, and capability escape |
| BFW-PRD-031 | staged activation, crash interruption, version skew, cache integrity, atomic publish, and rollback tests |
| BFW-PRD-032 | disabled/removed/incompatible/untrusted route denial and unhealthy read-only diagnostic tests |
| BFW-PRD-033 | web-down local CLI recovery tests proving the same core admission path is used |
| BFW-PRD-034 | web/UI crash, restart, and upgrade tests proving packet policy and core authority remain intact |
| BFW-PRD-035 | repository-content and release-governance checks proving the meta repo contains no product runtime |
| BFW-PRD-036 | component ownership, immutable pin, no-source-copy, and independent-versioning checks |
| BFW-PRD-037 | routing ownership tests proving no routing implementation or domain policy resides in core |
| BFW-PRD-038 | routing plan determinism, admission, idempotency, platform apply/oracle, boundary, and rollback tests |
| BFW-PRD-039 | signed release composition, exact revision, compatibility, migration-order, evidence, and rollback-pair checks |
| BFW-PRD-040 | generic OIDC conformance plus Authentik integration tests without provider-specific authority |
| BFW-PRD-041 | authorization-code/PKCE, redirect, TLS, state, nonce, and bounded-transaction tests |
| BFW-PRD-042 | hostile issuer/JWKS/algorithm/audience/azp/nonce/time/assurance and key-rotation tests |
| BFW-PRD-043 | issuer-subject role mapping, deny-default, claim-change, and no-auto-admin tests |
| BFW-PRD-044 | keyring mediation and secret/token absence scans across config, env, argv, logs, exports, browser, UI, and plugin surfaces |
| BFW-PRD-045 | opaque-cookie, Secure/HttpOnly/SameSite, rotation, inactivity, absolute-expiry, logout, and CSRF tests |
| BFW-PRD-046 | plugin-boundary tests proving no raw OIDC token or provider session crosses the core |
| BFW-PRD-047 | issuer/client/origin/algorithm/claim/assurance pinning and forwarded-header denial tests |
| BFW-PRD-048 | provider/JWKS outage tests for new-login denial and bounded existing-session behavior |
| BFW-PRD-049 | isolated local-console recovery and no-remote-fallback tests during identity/network failures |
| BFW-PRD-050 | redacted authentication, mapping, session, logout, denial, recovery, and policy-change audit tests |
| BFW-PRD-051 | catalog schema, ownership, dependency/conflict, platform, permission, health, UI, migration/rollback, and no-authority-by-presence checks |
| BFW-PRD-052 | firewall/network/switching/routing ownership and atomic cross-domain transaction tests |
| BFW-PRD-053 | per-service configuration/status/platform/UI/failure/rollback contract suites |
| BFW-PRD-054 | WireGuard site-to-site and per-device remote-access contract plus generic VPN compatibility tests |
| BFW-PRD-055 | unique-device identity, keyring-only secret, one-time delivery, expiry, revocation, and no-key-sharing tests |
| BFW-PRD-056 | AllowedIPs, overlap, loop, reachability, MTU, firewall/NAT, kill-switch, failover, partial-activation, and rollback tests |
| BFW-PRD-057 | native reverse-proxy HTTP/TLS/route/upstream/health/limit/UI/apply/verify/rollback tests plus absence of a Caddy runtime/config/API dependency |
| BFW-PRD-058 | proxy authority-denial, keyring, DNS/ACME/firewall dependency, header stripping, and forwarded-identity trust tests |
| BFW-PRD-059 | native HA membership, VRRP/CARP/platform mechanism, virtual-address, synchronization, failover, interoperability, recovery, UI, and audit tests plus absence of a Keepalived runtime/config/API dependency |
| BFW-PRD-060 | HA peer identity, release/config compatibility, quorum/fencing, stale-state, duplicate-owner, split-brain, ordering, and rollback tests |
| BFW-PRD-061 | advanced-network plugin ownership, coordination, and no-authority-collapse tests |
| BFW-PRD-062 | security/access ownership tests plus default-disabled and bounded UPnP/NAT-PMP/PCP tests |
| BFW-PRD-063 | operations-plugin redaction, destination, retention, signature, recovery, and external-side-effect tests |
| BFW-PRD-064 | typed dependency version/admission tests and missing/unhealthy/incompatible dependency mutation denial |
| BFW-PRD-065 | exact platform matrix, semantic-gap, unsupported-feature, and explicitly admitted degraded-mode tests |
| BFW-PRD-066 | meta-planning dependency-order and change-admission checks |
| BFW-PRD-067 | signed UI contribution, typed action, and no-secondary-management-plane tests for every managed plugin |
| BFW-PRD-068 | provider scope, generation, confused-deputy, privilege, secret, path, process, and network non-expansion tests |
| BFW-PRD-069 | modal grammar and prompt golden tests for EXEC, global configuration, and domain submodes |
| BFW-PRD-070 | role, step-up, mode-transition, shared-password-denial, and no-authority-expansion tests |
| BFW-PRD-071 | contextual help, completion, unambiguous-interactive-abbreviation, canonical-script, and structured-output compatibility tests |
| BFW-PRD-072 | parser-to-typed-action golden and fuzz tests plus shell, file, plugin-socket, and direct-mutation denial tests |
| BFW-PRD-073 | candidate ownership, base-generation, expiry, disconnect, authorization-change, and audit-correlation tests |
| BFW-PRD-074 | diff, validation, commit, commit-confirmed timeout, conflict, failure, verification, and rollback tests |
| BFW-PRD-075 | authorization-filtered show views, stable structured output, deterministic rendering, and no-second-authority tests |
| BFW-PRD-076 | no/default grammar, schema derivation, absence/deletion/inheritance/default distinction, and round-trip tests |
| BFW-PRD-077 | signed declarative plugin grammar, namespace, compatibility, typed-binding, parser-code, shell-escape, and secondary-plane tests |
| BFW-PRD-078 | secret-input history exclusion plus completion, diagnostic, output, audit, support-bundle, and recovery redaction tests |
| BFW-PRD-079 | component/release schema, complete-field, immutable-admitted-pin, dependency, platform, migration/rollback, and evidence-hash validation |
| BFW-PRD-080 | exact PRD/trace/verification ID-set equality plus owner, state, blocker, command, evidence, and admission-field validation |
| BFW-PRD-081 | JSON Schema parse, identifier/version, strict-object, reference, representative-valid, and representative-invalid fixture tests |
| BFW-PRD-082 | pinned dependency revision, required/passed gate, gap, evidence, review, admission, and fail-closed runtime-start checks |
| BFW-PRD-083 | ADR filename/id/status/index, requirement-link, supersession, and accepted-decision consistency checks |
| BFW-PRD-084 | threat inventory, trust-boundary, requirement, mitigation, verification, and residual-risk trace review |
| BFW-PRD-085 | transaction phase/state-machine, participant, generation, idempotency, partial-failure, verification, rollback, and recovery model tests |
| BFW-PRD-086 | clean-checkout Forgejo CI execution of governance validation, generated-view checks, secret scanning, and diff hygiene |
| BFW-PRD-087 | exact included/deferred partition, dependency closure, platform profile, and no-unplanned-MVP-component checks |
| BFW-PRD-088 | required component-template set, placeholder, authority-boundary, evidence, and independent-review checks |
| BFW-PRD-089 | signed-artifact, SBOM/provenance, reproducibility, staged activation, interruption, migration, console rollback, and last-known-good exercises |
| BFW-PRD-090 | pinned image/topology, isolation, role-count, scenario, packet/state oracle, platform, upgrade, HA, split-brain, and recovery evidence checks |
| BFW-PRD-091 | product-profile and end-to-end tests proving one appliance supports admitted Layer-2 switching and Layer-3 routing/firewall roles |
| BFW-PRD-092 | ownership tests proving switching, network, routing, and firewall plans cannot mutate one another's domains directly |
| BFW-PRD-093 | VLAN, bridge, FDB, STP-family, LACP, isolation, storm-control, snooping, and LLDP contract/conformance suites |
| BFW-PRD-094 | loop, VLAN leakage, duplicate membership, uncertain-STP, unsupported-feature, and last-known-good negative tests |
| BFW-PRD-095 | atomic cross-domain port/switching/routing/firewall/DHCP transaction, ordering, failure, and rollback tests |
| BFW-PRD-096 | platform semantic-gap matrix plus Linux, FreeBSD, Windows, and separately admitted offload adapter conformance tests |
| BFW-PRD-097 | observed-state authorization, bounds, FDB, VLAN, STP, LACP, counter, offload, health, and drift tests |
| BFW-PRD-098 | management-VLAN/uplink commit-confirmed timeout, local/OOB recovery, verification-failure, and automatic rollback tests |
| BFW-PRD-099 | exact v0.1 composition and Linux software-switch baseline tests with hardware-offload admission kept optional |
| BFW-PRD-100 | exact router/switch/converged profile identifiers, shared-management-plane, and no-edition-fork checks |
| BFW-PRD-101 | router-profile component closure plus user-traffic Layer-2 switching disabled/absent tests |
| BFW-PRD-102 | switch-profile Layer-2 forwarding plus Layer-3 transit and NAT deny-default tests with bounded management addressing |
| BFW-PRD-103 | converged inter-VLAN, routed-port, SVI, firewall, DHCP, reachability, and atomic transaction tests |
| BFW-PRD-104 | role-transition preflight, commit-confirmed, management-loss, partial-apply, restart, and last-known-good rollback tests |
| BFW-PRD-105 | catalog/profile/platform capability negotiation, unsupported-required-feature denial, and no-v0.1-overclaim checks |
| BFW-PRD-106 | Layer-2 VLAN/FDB/STP/LACP plus SVI, routed-switchport, inter-VLAN, and local-fabric Layer-3 switching tests |
| BFW-PRD-107 | switch-profile WAN-edge/NAT denial and management-interface non-transit tests with routing-plan ownership checks |
| BFW-PRD-108 | Layer-3 forwarding plus TCP/UDP state, NAT, port-forward, connection-state, and transport-steering router tests |
| BFW-PRD-109 | routing/firewall ownership tests plus negative Layer-7 proxy, TLS, payload-inspection, and identity-policy implication checks |
| BFW-PRD-110 | declared-layer capability negotiation, partial-observation rejection, and last-known-good preservation tests |
| BFW-PRD-111 | build/dependency/source scans plus provenance review proving no Snort runtime, executable, copied source, or private implementation dependency |
| BFW-PRD-112 | passive/inline mode, capture-point identity, no-implicit-prevention, activation, and authorization tests |
| BFW-PRD-113 | fragment/TCP reassembly, flow direction/state, decoder, content/regex, threshold/suppression, checksum/overlap/truncation, and evasion corpus tests |
| BFW-PRD-114 | canonical-rule determinism plus versioned Snort-dialect accepted/rejected keyword, action, preprocessor, PCRE, and ambiguity fixtures |
| BFW-PRD-115 | CPU/memory/byte/depth/time/cardinality/retention boundary and incomplete-inspection reporting tests |
| BFW-PRD-116 | signature/provenance/digest/compatibility/expiry, deterministic compile, atomic activation, interruption, and rollback tests |
| BFW-PRD-117 | alert schema, stable flow/capture identity, truncation fact, payload/PCAP deny-default, access, redaction, retention, and audit tests |
| BFW-PRD-118 | confused-deputy and direct-mutation denial plus core/firewall typed enforcement transaction tests |
| BFW-PRD-119 | inline fail-open/fail-closed, bypass, backlog, overload, watchdog, health, confirmation, restart, and recovery tests |
| BFW-PRD-120 | per-platform timestamp/checksum/offload/VLAN/multi-queue/zero-copy/injection/loss/ordering semantic and completeness tests |
| BFW-PRD-121 | canonical/differential corpora, fuzz, race, restart, upgrade, rollback, loss, overload, latency, throughput, CPU, memory, and allocation evidence |
| BFW-PRD-122 | compatibility-matrix and documentation checks rejecting unqualified parity or endorsement claims |
| BFW-PRD-123 | router/switch/converged crossed with standalone/fabric profile validation and shared-management-authority tests |
| BFW-PRD-124 | fabric versus switching/routing/firewall ownership and no-direct-domain-mutation tests |
| BFW-PRD-125 | node enrollment/revocation, cryptographic identity, liveness/generation, release/schema/capability, role, and encrypted-channel tests |
| BFW-PRD-126 | quorum, leader/term, fencing, minority, stale generation, journal/restart, idempotency, and split-brain tests |
| BFW-PRD-127 | overlay/VNI, EVPN-class MAC/IP, split-horizon, designated-forwarder, BUM, ARP/ND suppression, mobility, duplication, and aging tests |
| BFW-PRD-128 | VRF, routed-VNI, anycast-gateway, ECMP, route-target, route-leak, next-hop, dynamic-protocol, and convergence tests |
| BFW-PRD-129 | deterministic distributed-policy placement, endpoint mobility, zone identity, asymmetric/symmetric flow, steering, state owner/replication/failover/staleness tests |
| BFW-PRD-130 | partition, node/control loss, reorder/delay, loop, duplicate endpoint, route conflict, placement gap, and incomplete-observation safety tests |
| BFW-PRD-131 | encapsulation MTU/PMTU, fragmentation, QoS/ECN, hash entropy, loop/BUM, and software/hardware-offload parity tests |
| BFW-PRD-132 | staged dependency/failure-domain rollout, readiness barrier, canary, node/end-to-end oracle, deadline, interruption, island, and rollback tests |
| BFW-PRD-133 | fail-static/isolate/open/closed traffic-class policy, time bound, audit, stricter-local-floor, and control-loss tests |
| BFW-PRD-134 | authorized topology/membership/term/generation/peer/MAC/IP/route/policy/state/loss/convergence/drift/rollback observation tests |
| BFW-PRD-135 | three-node multi-failure-domain partition/mobility/churn/ECMP/upgrade/rollback/scale/resource/performance admission matrix |
| BFW-PRD-136 | first-party Kubernetes-managed scope, shared-authority, inventory, intent, rollout, observation, and no-edition-fork tests |
| BFW-PRD-137 | single-controller non-HA labeling plus odd three-or-more controller quorum and failure-domain validation |
| BFW-PRD-138 | API/scheduler/CNI/service/overlay/storage outage tests proving forwarding, fast failover, and local recovery independence |
| BFW-PRD-139 | native-agent identity, signed-service, no-worker-membership, and no-container-runtime dependency tests |
| BFW-PRD-140 | controller-loss mutation freeze plus last-known-good, BFD, EVPN/routing, ECMP, gateway, and firewall-state continuity tests |
| BFW-PRD-141 | mutual-authentication, authorization, signature, generation, expiry, idempotency, readiness, verification, audit, and rollback tests |
| BFW-PRD-142 | dedicated/OOB management path, shared-path risk admission, commit-confirmed, bootstrap, rebuild, and local-recovery tests |
| BFW-PRD-143 | pinned Kubernetes/K3s/runtime/CNI/storage/image/manifest/CRD/API/RBAC/NetworkPolicy/Pod-Security/provenance compatibility matrix |
| BFW-PRD-144 | quorum/member/total-control/API/etcd/CNI/storage/partition/replay/restart/rebuild/upgrade/rollback/secret/autonomy admission matrix |
| BFW-PRD-145 | clean-room provenance, license/source/dependency/build scan, product-name, and no-Keepalived-runtime tests |
| BFW-PRD-146 | VRRPv2/v3 IPv4/IPv6 election, priority, timer, owner, preemption, multicast/unicast, and malformed-protocol tests |
| BFW-PRD-147 | typed effect-plan ownership, authorization, generation, verification, rollback, and direct-mutation denial tests |
| BFW-PRD-148 | typed health interval/timeout/rise/fall/weight/freshness/incomplete-state tests plus shell/env/process denial |
| BFW-PRD-149 | duplicate-owner, split-brain, replay, stale generation, ambiguity, timer/clock, partial transition, restart, fencing, and last-known-good tests |
| BFW-PRD-150 | exact Keepalived-dialect accepted/rejected directive, script/hook, IPVS, order, and ambiguity fixture tests |
| BFW-PRD-151 | Linux VRRP/netlink, FreeBSD CARP, unsupported-platform, semantic-gap, and parity admission tests |
| BFW-PRD-152 | bounded authorized instance/role/peer/timer/health/generation/transition/degraded/rollback observation and leakage tests |
| BFW-PRD-153 | provenance, conformance, interop, deterministic state machine, packet corpus/fuzz/race/endurance, platform, upgrade, and performance matrix |
| BFW-PRD-154 | exact two-profile identifier, first-party packaging, no-third-party-addon, and catalog checks |
| BFW-PRD-155 | canonical config/core/CLI/web/API/audit/transaction/release/recovery parity tests across both profiles |
| BFW-PRD-156 | GoKA-native no-external-orchestrator, peer coordination, election, health, fencing, and failover tests |
| BFW-PRD-157 | Kubernetes controller/chart/manifest/CRD/policy/compatibility packaging and admitted-substrate tests |
| BFW-PRD-158 | single coordinator ownership, no competing writer, native fast-failover preservation, and composition tests |
| BFW-PRD-159 | profile selection/migration preflight, commit-confirmed, handoff, continuity/isolation, verification, and rollback tests |
| BFW-PRD-160 | packaged/configured/controller/forwarding/degraded/unsupported/admitted capability-state tests |
| BFW-PRD-161 | release composition, recovery assets, cross-profile migration, failure matrix, semantic parity, and no-v0.1-overclaim checks |
| BFW-PRD-162 | process/route/interface/credential/authorization boundary and direct-FIB-mutation denial tests |
| BFW-PRD-163 | machine-readable exact-build capability matrix completeness, cross-product, unsupported/partial, and no-boolean-overclaim checks |
| BFW-PRD-164 | eBGP/iBGP, reflector, confederation, route-server, multihop, numbered/unnumbered, dynamic-neighbor, peer-group, VRF, and per-family tests |
| BFW-PRD-165 | independent AFI/SAFI conformance, isolation, unsupported-provider, semantic-gap, route import/export, and withdrawal tests |
| BFW-PRD-166 | capability negotiation, mismatch, downgrade, refresh, restart, Add-Path, extended-next-hop/message, label, and Roles/OTC tests |
| BFW-PRD-167 | typed import/export policy ordering, matching/setting, default-deny, ambiguity rejection, attribute/community, and deterministic replay tests |
| BFW-PRD-168 | peer binding, GTSM, limit, MD5/AO keyring, RPKI, ASPA, BGPsec, Roles/OTC, bogon/own-route, outage, and secret-leakage tests |
| BFW-PRD-169 | BFD, graceful shutdown/restart/LLGR, stale/EOR, dampening, advertisement, Add-Path withdrawal, next-hop, ECMP, and restart tests |
| BFW-PRD-170 | reproducible best-path/multipath/reflection/confederation/route-server/VPN/EVPN/FlowSpec decision and rejection-reason tests |
| BFW-PRD-171 | candidate/preflight/preview/apply/converge/confirm/reconcile/interruption/rollback and management-lockout tests |
| BFW-PRD-172 | bounded peer/RIB/policy/validation/convergence/drift telemetry plus authorized BMP/MRT destination, retention, and redaction tests |
| BFW-PRD-173 | CLI/web typed-action, authorization, visibility, preview, clear/refresh, confirmation, rollback, degradation, and direct-provider denial tests |
| BFW-PRD-174 | malformed-message corpus/fuzz, leak/hijack/churn/partition, cardinality/byte/rate/queue/CPU/memory/time bounds, scale, and endurance evidence |
| BFW-PRD-175 | pinned-RFC interpretation and FRR/BIRD/GoBGP/vendor interop matrix plus unsupported/partial/experimental disclosure and claim lint |
| BFW-PRD-176 | provider-neutral route model, admitted-provider boundary, exact suite matrix, alternate-provider isolation, and unsupported-row tests |
| BFW-PRD-177 | OSPFv2/v3 area/network/election/LSA/SPF/external/auth/GR/TE/SR conformance, fuzz, scale, restart, and interop tests |
| BFW-PRD-178 | IS-IS level/adjacency/DIS/area/metric/topology/auth/overload/leak/GR/TE/SR TLV, fuzz, scale, restart, and interop tests |
| BFW-PRD-179 | RIP v1/v2/RIPng, Babel, EIGRP, NHRP exact feature/status, legacy/alpha deny-default, auth, malformed-input, convergence, and interop tests |
| BFW-PRD-180 | IGMP/MLD/PIM/MSDP RP/RPF/join/prune/register/assert/source-group/boundary/state-limit and Layer-2 ownership tests |
| BFW-PRD-181 | LDP/targeted-LDP/MPLS/BGP-label/SR-MPLS/SRv6/RSVP-TE/PCEP capability, label/SID/path authority, platform, and unsupported-row tests |
| BFW-PRD-182 | shared BFD ownership, mode/timer/auth/discriminator/generation/bounds/dampening/duplicate-session and consumer-race tests |
| BFW-PRD-183 | deny-default directed redistribution graph, metric/tag/provenance/loop/cardinality/withdrawal/preview and all-enabled-pair tests |
| BFW-PRD-184 | adjacency identity/interface/VRF/family/capability/timer/limit/generation/keyring and trust-outage tests |
| BFW-PRD-185 | cross-protocol adjacency/SPF/vector/path/recursion/preference/ECMP/BFD/GR/stale/FIB/rollback convergence and completeness tests |
| BFW-PRD-186 | bounded typed CLI/web/API/audit protocol database/RIB/decision/timer/auth/redistribution/drift and raw-provider-authority denial tests |
| BFW-PRD-187 | pinned provider/platform/standard interop, malformed corpus/fuzz, topology/partition/restart/upgrade, loop/leak, scale/resource, FIB, and packet evidence |
| BFW-PRD-188 | deprecated/experimental/alpha/proprietary/unavailable named-row denial, semantic-gap, provider-boundary, and support-claim tests |
| BFW-PRD-189 | release-composition protocol-row and redistribution-cross-product completeness, recovery, failure-matrix, and branding-inference denial tests |
| BFW-PRD-190 | switching matrix completeness across standard/dialect/provider/platform/hardware/role/topology/limit/interop/admission states and no-device-name inference |
| BFW-PRD-191 | 802.1Q/access/trunk/native/PVID/priority/allow/translation/Q-in-Q/MVRP/GVRP/VTP semantics, isolation, malformed-frame, and interop tests |
| BFW-PRD-192 | STP/RSTP/MSTP/PVST dialect, region/root/cost/role/state/timer/topology/BPDU/edge/guard, loop, restart, and interop tests |
| BFW-PRD-193 | static-LAG/LACP actor/partner/key/state/timer/selection/min-links/hash/churn/fallback plus MLAG/ICCP/vendor fencing/split-brain tests |
| BFW-PRD-194 | LLDP/LLDP-MED and vendor-discovery TLV/dialect/bounds/age/identity/address-filter/untrusted-input/interoperability tests |
| BFW-PRD-195 | IGMP/MLD snooping/querier/proxy/router-port/fast-leave/unknown-multicast/MVR/group-source-limit/aging and L3-ownership tests |
| BFW-PRD-196 | 802.1X/EAPOL/MAB/VLAN-ACL/MACsec-MKA/DHCP-snooping/DAI/IPSG/RA-Guard dependency, secret, bypass, failure, and port-isolation tests |
| BFW-PRD-197 | VXLAN/GENEVE/NVGRE VTEP/VNI/split-horizon/BUM/ARP-ND/mobility/duplication/MTU plus EVPN authority and tenant-isolation tests |
| BFW-PRD-198 | SPB/TRILL/ERPS/REP/FabricPath/ring/stack/fabric exact-status, no-weak-emulation, loop/partition/recovery, and vendor-interop tests |
| BFW-PRD-199 | 802.1p/PFC/ETS/DCBX/congestion/802.1AS/Qav/Qbv/Qbu/Qci/Qcc timing/queue/resource/QoS-boundary and semantic-gap tests |
| BFW-PRD-200 | 802.3ah/802.1ag/Y.1731 domain/association/endpoint/CCM/loopback/linktrace/loss/delay/rate and diagnostic-authority tests |
| BFW-PRD-201 | topology/preflight/management-path/stage/converge/control-frame/native/packet/confirm/interruption/rollback and lockout/loop tests |
| BFW-PRD-202 | bounded bridge/VLAN/port/protocol/LAG/discovery/multicast/security/overlay/OAM/offload/convergence/drift UI and completeness tests |
| BFW-PRD-203 | dialect/platform/hardware/peer malformed-control fuzz, loop/storm/partition/churn/leakage/rollback/scale/resource and honest-claim matrix |
| BFW-PRD-204 | router/switch/converged sticky-binding variant, role-boundary, sticky-flow-confusion, and unsupported-link tests |
| BFW-PRD-205 | switched port-generation/bridge/VLAN/MAC enrollment, persistence, limits, static/FDB/LAG/overlay/offload conflict tests |
| BFW-PRD-206 | routed interface-generation/VRF/encapsulation/AF/MAC/IP ARP/NDP/DHCP evidence and cross-domain enforcement tests |
| BFW-PRD-207 | unknown/excess/move/duplicate/stale/spoof/provider-disagreement drop, alarm, restrict/quarantine/disable, and no-relearn tests |
| BFW-PRD-208 | typed lifecycle, CAS/idempotency, observation/UI/audit, reboot/upgrade/failover/recreation/migration/rollback tests |
| BFW-PRD-209 | Alpine stable live-media baseline, exact APK/kernel/toolchain/inventory/tailoring/recovery/hardware-matrix/ISO pins, edge and moving-input denial tests |
| BFW-PRD-210 | separately versioned installer, content-addressed offline inputs, reproducible live ISO/recovery, signature/SBOM/provenance, no release private key, and no-policy-authority tests |
| BFW-PRD-211 | normalized machine inventory/plan, x86-64 UEFI/BIOS, offline install, stable disk identity, exact confirmation, and installer secret-leakage tests |
| BFW-PRD-212 | exact APK/service/kernel/initramfs/module/firmware closure, APK ownership, custom-layer bounds, recovery boot, system/state separation, least privilege, fail-closed startup, and drift tests |
| BFW-PRD-213 | inventory-aware inactive-slot rebuild, signed activation, boot confirmation, migration, Alpine lifecycle, last-known-good, and console-recovery tests |
| BFW-PRD-214 | reproducible media/plan, inventory change, closure, recovery boot, media/DB corruption, destructive-stage interruption/power loss, hardware rejection, install/upgrade/rollback/recovery/resource and packet-state oracle matrix |
| BFW-PRD-215 | separately signed development/alpha/beta/stable metadata, no-auto-promotion, and cross-channel replay/relabel denial tests |
| BFW-PRD-216 | exact first-alpha scope manifest, unsupported-capability denial, single-node/software-data-plane, and published-limit tests |
| BFW-PRD-217 | source/offline permission plus host-network, installer-disk, and distribution effect-gate negative tests |
| BFW-PRD-218 | rpc-plugin-system v2 and Linux dependency pin, identity/liveness/generation/bounds/teardown, and no-local-fork tests |
| BFW-PRD-219 | wrong-disk, unintended-traffic, credential-leak, config-corruption, stale-authority, and unknown-success alpha disqualifier tests |
| BFW-PRD-220 | bounded decision telemetry, provenance, redaction, known-limit, reset/recovery, and decision-log completeness tests |
| BFW-PRD-221 | alpha-evidence non-promotion plus full Phase 0, B+ threshold, P0/P1, install/upgrade/rollback/recovery, and cold-review beta tests |
| BFW-PRD-222 | per-dependency A/A+ evidence and independent-admission enforcement, no averaging/inheritance/demo substitution, and out-of-alpha implementation denial tests |
| BFW-PRD-223 | exact supported FreeBSD release/source/package/kernel/module/firmware/boot/architecture/image pins and generic-profile claim tests |
| BFW-PRD-224 | supported source-build/NanoBSD-style composition, isolated reproducibility, signature/SBOM/provenance, and installer-authority tests |
| BFW-PRD-225 | generic x86-64 UEFI/BIOS matrix, offline install, stable disk identity, exact confirmation, unknown-hardware denial, and appliance-specific-profile exclusion tests |
| BFW-PRD-226 | `src.conf`/kernel/package manifest closure, required capability retention, private-repository signature, and manual-deletion drift tests |
| BFW-PRD-227 | read-only system, dual-slot activation, durable-state separation, boot confirmation, migration, rollback, and recovery tests |
| BFW-PRD-228 | independent FreeBSD build/install/update/recovery plus PF/routing/bridge/CARP/FRR/native-state/packet and cross-platform non-inheritance tests |
| BFW-PRD-229 | Repository identity, preserved history and BFW namespaces; canonical/private versus public-mirror parity and private-reporting checks |
| BFW-PRD-230 | Source-backed reuse matrix, exact dependency/license/API selection, consumer compatibility and upgrade/rollback evidence |
| BFW-PRD-231 | Single-supervisor lifecycle mapping, keyring/filesystem/exec boundaries, stale-generation and unauthorized-effect denial tests |
| BFW-PRD-232 | No-JS server-rendered management, progressive-enhancement parity, scoped Stack API and absence of direct privileged mutations |
| BFW-PRD-233 | Remote service/database/identity loss with retained forwarding, commit-confirmed rollback and console recovery; bounded retry/cancellation tests |
| BFW-PRD-234 | Placeholder-versus-implementation checks, immutable consumer evidence and unchanged alpha/Phase 0 gates; independent review |
| BFW-PRD-235 | Local/off-box profile, runnable-service/library distinction and unsupported-placement tests |
| BFW-PRD-236 | Artifact/lifecycle/host/secret scopes, quotas, headroom, saturation and rollback tests |
| BFW-PRD-237 | Caddy UI no-JS/API parity, approved route preview/apply/verify/rollback and native-proxy separation |
| BFW-PRD-238 | Single-writer fencing, ownership/revocation, listener conflict, SSRF/rebinding/header/TLS and Admin API denial tests |
| BFW-PRD-239 | Service/dependency outage, restart persistence, unknown outcome, expiry and packet/console recovery tests |
| BFW-PRD-240 | Keyring/Caddy custody, immutable profile/resource/performance evidence and unchanged release/safety gates |
