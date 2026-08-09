# Linux learning-alpha admission path

Canonical state, dependencies, blockers, review, and evidence are defined only in root `workflow.toml`.

This feature creates a usable, explicitly non-production Linux appliance for
decision-making before beta contracts are frozen. It does not lower destructive
or authority safety boundaries and does not admit beta or stable.

Planned scope:

- implement BFW-PRD-215 through BFW-PRD-222 after this feature becomes the
  single active workflow
- select immutable `rpc-plugin-system` v2 and Linux-compatible keyring,
  filesystem, and execution releases
- implement the exact single-node Alpine x86-64 software-data-plane alpha
  scope and explicit unsupported-capability behavior
- admit `BFW-ALPHA-0` before designated host-network mutation, installer-disk
  mutation, or signed alpha distribution
- capture bounded decision telemetry, exact limitations, recovery/reset
  behavior, and owner decisions without treating alpha evidence as promotion
- preserve full `BFW-PHASE-0` admission for beta and stable
- block every out-of-alpha implementation subtree until all four Phase 0
  dependencies independently earn A or A+ admissions

This planned record creates no runtime source, component repository, process,
ISO, disk or network mutation, release, deployment, or support claim.
