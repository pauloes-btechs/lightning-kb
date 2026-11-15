---
title: 'Wavelength concepts: Ark, VTXOs, balances, lifecycle'
type: concept
sources:
  - raw/wavelength/concepts/activity-and-events.md
  - raw/wavelength/concepts/balances-and-vtxos.md
  - raw/wavelength/concepts/keys-backup-and-recovery.md
  - raw/wavelength/concepts/leaving-ark.md
  - raw/wavelength/concepts/lightning-payments-are-swaps.md
  - raw/wavelength/concepts/networks-and-config.md
  - raw/wavelength/concepts/wallet-lifecycle-and-auth.md
  - raw/wavelength/glossary.md
  - raw/wavelength/introduction/system-architecture.md
updated: 2026-11-14
---

# Wavelength concepts: Ark, VTXOs, balances, lifecycle

This page summarises the concept pages and glossary of the [[wavelength]] docs. For step-by-step code, see [[wavelength-wallet-guides]] and [[wavelength-unilateral-exit]].

## Ark and the operator

Ark is the shared off-chain protocol layer Wavelength builds on. Users hold VTXOs that settle on-chain in batched rounds, so payments are instant and cheap while remaining self-custodial, and users can always exit to on-chain Bitcoin unilaterally. ([source](../../raw/wavelength/glossary.md))

The operator, also called the Ark Service Provider (ASP), runs the Ark coordinator that constructs batch transactions, co-signs off-chain spends, and maintains the VTXO index. You trust the operator for availability and honest signing, but not for custody. Its endpoint is configured as `arkServerAddress`. ([source](../../raw/wavelength/glossary.md))

A **round** is one cycle in which the operator collects participant requests, constructs a batch transaction, co-signs it with clients, and broadcasts it on-chain, aggregating boarding inputs, leave requests, batch swaps, and new VTXO allocations. The **mailbox** is the operator's asynchronous message channel for push-style events such as swap notifications and round updates; it shares `arkServerAddress`, and Wavelength polls and acknowledges mailbox messages as part of background sync. **OOR (out-of-round)** transfers move VTXOs between owners without waiting for the next round; Wavelength handles them internally. ([source](../../raw/wavelength/glossary.md))

## VTXOs

Spendable balance in Ark is a set of **Virtual Transaction Outputs (VTXOs)**: off-chain outputs created inside the operator's periodic batch transactions. Each batch builds a Virtual Transaction Tree (VTXT) whose leaves are individual VTXOs. Each VTXO has two spend paths: a **collaborative path** where you and the operator co-sign, and a **unilateral exit path** you alone can broadcast after a relative timelock (CSV delay). ([source](../../raw/wavelength/concepts/balances-and-vtxos.md))

VTXOs have a **sweep delay** (CSV expiry) tied to their batch. Before the operator can sweep the batch, a VTXO should be refreshed through a **batch swap** (forfeiting it in a round for a fresh VTXO in a newer batch) or moved on-chain. The refresh is daemon-driven; there is no method to call. Automatic refreshes only happen inside the operator's advertised **free refresh window** and never pay a fee; if there is no usable window, the daemon's critical-exit handling moves the VTXO on-chain instead. The window width surfaces as `serverInfo.freeRefreshWindowBlocks` on `getInfo()`, and `wavecli ark vtxos refresh` can still pay a fee to refresh outside the window. ([source](../../raw/wavelength/concepts/balances-and-vtxos.md))

`balance()` and `list({ view: 'vtxos' })` read the embedded daemon's view of live VTXOs; the operator's indexer is authoritative on the network side. ([source](../../raw/wavelength/concepts/balances-and-vtxos.md))

## Balances: confirmed vs pending

`balance()` returns three satoshi fields:

- `confirmedSat`: settled funds, available for send, swap, or leave. This is what to show as "available".
- `pendingInSat`: inbound value still moving through boarding, a Lightning swap, or an unfinished round.
- `pendingOutSat`: outbound value reserved by in-flight sends, swap funding, or leave requests, held aside so the same VTXOs are not double-spent.

