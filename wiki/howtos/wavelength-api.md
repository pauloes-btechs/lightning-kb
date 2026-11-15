---
title: Wavelength remote API (gRPC and REST)
type: howto
sources:
  - raw/wavelength/api.md
  - raw/wavelength/api/get-started.md
  - raw/wavelength/api/rest.md
  - raw/wavelength/api/wallet/create.md
  - raw/wavelength/api/wallet/unlock.md
  - raw/wavelength/api/wallet/status.md
  - raw/wavelength/api/wallet/prepare-send.md
  - raw/wavelength/api/wallet/send.md
  - raw/wavelength/api/wallet/recv.md
  - raw/wavelength/api/wallet/deposit.md
  - raw/wavelength/api/wallet/balance.md
  - raw/wavelength/api/wallet/list.md
  - raw/wavelength/api/wallet/subscribe-wallet.md
  - raw/wavelength/api/wallet/inspect-activity.md
  - raw/wavelength/api/wallet/get-exit-plan.md
  - raw/wavelength/api/wallet/exit.md
  - raw/wavelength/api/wallet/exit-status.md
  - raw/wavelength/api/wallet/exit-summary.md
  - raw/wavelength/api/wallet/sweep-wallet.md
updated: 2026-11-14
---

# Wavelength remote API (gRPC and REST)

The Wavelength wallet daemon (`waved`) exposes a wallet API, `WalletService`, over both gRPC and REST. It has 15 methods covering create and unlock, sending and receiving Lightning and on-chain payments, balance and activity, and exiting to a self-custodial on-chain position. A companion service, `WalletInspectionService`, adds one read-only method for inspecting activity entries, for 16 methods total. ([source](../../raw/wavelength/api.md))

The API is meant for remote integrations: a backend service managing a wallet for your product, an internal dashboard, a monitoring script, or any process talking to a `waved` instance you run yourself. The SDK instead compiles `waved` to run inside your app (WebAssembly in the browser, or into the app binary on React Native), with keys on each user's device. The source recommends the SDK when each user holds their own keys, and this API when automating or operating a wallet from a backend you control. ([source](../../raw/wavelength/api.md))

The API surface is versioned together with the daemon, not independently; the source says to pin a specific daemon version for production integrations. ([source](../../raw/wavelength/api.md))

See also: [[wavelength]], [[wavelength-cli]], [[wavelength-concepts]], [[wavelength-unilateral-exit]], [[wavelength-sdk-reference]], [[macaroons]].

## Getting started

### Build tags

`WalletService` and `WalletInspectionService` are compiled into `waved` only when it is built with both the `wavewalletrpc` and `swapruntime` build tags. With `wavewalletrpc` but not `swapruntime` the build succeeds, but a stub takes over and the wallet API is silently omitted. A default source build (`make build`) includes neither tag, and calls against it fail with gRPC's unknown-service error, surfacing as the `Unimplemented` status code. ([source](../../raw/wavelength/api/get-started.md))

Prebuilt release binaries carry both tags as of `v0.1.2-rc4`, so the `waved` in any per-platform archive (`wavelength-<os>-<arch>-<version>`, a `.tar.gz` except for the Windows `.zip`) already serves the wallet API. To build from source with the tags:

```bash
make build-wavewalletrpc
```

This produces `bin/waved` and `bin/wavecli`. `make install-wavewalletrpc` does the same via `go install`, placing the binaries in `$GOPATH/bin`. ([source](../../raw/wavelength/api/get-started.md))

### Endpoints and security

| Protocol | Default address | Notes |
| --- | --- | --- |
| gRPC | `localhost:10029` | The daemon's own RPC server. |
| REST | `localhost:10031` | An HTTP/JSON gateway in front of the same RPCs, enabled by default. |

Every `WalletService` and `WalletInspectionService` method is reachable on both listeners with the same request and response shape, modulo JSON encoding. ([source](../../raw/wavelength/api/get-started.md))

The gRPC listener serves TLS and enforces a macaroon on every call. For loopback development and regtest both can be disabled with `--rpc.notls` and `--rpc.no-macaroons`, but on a mainnet TCP listener the daemon refuses both. A deployment that terminates TLS and enforces authentication at an external proxy can set `allow-insecure-mainnet` to override that refusal. ([source](../../raw/wavelength/api/get-started.md))

