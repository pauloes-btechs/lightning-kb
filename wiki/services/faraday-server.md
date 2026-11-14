---
title: faraday faraday-server service
type: service
sources:
  - raw/api/api-docs/api/faraday.md
  - raw/api/api-docs/api/faraday/rest-endpoints.md
  - raw/api/api-docs/api/faraday/faraday-server/channel-insights.md
  - raw/api/api-docs/api/faraday/faraday-server/close-report.md
  - raw/api/api-docs/api/faraday/faraday-server/exchange-rate.md
  - raw/api/api-docs/api/faraday/faraday-server/forwarding-ability.md
  - raw/api/api-docs/api/faraday/faraday-server/get-channel-events.md
  - raw/api/api-docs/api/faraday/faraday-server/node-audit.md
  - raw/api/api-docs/api/faraday/faraday-server/outlier-recommendations.md
  - raw/api/api-docs/api/faraday/faraday-server/revenue-report.md
  - raw/api/api-docs/api/faraday/faraday-server/threshold-recommendations.md
updated: 2026-11-14
---

# faraday faraday-server service

The faraday-server service is the gRPC service of [[faraday]]. It has nine RPCs covering channel insights, revenue reports, close recommendations, close reports, channel events, forwarding ability, fiat exchange rates and a node audit. Its messages are in the `frdrpc` package. For the `frcli` commands that go with it see [[using-faraday]]. ([source](../../raw/api/api-docs/api/faraday/rest-endpoints.md), [source](../../raw/api/api-docs/api/faraday/faraday-server/forwarding-ability.md))

The reference was generated against commit `7226d871511a1995cd1aa08467b469809a36e508` of `lightninglabs/faraday` (`frdrpc/faraday.proto`). ([source](../../raw/api/api-docs/api/faraday.md))

A request needs a TLS/SSL connection and a macaroon used for RPC authentication (see [[macaroons]]). The code samples assume gRPC on port `8465`. ([source](../../raw/api/api-docs/api/faraday.md))

## ChannelInsights

List currently open channel with routing and uptime information.

```
rpc ChannelInsights (ChannelInsightsRequest) returns (ChannelInsightsResponse);
```

- REST: `GET /v1/faraday/insights`
- Request: `frdrpc.ChannelInsightsRequest` (no parameters).
- Response: `frdrpc.ChannelInsightsResponse`, with `channel_insights`, an array of `frdrpc.ChannelInsight`.
- `ChannelInsight` fields: `chan_point`, `monitored_seconds`, `uptime_seconds`, `volume_incoming_msat`, `volume_outgoing_msat`, `fees_earned_msat`, `confirmations`, `private`. Fees in `fees_earned_msat` are attributed evenly across incoming and outgoing channels.

([source](../../raw/api/api-docs/api/faraday/faraday-server/channel-insights.md))

## CloseReport

Get a channel close report for a specific channel.

```
rpc CloseReport (CloseReportRequest) returns (CloseReportResponse);
```

- REST: `GET /v1/faraday/closereport`
- Request: `frdrpc.CloseReportRequest`, with `channel_point`, the funding outpoint of the channel, formatted txid:outpoint.
- Response: `frdrpc.CloseReportResponse`, with `channel_point`, `channel_initiator` (true if we opened the channel), `close_type`, `close_txid`, `open_fee` and `close_fee`. `open_fee` and `close_fee` are in satoshis and are zero if the remote party paid.

([source](../../raw/api/api-docs/api/faraday/faraday-server/close-report.md))

## ExchangeRate

Get fiat prices for btc.

```
rpc ExchangeRate (ExchangeRateRequest) returns (ExchangeRateResponse);
```

- REST: `GET /v1/faraday/exchangerate`
- Request: `frdrpc.ExchangeRateRequest`, with `timestamps` (the set of timestamps for which the bitcoin price is wanted), `granularity`, `fiat_backend`, and `custom_prices` (used if the `CUSTOM` FiatBackend option is set).
- Response: `frdrpc.ExchangeRateResponse`, with `rates`, an array of `frdrpc.ExchangeRate` (`timestamp`, `btc_price`). `btc_price` is a `frdrpc.BitcoinPrice` (`price`, `price_timestamp`, `currency`) and carries its own timestamp because a price point for the exact timestamp queried is not guaranteed.
- `frdrpc.FiatBackend` values: `UNKNOWN_FIATBACKEND`, `COINCAP`, `COINDESK`, `CUSTOM`, `COINGECKO`, `BITFINEX`.
- `frdrpc.Granularity` values: `UNKNOWN_GRANULARITY`, `MINUTE`, `FIVE_MINUTES`, `FIFTEEN_MINUTES`, `THIRTY_MINUTES`, `HOUR`, `SIX_HOURS`, `TWELVE_HOURS`, `DAY`.

