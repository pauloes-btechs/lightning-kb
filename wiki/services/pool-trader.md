---
title: pool trader service
type: service
sources:
  - raw/api/api-docs/api/pool.md
  - raw/api/api-docs/api/pool/rest-endpoints.md
  - raw/api/api-docs/api/pool/trader/account-modification-fees.md
  - raw/api/api-docs/api/pool/trader/auction-fee.md
  - raw/api/api-docs/api/pool/trader/batch-snapshot.md
  - raw/api/api-docs/api/pool/trader/batch-snapshots.md
  - raw/api/api-docs/api/pool/trader/bump-account-fee.md
  - raw/api/api-docs/api/pool/trader/cancel-order.md
  - raw/api/api-docs/api/pool/trader/cancel-sidecar.md
  - raw/api/api-docs/api/pool/trader/close-account.md
  - raw/api/api-docs/api/pool/trader/decode-sidecar-ticket.md
  - raw/api/api-docs/api/pool/trader/deposit-account.md
  - raw/api/api-docs/api/pool/trader/expect-sidecar-channel.md
  - raw/api/api-docs/api/pool/trader/get-info.md
  - raw/api/api-docs/api/pool/trader/get-lsat-tokens.md
  - raw/api/api-docs/api/pool/trader/init-account.md
  - raw/api/api-docs/api/pool/trader/lease-durations.md
  - raw/api/api-docs/api/pool/trader/leases.md
  - raw/api/api-docs/api/pool/trader/list-accounts.md
  - raw/api/api-docs/api/pool/trader/list-orders.md
  - raw/api/api-docs/api/pool/trader/list-sidecars.md
  - raw/api/api-docs/api/pool/trader/next-batch-info.md
  - raw/api/api-docs/api/pool/trader/node-ratings.md
  - raw/api/api-docs/api/pool/trader/offer-sidecar.md
  - raw/api/api-docs/api/pool/trader/quote-account.md
  - raw/api/api-docs/api/pool/trader/quote-order.md
  - raw/api/api-docs/api/pool/trader/recover-accounts.md
  - raw/api/api-docs/api/pool/trader/register-sidecar.md
  - raw/api/api-docs/api/pool/trader/renew-account.md
  - raw/api/api-docs/api/pool/trader/stop-daemon.md
  - raw/api/api-docs/api/pool/trader/submit-order.md
  - raw/api/api-docs/api/pool/trader/withdraw-account.md
updated: 2026-11-14
---

# pool trader service

The trader service is the gRPC and REST API of a local `poold` instance, the Pool client daemon of [[pool]]. The Pool overview page lists three `*.proto` files from which the gRPC documentation was generated, `auctioneerrpc/auctioneer.proto`, `auctioneerrpc/hashmail.proto` and `poolrpc/trader.proto`, and says the reference was generated automatically against commit `561c94bda9d5816e51205b5a7b15dce66520f39b` of the `lightninglabs/pool` repository. ([source](../../raw/api/api-docs/api/pool.md)) The RPC's "Source:" link on the GetInfo page names `poolrpc/trader.proto`. ([source](../../raw/api/api-docs/api/pool/trader/get-info.md))

See also: [[pool-channel-auctioneer]], [[pool-hash-mail]].

The reference's code samples assume a local `poold` listening for gRPC connections on port `12010` and for REST connections on port `8281`. A request needs a TLS/SSL connection and a macaroon used for RPC authentication. The base directory of `poold` is by default `~/.pool` on Linux and `~/Library/Application Support/Pool` on macOS. ([source](../../raw/api/api-docs/api/pool.md))

For REST, a `byte` field must be set as the base64 encoded string representation of a raw byte array. When such a value is used in a URL path, the base64 string must use the URL and Filename Safe Alphabet: replace `+` with `-`, `/` with `_`, and keep the trailing `=` as is. Url encoding (ie. `%2F`) will not work. ([source](../../raw/api/api-docs/api/pool.md))

The REST Endpoints page lists 26 REST endpoints for Pool, all under `/v1/pool/` and all pointing to RPCs of this service. ([source](../../raw/api/api-docs/api/pool/rest-endpoints.md))

The 30 RPCs below are grouped by topic:

- Daemon: GetInfo, StopDaemon, GetLsatTokens
- Accounts (see [[pool-accounts]]): QuoteAccount, InitAccount, ListAccounts, CloseAccount, WithdrawAccount, DepositAccount, RenewAccount, BumpAccountFee, RecoverAccounts, AccountModificationFees
- Orders (see [[pool-orders-and-batches]]): SubmitOrder, ListOrders, CancelOrder, QuoteOrder
- Market and batches (see [[pool-orders-and-batches]] and [[pool-channel-leases]]): AuctionFee, LeaseDurations, NextBatchInfo, BatchSnapshot, BatchSnapshots, Leases, NodeRatings
- Sidecar channels (see [[sidecar-channels]]): OfferSidecar, RegisterSidecar, ExpectSidecarChannel, DecodeSidecarTicket, ListSidecars, CancelSidecar

