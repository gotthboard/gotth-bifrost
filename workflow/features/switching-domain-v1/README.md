# Switching domain v1 workflow

Canonical state, dependencies, blockers, review, and evidence are defined only in root `workflow.toml`.

This feature makes managed Layer-2 switching a first-class Bifrost product
domain while retaining distinct network, routing, and firewall authorities.

Scope:

- add BFW-PRD-091 through BFW-PRD-099
- add `bfw-switching` to the component catalog and v0.1 profile
- define switching architecture, schema, ADR, threat, transaction, recovery,
  platform-semantic, observed-state, and admission-test contracts
- keep runtime implementation and external actions prohibited

Completion requires governance validation, generated-view reconciliation,
tool tests, static analysis, diff hygiene, two cold review passes, and immutable
local evidence. It does not admit a runtime component or release.
