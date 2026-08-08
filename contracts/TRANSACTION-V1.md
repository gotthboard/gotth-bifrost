# Bifrost cross-component transaction contract v1 draft

Contract identifier: `bfw.transaction/v1-draft`

Requirements: BFW-PRD-001 through BFW-PRD-005, BFW-PRD-023, BFW-PRD-029,
BFW-PRD-038, BFW-PRD-052, BFW-PRD-074, BFW-PRD-085, BFW-PRD-095,
BFW-PRD-098

The JSON envelope is defined by `schemas/v1/transaction.schema.json`. This
document defines the state machine and authority rules that syntax alone cannot
express.

## Invariants

- The core is the only transaction coordinator and commit authority.
- Each participant owns only its typed domain effects.
- A transaction binds actor and authorization generation, base configuration
  generation, target release composition, participant generations, deadline,
  idempotency keys, and last-known-good record.
- Prepare tokens are opaque, single-transaction, single-generation,
  non-transferable fingerprints; they are not ambient capability.
- No successful-looking partial result is commit evidence.

## State machine

```text
candidate
  -> validating
  -> prepared
  -> applying
  -> verifying
  -> committed

any pre-commit failure
  -> rolling_back
  -> rolled_back | failed_closed
```

1. **Validate:** Pure schema, authorization, dependency, compatibility,
   platform-semantic, conflict, resource-bound, and cross-domain validation.
   No participant may mutate native state.
2. **Prepare:** Participants resolve current identity/generation and return
   bounded preconditions, predicted effects, verification oracles, rollback
   plans, and opaque prepare-token fingerprints. Preparation is read-only or
   uses explicitly disposable staging.
3. **Apply:** The coordinator dispatches the immutable ordered plan. Every step
   is idempotent under its transaction and step key. A participant rejects a
   changed generation, stale token, wrong target, or repeated key with changed
   operands.
4. **Verify:** Independent observed-state and packet/service completeness
   oracles prove the entire plan. Warnings, truncation, unknown state, missing
   end markers, or unhealthy required dependencies are failures.
5. **Commit:** Only after verification does the core atomically make the target
   configuration generation current and append the audit/transaction record.
6. **Rollback:** Reverse applied reversible steps in declared order and verify
   the recorded last-known-good release/configuration pair. Irreversible effects
   require explicit pre-admission and a compensating recovery plan. If safe
   restoration cannot be proved, enter `failed_closed` and preserve evidence.

## Concurrency and recovery

One configuration generation has at most one committing transaction. Parallel
read-only validation is allowed; commits use compare-and-swap against the base
generation. Coordinator restart reconstructs state from an append-only journal
and participant observations; it never guesses success from a missing reply.
Unknown in-flight state resumes verification or rollback under the original
transaction identity. Expired transactions cannot be revived with new tokens.

## Provider composition

Keyring, filesystem, and execution uses are separate transaction participants
with individually scoped authority. Secret bytes do not become plan data, file
content does not become argv, command output does not become a path, and opaque
provider references never cross boundaries unless a versioned typed transfer
contract explicitly permits that exact use.

## Required tests

- every phase success and denial transition
- stale base, actor, participant, provider, policy, and credential generations
- duplicate idempotency key with same and changed operands
- participant crash before/after apply, lost reply, timeout, cancellation, and
  coordinator restart at every phase
- forward apply and reverse rollback order across firewall, network, switching,
  routing,
  DNS/DHCP, VPN, HA, keyring, filesystem, and execution participants
- warning/partial-result rejection and independent completeness oracles
- rollback failure and verified failed-closed packet behavior