## GetInfo

GetInfo returns general information about the state of the Pool trader daemon. ([source](../../raw/api/api-docs/api/pool/trader/get-info.md))

- gRPC: `rpc GetInfo (GetInfoRequest) returns (GetInfoResponse);`
- REST: `GET` `/v1/pool/info`
- Request message: `poolrpc.GetInfoRequest` (no parameters)
- Response message: `poolrpc.GetInfoResponse`

The response fields are `version`, `accounts_total`, `accounts_active`, `accounts_active_expired`, `accounts_archived`, `orders_total`, `orders_active`, `orders_archived`, `current_block_height`, `batches_involved`, `node_rating`, `lsat_tokens`, `subscribed_to_auctioneer`, `new_nodes_only` and `market_info`. `subscribed_to_auctioneer` indicates whether there is an active subscription connection to the auctioneer; it will never be true if there is no active account. `new_nodes_only` indicates whether the global `--newnodesonly` command line flag or `newnodesonly=true` configuration parameter was set on the Pool trader daemon. `market_info` is a map of all markets identified by their lease duration, with `num_asks`, `num_bids`, `ask_open_interest_units` and `bid_open_interest_units` per node tier. ([source](../../raw/api/api-docs/api/pool/trader/get-info.md))

## StopDaemon

Stop gracefully shuts down the Pool trader daemon. ([source](../../raw/api/api-docs/api/pool/trader/stop-daemon.md))

- gRPC: `rpc StopDaemon (StopDaemonRequest) returns (StopDaemonResponse);`
- REST: `POST` `/v1/pool/stop`
- Request message: `poolrpc.StopDaemonRequest`
- Response message: `poolrpc.StopDaemonResponse`

Neither the request nor the response has parameters. ([source](../../raw/api/api-docs/api/pool/trader/stop-daemon.md))

## GetLsatTokens

GetLsatTokens returns all LSAT tokens the daemon ever paid for. ([source](../../raw/api/api-docs/api/pool/trader/get-lsat-tokens.md))

- gRPC: `rpc GetLsatTokens (TokensRequest) returns (TokensResponse);`
- REST: `GET` `/v1/pool/lsat/tokens`
- Request message: `poolrpc.TokensRequest` (no parameters)
- Response message: `poolrpc.TokensResponse`

`tokens` is the list of all tokens the daemon knows of, including old/expired tokens. Each `LsatToken` has `base_macaroon`, `payment_hash`, `payment_preimage`, `amount_paid_msat`, `routing_fee_paid_msat`, `time_created`, `expired` and `storage_name`. If `payment_preimage` is set to all zeros, the payment is still pending and the token is not yet fully valid. ([source](../../raw/api/api-docs/api/pool/trader/get-lsat-tokens.md))

## QuoteAccount

QuoteAccount gets a fee quote to fund an account of the given size with the given confirmation target. If the connected lnd wallet doesn't have enough balance to fund an account of the requested size, an error is returned. ([source](../../raw/api/api-docs/api/pool/trader/quote-account.md))

- gRPC: `rpc QuoteAccount (QuoteAccountRequest) returns (QuoteAccountResponse);`
- REST: `POST` `/v1/pool/accounts/quote`
- Request message: `poolrpc.QuoteAccountRequest`
- Response message: `poolrpc.QuoteAccountResponse`

The request fields are `account_value` and `conf_target`; the response fields are `miner_fee_rate_sat_per_kw` and `miner_fee_total`. ([source](../../raw/api/api-docs/api/pool/trader/quote-account.md))

## InitAccount

InitAccount creates a new account with the requested size and expiration, funding it from the wallet of the connected lnd node. ([source](../../raw/api/api-docs/api/pool/trader/init-account.md))

- gRPC: `rpc InitAccount (InitAccountRequest) returns (Account);`
- REST: `POST` `/v1/pool/accounts`
- Request message: `poolrpc.InitAccountRequest`
- Response message: `poolrpc.Account`

