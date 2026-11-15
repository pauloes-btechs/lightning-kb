---
title: 'Wavelength wallet guides: create, send, receive, restore'
type: howto
sources:
  - raw/wavelength/guides/create-a-wallet.md
  - raw/wavelength/guides/get-a-deposit-address.md
  - raw/wavelength/guides/handle-phases-and-errors.md
  - raw/wavelength/guides/receive-a-lightning-payment.md
  - raw/wavelength/guides/restore-a-wallet.md
  - raw/wavelength/guides/send-a-payment.md
  - raw/wavelength/guides/show-balance-and-activity.md
  - raw/wavelength/guides/use-a-passkey.md
  - raw/wavelength/concepts/wallet-lifecycle-and-auth.md
  - raw/wavelength/concepts/lightning-payments-are-swaps.md
updated: 2026-11-14
---

# Wavelength wallet guides: create, send, receive, restore

These are the React-based wallet guides from the [[wavelength]] docs, in the order an app usually needs them. Background is on [[wavelength-concepts]]; leaving Ark is on [[wavelength-unilateral-exit]].

## 1. Install the packages

The SDK ships as one transport package per platform plus `@lightninglabs/wavelength-react`. The web transport runs the daemon compiled to WebAssembly and uses OPFS for storage; its wasm runtime assets are not in the npm package, so you host them and point `runtimeBaseUrl` at them. The React Native transport wraps a runtime compiled into the app binary. ([source](../../raw/wavelength/guides/create-a-wallet.md))

```bash
npm install @lightninglabs/wavelength-web @lightninglabs/wavelength-react
npm install @lightninglabs/wavelength-react-native @lightninglabs/wavelength-react
```

([source](../../raw/wavelength/guides/create-a-wallet.md))

## 2. Add the provider

Build a `WalletEngine` outside the component tree and wrap the app in `WavelengthProvider`. Passing `config` and `autoStart: true` makes the engine boot the daemon as soon as the runtime is ready. Start with `defaultConfig('signet')`; move to `defaultConfig('mainnet', { allowMainnet: true })` only once key backup and recovery are in place. ([source](../../raw/wavelength/guides/create-a-wallet.md))

```tsx
import { createWebWalletEngine } from '@lightninglabs/wavelength-web';
import { WavelengthProvider } from '@lightninglabs/wavelength-react';
import { defaultConfig } from '@lightninglabs/wavelength-web';

const engine = createWebWalletEngine({
  runtimeBaseUrl: '/wavewalletdk/',
  config: defaultConfig('signet'),
  autoStart: true,
});
```

On React Native, use `createNativeWalletEngine({ config: defaultConfig('signet'), autoStart: true })` from `@lightninglabs/wavelength-react-native`. To call `start()` yourself instead, omit `autoStart` and drive it from `useWallet()`. ([source](../../raw/wavelength/guides/create-a-wallet.md))

## 3. Gate the UI on phase

`phase` from `useWallet()` is one of `loading`, `runtimeReady`, `starting`, `needsWallet`, `locked`, `syncing`, `restoring`, `ready`, `stopping`, `stopped`, `error`. A failed `start()` or `stop()` goes straight to `'error'`; read `error` from `useWallet()` for the reason. `info.walletState` from `useWalletInfo()` gives the underlying `WalletState` (`none`, `locked`, `ready`, `syncing`). ([source](../../raw/wavelength/guides/handle-phases-and-errors.md))

## 4. Create a wallet (password)

When `phase` is `'needsWallet'`, call `create({ password })` from `useWalletCreate()`. It generates an HD seed on-device and encrypts it with the password. The SDK enforces no minimum length or complexity, so validate the password yourself. The result includes `mnemonic`; this is the only time the SDK returns it, so show it immediately for backup. ([source](../../raw/wavelength/guides/create-a-wallet.md))

## 5. Or use a passkey

`useWalletPasskey(ceremony)` takes a ceremony injected from the transport: `webPasskeyCeremony` from `@lightninglabs/wavelength-web`, or `createNativePasskeyCeremony({ rpId })` from `@lightninglabs/wavelength-react-native` (the `rpId` domain must be associated with the app). `create(appName)` registers a credential and derives the seed from the PRF output; persist `outcome.credentialId` to scope future unlocks. ([source](../../raw/wavelength/guides/use-a-passkey.md))

`supported` is `boolean | null`: `null` while the capability probe runs, so hold a loading state rather than showing the unsupported branch. The probe (`ceremony.supportsPasskeyPrf()`) is memoized per ceremony instance; the guide suggests warming it at app boot with `void webPasskeyCeremony.supportsPasskeyPrf();`. ([source](../../raw/wavelength/guides/use-a-passkey.md))

When `phase === 'locked'`, call `open(credentialId?)`; omit the id for a discoverable-credential flow (for example on a new device with a synced passkey). If the user dismisses the prompt, `create`/`open` reject with `PasskeyCancelledError`, which is not recorded into `createError`/`openError`; treat it as a no-op. Browsers collapse many WebAuthn failures (permissions-policy block, iframe restriction, mismatched `rpId`) into the same signal, so a ceremony that always "cancels" usually means checking `rpId` and the `.well-known/assetlinks.json` (Android) or `apple-app-site-association` (iOS) file. ([source](../../raw/wavelength/guides/use-a-passkey.md))

`outcome.result.imported` is `true` when the ceremony created a new local wallet from the derived seed, and `outcome.result.mnemonic` is populated only then. If the passkey is unavailable, `open` rejects with a genuine error; offer a recovery-phrase fallback with `restore({ password, mnemonic, recoverState: true })`. ([source](../../raw/wavelength/guides/use-a-passkey.md))

