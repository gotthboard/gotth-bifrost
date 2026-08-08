# Native Go IDS/IPS v1 workflow

Status: completed

This feature defines a clean-room native Go Snort-class IDS/IPS component while
keeping detection, enforcement, evidence, platform, and licensing/provenance
boundaries explicit.

Scope:

- add BFW-PRD-111 through BFW-PRD-122
- define passive IDS and separately admitted inline IPS
- define bounded capture normalization, flow/stream reassembly, decoders,
  canonical rules, alerts, health, resource limits, and platform semantics
- define a versioned Snort-rule compatibility subset with hard rejection of
  unsupported or ambiguous semantics
- preserve core authorization and firewall-only enforcement mutation

The component remains deferred outside v0.1. No runtime implementation,
repository, rule feed, release, compatibility claim, or admission is created.
