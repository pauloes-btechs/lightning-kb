---
title: pool channel-auctioneer service
type: service
sources:
  - raw/api/api-docs/api/pool.md
  - raw/api/api-docs/api/pool/rest-endpoints.md
  - raw/api/api-docs/api/pool/channel-auctioneer/batch-snapshot.md
  - raw/api/api-docs/api/pool/channel-auctioneer/batch-snapshots.md
  - raw/api/api-docs/api/pool/channel-auctioneer/cancel-order.md
  - raw/api/api-docs/api/pool/channel-auctioneer/init-account.md
  - raw/api/api-docs/api/pool/channel-auctioneer/market-info.md
  - raw/api/api-docs/api/pool/channel-auctioneer/modify-account.md
  - raw/api/api-docs/api/pool/channel-auctioneer/node-rating.md
  - raw/api/api-docs/api/pool/channel-auctioneer/order-state.md
  - raw/api/api-docs/api/pool/channel-auctioneer/relevant-batch-snapshot.md
  - raw/api/api-docs/api/pool/channel-auctioneer/reserve-account.md
  - raw/api/api-docs/api/pool/channel-auctioneer/submit-order.md
  - raw/api/api-docs/api/pool/channel-auctioneer/subscribe-batch-auction.md
  - raw/api/api-docs/api/pool/channel-auctioneer/subscribe-sidecar.md
  - raw/api/api-docs/api/pool/channel-auctioneer/terms.md
updated: 2026-11-14
---

# pool channel-auctioneer service

The channel-auctioneer service is a gRPC service in the API reference of [[pool]]. The Pool overview page lists three `*.proto` files from which the gRPC documentation was generated, `auctioneerrpc/auctioneer.proto`, `auctioneerrpc/hashmail.proto` and `poolrpc/trader.proto`, and says the reference was generated automatically against commit `561c94bda9d5816e51205b5a7b15dce66520f39b` of the `lightninglabs/pool` repository. ([source](../../raw/api/api-docs/api/pool.md)) The RPC's "Source:" link on the ReserveAccount page names `auctioneerrpc/auctioneer.proto`. ([source](../../raw/api/api-docs/api/pool/channel-auctioneer/reserve-account.md))

See also: [[pool-trader]], [[pool-hash-mail]].

The reference has 14 RPC pages for this service. None of them carries a prose description of the RPC and none has a REST section; what follows is taken from the gRPC signatures and the field descriptions of the messages. ([source](../../raw/api/api-docs/api/pool/channel-auctioneer/batch-snapshot.md), [source](../../raw/api/api-docs/api/pool/channel-auctioneer/batch-snapshots.md), [source](../../raw/api/api-docs/api/pool/channel-auctioneer/cancel-order.md), [source](../../raw/api/api-docs/api/pool/channel-auctioneer/init-account.md), [source](../../raw/api/api-docs/api/pool/channel-auctioneer/market-info.md), [source](../../raw/api/api-docs/api/pool/channel-auctioneer/modify-account.md), [source](../../raw/api/api-docs/api/pool/channel-auctioneer/node-rating.md), [source](../../raw/api/api-docs/api/pool/channel-auctioneer/order-state.md), [source](../../raw/api/api-docs/api/pool/channel-auctioneer/relevant-batch-snapshot.md), [source](../../raw/api/api-docs/api/pool/channel-auctioneer/reserve-account.md), [source](../../raw/api/api-docs/api/pool/channel-auctioneer/submit-order.md), [source](../../raw/api/api-docs/api/pool/channel-auctioneer/subscribe-batch-auction.md), [source](../../raw/api/api-docs/api/pool/channel-auctioneer/subscribe-sidecar.md), [source](../../raw/api/api-docs/api/pool/channel-auctioneer/terms.md))

The REST Endpoints page for Pool lists no path for these RPCs. ([source](../../raw/api/api-docs/api/pool/rest-endpoints.md))

The RPCs below are grouped by topic:

- Accounts (see [[pool-accounts]]): ReserveAccount, InitAccount, ModifyAccount
- Orders (see [[pool-orders-and-batches]]): SubmitOrder, CancelOrder, OrderState
- Streams: SubscribeBatchAuction, SubscribeSidecar
- Market and batches: Terms, RelevantBatchSnapshot, BatchSnapshot, BatchSnapshots, NodeRating, MarketInfo

## ReserveAccount

No description is given on the page. ([source](../../raw/api/api-docs/api/pool/channel-auctioneer/reserve-account.md))

- gRPC: `rpc ReserveAccount (ReserveAccountRequest) returns (ReserveAccountResponse);`
- REST: none listed on the page
- Request message: `poolrpc.ReserveAccountRequest`
- Response message: `poolrpc.ReserveAccountResponse`

The request fields are `account_value` (the desired value of the account in satoshis), `account_expiry` (the block height at which the account should expire), `trader_key` and `version`, which must be set to 0 for legacy (non-taproot) accounts. The response fields are `auctioneer_key` and `initial_batch_key`. `auctioneer_key` is the base key of the auctioneer; for a version 1, Taproot enabled account, the trader and auctioneer key are combined into a MuSig2 combined key that is static throughout the lifetime of the account. `initial_batch_key` is the initial per-batch key to be used for the account; for every cleared batch that the account participates in, this key is incremented by the base point of its curve. ([source](../../raw/api/api-docs/api/pool/channel-auctioneer/reserve-account.md))

## InitAccount

No description is given on the page. ([source](../../raw/api/api-docs/api/pool/channel-auctioneer/init-account.md))

- gRPC: `rpc InitAccount (ServerInitAccountRequest) returns (ServerInitAccountResponse);`
- REST: none listed on the page
- Request message: `poolrpc.ServerInitAccountRequest`
- Response message: `poolrpc.ServerInitAccountResponse` (no parameters)

The request fields are `account_point`, `account_script`, `account_value`, `account_expiry`, `trader_key`, `user_agent` and `version`. `account_point` is the transaction output of the account; it has to be unspent and be a P2WSH of the account script, and its amount must exactly correspond to `account_value`. `user_agent` identifies the software running on the user's side and *SHOULD* conform to the pattern `Agent-Name/semver-version(/additional-info)` and use less than 256 characters; the examples given are `poold/v0.4.2-beta/commit=3b635821,initiator=pool-cli` and `litd/v0.4.0-alpha/commit=326d754,initiator=lit-ui`. ([source](../../raw/api/api-docs/api/pool/channel-auctioneer/init-account.md))

## ModifyAccount

No description is given on the page. ([source](../../raw/api/api-docs/api/pool/channel-auctioneer/modify-account.md))

- gRPC: `rpc ModifyAccount (ServerModifyAccountRequest) returns (ServerModifyAccountResponse);`
- REST: none listed on the page
- Request message: `poolrpc.ServerModifyAccountRequest`
- Response message: `poolrpc.ServerModifyAccountResponse`

The request fields are `trader_key`, `new_inputs`, `new_outputs`, `new_params`, `trader_nonces` and `prev_outputs`. `new_inputs` can be used to deposit more funds into an account and must be under control of the backing lnd node's wallet; `new_outputs` can be used to withdraw funds from an account. `new_params` is a `NewAccountParameters` with `value`, `expiry` (as an absolute height) and `version`. `prev_outputs` is required when spending a Taproot enabled (account version 1) output or when adding additional Taproot inputs. ([source](../../raw/api/api-docs/api/pool/channel-auctioneer/modify-account.md))

The response fields are `account_sig` and `server_nonces`. `account_sig` is the auctioneer's signature that allows a trader to broadcast a transaction spending from an account output; for version 1 (Taproot enabled) accounts it is a partial MuSig2 signature that the trader daemon combines into a full signature by adding its own partial signature. ([source](../../raw/api/api-docs/api/pool/channel-auctioneer/modify-account.md))

## SubmitOrder

No description is given on the page. ([source](../../raw/api/api-docs/api/pool/channel-auctioneer/submit-order.md))

