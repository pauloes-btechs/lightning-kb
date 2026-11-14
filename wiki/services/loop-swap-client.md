---
title: loop swap-client service
type: service
sources:
  - raw/api/api-docs/api/loop.md
  - raw/api/api-docs/api/loop/rest-endpoints.md
  - raw/api/api-docs/api/loop/debug/force-auto-loop.md
  - raw/api/api-docs/api/loop/swap-client/loop-out.md
  - raw/api/api-docs/api/loop/swap-client/loop-in.md
  - raw/api/api-docs/api/loop/swap-client/monitor.md
  - raw/api/api-docs/api/loop/swap-client/list-swaps.md
  - raw/api/api-docs/api/loop/swap-client/swap-info.md
  - raw/api/api-docs/api/loop/swap-client/abandon-swap.md
  - raw/api/api-docs/api/loop/swap-client/sweep-htlc.md
  - raw/api/api-docs/api/loop/swap-client/loop-out-terms.md
  - raw/api/api-docs/api/loop/swap-client/loop-out-quote.md
  - raw/api/api-docs/api/loop/swap-client/get-loop-in-terms.md
  - raw/api/api-docs/api/loop/swap-client/get-loop-in-quote.md
  - raw/api/api-docs/api/loop/swap-client/probe.md
  - raw/api/api-docs/api/loop/swap-client/get-l402-tokens.md
  - raw/api/api-docs/api/loop/swap-client/get-lsat-tokens.md
  - raw/api/api-docs/api/loop/swap-client/fetch-l402-token.md
  - raw/api/api-docs/api/loop/swap-client/get-info.md
  - raw/api/api-docs/api/loop/swap-client/stop-daemon.md
  - raw/api/api-docs/api/loop/swap-client/get-liquidity-params.md
  - raw/api/api-docs/api/loop/swap-client/set-liquidity-params.md
  - raw/api/api-docs/api/loop/swap-client/suggest-swaps.md
  - raw/api/api-docs/api/loop/swap-client/list-reservations.md
  - raw/api/api-docs/api/loop/swap-client/instant-out.md
  - raw/api/api-docs/api/loop/swap-client/instant-out-quote.md
  - raw/api/api-docs/api/loop/swap-client/list-instant-outs.md
  - raw/api/api-docs/api/loop/swap-client/new-static-address.md
  - raw/api/api-docs/api/loop/swap-client/list-unspent-deposits.md
  - raw/api/api-docs/api/loop/swap-client/withdraw-deposits.md
  - raw/api/api-docs/api/loop/swap-client/list-static-address-deposits.md
  - raw/api/api-docs/api/loop/swap-client/list-static-address-withdrawals.md
  - raw/api/api-docs/api/loop/swap-client/list-static-address-swaps.md
  - raw/api/api-docs/api/loop/swap-client/get-static-address-summary.md
  - raw/api/api-docs/api/loop/swap-client/static-address-loop-in.md
  - raw/api/api-docs/api/loop/swap-client/static-open-channel.md
updated: 2026-11-14
---

# loop swap-client service (SwapClient)

The swap-client service is a gRPC service in the API reference for [[loop]], which documents communicating with a local `loopd` instance through gRPC. ([source](../../raw/api/api-docs/api/loop.md)) Its RPC pages give `looprpc/client.proto` as their source, for example LoopOut. ([source](../../raw/api/api-docs/api/loop/swap-client/loop-out.md)) ForceAutoLoop, the RPC of [[loop-debug]], gives `looprpc/debug.proto` as its source. ([source](../../raw/api/api-docs/api/loop/debug/force-auto-loop.md))

Version: the reference was generated automatically against commit `9158aed2a8347d78585faa2e7a89a08f66692a09` of the `lightninglabs/loop` repository, and every "Source:" link on the RPC pages points at that commit. ([source](../../raw/api/api-docs/api/loop.md))

Connecting: the reference's code samples assume a local `loopd` instance listening for gRPC connections on port `11010` and for REST connections on port `8081`. A request needs a TLS/SSL connection and a macaroon used for RPC authentication. The base directory of `loopd` is by default `~/.loop` on Linux and `~/Library/Application Support/Loop` on macOS. ([source](../../raw/api/api-docs/api/loop.md))

REST encoding: a `byte` field must be set as the base64 encoded string representation of a raw byte array, and when it is used in a URL path the base64 string must use the URL and Filename Safe Alphabet (replace `+` with `-`, `/` with `_`, keep the trailing `=`); URL encoding such as `%2F` will not work. ([source](../../raw/api/api-docs/api/loop.md))

The REST endpoints page lists 28 REST paths for Loop, all of them for RPCs of this service; each path is repeated in the RPC sections below. ([source](../../raw/api/api-docs/api/loop/rest-endpoints.md))

