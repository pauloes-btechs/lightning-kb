---
title: wavecli command reference
type: howto
sources:
  - raw/wavelength/cli.md
  - raw/wavelength/cli/create.md
  - raw/wavelength/cli/unlock.md
  - raw/wavelength/cli/send.md
  - raw/wavelength/cli/recv.md
  - raw/wavelength/cli/activity.md
  - raw/wavelength/cli/balance.md
  - raw/wavelength/cli/exit.md
  - raw/wavelength/cli/wallet-sweep.md
  - raw/wavelength/cli/getinfo.md
  - raw/wavelength/cli/bakemacaroon.md
  - raw/wavelength/cli/schema.md
  - raw/wavelength/cli/mcp.md
  - raw/wavelength/cli/ark.md
  - raw/wavelength/cli/recovery.md
  - raw/wavelength/cli/dev.md
updated: 2026-11-14
---

# wavecli command reference

`wavecli` is the command-line client for the Wavelength wallet daemon (`waved`). It issues gRPC calls to a running daemon and prints human or machine-readable output. The everyday surface is a small set of wallet verbs (create, unlock, send, recv, activity, balance, exit), plus daemon-introspection commands and advanced subtrees. For integrating over gRPC or REST from your own code, the source points to the API reference for `WalletService` and `WalletInspectionService`. ([source](../../raw/wavelength/cli.md))

See also: [[wavelength]], [[wavelength-api]], [[wavelength-concepts]], [[wavelength-wallet-guides]], [[wavelength-unilateral-exit]], [[macaroons]].

## Connecting

Every command talks to the daemon over gRPC, configured by persistent flags available on every command:

| Flag | Default | Description |
| --- | --- | --- |
| `--rpcserver` | `localhost:10029` | Daemon gRPC server address (`host:port`). |
| `--network` | `mainnet` | Bitcoin network used to resolve the default TLS certificate and macaroon paths. |
| `--tlscertpath` | (none) | Path to the daemon TLS certificate. |
| `--macaroonpath` | (none) | Path to the daemon RPC macaroon. |
| `--no-tls` | `false` | Disable TLS (development and regtest). |
| `--no-macaroons` | `false` | Disable macaroon authentication (development and regtest). |
| `--timeout` | `30s` | Maximum duration for each daemon RPC. `0` disables the deadline. |
| `--json` | `false` | Emit JSON output; shorthand for `--format json` on commands with a `--format` selector. |
| `--no-input` | `false` | Never prompt or implicitly consume stdin. `CI=true` has the same effect. |
| `--request-json` | (none) | Raw JSON request payload mapping directly to the RPC request proto. Do not combine with command-specific request inputs. |

([source](../../raw/wavelength/cli.md))

Flags are kebab-case, but every flag also accepts the snake_case spelling (`--max_fee` resolves to `--max-fee`). Ctrl-C and SIGTERM cancel the running command cleanly; a command interrupted while waiting on settlement reports a `CANCELED` envelope with the last observed phase. A local regtest daemon typically runs without TLS or macaroon auth, so pass `--no-tls --no-macaroons`. ([source](../../raw/wavelength/cli.md))

## Output and exit codes

Successful commands print a JSON object to stdout, using proto field names (snake_case) with unpopulated fields emitted. Prompts, the generated seed on `create`, and progress lines go to stderr. The exception is `activity`, which prints a table to stdout by default. On failure the command writes a JSON error envelope (`error` with `code`, `message`, `details`, `retryable`, and sometimes `remediation`) to stderr and exits non-zero. Example codes: `INVALID_ARGS`, `WALLET_LOCKED`, `NOT_FOUND`, `METHOD_NOT_FOUND`, `CONFIRMATION_REQUIRED`, `CANCELED`; codes that can fire after a fund-moving RPC was accepted (`DEADLINE_EXCEEDED`, `ABORTED`, `WAIT_TIMEOUT`) report `retryable: false`. ([source](../../raw/wavelength/cli.md))

| Exit code | Name | Meaning |
| --- | --- | --- |
| `0` | success | The command completed. |
| `1` | generic error | Catch-all failure. |
| `2` | invalid arguments | Rejected before reaching the daemon (missing required flag, malformed outpoint, conflicting `--offchain`/`--onchain`). |
| `3` | auth failure | Unauthenticated or not permitted, or the wallet is not ready (locked, not created, syncing). |
| `4` | not found | A queried resource does not exist. |
| `5` | confirmation required | A fund-moving action needs `--yes` (or `--force`) in a non-interactive environment. |

