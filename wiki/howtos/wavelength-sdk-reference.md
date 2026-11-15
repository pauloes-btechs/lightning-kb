---
title: Wavelength SDK packages
type: howto
sources:
  - raw/wavelength/reference/wavelength-core.md
  - raw/wavelength/reference/wavelength-web.md
  - raw/wavelength/reference/wavelength-react.md
  - raw/wavelength/reference/wavelength-react-native.md
updated: 2026-11-14
---

# Wavelength SDK packages

This is a compact index of the four [[wavelength]] SDK packages and everything their reference pages list. Platform setup is covered on [[wavelength-web-sdk]] and [[wavelength-react-native-sdk]].

| Package | Role |
|---|---|
| `@lightninglabs/wavelength-core` | The portable wallet contract (typed client, shared primitives, error model), with no dependency on the browser, React or React Native. |
| `@lightninglabs/wavelength-web` | The browser/wasm transport. It runs the daemon as WebAssembly in a Web Worker (the default) or on the main thread, and ships the WebAuthn/PRF passkey ceremony. It re-exports all of core (`export * from '@lightninglabs/wavelength-core'`). |
| `@lightninglabs/wavelength-react` | `WavelengthProvider` plus hooks over an injected `WalletEngine`. It re-exports the complete core contract but no transport engine factory. |
| `@lightninglabs/wavelength-react-native` | The React Native transport (the daemon compiled in through gomobile bindings), the native passkey ceremony and a data-directory helper. It re-exports all of core. |

([source](../../raw/wavelength/reference/wavelength-core.md), [source](../../raw/wavelength/reference/wavelength-web.md), [source](../../raw/wavelength/reference/wavelength-react.md), [source](../../raw/wavelength/reference/wavelength-react-native.md))

## wavelength-core

### Configuration

- **`networkDefaults(network: PresetNetwork, transport: ServerTransport): Partial<RuntimeConfig>`** returns the public endpoint preset in REST (`'rest'`) or gRPC (`'grpc'`) flavor. It is the building block for the transports' `defaultConfig`. `regtest` has no preset.
- **`DEBUG_LEVELS`** is `'trace', 'debug', 'info', 'warn', 'error', 'critical', 'off'` (type `DebugLevel`). `debugLevel` itself stays a string, because the daemon also accepts per-subsystem lists such as `'ROND=debug,info'`.
- **`ServerTransport`** is `'rest' | 'grpc'`. Browser transports use `rest`; native transports use `grpc`.
- **`Network`** is `'mainnet' | 'testnet' | 'testnet4' | 'signet' | 'regtest'`. `PresetNetwork` narrows it to networks with a preset. `testnet4` carries a preset but its deployment is not supported yet.
- **`MobileConfig`** is the internal snake_case shape (`data_dir`, `server_address`, `server_transport`, `swap_server_transport`, and so on) passed to the mobile facade. It is not exported.

([source](../../raw/wavelength/reference/wavelength-core.md))

**`RuntimeConfig`** fields: `network`, `allowMainnet`, `dataDir`, `debugLevel`, `arkServerAddress`, `arkServerTlsCertPath`, `arkServerInsecure`, `walletType` (`'lwwallet' | 'btcwallet'`, default `lwwallet`), `walletEsploraUrl`, `walletPasswordFile`, `walletPollIntervalSeconds`, `walletRecoveryWindow`, `walletFeeUrl`, `walletBlockHeadersSource`, `walletFilterHeadersSource`, `swapServerAddress`, `swapServerTlsCertPath`, `swapServerInsecure`, `swapDatabaseFileName`, `disableSwaps`, `maxOperatorFeeSat`, `maxPaymentCLTV`, `signingWorkers`, `bufferSize`. The `lwwallet`-only fields are `walletEsploraUrl`, `walletPasswordFile` and `walletPollIntervalSeconds`. The `btcwallet`-only fields are `walletFeeUrl`, `walletBlockHeadersSource` and `walletFilterHeadersSource`. The SDK validates the config before it starts the daemon. It rejects fields that belong to the other `walletType`, invalid numbers, mainnet without `allowMainnet: true`, and `arkServerTlsCertPath` on web. ([source](../../raw/wavelength/reference/wavelength-core.md))