Related guides: [[using-loop]] for the CLI, [[autoloop]] for the liquidity manager RPCs, [[instant-loop-outs]] for reservations and instant outs, [[static-loop-in-addresses]] for the static address RPCs. Background: [[submarine-swaps]], [[l402]], [[macaroons]].

## Swaps

### LoopOut

LoopOut initiates an loop out swap with the given parameters. The call returns after the swap has been set up with the swap server. From that point onwards, progress can be tracked via the SwapStatus stream that is returned from Monitor(). ([source](../../raw/api/api-docs/api/loop/swap-client/loop-out.md))

- gRPC: `rpc LoopOut (LoopOutRequest) returns (SwapResponse);`
- REST: `POST` `/v1/loop/out`
- Request message: `looprpc.LoopOutRequest`
- Response message: `looprpc.SwapResponse`

Request fields that matter: `amt` is the requested swap amount in sat and does not include the swap and miner fee; `dest` is the Base58 encoded destination address for the swap; the fee limits are `max_swap_routing_fee`, `max_prepay_routing_fee`, `max_swap_fee`, `max_prepay_amt` and `max_miner_fee`; `outgoing_chan_set` restricts the channels that may be used and replaces the deprecated `loop_out_channel`; `sweep_conf_target` is the number of blocks from the on-chain HTLC's confirmation height that it should be swept within; `swap_publication_deadline` is the latest time (in unix seconds) the server may wait before publishing the HTLC, which gives it the opportunity to batch swaps; `label` is limited to 500 characters and may not start with the prefix [reserved]; `account` and `account_addr_type` name an lnd account as an alternative destination address source; `reservation_ids` makes loop try the instant out flow, and the swap amount must then equal the sum of the reservation amounts; `asset_info` and `asset_rfq_info` are for swaps paid in an asset. The response carries `id_bytes` (the string `id` is deprecated), `htlc_address_p2wsh`, `htlc_address_p2tr` (the deprecated `htlc_address` is also present) and `server_message`. ([source](../../raw/api/api-docs/api/loop/swap-client/loop-out.md))

### LoopIn

LoopIn initiates a loop in swap with the given parameters. The call returns after the swap has been set up with the swap server. From that point onwards, progress can be tracked via the SwapStatus stream that is returned from Monitor(). ([source](../../raw/api/api-docs/api/loop/swap-client/loop-in.md))

- gRPC: `rpc LoopIn (LoopInRequest) returns (SwapResponse);`
- REST: `POST` `/v1/loop/in`
- Request message: `looprpc.LoopInRequest`
- Response message: `looprpc.SwapResponse`

Request fields that matter: `amt` (sat, excluding the swap and miner fee), `max_swap_fee`, `max_miner_fee`, `last_hop` (if empty, the last hop is selected based on the lowest routing fee for the swap payment from the server), `external_htlc` (if true, the htlc is expected to be published by an external actor), `htlc_conf_target`, `label` (limited to 500 characters), `initiator`, `route_hints` and `private`. The response is the same `looprpc.SwapResponse` as for LoopOut. ([source](../../raw/api/api-docs/api/loop/swap-client/loop-in.md))

### Monitor

Monitor will return a stream of swap updates for currently active swaps. ([source](../../raw/api/api-docs/api/loop/swap-client/monitor.md))

- gRPC: `rpc Monitor (MonitorRequest) returns (stream SwapStatus);`
- REST: none listed on the page
- Request message: `looprpc.MonitorRequest`
- Response message: `looprpc.SwapStatus` (stream)

The page marks this as a server-streaming RPC and lists no REST path. `MonitorRequest` has no parameters. Each `SwapStatus` carries `amt`, `id_bytes` (the string `id` is deprecated), `type` (`SwapType`: `LOOP_OUT`, `LOOP_IN`, `STATIC_LOOP_IN`), `state` (`SwapState`: `INITIATED`, `PREIMAGE_REVEALED`, `HTLC_PUBLISHED`, `SUCCESS`, `FAILED`, `INVOICE_SETTLED`), `static_loop_in_state`, `failure_reason` (`FailureReason`, only set if the swap has failed), `initiation_time`, `last_update_time`, `htlc_address_p2wsh`, `htlc_address_p2tr`, `cost_server`, `cost_onchain`, `cost_offchain`, `last_hop`, `outgoing_chan_set`, `label` and `asset_info`. ([source](../../raw/api/api-docs/api/loop/swap-client/monitor.md))

### ListSwaps

ListSwaps returns a list of all currently known swaps and their current status. ([source](../../raw/api/api-docs/api/loop/swap-client/list-swaps.md))