The default macaroon is written to `admin.macaroon` under the daemon's network directory. The REST gateway is a local plaintext HTTP proxy that forwards the `macaroon` HTTP header to the gRPC backend, so REST calls need that header whenever macaroons are enabled. The daemon refuses a non-loopback `rpc.gateway.listenaddr` on mainnet unless `allow-insecure-mainnet` is set. ([source](../../raw/wavelength/api/get-started.md))

### First call

`StatusRequest` is empty, so an empty JSON object is a complete request body. Against a local daemon started with `--rpc.no-macaroons` (otherwise add `-H "macaroon: <hex>"`):

```bash
curl -X POST http://localhost:10031/v1/wallet/status -d '{}'
```

The CLI equivalent is `wavecli getinfo --no-tls --no-macaroons`, which talks to the daemon's `DaemonService` rather than `WalletService.Status`, but confirms that `wavecli` can reach `waved`. ([source](../../raw/wavelength/api/get-started.md))

## REST conventions

The REST gateway is a grpc-gateway HTTP/JSON proxy. Every method is a `POST` under `/v1/wallet/...`, whether the RPC reads or writes. Request bodies are JSON objects whose field names match the proto field names exactly, in `snake_case`. Methods with an empty request message still take a body: `{}`. ([source](../../raw/wavelength/api/rest.md))

`uint64` fields such as `amt_sat` and `max_fee_sat` are encoded as JSON strings to avoid precision loss; omitted fields take their proto zero value. For a `oneof` (for example `invoice` / `onchain_address` in `PrepareSendRequest`), set only one member per call. ([source](../../raw/wavelength/api/rest.md))

Errors come back as a JSON body shaped like `google.rpc.Status` with `code`, `message` and `details`. `code` is the numeric gRPC status code (for example `3` for `INVALID_ARGUMENT`), not the HTTP status; the gateway also sets the HTTP status via its own mapping (`INVALID_ARGUMENT` becomes `400`, `NOT_FOUND` becomes `404`). This is the grpc-gateway default error handler; the daemon installs no custom mapper. ([source](../../raw/wavelength/api/rest.md))

`SubscribeWallet` is the one server-streaming method (`POST /v1/wallet/subscribe`). The gateway keeps the connection open and emits one newline-delimited envelope per message, under a `result` field. The gateway's HTTP server disables its write timeout entirely, so the connection stays open until the client closes it. This envelope is separate from Wavelength's camelCase facade stream, which delivers an `Entry` as the payload of an `activity` event. ([source](../../raw/wavelength/api/rest.md))

## Shared message: `WalletEntry`

`WalletEntry` is the flat row type returned by the ACTIVITY view of `List` and by `SubscribeWallet`; power-user detail belongs in `WalletInspectionService.InspectActivity`. ([source](../../raw/wavelength/api/wallet/send.md)) It also appears as the `entry` field of `SendResponse`, `RecvResponse`, `DepositResponse` and `InspectActivityResponse`. ([source](../../raw/wavelength/api/wallet/send.md), [source](../../raw/wavelength/api/wallet/recv.md), [source](../../raw/wavelength/api/wallet/deposit.md), [source](../../raw/wavelength/api/wallet/inspect-activity.md))

Fields: `id`, `kind` (`EntryKind`), `status` (`EntryStatus`), `amount_sat` (signed: positive incoming, negative outgoing), `fee_sat`, `counterparty`, `created_at_unix`, `updated_at_unix`, `note`, `failure_reason`, `request` (`WalletEntryRequest`), `progress` (`WalletEntryProgress`), and optional `failure_code` (`EntryFailureCode`, set only on FAILED entries). ([source](../../raw/wavelength/api/wallet/send.md))

`id` is the Lightning `payment_hash` for swap-backed SEND and RECV rows, the credit operation id for credit-backed RECV rows, `leave_job_id` (or sweep txid) for EXIT rows, and the boarding outpoint or txid for DEPOSIT rows. ([source](../../raw/wavelength/api/wallet/send.md))

`EntryKind` values: `ENTRY_KIND_UNSPECIFIED`, `ENTRY_KIND_SEND`, `ENTRY_KIND_RECV`, `ENTRY_KIND_DEPOSIT`, `ENTRY_KIND_EXIT`. `EntryStatus` values: `ENTRY_STATUS_UNSPECIFIED`, `ENTRY_STATUS_PENDING`, `ENTRY_STATUS_COMPLETE`, `ENTRY_STATUS_FAILED`. `EntryFailureCode` values: `ENTRY_FAILURE_CODE_UNSPECIFIED`, `ENTRY_FAILURE_CODE_TIMED_OUT`, `ENTRY_FAILURE_CODE_EXPIRED`, `ENTRY_FAILURE_CODE_REFUNDED`, `ENTRY_FAILURE_CODE_NEEDS_INTERVENTION`, `ENTRY_FAILURE_CODE_FAILED`. ([source](../../raw/wavelength/api/wallet/send.md))