- gRPC: `rpc SubmitOrder (ServerSubmitOrderRequest) returns (ServerSubmitOrderResponse);`
- REST: none listed on the page
- Request message: `poolrpc.ServerSubmitOrderRequest`
- Response message: `poolrpc.ServerSubmitOrderResponse`

The request fields are `ask` (a `ServerAsk`), `bid` (a `ServerBid`) and `user_agent`. Both order types carry `details` (a `ServerOrder`), `lease_duration_blocks` and `version`. A `ServerAsk` adds `announcement_constraints` and `confirmation_constraints`; a `ServerBid` adds `min_node_tier`, `self_chan_balance`, `is_sidecar_channel`, `unannounced_channel` and `zero_conf_channel`. If `is_sidecar_channel` is set to true, the multi\_sig\_key, node\_pub and node\_addr fields of the order details must correspond to the recipient node's details. ([source](../../raw/api/api-docs/api/pool/channel-auctioneer/submit-order.md))

The `ServerOrder` fields are `trader_key`, `rate_fixed`, `amt`, `min_chan_amt`, `order_nonce`, `order_sig`, `multi_sig_key`, `node_pub`, `node_addr`, `channel_type`, `max_batch_fee_rate_sat_per_kw`, `allowed_node_ids`, `not_allowed_node_ids`, `auction_type` and `is_public`. `order_nonce` is of 32 byte length and acts as unique order identifier. `order_sig` is the signature of the order's digest, signed with the user's account key. The response fields are `invalid_order` (order failed with the given reason) and `accepted`. ([source](../../raw/api/api-docs/api/pool/channel-auctioneer/submit-order.md))

## CancelOrder

No description is given on the page. ([source](../../raw/api/api-docs/api/pool/channel-auctioneer/cancel-order.md))

- gRPC: `rpc CancelOrder (ServerCancelOrderRequest) returns (ServerCancelOrderResponse);`
- REST: none listed on the page
- Request message: `poolrpc.ServerCancelOrderRequest`
- Response message: `poolrpc.ServerCancelOrderResponse` (no parameters)

The only request field is `order_nonce_preimage`, the preimage to the order's unique nonce. ([source](../../raw/api/api-docs/api/pool/channel-auctioneer/cancel-order.md))

## OrderState

No description is given on the page. ([source](../../raw/api/api-docs/api/pool/channel-auctioneer/order-state.md))

- gRPC: `rpc OrderState (ServerOrderStateRequest) returns (ServerOrderStateResponse);`
- REST: none listed on the page
- Request message: `poolrpc.ServerOrderStateRequest`
- Response message: `poolrpc.ServerOrderStateResponse`

The request field is `order_nonce`. The response fields are `state` and `units_unfulfilled`. `state` is an `OrderState`: `ORDER_SUBMITTED`, `ORDER_CLEARED`, `ORDER_PARTIALLY_FILLED`, `ORDER_EXECUTED`, `ORDER_CANCELED`, `ORDER_EXPIRED` or `ORDER_FAILED`. ([source](../../raw/api/api-docs/api/pool/channel-auctioneer/order-state.md))

## SubscribeBatchAuction

No description is given on the page. This is a bidirectional-streaming RPC. ([source](../../raw/api/api-docs/api/pool/channel-auctioneer/subscribe-batch-auction.md))

- gRPC: `rpc SubscribeBatchAuction (stream ClientAuctionMessage) returns (stream ServerAuctionMessage);`
- REST: none listed on the page
- Request message: `poolrpc.ClientAuctionMessage`
- Response message: `poolrpc.ServerAuctionMessage`

The stream starts with a 3-way authentication handshake. Step 1 is the client's `commit` (an `AccountCommitment` with `commit_hash` = `SHA256(accountPubKey || nonce)` and `batch_version`). Step 2 is the server's `challenge` (a `ServerChallenge`). Step 3 is the client's `subscribe` (an `AccountSubscription` with `trader_key`, `commit_nonce` and `auth_sig`), where the signature is over `auth_hash = SHA256(SHA256(accountPubKey || nonce) || challenge)` and is created with the trader's account key. The server answers with `success` or `error`. Clients that don't use the latest `batch_version` will be declined to connect and participate in an auction. ([source](../../raw/api/api-docs/api/pool/channel-auctioneer/subscribe-batch-auction.md))

