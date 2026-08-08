# Cold review 2: operations, recovery, and completeness

Decision: PASS

Scope: v0.1 composition, Linux software baseline, management recovery,
observed state, platform gaps, test lab, traceability, and validator behavior.

Findings:

- `bfw-switching` is present exactly once in the catalog and v0.1 included set,
  absent from deferred, and ordered after network and before routing.
- The contract covers access/trunk/native VLANs, bridges, FDB, STP/RSTP/MSTP,
  LACP, isolation, storm control, IGMP/MLD snooping, and LLDP observations.
- Management VLAN/uplink changes require commit-confirmed or proven local/OOB
  recovery, with verification and automatic rollback before lockout.
- Test-lab roles and scenarios cover independent traffic observation, loops,
  isolation, convergence, member loss, FDB lifecycle, storm, snooping, recovery,
  and optional software/offload parity.
- Requirement, verification-map, trace-registry, component, release, schema,
  ADR, workflow, and generated-view validation reconcile without drift.

No blocking design defect was found. Passing these governance checks does not
claim that a switch implementation or native behavior has passed.
