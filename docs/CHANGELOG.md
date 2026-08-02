# Changelog

## Unreleased

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
