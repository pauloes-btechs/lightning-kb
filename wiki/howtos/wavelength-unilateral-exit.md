---
title: 'Leaving Ark: unilateral exit'
type: howto
sources:
  - raw/wavelength/guides/unilateral-exit.md
  - raw/wavelength/concepts/leaving-ark.md
updated: 2026-11-14
---

# Leaving Ark: unilateral exit

Every VTXO in [[wavelength]] leaves Ark one of two ways: a cooperative leave the operator settles in the next round, or a unilateral exit forced on-chain by the user. The React hooks are `useWalletExit` (one outpoint), `useWalletExitBatch` (several), `useWalletExitPlan`, `useWalletExitStatus`, `useWalletExits`, and `useWalletSweep`. ([source](../../raw/wavelength/guides/unilateral-exit.md))

Background on VTXOs and rounds is on [[wavelength-concepts]]; everyday sends are on [[wavelength-wallet-guides]].

## Choose the path

A **cooperative leave** forfeits selected VTXOs in an operator round, and the batch includes a leave output paying the destination address. The operator co-signs, so it settles in roughly one round cadence instead of waiting for CSV timelocks. It is the default for `prepareSend` / `send` with `onchainAddress` and for `exit({ outpoint, destination })`; activity shows kind `exit` (or a `send` on the on-chain rail) and the exit result's path is `cooperative`. It requires a live, honest operator. ([source](../../raw/wavelength/concepts/leaving-ark.md))

A **unilateral exit** (unilateral unroll) broadcasts the pre-signed Virtual Transaction Tree branch for a VTXO without operator cooperation, then walks proof and checkpoint transactions until the funds are plain UTXOs. It is slow and expensive: CSV delays must mature, multiple on-chain transactions may be needed, and a backing wallet may need funding for fees. ([source](../../raw/wavelength/concepts/leaving-ark.md))

| Situation | Prefer |
| --- | --- |
| User taps "Withdraw to my exchange address" | Cooperative leave |
| Operator online, routine payout | Cooperative leave |
| Operator unresponsive or dishonest | Unilateral exit |
| User needs funds soon and network is healthy | Cooperative leave |
| User accepts higher fees and multi-block delays for trustlessness | Unilateral exit |

([source](../../raw/wavelength/concepts/leaving-ark.md))

Unilateral exit is irreversible once broadcast and can cost many times the fee of a cooperative leave; the docs say to preview `getExitPlan({ outpoints })`, explain delays, and never trigger it silently from a primary "Send" button. ([source](../../raw/wavelength/concepts/leaving-ark.md))

## Opt in with FORCE_UNROLL_ACK

Calling `exit({ outpoint })` with no `forceUnrollAck` is a cooperative leave. A cooperative failure rejects the call and never silently starts a unilateral exit. Starting a unilateral exit requires the exported `FORCE_UNROLL_ACK` constant, and `destination` (cooperative) and `forceUnrollAck` (unilateral) are mutually exclusive on `ExitRequest`. ([source](../../raw/wavelength/guides/unilateral-exit.md))

```ts
import { FORCE_UNROLL_ACK } from '@lightninglabs/wavelength-react';

await client.exit({ outpoint, forceUnrollAck: FORCE_UNROLL_ACK });
```

([source](../../raw/wavelength/guides/unilateral-exit.md))

`FORCE_UNROLL_ACK` can be imported from any Wavelength package (the concept page imports it from `@lightninglabs/wavelength-core`) and carries the exact acknowledgement string the daemon requires. Once a unilateral job exists, the daemon's unroll actor broadcasts the proof and checkpoint transactions and the final sweep itself. ([source](../../raw/wavelength/concepts/leaving-ark.md))

## Preview with getExitPlan

Before starting, call `client.getExitPlan({ outpoints })` (or `useWalletExitPlan`) and show the `plans` summary. `confTarget` (in blocks) influences the fee rate for the recommended-funding estimate. The result has `canStart` and `totalRecommendedFundingSat`. ([source](../../raw/wavelength/guides/unilateral-exit.md))

