# Bifrost Firewall (BFW) Architecture

Status: initial boundary architecture

## Naming boundary

**Bifrost Firewall** is the product name; **BFW** is its canonical acronym and
`bfw` is the lowercase public namespace. Component names must compose beneath
that namespace rather than inventing another product acronym. Internal working
names such as `bifrostd` or `bifrost-web` remain provisional until executable,
service, API, package, and upgrade naming is admitted as one compatibility
contract.

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
- **credential authority:** `agent-keyring` stores and governs secret payloads;
  Bifrost stores only selectors, redacted metadata, opaque-reference
  fingerprints, and audit correlation
- **filesystem provider:** `agent-filesystem` performs scoped, race-safe host
  file operations after core admission; it is not canonical-state authority
- **execution provider:** `agent-exec` performs bounded local process mechanics
  after core admission; it is not shell, privilege, or policy authority
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

## Credential authority

Credential management is a separate trust boundary from action authorization:

```text
browser or operator
  -> unprivileged bifrost-web
  -> bifrostd validates and admits the exact action
  -> agent-keyring issues a scoped, short-lived lease or opaque reference
  -> admitted plugin or host-mediated executor performs the exact use
  -> Bifrost and agent-keyring record correlated, redacted audit evidence
```

`agent-keyring` is the sole credential authority. Bifrost's canonical state may
contain a credential selector and non-secret binding metadata, but never the
secret payload, an exportable private key, a reusable token, or an ambient
credential path. The web UI and ordinary plugins cannot request raw secrets or
talk around core admission.

The core's admission record must exist before keyring access. Every lease or
non-exporting reference is bound to the admitted caller and action, runtime and
provider generations, target and audience, usage and access mode, policy and
credential generations, keyring authority generation, and a short expiry.
Rotation, revocation, restore, restart, or a relevant generation change
invalidates stale authority. Credential possession never substitutes for core
authorization.

Provider operations should prefer non-exporting references. For example, an
ACME or VPN plugin receives authority for one admitted operation without
receiving a reusable account key. Secret-bearing response types, if a future
contract admits them at all, must remain distinct, non-loggable, narrowly
scoped, and unavailable to the web UI.

## Filesystem and execution providers

Bifrost uses `agent-filesystem` for admitted host-file work outside the core's
private canonical state: generated service configuration, bounded imports and
exports, backup artifacts, diagnostics, and support bundles. The core remains
responsible for its own private transactional state and migrations; neither a
plugin nor the web UI receives ambient access to it.

Every file operation carries an admitted root and operation set, byte and
recursion bounds, link and special-file policy, mutation preconditions,
generation/expiry, recovery requirements, and audit correlation. Paths, file
descriptors, trash/COW records, rollback references, and provider-private
storage are never reusable authority. Secret-denied scopes must cover keyring
payload and authority storage.

Bifrost uses `agent-exec` only when an admitted operation genuinely requires a
local process. Native OS APIs remain the preferred path for firewall, routing,
and interface mutations. The execution envelope binds executable identity and
resolution, argv or an explicitly admitted shell payload, cwd, environment,
stdio, timeout/cancellation, process tree, resources, network policy,
filesystem containment, side-effect class, idempotency, generation/expiry, and
audit rules. Cwd is not containment; process reachability is not permission.

Shell execution, PATH lookup, inherited environment, network access, and
privilege transitions are denied unless separately and explicitly admitted.
Credentials are never placed in argv, environment, stdin, output, transcripts,
or diagnostics. If an operation needs credential use, `agent-keyring` supplies
an opaque, scoped authority reference through the admitted mediation contract;
`agent-exec` does not read the keyring or collect passwords.

Multi-provider composition is fail-closed:

```text
one sealed Bifrost action plan
  -> distinct keyring authority use, if required
  -> distinct filesystem authority use, if required
  -> distinct execution authority use, if required
  -> correlated redacted result and audit evidence
```

Each use is bound to the same action, target/audience, policy, correlation, and
current provider/plugin generations. File content does not become a command,
a command result does not become a path, and a provider-owned reference does
not cross a boundary unless the sealed plan explicitly types, bounds, and
admits that transfer.

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

The current `agent-keyring` v1 service also uses a local Unix-domain socket.
Before Bifrost integrates credentials across platforms, the credential
substrate must preserve the same authority semantics across Unix sockets and
Windows named pipes, platform peer identity, encrypted payload storage and
unlock, SDK compatibility, redaction, lease/ref invalidation, backup/restore,
and recovery. Platform storage adapters may protect keyring material, but they
must not become competing sources of credential truth.

The current `agent-filesystem` v1 is a local POSIX provider, and the current
`agent-exec` contract is centered on local Linux/dedicated-account execution.
Before Bifrost depends on them across platforms, their contracts must define
and test Windows and supported BSD/macOS path/process semantics, race-safe path
containment, symlink/reparse-point behavior, atomicity and durability,
trash/recovery semantics, executable identity, account/sandbox/resource
controls, cancellation/process-tree behavior, opaque lifecycle references,
and consistent audit redaction. Unsupported security semantics fail closed;
provider-local compatibility shortcuts are forbidden.

## Recovery

The detailed recovery model is not yet selected. Implementation is blocked
until the project defines local-console recovery, last-known-good selection,
interrupted-upgrade behavior, configuration export/import, and appliance-image
rollback.