## 6. Get a deposit address

`deposit()` from `useWalletDeposit()` creates a tracked boarding address; on-chain bitcoin sent there is swept into the VTXO balance in the next round. The `DepositResult` includes the address and an initial activity entry. It accepts an optional `{ amountSatHint }`, for example `deposit({ amountSatHint: 100000 })`. Watch with `useWalletActivity()` filtered on `entry.kind === 'deposit'`; entries flip to `'complete'` once the round settles, or `'failed'` with `entry.failureReason`. ([source](../../raw/wavelength/guides/get-a-deposit-address.md))

## 7. Show balance and activity

`useWalletBalance()` returns the current `Balance` directly (`null` before it is known; there is no pending flag). Display `confirmedSat` as spendable, adding `pendingInSat` and `pendingOutSat` for in-flight funds. `useWalletActivity()` returns the full history array; each `Entry` has `id`, `kind` (`send`, `receive`, `deposit`, `exit`), signed `amountSat`, `status`, timestamps, `feeSat`, `counterparty`, `note`, and `failureReason`. Both update on their own; for pull-to-refresh, call `refresh()` from `useWalletRefresh()` and show `refreshPending`, which only reflects that hook instance's own calls. ([source](../../raw/wavelength/guides/show-balance-and-activity.md))

## 8. Receive a Lightning payment

`receive({ amountSat, memo })` from `useWalletReceive()` triggers a receive swap; `ReceiveResult.invoice` is a BOLT11 string (see [[lightning-invoices]]). Match the activity entry by `entry.request?.lightningInvoice`; it is `'pending'` from creation through settlement and becomes `'complete'` once the receive swap round completes, or `'failed'`. For "waiting for payment" vs "settling", read `entry.progress?.phase`. ([source](../../raw/wavelength/guides/receive-a-lightning-payment.md))

## 9. Send a payment

Over Lightning, `prepare({ invoice })` from `useWalletPrepareSend()` returns a fee quote and a single-use `sendIntentId`; pass the result to `sendPrepared()` from `useWalletSend()`. The quote expires at `expiresAtUnix`. Check `feeKnown` before displaying `expectedFeeSat` (when `false` it is an estimate) and show `warning` if present. For one step, call `send({ invoice })`. ([source](../../raw/wavelength/guides/send-a-payment.md))

On-chain, `send({ onchainAddress, amountSat })` performs a cooperative leave; `SendResult` includes the activity entry and `actualAmountSat`. To drain the wallet, set `sweepAll: true` instead of `amountSat` and show `actualAmountSat`, since any earlier quote is an estimate. ([source](../../raw/wavelength/guides/send-a-payment.md))

Errors from `prepare` are safe to retry; errors from `sendPrepared` may mean the payment was already sent, so check the activity feed before retrying. ([source](../../raw/wavelength/guides/send-a-payment.md))

## 10. Restore a wallet

Restores are always local password wallets. Pass `mnemonic` (and `seedPassphrase` if the original used a BIP-39 passphrase) plus a new `password` to `restore` from `useWalletRestore()`. Set `recoverState: true` for server-assisted recovery of boarding outputs, VTXOs, and Lightning receive history; without it the wallet starts at zero balance. `recoveryWindow` is an optional per-key-family address look-ahead. ([source](../../raw/wavelength/guides/restore-a-wallet.md))

`restore` resolves as soon as the wallet is usable; `phase` goes `'restoring'` then `'ready'` while the scan continues in the background. `useWalletRecovery()` returns `recovery` (status `idle`, `restoring`, `done`, `failed`) and `acknowledge`. On `'failed'`, `recovery.walletUsable` tells whether the background scan failed on a usable wallet (`true`) or the restore itself failed (`false`). During the scan the balance is understated, but sending and receiving are safe. ([source](../../raw/wavelength/guides/restore-a-wallet.md))

## Errors

Mutation hooks share a throw-and-capture shape: an action, `<verb>Pending`, `<verb>Error: Error | null`, and (except `useWalletRefresh` and `useWalletPasskey`) `<verb>Data`; `reset<Verb>()` returns it to idle. SDK errors extend `WavelengthError` with a `code`; named codes include `runtime_not_ready`, `asset_load_failed`, `asset_integrity_failed`, `worker_error`, `wallet_locked`, and `runtime_lock_unavailable`, and daemon-originated errors currently use `wavelength_error`. `wallet_locked` means another tab owns the runtime (browser storage is exclusive to one runtime per origin), not the `locked` phase; branch on `code` rather than `instanceof` when duplicate bundled copies of core are possible. ([source](../../raw/wavelength/guides/handle-phases-and-errors.md))

## Conflicts

- **Phase after create.** The create guide says that after `create({ password })` resolves, `phase` becomes `'ready'` ([source](../../raw/wavelength/guides/create-a-wallet.md)). The lifecycle concept page says that after `createWallet()` the daemon often lands in the syncing phase first, and the engine advances it to ready ([source](../../raw/wavelength/concepts/wallet-lifecycle-and-auth.md)).
- **Who sets up a Lightning receive.** The receive guide says "the Ark server sets up a Lightning payment path" ([source](../../raw/wavelength/guides/receive-a-lightning-payment.md)); the swaps concept page says the swap server holds the Lightning HTLC and funds the vHTLC ([source](../../raw/wavelength/concepts/lightning-payments-are-swaps.md)).

See also: [[wavelength-web-sdk]], [[wavelength-react-native-sdk]], [[wavelength-sdk-reference]].