Preset endpoints (REST / gRPC) ([source](../../raw/wavelength/reference/wavelength-core.md)):

| Network | `arkServerAddress` | `walletEsploraUrl` | `swapServerAddress` |
|---|---|---|---|
| signet | `https://signet.wavelength-rest.lightning.finance` / `signet.wavelength.lightning.finance:443` | `https://mempool-signet.testnet.lightningcluster.com/api` | `https://signet.swapd-rest.lightning.finance` / `swap.signet.wavelength.lightning.finance:443` |
| testnet | `https://test.wavelength-rest.lightning.finance` / `test.wavelength.lightning.finance:443` | `https://mempool-testnet3.testnet.lightningcluster.com/api` | `https://test.swapd-rest.lightning.finance` / `swap.test.wavelength.lightning.finance:443` |
| mainnet | `https://wavelength-rest.lightning.finance` / `wavelength.lightning.finance:443` | `https://mempool.staging.lightningcluster.com/api` | `https://swapd-rest.lightning.finance` / `swap.wavelength.lightning.finance:443` |

### Client lifecycle

- **`WavelengthClient`** is the typed RPC interface every transport implements. Its methods are `ready`, `start`, `stop`, `getInfo`, `status`, `balance`, `createWallet`, `unlockWallet`, `openWalletFromPasskey`, `deposit`, `receive`, `prepareSend`, `sendPrepared`, `send`, `list`, `exit`, `exitStatus`, `exitSummary`, `getExitPlan`, `sweepWallet`, `callFacade`, `isRunning`, `subscribe`, `startActivity`, `stopActivity` and `dispose`. The call order is: await `ready()`, call one start method, use the wallet, `stop()`, then `dispose()`. `dispose()` is terminal.
- **`ExternalSeedWalletClient`** extends `WavelengthClient` with `startExternalSeedWallet(config, req)`. The official web and React Native factories return this subtype.
- **`ready(): Promise<void>`** rejects with `asset_load_failed` or `asset_integrity_failed`.
- **`startExternalSeedWallet(config, req): Promise<ExternalSeedWalletOpenResult>`** imports or unlocks a wallet from exactly 16 bytes of entropy at a host-chosen nonempty `config.dataDir`. `ExternalSeedWalletRequest` has `seedEntropy: Uint8Array`, `expectedIdentityPubKey?`, `recoverState?` and `recoveryWindow?`. `ExternalSeedWalletOpenResult` has `imported`, `identityPubKey`, `recoveryRan`, `recoveredBoardingAddresses`, `recoveredBoardingUTXOs`, `recoveredVTXOs`, `recoveredOORReceiveScripts` and `recoveredOORRecipientEvents`.
- **`start(config: RuntimeConfig): Promise<WalletInfo>`**: a second call while a session is running coalesces onto it and ignores the new config.
- **`stop(): Promise<void>`**: the client stays usable after a stop.
- **`dispose(): void`** releases resources and, for the worker transport, terminates the Worker.

([source](../../raw/wavelength/reference/wavelength-core.md))

### Wallet engine