gRPC `InvalidArgument`, `OutOfRange` and `FailedPrecondition` map to `2`; `Unauthenticated` and `PermissionDenied` to `3`; `NotFound` to `4`; everything else to `1`. Wallet lifecycle preconditions arrive as `FailedPrecondition` but exit `3`. A wrong password on `unlock` exits `2`. ([source](../../raw/wavelength/cli.md))

## Wallet commands

### create

Initializes a new wallet: the daemon generates a 24-word aezeed mnemonic, prints it to stderr, and encrypts the seed with the supplied password. `--recover` with `--mnemonic-file` imports an existing mnemonic and rebuilds Ark wallet state. The password is never read from the command line; it comes, in priority order, from `WAVED_WALLET_PASSWORD`, `--wallet-password-file`, `--password-stdin`, or an interactive prompt, and otherwise the command exits `2`. The optional seed passphrase comes from `WAVED_SEED_PASSPHRASE` or `--seed-passphrase-file`. On a fresh create the mnemonic is written to stderr exactly once and is not in the stdout JSON unless `--print-mnemonic-json` is passed. ([source](../../raw/wavelength/cli/create.md))

| Flag | Default | Description |
| --- | --- | --- |
| `--wallet-password-file` | (none) | Path to a file containing the wallet password. |
| `--password-stdin` | `false` | Read one wallet password line from stdin. |
| `--seed-passphrase-file` | (none) | Path to a file containing the optional aezeed passphrase. |
| `--print-mnemonic-json` | `false` | Include the mnemonic in the JSON response on stdout. |
| `--recover` | `false` | Import an existing mnemonic and recover Ark wallet state. |
| `--mnemonic-file` | (none) | Path to an existing 24-word aezeed mnemonic. Requires `--recover`. |
| `--recovery-window` | `0` | Key indexes to scan per recovery family. Requires `--recover`; `0` uses the daemon default. |

```bash
printf '%s\n' 'hunter2hunter2' | wavecli create --password-stdin
```

Calls `WalletService.Create`. ([source](../../raw/wavelength/cli/create.md))

### unlock

Decrypts the on-disk wallet seed and starts the wallet subsystem. The password sources and priority order are the same as `create`. A wrong password exits `2` with an `INVALID_ARGUMENT` envelope; other commands against a locked wallet return `WALLET_LOCKED` and exit `3`. Calls `WalletService.Unlock`. ([source](../../raw/wavelength/cli/unlock.md))

| Flag | Default | Description |
| --- | --- | --- |
| `--wallet-password-file` | (none) | Path to a file containing the wallet password. |
| `--password-stdin` | `false` | Read one wallet password line from stdin. |

([source](../../raw/wavelength/cli/unlock.md))

### send

Dispatches an outbound payment: `wavecli send <invoice-or-onchain-address>`. With `--offchain` (the default) the destination is a BOLT-11 invoice routed through the swap subsystem, which picks a same-Ark peer-to-peer transfer or real Lightning. With `--onchain` the destination is a bech32 address and the daemon lands exactly `--amt` sats there, returning the residual as a change VTXO; `--sweep-all` with `--amt 0` drains every live VTXO. The CLI never sniffs the destination string. A Lightning send waits until a terminal state by default and prints the preimage on completion; on-chain sends never block and return a pending receipt. ([source](../../raw/wavelength/cli/send.md))

| Flag | Default | Description |
| --- | --- | --- |
| `--offchain` | `false` | Force offchain (BOLT-11 invoice) dispatch. Default when neither is set. |
| `--onchain` | `false` | Force onchain dispatch. |
| `--amt` | `0` | Amount in satoshis. Required for on-chain sends unless `--sweep-all`. |
| `--max-fee` | `0` | Max swap fee for invoice sends. `0` lets the daemon cap the fee at roughly 1% of the amount. |
| `--max-credit` | `0` | Offchain only: maximum total server credit the send may reserve. `0` disables credit use. |
| `--max-credit-topup` | `0` | Offchain only: maximum new Ark value the send may move into server credit. |
| `--note` | (none) | Caller-supplied label attached to the entry. |
| `--sweep-all` | `false` | On-chain only: drain the wallet to the destination. `--amt` must be `0`. |
| `--dry-run` | `false` | Prepare and print the preview without dispatching funds. |
| `--force` | `false` | Skip the interactive confirmation after prepare. |
| `--yes` | `false` | Alias for `--force`. |
| `--no-wait` | `false` | Return as soon as the send is dispatched. |
| `--wait-timeout` | `5m` | Give up waiting after this long. `0` waits indefinitely. |
| `--wait-poll-interval` | `200ms` | How often to poll the daemon while waiting. |

