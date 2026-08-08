# ADR-0015: Two first-party out-of-the-box HA profiles

Status: Accepted

Requirements: BFW-PRD-154 through BFW-PRD-161

## Context

Bifrost needs a simple supported HA product story without collapsing native
fast failover into Kubernetes or forcing every deployment to operate a cluster.

## Decision

Ship exactly two first-party HA deployment profiles: `goka-native` and
`kubernetes-managed`. Both use the same Bifrost configuration and authority
contracts. Only one management coordinator owns an HA domain at a time.
Kubernetes-managed deployments may coordinate native GoKA or routing/platform
mechanisms, but fast forwarding failover remains node-local.

## Consequences

- GoKA-native requires no external orchestrator.
- Kubernetes-managed ships its Bifrost controller assets but requires an
  admitted Kubernetes/K3s substrate.
- Both profiles are packaged out of the box once HA is release-admitted.
- v0.1 remains honest: both are deferred until their runtime evidence exists.
- Cross-profile migration becomes an admission-critical transaction.

## Alternatives considered

- Support arbitrary HA backends: rejected because compatibility and recovery
  semantics would be unbounded.
- Make Kubernetes the forwarding authority: rejected due to circular network
  dependency and unsuitable fast-path recovery.
- Ship Kubernetes support as a third-party add-on: rejected by product direction.
- Enable both coordinators concurrently: rejected due to split authority.

## Verification

- exact profile/catalog/package checks
- shared configuration, CLI/API, authorization, audit, and recovery parity
- single-coordinator and competing-writer denial tests
- transactional cross-profile migration and rollback
- release composition, failure matrix, and no-v0.1-overclaim checks
