# Bifrost global coverage map

Generated from `workflow.toml`; do not edit by hand.

This records governance and system-evidence posture. It does not claim runtime coverage where artifacts do not exist.

| Subsystem | Owner | Risk | Required harness | Evidence | Known gaps | Plan | Next increment |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `meta-governance` | meta | high | `syntax`<br>`unit`<br>`negative`<br>`generated-view`<br>`workflow-state`<br>`diff` | 2 | none | complete | Preserve fail-closed regression coverage for every governance-state change. |
| `routing-switching-contracts` | bfw-routing,bfw-switching | critical | `trace`<br>`architecture-review`<br>`security-review`<br>`negative-policy`<br>`interoperability-plan` | 0 | Independent architecture review absent.<br>Independent security review absent.<br>Immutable verification record absent. | `workflow/features/routing-switching-protocol-suites-v1/REVIEW-PLAN.md` | Complete two independent reviews over one immutable revision and record verification evidence. |
| `alpine-installer-alpha` | bfw-installer,meta | critical | `wrong-disk`<br>`offline-install`<br>`power-loss`<br>`rollback`<br>`recovery`<br>`first-boot-packet-state`<br>`channel-isolation` | 0 | Exact Alpine and APK snapshot unselected.<br>Installer and appliance artifacts do not exist.<br>BFW-ALPHA-0 is blocked. | `workflow/features/alpine-linux-appliance-iso-v1/DECOMPOSITION.md` | Finish ISO decomposition, select immutable inputs, and create component-owned implementation work. |
| `phase0-substrates` | meta | critical | `revision-binding`<br>`grade-evidence`<br>`independent-review`<br>`catalog-admission`<br>`cross-platform`<br>`release-gate` | 0 | rpc-plugin-system is ungraded.<br>agent-keyring is ungraded.<br>agent-filesystem is ungraded.<br>agent-exec is ungraded. | `workflow/PHASE0-ADMISSION-PLAN.md` | Admit each exact dependency revision independently at A or A+; do not aggregate grades. |
| `release-composition` | meta | critical | `composition`<br>`signature`<br>`sbom`<br>`provenance`<br>`upgrade`<br>`rollback`<br>`recovery`<br>`channel-gate` | 0 | v0.1 remains a design-only profile.<br>No component artifacts or admitted composition exist. | `workflow/RELEASE-COMPOSITION-PLAN.md` | Create an immutable alpha composition only after component artifacts and BFW-ALPHA-0 evidence exist. |
