# Feature: executable product governance

Canonical state, dependencies, blockers, review, and evidence are defined only in root `workflow.toml`.

Base revision: `a3afae76b4b2eb31a965b7a067258a298ec6e7f8`

Scope:

- preserve the uncommitted Cisco IOS-style CLI architecture work
- add BFW-PRD-079 through BFW-PRD-090
- implement all twelve approved meta-repository governance capabilities
- add only governance tooling and contracts, never Bifrost runtime code
- leave commit, push, repository creation, release, deployment, and runtime
  mutation outside this task's authority

Acceptance requires exact trace equality, valid deterministic machine-readable
state, fail-closed Phase 0/release semantics, validator tests, static analysis,
diff inspection, two fresh review passes, and cleanup accounting.