- **`createWalletEngine(options: WalletEngineOptions): WalletEngine`** calls `client.ready()` immediately, which moves `phase` from `'loading'` to `'runtimeReady'`. `WalletEngineOptions` is `{ onPerformance? } & ({ client, config, autoStart: true } | { client, config?, autoStart?: false })`, so `autoStart: true` without `config` is a compile error. **`DistributiveOmit<T, K>`** is a helper type for implementers.
- **`WalletEngine`** has `client`, `getSnapshot`, `subscribe`, `start(config?)`, `stop`, `refresh`, `createWallet`, `restoreWallet`, `acknowledgeRecovery`, `unlockWallet`, `openWalletFromPasskey`, `deposit`, `receive`, `prepareSend`, `sendPrepared`, `send`, `exit`, `exitStatus`, `exitSummary`, `getExitPlan`, `sweepWallet`, `exitBatch(opts & { signal?, onEvent? })`, `list`, `clearLogs` and `dispose`. Mutations kick a background refresh. Read-only calls (`prepareSend`, `exitStatus`, `exitSummary`, `getExitPlan`, `list`, and `sweepWallet` with `broadcast: false`) do not.
- **Background processes:**
  - When `'ready'`, the engine runs activity-stream auto-refresh with re-reads at 750ms, 1500ms and 3000ms.
  - It runs activity-stream recovery from the last cursor with bounded exponential backoff.
  - When `'syncing'`, it runs a sync auto-poll every 2000ms that escalates to `'error'` after 5 consecutive failures.
  - When `'restoring'`, it runs a restore readiness poll of `getInfo()` every 1500ms.
  - A shared 5-failure background-refresh budget applies to all of the above.
  - A `runtimeStopped` event moves the engine to `'stopped'` (unless it is already in `'error'`).
- **`WalletSnapshot`** is `{ phase, error, info, balance, activity, recovery, logs }`. `logs` holds up to 200 entries.
- **`RecoveryState`** is `{ status: 'idle' } | { status: 'restoring' } | { status: 'done'; result: CreateWalletResult } | { status: 'failed'; error: Error; walletUsable: boolean }`.
- **`RestoreWalletRequest`** is `CreateWalletRequest & { mnemonic: string[] }`.

([source](../../raw/wavelength/reference/wavelength-core.md))

### Wallet setup and authentication

- **`createWallet(req)`**: `CreateWalletRequest` is `{ password, mnemonic?, seedPassphrase?, recoverState?, recoveryWindow? }`, where `recoverState` defaults to false. `CreateWalletResult` is `{ mnemonic, encipheredSeed, identityPubKey, recoveryRan, recoveredBoardingAddresses, recoveredBoardingUTXOs, recoveredVTXOs, recoveredOORReceiveScripts, recoveredOORRecipientEvents }`.
- **`unlockWallet(req)`**: `UnlockWalletRequest` is `{ password }` and `UnlockWalletResult` is `{ identityPubKey }`.
- **`openWalletFromPasskey(req)`**: `OpenWalletFromPasskeyRequest` is `{ prfOutput }` (hex). `OpenWalletFromPasskeyResult` is `{ imported, mnemonic, identityPubKey }`, and `mnemonic` is populated only when `imported` is true.

([source](../../raw/wavelength/reference/wavelength-core.md))

### Reading wallet state

- **`getInfo(): Promise<WalletInfo>`**: `WalletInfo` is `{ version, commit, network, blockHeight, serverConnected, walletType, identityPubKey, walletState, walletReady, serverInfo? }`. `ServerInfo` is `{ freeRefreshWindowBlocks }`, where 0 means the operator advertises no waiver window.
- **`status(): Promise<WalletStatus>`**: `WalletStatus` is `{ ready, unlocked, network, balance, pendingCount }`.
- **`balance(): Promise<Balance>`**: `Balance` is `{ confirmedSat, pendingInSat, pendingOutSat }`.
- **`isRunning(): Promise<boolean>`** reports only whether the daemon process is running, not wallet readiness.

([source](../../raw/wavelength/reference/wavelength-core.md))

### Deposits, receiving and sending

