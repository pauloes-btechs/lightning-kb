---
title: lnd router service
type: service
sources:
  - raw/api/api-docs/api/lnd.md
  - raw/api/api-docs/api/lnd/rest-endpoints.md
  - raw/api/api-docs/api/lnd/router/build-route.md
  - raw/api/api-docs/api/lnd/router/delete-forwarding-history.md
  - raw/api/api-docs/api/lnd/router/estimate-route-fee.md
  - raw/api/api-docs/api/lnd/router/get-mission-control-config.md
  - raw/api/api-docs/api/lnd/router/htlc-interceptor.md
  - raw/api/api-docs/api/lnd/router/query-mission-control.md
  - raw/api/api-docs/api/lnd/router/query-probability.md
  - raw/api/api-docs/api/lnd/router/reset-mission-control.md
  - raw/api/api-docs/api/lnd/router/send-payment-v2.md
  - raw/api/api-docs/api/lnd/router/send-to-route-v2.md
  - raw/api/api-docs/api/lnd/router/set-mission-control-config.md
  - raw/api/api-docs/api/lnd/router/subscribe-htlc-events.md
  - raw/api/api-docs/api/lnd/router/track-payment-v2.md
  - raw/api/api-docs/api/lnd/router/track-payments.md
  - raw/api/api-docs/api/lnd/router/update-chan-status.md
  - raw/api/api-docs/api/lnd/router/x-add-local-chan-aliases.md
  - raw/api/api-docs/api/lnd/router/x-delete-local-chan-aliases.md
  - raw/api/api-docs/api/lnd/router/x-find-base-local-chan-alias.md
  - raw/api/api-docs/api/lnd/router/x-import-mission-control.md
updated: 2026-11-14
---

# lnd router service (Router)

The router service of [[lnd]] is documented through the RPC pages summarised below. The SendPaymentV2 page gives `routerrpc/router.proto` as its source. ([source](../../raw/api/api-docs/api/lnd/router/send-payment-v2.md))

The reference was generated automatically against commit `895118ac4ec59e78b2c14f5b0d31ac6f862434bb` of the `lightningnetwork/lnd` repository. ([source](../../raw/api/api-docs/api/lnd.md))

The REST endpoints page lists 19 `routerrpc` RPCs under `/v2/router/`: DeleteForwardingHistory, SubscribeHtlcEvents, HtlcInterceptor, QueryMissionControl, QueryProbability, ResetMissionControl, GetMissionControlConfig, SetMissionControlConfig, TrackPayments, BuildRoute, EstimateRouteFee, SendToRouteV2, SendPaymentV2, TrackPaymentV2, UpdateChanStatus, XAddLocalChanAliases, XDeleteLocalChanAliases, XFindBaseLocalChanAlias and XImportMissionControl. ([source](../../raw/api/api-docs/api/lnd/rest-endpoints.md))

See also: [[lnd-invoices]], [[lnd-switch]], [[lnd-lightning]], [[lnd-interceptors]], [[lnd-sending-payments]], [[lnd-receiving-payments]], [[htlc]], [[multipath-payments]], [[pathfinding]], [[lightning-invoices]].

## SendPaymentV2

SendPaymentV2 attempts to route a payment described by the passed PaymentRequest to the final destination. The call returns a stream of payment updates. When using this RPC, make sure to set a fee limit, as the default routing fee limit is 0 sats; without a non-zero fee limit only routes without fees will be attempted, which often fails with `FAILURE_REASON_NO_ROUTE`. The page marks it as a server-streaming RPC. ([source](../../raw/api/api-docs/api/lnd/router/send-payment-v2.md))

- gRPC: `rpc SendPaymentV2 (SendPaymentRequest) returns (stream Payment);`
- REST: `POST /v2/router/send`
- Request message: `routerrpc.SendPaymentRequest`
- Response message: stream of `lnrpc.Payment`

Selected request fields:

- `payment_request`: a bare-bones invoice for a payment within the Lightning Network. The amount in the payment request may be zero, in which case it is required to set the `amt` field as well. If no payment request is specified, the following fields are required: `dest`, `amt` and `payment_hash`.
- `amt` and `amt_msat`: number of satoshis or millisatoshis to send; mutually exclusive.
- `fee_limit_sat` and `fee_limit_msat`: the maximum fee for the payment; mutually exclusive. If left to the default value of 0, only zero-fee routes will be considered. To send the payment without a fee limit, use max int.
- `timeout_seconds`: an optional limit, in seconds, on the time to wait before attempting the first HTLC. Once HTLCs are in flight, the payment will not be aborted until the HTLCs are either settled or failed. If not set or explicitly set to zero, the default value of 60 seconds will be applied.
- `cltv_limit`: an optional maximum total time lock for the route. This should not exceed lnd's `--max-cltv-expiry` setting. If zero, the value of `--max-cltv-expiry` is enforced.
- `final_cltv_delta`: the CLTV delta from the current height that should be used to set the timelock for the final hop.
- `outgoing_chan_ids`: the channel ids of the channels allowed for the first hop. If empty, any channel may be used.
- `last_hop_pubkey`: the pubkey of the last hop of the route. If empty, any hop may be used.
- `allow_self_payment`: if set, circular payments to self are permitted.
- `max_parts`: the maximum number of partial payments that may be used to complete the full amount.
- `max_shard_size_msat`: the largest payment split that should be attempted when making a payment if splitting is necessary.
- `amp`: if set, an AMP-payment will be attempted.
- `time_pref`: the time preference for this payment. Set to -1 to optimize for fees only, to 1 to optimize for reliability only, or a value in between for a mix.
- `no_inflight_updates`: if set, only the final payment update is streamed back.
- `cancelable`: if set, the payment loop can be interrupted by manually canceling the payment context, even before the payment timeout is reached. The payment may still succeed after cancellation, as in-flight attempts can still settle afterwards.
- `route_hints`, `dest_custom_records`, `dest_features`, `payment_addr`, `first_hop_custom_records`: further optional fields listed on the page.

In the `lnrpc.Payment` response, `status` is an `lnrpc.Payment.PaymentStatus` with the values `UNKNOWN` (deprecated, never returned), `IN_FLIGHT`, `SUCCEEDED`, `FAILED` and `INITIATED`. `htlcs` lists the HTLCs made in attempt to settle the payment, and `failure_reason` is an `lnrpc.PaymentFailureReason`. ([source](../../raw/api/api-docs/api/lnd/router/send-payment-v2.md))

## TrackPaymentV2

TrackPaymentV2 returns an update stream for the payment identified by the payment hash. The page marks it as a server-streaming RPC. ([source](../../raw/api/api-docs/api/lnd/router/track-payment-v2.md))

- gRPC: `rpc TrackPaymentV2 (TrackPaymentRequest) returns (stream Payment);`
- REST: `GET /v2/router/track/{payment_hash}`
- Request message: `routerrpc.TrackPaymentRequest`
- Response message: stream of `lnrpc.Payment`

Request fields: `payment_hash` (the hash of the payment to look up) and `no_inflight_updates` (if set, only the final payment update is streamed back). ([source](../../raw/api/api-docs/api/lnd/router/track-payment-v2.md))

## TrackPayments

TrackPayments returns an update stream for every payment that is not in a terminal state. If payments are in-flight while starting a new subscription, the start of the payment stream could produce out-of-order and/or duplicate events. To get updates for every in-flight payment attempt, subscribe to this method before initiating any payments. The page marks it as a server-streaming RPC. ([source](../../raw/api/api-docs/api/lnd/router/track-payments.md))

- gRPC: `rpc TrackPayments (TrackPaymentsRequest) returns (stream Payment);`
- REST: `GET /v2/router/payments`
- Request message: `routerrpc.TrackPaymentsRequest`
- Response message: stream of `lnrpc.Payment`

The request has one field, `no_inflight_updates`. ([source](../../raw/api/api-docs/api/lnd/router/track-payments.md))

## EstimateRouteFee

