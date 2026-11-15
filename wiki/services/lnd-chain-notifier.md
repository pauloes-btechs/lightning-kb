---
title: lnd chain-notifier service
type: service
sources:
  - raw/api/api-docs/api/lnd.md
  - raw/api/api-docs/api/lnd/rest-endpoints.md
  - raw/api/api-docs/api/lnd/chain-notifier/register-block-epoch-ntfn.md
  - raw/api/api-docs/api/lnd/chain-notifier/register-confirmations-ntfn.md
  - raw/api/api-docs/api/lnd/chain-notifier/register-spend-ntfn.md
updated: 2026-11-14
---

# lnd chain-notifier service (ChainNotifier)

This page covers the ChainNotifier service of [[lnd]]. RegisterBlockEpochNtfn is a synchronous response-streaming RPC that registers an intent for a client to be notified of blocks in the chain. ([source](../../raw/api/api-docs/api/lnd/chain-notifier/register-block-epoch-ntfn.md)) RegisterConfirmationsNtfn is a synchronous response-streaming RPC that registers an intent for a client to be notified once a confirmation request has reached its required number of confirmations. ([source](../../raw/api/api-docs/api/lnd/chain-notifier/register-confirmations-ntfn.md)) RegisterSpendNtfn is likewise a synchronous response-streaming RPC, for a spend request, and its page gives `chainrpc/chainnotifier.proto` as its source. ([source](../../raw/api/api-docs/api/lnd/chain-notifier/register-spend-ntfn.md))

The lnd API overview lists Service *ChainNotifier* (file: `chainrpc/chainnotifier.proto`) among the experimental services, which are subject to change and need a compile-time flag to be active (they are active in the official release binaries). The reference was generated against commit `895118ac4ec59e78b2c14f5b0d31ac6f862434bb`. ([source](../../raw/api/api-docs/api/lnd.md))

The REST endpoints page lists three ChainNotifier RPCs under `/v2/chainnotifier/register/`: RegisterBlockEpochNtfn, RegisterConfirmationsNtfn and RegisterSpendNtfn. ([source](../../raw/api/api-docs/api/lnd/rest-endpoints.md))

See also: [[lnd-chain-kit]], [[lnd-wallet-kit]].

## RegisterConfirmationsNtfn

RegisterConfirmationsNtfn is a synchronous response-streaming RPC that registers an intent for a client to be notified once a confirmation request has reached its required number of confirmations on-chain. A confirmation request must have a valid output script; a transaction ID may also be given. If the transaction ID is not set, a notification is sent once the output script confirms; if it is set, a notification is sent once the output script confirms in the given transaction. ([source](../../raw/api/api-docs/api/lnd/chain-notifier/register-confirmations-ntfn.md))

- gRPC: `rpc RegisterConfirmationsNtfn (ConfRequest) returns (stream ConfEvent);`
- REST: `POST /v2/chainnotifier/register/confirmations`
- Request: `chainrpc.ConfRequest`, fields `txid` (a hash of all zeros requests the notification for the script instead), `script`, `num_confs`, `height_hint` (in most cases the broadcast height) and `include_block`
- Response stream: `chainrpc.ConfEvent`, either `conf` (`ConfDetails`: `raw_tx`, `block_hash`, `block_height`, `tx_index`, `raw_block` only if `include_block` was set) or `reorg`

([source](../../raw/api/api-docs/api/lnd/chain-notifier/register-confirmations-ntfn.md))

## RegisterSpendNtfn

RegisterSpendNtfn is a synchronous response-streaming RPC that registers an intent for a client to be notified once a spend request has been spent by a transaction that has confirmed on-chain. A client can request the notification for a particular outpoint, or for an output script by specifying a zero outpoint. ([source](../../raw/api/api-docs/api/lnd/chain-notifier/register-spend-ntfn.md))

- gRPC: `rpc RegisterSpendNtfn (SpendRequest) returns (stream SpendEvent);`
- REST: `POST /v2/chainnotifier/register/spends`
- Request: `chainrpc.SpendRequest`, fields `outpoint` (`hash`, `index`), `script` and `height_hint`
- Response stream: `chainrpc.SpendEvent`, either `spend` (`SpendDetails`: `spending_outpoint`, `raw_spending_tx`, `spending_tx_hash`, `spending_input_index`, `spending_height`) or `reorg`

A zero or nil outpoint is not supported for Taproot spends, so an outpoint must always be specified when registering a spend notification for a Taproot output. ([source](../../raw/api/api-docs/api/lnd/chain-notifier/register-spend-ntfn.md))

## RegisterBlockEpochNtfn

RegisterBlockEpochNtfn is a synchronous response-streaming RPC that registers an intent for a client to be notified of blocks in the chain. The stream returns a hash and height tuple for each new or stale block, and it is the client's responsibility to determine which it is. A client can also request a historical backlog of blocks from a particular point. ([source](../../raw/api/api-docs/api/lnd/chain-notifier/register-block-epoch-ntfn.md))

- gRPC: `rpc RegisterBlockEpochNtfn (BlockEpoch) returns (stream BlockEpoch);`
- REST: `POST /v2/chainnotifier/register/blocks`
- Request and response stream: `chainrpc.BlockEpoch`, fields `hash` and `height`

([source](../../raw/api/api-docs/api/lnd/chain-notifier/register-block-epoch-ntfn.md))