- **`deposit(req?)`**: `DepositRequest` is `{ amountSatHint? }` and `DepositResult` is `{ address, entry }`.
- **`receive(req)`**: `ReceiveRequest` is `{ amountSat, memo? }` and `ReceiveResult` is `{ invoice, entry }`.
- **`prepareSend(req: SendRequest): Promise<PrepareSendResult>`**, then **`sendPrepared(prepared)`**, or **`send(req)`** for both in one call. A `sendIntentId` is single-use.
- **`SendRequest`** has a Lightning arm, `{ invoice, amountSat?, note?, maxFeeSat?, maxCreditSat?, maxCreditTopupSat? }`, and an on-chain arm, `{ onchainAddress, amountSat?, sweepAll?, note?, maxFeeSat? }`. Credit use is opt-in through `maxCreditSat`.
- **`PrepareSendResult`** is `{ sendIntentId, amountSat, expectedFeeSat, feeKnown, expectedTotalOutflowSat, totalOutflowKnown, rail, quoteStatus ('unspecified' | 'complete' | 'local_only'), destinationSummary, invoiceDescription, paymentHash, expiresAtUnix, selectedOutpoints, warning }`.
- **`SendResult`** is `{ entry, actualAmountSat, paymentHash? }`.
- **`SendRail`** is `'unspecified' | 'offchain_unknown' | 'in_ark' | 'lightning' | 'onchain' | 'credit' | 'mixed'`.
- **`classifyDestination(raw: string): Destination`** is pure and offline, and it does not name a rail. `Destination` is `{ kind: 'empty' } | { kind: 'invoice'; amount: InvoiceAmount } | { kind: 'address' }`. `InvoiceAmount` is `{ status: 'known'; sat } | { status: 'amountless' } | { status: 'unrepresentable' }`.

([source](../../raw/wavelength/reference/wavelength-core.md))

### Activity and history

- **`list(req?)`**: `ListRequest` is `{ view?, pendingOnly?, kinds?, limit?, offset?, cursor? }`. `ListView` is `'activity' | 'vtxos' | 'onchain'` (default `'activity'`). `ListResult` is `{ view, activity?, vtxos?, onchain? }`.
  - `ActivityList` is `{ entries, total, hasMore, nextCursor }`.
  - `VTXOInventory` is `{ vtxos, total }`.
  - `WalletVTXO` is `{ outpoint, amountSat, status, batchExpiry, relativeExpiry, commitmentTxid }`.
  - `OnchainHistory` is `{ txs, total, hasMore }`.
  - `OnchainTx` is `{ txid, kind, amountSat, feeSat, status, confirmationHeight, createdAt, description }`.
- **`subscribe(listener: WavelengthListener): () => void`**.
- **`startActivity(opts?: ActivityStreamOptions)`**: the options are `{ includeExisting?, kinds?, cursor? }`. **`stopActivity()`** closes the stream.
- **`Entry`** is `{ id, kind, status, amountSat, feeSat, counterparty, createdAt, updatedAt, note, failureReason, failureCode, cursor, progress?, request? }`. `id` is an activity id, not a payment hash.
- **`EntryProgress`** is `{ phase, phaseLabel, paymentHash, txid, confirmationHeight, vTXOOutpoint, preimage }`.
- **`EntryRequest`** is `{ type, lightningInvoice, paymentHash, onchainAddress, arkAddress }`.
- **`EntryKind`** is `'send' | 'receive' | 'deposit' | 'exit'`. **`EntryStatus`** is `'pending' | 'complete' | 'failed'`.
- **`EntryPhase`** is `'unspecified' | 'request_created' | 'waiting_for_payment' | 'payment_detected' | 'settling' | 'confirmed' | 'refunding' | 'refunded' | 'failed' | 'waiting_for_confirmation'`.
- **`EntryFailureCode`** is `'timed_out' | 'expired' | 'refunded' | 'needs_intervention' | 'failed'`. **`EntryRequestType`** is `'lightning' | 'onchain' | 'ark'`.

([source](../../raw/wavelength/reference/wavelength-core.md))

### Exiting Ark