EstimateRouteFee allows callers to obtain a lower bound w.r.t how much it may cost to send an HTLC to the target end destination. ([source](../../raw/api/api-docs/api/lnd/router/estimate-route-fee.md))

- gRPC: `rpc EstimateRouteFee (RouteFeeRequest) returns (RouteFeeResponse);`
- REST: `POST /v2/router/route/estimatefee`
- Request message: `routerrpc.RouteFeeRequest`
- Response message: `routerrpc.RouteFeeResponse`

Request fields:

- `dest`: the destination one wishes to obtain a routing fee quote to. If set, `amt_sat` must also be set. This combination triggers a graph based routing fee estimation, executed on the in memory graph, as opposed to a payment probe based estimate.
- `amt_sat`: the amount one wishes to send to the target destination; only to be used in combination with `dest`.
- `payment_request`: a payment request of the target node. Its parameters are input to probe payments that estimate routing fees. Cannot be used in combination with `dest` and `amt_sat`.
- `timeout`: how long a probe payment should maximally be allowed to take, in seconds. If not set or explicitly set to zero, the default value of 60 seconds will be applied.
- `outgoing_chan_ids`: the channel ids of the channels that are allowed for the first hop. If empty, any channel may be used.

Response fields: `routing_fee_msat` (a lower bound of the estimated fee, in milli-satoshis), `time_lock_delay` (an estimate of the worst case time delay; callers still need to factor in the final CLTV delta of the last hop) and `failure_reason` (whether a probing payment succeeded or why it failed; `FAILURE_REASON_NONE` indicates success). ([source](../../raw/api/api-docs/api/lnd/router/estimate-route-fee.md))

## BuildRoute

BuildRoute builds a fully specified route based on a list of hop public keys. It retrieves the relevant channel policies from the graph in order to calculate the correct fees and time locks. LND will use its default `final_cltv_delta` if no value is supplied, and the caller has to provide the `payment_addr` if the route is paying an invoice which signaled it. ([source](../../raw/api/api-docs/api/lnd/router/build-route.md))

- gRPC: `rpc BuildRoute (BuildRouteRequest) returns (BuildRouteResponse);`
- REST: `POST /v2/router/route`
- Request message: `routerrpc.BuildRouteRequest`
- Response message: `routerrpc.BuildRouteResponse`

