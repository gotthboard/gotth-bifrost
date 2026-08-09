# Bifrost governance data

This directory is the machine-readable control plane for Bifrost product
development. It does not authorize or implement a Bifrost runtime.

Authority is divided deliberately:

- `requirements.toml` is authoritative for requirement ownership, lifecycle,
  blockers, verification state, evidence, and admission. Normative requirement
  statements remain in `documents/PRD.md`; validation requires an exact ID set.
- `components.toml` is authoritative for component identity, ownership,
  dependencies, conflicts, platform declarations, immutable pins, and
  admission state. `components/README.md` is its human-oriented explanation.
- `alpha.toml` is authoritative for the minimum safety gate separating source
  implementation and offline simulation from designated non-production
  host-network, installer-disk, and alpha-distribution effects.
- `phase0.toml` is authoritative for beta, stable, and production runtime
  admission. Alpha evidence cannot satisfy that cross-platform gate.
- `releases/*.toml` is authoritative for product profiles and admitted release
  composition. A draft profile with empty pins is not a release.
- `test-lab.toml` is authoritative for the required lab roles and evidence
  classes. Exact operating-system images remain blocked until their hashes are
  recorded.

If machine-readable state and prose disagree, validation fails and the
disagreement must be resolved explicitly. Missing evidence is never inferred
from a passing metadata check.

Run the local governance gate with:

```sh
python tools/governance.py validate
python tools/governance.py render --check
```

The first command validates structure, references, dependency cycles, pins,
schema hygiene, release/profile completeness, alpha and Phase 0 honesty, ADR/template
coverage, changelog state, and the meta-repository boundary. The second proves
that generated human views match their authoritative TOML inputs.
