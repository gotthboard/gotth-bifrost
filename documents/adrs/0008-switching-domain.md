# ADR-0008: First-class Layer-2 switching domain

Status: Accepted

Requirements: BFW-PRD-091 through BFW-PRD-099

## Context

Bifrost was already defined as a firewall and router, while VLANs, bridges, and
LAGs were grouped under generic interface management. A managed switch needs
an explicit authority for forwarding databases, loop prevention, tagging,
aggregation, and hardware semantic gaps. Leaving those behaviors implicit
would collapse port construction, Layer-2 forwarding, routing, and filtering
into one oversized authority and make cross-domain rollback unverifiable.

## Decision

Create `bfw-switching` as a separately versioned foundation plugin. It owns
Layer-2 bridge/VLAN forwarding semantics, FDB, STP/RSTP/MSTP, LACP, isolation,
storm control, multicast snooping, LLDP observations, health, drift, and
rollback effects. `bfw-network` continues to own ports and interfaces,
`bfw-routing` owns Layer-3 routes, and `bfw-firewall` owns filter/NAT policy.

Linux software bridge/VLAN is the v0.1 baseline. Hardware offload and other
operating-system mechanisms are admitted adapter profiles, never assumed
equivalent. Changes spanning these domains use the core transaction contract;
management-path changes require commit-confirmed or proven local/OOB recovery.

## Consequences

- Bifrost is explicitly both a managed switch and router/firewall system.
- The v0.1 profile gains one component and switching-plan schema.
- Platform matrices must describe software and hardware-offload semantics.
- Loop, VLAN-isolation, FDB, STP, LACP, and management-lockout tests become
  admission requirements.
- Physical switch silicon and vendor SDK support remain optional and explicit.

## Alternatives considered

- Keep switching inside `bfw-network`: rejected because link construction and
  Layer-2 forwarding have different authority, failure, and observation models.
- Put switching in `bfw-routing`: rejected because Layer-2 and Layer-3 control
  planes have distinct semantics and platform APIs.
- Require hardware offload in v0.1: rejected because it would make the product
  vendor-specific before the portable software baseline is proven.

## Verification

- governance catalog and v0.1 composition validation
- switching schema strictness and fixture tests
- ownership, cross-domain transaction, loop, VLAN leakage, STP/LACP, observed
  state, semantic-gap, management rollback, and offload-parity test plans
