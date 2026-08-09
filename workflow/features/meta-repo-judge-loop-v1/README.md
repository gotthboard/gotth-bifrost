# Cumulative meta-repository Judge loop

Canonical state, dependencies, blockers, review, and evidence are defined only in root `workflow.toml`.

This feature performs a cold, fail-closed review of the complete local diff from
`a3afae76b4b2eb31a965b7a067258a298ec6e7f8`. It reviews governance integrity,
trace and evidence binding, workflow history, schemas and fixtures, component
authority boundaries, generated views, and the documented no-runtime boundary.

The loop is complete only after every blocking finding is repaired, the full
verification suite passes, and two fresh post-repair Judge reviews pass.