([source](../../raw/api/api-docs/api/faraday/faraday-server/exchange-rate.md))

## ForwardingAbility

Get forwarding ability analysis of peer pairs.

```
rpc ForwardingAbility (ForwardingAbilityRequest) returns (ForwardingAbilityResponse);
```

- REST: the page gives no REST method or path.
- Request: `frdrpc.ForwardingAbilityRequest`, with `start_time` (unix seconds, 0 means the earliest available data), `end_time` (unix seconds, 0 means the server's current time), `liquidity_floor_sat` (minimum directional liquidity in satoshis for a peer pair to count as economically forwardable; 0 selects the server default) and `uptime_threshold` (fraction in [0, 1]; 0 selects the server default).
- Response: `frdrpc.ForwardingAbilityResponse`, with `peers`, `entries`, `start_time`, `end_time`, `up_but_idle_bitmask` and `uptime_threshold`.
- `entries` is a sparse list of `frdrpc.ForwardingAbilityEntry` (`packed_idx`, `effective_uptime_s`, `forwarded_msat`, `fee_msat`, `forwards`); an entry is present only for a pair that carried at least one forward. `packed_idx` is `(in << 16) | out`, indexing into `peers`.
- `up_but_idle_bitmask` is a packed bitmask over the n*n ordered peer pairs; the bit at index in*n+out is set when the pair held at least the `uptime_threshold` fraction of effective uptime but carried no forward. A pair neither listed in `entries` nor flagged had sub-threshold uptime and no forwards.
- If no pair meets the threshold the server returns a FailedPrecondition error.

([source](../../raw/api/api-docs/api/faraday/faraday-server/forwarding-ability.md))

## GetChannelEvents

Get a list of channel events that occurred for a given channel.

```
rpc GetChannelEvents (ChannelEventsRequest) returns (ChannelEventsResponse);
```

- REST: `POST /v1/faraday/getchannelevents`
- Request: `frdrpc.ChannelEventsRequest`, with `chan_point` (formatted txid:outpoint), `start_time` (inclusive, Unix seconds, zero means no lower bound), `end_time` (exclusive, Unix seconds, zero means the server's current time), `max_events` (zero uses the server default; values above the server's hard cap are clamped) and `last_id` (pagination cursor; pass zero on the first call).
- Response: `frdrpc.ChannelEventsResponse`, with `events`, `last_id` and `has_more`. Callers should keep paginating until `has_more` is false.
- Each `frdrpc.ChannelEvent` has `timestamp`, `event_type`, `local_balance`, `remote_balance` (both in sat) and `id`.
- `frdrpc.ChannelEventType` values: `CHAN_EVENT_UNKNOWN`, `CHAN_EVENT_ONLINE`, `CHAN_EVENT_OFFLINE`, `CHAN_EVENT_UPDATE`.

([source](../../raw/api/api-docs/api/faraday/faraday-server/get-channel-events.md))

## NodeAudit

Get a report of your node's activity over a period.

```
rpc NodeAudit (NodeAuditRequest) returns (NodeAuditResponse);
```

- REST: `GET /v1/faraday/nodeaudit`
- Request: `frdrpc.NodeAuditRequest`, with `start_time` (unix time, inclusive), `end_time` (unix time, exclusive), `disable_fiat` (if set, fiat values display as 0), `granularity`, `custom_categories`, `fiat_backend` and `custom_prices`.
- `custom_categories` is an array of `frdrpc.CustomCategory` (`name`, `on_chain`, `off_chain`, `label_patterns`). `label_patterns` are regular expressions matched against the label of on chain transactions and the memo of off chain receipts; at present there is no way to match forwards or off chain payments. The expressions must be unique across custom categories.
- Response: `frdrpc.NodeAuditResponse`, with `reports`, an array of `frdrpc.ReportEntry` (`timestamp`, `on_chain`, `amount`, `credit`, `asset`, `type`, `custom_category`, `txid`, `fiat`, `reference`, `note`, `btc_price`). `amount` is expressed in millisatoshis.
- `frdrpc.EntryType` values: `UNKNOWN`, `LOCAL_CHANNEL_OPEN`, `REMOTE_CHANNEL_OPEN`, `CHANNEL_OPEN_FEE`, `CHANNEL_CLOSE`, `RECEIPT`, `PAYMENT`, `FEE`, `CIRCULAR_RECEIPT`, `FORWARD`, `FORWARD_FEE`, `CIRCULAR_PAYMENT`, `CIRCULAR_FEE`, `SWEEP`, `SWEEP_FEE`, `CHANNEL_CLOSE_FEE`.

([source](../../raw/api/api-docs/api/faraday/faraday-server/node-audit.md))

## OutlierRecommendations

Get close recommendations for currently open channels based on whether it is an outlier.

```
rpc OutlierRecommendations (OutlierRecommendationsRequest) returns (CloseRecommendationsResponse);
```

- REST: `GET /v1/faraday/outliers/{rec_request.metric}`
- Request: `frdrpc.OutlierRecommendationsRequest`, with `rec_request` (a `frdrpc.CloseRecommendationRequest` with `minimum_monitored` and `metric`) and `outlier_multiplier`.
- `outlier_multiplier` is the number of inter-quartile ranges a value needs to be beneath the lower quartile or above the upper quartile to be considered an outlier. Recommended values are 1.5 for aggressive recommendations and 3 for conservative recommendations.
- `frdrpc.CloseRecommendationRequest.Metric` values: `UNKNOWN`, `UPTIME`, `REVENUE`, `INCOMING_VOLUME`, `OUTGOING_VOLUME`, `TOTAL_VOLUME`.
- Response: `frdrpc.CloseRecommendationsResponse`, with `total_channels`, `considered_channels` and `recommendations`, an array of `frdrpc.Recommendation` (`chan_point`, `value`, `recommend_close`). A channel absent from `recommendations` was not considered because it is private or has not been monitored for long enough.

([source](../../raw/api/api-docs/api/faraday/faraday-server/outlier-recommendations.md))

## RevenueReport

Get a pairwise revenue report for a channel.

```
rpc RevenueReport (RevenueReportRequest) returns (RevenueReportResponse);
```

- REST: `GET /v1/faraday/revenue`
- Request: `frdrpc.RevenueReportRequest`, with `chan_points` (format fundingTxID:outpoint; if empty, the report is generated for all open and closed channels), `start_time` and `end_time` (unix epoch offset in seconds).
- Response: `frdrpc.RevenueReportResponse`, with `reports`, an array of `frdrpc.RevenueReport` (`target_channel`, `pair_reports`).
- `pair_reports` maps the channel point of a peer to a `frdrpc.PairReport` with `amount_outgoing_msat`, `fees_outgoing_msat`, `amount_incoming_msat` and `fees_incoming_msat`.

([source](../../raw/api/api-docs/api/faraday/faraday-server/revenue-report.md))

## ThresholdRecommendations

Get close recommendations for currently open channels based whether they are below a set threshold.

```
rpc ThresholdRecommendations (ThresholdRecommendationsRequest) returns (CloseRecommendationsResponse);
```

- REST: `GET /v1/faraday/threshold/{rec_request.metric}`
- Request: `frdrpc.ThresholdRecommendationsRequest`, with `rec_request` (a `frdrpc.CloseRecommendationRequest` with `minimum_monitored` and `metric`) and `threshold_value`.
- `threshold_value` is, for uptime, the ratio of uptime to observed lifetime beneath which channels will be recommended for closure; for revenue, incoming volume, outgoing volume and total volume it is a per block value, so that channels that have been open for different periods of time can be compared.
- Response: `frdrpc.CloseRecommendationsResponse`, the same message [OutlierRecommendations](#outlierrecommendations) returns.

([source](../../raw/api/api-docs/api/faraday/faraday-server/threshold-recommendations.md))

## Conflicts

- REST port. The API overview says the code samples assume REST connections on port `8082` ([source](../../raw/api/api-docs/api/faraday.md)); the example requests on the RPC pages use port 8466, for example `http://localhost:8466/v1/faraday/insights` ([source](../../raw/api/api-docs/api/faraday/faraday-server/channel-insights.md)).
- Metric options. The description of `metric` in `frdrpc.CloseRecommendationRequest` names two available options, Uptime and Revenue, while the `frdrpc.CloseRecommendationRequest.Metric` enum on the same page lists `UPTIME`, `REVENUE`, `INCOMING_VOLUME`, `OUTGOING_VOLUME` and `TOTAL_VOLUME` ([source](../../raw/api/api-docs/api/faraday/faraday-server/threshold-recommendations.md)).
