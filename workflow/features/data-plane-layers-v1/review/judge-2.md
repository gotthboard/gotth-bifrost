# Cold review 2: profile completeness, failure, and verification

Decision: PASS

Scope: exact component closures, layer/effect declarations, v0.1 language,
test-lab scenarios, transition/recovery behavior, traceability, and checks.

Findings:

- Machine profiles declare exact layer sets: router `{3,4}`, switch `{2,3}`,
  and converged `{2,3,4}`.
- Switch component closure includes network, switching, and routing; converged
  includes their union with firewall.
- Test scenarios distinguish SVI/inter-VLAN/routed-port/local-fabric behavior
  from WAN edge behavior and cover TCP/UDP state, NAT, port forwarding,
  management non-transit, and denial of implied Layer-7 authority.
- Missing, unsupported, or partially observed required behavior rejects
  activation and preserves last-known-good state.
- PRD, architecture, implementation map, profile metadata, schema, ADR, threat,
  test lab, workflow, and validator are consistent.

No blocking design defect was found. Native packet-path evidence remains absent
and is not claimed by the governance pass.