- gRPC: `rpc ListSwaps (ListSwapsRequest) returns (ListSwapsResponse);`
- REST: `GET` `/v1/loop/swaps`
- Request message: `looprpc.ListSwapsRequest`
- Response message: `looprpc.ListSwapsResponse`

The request takes an optional `list_swap_filter` (`ListSwapsFilter`: `swap_type`, `pending_only`, `outgoing_chan_set`, `label`, `loop_in_last_hop`, `asset_swap_only`, `start_timestamp_ns`) and `max_swaps`. The response has `swaps` (a list of `SwapStatus`) and `next_start_time`, the timestamp to use for paging `start_timestamp_ns`. ([source](../../raw/api/api-docs/api/loop/swap-client/list-swaps.md))

### SwapInfo

SwapInfo returns all known details about a single swap. ([source](../../raw/api/api-docs/api/loop/swap-client/swap-info.md))

- gRPC: `rpc SwapInfo (SwapInfoRequest) returns (SwapStatus);`
- REST: `GET` `/v1/loop/swap/{id}`
- Request message: `looprpc.SwapInfoRequest`
- Response message: `looprpc.SwapStatus`

`id` is the swap identifier, which currently is the hash that locks the HTLCs; when using REST it must be encoded as URL safe base64. The response is the same `looprpc.SwapStatus` message that Monitor streams. ([source](../../raw/api/api-docs/api/loop/swap-client/swap-info.md))

### AbandonSwap

AbandonSwap allows the client to abandon a swap. ([source](../../raw/api/api-docs/api/loop/swap-client/abandon-swap.md))

- gRPC: `rpc AbandonSwap (AbandonSwapRequest) returns (AbandonSwapResponse);`
- REST: none listed on the page
- Request message: `looprpc.AbandonSwapRequest`
- Response message: `looprpc.AbandonSwapResponse`

The page lists no REST path. `id` is the swap identifier. `i_know_what_i_am_doing` is a flag that tries to ensure that the client understands that they are risking loss of funds by abandoning a swap. The response has no parameters. ([source](../../raw/api/api-docs/api/loop/swap-client/abandon-swap.md))

### SweepHtlc

SweepHtlc spends a swap HTLC output via either the preimage success path or the cooperative key path, using stored or stateless recovery data. ([source](../../raw/api/api-docs/api/loop/swap-client/sweep-htlc.md))

- gRPC: `rpc SweepHtlc (SweepHtlcRequest) returns (SweepHtlcResponse);`
- REST: `POST` `/v1/loop/out/sweephtlc`
- Request message: `looprpc.SweepHtlcRequest`
- Response message: `looprpc.SweepHtlcResponse`

Request fields: `outpoint` (the HTLC outpoint to sweep, formatted as "txid:vout"), `htlc_address`, `sat_per_vbyte`, `dest_address` (optional; defaults to a new address derived from the connected lnd wallet), `preimage` (optional override, required when `stateless_recovery` is set), `publish` (if true, publish the sweep transaction immediately), `stateless_recovery` (`StatelessRecovery`: `server_pubkey`, `client_pubkey`, `cltv_expiry`, `swap_initiation_height`, `key_scan_limit`) and `cooperative` (`CooperativeSweep`: `payment_address`). The response has `sweep_tx` (raw sweep transaction bytes), `fee_sats` (miner fee paid by the sweep transaction) and the fields `not_requested`, `published` and `failed` (`PublishFailed` carries an `error` string). ([source](../../raw/api/api-docs/api/loop/swap-client/sweep-htlc.md))

## Terms, quotes and probing

### LoopOutTerms

LoopOutTerms returns the terms that the server enforces for a loop out swap. ([source](../../raw/api/api-docs/api/loop/swap-client/loop-out-terms.md))

- gRPC: `rpc LoopOutTerms (TermsRequest) returns (OutTermsResponse);`
- REST: `GET` `/v1/loop/out/terms`
- Request message: `looprpc.TermsRequest`
- Response message: `looprpc.OutTermsResponse`

`TermsRequest` has no parameters. The response has `min_swap_amount` and `max_swap_amount` (both in sat), `min_cltv_delta` and `max_cltv_delta`. ([source](../../raw/api/api-docs/api/loop/swap-client/loop-out-terms.md))

### LoopOutQuote

LoopOutQuote returns a quote for a loop out swap with the provided parameters. ([source](../../raw/api/api-docs/api/loop/swap-client/loop-out-quote.md))

- gRPC: `rpc LoopOutQuote (QuoteRequest) returns (OutQuoteResponse);`
- REST: `GET` `/v1/loop/out/quote/{amt}`
- Request message: `looprpc.QuoteRequest`
- Response message: `looprpc.OutQuoteResponse`

