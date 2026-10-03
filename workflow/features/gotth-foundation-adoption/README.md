# GOTTH shared-foundation adoption

The repository-family transition is documented in
[the adoption contract](../../../documents/GOTTH-INTEGRATION.md).
Runtime implementation state, dependencies, review and evidence are owned by
`workflow.toml`, not this README.

This feature plans BFW-PRD-229 through BFW-PRD-234. It requires explicit
activation after its existing design dependencies; the repository update does
not start it, create runtime components or change any alpha/Phase 0 decision.

Follow [PLAN.md](PLAN.md) in bounded vertical slices. Reuse implemented GOTTH
mechanisms, leave placeholders visible, and retain Bifrost's core, native
network, supervisor, credential, filesystem, execution and recovery authority.
