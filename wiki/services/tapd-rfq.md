---
title: taproot-assets rfq service
type: service
sources:
  - raw/api/api-docs/api/taproot-assets.md
  - raw/api/api-docs/api/taproot-assets/rest-endpoints.md
  - raw/api/api-docs/api/taproot-assets/rfq/add-asset-buy-order.md
  - raw/api/api-docs/api/taproot-assets/rfq/add-asset-sell-order.md
  - raw/api/api-docs/api/taproot-assets/rfq/add-asset-sell-offer.md
  - raw/api/api-docs/api/taproot-assets/rfq/add-asset-buy-offer.md
  - raw/api/api-docs/api/taproot-assets/rfq/query-peer-accepted-quotes.md
  - raw/api/api-docs/api/taproot-assets/rfq/subscribe-rfq-event-ntfns.md
  - raw/api/api-docs/api/taproot-assets/rfq/forwarding-history.md
updated: 2026-11-14
---

# taproot-assets rfq service

The rfq service is a gRPC service in the API reference of [[taproot-assets]]. The Taproot Assets overview page lists `rfqrpc/rfq.proto` among the `*.proto` files from which the gRPC documentation was generated, and says the reference was generated automatically against commit `14aa3fd90e6aace4d3b2cfc72a51d15ce4afd891` of the `lightninglabs/taproot-assets` repository. ([source](../../raw/api/api-docs/api/taproot-assets.md)) The "Source:" link on each RPC page of this service names `rfqrpc/rfq.proto`, and the request message on each page carries the `rfqrpc.` prefix. ([source](../../raw/api/api-docs/api/taproot-assets/rfq/add-asset-buy-order.md), [source](../../raw/api/api-docs/api/taproot-assets/rfq/add-asset-sell-order.md), [source](../../raw/api/api-docs/api/taproot-assets/rfq/add-asset-sell-offer.md), [source](../../raw/api/api-docs/api/taproot-assets/rfq/add-asset-buy-offer.md), [source](../../raw/api/api-docs/api/taproot-assets/rfq/query-peer-accepted-quotes.md), [source](../../raw/api/api-docs/api/taproot-assets/rfq/subscribe-rfq-event-ntfns.md), [source](../../raw/api/api-docs/api/taproot-assets/rfq/forwarding-history.md))

The reference has seven RPCs for this service: AddAssetBuyOrder, AddAssetSellOrder, AddAssetSellOffer, AddAssetBuyOffer, QueryPeerAcceptedQuotes, SubscribeRfqEventNtfns, ForwardingHistory. ([source](../../raw/api/api-docs/api/taproot-assets/rfq/add-asset-buy-order.md), [source](../../raw/api/api-docs/api/taproot-assets/rfq/add-asset-sell-order.md), [source](../../raw/api/api-docs/api/taproot-assets/rfq/add-asset-sell-offer.md), [source](../../raw/api/api-docs/api/taproot-assets/rfq/add-asset-buy-offer.md), [source](../../raw/api/api-docs/api/taproot-assets/rfq/query-peer-accepted-quotes.md), [source](../../raw/api/api-docs/api/taproot-assets/rfq/subscribe-rfq-event-ntfns.md), [source](../../raw/api/api-docs/api/taproot-assets/rfq/forwarding-history.md))

Every one of these RPC pages has a REST section, and the REST Endpoints page lists the same paths under `/v1/taproot-assets/` against the `rfqrpc.` RPC names. ([source](../../raw/api/api-docs/api/taproot-assets/rest-endpoints.md), [source](../../raw/api/api-docs/api/taproot-assets/rfq/add-asset-buy-order.md), [source](../../raw/api/api-docs/api/taproot-assets/rfq/add-asset-sell-order.md), [source](../../raw/api/api-docs/api/taproot-assets/rfq/add-asset-sell-offer.md), [source](../../raw/api/api-docs/api/taproot-assets/rfq/add-asset-buy-offer.md), [source](../../raw/api/api-docs/api/taproot-assets/rfq/query-peer-accepted-quotes.md), [source](../../raw/api/api-docs/api/taproot-assets/rfq/subscribe-rfq-event-ntfns.md), [source](../../raw/api/api-docs/api/taproot-assets/rfq/forwarding-history.md))

See also: [[tapd-taproot-asset-channels]], [[tapd-price-oracle]], [[tapd-portfolio-pilot]], [[tapd-rfq-guide]], [[edge-node-operation]], [[taproot-assets-on-lightning]].