- **`exit(req: ExitRequest): Promise<ExitResult>`**. `ExitRequest` is `{ outpoint, destination? }` (cooperative) or `{ outpoint, forceUnrollAck: FORCE_UNROLL_ACK }` (unilateral), where `FORCE_UNROLL_ACK = 'I_KNOW_WHAT_I_AM_DOING'`. A cooperative error never falls back to a unilateral exit. `ExitResult` is `{ path, cooperative, queuedOutpoints, created, actorID, cooperativeError }`. `ExitPath` is `'cooperative' | 'unilateral' | 'unilateral_fallback'`; `unilateral_fallback` is never returned by current wallet RPC behavior.
- **`exitStatus(req)`**: `ExitStatusRequest` is `{ outpoint, detailed? }`. `ExitStatusResult` is `{ found, status, sweepTxid, lastError, phaseDetail, progress?, cSV?, fees?, bestCaseBlocksRemaining, currentHeight }`.
  - `ExitProgress` is `{ confirmedTxs, inFlightTxs, readyTxs, blockedTxs, totalTxs, currentLayer, totalLayers, targetConfirmed, allProofConfirmed }`.
  - `ExitCSV` is `{ targetConfirmHeight, maturityHeight, blocksRemaining, mature }`.
  - `ExitFees` is `{ cPFPFeeSat, sweepFeeSat, totalCostSat, spentSoFarSat, vTXOAmountSat, netRecoveredSat, feeRateSatVByte, sweepFeeActual }`.
  - `ExitJobStatus` is `'unspecified' | 'pending' | 'materializing' | 'csv_pending' | 'sweeping' | 'completed' | 'failed'`.
- **`exitSummary(req?)`**: `ExitSummaryRequest` is `Record<string, never>`. `ExitSummaryResult` is `{ exits, totalExits, totalVTXOAmountSat, totalEstFeeSat, totalEstNetRecoveredSat }`. `ExitSummaryEntry` is `{ outpoint, status, vTXOAmountSat, estTotalFeeSat, estNetRecoveredSat }`.
- **`getExitPlan(req)`**: `GetExitPlanRequest` is `{ outpoints, confTarget? }`. `GetExitPlanResult` is `{ plans, feeRateSatPerVByte, canStart, totalFundingShortfallSat, totalRecommendedFundingSat }`. `ExitPlanEntry` is `{ outpoint, fundingAddress, requiredConfirmations, requiredFeeUTXOCount, usableFeeUTXOCount, recommendedUTXOAmountSat, recommendedTotalFundingSat, fundingShortfallSat, canStart, infeasibilityReason, exitJobFound, exitStatus, sweepTxid, lastError, roundCommitment, err }`. `ExitInfeasibilityReason` is `'unspecified' | 'sweep_below_dust' | 'uneconomical' | 'wallet_underfunded' | 'wallet_too_few_inputs' | 'round_committed'`.
- **`exitBatch(opts: ExitBatchOptions & { client, signal?, onEvent? }): Promise<ExitBatchResult>`** resolves once every exit has started, not when they complete.
  - `ExitBatchOptions` is `{ mode: 'cooperative'; outpoints; destination? } | { mode: 'unilateral'; outpoints; confTarget? }`.
  - `ExitBatchEvent` types are `'planned' | 'starting' | 'started' | 'stopped'`.
  - `ExitBatchStop` is `{ reason: 'infeasible'; plan } | { reason: 'rejected'; outpoint; error }`.
  - `ExitBatchResult` is `{ started, skipped, remaining, stoppedBy? }`.
- **`isExitInfeasibilityFundable(reason): boolean`** returns true only for `wallet_underfunded` and `wallet_too_few_inputs`.
- **`sweepWallet(req)`**: `SweepWalletRequest` is `{ destinationAddress, broadcast?, feeRateSatPerVByte?, confTarget? }`, and `broadcast` defaults to false (preview). `SweepWalletResult` is `{ inputs, totalInputSat, estimatedFeeSat, netAmountSat, feeRateSatPerVByte, canBroadcast, txid, failureReason }`. `WalletSweepInput` is `{ outpoint, amountSat }`.

([source](../../raw/wavelength/reference/wavelength-core.md))