`WalletEntryProgress` carries `phase` (`WalletEntryPhase`), `phase_label`, `payment_hash`, `txid`, `confirmation_height`, `vtxo_outpoint`, `preimage` (proof of payment for a completed Lightning-backed send), `waiting_reason` and `batch_window` (`ScheduledBatchWindow`: `registration_opens_unix`, `cutoff_unix`, `planned_join_unix_ms`). `WalletEntryRequest` is a oneof of `lightning_invoice` (`invoice`, `payment_hash`), `onchain_address` (`address`, `sweep_all`) and `ark_address` (`address`). ([source](../../raw/wavelength/api/wallet/send.md))

## Wallet lifecycle

### Create

Initializes a new wallet from a freshly generated aezeed mnemonic, encrypts it with the supplied password, and returns the mnemonic. For recovery the caller may supply an existing mnemonic, which is echoed back. Proxies `waverpc.GenSeed` + `waverpc.InitWallet`.

- gRPC: `rpc Create(CreateRequest) returns (CreateResponse)`
- REST: `POST /v1/wallet/create`
- CLI: `wavecli create`
- Request: `wallet_password` (at least 8 bytes), `seed_passphrase`, `mnemonic` (24 words; empty generates a fresh seed), `recover_state`, `recovery_window` (zero uses the daemon `wallet.recoverywindow` config value).
- Response: `mnemonic`, `identity_pubkey`, `recovery_ran`, `recovered_boarding_addresses`, `recovered_boarding_utxos`, `recovered_vtxos`, `recovered_oor_receive_scripts`, `recovered_oor_events`.

For fresh wallets the caller must persist the mnemonic offline; losing it makes the wallet unrecoverable. ([source](../../raw/wavelength/api/wallet/create.md))

### Unlock

Decrypts the on-disk wallet seed with the supplied password and starts the wallet subsystem. Proxies `waverpc.UnlockWallet`.

- gRPC: `rpc Unlock(UnlockRequest) returns (UnlockResponse)`
- REST: `POST /v1/wallet/unlock`
- CLI: `wavecli unlock`
- Request: `wallet_password`.
- Response: `identity_pubkey`.

([source](../../raw/wavelength/api/wallet/unlock.md))

### Status

Returns a wallet-level readiness summary: daemon readiness, wallet-unlocked state, balance summary and pending-entry count. Not surfaced as a CLI verb; `getinfo` covers the human-facing readiness view.

- gRPC: `rpc Status(StatusRequest) returns (StatusResponse)`
- REST: `POST /v1/wallet/status`
- Request: `StatusRequest` has no fields.
- Response: `ready`, `unlocked` (a legacy wallet-exists signal; use `ready` to check whether wallet RPCs are usable), `network`, `balance` (`BalanceResponse`), `pending_count`.

([source](../../raw/wavelength/api/wallet/status.md))

## Sending

### PrepareSend

Validates and previews an outbound payment without moving funds. The response carries a short-lived `send_intent_id` that must be consumed by `Send`.

- gRPC: `rpc PrepareSend(PrepareSendRequest) returns (PrepareSendResponse)`
- REST: `POST /v1/wallet/prepare-send`
- CLI: `wavecli send`
- Request: oneof `destination` (`invoice` or `onchain_address`), `amt_sat`, `note`, `max_fee_sat`, `sweep_all`, `max_credit_sat`, `max_credit_topup_sat`.
- Response: `send_intent_id`, `amount_sat`, `expected_fee_sat`, `fee_known`, `expected_total_outflow_sat`, `total_outflow_known`, `rail` (`SendRail`), `quote_status` (`SendQuoteStatus`), `destination_summary`, `invoice_description`, `payment_hash`, `expires_at_unix`, `selected_outpoints`, `warning`, `credit_preview` (`CreditPreview`).