`amt` is the amount to swap in satoshis and is placed in the REST path. Other `QuoteRequest` fields include `conf_target`, `external_htlc`, `swap_publication_deadline` (only has an effect on loop out quotes), `private` and `asset_info`. The response has `swap_fee_sat`, `prepay_amt_sat`, `htlc_sweep_fee_sat`, `swap_payment_dest`, `cltv_delta`, `conf_target` and `asset_rfq_info`. ([source](../../raw/api/api-docs/api/loop/swap-client/loop-out-quote.md))

### GetLoopInTerms

GetTerms returns the terms that the server enforces for swaps. ([source](../../raw/api/api-docs/api/loop/swap-client/get-loop-in-terms.md))

- gRPC: `rpc GetLoopInTerms (TermsRequest) returns (InTermsResponse);`
- REST: `GET` `/v1/loop/in/terms`
- Request message: `looprpc.TermsRequest`
- Response message: `looprpc.InTermsResponse`

`TermsRequest` has no parameters. The response has `min_swap_amount` and `max_swap_amount`, both in sat. ([source](../../raw/api/api-docs/api/loop/swap-client/get-loop-in-terms.md))

### GetLoopInQuote

GetQuote returns a quote for a swap with the provided parameters. ([source](../../raw/api/api-docs/api/loop/swap-client/get-loop-in-quote.md))

- gRPC: `rpc GetLoopInQuote (QuoteRequest) returns (InQuoteResponse);`
- REST: `GET` `/v1/loop/in/quote/{amt}`
- Request message: `looprpc.QuoteRequest`
- Response message: `looprpc.InQuoteResponse`

The request is the same `looprpc.QuoteRequest` as for LoopOutQuote; the loop-in specific fields are `loop_in_last_hop`, `loop_in_route_hints`, `deposit_outpoints`, `auto_select_deposits` (must be false in the legacy loop-in case) and `fast` (only available for static address loop in swaps). The response has `swap_fee_sat`, `htlc_publish_fee_sat`, `cltv_delta`, `conf_target` and `quoted_amt`. An `htlc_publish_fee_sat` of 0 means the `external_htlc` flag was set and the fee estimation was skipped; -1 means lnd's wallet could not create a sample estimation transaction because not enough funds are available. ([source](../../raw/api/api-docs/api/loop/swap-client/get-loop-in-quote.md))

### Probe

Probe asks he sever to probe the route to us to have a better upfront estimate about routing fees when loopin-in. ([source](../../raw/api/api-docs/api/loop/swap-client/probe.md))

- gRPC: `rpc Probe (ProbeRequest) returns (ProbeResponse);`
- REST: `GET` `/v1/loop/in/probe/{amt}`
- Request message: `looprpc.ProbeRequest`
- Response message: `looprpc.ProbeResponse`

Request fields: `amt` (the amount to probe, in the REST path), `last_hop` and `route_hints`. The response has no parameters. ([source](../../raw/api/api-docs/api/loop/swap-client/probe.md))

## L402 tokens

### GetL402Tokens

GetL402Tokens returns all L402 tokens the daemon ever paid for. ([source](../../raw/api/api-docs/api/loop/swap-client/get-l402-tokens.md))

- gRPC: `rpc GetL402Tokens (TokensRequest) returns (TokensResponse);`
- REST: `GET` `/v1/l402/tokens`
- Request message: `looprpc.TokensRequest`
- Response message: `looprpc.TokensResponse`

`TokensRequest` has no parameters. The response field `tokens` lists all tokens the daemon knows of, including old/expired tokens. Each `L402Token` has `base_macaroon`, `payment_hash`, `payment_preimage`, `amount_paid_msat`, `routing_fee_paid_msat`, `time_created`, `expired`, `storage_name` and `id`. ([source](../../raw/api/api-docs/api/loop/swap-client/get-l402-tokens.md))

### GetLsatTokens

The page marks this RPC as deprecated: "This RPC is deprecated and will be removed in a future version." Deprecated: use GetL402Tokens. This API is provided to maintain backward compatibility with gRPC clients (e.g. `loop listauth`, Terminal Web, RTL). Type LsatToken used by GetLsatTokens in the past was renamed to L402Token, but this does not affect binary encoding, so we can use type L402Token here. ([source](../../raw/api/api-docs/api/loop/swap-client/get-lsat-tokens.md))

- gRPC: `rpc GetLsatTokens (TokensRequest) returns (TokensResponse);`
- REST: none listed on the page
- Request message: `looprpc.TokensRequest`
- Response message: `looprpc.TokensResponse`

The page lists no REST path. It uses the same `TokensRequest` and `TokensResponse` messages as GetL402Tokens. ([source](../../raw/api/api-docs/api/loop/swap-client/get-lsat-tokens.md))