The other `ClientAuctionMessage` fields are `accept` (an `OrderMatchAccept`: accept the orders to be matched), `reject` (an `OrderMatchReject`: reject a whole batch), `sign` (an `OrderMatchSign`: the channel funding negotiations with the matched peer were successful and the inputs to spend from the accounts are now signed) and `recover` (an `AccountRecovery`: the trader has lost its database and is trying to recover their accounts). `recover` must only be sent if the auctioneer knows of the account, otherwise it will regard it as a critical error and terminate the connection. ([source](../../raw/api/api-docs/api/pool/channel-auctioneer/subscribe-batch-auction.md))

The other `ServerAuctionMessage` fields are `prepare`, `sign`, `finalize` and `account`. `prepare` (an `OrderMatchPrepare`) means the auctioneer has matched a set of orders into a batch and instructs the traders to validate the batch and prepare for order execution; because traders can back out of a batch, multiple of these messages with the same batch\_id can be sent. `sign` (an `OrderMatchSignBegin`) is sent after all traders send back an OrderMatchAccept; it signals that the traders should execute their local funding protocol, then send signatures for their account inputs. `finalize` (an `OrderMatchFinalize`, fields `batch_id` and `batch_txid`) means all traders have accepted and signed the batch and the final transaction was broadcast. `account` (an `AuctionAccount`) is the answer to a trader's request for account recovery. ([source](../../raw/api/api-docs/api/pool/channel-auctioneer/subscribe-batch-auction.md))

`OrderMatchPrepare` has `charged_accounts`, `execution_fee`, `batch_transaction`, `fee_rate_sat_per_kw`, `fee_rebate_sat`, `batch_id`, `batch_version`, `matched_markets` and `batch_height_hint`, plus the deprecated `matched_orders` and `clearing_price_rate`. `OrderMatchReject` has `batch_id`, `reason`, `reason_code` and `rejected_orders`; `reason_code` is `UNKNOWN`, `SERVER_MISBEHAVIOR`, `BATCH_VERSION_MISMATCH` or `PARTIAL_REJECT`, and `rejected_orders` is only considered by the auctioneer if the main reason\_code is set to PARTIAL\_REJECT. The auctioneer will only accept a certain number of partial rejects before a trader's account is removed completely from the current batch, and abusing this functionality can also lead to a ban of the trader. An individual `OrderReject` has the reason code `DUPLICATE_PEER` or `CHANNEL_FUNDING_FAILED`. ([source](../../raw/api/api-docs/api/pool/channel-auctioneer/subscribe-batch-auction.md))

`SubscribeError` has `error`, `error_code`, `trader_key` and `account_reservation`; `error_code` is `UNKNOWN`, `SERVER_SHUTDOWN`, `ACCOUNT_DOES_NOT_EXIST` or `INCOMPLETE_ACCOUNT_RESERVATION`. On `SERVER_SHUTDOWN` traders should close the long-lived stream/connection and try to connect again after some time. `AuctionAccount` has `value`, `expiry`, `trader_key`, `auctioneer_key`, `batch_key`, `state`, `height_hint`, `outpoint`, `latest_tx` and `version`; its `state` is an `AuctionAccountState`: `STATE_PENDING_OPEN`, `STATE_OPEN`, `STATE_EXPIRED`, `STATE_PENDING_UPDATE`, `STATE_CLOSED`, `STATE_PENDING_BATCH` or `STATE_EXPIRED_PENDING_UPDATE`. ([source](../../raw/api/api-docs/api/pool/channel-auctioneer/subscribe-batch-auction.md))

## SubscribeSidecar