`amt_sat` is required and strictly positive for on-chain sends unless `sweep_all` is set, in which case it must be zero. For invoice sends `amt_sat` is ignored: v1 requires an amount-bearing BOLT-11 invoice. `SendRail` values: `SEND_RAIL_UNSPECIFIED`, `SEND_RAIL_OFFCHAIN_UNKNOWN`, `SEND_RAIL_IN_ARK`, `SEND_RAIL_LIGHTNING`, `SEND_RAIL_ONCHAIN`, `SEND_RAIL_CREDIT`, `SEND_RAIL_MIXED`. `SendQuoteStatus` values: `SEND_QUOTE_STATUS_UNSPECIFIED`, `SEND_QUOTE_STATUS_COMPLETE`, `SEND_QUOTE_STATUS_LOCAL_ONLY`. `CreditPreview` fields: `must_use_credit`, `credit_applied_sat`, `credit_shortfall_sat`, `credit_topup_sat`, `ark_funding_sat`. ([source](../../raw/wavelength/api/wallet/prepare-send.md))

### Send

Dispatches a previously prepared outbound payment. The request is intent-only: callers must use `PrepareSend` first.

- gRPC: `rpc Send(SendRequest) returns (SendResponse)`
- REST: `POST /v1/wallet/send`
- CLI: `wavecli send`
- Request: `send_intent_id` (may be consumed once).
- Response: `entry` (`WalletEntry`), `actual_amount_sat`.

For a `sweep_all` on-chain send, `actual_amount_sat` reflects the sum of the swept VTXOs; the source says CLI and UI surfaces should echo it back before treating the send as confirmed. Callers can poll `List` or `SubscribeWallet` for status transitions. ([source](../../raw/wavelength/api/wallet/send.md))

## Receiving

### Recv

Asks the daemon for a Lightning invoice the caller can hand out. The daemon sets up the inbound receive via its swap subsystem; the invoice is signed with a daemon-managed key.

- gRPC: `rpc Recv(RecvRequest) returns (RecvResponse)`
- REST: `POST /v1/wallet/recv`
- CLI: `wavecli recv` (`--offchain`)
- Request: `amt_sat`, `memo`.
- Response: `invoice`, `entry` (`WalletEntry`), `credit_receive` (`CreditReceive`: `operation_id`, `amount_sat`, `payment_hash`), populated when the receive is backed by server credits rather than a client-claimable vHTLC.

([source](../../raw/wavelength/api/wallet/recv.md))

### Deposit

Returns a boarding on-chain address the caller can fund; the daemon rolls the boarding output into a VTXO during the next round. Surfaced via `recv --onchain`; not a top-level CLI verb.

- gRPC: `rpc Deposit(DepositRequest) returns (DepositResponse)`
- REST: `POST /v1/wallet/deposit`
- Request: `amt_sat_hint` (optional; the returned address is not amount-bound).
- Response: `onchain_address`, `entry` (a DEPOSIT-kind `WalletEntry`).

([source](../../raw/wavelength/api/wallet/deposit.md))

## Balance and activity

### Balance

Returns the unified balance across confirmed VTXOs and in-flight inbound and outbound amounts.

- gRPC: `rpc Balance(BalanceRequest) returns (BalanceResponse)`
- REST: `POST /v1/wallet/balance`
- CLI: `wavecli balance`
- Request: `BalanceRequest` has no fields.
- Response: `confirmed_sat`, `pending_in_sat` (boarding plus receive), `pending_out_sat` (send plus exit), `credit_available_sat`, `credit_reserved_sat`.

([source](../../raw/wavelength/api/wallet/balance.md))

### List

Returns the wallet view selected by `ListRequest.view`: ACTIVITY (default) is the merged `WalletEntry` stream, VTXOS the live VTXO inventory, ONCHAIN the boarding-plus-sweep on-chain history.

- gRPC: `rpc List(ListRequest) returns (ListResponse)`
- REST: `POST /v1/wallet/list`
- CLI: `wavecli activity`
- Request: `view` (`ListView`: `LIST_VIEW_UNSPECIFIED`, `LIST_VIEW_ACTIVITY`, `LIST_VIEW_VTXOS`, `LIST_VIEW_ONCHAIN`), `pending_only`, `kinds`, `limit`, `offset` (VTXOS and ONCHAIN only), `cursor` (ACTIVITY only).
- Response: oneof `body`: `activity` (`ActivityList`: `entries`, `total`, `has_more`, `next_cursor`), `vtxos` (`VTXOInventory`: `vtxos`, `total`), or `onchain` (`OnchainHistory`: `txs`, `total`, `has_more`).

