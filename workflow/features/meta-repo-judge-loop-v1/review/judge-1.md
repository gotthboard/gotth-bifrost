# Judge pass 1 — FAIL

Scope: complete cumulative local diff from
`a3afae76b4b2eb31a965b7a067258a298ec6e7f8`.

## Blocking findings

1. Seven Unreleased changelog entries claim the one allowed current-commit
   marker. One dirty tree cannot honestly identify seven different commits.
2. The workflow event log is not chronological: `switching-domain-v1` starts
   before `meta-governance-v1` completes, despite the one-active-feature model.
   The validator checks neither chronology nor legal state transitions.
3. Governance evidence is accepted when it belongs to any feature, rather than
   being bound to the requirement that cites it. An unrelated digest can verify
   a requirement.
4. `bfw-fabric` depends on the human OIDC component `bfw-identity` for a node
   identity contract. Fabric node identity, liveness, and generation belong to
   `rpc-plugin-system`; durable control credentials belong to `agent-keyring`.
5. The implementation map promises representative valid and invalid schema
   fixtures, but no instance fixtures are run. The validator only parses schema
   documents and checks shallow structure/references.
6. A fabric placement can carry null switch, route, and firewall plans, so the
   schema admits a placement with no owned data-plane action.

Decision: FAIL. These findings block completion and require a full rerun plus
two fresh post-repair Judge passes.