The request fields are `account_value`, `absolute_height`, `relative_height`, `conf_target`, `fee_rate_sat_per_kw`, `initiator` and `version`. `initiator` is an optional identification string that is appended to the user agent string sent to the server. `version` is an `AccountVersion`: `ACCOUNT_VERSION_LND_DEPENDENT` (0), `ACCOUNT_VERSION_LEGACY` (1), `ACCOUNT_VERSION_TAPROOT` (2) or `ACCOUNT_VERSION_TAPROOT_V2` (3). With `ACCOUNT_VERSION_LND_DEPENDENT` the version of lnd decides: a Taproot account is created if lnd >= 0.15.0-beta is detected, a legacy account for earlier versions, and a Taproot v2 account if lnd >= 0.16.0-beta is detected. ([source](../../raw/api/api-docs/api/pool/trader/init-account.md))

The returned `Account` has `trader_key`, `outpoint`, `value`, `available_balance`, `expiration_height`, `state`, `latest_txid` and `version`. `trader_key` is the identifying component of an account: the key used for the trader in the 2-of-2 multi-sig construction of an account with an auctioneer. `state` is an `AccountState`: `PENDING_OPEN`, `PENDING_UPDATE`, `OPEN`, `EXPIRED`, `PENDING_CLOSED`, `CLOSED`, `RECOVERY_FAILED` or `PENDING_BATCH`. ([source](../../raw/api/api-docs/api/pool/trader/init-account.md))

## ListAccounts

ListAccounts returns a list of all accounts known to the trader daemon and their current state. ([source](../../raw/api/api-docs/api/pool/trader/list-accounts.md))

- gRPC: `rpc ListAccounts (ListAccountsRequest) returns (ListAccountsResponse);`
- REST: `GET` `/v1/pool/accounts`
- Request message: `poolrpc.ListAccountsRequest`
- Response message: `poolrpc.ListAccountsResponse`

The request field `active_only` lists only accounts that are still active. The response field `accounts` is a list of `Account` messages. ([source](../../raw/api/api-docs/api/pool/trader/list-accounts.md))

## CloseAccount

CloseAccount closes an account and returns the funds locked in that account to the connected lnd node's wallet. ([source](../../raw/api/api-docs/api/pool/trader/close-account.md))

- gRPC: `rpc CloseAccount (CloseAccountRequest) returns (CloseAccountResponse);`
- REST: `DELETE` `/v1/pool/accounts`
- Request message: `poolrpc.CloseAccountRequest`
- Response message: `poolrpc.CloseAccountResponse`

The request fields are `trader_key`, `output_with_fee` and `outputs`. `output_with_fee` (fields `address`, `conf_target`, `fee_rate_sat_per_kw`) is a single output/address to which the remaining funds are sent at the specified fee; if an address is not specified, the funds are sent to an address the backing lnd node controls. `outputs` should only be used when wanting to create two or more outputs; the fee of the closing transaction is then implicitly defined by the combined value of all outputs. The response field is `close_txid`. ([source](../../raw/api/api-docs/api/pool/trader/close-account.md))

## WithdrawAccount

WithdrawAccount splits off parts of the account balance into the specified outputs while recreating the account with a reduced balance. ([source](../../raw/api/api-docs/api/pool/trader/withdraw-account.md))

- gRPC: `rpc WithdrawAccount (WithdrawAccountRequest) returns (WithdrawAccountResponse);`
- REST: `POST` `/v1/pool/accounts/withdraw`
- Request message: `poolrpc.WithdrawAccountRequest`
- Response message: `poolrpc.WithdrawAccountResponse`

The request fields are `trader_key`, `outputs` (each `Output` has `value_sat` and `address`), `fee_rate_sat_per_kw`, `absolute_expiry`, `relative_expiry` and `new_version`. If `new_version` is set and is a valid version greater than the account's current version, the account is upgraded to that version during the withdrawal. The response fields are `account` and `withdraw_txid`. ([source](../../raw/api/api-docs/api/pool/trader/withdraw-account.md))

## DepositAccount

DepositAccount adds more funds from the connected lnd node's wallet to an account. ([source](../../raw/api/api-docs/api/pool/trader/deposit-account.md))

- gRPC: `rpc DepositAccount (DepositAccountRequest) returns (DepositAccountResponse);`
- REST: `POST` `/v1/pool/accounts/deposit`
- Request message: `poolrpc.DepositAccountRequest`
- Response message: `poolrpc.DepositAccountResponse`

The request fields are `trader_key`, `amount_sat`, `fee_rate_sat_per_kw`, `absolute_expiry`, `relative_expiry` and `new_version`. The response fields are `account` and `deposit_txid`. ([source](../../raw/api/api-docs/api/pool/trader/deposit-account.md))

## RenewAccount

RenewAccount renews the expiration of an account. ([source](../../raw/api/api-docs/api/pool/trader/renew-account.md))

- gRPC: `rpc RenewAccount (RenewAccountRequest) returns (RenewAccountResponse);`
- REST: `POST` `/v1/pool/accounts/renew`
- Request message: `poolrpc.RenewAccountRequest`
- Response message: `poolrpc.RenewAccountResponse`