([source](../../raw/wavelength/concepts/balances-and-vtxos.md))

## Boarding

On-chain Bitcoin enters Ark through **boarding**. `deposit()` returns a **boarding address** and an initial deposit activity entry. Once the deposit confirms and meets the operator's policy, the wallet submits a boarding request for the next round; when the round completes, the boarded sats become one or more VTXOs and confirmed balance increases. Show pending inbound balance and the deposit entry's phase (`waiting_for_confirmation`, then `settling`) while this happens. ([source](../../raw/wavelength/concepts/balances-and-vtxos.md))

## Lightning payments are swaps

Wavelength does not open Lightning channels. Lightning payments are atomic swaps between Lightning and Ark through the swap server, built on a **virtual HTLC (vHTLC)**: a taproot output with the same hashlock/timelock structure as a Lightning HTLC (see [[htlc]]), settled inside Ark. ([source](../../raw/wavelength/concepts/lightning-payments-are-swaps.md))

- **Receive**: `receive()` builds a BOLT-11 invoice whose payment hash locks a vHTLC. A payer routes to the swap server via a route hint in the invoice; the swap server holds the incoming HTLC and funds a matching vHTLC; the wallet claims it with the preimage, and the swap server uses the preimage to settle the Lightning side.
- **Send**: `prepareSend({ invoice })` (or `send()`) selects VTXOs and constructs a swap session; the wallet funds a vHTLC locked to the invoice's payment hash; the swap server claims it, learns the preimage, and pays the invoice. On success `entry.progress.phase` reaches `confirmed` and `entry.status` becomes `complete`. The `SendRail` of a prepared send is `'lightning'` on the invoice path.

([source](../../raw/wavelength/concepts/lightning-payments-are-swaps.md))

Every vHTLC encodes refund paths with CLTV and CSV timelocks. The daemon arms automatic refund recovery on pay sessions: it unwinds cooperatively first (operator-co-signed OOR refunds) and, if needed, falls back to on-chain unilateral leaves after delays elapse. Entries may pass through `refunding` and `refunded` phases. ([source](../../raw/wavelength/concepts/lightning-payments-are-swaps.md))

See also: [[submarine-swaps]], [[lightning-invoices]].

## Leaving Ark

A **cooperative leave** forfeits selected VTXOs in an operator round; the batch includes a leave output paying the destination address. It is the default for `send` with `onchainAddress` and for `exit({ outpoint, destination })`, and needs a live, honest operator. A **unilateral exit** broadcasts the pre-signed tree branch without the operator; it is slow and expensive and needs an explicit `forceUnrollAck`. Wavelength never silently falls back from cooperative to unilateral. Details are on [[wavelength-unilateral-exit]]. ([source](../../raw/wavelength/concepts/leaving-ark.md))

## Activity and events

Wallet history is an **activity stream** of `Entry` objects, one per user-visible operation; entries are created when an operation starts and update in place as it settles. Read it with `list({ view: 'activity' })` (filter with `pendingOnly` or `kinds`, page with `limit` and the string list cursor) or stream it with `startActivity()` until `stopActivity()`. For a live stream, call `subscribe()` first, then `startActivity({ includeExisting: true, kinds })`, and resume later by passing the last numeric `Entry.cursor` as `cursor`. `stopActivity()` leaves the `subscribe()` listener registered. ([source](../../raw/wavelength/concepts/activity-and-events.md))

`WavelengthEvent` is a discriminated union delivered through the one `subscribe(listener)` callback:

