# Shared-foundation implementation plan

This is a checked decomposition, not implementation or runtime admission.
Existing active workflow and minimum safety gates remain authoritative.

1. **Dependency selection:** pin the exact consumer component, upstream GOTTH
   version, toolchain and platform. Review actual API, license and limitations;
   define expected success, denial, outage, migration and rollback behavior.
2. **Identity slice first:** implement `bfw-identity` against `gotth-oidc` in
   its separately versioned component repository. Write contract-based tests
   before implementation. Prove invalid-token/replay denial, keyring custody,
   no implicit roles, core-owned session behavior and offline recovery.
3. **Management slice:** Go/templ + HTMX + Tailwind `bfw-web`, plus the existing
   `bfw` API client. Prove a bounded read/preview/confirmation flow, no-JS use,
   accessibility and authority separation without native packet mutation.
4. **Shared support slices:** add selected portability and release mechanisms;
   add optional jobs/SCIM/notification/Stack adapters only with explicit
   product and deployment contracts. Respect PostgreSQL and public-webhook
   limitations; do not force controller dependencies into standalone nodes.
5. **Compatibility and admission:** map shared extension contracts to the
   sole `rpc-plugin-system` lifecycle. Test generation, expiry, cancellation,
   stale authority and recovery. Record exact dependency edges, revisions,
   evidence and rollback only after independent component admission.
6. **System proof:** run the applicable alpha safety or full Phase 0 gates,
   exact-artifact, platform, end-to-end packet/state, recovery and performance
   checks. Source-library tests and governance validation are not substitutes.

Exit criteria: the selected slice is implemented and independently verified,
dependencies are actually pinned/admitted, and canonical workflow evidence
identifies limits. No completion is inferred from naming, successful imports,
rendered HTML, or a public mirror. Unsupported claims remain blocked.