The request fields are `account_key`, `absolute_expiry`, `relative_expiry`, `fee_rate_sat_per_kw` and `new_version`. The response fields are `account` and `renewal_txid`. ([source](../../raw/api/api-docs/api/pool/trader/renew-account.md))

## BumpAccountFee

BumpAccountFee attempts to bump the fee of an account's transaction through child-pays-for-parent (CPFP). Since the CPFP is performed through the backing lnd node, the account transaction must contain an output under its control for a successful bump. If a CPFP has already been performed for an account, and this RPC is invoked again, then a replacing transaction (RBF) of the child will be broadcast. ([source](../../raw/api/api-docs/api/pool/trader/bump-account-fee.md))

- gRPC: `rpc BumpAccountFee (BumpAccountFeeRequest) returns (BumpAccountFeeResponse);`
- REST: `POST` `/v1/pool/accounts/bump`
- Request message: `poolrpc.BumpAccountFeeRequest`
- Response message: `poolrpc.BumpAccountFeeResponse` (no parameters)

The request fields are `trader_key` and `fee_rate_sat_per_kw`, the new fee rate, in satoshis per kw, to use for the child of the account transaction. ([source](../../raw/api/api-docs/api/pool/trader/bump-account-fee.md))

## RecoverAccounts

RecoverAccounts queries the auction server for this trader daemon's accounts in case we lost our local account database. ([source](../../raw/api/api-docs/api/pool/trader/recover-accounts.md))

- gRPC: `rpc RecoverAccounts (RecoverAccountsRequest) returns (RecoverAccountsResponse);`
- REST: `POST` `/v1/pool/accounts/recover`
- Request message: `poolrpc.RecoverAccountsRequest`
- Response message: `poolrpc.RecoverAccountsResponse`

`full_client` recovers the latest account states without interacting with the Lightning Labs server. The remaining request fields are used during the `full_client` recovery process: `account_target`, `auctioneer_key`, `height_hint`, `bitcoin_host`, `bitcoin_user`, `bitcoin_password`, `bitcoin_httppostmode`, `bitcoin_usetls` and `bitcoin_tlspath`. `auctioneer_key` should be left empty for testnet/mainnet, as its value is already hardcoded in the codebase. The response field is `num_recovered_accounts`. ([source](../../raw/api/api-docs/api/pool/trader/recover-accounts.md))

## AccountModificationFees

AccountModificationFees returns a map from account key to an ordered list of account action modification fees. ([source](../../raw/api/api-docs/api/pool/trader/account-modification-fees.md))

- gRPC: `rpc AccountModificationFees (AccountModificationFeesRequest) returns (AccountModificationFeesResponse);`
- REST: none listed on the page
- Request message: `poolrpc.AccountModificationFeesRequest` (no parameters)
- Response message: `poolrpc.AccountModificationFeesResponse`

The response field `accounts` maps an account key to a `ListOfAccountModificationFees`. Each `AccountModificationFee` has `action`, `txid`, `block_height`, `timestamp`, `output_amount`, `fee_null` and `fee_value`; `fee_null` is true if the fee value has not been set. ([source](../../raw/api/api-docs/api/pool/trader/account-modification-fees.md))

## SubmitOrder

SubmitOrder creates a new ask or bid order and submits for the given account and submits it to the auction server for matching. ([source](../../raw/api/api-docs/api/pool/trader/submit-order.md))

- gRPC: `rpc SubmitOrder (SubmitOrderRequest) returns (SubmitOrderResponse);`
- REST: `POST` `/v1/pool/orders`
- Request message: `poolrpc.SubmitOrderRequest`
- Response message: `poolrpc.SubmitOrderResponse`

The request fields are `ask`, `bid` and `initiator`. Both `Ask` and `Bid` carry `details` (an `Order`, the common fields shared between both order types), `lease_duration_blocks` and `version`. An `Ask` adds `announcement_constraints` (`ANNOUNCEMENT_NO_PREFERENCE`, `ONLY_ANNOUNCED`, `ONLY_UNANNOUNCED`) and `confirmation_constraints` (`CONFIRMATION_NO_PREFERENCE`, `ONLY_CONFIRMED`, `ONLY_ZEROCONF`). A `Bid` adds `min_node_tier`, `self_chan_balance`, `sidecar_ticket`, `unannounced_channel` and `zero_conf_channel`. ([source](../../raw/api/api-docs/api/pool/trader/submit-order.md))

