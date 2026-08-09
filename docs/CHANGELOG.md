# Changelog

## Unreleased

### 2026-08-09 01:54–02:30 CDT — Add a bounded Linux learning-alpha path

Affected files:

- `README.md`
- `documents/`
- `governance/`
- `tools/`
- `workflow/features/linux-learning-alpha-v1/`

Explanation:

Split early source implementation and offline simulation from destructive or
externally consumable effects. Add `BFW-ALPHA-0` for a single-node Alpine Linux
x86-64 learning appliance using `rpc-plugin-system` v2 and Linux-compatible
authority providers. The alpha is allowed to be incomplete, rough, slow, and
reset-oriented, but wrong-disk selection, unintended packet exposure, reusable
secret leakage, silent configuration corruption, stale authority, and
unknown-as-success remain disqualifying. Keep full cross-platform Phase 0
mandatory for beta and stable, with no automatic or evidentiary promotion from
alpha. Require every Phase 0 dependency to earn its own A or A+ admission
before any implementation outside the exact alpha scope begins; aggregate
grades and successful demos cannot hide a weak substrate.

Verification completed locally:

- `python3 tools/governance.py render --check`
- `python3 tools/governance.py validate`
- `python3 -m unittest discover -s tools/tests -v` (31 tests)
- `git diff --check`

Risks / non-goals:

- The alpha gate is currently blocked: no v2 runtime or provider release is
  selected, and no host, disk, distribution, release, or deployment authority
  is granted.
- No runtime implementation, ISO build, package fetch, process launch, release,
  or deployment is performed.

### 2026-08-09 01:08–01:40 CDT — Define network suites, sticky ports, and Alpine Linux appliance distribution

Affected files:

- `README.md`
- `components/README.md`
- `documents/`
- `governance/`
- `workflow.toml`
- `workflow/`
- `workflow.events.jsonl`

Explanation:

Replace vague dynamic-routing and broad switching language with explicit,
matrix-defined routing and switching protocol suites. BGP remains owned by
`bfw-frr` behind the typed `bfw-routing` authority boundary. Add OSPF, IS-IS,
RIP/RIPng, Babel, multicast, MPLS/SR/TE, BFD, redistribution, VLAN/provider
bridging, STP-family, aggregation/multi-chassis, discovery, snooping, access/
link security, overlays, resilient fabrics, DCB/TSN, and OAM contracts. Define
capability, security, convergence, lifecycle, observability, scale, resource,
interoperability, threat, and isolated-lab behavior without claiming runtime
support. Add distinct persistent sticky endpoint bindings for switched
MAC/port/VLAN and routed interface/VRF/MAC/IP identities, with drop-and-alarm
violations and no silent relearning. Establish Alpine Linux as the canonical
first-party Linux appliance and installer-ISO base, add the deferred
`bfw-installer` component, define an Alpine 3.24 stable/x86-64 starting target,
and require exact immutable release inputs, reproducible signed offline media,
stable target-disk confirmation, first-boot verification, and recovery.

Verification completed before commit:

- `python tools/governance.py validate`
- `python tools/governance.py render --check`
- `python -m unittest discover -s tools/tests -v`
- `git diff --check`

Risks / non-goals:

- Dynamic routing and expanded switching remain deferred outside v0.1; no
  protocol process, peer session, route/switch mutation, repository, release,
  or deployment is created.
- Alpine ISO work is a separate planned workflow behind the current active
  routing/switching design; no installer repository, ISO, disk write, package
  fetch, boot, or appliance support claim is created.
- “All flavors” is an exact published matrix, not an impossible claim covering
  every obsolete, proprietary, experimental, or future extension.

### 2026-08-08 12:39–14:01 CDT — Build and Judge the executable Bifrost governance tree

Commit: current commit; hash assigned by Git after commit

Affected files:

- `README.md`
- `components/README.md`
- `documents/`
- `governance/`
- `schemas/v1/fabric-plan.schema.json`
- `tools/`
- `workflow.toml`
- `workflow/`
- `workflow.events.jsonl`

Explanation:

