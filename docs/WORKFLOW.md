# Bifrost workflow status

Generated from `workflow.toml`; do not edit by hand.

Profile: **strict**
Active feature: **`routing-switching-protocol-suites-v1`**
Runtime code allowed in meta repo: **false**
External actions allowed: **false**

| Feature | State | Phase | Risk | Dependencies | Plan | Review | Evidence | Blockers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `meta-governance-v1` | done | governance | high | none | complete | approved | 1 | none |
| `switching-domain-v1` | done | design | high | `meta-governance-v1` | complete | approved | 1 | none |
| `deployment-roles-v1` | done | design | high | `switching-domain-v1` | complete | approved | 1 | none |
| `data-plane-layers-v1` | done | design | critical | `deployment-roles-v1` | complete | approved | 1 | none |
| `native-go-ids-v1` | done | design | critical | `data-plane-layers-v1` | complete | approved | 1 | none |
| `distributed-fabric-v1` | done | design | critical | `data-plane-layers-v1` | complete | approved | 1 | none |
| `meta-repo-judge-loop-v1` | done | verification | high | `native-go-ids-v1`<br>`distributed-fabric-v1` | complete | approved | 1 | none |
| `kubernetes-managed-ha-v1` | done | design | critical | `distributed-fabric-v1` | complete | approved | 1 | none |
| `goka-clean-room-ha-v1` | done | design | critical | `data-plane-layers-v1` | complete | approved | 1 | none |
| `two-out-of-box-ha-profiles-v1` | done | design | critical | `kubernetes-managed-ha-v1`<br>`goka-clean-room-ha-v1` | complete | approved | 1 | none |
| `routing-switching-protocol-suites-v1` | in_progress | design | critical | `data-plane-layers-v1`<br>`two-out-of-box-ha-profiles-v1` | `workflow/features/routing-switching-protocol-suites-v1/REVIEW-PLAN.md` | pending | 0 | independent architecture review<br>independent security review<br>verification evidence<br>workflow handoff |
| `alpine-linux-appliance-iso-v1` | planned | decomposition | critical | `routing-switching-protocol-suites-v1` | `workflow/features/alpine-linux-appliance-iso-v1/DECOMPOSITION.md` | pending | 0 | active routing/switching workflow<br>exact Alpine patch and APK snapshot unselected<br>bfw-installer repository absent<br>installer safety evidence absent |
| `linux-learning-alpha-v1` | planned | decomposition | critical | `routing-switching-protocol-suites-v1`<br>`alpine-linux-appliance-iso-v1` | `workflow/features/linux-learning-alpha-v1/DECOMPOSITION.md` | pending | 0 | active routing/switching workflow<br>Alpine ISO workflow incomplete<br>Linux-alpha dependency revisions unselected<br>BFW-ALPHA-0 safety evidence absent |
| `freebsd-generic-appliance-iso-v1` | planned | decomposition | critical | `routing-switching-protocol-suites-v1`<br>`alpine-linux-appliance-iso-v1` | `workflow/features/freebsd-generic-appliance-iso-v1/DECOMPOSITION.md` | pending | 0 | active routing/switching workflow<br>shared installer contract and Alpine ISO workflow incomplete<br>exact supported FreeBSD release/source/package snapshot unselected<br>generic x86-64 hardware matrix unselected<br>FreeBSD installer and A/B safety evidence absent |