### FetchL402Token

FetchL402Token fetches an L402 token from the server, this is required in order to receive reservation notifications from the server. ([source](../../raw/api/api-docs/api/loop/swap-client/fetch-l402-token.md))

- gRPC: `rpc FetchL402Token (FetchL402TokenRequest) returns (FetchL402TokenResponse);`
- REST: none listed on the page
- Request message: `looprpc.FetchL402TokenRequest`
- Response message: `looprpc.FetchL402TokenResponse`

The page lists no REST path. Neither the request nor the response has parameters. ([source](../../raw/api/api-docs/api/loop/swap-client/fetch-l402-token.md))

## Daemon

### GetInfo

GetInfo gets basic information about the loop daemon. ([source](../../raw/api/api-docs/api/loop/swap-client/get-info.md))

- gRPC: `rpc GetInfo (GetInfoRequest) returns (GetInfoResponse);`
- REST: `GET` `/v1/loop/info`
- Request message: `looprpc.GetInfoRequest`
- Response message: `looprpc.GetInfoResponse`

The request has no parameters. The response has `version`, `network`, `rpc_listen`, `rest_listen`, `macaroon_path`, `tls_cert_path`, `loop_out_stats`, `loop_in_stats` (both `LoopStats`: `pending_count`, `success_count`, `fail_count`, `sum_pending_amt`, `sum_succeeded_amt`) and `commit_hash`. ([source](../../raw/api/api-docs/api/loop/swap-client/get-info.md))

### StopDaemon

StopDaemon instructs the daemon to shut down gracefully. ([source](../../raw/api/api-docs/api/loop/swap-client/stop-daemon.md))

- gRPC: `rpc StopDaemon (StopDaemonRequest) returns (StopDaemonResponse);`
- REST: `POST` `/v1/daemon/stop`
- Request message: `looprpc.StopDaemonRequest`
- Response message: `looprpc.StopDaemonResponse`

Neither the request nor the response has parameters. ([source](../../raw/api/api-docs/api/loop/swap-client/stop-daemon.md))

## Liquidity manager (autoloop)

### GetLiquidityParams

GetLiquidityParams gets the parameters that the daemon's liquidity manager is currently configured with. This may be nil if nothing is configured. [EXPERIMENTAL]: endpoint is subject to change. ([source](../../raw/api/api-docs/api/loop/swap-client/get-liquidity-params.md))

- gRPC: `rpc GetLiquidityParams (GetLiquidityParamsRequest) returns (LiquidityParameters);`
- REST: `GET` `/v1/liquidity/params`
- Request message: `looprpc.GetLiquidityParamsRequest`
- Response message: `looprpc.LiquidityParameters`

The request has no parameters. `LiquidityParameters` has: `rules` (a list of `LiquidityRule`: `channel_id`, `swap_type`, `pubkey`, `type`, `incoming_threshold`, `outgoing_threshold`), `fee_ppm`, `sweep_fee_rate_sat_per_vbyte`, `max_swap_fee_ppm`, `max_routing_fee_ppm`, `max_prepay_routing_fee_ppm`, `max_prepay_sat`, `max_miner_fee_sat`, `sweep_conf_target`, `failure_backoff_sec`, `autoloop`, `autoloop_budget_sat`, `autoloop_budget_start_sec` (deprecated), `auto_max_in_flight`, `min_swap_amount`, `max_swap_amount`, `htlc_conf_target`, `autoloop_dest_address`, `autoloop_budget_refresh_period_sec`, `autoloop_budget_last_refresh`, `easy_autoloop`, `easy_autoloop_local_target_sat`, `account`, `account_addr_type`, `easy_asset_params`, `fast_swap_publication`, `easy_autoloop_excluded_peers` and `loop_in_source` (`LOOP_IN_SOURCE_WALLET` or `LOOP_IN_SOURCE_STATIC_ADDRESS`). `fee_ppm` may not be set in conjunction with sweep fee rate, swap fee ppm, routing fee ppm, prepay routing, max prepay and max miner fee. See [[autoloop]] for the CLI side. ([source](../../raw/api/api-docs/api/loop/swap-client/get-liquidity-params.md))

### SetLiquidityParams

SetLiquidityParams sets a new set of parameters for the daemon's liquidity manager. Note that the full set of parameters must be provided, because this call fully overwrites our existing parameters. [EXPERIMENTAL]: endpoint is subject to change. ([source](../../raw/api/api-docs/api/loop/swap-client/set-liquidity-params.md))

- gRPC: `rpc SetLiquidityParams (SetLiquidityParamsRequest) returns (SetLiquidityParamsResponse);`
- REST: `POST` `/v1/liquidity/params`
- Request message: `looprpc.SetLiquidityParamsRequest`
- Response message: `looprpc.SetLiquidityParamsResponse`

