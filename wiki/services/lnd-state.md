---
title: lnd state service
type: service
sources:
  - raw/api/api-docs/api/lnd.md
  - raw/api/api-docs/api/lnd/rest-endpoints.md
  - raw/api/api-docs/api/lnd/state/get-state.md
  - raw/api/api-docs/api/lnd/state/subscribe-state.md
updated: 2026-11-14
---

# lnd state service (State)

The State service of [[lnd]] reports the wallet state. Its RPC pages give `stateservice.proto` as their source. ([source](../../raw/api/api-docs/api/lnd/state/get-state.md))

The REST endpoints page lists two State RPCs under `/v1/state`: `lnrpc.GetState` and `lnrpc.SubscribeState`. ([source](../../raw/api/api-docs/api/lnd/rest-endpoints.md))

The reference was generated against commit `895118ac4ec59e78b2c14f5b0d31ac6f862434bb`; `stateservice.proto` is not among the services the overview lists as experimental. ([source](../../raw/api/api-docs/api/lnd.md))

See also: [[lnd-wallet-unlocker]], [[running-lnd]].

## Wallet states

Both RPCs return a `state` of enum `lnrpc.WalletState`: `NON_EXISTING` (`0`, wallet not yet initialized), `LOCKED` (`1`, requires a password to unlock), `UNLOCKED` (`2`, unlocked but the RPC server isn't ready), `RPC_ACTIVE` (`3`, lnd server active but not fully ready for calls), `SERVER_ACTIVE` (`4`, ready to accept calls) and `WAITING_TO_START` (`255`, waiting to become the leader in a cluster). ([source](../../raw/api/api-docs/api/lnd/state/get-state.md))

## SubscribeState

SubscribeState subscribes to the state of the wallet. The current wallet state will always be delivered immediately. It is a server-streaming RPC. ([source](../../raw/api/api-docs/api/lnd/state/subscribe-state.md))

- gRPC: `rpc SubscribeState (SubscribeStateRequest) returns (stream SubscribeStateResponse);`
- REST: `GET /v1/state/subscribe`
- Request: `lnrpc.SubscribeStateRequest` (no parameters)
- Response stream: `lnrpc.SubscribeStateResponse`, field `state` (`WalletState`)

([source](../../raw/api/api-docs/api/lnd/state/subscribe-state.md))

## GetState

GetState returns the current wallet state without streaming further changes. ([source](../../raw/api/api-docs/api/lnd/state/get-state.md))

- gRPC: `rpc GetState (GetStateRequest) returns (GetStateResponse);`
- REST: `GET /v1/state`
- Request: `lnrpc.GetStateRequest` (no parameters)
- Response: `lnrpc.GetStateResponse`, field `state` (`WalletState`)

([source](../../raw/api/api-docs/api/lnd/state/get-state.md))