### Facade, state model, events, errors, passkeys

- **`callFacade<T>(method: FacadeMethod, params?)`** is a low-level escape hatch. `FacadeMethod` lists `start`, `startExternalSeedWallet`, `stop`, `getInfo`, `status`, `balance`, `createWallet`, `unlockWallet`, `openWalletFromPasskey`, `deposit`, `receive`, `prepareSend`, `sendPrepared`, `list`, `exit`, `exitStatus`, `exitSummary`, `getExitPlan`, `sweepWallet`, `confirmedBalanceSat`, `pendingInboundSat`, `walletReady` and `isRunning`. Calls to `start`, `startExternalSeedWallet` and `stop` are rejected.
- **`camelizeKeys<T>(value)`** maps daemon PascalCase JSON to camelCase.
- **`WalletState`** is a const: `None: 'none'`, `Locked: 'locked'`, `Ready: 'ready'`, `Syncing: 'syncing'`.
- **`RuntimePhase`** is `'loading' | 'runtimeReady' | 'starting' | 'needsWallet' | 'locked' | 'syncing' | 'restoring' | 'ready' | 'stopping' | 'stopped' | 'error'`.
- **`WalletPhase`** is `'needsWallet' | 'locked' | 'syncing' | 'ready'`. **`phaseFromInfo(info)`** derives it.
- **`normalizeInfo(raw): WalletInfo`** and **`walletStateFromProto(value)`** do the mapping: `1` to `'none'`, `2` to `'locked'`, `3` to `'ready'` and `4` to `'syncing'`. Undefined or 0 becomes `'none'`, and an unknown non-zero value becomes `'locked'`.
- **`WavelengthEvent`** types are `runtimeReady`, `runtimeStopped`, `activity` (`Entry`), `activityStream` (`ActivityStreamPayload`) and `log` (`WavelengthLogPayload`).
  - `ActivityStreamState` is `'ended' | 'failed'`.
  - `WavelengthEventType` is `WavelengthEvent['type']`.
  - `WavelengthListener` is `(event) => void`.
  - `WavelengthLogPayload` is `{ level, message }`, and `WavelengthLogLevel` is `'debug' | 'info' | 'warn' | 'error'`.
- **`WavelengthPerformanceEvent`** is `{ stage: 'runtime' | 'wallet' | 'passkey'; phase; durationMs; detail? }`. **`WavelengthPerformanceListener`** receives these samples, and one that throws is swallowed.
- **`WavelengthError`** (class) has `code: WavelengthErrorCode`, which defaults to `wavelength_error`. The codes are `wavelength_error`, `runtime_not_ready`, `asset_load_failed`, `asset_integrity_failed`, `worker_error`, `wallet_locked`, `runtime_lock_unavailable`, `unsupported_facade_method`, `invalid_cursor`, `invalid_config`, `invalid_external_seed` and `runtime_active`.
- **`PasskeyCancelledError`** (class) has the default message `'passkey ceremony was cancelled'`. **`toError(value): Error`** normalizes thrown values to an `Error`.
- **`WalletKind`** is `'passkey' | 'password'`. **`PasskeyAssertion`** is `{ prfOutput, credentialId }`. **`PasskeyCeremony`** is `{ supportsPasskeyPrf(), registerPasskeyWallet(appName), assertPasskeyPrf(allowCredentialId?) }`.

([source](../../raw/wavelength/reference/wavelength-core.md))

## wavelength-web

- **`defaultConfig(network: PresetNetwork, overrides?: Partial<RuntimeConfig>): RuntimeConfig`** fills in the REST gateway endpoints. `'regtest'` is not accepted, and `'mainnet'` needs `allowMainnet`.
- **`createWebClient(options?: WebClientOptions): ExternalSeedWalletClient`** defaults to the worker transport (`WorkerWavelengthClient`, which is not exported).
- **`WebClientOptions`** fields:
  - `workerURL`: default is the bundler-emitted worker URL.
  - `runtimeBaseUrl`: default unset, which means page-relative.
  - `runtimeThread`: default `'worker'`.
  - `runtimeCache`: default true.
  - `debug`: default false. It logs RPC payloads with secrets redacted and is meant for development only.
  - `onPerformance`: default unset.
  - `runtimeIntegrity`: default true. A mainnet start rejects with `invalid_config` when this is false.
