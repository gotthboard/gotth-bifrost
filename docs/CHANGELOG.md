# Changelog

## Unreleased

### 2026-08-01 20:59 CDT — Gate Bifrost on the completed plugin substrate

Commit: current commit; hash assigned by Git after commit

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
- requirement trace inspection for BFR-PRD-013
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
- design traceability inspection for BFR-PRD-009 through BFR-PRD-012

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