The `Order` fields are `trader_key`, `rate_fixed` (fixed order rate in parts per billion), `amt` (order amount in satoshis), `max_batch_fee_rate_sat_per_kw`, `order_nonce`, `state`, `units`, `units_unfulfilled`, `reserved_value_sat`, `creation_timestamp_ns`, `events`, `min_units_match`, `channel_type`, `allowed_node_ids`, `not_allowed_node_ids`, `auction_type` and `is_public`. `allowed_node_ids` and `not_allowed_node_ids` are incompatible with each other. `auction_type` is `AUCTION_TYPE_BTC_INBOUND_LIQUIDITY` (the default, where the bidder is paying for getting bitcoin inbound liquidity from the asker) or `AUCTION_TYPE_BTC_OUTBOUND_LIQUIDITY` (the bidder is paying the asker to accept a channel from the bidder). ([source](../../raw/api/api-docs/api/pool/trader/submit-order.md))

`min_node_tier` is a `NodeTier`: `TIER_DEFAULT` (0), `TIER_0` (1) or `TIER_1` (2); `TIER_1` is described as the current default node tier when submitting bid orders. `channel_type` is an `OrderChannelType`: `ORDER_CHANNEL_TYPE_UNKNOWN`, `ORDER_CHANNEL_TYPE_PEER_DEPENDENT`, `ORDER_CHANNEL_TYPE_SCRIPT_ENFORCED` or `ORDER_CHANNEL_TYPE_SIMPLE_TAPROOT`. For `self_chan_balance`, the `min_chan_amt` must be set to the full order amount, and for the inbound liquidity market the `self_chan_balance` can be at most the same as the order amount. ([source](../../raw/api/api-docs/api/pool/trader/submit-order.md))

The response fields are `invalid_order` (order failed with the given reason), `accepted_order_nonce` and `updated_sidecar_ticket`, which is set when a bid order was submitted for a sidecar ticket: the ticket is updated with the new state and bid order nonce. ([source](../../raw/api/api-docs/api/pool/trader/submit-order.md))

See [[pool-zero-conf-channels]] for `zero_conf_channel` and [[sidecar-channels]] for `sidecar_ticket`.

## ListOrders

ListOrders returns a list of all active and archived orders that are currently known to the trader daemon. ([source](../../raw/api/api-docs/api/pool/trader/list-orders.md))

- gRPC: `rpc ListOrders (ListOrdersRequest) returns (ListOrdersResponse);`
- REST: `GET` `/v1/pool/orders`
- Request message: `poolrpc.ListOrdersRequest`
- Response message: `poolrpc.ListOrdersResponse`

The request fields are `verbose`, which lists the orders including all events, and `active_only`. The response fields are `asks` and `bids`. An order's `state` is an `OrderState`: `ORDER_SUBMITTED`, `ORDER_CLEARED`, `ORDER_PARTIALLY_FILLED`, `ORDER_EXECUTED`, `ORDER_CANCELED`, `ORDER_EXPIRED` or `ORDER_FAILED`. Each `OrderEvent` has `timestamp_ns`, `event_str`, `state_change` and `matched`; a `MatchEvent` has a `match_state` of `PREPARE`, `ACCEPTED`, `REJECTED`, `SIGNED` or `FINALIZED`, and a `reject_reason` that is only set if `match_state` is set to REJECTED. ([source](../../raw/api/api-docs/api/pool/trader/list-orders.md))

## CancelOrder

CancelOrder cancels an active order with the auction server to remove it from future matching. ([source](../../raw/api/api-docs/api/pool/trader/cancel-order.md))

- gRPC: `rpc CancelOrder (CancelOrderRequest) returns (CancelOrderResponse);`
- REST: `DELETE` `/v1/pool/orders/{order_nonce}`
- Request message: `poolrpc.CancelOrderRequest`
- Response message: `poolrpc.CancelOrderResponse` (no parameters)

The only request field is `order_nonce`, placed in the REST path. ([source](../../raw/api/api-docs/api/pool/trader/cancel-order.md))

## QuoteOrder

QuoteOrder calculates the premium, execution fees and max batch fee rate for an order based on the given order parameters. ([source](../../raw/api/api-docs/api/pool/trader/quote-order.md))

- gRPC: `rpc QuoteOrder (QuoteOrderRequest) returns (QuoteOrderResponse);`
- REST: `POST` `/v1/pool/orders/quote`
- Request message: `poolrpc.QuoteOrderRequest`
- Response message: `poolrpc.QuoteOrderResponse`

The request fields are `amt`, `rate_fixed`, `lease_duration_blocks`, `max_batch_fee_rate_sat_per_kw` and `min_units_match`. The response fields are `total_premium_sat`, `rate_per_block`, `rate_percent`, `total_execution_fee_sat` and `worst_case_chain_fee_sat`. `total_premium_sat` is the interest amount paid to the maker by the taker excluding any execution or chain fees. `worst_case_chain_fee_sat` assumes chain fees for the chain footprint of opening amt/min\_units\_match channels at the `max_batch_fee_rate_sat_per_kw` value of the request. ([source](../../raw/api/api-docs/api/pool/trader/quote-order.md))