Build the cumulative local governance change covering the Cisco-style CLI,
executable product governance, Layer-2/3 switching, Layer-3/4-aware routing,
router/switch/converged roles, native Go Snort-class IDS/IPS, and an orthogonal
distributed fabric scope. Add optional dedicated Kubernetes/K3s-managed HA
whose controller coordinates native autonomous nodes without becoming a
forwarding dependency. Formalize the clean-room native Go HA engine as GoKA,
with bounded VRRP compatibility and no Keepalived code/runtime authority.
Define GoKA-native and Kubernetes-managed as the exactly two first-party,
out-of-the-box HA profiles once HA is release-admitted. Run
a fail-closed Judge loop over the whole change,
repair evidence binding, workflow chronology, component identity authority,
schema fixtures, and fabric placement constraints, then rerun all gates.

The distributed scope adds a deferred `bfw-fabric` component and defines
cryptographic membership, quorum/fencing and partition behavior,
Define cryptographic membership, quorum/fencing and partition behavior,
EVPN/VXLAN-class Layer-2/3 overlays, VRFs/anycast/ECMP, endpoint mobility,
deterministic node-local firewall placement, state symmetry/ownership/failover,
MTU/offload/BUM semantics, staged multi-node transactions, last-known-good
local enforcement, convergence observations, rolling rollback, and three-node
admission evidence. Domain ownership remains with switching, routing, and
firewall components.

Verification:

- `python tools/governance.py validate`
- `python tools/governance.py render --check`
- `python -m unittest discover -s tools/tests -v`
- `pyright tools/governance.py tools/tests/test_governance.py`
- `git diff --check`
- two cold distributed-systems/security reviews

Risks / non-goals:

- Fabric scope remains deferred outside v0.1; no implementation, cluster,
  tunnel, protocol session, repository, release, or deployment is created.
- EVPN/VXLAN/GENEVE terminology describes required compatible semantics and is
  not evidence that a protocol stack or hardware offload has been admitted.

### 2026-08-08 13:44 CDT — Define native Go Snort-class IDS/IPS

Commit: included in the cumulative current change above

Affected files:

- `README.md`
- `components/README.md`
- `documents/`
- `governance/`
- `schemas/v1/ids-plan.schema.json`
- `tools/`
- `workflow.toml`
- `workflow/`
- `workflow.events.jsonl`

Explanation:

Define `bfw-ids` as a clean-room native Go Snort-class IDS/IPS engine rather
than a Snort process wrapper. Add passive and separately admitted inline modes,
bounded capture/normalization and flow/stream state, protocol/rule evaluation,
signed atomic rulesets, typed alerts/evidence, explicit overload/loss health,
platform capture semantics, a strict Snort-rule compatibility matrix, and
core-authorized firewall-only enforcement.

Verification:

- `python tools/governance.py validate`
- `python tools/governance.py render --check`
- `python -m unittest discover -s tools/tests -v`
- `pyright tools/governance.py tools/tests/test_governance.py`
- `git diff --check`
- two cold security/architecture reviews

Risks / non-goals:

- The IDS component remains deferred outside v0.1; no implementation,
  repository, ruleset, packet test, performance result, or release is created.
- No complete Snort rule, decoder, preprocessor, detection, or performance
  parity is claimed, and Snort is referenced descriptively only.

### 2026-08-08 13:38 CDT — Define Layer-2/3 switch and Layer-3/4 router behavior

Commit: included in the cumulative current change above

Affected files:

- `README.md`
- `documents/`
- `governance/deployment-profiles.toml`
- `governance/requirements.toml`
- `governance/test-lab.toml`
- `schemas/v1/deployment-profile.schema.json`
- `tools/`
- `workflow.toml`
- `workflow/`
- `workflow.events.jsonl`

Explanation:

Refine Bifrost's roles so switch mode supports both Layer 2 and bounded Layer 3
switching through SVIs, routed switchports, inter-VLAN routing, and local-fabric
routes, while router mode composes Layer 3 forwarding with Layer-4-aware
stateful policy, NAT, port forwarding, and transport-aware steering. Preserve
separate switching, routing, and firewall authority, deny WAN/NAT/implicit
Layer-4 effects in switch mode, and explicitly reject any implication that
Layer-4 awareness grants Layer-7 proxy or payload authority.

Verification:

- `python tools/governance.py validate`
- `python tools/governance.py render --check`
- `python -m unittest discover -s tools/tests -v`
- `pyright tools/governance.py tools/tests/test_governance.py`
- `git diff --check`
- two cold governance/security reviews

Risks / non-goals:

- This is product architecture and executable governance only; it implements
  no packet path, switch/router runtime, release, or deployment.
- "Layer 4 router" is intentionally modeled as Layer-3 routing composed with
  stateful Layer-4-aware firewall/NAT effects, not as a new routing authority.

