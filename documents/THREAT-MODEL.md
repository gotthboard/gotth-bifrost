# Bifrost threat model

Status: initial system threat baseline; runtime evidence absent

Requirements: BFW-PRD-003, BFW-PRD-007, BFW-PRD-009 through BFW-PRD-024,
BFW-PRD-029 through BFW-PRD-034, BFW-PRD-060, BFW-PRD-068, BFW-PRD-084,
BFW-PRD-091 through BFW-PRD-099, BFW-PRD-100 through BFW-PRD-105, and
BFW-PRD-106 through BFW-PRD-110, BFW-PRD-111 through BFW-PRD-122, and
BFW-PRD-123 through BFW-PRD-135, BFW-PRD-136 through BFW-PRD-144, and
BFW-PRD-145 through BFW-PRD-153, and BFW-PRD-154 through BFW-PRD-161

## Protected assets

- packet-policy integrity and last-known-good enforcement
- canonical configuration, release composition, and audit continuity
- operator identity, authorization policy, and recovery authority
- private keys, tokens, passwords, signing material, and opaque authority
- plugin/provider generations, peer identity, and transaction state
- availability of management, switching, routing, DNS/DHCP, VPN, and HA
  recovery paths

## Trust boundaries

```text
operator terminal/browser
  | untrusted input
bfw / bfw-web / bfw-identity (unprivileged clients)
  | authenticated, versioned typed API
bfwd core (authorization and transaction authority)
  | separately admitted generation-bound capabilities
rpc-plugin-system -> domain/platform plugins -> native OS/service APIs
  | separate provider authorities
agent-keyring / agent-filesystem / agent-exec
  | verified native state and redacted evidence
last-known-good configuration and release records
```

Package repositories, update mirrors, OIDC providers, DNS, peers, plugins,
support destinations, and all network inputs are untrusted until their exact
contract is authenticated and admitted.

## Threat register

