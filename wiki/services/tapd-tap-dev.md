---
title: taproot-assets tap-dev service
type: service
sources:
  - raw/api/api-docs/api/taproot-assets.md
  - raw/api/api-docs/api/taproot-assets/rest-endpoints.md
  - raw/api/api-docs/api/taproot-assets/tap-dev/import-proof.md
  - raw/api/api-docs/api/taproot-assets/tap-dev/subscribe-send-asset-event-ntfns.md
  - raw/api/api-docs/api/taproot-assets/tap-dev/subscribe-receive-asset-event-ntfns.md
updated: 2026-11-14
---

# taproot-assets tap-dev service

The tap-dev service is a gRPC service in the API reference of [[taproot-assets]]. The Taproot Assets overview page lists `tapdevrpc/tapdev.proto` among the `*.proto` files from which the gRPC documentation was generated, and says the reference was generated automatically against commit `14aa3fd90e6aace4d3b2cfc72a51d15ce4afd891` of the `lightninglabs/taproot-assets` repository. ([source](../../raw/api/api-docs/api/taproot-assets.md)) The "Source:" link on each RPC page of this service names `tapdevrpc/tapdev.proto`, and the request message on each page carries the `tapdevrpc.` prefix. ([source](../../raw/api/api-docs/api/taproot-assets/tap-dev/import-proof.md), [source](../../raw/api/api-docs/api/taproot-assets/tap-dev/subscribe-send-asset-event-ntfns.md), [source](../../raw/api/api-docs/api/taproot-assets/tap-dev/subscribe-receive-asset-event-ntfns.md))

The reference has three RPCs for this service: ImportProof, SubscribeSendAssetEventNtfns, SubscribeReceiveAssetEventNtfns. ([source](../../raw/api/api-docs/api/taproot-assets/tap-dev/import-proof.md), [source](../../raw/api/api-docs/api/taproot-assets/tap-dev/subscribe-send-asset-event-ntfns.md), [source](../../raw/api/api-docs/api/taproot-assets/tap-dev/subscribe-receive-asset-event-ntfns.md))

None of these RPC pages has a REST section. ([source](../../raw/api/api-docs/api/taproot-assets/tap-dev/import-proof.md), [source](../../raw/api/api-docs/api/taproot-assets/tap-dev/subscribe-send-asset-event-ntfns.md), [source](../../raw/api/api-docs/api/taproot-assets/tap-dev/subscribe-receive-asset-event-ntfns.md))

The REST Endpoints page for Taproot Assets lists no path for a `tapdevrpc.` RPC. ([source](../../raw/api/api-docs/api/taproot-assets/rest-endpoints.md))

See also: [[tapd-taproot-assets]], [[tapd-asset-wallet]], [[tapd-universe]].

## ImportProof

The page marks this RPC as deprecated and says it will be removed in a future version: "Deprecated, use the new taprpc.RegisterTransfer RPC instead!" ImportProof attempts to import a proof file into the daemon. If successful, a new asset will be inserted on disk, spendable using the specified target script key, and internal key. The page notes that this RPC will be removed with the next major release. ([source](../../raw/api/api-docs/api/taproot-assets/tap-dev/import-proof.md))

- gRPC: `rpc ImportProof (ImportProofRequest) returns (ImportProofResponse);`
- REST: none listed on the page
- Request message: `tapdevrpc.ImportProofRequest`
- Response message: `tapdevrpc.ImportProofResponse`

The request fields are `proof_file` and `genesis_point`; the page gives no description for either. The response has no parameters. ([source](../../raw/api/api-docs/api/taproot-assets/tap-dev/import-proof.md))

## SubscribeSendAssetEventNtfns

SubscribeSendAssetEventNtfns registers a subscription to the event notification stream which relates to the asset sending process. The page marks it as a server-streaming RPC. ([source](../../raw/api/api-docs/api/taproot-assets/tap-dev/subscribe-send-asset-event-ntfns.md))

- gRPC: `rpc SubscribeSendAssetEventNtfns (SubscribeSendAssetEventNtfnsRequest) returns (stream SendAssetEvent);`
- REST: none listed on the page
- Request message: `tapdevrpc.SubscribeSendAssetEventNtfnsRequest`
- Response message: `tapdevrpc.SendAssetEvent`

The request has no parameters. `SendAssetEvent` has `execute_send_state_event` (an event which indicates that a send state is about to be executed) and `proof_transfer_backoff_wait_event` (an event which indicates that the proof transfer backoff wait period will start imminently). `ExecuteSendStateEvent` has `timestamp` and `send_state`; `ProofTransferBackoffWaitEvent` has `timestamp`, `backoff`, `tries_counter` and `transfer_type`, whose values are `PROOF_TRANSFER_TYPE_SEND` and `PROOF_TRANSFER_TYPE_RECEIVE`. ([source](../../raw/api/api-docs/api/taproot-assets/tap-dev/subscribe-send-asset-event-ntfns.md))

## SubscribeReceiveAssetEventNtfns

SubscribeReceiveAssetEventNtfns registers a subscription to the event notification stream which relates to the asset receive process. The page marks it as a server-streaming RPC. ([source](../../raw/api/api-docs/api/taproot-assets/tap-dev/subscribe-receive-asset-event-ntfns.md))

- gRPC: `rpc SubscribeReceiveAssetEventNtfns (SubscribeReceiveAssetEventNtfnsRequest) returns (stream ReceiveAssetEvent);`
- REST: none listed on the page
- Request message: `tapdevrpc.SubscribeReceiveAssetEventNtfnsRequest`
- Response message: `tapdevrpc.ReceiveAssetEvent`

The request has no parameters. `ReceiveAssetEvent` has `proof_transfer_backoff_wait_event` (an event which indicates that the proof transfer backoff wait period will start imminently) and `asset_receive_complete_event` (an event which indicates that an asset receive process has finished). `AssetReceiveCompleteEvent` has `timestamp`, `address` (the address that received the asset, a `taprpc.Addr`) and `outpoint` (the outpoint of the transaction that was used to receive the asset). ([source](../../raw/api/api-docs/api/taproot-assets/tap-dev/subscribe-receive-asset-event-ntfns.md))