## AuctionFee

AuctionFee returns the current auction order execution fee specified by the auction server. ([source](../../raw/api/api-docs/api/pool/trader/auction-fee.md))

- gRPC: `rpc AuctionFee (AuctionFeeRequest) returns (AuctionFeeResponse);`
- REST: `GET` `/v1/pool/fee`
- Request message: `poolrpc.AuctionFeeRequest` (no parameters)
- Response message: `poolrpc.AuctionFeeResponse`

The response field `execution_fee` is an `ExecutionFee` with `base_fee`, the base fee in satoshis charged per order regardless of the matched size, and `fee_rate`, the fee rate in parts per million. ([source](../../raw/api/api-docs/api/pool/trader/auction-fee.md))

## LeaseDurations

LeaseDurations returns the current set of valid lease duration in the market as is, and also information w.r.t if the market is currently active. ([source](../../raw/api/api-docs/api/pool/trader/lease-durations.md))

- gRPC: `rpc LeaseDurations (LeaseDurationRequest) returns (LeaseDurationResponse);`
- REST: `GET` `/v1/pool/lease_durations`
- Request message: `poolrpc.LeaseDurationRequest` (no parameters)
- Response message: `poolrpc.LeaseDurationResponse`

The response fields are `lease_durations` (deprecated, use `lease_duration_buckets`) and `lease_duration_buckets`, which maps each lease duration to a `DurationBucketState`: `NO_MARKET`, `MARKET_CLOSED`, `ACCEPTING_ORDERS` (accepting orders for this bucket, but not yet clearing for this duration) or `MARKET_OPEN` (accepting orders, and fully clearing the market for this duration). ([source](../../raw/api/api-docs/api/pool/trader/lease-durations.md))

## NextBatchInfo

NextBatchInfo returns information about the next batch the auctioneer will perform. ([source](../../raw/api/api-docs/api/pool/trader/next-batch-info.md))

- gRPC: `rpc NextBatchInfo (NextBatchInfoRequest) returns (NextBatchInfoResponse);`
- REST: `GET` `/v1/pool/batch/next`
- Request message: `poolrpc.NextBatchInfoRequest` (no parameters)
- Response message: `poolrpc.NextBatchInfoResponse`

The response fields are `conf_target`, `fee_rate_sat_per_kw`, `clear_timestamp` (the absolute unix timestamp in seconds at which the auctioneer will attempt to clear the next batch) and `auto_renew_extension_blocks` (the value used by the auctioneer to determine if an account expiry height needs to be extended after participating in a batch and for how long). ([source](../../raw/api/api-docs/api/pool/trader/next-batch-info.md))

## BatchSnapshot

This RPC is deprecated and will be removed in a future version. BatchSnapshot returns the snapshot of a past batch identified by its ID. If no ID is provided, the snapshot of the last finalized batch is returned. Deprecated, use BatchSnapshots instead. ([source](../../raw/api/api-docs/api/pool/trader/batch-snapshot.md))

- gRPC: `rpc BatchSnapshot (BatchSnapshotRequest) returns (BatchSnapshotResponse);`
- REST: `GET` `/v1/pool/batch/snapshot`
- Request message: `poolrpc.BatchSnapshotRequest`
- Response message: `poolrpc.BatchSnapshotResponse`

The request field is `batch_id`, the unique identifier of the batch encoded as a compressed pubkey. The response fields are `version`, `batch_id`, `prev_batch_id`, `clearing_price_rate` (deprecated), `matched_orders` (deprecated), `batch_tx_id`, `batch_tx`, `batch_tx_fee_rate_sat_per_kw`, `creation_timestamp_ns` and `matched_markets`, which maps the distinct lease duration markets to the orders that were matched within and the discovered market clearing price. ([source](../../raw/api/api-docs/api/pool/trader/batch-snapshot.md))

## BatchSnapshots

BatchSnapshots returns a list of batch snapshots starting at the start batch ID and going back through the history of batches, returning at most the number of specified batches. A maximum of 100 snapshots can be queried in one call. If no start batch ID is provided, the most recent finalized batch is used as the starting point to go back from. ([source](../../raw/api/api-docs/api/pool/trader/batch-snapshots.md))

- gRPC: `rpc BatchSnapshots (BatchSnapshotsRequest) returns (BatchSnapshotsResponse);`
- REST: `GET` `/v1/pool/batch/snapshots`
- Request message: `poolrpc.BatchSnapshotsRequest`
- Response message: `poolrpc.BatchSnapshotsResponse`