No description is given on the page. This is a bidirectional-streaming RPC. ([source](../../raw/api/api-docs/api/pool/channel-auctioneer/subscribe-sidecar.md))

- gRPC: `rpc SubscribeSidecar (stream ClientAuctionMessage) returns (stream ServerAuctionMessage);`
- REST: none listed on the page
- Request message: `poolrpc.ClientAuctionMessage`
- Response message: `poolrpc.ServerAuctionMessage`

The page lists the same `ClientAuctionMessage` and `ServerAuctionMessage` messages, with the same fields, as SubscribeBatchAuction. It does not say how the sidecar stream differs. ([source](../../raw/api/api-docs/api/pool/channel-auctioneer/subscribe-sidecar.md))

See [[sidecar-channels]] for the sidecar flow on the trader side.

## Terms

No description is given on the page. ([source](../../raw/api/api-docs/api/pool/channel-auctioneer/terms.md))

- gRPC: `rpc Terms (TermsRequest) returns (TermsResponse);`
- REST: none listed on the page
- Request message: `poolrpc.TermsRequest` (no parameters)
- Response message: `poolrpc.TermsResponse`

The response fields are `max_account_value` (the maximum account size in satoshis currently allowed by the auctioneer), `execution_fee` (an `ExecutionFee` with `base_fee` and `fee_rate`), `next_batch_conf_target`, `next_batch_fee_rate_sat_per_kw`, `next_batch_clear_timestamp`, `lease_duration_buckets` and `auto_renew_extension_blocks`, plus the deprecated `max_order_duration_blocks` and `lease_durations`. `lease_duration_buckets` maps each lease duration to a `DurationBucketState`: `NO_MARKET`, `MARKET_CLOSED`, `ACCEPTING_ORDERS` or `MARKET_OPEN`. ([source](../../raw/api/api-docs/api/pool/channel-auctioneer/terms.md))

## RelevantBatchSnapshot

No description is given on the page. ([source](../../raw/api/api-docs/api/pool/channel-auctioneer/relevant-batch-snapshot.md))

- gRPC: `rpc RelevantBatchSnapshot (RelevantBatchRequest) returns (RelevantBatch);`
- REST: none listed on the page
- Request message: `poolrpc.RelevantBatchRequest`
- Response message: `poolrpc.RelevantBatch`

The request fields are `id`, the unique identifier of the batch, and `accounts`, the set of accounts the trader is interested in retrieving information for within the batch, each identified by its trader key. The response fields are `version`, `id`, `charged_accounts`, `execution_fee`, `transaction`, `fee_rate_sat_per_kw`, `creation_timestamp_ns` and `matched_markets`, plus the deprecated `matched_orders` and `clearing_price_rate`. Each `AccountDiff` in `charged_accounts` has `ending_balance`, `ending_state`, `outpoint_index`, `trader_key`, `new_expiry` and `new_version`; `ending_state` is `OUTPUT_RECREATED`, `OUTPUT_DUST_EXTENDED_OFFCHAIN`, `OUTPUT_DUST_ADDED_TO_FEES` or `OUTPUT_FULLY_SPENT`. ([source](../../raw/api/api-docs/api/pool/channel-auctioneer/relevant-batch-snapshot.md))

## BatchSnapshot

No description is given on the page. ([source](../../raw/api/api-docs/api/pool/channel-auctioneer/batch-snapshot.md))

- gRPC: `rpc BatchSnapshot (BatchSnapshotRequest) returns (BatchSnapshotResponse);`
- REST: none listed on the page
- Request message: `poolrpc.BatchSnapshotRequest`
- Response message: `poolrpc.BatchSnapshotResponse`

The request field is `batch_id`, the unique identifier of the batch encoded as a compressed pubkey. The response fields are `version`, `batch_id`, `prev_batch_id`, `batch_tx_id`, `batch_tx`, `batch_tx_fee_rate_sat_per_kw`, `creation_timestamp_ns` and `matched_markets`, plus the deprecated `clearing_price_rate` and `matched_orders`. Each `MatchedMarketSnapshot` has `matched_orders` and `clearing_price_rate`, the uniform clearing price rate in parts per billion that was used for this batch. Each `MatchedOrderSnapshot` has `ask`, `bid`, `matching_rate`, `total_sats_cleared` and `units_matched`. ([source](../../raw/api/api-docs/api/pool/channel-auctioneer/batch-snapshot.md))

