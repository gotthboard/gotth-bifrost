# Router-hosted GOTTH edge services

Date: 2026-10-02. Scope: BFW-PRD-235 through BFW-PRD-240.
Status: product direction and design; no hosted runtime admitted.

## Intent

Bifrost is intended to host selected `gotth-*` services **on the router**, not
merely consume GOTTH libraries during development. Operators can place admitted
applications/extensions at the network edge and expose approved local or LAN
services through an optional Caddy managed by **GOTTH Caddy** (`gotth-caddy`).
Hardware capability, platform support, isolation and dependency admission decide
what can run locally. Off-box service placement remains supported by design;
no router is required to run the entire GOTTH family.

## Distinguish three kinds of reuse

- **Libraries:** OIDC, SCIM, portability and similar mechanisms are imported by
  concrete consumers; repository names alone do not make runnable services.
- **Hosted products/extensions:** selected executable GOTTH products and
  extensions may run as isolated services after their own contracts, artifacts,
  resource budgets, dependencies and recovery are admitted. Placeholders are
  not installable, and even implemented libraries are not deployable products.
- **Infrastructure:** Caddy is a separate HTTP(S) serving process. GOTTH Caddy
  provides its planned UI/API; optional Stack provides unified orchestration.
  A database, identity provider or container runtime is included only if an
  explicitly selected service/profile requires it, never for basic forwarding.

## Ownership and traffic

```text
Internet -> Bifrost firewall/listener admission -> edge Caddy
                                             -> selected router-local service
                                             -> approved LAN service

operator -> GOTTH Caddy UI / optional Stack panel -> scoped Caddy control
operator -> bfw CLI/web -> Bifrost core -> network and host-effect providers
```

Bifrost core and domain plugins retain network, placement, exposure and host
effect authority. Stack orchestrates through scoped product APIs. GOTTH Caddy
owns Caddy-specific presentation and management contracts, while exactly one
selected controller composes each instance: GOTTH Caddy standalone, or Stack in
Stack-managed mode. The latter UI cannot bypass Stack during its outage.
Caddy executes admitted HTTP(S)/TLS configuration. Neither Caddy nor its UI can
claim router administration by publishing a route.

The existing `bfw-reverse-proxy` remains a native Go engine with no Caddy runtime
dependency. Hosting Caddy as a separate optional edge service does not embed or
replace it. One admitted owner holds each address/port; overlapping Caddy,
native proxy, management, ACME or product listeners are rejected before apply.
No default nested proxy chain or public router-management endpoint is implied.
SMTP/IMAP and other non-HTTP protocols remain separately owned/admitted.

## Hosting admission

Every local deployment must declare immutable artifact/dependency/module pins,
platform/hardware support, process identity, filesystem roots, secret references,
listeners, approved service destinations, egress, startup order, persistent data,
backup/migration/rollback and health semantics. Define CPU/memory/process/disk/I/O
and network budgets with reserved router headroom, log bounds, restart/backoff
limits and load-shedding priority. Prove packet forwarding and recovery under
resource exhaustion, service crash, upgrade and dependency loss.

One lifecycle owner is admitted per executable. Bifrost plugins continue under
`rpc-plugin-system`; hosted-service lifecycle mappings must preserve its
contracts and the `agent-keyring`, `agent-filesystem` and `agent-exec` boundaries.
No raw container-engine socket, privileged container or independent host writer
is admitted. Native service versus container packaging is a per-platform design
gate, not a reason to bypass supervision or require Kubernetes on every node.
A workload unable to meet isolation/headroom is rejected or placed off-box.

## Caddy and credentials

[gotth-caddy](https://github.com/gotthboard/gotth-caddy) is a new design-only
project, not an implemented UI or Bifrost dependency. Its scope includes domains,
host/path routes, approved upstreams, TLS/certificate status, health/log views,
validation, preview, confirmation, apply verification and rollback.

Keep Caddy Admin API private and reachable only by an admitted adapter; no
browser access or tenant-provided raw config. Scope owners/hostnames/targets,
reject SSRF, DNS rebinding, metadata/management destinations and proxy cycles,
restrict direct backend access, and preserve other tenants' routes. Verify
cross-host TLS and trusted proxy headers. Assign one certificate lifecycle
owner per termination point; DNS grants and challenge cleanup are scoped.

Caddy requires private TLS/ACME material. Its storage/use model must be mapped
to Bifrost's keyring contract, including restart/unlock, rotation, revocation,
backup and recovery. Stock Caddy is not assumed to support opaque keyring
handles. No new raw-secret exception is granted here; unresolved compatibility
blocks that router profile, not independent documentation or off-box design.

## Failure behavior and implementation sequence

Forwarding, last-known-good firewall/routes, commit-confirmed rollback and
console recovery are independent of hosted services, Stack, databases and
remote identity. Caddy continues its last valid HTTP(S) configuration across
management outage where runtime/keys/certificates/upstreams permit; Caddy failure
may interrupt those web routes. Certificate expiry and shared hardware are real
limits, so this is neither an HA nor indefinite availability promise.

1. Finish eligible existing Bifrost design work without changing alpha/Phase 0.
2. Define one exact edge-hosting profile and a scoped host adapter; first prove
   placement/listener/resource admission with no unauthorized network effects.
3. Implement GOTTH Caddy's read-only UI then one safe route on a disposable
   server profile; validate single-writer and restart/rollback semantics.
4. Admit Caddy credential use and the exact Bifrost hosting profile, then test
   router-local and approved LAN backends, resource exhaustion and outages.
5. Add other GOTTH services individually with compatibility and recovery proof.

This updates product scope, not v0.1/alpha release contents or active workflow.
All new requirements and `gotth-caddy` remain not admitted. The existing GOTTH
identity-library slice remains useful but is not the whole edge-hosting goal.