The request fields are `start_batch_id` and `num_batches_back`, the number of batches to return at most, including the start batch. The response field `batches` is a list of `BatchSnapshotResponse` messages. ([source](../../raw/api/api-docs/api/pool/trader/batch-snapshots.md))

## Leases

Leases returns the list of channels that were either purchased or sold by the trader within the auction. ([source](../../raw/api/api-docs/api/pool/trader/leases.md))

- gRPC: `rpc Leases (LeasesRequest) returns (LeasesResponse);`
- REST: `GET` `/v1/pool/leases`
- Request message: `poolrpc.LeasesRequest`
- Response message: `poolrpc.LeasesResponse`

The optional request fields `batch_ids` and `accounts` filter the result; if empty, leases throughout all batches and for all accounts are returned. The response fields are `leases`, `total_amt_earned_sat` and `total_amt_paid_sat`. Each `Lease` has `channel_point`, `channel_amt_sat`, `channel_duration_blocks`, `channel_lease_expiry`, `premium_sat`, `execution_fee_sat`, `chain_fee_sat`, `clearing_rate_price`, `order_fixed_rate`, `order_nonce`, `matched_order_nonce`, `purchased`, `channel_remote_node_key`, `channel_node_tier`, `self_chan_balance` and `sidecar_channel`. ([source](../../raw/api/api-docs/api/pool/trader/leases.md))

## NodeRatings

Returns the Node Tier information for this target Lightning node, and other related ranking information. ([source](../../raw/api/api-docs/api/pool/trader/node-ratings.md))

- gRPC: `rpc NodeRatings (NodeRatingRequest) returns (NodeRatingResponse);`
- REST: `GET` `/v1/pool/node_ratings`
- Request message: `poolrpc.NodeRatingRequest`
- Response message: `poolrpc.NodeRatingResponse`

The request field is `node_pubkeys`. The response field `node_ratings` is a list of `NodeRating` messages, each with `node_pubkey` and `node_tier`. ([source](../../raw/api/api-docs/api/pool/trader/node-ratings.md))

## OfferSidecar

OfferSidecar is step 1/4 of the sidecar negotiation between the provider (the trader submitting the bid order) and the recipient (the trader receiving the sidecar channel). This step must be run by the provider. The result is a sidecar ticket with an offer to lease a sidecar channel for the recipient. The offer will be signed with the provider's lnd node public key. The ticket returned by this call will have the state "offered". ([source](../../raw/api/api-docs/api/pool/trader/offer-sidecar.md))

- gRPC: `rpc OfferSidecar (OfferSidecarRequest) returns (SidecarTicket);`
- REST: `POST` `/v1/pool/sidecar/offer`
- Request message: `poolrpc.OfferSidecarRequest`
- Response message: `poolrpc.SidecarTicket`

The request fields are `auto_negotiate` and `bid`. If `auto_negotiate` is false, only the trader\_key, unit, self\_chan\_balance, and lease\_duration\_blocks need to be set in the bid; otherwise, the fields as they're set when submitting a bid need to be filled in. The response field `ticket` is the complete sidecar ticket in its string encoded form, which is base58 encoded, has a human readable prefix ('sidecar...') and a checksum built in. The string encoded version is only used on the trader side of the API; all requests to the auctioneer expect the ticket in its raw, tlv encoded byte form. ([source](../../raw/api/api-docs/api/pool/trader/offer-sidecar.md))

## RegisterSidecar

RegisterSidecarRequest is step 2/4 of the sidecar negotiation between the provider (the trader submitting the bid order) and the recipient (the trader receiving the sidecar channel). This step must be run by the recipient. The result is a sidecar ticket with the recipient's node information and channel funding multisig pubkey filled in. The ticket returned by this call will have the state "registered". ([source](../../raw/api/api-docs/api/pool/trader/register-sidecar.md))

- gRPC: `rpc RegisterSidecar (RegisterSidecarRequest) returns (SidecarTicket);`
- REST: `POST` `/v1/pool/sidecar/register`
- Request message: `poolrpc.RegisterSidecarRequest`
- Response message: `poolrpc.SidecarTicket`

The request fields are `ticket`, which must be in the state "offered", and `auto_negotiate`. If `auto_negotiate` is True, the daemon will attempt to finish negotiating the details of the sidecar channel automatically in the background, and this method will block until the sidecar negotiation either finishes or breaks down. The field description says the progress of the ticket can be monitored using the SidecarState RPC. ([source](../../raw/api/api-docs/api/pool/trader/register-sidecar.md))

## ExpectSidecarChannel

