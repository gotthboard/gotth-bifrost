# Bifrost Product Requirements

Status: initial planning baseline

## Product objective

Build a Go-based firewall and routing appliance for Linux that provides a
coherent administration plane over proven kernel networking facilities. The
system must prioritize safety, deterministic behavior, recoverability, and
clear operational evidence over feature count.

## Initial requirements

- **BFR-PRD-001:** Bifrost shall compile its canonical policy into deterministic
  `nftables` transactions and verify the applied result.
- **BFR-PRD-002:** Configuration changes shall be schema-validated, versioned,
  audited, and recoverable through rollback.
- **BFR-PRD-003:** Failed validation, partial configuration, and uncertain
  runtime state shall fail closed without silently discarding the last
  known-good configuration.
- **BFR-PRD-004:** The management plane shall support explicit network exposure
  controls and a local recovery path.
- **BFR-PRD-005:** Routing, interface, NAT, firewall, DHCP, DNS, and VPN
  integrations shall have explicit ownership boundaries and health evidence.
- **BFR-PRD-006:** Upgrades shall be signed, preflighted, transactional where
  practical, and recoverable after interruption.
- **BFR-PRD-007:** Secrets shall be stored separately from ordinary
  configuration and excluded from logs, exports, and source control.
- **BFR-PRD-008:** Supported Linux distribution, kernel, architecture, and
  appliance-image targets shall be pinned before implementation admission.

## Bootstrap acceptance criteria

- Private `danny/Bifrost` repository exists on Forgejo with default branch
  `main`.
- README states the Go/Linux architecture boundary and planning-only status.
- Canonical PRD, architecture, and implementation specification exist under
  `documents/` in the required order.
- Go module identity is established without executable firewall code.

## Non-goals for this slice

- packet-filter implementation
- web UI or API implementation
- installer or bootable appliance image
- production deployment
- feature-parity claim against OPNsense