## AddAssetBuyOrder

AddAssetBuyOrder is used to add a buy order for a specific asset. If a buy order already exists for the asset, it will be updated. A buy order instructs the RFQ (Request For Quote) system to request a quote from a peer for the acquisition of an asset. ([source](../../raw/api/api-docs/api/taproot-assets/rfq/add-asset-buy-order.md))

The page gives the normal use of a buy order as follows. ([source](../../raw/api/api-docs/api/taproot-assets/rfq/add-asset-buy-order.md))

1. Alice, operating a wallet node, wants to receive a Tap asset as payment by issuing a Lightning invoice.
2. Alice has an asset channel established with Bob's edge node.
3. Before issuing the invoice, Alice needs to agree on an exchange rate with Bob, who will facilitate the asset transfer.
4. To obtain the best exchange rate, Alice creates a buy order specifying the desired asset.
5. Alice's RFQ subsystem processes the buy order and sends buy requests to relevant peers to find the best rate. In this example, Bob is the only available peer.
6. Once Bob provides a satisfactory quote, Alice accepts it.
7. Alice issues the Lightning invoice, which Charlie will pay.
8. Instead of paying Alice directly, Charlie pays Bob.
9. Bob then forwards the agreed amount of the Tap asset to Alice over their asset channel. ([source](../../raw/api/api-docs/api/taproot-assets/rfq/add-asset-buy-order.md))

- gRPC: `rpc AddAssetBuyOrder (AddAssetBuyOrderRequest) returns (AddAssetBuyOrderResponse);`
- REST: `POST /v1/taproot-assets/rfq/buyorder/asset-id/{asset_specifier.asset_id_str}`
- Request message: `rfqrpc.AddAssetBuyOrderRequest`
- Response message: `rfqrpc.AddAssetBuyOrderResponse`

The request fields are `asset_specifier`, `asset_max_amt`, `expiry`, `peer_pub_key`, `timeout_seconds`, `skip_asset_channel_check`, `price_oracle_metadata`, `asset_min_amt`, `asset_rate_limit` and `execution_policy`. `asset_max_amt` is the maximum amount of the asset that the provider must be willing to offer, `expiry` is the unix timestamp in seconds after which the order is no longer valid, and `timeout_seconds` is the number of seconds to wait for the peer to respond with an accepted quote (or a rejection). The page says `skip_asset_channel_check` shouldn't be set outside of test scenarios. ([source](../../raw/api/api-docs/api/taproot-assets/rfq/add-asset-buy-order.md))

`asset_min_amt`, if set, must be less than or equal to `asset_max_amt`; when omitted it defaults to `asset_max_amt` (full-fill expected), and it can be set explicitly to 0 to accept any partial fill. For buy orders `asset_rate_limit` is the minimum acceptable rate (asset units per BTC); if unset, no rate floor is enforced. For `execution_policy`, IOC (default) accepts any partial fill >= min threshold and FOK requires the rate to support the full max amount; the enum values are `EXECUTION_POLICY_IOC` and `EXECUTION_POLICY_FOK`. The maximum length of `price_oracle_metadata` is 32'768 bytes. ([source](../../raw/api/api-docs/api/taproot-assets/rfq/add-asset-buy-order.md))

The response fields are `accepted_quote` (a `PeerAcceptedBuyQuote`, the quote received from the peer as a response to our quote request), `invalid_quote` (an `InvalidQuoteResponse`, returned if the quote response received from the peer was invalid or insufficient) and `rejected_quote` (a `RejectedQuoteResponse`, returned if the quote request was rejected by the peer). `PeerAcceptedBuyQuote` has `peer`, `id`, `scid`, `asset_max_amount`, `ask_asset_rate`, `expiry`, `min_transportable_units`, `price_oracle_metadata`, `asset_spec` and `accepted_max_amount`. `min_transportable_units` is described as the asset unit equivalent of 354 satoshis, which is the minimum amount for an HTLC to be above the dust limit. ([source](../../raw/api/api-docs/api/taproot-assets/rfq/add-asset-buy-order.md))

## AddAssetSellOrder

AddAssetSellOrder is used to add a sell order for a specific asset. If a sell order already exists for the asset, it will be updated. ([source](../../raw/api/api-docs/api/taproot-assets/rfq/add-asset-sell-order.md))