The single request field `parameters` is a `LiquidityParameters` message (described under GetLiquidityParams); the current set of parameters is completely overwritten by the parameters provided (if they are valid). The response has no parameters. ([source](../../raw/api/api-docs/api/loop/swap-client/set-liquidity-params.md))

### SuggestSwaps

SuggestSwaps returns a list of recommended swaps based on the current state of your node's channels and it's liquidity manager parameters. Note that only loop out suggestions are currently supported. [EXPERIMENTAL]: endpoint is subject to change. ([source](../../raw/api/api-docs/api/loop/swap-client/suggest-swaps.md))

- gRPC: `rpc SuggestSwaps (SuggestSwapsRequest) returns (SuggestSwapsResponse);`
- REST: `GET` `/v1/auto/suggest`
- Request message: `looprpc.SuggestSwapsRequest`
- Response message: `looprpc.SuggestSwapsResponse`

The request has no parameters. The response has `loop_out` (a list of `LoopOutRequest`), `loop_in` (a list of `LoopInRequest`), `static_loop_in` (a list of `StaticAddressLoopInRequest`) and `disqualified` (a list of `Disqualified`: `channel_id`, `pubkey`, `reason`). `reason` is an `AutoReason` enum value such as `AUTO_REASON_BUDGET_ELAPSED`, `AUTO_REASON_SWEEP_FEES`, `AUTO_REASON_IN_FLIGHT` or `AUTO_REASON_LIQUIDITY_OK`. ([source](../../raw/api/api-docs/api/loop/swap-client/suggest-swaps.md))

## Instant out and reservations

### ListReservations

ListReservations returns a list of all reservations the server opened to us. ([source](../../raw/api/api-docs/api/loop/swap-client/list-reservations.md))

- gRPC: `rpc ListReservations (ListReservationsRequest) returns (ListReservationsResponse);`
- REST: `GET` `/v1/instantout/reservations`
- Request message: `looprpc.ListReservationsRequest`
- Response message: `looprpc.ListReservationsResponse`

The request has no parameters. The response field `reservations` is a list of `ClientReservation`: `reservation_id`, `state`, `amount`, `tx_id`, `vout`, `expiry`. ([source](../../raw/api/api-docs/api/loop/swap-client/list-reservations.md))

### InstantOut

InstantOut initiates an instant out swap with the given parameters. ([source](../../raw/api/api-docs/api/loop/swap-client/instant-out.md))

- gRPC: `rpc InstantOut (InstantOutRequest) returns (InstantOutResponse);`
- REST: `POST` `/v1/instantout`
- Request message: `looprpc.InstantOutRequest`
- Response message: `looprpc.InstantOutResponse`

