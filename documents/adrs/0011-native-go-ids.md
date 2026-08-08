# ADR-0011: Native Go Snort-class IDS/IPS

Status: Accepted

Requirements: BFW-PRD-111 through BFW-PRD-122

## Context

Bifrost needs a first-party intrusion-detection and prevention capability with
the operational depth operators expect from Snort-class systems. Wrapping a
Snort process would add a second configuration/runtime authority and make
cross-platform lifecycle, typed plans, failure semantics, resource bounds, and
evidence harder to integrate. Claiming blanket rule compatibility would also
be unsafe because rule dialects, preprocessors, PCRE features, and packet
normalization semantics differ.

## Decision

Implement `bfw-ids` as a clean-room native Go engine. It owns bounded capture
normalization, flow/fragment/TCP-stream state, protocol decoders, canonical
rule evaluation, threshold/suppression state, alerts, health, and enforcement
proposals. It does not embed, execute, supervise, or copy Snort.

Bifrost owns a canonical rule IR and may import a declared Snort-rule dialect
only through a tested feature matrix. Unsupported or ambiguous semantics are
hard errors. Passive IDS and inline IPS are separately admitted modes. Only the
core and `bfw-firewall` can authorize and apply enforcement.

Rules and feeds are signed, provenance-bound, deterministic, atomic, expirable,
and rollback-capable. Packet/flow/decoder/matcher/evidence work is bounded.
Packet loss, truncation, overload, unknown decoding, or incomplete inspection
is explicit and never reported as complete.

## Consequences

- Bifrost gains a native portable IDS/IPS product direction without a Snort
  runtime dependency.
- Rule compatibility is narrower but honest and mechanically testable.
- Platform capture/injection adapters and performance evidence are substantial
  future work and remain outside v0.1.
- Inline failure behavior becomes an explicit per-zone safety decision.
- Raw payload and PCAP evidence remains opt-in, bounded, and protected.

## Alternatives considered

- Supervise Snort directly: rejected because it creates a second runtime and
  configuration authority and conflicts with the native Go direction.
- Translate every Snort rule best-effort: rejected because silent semantic
  weakening creates false-negative security claims.
- Start with inline prevention only: rejected because prevention has greater
  availability and lockout risk than passive detection.

## Verification

- no-Snort-runtime/source dependency and provenance scans
- rule-dialect conformance and explicit-rejection fixtures
- canonical packet/flow/evasion corpora and deterministic alert oracles
- fuzz, race, resource-bound, overload/loss, restart, rollback, and performance
  evidence on every admitted platform and mode
- enforcement confused-deputy and direct-firewall-mutation denial tests
