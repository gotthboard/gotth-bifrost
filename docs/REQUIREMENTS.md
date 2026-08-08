# Bifrost requirement trace

Generated from `governance/requirements.toml`; do not edit by hand.

| Requirement | Owner | Status | Blockers | Admission |
| --- | --- | --- | --- | --- |
| BFW-PRD-000 | `meta` | defined | none | not_admitted |
| BFW-PRD-001 | `bfw-core` | defined | `BFW-PHASE-0` | not_admitted |
| BFW-PRD-002 | `bfw-core` | defined | `BFW-PHASE-0` | not_admitted |
| BFW-PRD-003 | `bfw-core` | defined | `BFW-PHASE-0` | not_admitted |
| BFW-PRD-004 | `bfw-core` | defined | `BFW-PHASE-0` | not_admitted |
| BFW-PRD-005 | `bfw-core` | defined | `BFW-PHASE-0` | not_admitted |
| BFW-PRD-006 | `bfw-updater` | defined | `BFW-PRD-089`, `BFW-PHASE-0` | not_admitted |
| BFW-PRD-007 | `bfw-core` | defined | `agent-keyring` | not_admitted |
| BFW-PRD-008 | `meta` | defined | `BFW-PRD-090` | not_admitted |
| BFW-PRD-009 | `bfw-core` | defined | `rpc-plugin-system` | not_admitted |
| BFW-PRD-010 | `bfw-core` | defined | `rpc-plugin-system` | not_admitted |
| BFW-PRD-011 | `bfw-plugin-sdk` | defined | `rpc-plugin-system` | not_admitted |
| BFW-PRD-012 | `bfw-core` | defined | `rpc-plugin-system` | not_admitted |
| BFW-PRD-013 | `rpc-plugin-system` | blocked | `rpc-plugin-system` | not_admitted |
| BFW-PRD-014 | `agent-keyring` | defined | `agent-keyring` | not_admitted |
| BFW-PRD-015 | `bfw-core` | defined | `agent-keyring` | not_admitted |
| BFW-PRD-016 | `agent-keyring` | defined | `agent-keyring` | not_admitted |
| BFW-PRD-017 | `agent-keyring` | defined | `agent-keyring` | not_admitted |
| BFW-PRD-018 | `agent-keyring` | blocked | `agent-keyring`, `rpc-plugin-system` | not_admitted |
| BFW-PRD-019 | `agent-filesystem` | defined | `agent-filesystem` | not_admitted |
| BFW-PRD-020 | `agent-filesystem` | defined | `agent-filesystem` | not_admitted |
| BFW-PRD-021 | `agent-exec` | defined | `agent-exec` | not_admitted |
| BFW-PRD-022 | `agent-exec` | defined | `agent-exec` | not_admitted |
| BFW-PRD-023 | `bfw-core` | defined | `agent-keyring`, `agent-filesystem`, `agent-exec` | not_admitted |
| BFW-PRD-024 | `meta` | blocked | `agent-filesystem`, `agent-exec`, `rpc-plugin-system` | not_admitted |
| BFW-PRD-025 | `bfw-web` | defined | `bfw-core` | not_admitted |
| BFW-PRD-026 | `bfw-plugin-sdk` | defined | `bfw-core` | not_admitted |
| BFW-PRD-027 | `bfw-core` | defined | `bfw-plugin-sdk` | not_admitted |
| BFW-PRD-028 | `bfw-web` | defined | `bfw-plugin-sdk` | not_admitted |
| BFW-PRD-029 | `bfw-core` | defined | `bfw-web` | not_admitted |
| BFW-PRD-030 | `bfw-web` | defined | `bfw-plugin-sdk` | not_admitted |
| BFW-PRD-031 | `bfw-core` | defined | `bfw-plugin-sdk` | not_admitted |
| BFW-PRD-032 | `bfw-core` | defined | `bfw-plugin-sdk` | not_admitted |
| BFW-PRD-033 | `bfw-cli` | defined | `bfw-core` | not_admitted |
| BFW-PRD-034 | `bfw-core` | defined | `bfw-web`, `bfw-plugin-sdk` | not_admitted |
| BFW-PRD-035 | `meta` | defined | none | not_admitted |
| BFW-PRD-036 | `meta` | defined | none | not_admitted |
| BFW-PRD-037 | `bfw-routing` | defined | `BFW-PHASE-0` | not_admitted |
| BFW-PRD-038 | `bfw-routing` | defined | `BFW-PHASE-0` | not_admitted |
| BFW-PRD-039 | `meta` | active | `BFW-PRD-079`, `BFW-PRD-089` | not_admitted |
| BFW-PRD-040 | `bfw-identity` | defined | `BFW-PHASE-0` | not_admitted |
| BFW-PRD-041 | `bfw-identity` | defined | `BFW-PHASE-0` | not_admitted |
| BFW-PRD-042 | `bfw-identity` | defined | `BFW-PHASE-0` | not_admitted |
| BFW-PRD-043 | `bfw-core` | defined | `bfw-identity` | not_admitted |
| BFW-PRD-044 | `bfw-identity` | defined | `agent-keyring` | not_admitted |
| BFW-PRD-045 | `bfw-identity` | defined | `bfw-core` | not_admitted |
| BFW-PRD-046 | `bfw-core` | defined | `bfw-identity` | not_admitted |
| BFW-PRD-047 | `bfw-identity` | defined | `bfw-reverse-proxy` | not_admitted |
| BFW-PRD-048 | `bfw-identity` | defined | `bfw-core` | not_admitted |
| BFW-PRD-049 | `bfw-core` | defined | `BFW-PRD-089` | not_admitted |
| BFW-PRD-050 | `bfw-identity` | defined | `bfw-core` | not_admitted |
| BFW-PRD-051 | `meta` | active | `BFW-PRD-079` | not_admitted |
| BFW-PRD-052 | `bfw-core` | defined | `bfw-firewall`, `bfw-network`, `bfw-switching`, `bfw-routing` | not_admitted |
| BFW-PRD-053 | `bfw-plugin-sdk` | defined | `BFW-PHASE-0` | not_admitted |
| BFW-PRD-054 | `bfw-wireguard` | defined | `BFW-PHASE-0` | not_admitted |
| BFW-PRD-055 | `bfw-wireguard` | defined | `agent-keyring` | not_admitted |
| BFW-PRD-056 | `bfw-wireguard` | defined | `bfw-firewall`, `bfw-routing` | not_admitted |
| BFW-PRD-057 | `bfw-reverse-proxy` | defined | `BFW-PHASE-0` | not_admitted |
| BFW-PRD-058 | `bfw-reverse-proxy` | defined | `bfw-dns`, `bfw-acme`, `bfw-firewall`, `agent-keyring` | not_admitted |
| BFW-PRD-059 | `bfw-ha` | defined | `BFW-PHASE-0` | not_admitted |
| BFW-PRD-060 | `bfw-ha` | defined | `bfw-network`, `bfw-routing`, `bfw-firewall` | not_admitted |
| BFW-PRD-061 | `bfw-plugin-sdk` | defined | `BFW-PHASE-0` | not_admitted |
| BFW-PRD-062 | `bfw-plugin-sdk` | defined | `BFW-PHASE-0` | not_admitted |
| BFW-PRD-063 | `bfw-plugin-sdk` | defined | `BFW-PHASE-0` | not_admitted |
| BFW-PRD-064 | `bfw-core` | defined | `bfw-plugin-sdk` | not_admitted |
| BFW-PRD-065 | `meta` | active | `BFW-PRD-090` | not_admitted |
| BFW-PRD-066 | `meta` | defined | `BFW-PRD-087` | not_admitted |
| BFW-PRD-067 | `bfw-plugin-sdk` | defined | `bfw-web`, `bfw-cli` | not_admitted |
| BFW-PRD-068 | `bfw-core` | defined | `agent-keyring`, `agent-filesystem`, `agent-exec` | not_admitted |
| BFW-PRD-069 | `bfw-cli` | defined | `bfw-core` | not_admitted |
| BFW-PRD-070 | `bfw-cli` | defined | `bfw-core` | not_admitted |
| BFW-PRD-071 | `bfw-cli` | defined | `bfw-plugin-sdk` | not_admitted |
| BFW-PRD-072 | `bfw-cli` | defined | `bfw-core` | not_admitted |
| BFW-PRD-073 | `bfw-cli` | defined | `bfw-core` | not_admitted |
| BFW-PRD-074 | `bfw-cli` | defined | `bfw-core` | not_admitted |
| BFW-PRD-075 | `bfw-cli` | defined | `bfw-core` | not_admitted |
| BFW-PRD-076 | `bfw-cli` | defined | `bfw-plugin-sdk` | not_admitted |
| BFW-PRD-077 | `bfw-cli` | defined | `bfw-plugin-sdk` | not_admitted |
| BFW-PRD-078 | `bfw-cli` | defined | `bfw-core` | not_admitted |
| BFW-PRD-079 | `meta` | verified | none | not_admitted |
| BFW-PRD-080 | `meta` | verified | none | not_admitted |
| BFW-PRD-081 | `meta` | verified | none | not_admitted |
| BFW-PRD-082 | `meta` | verified | `rpc-plugin-system`, `agent-keyring`, `agent-filesystem`, `agent-exec` | not_admitted |
| BFW-PRD-083 | `meta` | verified | none | not_admitted |
| BFW-PRD-084 | `meta` | verified | none | not_admitted |
| BFW-PRD-085 | `bfw-core` | verified | `BFW-PHASE-0` | not_admitted |
| BFW-PRD-086 | `meta` | verified | none | not_admitted |
| BFW-PRD-087 | `meta` | verified | `BFW-PHASE-0` | not_admitted |
| BFW-PRD-088 | `meta` | verified | none | not_admitted |
| BFW-PRD-089 | `meta` | verified | `BFW-PHASE-0` | not_admitted |
| BFW-PRD-090 | `meta` | verified | none | not_admitted |
| BFW-PRD-091 | `meta` | verified | `BFW-PHASE-0` | not_admitted |
| BFW-PRD-092 | `bfw-switching` | verified | `BFW-PHASE-0` | not_admitted |
| BFW-PRD-093 | `bfw-switching` | verified | `BFW-PHASE-0` | not_admitted |
| BFW-PRD-094 | `bfw-switching` | verified | `BFW-PHASE-0` | not_admitted |
| BFW-PRD-095 | `bfw-core` | verified | `bfw-network`, `bfw-switching`, `bfw-routing`, `bfw-firewall` | not_admitted |
| BFW-PRD-096 | `bfw-switching` | verified | `bfw-platform-linux`, `bfw-platform-freebsd`, `bfw-platform-windows` | not_admitted |
| BFW-PRD-097 | `bfw-switching` | verified | `BFW-PHASE-0` | not_admitted |
| BFW-PRD-098 | `bfw-switching` | verified | `bfw-cli`, `bfw-network` | not_admitted |
| BFW-PRD-099 | `meta` | verified | `bfw-switching` | not_admitted |
| BFW-PRD-100 | `meta` | verified | `BFW-PHASE-0` | not_admitted |
| BFW-PRD-101 | `bfw-core` | verified | `bfw-network`, `bfw-routing`, `bfw-firewall` | not_admitted |
| BFW-PRD-102 | `bfw-core` | verified | `bfw-network`, `bfw-switching`, `bfw-routing` | not_admitted |
| BFW-PRD-103 | `bfw-core` | verified | `bfw-network`, `bfw-switching`, `bfw-routing`, `bfw-firewall` | not_admitted |
| BFW-PRD-104 | `bfw-core` | verified | `bfw-cli`, `BFW-PHASE-0` | not_admitted |
| BFW-PRD-105 | `meta` | verified | `BFW-PRD-065`, `BFW-PRD-087` | not_admitted |
| BFW-PRD-106 | `bfw-switching` | verified | `bfw-network`, `bfw-routing` | not_admitted |
| BFW-PRD-107 | `bfw-routing` | verified | `bfw-switching`, `bfw-network` | not_admitted |
| BFW-PRD-108 | `bfw-core` | verified | `bfw-routing`, `bfw-firewall` | not_admitted |
| BFW-PRD-109 | `bfw-core` | verified | `bfw-routing`, `bfw-firewall` | not_admitted |
| BFW-PRD-110 | `meta` | verified | `BFW-PRD-065`, `BFW-PHASE-0` | not_admitted |
| BFW-PRD-111 | `bfw-ids` | verified | `BFW-PHASE-0` | not_admitted |
| BFW-PRD-112 | `bfw-ids` | verified | `bfw-network`, `bfw-firewall` | not_admitted |
| BFW-PRD-113 | `bfw-ids` | verified | `BFW-PHASE-0` | not_admitted |
| BFW-PRD-114 | `bfw-ids` | verified | `bfw-plugin-sdk` | not_admitted |
| BFW-PRD-115 | `bfw-ids` | verified | `BFW-PHASE-0` | not_admitted |
| BFW-PRD-116 | `bfw-ids` | verified | `agent-keyring`, `agent-filesystem` | not_admitted |
| BFW-PRD-117 | `bfw-ids` | verified | `agent-filesystem`, `bfw-logging` | not_admitted |
| BFW-PRD-118 | `bfw-ids` | verified | `bfw-core`, `bfw-firewall` | not_admitted |
| BFW-PRD-119 | `bfw-ids` | verified | `bfw-network`, `bfw-firewall` | not_admitted |
| BFW-PRD-120 | `bfw-ids` | verified | `bfw-platform-linux`, `bfw-platform-freebsd`, `bfw-platform-windows` | not_admitted |
| BFW-PRD-121 | `bfw-ids` | verified | `BFW-PHASE-0` | not_admitted |
| BFW-PRD-122 | `meta` | verified | `bfw-ids` | not_admitted |
| BFW-PRD-123 | `meta` | verified | `bfw-fabric` | not_admitted |
| BFW-PRD-124 | `bfw-fabric` | verified | `bfw-switching`, `bfw-routing`, `bfw-firewall` | not_admitted |
| BFW-PRD-125 | `bfw-fabric` | verified | `rpc-plugin-system`, `agent-keyring`, `BFW-PHASE-0` | not_admitted |
| BFW-PRD-126 | `bfw-fabric` | verified | `bfw-ha`, `BFW-PHASE-0` | not_admitted |
| BFW-PRD-127 | `bfw-fabric` | verified | `bfw-network`, `bfw-switching`, `bfw-frr` | not_admitted |
| BFW-PRD-128 | `bfw-fabric` | verified | `bfw-routing`, `bfw-frr` | not_admitted |
| BFW-PRD-129 | `bfw-fabric` | verified | `bfw-firewall`, `bfw-routing` | not_admitted |
| BFW-PRD-130 | `bfw-fabric` | verified | `bfw-ha`, `bfw-switching`, `bfw-routing`, `bfw-firewall` | not_admitted |
| BFW-PRD-131 | `bfw-fabric` | verified | `bfw-network`, `bfw-switching`, `bfw-routing` | not_admitted |
| BFW-PRD-132 | `bfw-core` | verified | `bfw-fabric`, `bfw-ha` | not_admitted |
| BFW-PRD-133 | `bfw-fabric` | verified | `bfw-firewall`, `bfw-ha` | not_admitted |
| BFW-PRD-134 | `bfw-fabric` | verified | `bfw-monitoring`, `bfw-logging` | not_admitted |
| BFW-PRD-135 | `meta` | verified | `bfw-fabric`, `BFW-PRD-090` | not_admitted |
| BFW-PRD-136 | `meta` | verified | `bfw-kubernetes-controller` | not_admitted |
| BFW-PRD-137 | `bfw-kubernetes-controller` | verified | `BFW-PHASE-0` | not_admitted |
| BFW-PRD-138 | `bfw-core` | verified | `bfw-kubernetes-controller`, `bfw-ha` | not_admitted |
| BFW-PRD-139 | `bfw-kubernetes-controller` | verified | `rpc-plugin-system`, `BFW-PHASE-0` | not_admitted |
| BFW-PRD-140 | `bfw-kubernetes-controller` | verified | `bfw-ha` | not_admitted |
| BFW-PRD-141 | `bfw-kubernetes-controller` | verified | `rpc-plugin-system`, `agent-keyring` | not_admitted |
| BFW-PRD-142 | `bfw-core` | verified | `bfw-network`, `bfw-kubernetes-controller` | not_admitted |
| BFW-PRD-143 | `meta` | verified | `bfw-kubernetes-controller`, `BFW-PHASE-0` | not_admitted |
| BFW-PRD-144 | `meta` | verified | `bfw-kubernetes-controller`, `BFW-PRD-090` | not_admitted |
| BFW-PRD-145 | `bfw-ha` | verified | `BFW-PHASE-0` | not_admitted |
| BFW-PRD-146 | `bfw-ha` | verified | `bfw-network` | not_admitted |
| BFW-PRD-147 | `bfw-ha` | verified | `bfw-network`, `bfw-routing`, `bfw-firewall` | not_admitted |
| BFW-PRD-148 | `bfw-ha` | verified | `rpc-plugin-system` | not_admitted |
| BFW-PRD-149 | `bfw-ha` | verified | `BFW-PHASE-0` | not_admitted |
| BFW-PRD-150 | `bfw-ha` | verified | `BFW-PRD-145` | not_admitted |
| BFW-PRD-151 | `bfw-ha` | verified | `bfw-platform-linux`, `bfw-platform-freebsd`, `bfw-platform-windows` | not_admitted |
| BFW-PRD-152 | `bfw-ha` | verified | `bfw-monitoring`, `bfw-logging` | not_admitted |
| BFW-PRD-153 | `meta` | verified | `bfw-ha`, `BFW-PRD-090` | not_admitted |
| BFW-PRD-154 | `meta` | verified | `bfw-ha`, `bfw-kubernetes-controller` | not_admitted |
| BFW-PRD-155 | `bfw-core` | verified | `bfw-ha`, `bfw-kubernetes-controller` | not_admitted |
| BFW-PRD-156 | `bfw-ha` | verified | `BFW-PHASE-0` | not_admitted |
| BFW-PRD-157 | `bfw-kubernetes-controller` | verified | `BFW-PHASE-0` | not_admitted |
| BFW-PRD-158 | `bfw-core` | verified | `bfw-ha`, `bfw-kubernetes-controller` | not_admitted |
| BFW-PRD-159 | `bfw-core` | verified | `bfw-ha`, `bfw-kubernetes-controller` | not_admitted |
| BFW-PRD-160 | `meta` | verified | `bfw-ha`, `bfw-kubernetes-controller` | not_admitted |
| BFW-PRD-161 | `meta` | verified | `BFW-PRD-087`, `BFW-PRD-090` | not_admitted |