ExpectSidecarChannel is step 4/4 of the sidecar negotiation between the provider (the trader submitting the bid order) and the recipient (the trader receiving the sidecar channel). This step must be run by the recipient once the provider has submitted the bid order for the sidecar channel. From this point onwards the Pool trader daemon of both the provider as well as the recipient need to be online to receive and react to match making events from the server. ([source](../../raw/api/api-docs/api/pool/trader/expect-sidecar-channel.md))

- gRPC: `rpc ExpectSidecarChannel (ExpectSidecarChannelRequest) returns (ExpectSidecarChannelResponse);`
- REST: `POST` `/v1/pool/sidecar/expect`
- Request message: `poolrpc.ExpectSidecarChannelRequest`
- Response message: `poolrpc.ExpectSidecarChannelResponse` (no parameters)

The request field `ticket` is the sidecar ticket to expect an incoming channel for; the ticket must be in the state "ordered". ([source](../../raw/api/api-docs/api/pool/trader/expect-sidecar-channel.md))

## DecodeSidecarTicket

Decodes the base58 encoded sidecar ticket into its individual data fields for a more human-readable representation. ([source](../../raw/api/api-docs/api/pool/trader/decode-sidecar-ticket.md))

- gRPC: `rpc DecodeSidecarTicket (SidecarTicket) returns (DecodedSidecarTicket);`
- REST: none listed on the page
- Request message: `poolrpc.SidecarTicket`
- Response message: `poolrpc.DecodedSidecarTicket`

The response fields are `id`, `version`, `state`, `offer_capacity`, `offer_push_amount`, `offer_lease_duration_blocks`, `offer_sign_pubkey`, `offer_signature`, `offer_auto`, `recipient_node_pubkey`, `recipient_multisig_pubkey`, `recipient_multisig_pubkey_index`, `order_bid_nonce`, `order_signature`, `execution_pending_channel_id`, `encoded_ticket`, `offer_unannounced_channel` and `offer_zero_conf_channel`. ([source](../../raw/api/api-docs/api/pool/trader/decode-sidecar-ticket.md))

## ListSidecars

ListSidecars lists all sidecar tickets currently in the local database. This includes tickets offered by our node as well as tickets that our node is the recipient of. Optionally a ticket ID can be provided to filter the tickets. ([source](../../raw/api/api-docs/api/pool/trader/list-sidecars.md))

- gRPC: `rpc ListSidecars (ListSidecarsRequest) returns (ListSidecarsResponse);`
- REST: none listed on the page
- Request message: `poolrpc.ListSidecarsRequest`
- Response message: `poolrpc.ListSidecarsResponse`

The optional request field `sidecar_id` filters by ticket ID. Because the ID is just 8 bytes and is randomly generated, there could be multiple tickets with the same ID but different offer public keys, which is why those keys should be checked as well. The response field `tickets` is a list of `DecodedSidecarTicket` messages. ([source](../../raw/api/api-docs/api/pool/trader/list-sidecars.md))

## CancelSidecar

CancelSidecar cancels the execution of a specific sidecar ticket. Depending on the state of the sidecar ticket its associated bid order might be canceled as well (if this ticket was offered by our node). ([source](../../raw/api/api-docs/api/pool/trader/cancel-sidecar.md))

- gRPC: `rpc CancelSidecar (CancelSidecarRequest) returns (CancelSidecarResponse);`
- REST: none listed on the page
- Request message: `poolrpc.CancelSidecarRequest`
- Response message: `poolrpc.CancelSidecarResponse` (no parameters)

The only request field is `sidecar_id`. ([source](../../raw/api/api-docs/api/pool/trader/cancel-sidecar.md))

## Notes

These are editorial observations, not statements from the sources.

- The four RPCs with no REST section on their own page (AccountModificationFees, DecodeSidecarTicket, ListSidecars, CancelSidecar) are also the four that are absent from the REST Endpoints listing, so the two sources agree: 26 of 30 RPCs have a REST path.
- The sidecar RPC pages describe steps 1/4, 2/4 and 4/4. No RPC page is labelled step 3/4; the step 4/4 text places it after "the provider has submitted the bid order", and SubmitOrder returns `updated_sidecar_ticket`.
- The RegisterSidecar page refers to a "SidecarState RPC". No RPC of that name exists in the trader, channel-auctioneer or hash-mail reference pages.
- The description on the RegisterSidecar page begins with the message name "RegisterSidecarRequest" rather than the RPC name; it is copied here as written.
- On the trader BatchSnapshot and BatchSnapshots pages, the message "Source:" links are labelled `auctioneerrpc/auctioneer.proto` but point at `poolrpc/trader.proto`. The same RPC names also exist on [[pool-channel-auctioneer]].
