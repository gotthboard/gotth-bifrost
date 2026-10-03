# Router edge-service implementation plan

Follow the ordered sequence in [EDGE-SERVICES.md](../../../documents/EDGE-SERVICES.md).
Select one bounded deployment profile, then prove scoped placement, listeners,
resource reservations, credential custody and recovery with a single Caddy
route before adding more services. GOTTH Caddy owns its own UI implementation.

Required proof: immutable profile and service closure; one lifecycle/config
writer; no unauthorized host/network effects; unrelated-route preservation;
resource exhaustion and controller/service/dependency loss; restart and unknown
outcome reconciliation; native packet/state and local recovery continuity.
Caddy and the native BFW proxy remain distinct with explicit listener conflicts.

All steps are pending. The active workflow and alpha/Phase 0 gates are unchanged.