Each `ExitPlanEntry` includes a per-outpoint `fundingAddress`, `fundingShortfallSat`, and its own `canStart`; fund the reported address until the shortfall clears and `canStart` becomes `true`. ([source](../../raw/wavelength/concepts/leaving-ark.md))

If `canStart` is `false`, check `ExitPlanEntry.infeasibilityReason`: a funding shortfall is fixable by sending sats to `fundingAddress`, but `sweep_below_dust` and `uneconomical` are structural. `round_committed` means a cooperative round currently owns the VTXO; show `roundCommitment` and normally wait. `isExitInfeasibilityFundable` identifies only the cases a top-up can resolve. ([source](../../raw/wavelength/guides/unilateral-exit.md))

## Start a single exit

`useWalletExit` exposes `exit`, `exitPending`, `exitError`, and `exitData`. Do not call it twice for the same outpoint; check `useWalletExitStatus` first. `exitData` is an `ExitResult` whose `path` discriminates the outcome: `queuedOutpoints` is populated when `path === 'cooperative'`; `created` and `actorID` when `path` is `'unilateral'` or `'unilateral_fallback'`. `cooperativeError` and `unilateral_fallback` are retained for source compatibility and not produced by the current RPC. ([source](../../raw/wavelength/guides/unilateral-exit.md))

## Batch exits

Exit funding is never reserved, so an earlier start can consume fee inputs a later one needs. `useWalletExitBatch` handles that: `exitBatch({ mode: 'unilateral', outpoints, confTarget: 6 })` re-plans between starts and stops cleanly if the daemon rejects a start mid-batch. It resolves once every outpoint has started, not completed. `{ mode: 'cooperative', outpoints, destination? }` queues every outpoint into the next cooperative round. Afterwards, `exitBatchData.started`, `.skipped`, `.remaining`, and `.stoppedBy` report the outcome; `exitBatchEvents` lists progress events. ([source](../../raw/wavelength/guides/unilateral-exit.md))

## Track status

`exitStatus({ outpoint })` returns an `ExitJobStatus` that advances through `pending`, `materializing` (proof transactions being broadcast and confirmed), `csv_pending` (waiting on CSV timelocks), `sweeping`, and `completed`. A job can land in `failed`, surfaced via `ExitStatusResult.lastError`; `found: false` is returned rather than an error when no job exists. ([source](../../raw/wavelength/concepts/leaving-ark.md))

`useWalletExitStatus(outpoint, opts?)` fetches on mount and when `outpoint` changes, defaulting to the phase-only call. `{ detailed: true }` adds recovery-tree progress, the CSV maturity countdown (`status.cSV.mature`, `status.cSV.blocksRemaining`), and a fee breakdown. `{ pollMs }` enables polling until unmount. `useWalletExits()` returns a wallet-wide `summary` (for example `totalExits`, `totalEstNetRecoveredSat`) and refetches when wallet activity changes. ([source](../../raw/wavelength/guides/unilateral-exit.md))

## Sweep the backing wallet

A unilateral exit creates claimable on-chain outputs over time rather than crediting a chosen address; `sweepWallet()` consolidates them once timelocks expire. ([source](../../raw/wavelength/concepts/leaving-ark.md))

Call `sweep()` from `useWalletSweep()` with `broadcast: false` to preview, then `broadcast: true` with a `destinationAddress`. `broadcast` defaults to `false`. Optional `feeRateSatPerVByte` and `confTarget` override the fee. Show the preview's `estimatedFeeSat` and `netAmountSat`; if `preview.canBroadcast` is `false`, do not broadcast and show `preview.failureReason`. ([source](../../raw/wavelength/guides/unilateral-exit.md))

```tsx
const preview = await sweep({ destinationAddress: 'bc1q...', broadcast: false });
if (preview.canBroadcast) {
  await sweep({ destinationAddress: 'bc1q...', broadcast: true });
}
```

([source](../../raw/wavelength/guides/unilateral-exit.md))

See also: [[wavelength-sdk-reference]], [[wavelength-cli]].
