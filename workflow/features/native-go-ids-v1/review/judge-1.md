# Cold review 1: IDS authority, safety, and failure semantics

Decision: PASS

Scope: BFW-PRD-111 through BFW-PRD-122, `bfw-ids` catalog boundary,
IDS-plan schema, ADR-0011, architecture, threats, and lab requirements.

Findings:

- `bfw-ids` owns observation, reconstruction, decoding, matching, alerts, and
  enforcement proposals but cannot mutate firewall, routing, switching,
  interface, file, credential, or process state directly.
- Passive IDS and inline IPS are distinct; the schema requires inline policy
  only for inline mode and requires it to be absent/null for passive mode.
- Inline fail-open/fail-closed, bypass, queue bounds, watchdog, health, and
  recovery are explicit per-zone policy rather than hidden runtime defaults.
- Packet loss, truncation, overload, unknown decode, and incomplete inspection
  are first-class failure/health facts and cannot look like complete success.
- Payload and PCAP retention is opt-in, bounded, access-controlled, redacted,
  and separately audited.
- Enforcement remains core-authorized and firewall-applied through a typed
  transaction, preventing a detection plugin from becoming policy authority.

No authority collapse, silent failover, unbounded evidence path, runtime code,
or release/admission claim was found.
