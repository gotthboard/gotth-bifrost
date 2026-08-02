# Bifrost Architecture

Status: initial boundary architecture

## Control and data planes

The Linux kernel is the data plane. Bifrost's Go services form the control and
management planes: they validate desired configuration, compile deterministic
runtime transactions, apply them through narrow adapters, verify observed
state, and preserve audit and rollback evidence.

```text
operator / API
  -> authenticated management plane
  -> versioned desired configuration
  -> validation and policy compiler
  -> transactional runtime adapters
  -> nftables / netlink / supervised network services
  -> observed-state verification and audit
```

## Proposed boundaries

- **configuration core:** canonical schemas, revisions, migrations, validation,
  and rollback
- **policy compiler:** pure desired-state conversion into reviewable firewall,
  NAT, and routing plans
- **runtime adapters:** narrow `nftables`, netlink, service, VPN, DHCP, and DNS
  integration surfaces
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

## Recovery

The detailed recovery model is not yet selected. Implementation is blocked
until the project defines local-console recovery, last-known-good selection,
interrupted-upgrade behavior, configuration export/import, and appliance-image
rollback.