Non-interactively, `send` prints the preview to stderr and exits `5` (`CONFIRMATION_REQUIRED`) unless `--force` or `--yes` is passed. A failed Lightning send exits with a `SEND_FAILED` envelope; a wait timeout emits a `WAIT_TIMEOUT` envelope. It calls `WalletService.PrepareSend`, then `WalletService.Send`, and polls `WalletInspectionService.InspectActivity` while waiting. ([source](../../raw/wavelength/cli/send.md))

### recv

With `--offchain` (the default) the daemon opens a receive swap and returns a BOLT-11 invoice signed with a daemon-managed key; `--amt` is required. With `--onchain` it returns a fresh boarding address that the daemon rolls into the next round once funded. The `--offchain` path calls `WalletService.Recv`; `--onchain` calls `WalletService.Deposit`. ([source](../../raw/wavelength/cli/recv.md))

| Flag | Default | Description |
| --- | --- | --- |
| `--offchain` | `false` | Force offchain (Lightning invoice) recv. Default when neither is set. |
| `--onchain` | `false` | Force onchain (boarding address) recv. |
| `--amt` | `0` | Amount in satoshis. Required for `--offchain`. |
| `--memo` | (none) | Optional memo embedded in the offchain invoice. |
| `--amt-hint` | `0` | Optional expected amount for `--onchain` (accounting only). |

([source](../../raw/wavelength/cli/recv.md))

### activity

Shows the wallet's feed of sends, receives, deposits and exits; calls `WalletService.List` with the activity view. The default table has columns `LAST UPDATE`, `KIND`, `STATUS`, `AMOUNT`, `FEE`, `PHASE`, `ID`, `NOTE`. ([source](../../raw/wavelength/cli/activity.md))

| Flag | Default | Description |
| --- | --- | --- |
| `--pending` | `false` | Only show entries still in flight. |
| `--kind` | (none) | Filter by kind (send, recv, deposit, exit); repeatable. |
| `--limit` | `0` | Page size; 0 uses the daemon default. |
| `--cursor` | (none) | Page token from a prior page's `next_cursor`. |
| `--format` | `table` | Output format: table, expanded, x, or json. |

`activity inspect <id>` inspects one entry with correlated swap, VTXO and ledger detail, calling `WalletInspectionService.InspectActivity`. Its flags are `--ledger-limit` (default `0`, the daemon maximum) and `--format` (default `expanded`; expanded, x, or json). ([source](../../raw/wavelength/cli/activity.md))

### balance

Returns the unified wallet balance (`confirmed_sat`, `pending_in_sat`, `pending_out_sat`) plus server-authoritative credit balances. Takes no bespoke flags beyond the global connection flags. Calls `WalletService.Balance`. ([source](../../raw/wavelength/cli/balance.md))

### exit

Queues a VTXO outpoint for cooperative leave; if `--onchain-address` is omitted the daemon generates a fresh backing-wallet destination. Unilateral unroll starts only when `--force-unroll-ack` is exactly `I_KNOW_WHAT_I_AM_DOING`. The default path calls `WalletService.Exit`. ([source](../../raw/wavelength/cli/exit.md))

| Flag | Default | Description |
| --- | --- | --- |
| `--outpoint` | (none) | Required. VTXO outpoint to exit, as `txid:vout`. |
| `--onchain-address` | (none) | Cooperative leave destination. Cannot be combined with `--force-unroll-ack`. |
| `--force-unroll-ack` | (none) | Exact acknowledgement (`I_KNOW_WHAT_I_AM_DOING`) required to force unilateral unroll. |
| `--dry-run` | `false` | Validate locally and print the preview without dispatching. |