| `type` | Payload | Meaning |
| --- | --- | --- |
| `'activity'` | `Entry` | A wallet operation was created or updated. |
| `'activityStream'` | `{ state: 'ended' }` or `{ state: 'failed', message }` | The stream ended or failed without a consumer-initiated close. |
| `'log'` | `{ level, message }` | Daemon log line (`debug`, `info`, `warn`, `error`). |
| `'runtimeReady'` | none | The runtime finished loading and can accept `start()`. |
| `'runtimeStopped'` | none | The runtime stopped. |

([source](../../raw/wavelength/concepts/activity-and-events.md))

Without a `WalletEngine`, the client does not retry a failed stream; the consumer chooses its own retry policy. `WalletEngine` reconciles with `list()`, retries from its last safe numeric cursor with bounded backoff, and the React `useWalletActivity` hook reads that snapshot newest-first. ([source](../../raw/wavelength/concepts/activity-and-events.md))

Entry fields include `kind`, `status` (`pending`, `complete`, `failed`), signed `amountSat` and `feeSat`, `cursor` (zero outside the subscription path), optional `progress` (phase, payment hash, txid, confirmation height, VTXO outpoint, Lightning preimage), optional `request`, and `failureReason` / `failureCode`. `failureCode` is one of `timed_out`, `expired`, `refunded`, `needs_intervention`, `failed`. Kinds are `deposit`, `receive`, `send`, and `exit`; for a `send`, `entry.request?.type` (`'lightning'`, `'onchain'`, or `'ark'`) tells which rail was used. Common phases: `request_created`, `waiting_for_payment`, `waiting_for_confirmation`, `payment_detected` / `settling`, `confirmed`, `refunding` / `refunded`, `failed`. ([source](../../raw/wavelength/concepts/activity-and-events.md))

## Wallet lifecycle and auth

`WalletState` (on `WalletInfo`) is one of `'none'`, `'locked'`, `'syncing'`, `'ready'`, mapped from the daemon's numeric enum by `walletStateFromProto`. Treat `'none'` and `'locked'` as non-spendable and wait for `'ready'` (or `walletReady === true`) before exposing payment actions. ([source](../../raw/wavelength/concepts/wallet-lifecycle-and-auth.md))

`RuntimePhase` merges runtime and wallet state: runtime-owned phases `loading`, `runtimeReady`, `starting`, `stopping`, `stopped`, `error`; wallet-owned phases from `phaseFromInfo()`: `needsWallet`, `locked`, `syncing`, `ready`; and the engine-owned `restoring`, entered by `restoreWallet()`. While its phase is `'syncing'`, the `WalletEngine` polls `refresh()` every 2000ms until the phase leaves syncing. Without an engine, poll `getInfo()` or subscribe to activity events yourself. ([source](../../raw/wavelength/concepts/wallet-lifecycle-and-auth.md))

Password wallets use `createWallet({ password })` and then `unlockWallet({ password })` on later sessions. Passkey wallets replace the password with a WebAuthn PRF output: a `PasskeyCeremony` derives `prfOutput`, and `openWalletFromPasskey({ prfOutput })` unlocks or creates the wallet. In React these run through `useWalletCreate()`, `useWalletUnlock()`, and `useWalletPasskey(webPasskeyCeremony)`. ([source](../../raw/wavelength/concepts/wallet-lifecycle-and-auth.md))

## Keys, backup and recovery

Every wallet is an HD wallet rooted in one seed. A password wallet's seed comes from a generated or imported 24-word mnemonic, with the password used directly as the wallet database passphrase. A passkey wallet derives the seed from the passkey: the SDK evaluates the PRF over `SHA-256("wavewalletdk-passkey:v1")` (exported as `PASSKEY_PRF_SALT_HEX`) and expands the output with HKDF-SHA256 into a 16-byte aezeed entropy (`info` `wavewalletdk:seed:v1`) and a 32-byte hex-encoded wallet DB password (`info` `wavewalletdk:dbpw:v1`). PRF outputs under 32 bytes are rejected. ([source](../../raw/wavelength/concepts/keys-backup-and-recovery.md))

