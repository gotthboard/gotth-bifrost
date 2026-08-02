# Changelog

## Unreleased

### 2026-08-01 20:43 CDT — Bootstrap Bifrost

Commit: current commit; hash assigned by Git after commit

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