Subcommands: `exit status --outpoint` (with `--detailed`, default `true`; `--detailed=false` for a cheaper phase-only status) calls `WalletService.ExitStatus`; `exit summary` takes no flags and calls `WalletService.ExitSummary`; `exit plan --outpoint` (repeatable) previews backing-wallet funding readiness without dispatching and calls `WalletService.GetExitPlan`. ([source](../../raw/wavelength/cli/exit.md))

### wallet-sweep

Previews, or with `--broadcast` publishes, a sweep of every confirmed backing-wallet UTXO to one destination. Boarding outputs are excluded (use `ark sweep`). Broadcasting non-interactively exits `5` unless `--yes` is passed. Calls `WalletService.SweepWallet`. ([source](../../raw/wavelength/cli/wallet-sweep.md))

| Flag | Default | Description |
| --- | --- | --- |
| `--destination` | (none) | Required. On-chain destination address. |
| `--broadcast` | `false` | Publish the sweep. Omitted means preview only. |
| `--yes` | `false` | Approve broadcasting the fund-moving sweep. |
| `--fee-rate` | `0` | Explicit fee rate in sat/vByte. `0` estimates at `--conf-target`. |
| `--conf-target` | `0` | Confirmation target for fee estimation when `--fee-rate` is `0`. |

([source](../../raw/wavelength/cli/wallet-sweep.md))

## Daemon commands

### getinfo

Returns version, network, wallet state, block height and identity pubkey; the source calls it the first call to make when checking the daemon is reachable. No bespoke flags. Calls `GetInfo` on `DaemonService`, which has no `WalletService` equivalent. ([source](../../raw/wavelength/cli/getinfo.md))

### bakemacaroon

Creates a daemon credential limited to named `entity:action` permissions, or to one exact method via the `uri` entity, for example `uri:/waverpc.DaemonService/GetInfo`. With `--request-json`, put `permissions` and `rootKeyId` in the JSON instead. Without `--save-to`, stdout has the hex macaroon in a `macaroon` field; with it, the binary credential is written with private file permissions and stdout has only its `path`. Calls `MacaroonService.BakeMacaroon`. ([source](../../raw/wavelength/cli/bakemacaroon.md))

| Flag | Default | Description |
| --- | --- | --- |
| `--save-to` | (none) | Save the binary macaroon to a new file; refuses to replace an existing file or symlink. |
| `--root-key-id` | `0` | Numeric macaroon root key ID. Zero uses the daemon default. |
| `--valid-for` | `0` | Client-side expiry in seconds. Zero means no expiry. |

([source](../../raw/wavelength/cli/bakemacaroon.md))

### schema

Returns a CLI command's method signature as JSON (parameters, types, required fields, enum values, request and response proto type names). With no arguments it lists method names; pass a name for one schema, or `--all` (default `false`) for every schema. Entries report `request_json_input`, `mcp_tool`, `side_effect`, `output_schema_id` and `output_schema_version`. An unknown name exits `4` with `METHOD_NOT_FOUND`. It makes no RPC call. ([source](../../raw/wavelength/cli/schema.md))

### mcp

`mcp serve` starts a Model Context Protocol server on stdio that exposes daemon RPCs as typed tool calls; `mcp` alone prints usage. No bespoke flags. Create, unlock and seed generation are never registered as MCP tools. Registered tools include `balance`, `getinfo`, the send surfaces, and the `ark.*` namespace (for example `ark.vtxos.list`, `ark.vtxos.refresh`, `ark.vtxos.leave`, `ark.oor.receive`, `ark.send.inround`, `ark.send.oor`). A real `ark.vtxos.refresh` or raw send requires `yes: true`; `dry_run: true` previews are ungated. ([source](../../raw/wavelength/cli/mcp.md))

## Advanced commands

### ark

Power-user entry point to the raw daemon RPCs. List-shaped subcommands accept `--fields` and `--ndjson`. `ark` itself takes no bespoke flags. ([source](../../raw/wavelength/cli/ark.md))