`WalletVTXO` fields: `outpoint`, `amount_sat`, `status`, `batch_expiry`, `relative_expiry`, `commitment_txid`. `OnchainTx` fields: `txid`, `kind`, `amount_sat`, `fee_sat`, `status`, `confirmation_height`, `created_at_unix`, `description`. In `ActivityList`, `total` is a page count; callers use `has_more` to decide whether to fetch again. ([source](../../raw/wavelength/api/wallet/list.md))

### SubscribeWallet

Streams activity updates as they happen. The stream is resumable: each response carries a monotonic cursor the client can reconnect from.

- gRPC: `rpc SubscribeWallet(SubscribeWalletRequest) returns (stream SubscribeWalletResponse)`
- REST: `POST /v1/wallet/subscribe`
- Request: `include_existing` (ignored when `cursor` is set), `kinds`, `cursor`.
- Response (stream): `cursor`, then oneof `update`: `entry` (`WalletEntry`) or `gap` (`SubscribeGap`: `reason`).

The cursor sequence is monotonic but not contiguous, so a client must not infer a dropped event from a gap in the numbers. A `gap` means the subscriber fell behind the live buffer and should reconcile via `List`, then resume from the cursor; the event log retains every event. ([source](../../raw/wavelength/api/wallet/subscribe-wallet.md))

### InspectActivity (WalletInspectionService)

Returns a technical trace for one `WalletEntry` id.