## BatchSnapshots

No description is given on the page. ([source](../../raw/api/api-docs/api/pool/channel-auctioneer/batch-snapshots.md))

- gRPC: `rpc BatchSnapshots (BatchSnapshotsRequest) returns (BatchSnapshotsResponse);`
- REST: none listed on the page
- Request message: `poolrpc.BatchSnapshotsRequest`
- Response message: `poolrpc.BatchSnapshotsResponse`

The request fields are `start_batch_id` and `num_batches_back`. `start_batch_id` represents the newest/most current batch to fetch; if it is empty or a zero batch ID, the most recent finalized batch is used as the starting point to go back from. `num_batches_back` is the number of batches to return at most, including the start batch. The response field `batches` is a list of `BatchSnapshotResponse` messages. ([source](../../raw/api/api-docs/api/pool/channel-auctioneer/batch-snapshots.md))

## NodeRating

No description is given on the page. ([source](../../raw/api/api-docs/api/pool/channel-auctioneer/node-rating.md))

- gRPC: `rpc NodeRating (ServerNodeRatingRequest) returns (ServerNodeRatingResponse);`
- REST: none listed on the page
- Request message: `poolrpc.ServerNodeRatingRequest`
- Response message: `poolrpc.ServerNodeRatingResponse`

The request field is `node_pubkeys`. The response field `node_ratings` is a list of `NodeRating` messages with `node_pubkey` and `node_tier`. `node_tier` is a `NodeTier`: `TIER_DEFAULT` (0), `TIER_0` (1), whose nodes are considered to have "no rating", or `TIER_1` (2), the "base" node tier and the current default node tier when submitting bid orders. ([source](../../raw/api/api-docs/api/pool/channel-auctioneer/node-rating.md))

## MarketInfo

No description is given on the page. ([source](../../raw/api/api-docs/api/pool/channel-auctioneer/market-info.md))

- gRPC: `rpc MarketInfo (MarketInfoRequest) returns (MarketInfoResponse);`
- REST: none listed on the page
- Request message: `poolrpc.MarketInfoRequest` (no parameters)
- Response message: `poolrpc.MarketInfoResponse`

The response field `markets` is a map of all markets identified by their lease duration and the current set of statistics. Each `MarketInfo` has `num_asks`, `num_bids`, `ask_open_interest_units` and `bid_open_interest_units`, each a list of `TierValue` entries (`tier`, `value`) per node tier. ([source](../../raw/api/api-docs/api/pool/channel-auctioneer/market-info.md))

## Notes

These are editorial observations, not statements from the sources.

- The reference pages do not say who runs this service or how a `poold` reaches it. The message names (`Server...` requests, "the auctioneer" in field descriptions) and the `user_agent` examples suggest it is the auction server's API that the trader daemon calls, with [[pool-trader]] being the local API a user calls.
- Five RPC names exist on both this service and [[pool-trader]]. InitAccount, SubmitOrder and CancelOrder use different request and response messages on the two services. BatchSnapshot and BatchSnapshots use the same messages with the same fields on both (`BatchSnapshotRequest`/`BatchSnapshotResponse` and `BatchSnapshotsRequest`/`BatchSnapshotsResponse`). Check which service a signature belongs to before using it.
- In the `MatchedBid` message the `bid` field is described as "The ask order that was matched against.", the same text as `MatchedAsk.ask`; this looks like a copy-paste in the proto comments.
- The Pool overview page lists an `auctioneerrpc/auctioneer.swagger.json` file, but no REST path for this service appears in the reference.
- See [[pool-channel-leases]] for lease durations and [[pool-zero-conf-channels]] for the `zero_conf_channel` / `ONLY_ZEROCONF` options.
