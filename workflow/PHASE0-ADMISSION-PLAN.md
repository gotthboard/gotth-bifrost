# Phase 0 substrate admission plan

This plan governs Bifrost admission of `rpc-plugin-system`, `agent-keyring`,
`agent-filesystem`, and `agent-exec`. It is not grade evidence. The exact row
state remains canonical in `governance/phase0.toml`.

Each dependency is admitted independently. External component repair and
evidence generation may proceed in parallel, but Bifrost records an admission
only through its one-active-feature workflow.

## Per-dependency gate

1. Freeze one immutable released revision and verify the repository, tag,
   artifact, dependency-lock, and source identities agree.
2. Import signed artifact digests, SBOM, provenance, supported-platform matrix,
   migration/rollback mate, and every required gate result.
3. Reproduce the relevant build and run the dependency's cross-platform,
   identity, lifecycle, failure, recovery, endurance, and redaction harnesses.
4. Bind all evidence to the exact revision. Evidence from a predecessor,
   branch name, moving tag, local dirty tree, or integrated demo is rejected.
5. Obtain an independent cold review naming reviewer, target revision, evidence
   set, verdict, limitations, and time. The component cannot grade itself.
6. Assign A or A+ only when no required gate, evidence item, review finding, or
   catalog gap remains. Scores cannot be averaged across dependencies.
7. Admit the exact component record and then the matching Bifrost Phase 0 row.
   Any revision or artifact change reopens that row.

## Phase completion

`BFW-PHASE-0` passes only when all four rows simultaneously have A/A+ grades,
revision-bound evidence, independent approved reviews, complete gates,
component-catalog admission, and no gaps. Until then, out-of-alpha
implementation and beta/stable admission remain false.