### 2026-08-08 13:29 CDT — Define router, switch, and converged roles

Commit: included in the cumulative current change above

Affected files:

- `README.md`
- `documents/`
- `governance/deployment-profiles.toml`
- `governance/requirements.toml`
- `governance/test-lab.toml`
- `schemas/v1/deployment-profile.schema.json`
- `tools/`
- `workflow.toml`
- `workflow/`
- `workflow.events.jsonl`

Explanation:

Clarify that Bifrost is one full-featured network operating system deployable
as a router, switch, or converged router-switch. Add exact role component
closure and forwarding effects, non-transit management addressing for switch
mode, shared configuration and management authority, transactional role
changes, fail-closed capability negotiation, and explicit limits on v0.1 and
platform/hardware support claims.

Verification:

- `python tools/governance.py validate`
- `python tools/governance.py render --check`
- `python -m unittest discover -s tools/tests -v`
- `pyright tools/governance.py tools/tests/test_governance.py`
- `git diff --check`
- two cold governance/security reviews

Risks / non-goals:

- This defines product and governance contracts only; no runtime role switch,
  component repository, release, deployment, or admission is created.
- "Full-featured" does not claim that v0.1 or every supported platform/hardware
  combination implements the entire catalog.

### 2026-08-08 12:48 CDT — Make Bifrost a router and managed switch system

Commit: included in the cumulative current change above

Affected files:

- `README.md`
- `components/README.md`
- `contracts/TRANSACTION-V1.md`
- `documents/`
- `governance/`
- `schemas/v1/switch-plan.schema.json`
- `tools/`
- `workflow.toml`
- `workflow/`
- `workflow.events.jsonl`

Explanation:

Add `bfw-switching` as the explicit Layer-2 authority and include it in the
narrow v0.1 profile. Define VLAN access/trunk/native behavior, bridge domains,
FDB, STP-family loop control, LACP, isolation, storm control, multicast
snooping, LLDP observations, desired-state drift, management-path recovery,
and cross-domain transaction semantics. Linux software switching is the
portable baseline; ASIC and OS-specific offload require separate platform
admission and semantic-parity evidence.

Verification:

- `python tools/governance.py validate`
- `python tools/governance.py render --check`
- `python -m unittest discover -s tools/tests -v`
- `pyright tools/governance.py tools/tests/test_governance.py`
- `git diff --check`
- two cold governance/security reviews

Risks / non-goals:

- This is architecture and executable governance only; no switch runtime,
  platform adapter, component repository, artifact, release, or admission is
  created.
- Phase 0, pinned test images, component artifacts, and native switching
  conformance evidence remain blockers.

### 2026-08-08 12:42 CDT — Add executable product governance

Commit: included in the cumulative current change above

Affected files:

- `.forgejo/workflows/governance.yml`
- `.gitignore`
- `contracts/`
- `governance/`
- `schemas/v1/`
- `templates/component/`
- `tools/`
- `workflow.toml`
- `workflow/`
- `workflow.events.jsonl`
- `README.md`
- `components/README.md`
- `documents/`
- `docs/`

Explanation:

Turn the Bifrost meta repository into an executable product-governance control
plane. Add an authoritative component catalog and v0.1 composition, complete
requirement trace registry, blocked Phase 0 dashboard with exact substrate
revisions, versioned contract schemas, accepted architecture decisions, a
formal system threat model, cross-component transaction contract, narrow v0.1
profile, component bootstrap/admission templates, release/recovery design,
test-lab specification, deterministic generated views, dependency-free local
validators, and Forgejo CI wiring. All empty runtime pins and lab image fields
remain explicit blockers; no runtime, component repository, release, or
admission is created.

Verification:

- `python tools/governance.py validate`
- `python tools/governance.py render --check`
- `python -m unittest discover -s tools/tests -v`
- `git diff --check`
- cold governance/security review
- meta-repository no-runtime and secret-pattern scans

Risks / non-goals:

- CI execution on the remote Forgejo runner is not claimed until this local
  change is committed, pushed, and observed in that environment.
- Draft JSON Schemas define contract shape but do not admit implementations or
  replace runtime conformance, failure, boundary, and platform tests.
- Exact test images, component artifacts, rollback mates, signatures, and
  evidence remain absent and therefore block release admission.

### 2026-08-08 12:39 CDT — Define the Cisco IOS-style `bfw` command line

Commit: included in the cumulative current change above

Affected files:

- `README.md`
- `components/README.md`
- `documents/PRD.md`
- `documents/ARCHITECTURE.md`
- `documents/IMPLEMENTATION-SPEC.md`

Explanation:

Make Cisco IOS-style command-line ergonomics a first-class Bifrost product
contract. The unprivileged `bfw` client now has specified EXEC and configuration
modes, familiar prompts and navigation, contextual help and completion,
`show`/`no`/`default` grammar, and declarative plugin command contributions.
Unlike classic immediate-mutation workflows, configuration commands edit a
session-owned candidate and reach live state only through Bifrost validation,
transactional commit, verification, audit, and rollback. `enable` is an
authorized mode transition rather than shared-password authority.

Verification:

- `git diff --check`
- complete and unique BFW-PRD-000 through BFW-PRD-078 trace inspection
- CLI authority-boundary and candidate/commit semantic review
- canonical-document scan for direct shell, plugin, file, or host mutation
- meta-repository no-runtime check

### 2026-08-01 22:32 CDT — Make proxy and HA native Bifrost plugins

Commit: `dc55813a4f2648ff68e696136ea9be2de6cdf9ea`

Affected files:

- `README.md`
- `components/README.md`
- `documents/PRD.md`
- `documents/ARCHITECTURE.md`
- `documents/IMPLEMENTATION-SPEC.md`

Explanation:

Correct the initial catalog assumption that Caddy and Keepalived would be
service adapters. `bfw-reverse-proxy` is now a native Go reverse-proxy data and
control plane with a Caddy-like operator experience but no Caddy runtime,
configuration, package, process, or API dependency. `bfw-ha` now implements its
portable HA control logic natively in Go, with VRRP protocol behavior and
platform mechanisms such as FreeBSD CARP, but no Keepalived runtime,
configuration, process, or API dependency.

Verification:

- `git diff --check`
- requirement trace inspection for BFW-PRD-057 and BFW-PRD-059
- canonical-document scan rejecting Caddy-as-adapter and
  Keepalived-as-runtime language
- reverse-proxy protocol/limit/dependency and HA interoperability/platform
  boundary review
- meta-repository no-runtime check

Risks / non-goals:

- This selects native implementation ownership, not Caddy or Keepalived
  configuration/API compatibility.
- No proxy, VRRP implementation, CARP configuration, plugin repository,
  executable, listener, virtual address, or deployed service is created.

### 2026-08-01 22:19 CDT — Define the initial capability plugin catalog

Commit: `28b4120039c659023d0be9fdb1e0becff6b974a0`

Affected files:

- `README.md`
- `components/README.md`
- `documents/PRD.md`
- `documents/ARCHITECTURE.md`
- `documents/IMPLEMENTATION-SPEC.md`

Explanation:

Promote the discussed WireGuard and full capability-plugin catalog into the
Bifrost meta-repository plan. Add a Caddy-style `bfw-reverse-proxy` plugin with
Caddy as the preferred first adapter, and a cross-platform `bfw-ha` plugin that
provides Keepalived-style behavior through admitted VRRP, CARP, or equivalent
platform adapters. Define all foundation, network-service, advanced-network,
security/access, and operations plugin planning identifiers, typed dependency
rules, phased sequencing, provider boundaries, UI integration, and
requirement-to-verification traces.

Verification:

- `git diff --check`
- requirement trace inspection for BFW-PRD-051 through BFW-PRD-068
- catalog consistency and duplicate-plugin-name checks
- WireGuard key/enrollment and routing/firewall boundary review
- reverse-proxy credential, DNS/ACME/firewall, and forwarded-identity boundary review
- HA peer identity, quorum/fencing, split-brain, state-sync, and domain-authority review
- meta-repository no-runtime check

Risks / non-goals:

- No component repository, plugin executable, Caddy or Keepalived service,
  WireGuard tunnel, firewall rule, route, virtual address, or deployed runtime
  is created in this slice.
- Catalog names remain planning identifiers until their repository and public
  interface contracts are independently admitted.

### 2026-08-01 22:02 CDT — Make OIDC a first-class web identity contract

Commit: `1d38dc4224f47d5518fa255d3cf0baa11b44b483`

Affected files:

- `README.md`
- `components/README.md`
- `documents/PRD.md`
- `documents/ARCHITECTURE.md`
- `documents/IMPLEMENTATION-SPEC.md`

Explanation:

Define standards-based OIDC login as a first-class Bifrost web capability with
Authentik as an intended provider. Separate authentication from core
authorization, place reusable provider credentials in `agent-keyring`, issue
opaque bounded Bifrost sessions, deny token propagation to plugins, and retain
a protected local-console recovery path.

Verification:

- `git diff --check`
- requirement trace inspection for BFW-PRD-040 through BFW-PRD-050
- OIDC trust, claim-mapping, token/secret, session, outage, and recovery-boundary
  review
- meta-repository no-runtime check

Risks / non-goals:

- No identity component repository, Authentik application, client secret,
  runtime login flow, user, or deployed service is created in this slice.

### 2026-08-01 22:00 CDT — Make Bifrost the meta repo and route through a plugin

Commit: `37d12d0aa224a928030358a94e6b76f07f6837ce`

Affected files:

- `README.md`
- `components/README.md`
- `documents/PRD.md`
- `documents/ARCHITECTURE.md`
- `documents/IMPLEMENTATION-SPEC.md`
- `go.mod` (removed)

Explanation:

Define `danny/Bifrost` as the product meta repository rather than a runtime Go
module. Move routing ownership into the planned separately versioned
`bfw-routing` plugin and define meta-level component pinning, release
composition, compatibility, verification, and rollback responsibilities.

Verification:

- `git diff --check`
- absence check for a root product Go module or runtime source
- requirement trace inspection for BFW-PRD-035 through BFW-PRD-039
- component-map and routing-boundary review

Risks / non-goals:

- No component repository is created or pinned in this slice.
- No routing implementation, platform mutation, or deployed service is added.

### 2026-08-01 21:31 CDT — Define independent web and plugin UI contributions

Commit: `327a2f23237ed94c26ff817f3139f0c414bfcace`

Affected files:

- `README.md`
- `documents/PRD.md`
- `documents/ARCHITECTURE.md`
- `documents/IMPLEMENTATION-SPEC.md`

Explanation:

Make the web UI an independent unprivileged client of the core API and define
OPNsense-style plugin UI contributions through signed manifests, declarative
shared components, a sanitized UI catalog, typed action bindings, isolated rich
extensions, atomic UI/backend release handling, and `bfw` CLI recovery.

Verification:

- `go mod edit -json`
- `git diff --check`
- requirement trace inspection for BFW-PRD-025 through BFW-PRD-034
- UI trust-boundary review for direct plugin, credential, DOM, asset, network,
  and authorization bypasses

Risks / non-goals:

- This admits architecture and requirements only. It adds no web runtime,
  frontend bundle, plugin UI, firewall mutation, or deployed service.

### 2026-08-01 21:25 CDT — Correct the full product name to Bifrost

Commit: `4f4bbe36006997ffb4c3affd6ca8ed5baf5e266a`

Affected files:

- `README.md`
- `documents/PRD.md`
- `documents/ARCHITECTURE.md`
- `documents/IMPLEMENTATION-SPEC.md`

Explanation:

Correct the formal product name to **Bifrost**. Retain **BFW** as the canonical
firewall shorthand (Bifrost Firewall), `bfw` as the lowercase public namespace,
and `BFW-PRD-*` as the planning-requirement namespace.

Verification:

- `go mod edit -json`
- `git diff --check`
- naming and requirement-trace inspection

Risks / non-goals:

- The repository and requirement identifiers do not change.
- No runtime code, package, executable, or installed service is renamed.

### 2026-08-01 21:10 CDT — Establish BFW as the product acronym

Commit: `a7d12f806e78fc8cbf305ffd422aa8f4a5e394c7`

Affected files:

- `README.md`
- `documents/PRD.md`
- `documents/ARCHITECTURE.md`
- `documents/IMPLEMENTATION-SPEC.md`

Explanation:

Name the product **Bifrost Firewall**, establish **BFW** as its canonical
acronym and `bfw` as its lowercase public namespace, and migrate planning
requirement identifiers from the provisional prefix to `BFW-PRD-*` before
implementation creates compatibility obligations.

Verification:

- `go mod edit -json`
- `git diff --check`
- naming and requirement-trace inspection
- absence check for the retired requirement prefix

Risks / non-goals:

- The repository remains `danny/Bifrost`.
- Final daemon and web-service executable names remain a later interface-design
  decision; no runtime code or installed service was renamed.

### 2026-08-01 21:08 CDT — Assign file and process operations to agent providers

Commit: `2ea4ae84d0d3593f613f3799340cd98ede4860f7`