| Subcommand | Key flags | Daemon RPC |
| --- | --- | --- |
| `vtxos list` | `--status` (repeatable), `--all`, `--min-amount`, `--asset-ref`, `--fields`, `--ndjson` | `ListVTXOs` |
| `vtxos refresh` | `--outpoint` (repeatable), `--all`, `--dry-run`, `--yes`, `--no-join` | `RefreshVTXOs` |
| `vtxos leave` | `--outpoint`, `--all`, `--address`, `--pk-script`, `--destination`, `--dry-run`, `--yes`, `--no-join` | `LeaveVTXOs` |
| `rounds get` | `--round-id` | `GetRound` |
| `rounds join` | (none) | `JoinNextRound` |
| `rounds list` | `--persisted-only`, `--page-size`, `--page-token`, `--state`, `--created-after`, `--created-before`, `--fields`, `--ndjson` | `ListRounds` |
| `rounds watch` | `--max-events`, `--for` | `WatchRounds` |
| `oor get` | `--session-id` | `GetOORSession` |
| `oor list` | `--direction` (default `all`), `--status` (default `all`), `--page-size`, `--page-token`, `--fields`, `--ndjson` | `ListOORSessions` |
| `oor receive` | `--label`, `--idempotency-key` | `NewReceiveScript` |
| `board` | `--target-vtxo-count`, `--no-persist` | `Board` |
| `sweep` | `--outpoint`, `--broadcast`, `--yes`, `--fee-rate-sat-per-vbyte`, `--conf-target`, `--sweep-address` | `SweepBoardingUTXOs` |
| `sweep list` | `--status`, `--page-size`, `--page-token`, `--fields`, `--ndjson` | `ListBoardingSweeps` |
| `fees estimate` | `--amount` (required), `--boarding` (default `true`), `--remaining-blocks` | `EstimateFee` |
| `fees history` | `--limit` (default `50`), `--offset`, `--after-entry-id`, `--event-type` | `GetFeeHistory` |
| `listtransactions` | `--from`, `--to`, `--limit` (default `50`), `--offset`, `--type`, `--fields`, `--ndjson` | `ListTransactions` |
| `send inround` | `--to`, `--pubkey`, `--amount`, `--dry-run`, `--yes` | `SendVTXO` |
| `send oor` | `--to`, `--pubkey`, `--amount`, `--dry-run`, `--yes`, `--idempotency-key` | `SendOOR` |

([source](../../raw/wavelength/cli/ark.md))

`vtxos refresh` is charged an operator fee, so it asks before queuing; non-interactively it exits `5` unless `--yes` or `--dry-run` is passed. `--dry-run` returns an itemized advisory estimate; the binding fee comes from the server-issued quote when the round seals. `vtxos refresh` and `vtxos leave` issue `ark rounds join` automatically unless `--no-join` is set. ([source](../../raw/wavelength/cli/ark.md))

### recovery

Manages already-armed vHTLC recovery rows; the source describes these as operator escalation and intervention tools, and says escalating starts costly on-chain unroll. ([source](../../raw/wavelength/cli/recovery.md))

| Subcommand | Flags | Daemon RPC |
| --- | --- | --- |
| `recovery list` | `--include-terminal` (default `false`) | `ListVHTLCRecoveries` |
| `recovery status <recovery_id>` | (none) | `GetVHTLCRecoveryStatus` |
| `recovery escalate <recovery_id>` | `--reason` (default `"manual client escalation"`), `--claim-preimage-hex`, `--yes` | `EscalateVHTLCRecovery` |
| `recovery cancel <recovery_id>` | `--reason` (default `"manual client cancellation"`), `--cooperative-txid` | `CancelVHTLCRecovery` |

`recovery escalate` non-interactively exits `5` with `CONFIRMATION_REQUIRED` unless `--yes` is passed. ([source](../../raw/wavelength/cli/recovery.md))

### dev

A generated command tree exposing every daemon gRPC method, built at startup from the proto descriptors compiled into the binary (the `devrpc` registry). Invocation is `dev <grpc_service> <call>`; method flags are generated from request fields, each leaf accepts `--request-json`, and `--describe` dumps the input-field schema without dispatching. Client-streaming methods are not supported. Exposed services: `waverpc.DaemonService` (alias `daemon`), `swapclientrpc.SwapClientService`, `wavewalletrpc.WalletService`, `wavewalletrpc.WalletInspectionService`, `walletrpc.VersionService` and `walletrpc.WalletService`. ([source](../../raw/wavelength/cli/dev.md))

```bash
wavecli dev
wavecli dev waverpc.DaemonService GetInfo --describe
```

([source](../../raw/wavelength/cli/dev.md))
