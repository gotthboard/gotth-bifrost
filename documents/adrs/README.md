# Bifrost architecture decision records

ADRs settle durable product-level choices. They do not admit runtime code or a
release. An accepted ADR remains in force until a later ADR explicitly
supersedes it.

| ADR | Status | Decision |
| --- | --- | --- |
| [ADR-0001](0001-platform-tiers.md) | Accepted | Linux-first v0.1 with FreeBSD and Windows compatibility tiers |
| [ADR-0002](0002-executable-names.md) | Accepted | `bfw`, `bfwd`, and `bfw-web` public executable roles |
| [ADR-0003](0003-identity-boundary.md) | Accepted | Separate `bfw-identity` component without authorization ownership |
| [ADR-0004](0004-platform-repositories.md) | Accepted | One platform-backend repository per operating-system family |
| [ADR-0005](0005-recovery-model.md) | Accepted | Verified last-known-good state, A/B images, and local-console recovery |
| [ADR-0006](0006-signing-roots.md) | Accepted | Offline root with scoped delegated signing roles |
| [ADR-0007](0007-versioning-and-channels.md) | Accepted | Semantic public contracts, bounded compatibility, and explicit channels |
| [ADR-0008](0008-switching-domain.md) | Accepted | First-class Layer-2 switching domain with a Linux software baseline |
| [ADR-0009](0009-deployment-roles.md) | Accepted | One product with router, switch, and converged deployment roles |
| [ADR-0010](0010-data-plane-layer-semantics.md) | Accepted | Layer-2/3 switching and Layer-3/4-aware router semantics |
| [ADR-0011](0011-native-go-ids.md) | Accepted | Clean-room native Go Snort-class IDS/IPS engine |
| [ADR-0012](0012-distributed-fabric.md) | Accepted | Distributed switching, routing, and firewall fabric |
| [ADR-0013](0013-kubernetes-managed-ha.md) | Accepted | First-party Kubernetes-managed HA without forwarding dependency |
| [ADR-0014](0014-goka-clean-room-ha.md) | Accepted | GoKA clean-room native Go HA engine |
| [ADR-0015](0015-two-first-party-ha-profiles.md) | Accepted | Exactly two first-party out-of-the-box HA profiles |
| [ADR-0016](0016-linux-learning-alpha.md) | Accepted | Linux-only learning alpha with a separate minimum safety gate |

New records start from [ADR-0000](0000-template.md). Accepted records must link
requirements, identify consequences, and name any deliberately unresolved
platform detail.
