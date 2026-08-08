# Cold review 2: clean-room compatibility, completeness, and admission

Decision: PASS

Scope: native Go/clean-room claim, Snort compatibility boundary, ruleset
lifecycle, platform semantics, conformance/performance evidence, and wording.

Findings:

- The design rejects embedding, executing, supervising, or copying Snort and
  requires provenance review; Snort is used descriptively without endorsement.
- Compatibility is an explicit dialect/feature matrix. Unsupported actions,
  keywords, preprocessors, PCRE constructs, decoders, and ambiguous semantics
  are hard errors, not best-effort translations.
- Canonical rules are signed, provenance-bound, content-addressed,
  deterministically compiled, atomically activated, expirable, and reversible.
- Reassembly, normalization, matching, state, evidence, and alerts carry
  explicit resource bounds and completeness/loss accounting.
- Platform capture/injection, timestamp, offload/checksum, VLAN, multi-queue,
  zero-copy, ordering, and loss behavior must be independently admitted.
- Canonical/differential corpora, deterministic oracles, fuzz/race/evasion,
  restart/rollback, overload/loss, and resource/performance evidence are required
  before any compatibility or runtime admission claim.

No unqualified Snort parity, copied-runtime dependency, or evidence laundering
was found. The component remains explicitly deferred outside v0.1.