- gRPC: `rpc AddAssetSellOrder (AddAssetSellOrderRequest) returns (AddAssetSellOrderResponse);`
- REST: `POST /v1/taproot-assets/rfq/sellorder/asset-id/{asset_specifier.asset_id_str}`
- Request message: `rfqrpc.AddAssetSellOrderRequest`
- Response message: `rfqrpc.AddAssetSellOrderResponse`

The request fields are `asset_specifier`, `payment_max_amt`, `expiry`, `peer_pub_key`, `timeout_seconds`, `skip_asset_channel_check`, `price_oracle_metadata`, `payment_min_amt`, `asset_rate_limit`, `execution_policy` and `payment_swap_amt`. `payment_max_amt` is the maximum msat amount that the responding peer must agree to pay. `payment_min_amt`, if set, must be less than or equal to `payment_max_amt`; when omitted it defaults to `payment_max_amt` (full-fill expected), and it can be set explicitly to 0 to accept any partial fill. ([source](../../raw/api/api-docs/api/taproot-assets/rfq/add-asset-sell-order.md))

For sell orders `asset_rate_limit` is the maximum acceptable rate (asset units per BTC); if unset, no rate ceiling is enforced. `payment_swap_amt` is the optional msat amount that is actually intended to be swapped, excluding any routing fee budget; if set it must be less than or equal to `payment_max_amt`, it is forwarded to the price oracle and the peer, and a value of 0 means unset. ([source](../../raw/api/api-docs/api/taproot-assets/rfq/add-asset-sell-order.md))

The response fields are `accepted_quote` (a `PeerAcceptedSellQuote`), `invalid_quote` (an `InvalidQuoteResponse`) and `rejected_quote` (a `RejectedQuoteResponse`). ([source](../../raw/api/api-docs/api/taproot-assets/rfq/add-asset-sell-order.md))

## AddAssetSellOffer

AddAssetSellOffer is used to add a sell offer for a specific asset. If a sell offer already exists for the asset, it will be updated. ([source](../../raw/api/api-docs/api/taproot-assets/rfq/add-asset-sell-offer.md))

- gRPC: `rpc AddAssetSellOffer (AddAssetSellOfferRequest) returns (AddAssetSellOfferResponse);`
- REST: `POST /v1/taproot-assets/rfq/selloffer/asset-id/{asset_specifier.asset_id_str}`
- Request message: `rfqrpc.AddAssetSellOfferRequest`
- Response message: `rfqrpc.AddAssetSellOfferResponse`

The request fields are `asset_specifier` (the subject asset) and `max_units` (the maximum amount of the asset to sell). The response has no parameters. ([source](../../raw/api/api-docs/api/taproot-assets/rfq/add-asset-sell-offer.md))

## AddAssetBuyOffer

AddAssetBuyOffer is used to add a buy offer for a specific asset. If a buy offer already exists for the asset, it will be updated. A buy offer is used by the node to selectively accept or reject incoming asset sell quote requests before price is considered. ([source](../../raw/api/api-docs/api/taproot-assets/rfq/add-asset-buy-offer.md))

- gRPC: `rpc AddAssetBuyOffer (AddAssetBuyOfferRequest) returns (AddAssetBuyOfferResponse);`
- REST: `POST /v1/taproot-assets/rfq/buyoffer/asset-id/{asset_specifier.asset_id_str}`
- Request message: `rfqrpc.AddAssetBuyOfferRequest`
- Response message: `rfqrpc.AddAssetBuyOfferResponse`

The request fields are `asset_specifier` (the subject asset) and `max_units` (the maximum amount of the asset to buy). The response has no parameters. ([source](../../raw/api/api-docs/api/taproot-assets/rfq/add-asset-buy-offer.md))

## QueryPeerAcceptedQuotes

QueryPeerAcceptedQuotes is used to query for quotes that were requested by our node and have been accepted our peers. ([source](../../raw/api/api-docs/api/taproot-assets/rfq/query-peer-accepted-quotes.md))

- gRPC: `rpc QueryPeerAcceptedQuotes (QueryPeerAcceptedQuotesRequest) returns (QueryPeerAcceptedQuotesResponse);`
- REST: `GET /v1/taproot-assets/rfq/quotes/peeraccepted`
- Request message: `rfqrpc.QueryPeerAcceptedQuotesRequest`
- Response message: `rfqrpc.QueryPeerAcceptedQuotesResponse`