- **`RuntimeThread`** is `'main' | 'worker'`.
- **`createWebWalletEngine(options?: WebWalletEngineOptions): WalletEngine`**. `WebWalletEngineOptions` is `WebClientOptions & ({ config; autoStart: true } | { config?; autoStart?: false })`.
- **`MainThreadWavelengthClient`** (class, `constructor(options?: WebClientOptions)`) runs the runtime on the main thread and blocks rendering while busy. The reference prefers `createWebClient({ runtimeThread: 'main' })`.
- **External-seed profile locking:** in worker mode, the Web Lock is scoped to the normalized `dataDir` and `network`. Legacy `start()` and main-thread external-seed starts keep an origin-global lock.
- **`RUNTIME_ASSETS`** maps keys to files: `wasm` to `wavewalletdk.wasm`, `wasmGz` to `wavewalletdk.wasm.gz`, `wasmExec` to `wasm_exec.js`, `sqliteBridge` to `sqlite-bridge.js`, `sqliteWorker` to `sqlite-worker.js`, `sqliteNodeVfs` to `sqlite-node-vfs.js`, `sqlite` to `sqlite3.js`, `sqliteWasm` to `sqlite3.wasm`, and `sqliteOpfsProxy` to `sqlite3-opfs-async-proxy.js`. **`RUNTIME_ASSET_FILES`** is `Object.values(RUNTIME_ASSETS)`. **`RUNTIME_ASSET_DIGESTS`** holds SRI `sha256-<base64>` digests by filename, generated by `pnpm gen:runtime-digests`. **`RUNTIME_MANIFEST_VERSION`** is the paired daemon build; it is defined in core.
- **Asset loading:** the base URL gets a trailing slash added if missing. The client fetches `.wasm.gz` first, then `.wasm`. It sniffs magic bytes (`1f 8b` for gzip, `00 61 73 6d` for wasm). Bootstrap scripts are verified and then executed from blob URLs.
- **Passkeys:**
  - **`webPasskeyCeremony`** (const `PasskeyCeremony`).
  - **`createWebPasskeyCeremony(options?: { onPerformance? })`**.
  - **`supportsPasskeyPrf(): Promise<boolean>`**, which is not a guarantee that PRF will work.
  - **`registerPasskeyWallet(appName, onPerformance?)`**.
  - **`assertPasskeyPrf(allowCredentialId?, onPerformance?)`**, which is discoverable when no id is given.
  - **`PasskeyAssertion`** is `{ prfOutput, credentialId }`.
  - The PRF salt is `SHA-256("wavewalletdk-passkey:v1")`.
- **Re-exported `SendRequest` and `ReceiveRequest`** are shown in full on the web page.

([source](../../raw/wavelength/reference/wavelength-web.md))

## wavelength-react

- **`WavelengthProvider(props: WavelengthProviderProps)`** takes `{ children: ReactNode; engine: WalletEngine }` and throws if `engine` is missing. It never calls `engine.dispose()`. `WavelengthProviderProps` is not itself an exported name.
- **`useWalletEngine(): WalletEngine`**.
- **`useWallet()`** returns `{ phase, error, start(config?), stop() }`.
- **Readers:**
  - `useWalletInfo(): WalletInfo | null`
  - `useWalletBalance(): Balance | null`
  - `useWalletActivity(): Entry[]`, which is always `list({ view: 'activity', pendingOnly: false })`
  - `useWalletRecovery()`, which returns `{ recovery, acknowledge }`
  - `useWalletLogs()`, which returns `{ logs, clear }` (up to 200 entries)