- gRPC: `rpc InspectActivity(InspectActivityRequest) returns (InspectActivityResponse)`
- REST: `POST /v1/wallet/inspect/activity`
- CLI: `wavecli activity inspect`
- Request: `id`, `ledger_limit` (zero uses the daemon's maximum list limit).
- Response: `entry` (`WalletEntry`), `swap` (`ActivitySwapTrace`), `vtxos` (repeated `ActivityVTXOTrace`), `ledger_rows` (repeated `ActivityLedgerTrace`), `notes`.

`vtxos` rows are best-effort correlations, and `ledger_rows` include rows hidden from the friendly activity feed. ([source](../../raw/wavelength/api/wallet/inspect-activity.md))

## Exit and sweep

### GetExitPlan

Previews unilateral-exit readiness for VTXOs, including CPFP fee input requirements and, when funding is needed, a backing-wallet address to fund before forced unroll.

- gRPC: `rpc GetExitPlan(GetExitPlanRequest) returns (GetExitPlanResponse)`
- REST: `POST /v1/wallet/exit-plan`
- CLI: `wavecli exit plan`
- Request: `outpoints`, `conf_target`.
- Response: `plans` (repeated `ExitPlanEntry`), `fee_rate_sat_per_vbyte`, `can_start`, `total_funding_shortfall_sat`, `total_recommended_funding_sat`.

`ExitPlanEntry` fields: `outpoint`, `funding_address`, `required_confirmations`, `required_fee_utxo_count`, `usable_fee_utxo_count`, `recommended_utxo_amount_sat`, `recommended_total_funding_sat`, `funding_shortfall_sat`, `can_start`, `exit_job_found`, `exit_status`, `sweep_txid`, `last_error`, `error`, `infeasibility_reason`, `round_commitment`. `ExitInfeasibilityReason` values: `EXIT_INFEASIBILITY_REASON_UNSPECIFIED`, `EXIT_INFEASIBILITY_REASON_SWEEP_BELOW_DUST`, `EXIT_INFEASIBILITY_REASON_UNECONOMICAL`, `EXIT_INFEASIBILITY_REASON_WALLET_UNDERFUNDED`, `EXIT_INFEASIBILITY_REASON_WALLET_TOO_FEW_INPUTS`, `EXIT_INFEASIBILITY_REASON_ROUND_COMMITTED`. Entries are evaluated against a running wallet allocation, so the top-level `can_start` is true only when every requested exit can be funded simultaneously. ([source](../../raw/wavelength/api/wallet/get-exit-plan.md))

### Exit

Queues a cooperative leave for the specified VTXO outpoint by default. When `force_unroll_ack` is supplied exactly, the daemon starts a unilateral unroll instead, after checking the outpoint is in the local backing wallet's UTXO set.

- gRPC: `rpc Exit(ExitRequest) returns (ExitResponse)`
- REST: `POST /v1/wallet/exit`
- CLI: `wavecli exit`
- Request: `outpoint` (`"txid:index"`), `onchain_address` (empty generates a fresh backing-wallet address), `force_unroll_ack` (must be exactly `"I_KNOW_WHAT_I_AM_DOING"`; cannot be combined with `onchain_address`; the server requires at least one confirmed local backing-wallet UTXO).
- Response: `created`, `actor_id`, `mode` (`ExitMode`: `EXIT_MODE_UNSPECIFIED`, `EXIT_MODE_COOPERATIVE`, `EXIT_MODE_UNILATERAL`), `queued_outpoints`, `onchain_address`.

([source](../../raw/wavelength/api/wallet/exit.md))

### ExitStatus

Reports the current phase of an unroll job for a VTXO outpoint, including recovery chain progress and sweep state. Proxies `waverpc.GetUnrollStatus`.

- gRPC: `rpc ExitStatus(ExitStatusRequest) returns (ExitStatusResponse)`
- REST: `POST /v1/wallet/exit-status`
- CLI: `wavecli exit status`
- Request: `outpoint`, `detailed`.
- Response: `found`, `status` (`ExitJobStatus`), `sweep_txid`, `last_error`, and, on a detailed query, `phase_detail`, `progress` (`ExitProgress`), `csv` (`ExitCSV`), `fees` (`ExitFees`), `best_case_blocks_remaining`, `current_height`.

`detailed` costs one extra child actor round-trip plus a fee estimate, so the source says to set it only for interactive status commands, not automated polling. `ExitJobStatus` values: `EXIT_JOB_STATUS_UNSPECIFIED`, `EXIT_JOB_STATUS_PENDING`, `EXIT_JOB_STATUS_MATERIALIZING`, `EXIT_JOB_STATUS_CSV_PENDING`, `EXIT_JOB_STATUS_SWEEPING`, `EXIT_JOB_STATUS_COMPLETED`, `EXIT_JOB_STATUS_FAILED`. ([source](../../raw/wavelength/api/wallet/exit-status.md))

### ExitSummary

Reports the wallet-wide portfolio of in-progress exits: one row per active exit plus aggregate totals. Only non-terminal exits are included.

- gRPC: `rpc ExitSummary(ExitSummaryRequest) returns (ExitSummaryResponse)`
- REST: `POST /v1/wallet/exit-summary`
- CLI: `wavecli exit summary`
- Request: `ExitSummaryRequest` has no fields.
- Response: `exits` (repeated `ExitSummaryItem`: `outpoint`, `status`, `vtxo_amount_sat`, `est_total_fee_sat`, `est_net_recovered_sat`), `total_exits`, `total_vtxo_amount_sat`, `total_est_fee_sat`, `total_est_net_recovered_sat`.

([source](../../raw/wavelength/api/wallet/exit-summary.md))

### SweepWallet

Previews or broadcasts a backing-wallet sweep to a caller-supplied Bitcoin address. It sweeps wallet-managed funds left after CPFP/change/unroll proceeds and does not sweep boarding outputs.

- gRPC: `rpc SweepWallet(SweepWalletRequest) returns (SweepWalletResponse)`
- REST: `POST /v1/wallet/sweep-wallet`
- CLI: `wavecli wallet-sweep`
- Request: `destination_address`, `broadcast`, `fee_rate_sat_per_vbyte` (overrides estimation when positive), `conf_target`.
- Response: `inputs` (repeated `WalletSweepInput`: `outpoint`, `amount_sat`), `total_input_sat`, `estimated_fee_sat`, `net_amount_sat`, `fee_rate_sat_per_vbyte`, `can_broadcast`, `txid` (set only when broadcast), `failure_reason`.

([source](../../raw/wavelength/api/wallet/sweep-wallet.md))

## Conflicts

- **CLI coverage of `WalletService`.** The get-started page says `wavecli` "wraps every `WalletService` method as a subcommand" ([source](../../raw/wavelength/api/get-started.md)), but the Status page says `Status` is "not surfaced as a CLI verb" ([source](../../raw/wavelength/api/wallet/status.md)), and the SubscribeWallet page names no CLI command ([source](../../raw/wavelength/api/wallet/subscribe-wallet.md)).
- **REST stream envelope shape.** The REST conventions page shows a streamed envelope as `{"result":{"id":"activity-id","kind":"ENTRY_KIND_SEND"}}`, with entry fields directly under `result` ([source](../../raw/wavelength/api/rest.md)), while the SubscribeWallet page defines each streamed `SubscribeWalletResponse` as `cursor` plus a oneof `entry` or `gap` ([source](../../raw/wavelength/api/wallet/subscribe-wallet.md)).
