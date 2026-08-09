# Bifrost workflow

`workflow.toml` is the only canonical state for meta-repository work. Feature
README files explain scope; they do not define state, dependencies, blockers,
review, evidence, or completion. `docs/WORKFLOW.md` and `workflow/COVERAGE.md`
are generated views and must never be edited by hand.

The checked equivalent of `workflow check` is
`python3 tools/governance.py validate`. The checked equivalent of
`workflow current` is `docs/WORKFLOW.md` after
`python3 tools/governance.py render`. State changes require an append-only
`workflow.events.jsonl` event and must preserve one active feature.

Meta-repository workflows may change only contracts, schemas, governance data,
workflow records, generated views, tests, and validation tooling. They may not
add Bifrost runtime code, create component repositories, mutate host networking
or disks, commit, push, release, or deploy without separate authorization.