- **Mutations** return `<verb>`, `<verb>Pending`, `<verb>Error`, `<verb>Data` and `reset<Verb>`. Their result types are exported as `UseWallet<Verb>Result`.
  - `useWalletCreate` (`create`)
  - `useWalletRestore` (`restore`): it resolves when the wallet is usable, not when the scan finishes.
  - `useWalletUnlock` (`unlock`)
  - `useWalletDeposit` (`deposit`)
  - `useWalletReceive` (`receive`)
  - `useWalletPrepareSend` (`prepare`)
  - `useWalletSend` (`send`, `sendPrepared`)
  - `useWalletRefresh` (`refresh`, with no data field)
- **Exit hooks:**
  - `useWalletExit` (`exit`)
  - `useWalletExitPlan` (`plan`)
  - `useWalletSweep` (`sweep`)
  - `useWalletExitBatch`, which returns `exitBatch` plus `exitBatchEvents`
  - `useWalletExitStatus(outpoint, opts?: { detailed?, pollMs? })`, which returns `{ status, statusPending, statusError, refreshStatus }`
  - `useWalletExits()`, which returns `{ summary, summaryPending, summaryError, refreshSummary }`
  - `useWalletList`, which keeps the last good `listData`
- **`useWalletPasskey(ceremony: PasskeyCeremony)`** returns `{ supported: boolean | null, create(appName), createPending, createError, resetCreate, open(credentialId?), openPending, openError, resetOpen }`. **`PasskeyWalletOutcome`** is `{ result: OpenWalletFromPasskeyResult; credentialId }`.

([source](../../raw/wavelength/reference/wavelength-react.md))

## wavelength-react-native

- **`defaultConfig(network, overrides?)`** fills in gRPC `host:port` presets. On native, `arkServerAddress` and `swapServerAddress` are `host:port` values.
- **`createNativeClient(): ExternalSeedWalletClient`** takes no options. Its `ready()` resolves immediately. Activity arrives as typed `activity` events re-emitted from native `wavelengthActivity` device events.
- **External-seed startup:** `startExternalSeedWallet` requires a final nonempty `config.dataDir`. It never fills in the platform default.
- **`createNativeWalletEngine(options?: NativeWalletEngineOptions): WalletEngine`**. `NativeWalletEngineOptions` is `{ onPerformance? } & ({ config; autoStart: true } | { config?; autoStart?: false })`.
- **`createNativePasskeyCeremony(options: NativePasskeyCeremonyOptions): PasskeyCeremony`** uses Android Credential Manager and iOS AuthenticationServices. iOS support needs iOS 18+ and is experimental. `NativePasskeyCeremonyOptions` is `{ rpId: string }`.
- **`getDefaultDataDir(): Promise<string>`** returns a plain absolute path. That path is not guaranteed to exist until the runtime has started.

([source](../../raw/wavelength/reference/wavelength-react-native.md))

## Conflicts

- **`RUNTIME_ASSETS` keys:** the TypeScript declaration on the wavelength-web reference lists eight keys and has no `sqliteNodeVfs`. The filename table on the same page lists nine keys, including `sqliteNodeVfs` mapped to `sqlite-node-vfs.js`. ([source](../../raw/wavelength/reference/wavelength-web.md))
- **`RecoveryState` failed variant:** wavelength-core defines `{ status: 'failed'; error: Error; walletUsable: boolean }` ([source](../../raw/wavelength/reference/wavelength-core.md)). The `useWalletRecovery` entry on wavelength-react describes it as `{ status: 'failed', error: Error }` and says to read `phase` to tell the two cases apart ([source](../../raw/wavelength/reference/wavelength-react.md)).

See also: [[wavelength]], [[wavelength-web-sdk]], [[wavelength-react-native-sdk]], [[wavelength-native-mobile]], [[wavelength-concepts]], [[wavelength-unilateral-exit]], [[wavelength-api]], [[wavelength-cli]].