The seed lives only in the encrypted wallet database: OPFS on web, or `RuntimeConfig.dataDir` on React Native (default from `getDefaultDataDir()`). Passkeys are bound to the relying-party ID (the page hostname on web, an explicit `rpId` on React Native), so moving domains breaks passkey recovery; the mnemonic is the domain-independent escape hatch. Two exports of the same passkey wallet show different 24-word phrases that decode to the same entropy. ([source](../../raw/wavelength/concepts/keys-backup-and-recovery.md))

| Scenario | Path |
| --- | --- |
| Same device, returning session | Passkey assertion + `openWalletFromPasskey()` / `unlockWallet({ password })` |
| New device, synced passkey | Discoverable passkey assertion + `openWalletFromPasskey()` |
| Lost passkey, has mnemonic | `createWallet({ password, mnemonic, recoverState: true })`; continues as a password wallet |
| Lost passkey and mnemonic | None; there is no custodial reset |

([source](../../raw/wavelength/concepts/keys-backup-and-recovery.md))

`recoverState: true` opts into server-assisted recovery: the daemon walks the seed's addresses and queries the operator's indexer to rebuild boarding outputs, VTXOs, and Lightning receive history. The passkey import path does not run that scan today. ([source](../../raw/wavelength/concepts/keys-backup-and-recovery.md))

## Networks and config

`RuntimeConfig` has one flat camelCase shape on both platforms. All endpoints must serve the same `network`; a mismatched Esplora or swap server is a common cause of stuck deposits or swaps that never fund. `defaultConfig(network)` returns presets for `'signet'`, `'testnet'`, and `'mainnet'`, with overrides as the second argument, for example `defaultConfig('signet', { dataDir: 'my-app-wallet' })`. `'regtest'` is excluded; build its config by hand with local endpoints and the insecure-transport flags. ([source](../../raw/wavelength/concepts/networks-and-config.md))

Mainnet requires `allowMainnet: true` with `network: 'mainnet'`, for example `defaultConfig('mainnet', { allowMainnet: true })`; without it the SDK rejects the config before startup. On mainnet, startup fails if `arkServerInsecure` or `swapServerInsecure` is set, or if `arkServerAddress` or `swapServerAddress` uses `http://`. Test networks ignore `allowMainnet`. ([source](../../raw/wavelength/concepts/networks-and-config.md))

Other fields include `dataDir`, `debugLevel`, `arkServerTlsCertPath`, `swapServerTlsCertPath`, `swapDatabaseFileName`, `disableSwaps`, and the numeric limits `maxOperatorFeeSat`, `maxPaymentCLTV`, `signingWorkers`, and `bufferSize`. `lwwallet` is the default wallet backend; `walletEsploraUrl`, `walletPasswordFile`, and `walletPollIntervalSeconds` apply only to `lwwallet`, while `walletFeeUrl`, `walletBlockHeadersSource`, and `walletFilterHeadersSource` apply only to `btcwallet`; `walletRecoveryWindow` applies to both. ([source](../../raw/wavelength/concepts/networks-and-config.md))

## Conflicts

- **Round cadence.** The architecture page says the round interval is operator-configured, "often well under a minute" ([source](../../raw/wavelength/introduction/system-architecture.md)). Balances & VTXOs says rounds are "often around one minute on public test networks; roughly 90 seconds end-to-end is a reasonable UX expectation" ([source](../../raw/wavelength/concepts/balances-and-vtxos.md)). The glossary says the round tick is "typically on the order of ~90 seconds" ([source](../../raw/wavelength/glossary.md)).
- **Esplora compatibility wording.** Networks & config says the endpoint is "electrs or mempool.space compatible" ([source](../../raw/wavelength/concepts/networks-and-config.md)); the glossary says "electrs or Blockstream-compatible" ([source](../../raw/wavelength/glossary.md)).

See also: [[wavelength-sdk-reference]], [[wavelength-web-sdk]], [[wavelength-react-native-sdk]].