| ID | Threat and attack path | Required mitigation | Requirements | Verification | Residual risk |
| --- | --- | --- | --- | --- | --- |
| BFW-THR-001 | Compromised web/CLI client proposes privileged or hidden mutation | unprivileged clients; typed core action; current identity, authorization, confirmation, generation, and audit | 025, 029, 033, 070-074 | hostile-client and direct-access denial tests | authorized operator can still request harmful but valid policy |
| BFW-THR-002 | Malicious or compromised plugin escapes its declared domain | separate process, signed package, permission manifest, generation identity, no peer authority, bounded typed plans | 009-012, 064, 067-068, 077 | malicious-plugin, confused-deputy, restart, and stale-generation tests | native platform bugs below the adapter boundary |
| BFW-THR-003 | Stale process, lease, prepare token, or response is replayed | bind authority to action, actor, target, policy, credential and runtime generations, expiry, and idempotency key | 016-017, 023, 029, 038, 073-074 | replay and generation-rotation tests | clock/source failure requires bounded monotonic handling |
| BFW-THR-004 | Supply-chain compromise substitutes package, UI, schema, image, or evidence | offline root, delegated roles, immutable digests, SBOM/provenance, compatibility admission, rollback protection | 006, 010, 026-031, 039, 079, 089 | signature, digest, expiry, revocation, substitution, and compromised-delegation tests | trusted signer/build system compromise before provenance capture |
| BFW-THR-005 | Secret leaks through config, argv/env, logs, history, UI, exports, support, or provider crossing | keyring authority; non-exporting references; field-aware redaction; deny ambient transfer | 007, 014-018, 022-023, 044, 055, 068, 078 | secret-seeded end-to-end scans and negative provider composition tests | endpoint compromise during an admitted use |
| BFW-THR-006 | Rollback or migration selects attacker-chosen or incompatible state | signed rollback mate, monotonic release rules, verified snapshots, schema compatibility, audit | 002, 006, 031, 039, 074, 089 | downgrade, interrupted migration, corrupted snapshot, and last-known-good tests | latent defect present in both current and rollback state |
| BFW-THR-007 | HA split brain or stale peer causes duplicate ownership | authenticated peers, release/config parity, fencing/quorum, duplicate-owner detection, fail closed | 059-060 | partition, stale peer, asymmetric loss, witness loss, and duplicate-address tests | availability loss is accepted to preserve packet safety |
| BFW-THR-008 | Management policy locks out every remote administrator | candidate config, commit-confirmed timer, independent local console, bounded recovery identity | 004, 033, 049, 074 | management-path removal, lost confirmation, IdP/DNS/cert outage, console recovery | physical console availability is an operational prerequisite |
| BFW-THR-009 | Recovery console is abused as a root or password bypass | local presence, separate protected identity, typed actions, no shell/direct file edits, redacted immutable audit | 004, 033, 049, 078, 089 | remote-unreachability, role limits, audit, brute-force, and direct-mutation denial tests | physical host compromise remains outside software-only protection |
| BFW-THR-010 | Warning, partial apply, or incomplete observation is treated as success and opens traffic | completeness oracle, warning-as-failure, atomic apply where possible, verify before commit, rollback/failed-closed state | 001-003, 005, 012, 038, 052, 085, 090 | boundary, truncation, warning, partial failure, packet oracle, and rollback tests | platforms without atomicity may briefly require conservative blocking rules |
| BFW-THR-011 | Misconfiguration, malicious control frames, or partial apply creates a Layer-2 loop or broadcast storm | typed topology validation, STP-family guards, storm control, ordered apply, convergence oracle, and fail-closed rollback | 091-095, 097 | physical/logical loop, STP manipulation, member loss, storm, convergence, and rollback tests | physical loops can disrupt traffic before detection on platforms without atomic staging |
| BFW-THR-012 | VLAN hopping, native-VLAN mismatch, FDB poisoning/overflow, or offload drift crosses an isolation boundary | explicit ingress/egress tagging, deny ambiguous native VLANs, bounded FDB policy, independent packet/state oracle, and offload parity admission | 092-097, 099 | hostile tag, double-tag, MAC churn, static-FDB conflict, software/offload parity, and leakage tests | compromised switch silicon/firmware remains below the adapter boundary |
| BFW-THR-013 | Switching a management port, VLAN, uplink, or port channel removes every management path | candidate diff, reachability preflight, commit-confirmed, local/OOB recovery, timer persistence, and automatic rollback | 004, 033, 074, 098 | management-VLAN/uplink/member removal, lost confirmation, restart, and console/OOB recovery tests | local/OOB access is an operational prerequisite for high-risk topology changes |
| BFW-THR-014 | Implicit or incomplete role selection leaves unintended Layer-2 or Layer-3 transit authority active | explicit machine-readable profile, admitted component closure, enabled/denied effects, non-transit management addressing, complete native-state oracle, and transactional transition | 100-105 | router/switch/converged selection, latent-forwarding, management-transit, partial transition, restart, and rollback tests | lower-layer platform defects may violate a correctly compiled denial |
| BFW-THR-015 | Layer labels collapse authority or accidentally grant edge/NAT/Layer-7 behavior to Layer-3 switching or Layer-4-aware routing | explicit per-layer effects, separate switching/routing/firewall owners, denied edge effects in switch mode, no implied application authority, and complete observed-state oracle | 102, 106-110 | SVI/routed-port versus edge-route, NAT/state denial, management non-transit, payload/proxy denial, and partial-observation tests | platform classifiers or offload firmware may misclassify packets below the admitted plan |
| BFW-THR-016 | Crafted packets, fragments, streams, encodings, or protocol ambiguity evade detection or make engine and endpoint interpret traffic differently | canonical normalization, bounded reassembly, explicit overlap/checksum/truncation policy, differential endpoint corpora, decoder health, and fail-honest incompleteness | 113, 115, 120-121 | fragmentation, overlap, retransmission, segmentation, checksum/offload, VLAN, encoding, malformed protocol, and evasion corpus/fuzz tests | unknown endpoint quirks and encrypted payloads limit visibility |
| BFW-THR-017 | Malicious or incompatible rules cause false confidence, catastrophic resource use, or silent semantic downgrade | canonical bounded rule IR, safe regex, signed/provenance-bound rules, exact dialect matrix, unsupported-feature rejection, deterministic compile, staged activation, and rollback | 114-116, 121-122 | hostile rule fuzzing, unsupported PCRE/preprocessor/action fixtures, complexity/resource boundaries, signature, expiry, interruption, and rollback tests | supported rules can still produce operationally costly false positives |
| BFW-THR-018 | IDS overload, capture loss, queue overflow, or crash silently creates an inspection gap or changes inline availability policy | loss/backlog/resource accounting, explicit incomplete health, per-zone fail policy, admitted bypass, watchdog, alerting, transactional mode change, and recovery | 112, 115, 119-121 | overload, packet loss, queue saturation, process kill/restart, fail-open/fail-closed, bypass, watchdog, and completeness-oracle tests | fail-open preserves availability with known exposure; fail-closed can deny service |
| BFW-THR-019 | Detection plugin directly blocks traffic or leaks sensitive payload/evidence beyond its authority | typed enforcement proposal, core authorization, firewall-only mutation, deny-default payload/PCAP retention, scoped filesystem authority, redaction, access control, and audit | 117-119 | confused-deputy/direct-mutation denial, payload/PCAP retention, access, export, redaction, expiry, and audit tests | authorized evidence readers may see sensitive traffic content |
| BFW-THR-020 | Fabric partition, stale leader, or split brain accepts conflicting topology, route, or policy generations | cryptographic membership, quorum, term/generation binding, fencing, durable journal, minority write denial, deterministic reconciliation, and duplicate-owner detection | 125-126, 130, 132-135 | asymmetric partition, delayed/reordered messages, stale leader/member, witness loss, restart, duplicate owner, and reconciliation tests | availability is sacrificed when safe ownership cannot be proven |
| BFW-THR-021 | Missing or stale distributed policy placement creates an unintended open path during mobility, convergence, or node loss | canonical generation, deterministic per-node placement, readiness barriers, endpoint identity, unknown-placement deny, node/end-to-end packet oracle, and bounded rollback/isolation | 124, 129-134 | endpoint mobility, node loss, partial placement, asymmetric path, state-owner loss, churn, canary, deadline, and rollback tests | transient loss may be accepted to prevent connectivity widening |
| BFW-THR-022 | Overlay or control-plane forgery injects MAC/IP, route, VNI, next-hop, or membership state | authenticated encrypted peers, explicit enrollment/revocation, typed advertisements, VRF/VNI/route-target scope, mobility sequence, duplicate detection, and current generation | 125, 127-128, 134 | rogue peer, replay, cross-VRF/VNI leak, MAC/IP duplication, stale mobility, route-target, and next-hop tests | compromised admitted node can originate malicious but syntactically valid state |
| BFW-THR-023 | Encapsulation, MTU, hashing, BUM, loop, or offload mismatch causes black holes, duplication, reordering, or policy bypass | end-to-end MTU/PMTU accounting, explicit fragmentation/QoS/ECN/hash/BUM policy, loop prevention, offload parity, loss/ordering telemetry, and packet oracle | 127-131, 134-135 | boundary MTU, encapsulation, ECMP entropy, member loss, BUM storm, loop, offload, reordering, and fragmentation tests | heterogeneous hardware may require conservative feature disablement |
| BFW-THR-024 | Kubernetes controller, API, etcd, CNI, storage, or management-path failure disables forwarding or prevents recovery | native node services, no worker/runtime requirement, forwarding-independent agent, mutation freeze, last-known-good state, local recovery, dedicated/OOB management | 136-142, 144 | total controller/API/etcd/CNI/storage loss, management partition, node restart, autonomous packet/state oracle, controller rebuild | controller loss intentionally removes new centralized mutations until safe recovery |
| BFW-THR-025 | Compromised controller workload, service account, image, CRD, or stale plan gains ambient node/network authority | pinned signed artifacts, least-privilege RBAC/NetworkPolicy/Pod Security, mutual node identity, typed signed generation-bound plans, expiry, node-local authorization and rollback | 139, 141, 143-144 | hostile workload/service account, image substitution, stale/replay, overbroad RBAC, direct node mutation, and secret scans | compromise of a currently admitted controller signer requires revocation and node trust-root recovery |
| BFW-THR-026 | Malformed or spoofed VRRP traffic, timer manipulation, replay, stale generation, or ambiguous peer state causes duplicate virtual-address ownership | strict protocol/state-machine validation, authenticated substrate identity where available, generation binding, duplicate-owner detection, quorum/fencing policy, bounded timers, fail-closed transition | 146, 149, 152-153 | malformed/spoofed packet corpus, timer/clock boundary, replay, partition, duplicate-owner, restart, and interoperable-peer tests | standard VRRP lacks strong peer authentication on some networks and therefore requires trusted-link or separately protected-path admission |
| BFW-THR-027 | Keepalived import, health script, hook, or direct native mutation expands GoKA authority or executes attacker-controlled input | exact subset importer, hard rejection, no shell/hooks/IPVS, typed bounded health, core-authorized effect plans, clean-room/source scans | 145, 147-150, 153 | hostile import fixtures, shell/env/process denial, direct-mutation/confused-deputy tests, dependency/source/license scans | operator may still import semantically harmful values that pass policy and require normal review/commit safeguards |
| BFW-THR-028 | GoKA and Kubernetes coordinators both believe they own one HA domain, producing conflicting generations or failover actions | exact selected profile, one canonical core authority, mutually exclusive coordinator lease/generation, fencing, migration handoff, competing-writer denial | 154-160 | dual-coordinator, stale lease, migration interruption, partition, rollback, and duplicate-owner tests | availability may be sacrificed during ambiguous handoff to preserve single authority |

## Review and lifecycle

Every new component, public contract, external dependency, provider capability,
or recovery path must add or update threats before admission. Threats are
closed only by pinned test evidence and independent review, not by design text.
The initial register is deliberately system-level; each component template
requires a component-specific threat model.