Request fields: `reservation_ids` (the reservations to use for the swap), `outgoing_chan_set`, `dest_addr` (optional; if not set, the funds are swept to the wallet's internal address) and `max_swap_fee_sat` (must be set; an explicitly set value of zero rejects any positive swap fee). The response has `instant_out_hash`, `sweep_tx_id` and `state`. ([source](../../raw/api/api-docs/api/loop/swap-client/instant-out.md))

### InstantOutQuote

InstantOutQuote returns a quote for an instant out swap with the provided parameters. ([source](../../raw/api/api-docs/api/loop/swap-client/instant-out-quote.md))

- gRPC: `rpc InstantOutQuote (InstantOutQuoteRequest) returns (InstantOutQuoteResponse);`
- REST: `POST` `/v1/instantout/quote`
- Request message: `looprpc.InstantOutQuoteRequest`
- Response message: `looprpc.InstantOutQuoteResponse`

Request fields: `amt` (satoshis) and `reservation_ids`; `num_reservations` is deprecated in favour of `reservation_ids`. The response has `service_fee_sat` and `sweep_fee_sat`, the estimated on-chain fee that needs to be paid to publish the Sweepless Sweep. ([source](../../raw/api/api-docs/api/loop/swap-client/instant-out-quote.md))

### ListInstantOuts

ListInstantOuts returns a list of all currently known instant out swaps and their current status. ([source](../../raw/api/api-docs/api/loop/swap-client/list-instant-outs.md))

- gRPC: `rpc ListInstantOuts (ListInstantOutsRequest) returns (ListInstantOutsResponse);`
- REST: `GET` `/v1/instantout/swaps`
- Request message: `looprpc.ListInstantOutsRequest`
- Response message: `looprpc.ListInstantOutsResponse`

The request has no parameters. The response field `swaps` is a list of `InstantOut`: `swap_hash`, `state`, `amount`, `reservation_ids`, `sweep_tx_id`. ([source](../../raw/api/api-docs/api/loop/swap-client/list-instant-outs.md))

## Static addresses

### NewStaticAddress

NewStaticAddress requests a new static address for loop-ins from the server. ([source](../../raw/api/api-docs/api/loop/swap-client/new-static-address.md))

- gRPC: `rpc NewStaticAddress (NewStaticAddressRequest) returns (NewStaticAddressResponse);`
- REST: `POST` `/v1/staticaddr`
- Request message: `looprpc.NewStaticAddressRequest`
- Response message: `looprpc.NewStaticAddressResponse`

The request field `client_key` is the client's public key for the 2-of-2 MuSig2 taproot static address. The response has `address` (the taproot static address) and `expiry` (the CSV expiry of the static address). ([source](../../raw/api/api-docs/api/loop/swap-client/new-static-address.md))

### ListUnspentDeposits

ListUnspentDeposits returns a list of utxos deposited at a static address. ([source](../../raw/api/api-docs/api/loop/swap-client/list-unspent-deposits.md))

- gRPC: `rpc ListUnspentDeposits (ListUnspentDepositsRequest) returns (ListUnspentDepositsResponse);`
- REST: `GET` `/v1/staticaddr/deposits/unspent`
- Request message: `looprpc.ListUnspentDepositsRequest`
- Response message: `looprpc.ListUnspentDepositsResponse`

Request fields: `min_confs` and `max_confs` (a zero value indicates that there is no maximum). The response field `utxos` is a list of `Utxo`: `static_address`, `amount_sat`, `outpoint`, `confirmations`. ([source](../../raw/api/api-docs/api/loop/swap-client/list-unspent-deposits.md))

### WithdrawDeposits

WithdrawDeposits withdraws a selection or all deposits of a static address. The page tags the RPC with the CLI reference loop:`static withdraw`. ([source](../../raw/api/api-docs/api/loop/swap-client/withdraw-deposits.md))

- gRPC: `rpc WithdrawDeposits (WithdrawDepositsRequest) returns (WithdrawDepositsResponse);`
- REST: `POST` `/v1/staticaddr/withdraw`
- Request message: `looprpc.WithdrawDepositsRequest`
- Response message: `looprpc.WithdrawDepositsResponse`

Request fields: `outpoints`, `all` (if true, all deposits will be withdrawn), `dest_addr`, `sat_per_vbyte` and `amount`. If there is change, it is sent back to the static address, and the fees for the transaction are taken from the change output. The response has `withdrawal_tx_hash` and `address`. ([source](../../raw/api/api-docs/api/loop/swap-client/withdraw-deposits.md))

### ListStaticAddressDeposits

ListStaticAddressDeposits returns a list of filtered static address deposits. The page tags the RPC with the CLI reference loop:`listdeposits`. ([source](../../raw/api/api-docs/api/loop/swap-client/list-static-address-deposits.md))

- gRPC: `rpc ListStaticAddressDeposits (ListStaticAddressDepositsRequest) returns (ListStaticAddressDepositsResponse);`
- REST: `GET` `/v1/staticaddr/deposits`
- Request message: `looprpc.ListStaticAddressDepositsRequest`
- Response message: `looprpc.ListStaticAddressDepositsResponse`

Request fields: `state_filter` (a `DepositState`) and `outpoints`. The response field `filtered_deposits` is a list of `Deposit`: `id`, `state`, `outpoint`, `value`, `confirmation_height`, `blocks_until_expiry`, `swap_hash`, `cost_onchain`, `cost_onchain_status`. `DepositState` values: `UNKNOWN_STATE`, `DEPOSITED`, `WITHDRAWING`, `WITHDRAWN`, `LOOPING_IN`, `LOOPED_IN`, `SWEEP_HTLC_TIMEOUT`, `HTLC_TIMEOUT_SWEPT`, `PUBLISH_EXPIRED`, `WAIT_FOR_EXPIRY_SWEEP`, `EXPIRED`, `OPENING_CHANNEL`, `CHANNEL_PUBLISHED`. ([source](../../raw/api/api-docs/api/loop/swap-client/list-static-address-deposits.md))

### ListStaticAddressWithdrawals

ListStaticAddressWithdrawals returns a list of static address withdrawals. The page tags the RPC with the CLI reference loop:`listwithdrawals`. ([source](../../raw/api/api-docs/api/loop/swap-client/list-static-address-withdrawals.md))

- gRPC: `rpc ListStaticAddressWithdrawals (ListStaticAddressWithdrawalRequest) returns (ListStaticAddressWithdrawalResponse);`
- REST: `GET` `/v1/staticaddr/withdrawals`
- Request message: `looprpc.ListStaticAddressWithdrawalRequest`
- Response message: `looprpc.ListStaticAddressWithdrawalResponse`

The request has no parameters. The response field `withdrawals` is a list of `StaticAddressWithdrawal`: `tx_id`, `deposits`, `total_deposit_amount_satoshis`, `withdrawn_amount_satoshis`, `change_amount_satoshis`, `confirmation_height`. ([source](../../raw/api/api-docs/api/loop/swap-client/list-static-address-withdrawals.md))

### ListStaticAddressSwaps

ListStaticAddressSwaps returns a list of filtered static address swaps. The page tags the RPC with the CLI reference loop:`listswaps`. ([source](../../raw/api/api-docs/api/loop/swap-client/list-static-address-swaps.md))

- gRPC: `rpc ListStaticAddressSwaps (ListStaticAddressSwapsRequest) returns (ListStaticAddressSwapsResponse);`
- REST: `GET` `/v1/staticaddr/swaps`
- Request message: `looprpc.ListStaticAddressSwapsRequest`
- Response message: `looprpc.ListStaticAddressSwapsResponse`

The request has no parameters. The response field `swaps` is a list of `StaticAddressLoopInSwap`: `swap_hash`, `deposit_outpoints`, `state`, `swap_amount_satoshis`, `payment_request_amount_satoshis` (the swap amount minus the quoted server fees), `deposits`, `initiation_time`, `last_update_time`, `cost_server`, `cost_onchain`, `cost_offchain`, `cost_onchain_status`. ([source](../../raw/api/api-docs/api/loop/swap-client/list-static-address-swaps.md))

### GetStaticAddressSummary

GetStaticAddressSummary returns a summary of static address related statistics. The page tags the RPC with the CLI reference loop:`static summary`. ([source](../../raw/api/api-docs/api/loop/swap-client/get-static-address-summary.md))

- gRPC: `rpc GetStaticAddressSummary (StaticAddressSummaryRequest) returns (StaticAddressSummaryResponse);`
- REST: `GET` `/v1/staticaddr/summary`
- Request message: `looprpc.StaticAddressSummaryRequest`
- Response message: `looprpc.StaticAddressSummaryResponse`

The request has no parameters. The response has `static_address`, `relative_expiry_blocks` (the CSV expiry of the static address), `total_num_deposits`, `value_unconfirmed_satoshis`, `value_deposited_satoshis`, `value_expired_satoshis`, `value_withdrawn_satoshis`, `value_looped_in_satoshis`, `value_htlc_timeout_sweeps_satoshis` and `value_channels_opened`. ([source](../../raw/api/api-docs/api/loop/swap-client/get-static-address-summary.md))

### StaticAddressLoopIn

StaticAddressLoopIn initiates a static address loop-in swap. The page tags the RPC with the CLI reference loop:`static in`. ([source](../../raw/api/api-docs/api/loop/swap-client/static-address-loop-in.md))

- gRPC: `rpc StaticAddressLoopIn (StaticAddressLoopInRequest) returns (StaticAddressLoopInResponse);`
- REST: `POST` `/v1/staticaddr/loopin`
- Request message: `looprpc.StaticAddressLoopInRequest`
- Response message: `looprpc.StaticAddressLoopInResponse`

Request fields: `outpoints` (the deposits to loop-in), `max_swap_fee_satoshis`, `last_hop`, `label`, `initiator`, `route_hints`, `private`, `payment_timeout_seconds`, `amount` and `fast`. `amount` is optional: provided with outpoints, the client takes this amount from the sum of the outpoints and sends the change back to the static address; provided without outpoints, the client selects deposits automatically. The response has `swap_hash`, `state`, `amount`, `htlc_cltv`, `quoted_swap_fee_satoshis`, `max_swap_fee_satoshis`, `initiation_height`, `protocol_version`, `label`, `initiator`, `payment_timeout_seconds`, `used_deposits`, `swap_amount`, `change` and `fast`. ([source](../../raw/api/api-docs/api/loop/swap-client/static-address-loop-in.md))

### StaticOpenChannel

StaticOpenChannel opens a channel funded by selected static address deposits. The page tags the RPC with the CLI reference loop:`static openchannel`. ([source](../../raw/api/api-docs/api/loop/swap-client/static-open-channel.md))

- gRPC: `rpc StaticOpenChannel (StaticOpenChannelRequest) returns (StaticOpenChannelResponse);`
- REST: none listed on the page
- Request message: `looprpc.StaticOpenChannelRequest`
- Response message: `looprpc.StaticOpenChannelResponse`

The page lists no REST path. The request field `open_channel_request` wraps lnd's `OpenChannelRequest`. The response has `channel_open_outpoint`, the outpoint of the channel opening transaction in the format "txid:output_index". ([source](../../raw/api/api-docs/api/loop/swap-client/static-open-channel.md))
