# Bifrost Architecture

Status: initial boundary architecture

## Control and data planes

The native operating-system networking stack is the data plane. Bifrost's
portable Go services form the control and management planes: they validate
desired configuration, compile a platform-neutral policy IR, admit plugin use,
apply deterministic runtime transactions through narrow platform adapters,
verify observed state, and preserve audit and rollback evidence.

```text
operator / API
  -> authenticated management plane
  -> versioned desired configuration
  -> validation and platform-neutral policy IR
  -> admitted platform/service plugin
  -> native transactional runtime adapter
  -> nftables/netlink, pf, WFP, or supervised network service
  -> observed-state verification and audit
```

## Proposed boundaries

- **configuration core:** canonical schemas, revisions, migrations, validation,
  and rollback
- **policy compiler:** pure desired-state conversion into reviewable,
  platform-neutral firewall, NAT, and routing plans
- **platform adapters:** narrow Linux, FreeBSD, Windows, and later platform
  translation and apply/verify surfaces
- **plugin catalog:** signed manifests, package provenance, compatibility,
  declared permissions, migrations, enable/disable state, and rollback
- **plugin supervisor:** separate-process lifecycle, generation identity,
  authentication, health, failure isolation, routing, and append-only logs
- **reconciler:** idempotent apply/verify loop with explicit drift handling
- **management API:** authenticated authorization boundary; no direct shell
  execution
- **web UI:** API client only; it never becomes configuration authority
- **evidence plane:** audit events, metrics, logs, diagnostics, and support
  bundles with secret redaction

## Safety invariants

- Configuration is not committed as current until validation and required
  runtime verification succeed.
- Runtime changes use atomic transactions where the subsystem supports them.
- A failed candidate leaves or restores the last known-good state.
- Management-access changes require a confirmation timer or local recovery
  mechanism before becoming permanent.
- Service and kernel warnings are failures when they imply incomplete policy.
- Plugin presence or capability advertisement is not permission; core admits
  each privileged operation against the declared contract.
- Plugin or supervisor failure leaves native last-known-good policy active.

## Plugin architecture

```text
Bifrost portable core
  -> admitted plugin contract
  -> cross-platform rpc-plugin-system substrate
  -> platform backend or optional service executable
  -> native OS/service API
```

The Bifrost contract owns domain meaning: schemas, desired state, policy IR,
permissions, idempotency, transaction results, and rollback consequences. The
`rpc-plugin-system` substrate owns executable lifecycle and trust facts. It must
not become firewall-policy authority.

Candidate plugin classes:

- platform firewall/routing/interface backends
- DHCP and DNS services
- VPN providers
- IDS/IPS and traffic-analysis services
- high-availability and configuration synchronization
- dynamic DNS, ACME, monitoring, backup, and support tooling

Core configuration, admission, audit, package verification, and recovery remain
non-optional. Plugins cannot replace or weaken them.

## Cross-platform substrate prerequisite

The current `rpc-plugin-system` v1 contract uses Unix-domain sockets, Go
`net/rpc`/gob, and Linux `SO_PEERCRED` hardening. Bifrost must not fork that
contract inside provider plugins. Before Bifrost depends on it across platforms,
the substrate must define and test:

- Unix-domain-socket and Windows-named-pipe transports behind one standard
- Linux, BSD/macOS, and Windows peer-identity adapters
- explicit protocol and capability-version negotiation
- an externally consumable, versioned SDK/module
- matching generation, auth, timeout, cancellation, logging, and teardown
  behavior on every supported platform

This substrate is a predecessor project, not a parallel convenience task.
Bifrost design and interface planning may continue, but runtime implementation
is blocked until the cross-platform substrate is complete and independently
admitted. Bifrost must not carry provider-local transport, authentication,
generation, lifecycle, or supervision forks as a shortcut.

## Recovery

The detailed recovery model is not yet selected. Implementation is blocked
until the project defines local-console recovery, last-known-good selection,
interrupted-upgrade behavior, configuration export/import, and appliance-image
rollback.
