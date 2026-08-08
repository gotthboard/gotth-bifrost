# ADR-0014: GoKA clean-room native Go HA engine

Status: Accepted

Requirements: BFW-PRD-145 through BFW-PRD-153

## Context

Bifrost needs portable virtual-router election, health tracking, and failover
coordination without making an external daemon or configuration language a
runtime authority. Keepalived is a useful behavioral reference, but its broad
script, hook, IPVS, and configuration surface does not match Bifrost's typed
least-authority model.

## Decision

Name the `bfw-ha` engine **GoKA** and implement it clean-room in Go from public
VRRP specifications and independently authored tests. GoKA owns election,
health, and failover intent but emits typed effect plans to Bifrost domain
owners. It never copies, embeds, links, invokes, supervises, or requires
Keepalived. Any importer accepts only an exact documented subset and treats
unsupported or ambiguous input as an error.

## Consequences

- GoKA has its own public schemas, protocol corpus, provenance, and admission.
- VRRPv2/v3 interoperability is measured rather than assumed.
- Arbitrary shell checks and notification hooks are not compatibility goals.
- FreeBSD CARP and other mechanisms require separately admitted semantic maps.
- Network, routing, firewall, platform, credential, and state authorities stay
  outside GoKA.

## Alternatives considered

- Bundle or supervise Keepalived: rejected due to runtime and authority coupling.
- Copy or translate Keepalived source: rejected; GoKA is clean-room.
- Full Keepalived configuration compatibility: rejected because silent semantic
  mismatch, scripts, hooks, and IPVS would expand authority.
- Let GoKA mutate native networking directly: rejected because it bypasses core
  authorization, transaction, observation, and rollback.

## Verification

- clean-room provenance, dependency/source/license, and reproducible-build scans
- VRRP state-machine, timer, packet, malformed-input, fuzz, and interop suites
- typed-effect/direct-mutation, health-boundary, partition, fencing, and restart tests
- Linux native, FreeBSD CARP, unsupported-platform, upgrade, rollback, and
  performance evidence