Affected files:

- `README.md`
- `documents/PRD.md`
- `documents/ARCHITECTURE.md`
- `documents/IMPLEMENTATION-SPEC.md`

Explanation:

Make `agent-filesystem` the provider for admitted host-file operations and
`agent-exec` the provider for admitted local process execution. Define strict
composition with `agent-keyring`, deny ambient filesystem/shell/process
authority, and extend the cross-platform Phase 0 admission gate.

Verification:

- `go mod edit -json`
- `git diff --check`
- requirement trace inspection for BFW-PRD-019 through BFW-PRD-024
- provider-boundary review for credential, path, command, privilege, and
  confused-deputy bypasses

Risks / non-goals:

- This does not modify the provider repositories, execute commands through
  them, mutate host files through them, or add Bifrost runtime code.

### 2026-08-01 21:05 CDT — Assign credentials to agent-keyring

Commit: `9cca949db349c65e352f134f57775ebb82b4d07a`

Affected files:

- `README.md`
- `documents/PRD.md`
- `documents/ARCHITECTURE.md`
- `documents/IMPLEMENTATION-SPEC.md`

Explanation:

Make `agent-keyring` Bifrost's credential authority. Require core action
admission before keyring access, scoped short-lived leases or non-exporting
opaque references, default denial of raw export, generation-bound revocation,
and a cross-platform keyring admission gate.

Verification:

- `go mod edit -json`
- `git diff --check`
- requirement trace inspection for BFW-PRD-014 through BFW-PRD-018
- credential-boundary review for raw-secret and authorization bypass paths

Risks / non-goals:

- This is architecture and sequencing only. It does not migrate credentials,
  modify `agent-keyring`, expose secrets, or add Bifrost runtime code.

### 2026-08-01 20:59 CDT — Gate Bifrost on the completed plugin substrate

Commit: `9c19dda84f8fd6928d49aeb93d9536e6e539f68b`

Affected files:

- `README.md`
- `documents/PRD.md`
- `documents/ARCHITECTURE.md`
- `documents/IMPLEMENTATION-SPEC.md`

Explanation:

Make completion and admission of the cross-platform `rpc-plugin-system` a
Phase 0 predecessor gate for Bifrost runtime implementation. Design work may
continue, but Bifrost may not fork transport, authentication, generation,
lifecycle, or supervision behavior to start implementation early.

Verification:

- `git diff --check`
- requirement trace inspection for BFW-PRD-013
- dependency-gate exit-evidence inspection

Risks / non-goals:

- This records sequencing only; it does not assign work, change
  `rpc-plugin-system`, or add Bifrost runtime code.

### 2026-08-01 20:55 CDT — Make cross-platform plugins a product requirement

Commit: `ca617495444cd5d9fa5e917860ce2248b50a4cff`

Affected files:

- `README.md`
- `documents/PRD.md`
- `documents/ARCHITECTURE.md`
- `documents/IMPLEMENTATION-SPEC.md`

Explanation:

Replace the Linux-only product boundary with a cross-platform native-engine
model and make OPNsense-style extensibility a first-class requirement. Define a
small portable core, signed and permission-declared packages, separate
platform/service executables, last-known-good persistence, and the required
cross-platform evolution of `rpc-plugin-system`.

Verification:

- `go mod edit -json`
- `git diff --check`
- design traceability inspection for BFW-PRD-009 through BFW-PRD-012

Risks / non-goals:

- This change admits architecture and requirements only; no plugin runtime,
  firewall backend, package manager, or host networking mutation is added.

### 2026-08-01 20:43 CDT — Bootstrap Bifrost

Commit: `b0b3f0b2a57b67c5b70833f9126a417e3ed85880`

Affected files:

- `.gitignore`
- `README.md`
- `go.mod`
- `documents/PRD.md`
- `documents/ARCHITECTURE.md`
- `documents/IMPLEMENTATION-SPEC.md`
- `docs/CHANGELOG.md`

Explanation:

Create the planning baseline for a Go-based Linux firewall and routing
appliance in the same broad product category as OPNsense. Establish the kernel
data-plane boundary, fail-closed posture, recovery requirements, and canonical
design-document sequence without adding executable firewall behavior.

Verification:

- `go mod edit -json`
- `git diff --check`
- exact local/remote ref comparison
- server-side Git integrity check

Risks / non-goals:

- No firewall, router, service, installer, or production deployment exists yet.
- Feature parity with OPNsense is not claimed.