The request has no parameters. The response fields are `buy_quotes` (a list of `PeerAcceptedBuyQuote`) and `sell_quotes` (a list of `PeerAcceptedSellQuote`). `PeerAcceptedBuyQuote` has `peer`, `id`, `scid`, `asset_max_amount`, `ask_asset_rate`, `expiry`, `min_transportable_units`, `price_oracle_metadata`, `asset_spec` and `accepted_max_amount`. `PeerAcceptedSellQuote` has `peer`, `id`, `scid`, `asset_amount`, `bid_asset_rate`, `expiry`, `min_transportable_msat`, `price_oracle_metadata`, `asset_spec` and `accepted_max_amount`. `min_transportable_msat` is described as the base amount of 354,000 milli-satoshi (the minimum amount for a non-dust HTLC) plus the equivalent of one asset unit in milli-satoshis. ([source](../../raw/api/api-docs/api/taproot-assets/rfq/query-peer-accepted-quotes.md))

## SubscribeRfqEventNtfns

SubscribeRfqEventNtfns is used to subscribe to RFQ events. The page marks it as a server-streaming RPC. ([source](../../raw/api/api-docs/api/taproot-assets/rfq/subscribe-rfq-event-ntfns.md))

- gRPC: `rpc SubscribeRfqEventNtfns (SubscribeRfqEventNtfnsRequest) returns (stream RfqEvent);`
- REST: `POST /v1/taproot-assets/rfq/ntfs`
- Request message: `rfqrpc.SubscribeRfqEventNtfnsRequest`
- Response message: `rfqrpc.RfqEvent`

The request has no parameters. `RfqEvent` has the fields `peer_accepted_buy_quote` (a `PeerAcceptedBuyQuoteEvent`, emitted when a peer accepted (incoming) asset buy quote message is received), `peer_accepted_sell_quote` (a `PeerAcceptedSellQuoteEvent`, emitted when a peer accepted (incoming) asset sell quote message is received) and `accept_htlc` (an `AcceptHtlcEvent`, sent when a HTLC is accepted by the RFQ service). `AcceptHtlcEvent` has `timestamp` (Unix timestamp in microseconds) and `scid`. ([source](../../raw/api/api-docs/api/taproot-assets/rfq/subscribe-rfq-event-ntfns.md))

## ForwardingHistory

ForwardingHistory is used to query for completed asset forwarding events. These are historical records of HTLCs that were settled successfully. ([source](../../raw/api/api-docs/api/taproot-assets/rfq/forwarding-history.md))

- gRPC: `rpc ForwardingHistory (ForwardingHistoryRequest) returns (ForwardingHistoryResponse);`
- REST: `GET /v1/taproot-assets/rfq/forwardinghistory`
- Request message: `rfqrpc.ForwardingHistoryRequest`
- Response message: `rfqrpc.ForwardingHistoryResponse`

The request fields are `min_timestamp`, `max_timestamp`, `peer`, `asset_specifier`, `limit` and `offset`; their REST placement is `query`. `min_timestamp` and `max_timestamp` are Unix timestamps in seconds bounding when the forwarding events settled, with no bound if not set. `peer` and `asset_specifier` are optional filters, `limit` is the maximum number of records to return and `offset` is the number of records to skip for pagination. ([source](../../raw/api/api-docs/api/taproot-assets/rfq/forwarding-history.md))

The response fields are `forwards` (a list of `ForwardingEvent`) and `total_count`, the total number of forwards matching the filter before pagination is applied. `ForwardingEvent` has `rfq_id`, `chan_id_in`, `chan_id_out`, `htlc_id`, `opened_at`, `settled_at`, `failed_at`, `asset_amt`, `amt_in_msat`, `amt_out_msat`, `policy_type`, `peer`, `asset_spec` and `rate`. `policy_type` indicates whether this was a sale or purchase of assets from the edge node's perspective, with the `RfqPolicyType` values `RFQ_POLICY_TYPE_SALE` and `RFQ_POLICY_TYPE_PURCHASE`. ([source](../../raw/api/api-docs/api/taproot-assets/rfq/forwarding-history.md))

## Conflicts

On the SubscribeRfqEventNtfns page, the `RfqEvent` field is named `peer_accepted_sell_quote`, while the description in the same table row calls it `peer_accepted_sell_offer`. ([source](../../raw/api/api-docs/api/taproot-assets/rfq/subscribe-rfq-event-ntfns.md))