Request fields: `amt_msat` (if set to zero, the minimum routable amount is used), `final_cltv_delta`, `outgoing_chan_id` (if zero, any channel may be used), `hop_pubkeys` (a list of hops that defines the route, not including the source hop pubkey), `payment_addr`, `first_hop_custom_records` and `source_pub_key` (if empty, the router's identity key is assumed). The response has one field, `route`, a fully specified `lnrpc.Route` that can be used to execute the payment. ([source](../../raw/api/api-docs/api/lnd/router/build-route.md))

## SendToRouteV2

SendToRouteV2 attempts to make a payment via the specified route. This method differs from SendPayment in that it allows users to specify a full route manually. This can be used for things like rebalancing, and atomic swaps. ([source](../../raw/api/api-docs/api/lnd/router/send-to-route-v2.md))

- gRPC: `rpc SendToRouteV2 (SendToRouteRequest) returns (HTLCAttempt);`
- REST: `POST /v2/router/route/send`
- Request message: `routerrpc.SendToRouteRequest`
- Response message: `lnrpc.HTLCAttempt`

Request fields: `payment_hash`, `route`, `skip_temp_err` (set it to true so the payment won't be failed unless a terminal error occurred, such as payment timeout, no routes, incorrect payment details, or insufficient funds) and `first_hop_custom_records`. The `lnrpc.HTLCAttempt` response has the fields `attempt_id`, `status`, `route`, `attempt_time_ns`, `resolve_time_ns`, `failure` and `preimage`; `status` is an `lnrpc.HTLCAttempt.HTLCStatus` with the values `IN_FLIGHT`, `SUCCEEDED` and `FAILED`. ([source](../../raw/api/api-docs/api/lnd/router/send-to-route-v2.md))

## QueryMissionControl

QueryMissionControl exposes the internal mission control state to callers. It is a development feature. ([source](../../raw/api/api-docs/api/lnd/router/query-mission-control.md))

- gRPC: `rpc QueryMissionControl (QueryMissionControlRequest) returns (QueryMissionControlResponse);`
- REST: `GET /v2/router/mc`
- Request message: `routerrpc.QueryMissionControlRequest` (no parameters)
- Response message: `routerrpc.QueryMissionControlResponse`

The response has one field, `pairs`, the node pair-level mission control state as a list of `routerrpc.PairHistory` (`node_from`, `node_to`, `history`). `history` is a `routerrpc.PairData` with the fields `fail_time`, `fail_amt_sat`, `fail_amt_msat`, `success_time`, `success_amt_sat` and `success_amt_msat`. ([source](../../raw/api/api-docs/api/lnd/router/query-mission-control.md))

## ResetMissionControl

ResetMissionControl clears all mission control state and starts with a clean slate. ([source](../../raw/api/api-docs/api/lnd/router/reset-mission-control.md))

- gRPC: `rpc ResetMissionControl (ResetMissionControlRequest) returns (ResetMissionControlResponse);`
- REST: `POST /v2/router/mc/reset`
- Request message: `routerrpc.ResetMissionControlRequest` (no parameters)
- Response message: `routerrpc.ResetMissionControlResponse` (no parameters)

([source](../../raw/api/api-docs/api/lnd/router/reset-mission-control.md))

## XImportMissionControl

XImportMissionControl is an experimental API that imports the state provided to the internal mission control's state, using all results which are more recent than the existing values. These values will only be imported in-memory, and will not be persisted across restarts. ([source](../../raw/api/api-docs/api/lnd/router/x-import-mission-control.md))

- gRPC: `rpc XImportMissionControl (XImportMissionControlRequest) returns (XImportMissionControlResponse);`
- REST: `POST /v2/router/x/importhistory`
- Request message: `routerrpc.XImportMissionControlRequest`
- Response message: `routerrpc.XImportMissionControlResponse` (no parameters)

Request fields: `pairs` (node pair-level mission control state to be imported) and `force` (whether to force override MC pair history; even with force override the failure pair is imported before the success pair and both still clamp existing failure/success amounts). ([source](../../raw/api/api-docs/api/lnd/router/x-import-mission-control.md))

## GetMissionControlConfig

GetMissionControlConfig returns mission control's current config. ([source](../../raw/api/api-docs/api/lnd/router/get-mission-control-config.md))

- gRPC: `rpc GetMissionControlConfig (GetMissionControlConfigRequest) returns (GetMissionControlConfigResponse);`
- REST: `GET /v2/router/mccfg`
- Request message: `routerrpc.GetMissionControlConfigRequest` (no parameters)
- Response message: `routerrpc.GetMissionControlConfigResponse`

The response has one field, `config`, a `routerrpc.MissionControlConfig`. Its fields are `half_life_seconds`, `hop_probability` and `weight` (all three deprecated in favour of AprioriParameters), `maximum_payment_results` (the maximum number of payment results that mission control will store), `minimum_failure_relax_interval`, `model`, `apriori` and `bimodal`. `model` is a `ProbabilityModel` with the values `APRIORI` and `BIMODAL`; the page notes that the bimodal estimator is experimental. `routerrpc.AprioriParameters` has the fields `half_life_seconds`, `hop_probability`, `weight` and `capacity_fraction` (allowed values are in [0.75, 1.0]; a value of 1.0 disables the capacity factor). `routerrpc.BimodalParameters` has the fields `node_weight`, `scale_msat` and `decay_time`. ([source](../../raw/api/api-docs/api/lnd/router/get-mission-control-config.md))

## SetMissionControlConfig

SetMissionControlConfig will set mission control's config, if the config provided is valid. ([source](../../raw/api/api-docs/api/lnd/router/set-mission-control-config.md))

- gRPC: `rpc SetMissionControlConfig (SetMissionControlConfigRequest) returns (SetMissionControlConfigResponse);`
- REST: `POST /v2/router/mccfg`
- Request message: `routerrpc.SetMissionControlConfigRequest`
- Response message: `routerrpc.SetMissionControlConfigResponse` (no parameters)

The request has one field, `config`, a `routerrpc.MissionControlConfig`. All values *must* be set, because the full config will be applied. ([source](../../raw/api/api-docs/api/lnd/router/set-mission-control-config.md))

## QueryProbability

The page marks this RPC as deprecated and says it will be removed in a future version. QueryProbability returns the current success probability estimate for a given node pair and amount. The call returns a zero success probability if no channel is available or if the amount violates min/max HTLC constraints. ([source](../../raw/api/api-docs/api/lnd/router/query-probability.md))

- gRPC: `rpc QueryProbability (QueryProbabilityRequest) returns (QueryProbabilityResponse);`
- REST: `GET /v2/router/mc/probability/{from_node}/{to_node}/{amt_msat}`
- Request message: `routerrpc.QueryProbabilityRequest`
- Response message: `routerrpc.QueryProbabilityResponse`

Request fields: `from_node`, `to_node` and `amt_msat`. Response fields: `probability` (the success probability for the requested pair) and `history` (the historical data for the requested pair, a `routerrpc.PairData`). ([source](../../raw/api/api-docs/api/lnd/router/query-probability.md))

## SubscribeHtlcEvents

SubscribeHtlcEvents creates a uni-directional stream from the server to the client which delivers a stream of htlc events. The page marks it as a server-streaming RPC. ([source](../../raw/api/api-docs/api/lnd/router/subscribe-htlc-events.md))

- gRPC: `rpc SubscribeHtlcEvents (SubscribeHtlcEventsRequest) returns (stream HtlcEvent);`
- REST: `GET /v2/router/htlcevents`
- Request message: `routerrpc.SubscribeHtlcEventsRequest` (no parameters)
- Response message: stream of `routerrpc.HtlcEvent`

`routerrpc.HtlcEvent` fields:

- `incoming_channel_id` and `incoming_htlc_id`: the short channel id the incoming htlc arrived on and its index in that channel. These values are zero for sends.
- `outgoing_channel_id` and `outgoing_htlc_id`: the short channel id the outgoing htlc left on and its index in that channel. These values are zero for receives.
- `timestamp_ns`: the time in unix nanoseconds that the event occurred.
- `event_type`: whether the htlc was part of a send, receive or forward. The `EventType` values are `UNKNOWN`, `SEND`, `RECEIVE` and `FORWARD`.
- `forward_event`, `forward_fail_event`, `settle_event`, `link_fail_event`, `subscribed_event`, `final_htlc_event`: the event payloads.

`routerrpc.LinkFailEvent` carries `info`, `wire_failure`, `failure_detail` and `failure_string`; `routerrpc.SettleEvent` carries `preimage`; `routerrpc.FinalHtlcEvent` carries `settled` and `offchain`. ([source](../../raw/api/api-docs/api/lnd/router/subscribe-htlc-events.md))

## HtlcInterceptor

HtlcInterceptor dispatches a bi-directional streaming RPC in which Forwarded HTLC requests are sent to the client and the client responds with a boolean that tells LND if this htlc should be intercepted. In case of interception, the htlc can be either settled, cancelled or resumed later by using the ResolveHoldForward endpoint. ([source](../../raw/api/api-docs/api/lnd/router/htlc-interceptor.md))

- gRPC: `rpc HtlcInterceptor (stream ForwardHtlcInterceptResponse) returns (stream ForwardHtlcInterceptRequest);`
- REST: `POST /v2/router/htlcinterceptor`
- Message sent by the client: `routerrpc.ForwardHtlcInterceptResponse`
- Message sent by the server: `routerrpc.ForwardHtlcInterceptRequest`

Selected `routerrpc.ForwardHtlcInterceptRequest` (server to client) fields:

- `incoming_circuit_key`: the key of this forwarded htlc, a `routerrpc.CircuitKey` (`chan_id`, `htlc_id`). Interceptor clients should handle requests for the same circuit key idempotently; requests may be replayed after reconnect.
- `incoming_amount_msat`: the amount the incoming peer actually committed to on the channel, and the only amount that can be trusted when deciding how to resolve the HTLC.
- `outgoing_amount_msat`: the amount the sender requested in the onion payload. It has NOT been validated against `incoming_amount_msat` or the forwarding policy of the outgoing channel yet; that validation only happens if the HTLC is resumed, and a SETTLE response skips it entirely.
- `payment_hash`: the htlc payment hash. This value is not guaranteed to be unique per request.
- `outgoing_requested_chan_id`: the requested outgoing channel id. Because of non-strict forwarding, this isn't necessarily the channel over which the packet will be forwarded eventually.
- `outgoing_requested_node_id`: the requested outgoing node for a blinded forward. When non-empty, `outgoing_requested_chan_id` is set to 18446744073709551615 (0xffffffffffffffff).
- `auto_fail_height`: the block height at which this htlc will be auto-failed to prevent the channel from force-closing.
- `incoming_expiry`, `outgoing_expiry`, `custom_records`, `onion_blob`, `in_wire_custom_records`: further fields listed on the page.

`routerrpc.ForwardHtlcInterceptResponse` (client to server) fields:

- `incoming_circuit_key`: the key of this forwarded htlc.
- `action`: the resolve action, a `routerrpc.ResolveHoldForwardAction` with the values `SETTLE`, `FAIL`, `RESUME` and `RESUME_MODIFIED`.
- `preimage`: the preimage in case the resolve action is Settle.
- `failure_message`: encrypted failure message in case the resolve action is Fail. If specified, `failure_code` must be set to zero.
- `failure_code`: the failure code to return in case the resolve action is Fail. For backwards-compatibility reasons, `TEMPORARY_CHANNEL_FAILURE` is the default value for this field.
- `in_amount_msat`: the amount to use in place of the actual incoming HTLC amount when resuming with `RESUME_MODIFIED`. A value of zero leaves the actual incoming amount unchanged.
- `out_amount_msat`: the amount to set on the p2p wire message of the resumed HTLC. Ignored if the action is not `RESUME_MODIFIED` or the amount is zero.
- `out_wire_custom_records`: custom records to set on the p2p wire message of the resumed HTLC. Ignored if the action is not `RESUME_MODIFIED`.

([source](../../raw/api/api-docs/api/lnd/router/htlc-interceptor.md))

## UpdateChanStatus

UpdateChanStatus attempts to manually set the state of a channel (enabled, disabled, or auto). A manual "disable" request will cause the channel to stay disabled until a subsequent manual request of either "enable" or "auto". ([source](../../raw/api/api-docs/api/lnd/router/update-chan-status.md))

- gRPC: `rpc UpdateChanStatus (UpdateChanStatusRequest) returns (UpdateChanStatusResponse);`
- REST: `POST /v2/router/updatechanstatus`
- Request message: `routerrpc.UpdateChanStatusRequest`
- Response message: `routerrpc.UpdateChanStatusResponse` (no parameters)

Request fields: `chan_point` (an `lnrpc.ChannelPoint`) and `action` (a `routerrpc.ChanStatusAction` with the values `ENABLE`, `DISABLE` and `AUTO`). ([source](../../raw/api/api-docs/api/lnd/router/update-chan-status.md))

## XAddLocalChanAliases

XAddLocalChanAliases is an experimental API that creates a set of new channel SCID alias mappings. The final total set of aliases in the manager after the add operation is returned. This is only a locally stored alias and will not be communicated to the channel peer via any message, so routing over such an alias will only work if the peer also calls this same RPC on their end. If an alias already exists, an error is returned. ([source](../../raw/api/api-docs/api/lnd/router/x-add-local-chan-aliases.md))

- gRPC: `rpc XAddLocalChanAliases (AddAliasesRequest) returns (AddAliasesResponse);`
- REST: `POST /v2/router/x/addaliases`
- Request message: `routerrpc.AddAliasesRequest`
- Response message: `routerrpc.AddAliasesResponse`

Both messages have one field, `alias_maps`, a list of `lnrpc.AliasMap` (`base_scid`, `aliases`). ([source](../../raw/api/api-docs/api/lnd/router/x-add-local-chan-aliases.md))

## XDeleteLocalChanAliases

XDeleteLocalChanAliases is an experimental API that deletes a set of alias mappings. The final total set of aliases in the manager after the delete operation is returned. The deletion will not be communicated to the channel peer via any message. ([source](../../raw/api/api-docs/api/lnd/router/x-delete-local-chan-aliases.md))

- gRPC: `rpc XDeleteLocalChanAliases (DeleteAliasesRequest) returns (DeleteAliasesResponse);`
- REST: `POST /v2/router/x/deletealiases`
- Request message: `routerrpc.DeleteAliasesRequest`
- Response message: `routerrpc.DeleteAliasesResponse`

Both messages have one field, `alias_maps`, a list of `lnrpc.AliasMap`. ([source](../../raw/api/api-docs/api/lnd/router/x-delete-local-chan-aliases.md))

## XFindBaseLocalChanAlias

XFindBaseLocalChanAlias is an experimental API that looks up the base scid for a local chan alias that was registered during the current runtime. ([source](../../raw/api/api-docs/api/lnd/router/x-find-base-local-chan-alias.md))

- gRPC: `rpc XFindBaseLocalChanAlias (FindBaseAliasRequest) returns (FindBaseAliasResponse);`
- REST: `POST /v2/router/x/findbasealias`
- Request message: `routerrpc.FindBaseAliasRequest`
- Response message: `routerrpc.FindBaseAliasResponse`

The request has one field, `alias` (the alias to look up the base scid for). The response has one field, `base` (the base scid that resulted from the look up). ([source](../../raw/api/api-docs/api/lnd/router/x-find-base-local-chan-alias.md))

## DeleteForwardingHistory

DeleteForwardingHistory allows the caller to delete forwarding history events with a timestamp at or before a specified time. This is useful for implementing data retention policies for privacy purposes. The call deletes events in batches and returns statistics including the total number of events deleted and the aggregate fees earned from those events. ([source](../../raw/api/api-docs/api/lnd/router/delete-forwarding-history.md))

- gRPC: `rpc DeleteForwardingHistory (DeleteForwardingHistoryRequest) returns (DeleteForwardingHistoryResponse);`
- REST: `POST /v2/router/fwdhistory/delete`
- Request message: `routerrpc.DeleteForwardingHistoryRequest`
- Response message: `routerrpc.DeleteForwardingHistoryResponse`

Request fields: `delete_before_time` (absolute Unix timestamp in seconds; events at or before this time are deleted) and `delete_before_duration` (a relative duration string indicating how far back to delete, e.g. "-30d" deletes events at or before 30 days ago). Response fields: `events_deleted`, `total_fee_msat` (the sum of (amt_in - amt_out) for all deleted events) and `status`. ([source](../../raw/api/api-docs/api/lnd/router/delete-forwarding-history.md))

## Conflicts

- HtlcInterceptor: the page's description says the client "responds with a boolean that tells LND if this htlc should be intercepted", while the client message `routerrpc.ForwardHtlcInterceptResponse` on the same page has no boolean field and instead carries `action`, a `ResolveHoldForwardAction` enum. The description also refers to a "ResolveHoldForward endpoint", which the page does not otherwise document. ([source](../../raw/api/api-docs/api/lnd/router/htlc-interceptor.md))
- On the SendPaymentV2 page, the "Source:" line of the `lnrpc.Payment` message is labelled `lightning.proto` while its link target is `lnrpc/routerrpc/router.proto`. The page does not say which proto file defines the message. ([source](../../raw/api/api-docs/api/lnd/router/send-payment-v2.md))
- The SendToRouteV2 page has the same mismatch for `lnrpc.HTLCAttempt`. ([source](../../raw/api/api-docs/api/lnd/router/send-to-route-v2.md))
