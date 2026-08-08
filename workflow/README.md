# Bifrost workflow

`workflow.toml` is the canonical state for meta-repository work. Supporting
evidence and coverage notes do not override it.

The active root is the executable governance slice. It may add schemas,
metadata, templates, documentation, and validation tooling. It may not add
Bifrost runtime code, create component repositories, mutate host networking,
commit, push, release, or deploy without separate authorization.
