---
title: taproot-assets portfolio-pilot service
type: service
sources:
  - raw/api/api-docs/api/taproot-assets.md
  - raw/api/api-docs/api/taproot-assets/rest-endpoints.md
  - raw/api/api-docs/api/taproot-assets/portfolio-pilot/resolve-request.md
  - raw/api/api-docs/api/taproot-assets/portfolio-pilot/verify-accept-quote.md
  - raw/api/api-docs/api/taproot-assets/portfolio-pilot/query-asset-rates.md
  - raw/api/api-docs/api/taproot-assets/price-oracle/query-asset-rates.md
updated: 2026-11-14
---

# taproot-assets portfolio-pilot service

The portfolio-pilot service is a gRPC service in the API reference of [[taproot-assets]]. The Taproot Assets overview page lists `portfoliopilotrpc/portfolio_pilot.proto` among the `*.proto` files from which the gRPC documentation was generated, and says the reference was generated automatically against commit `14aa3fd90e6aace4d3b2cfc72a51d15ce4afd891` of the `lightninglabs/taproot-assets` repository. ([source](../../raw/api/api-docs/api/taproot-assets.md)) The "Source:" link on each RPC page of this service names `portfoliopilotrpc/portfolio_pilot.proto`, and the request message on each page carries the `portfoliopilotrpc.` prefix. ([source](../../raw/api/api-docs/api/taproot-assets/portfolio-pilot/resolve-request.md), [source](../../raw/api/api-docs/api/taproot-assets/portfolio-pilot/verify-accept-quote.md), [source](../../raw/api/api-docs/api/taproot-assets/portfolio-pilot/query-asset-rates.md))

The reference has three RPCs for this service: ResolveRequest, VerifyAcceptQuote, QueryAssetRates. ([source](../../raw/api/api-docs/api/taproot-assets/portfolio-pilot/resolve-request.md), [source](../../raw/api/api-docs/api/taproot-assets/portfolio-pilot/verify-accept-quote.md), [source](../../raw/api/api-docs/api/taproot-assets/portfolio-pilot/query-asset-rates.md))

None of these RPC pages has a REST section. ([source](../../raw/api/api-docs/api/taproot-assets/portfolio-pilot/resolve-request.md), [source](../../raw/api/api-docs/api/taproot-assets/portfolio-pilot/verify-accept-quote.md), [source](../../raw/api/api-docs/api/taproot-assets/portfolio-pilot/query-asset-rates.md))

The REST Endpoints page for Taproot Assets lists no path for a `portfoliopilotrpc.` RPC. ([source](../../raw/api/api-docs/api/taproot-assets/rest-endpoints.md))

The price-oracle service of [[tapd-price-oracle]] also has an RPC named QueryAssetRates, with the signature `rpc QueryAssetRates (QueryAssetRatesRequest) returns (QueryAssetRatesResponse);` and its own `priceoraclerpc.` messages. ([source](../../raw/api/api-docs/api/taproot-assets/price-oracle/query-asset-rates.md))

See also: [[tapd-rfq]], [[tapd-price-oracle]], [[tapd-taproot-asset-channels]], [[tapd-rfq-guide]], [[edge-node-operation]].

## ResolveRequest

ResolveRequest resolves a quote request by returning either an accepted asset rate or a rejection reason. ([source](../../raw/api/api-docs/api/taproot-assets/portfolio-pilot/resolve-request.md))

- gRPC: `rpc ResolveRequest (ResolveRequestRequest) returns (ResolveRequestResponse);`
- REST: none listed on the page
- Request message: `portfoliopilotrpc.ResolveRequestRequest`
- Response message: `portfoliopilotrpc.ResolveRequestResponse`

The request fields are `buy_request` (a `BuyRequest`, a request to buy the subject asset) and `sell_request` (a `SellRequest`, a request to sell the subject asset). `BuyRequest` has `asset_specifier`, `asset_max_amount`, `asset_rate_hint`, `price_oracle_metadata`, `peer_id`, `asset_min_amount`, `asset_rate_limit` and `execution_policy`. `SellRequest` has `asset_specifier`, `payment_max_amount`, `asset_rate_hint`, `price_oracle_metadata`, `peer_id`, `payment_min_amount`, `asset_rate_limit`, `execution_policy` and `payment_swap_amount`. ([source](../../raw/api/api-docs/api/taproot-assets/portfolio-pilot/resolve-request.md))

`asset_rate_limit` is an optional minimum acceptable rate (asset units per BTC) on a `BuyRequest` and an optional maximum acceptable rate (asset units per BTC) on a `SellRequest`. The `ExecutionPolicy` values are `EXECUTION_POLICY_IOC` (Immediate-Or-Cancel, accepts any partial fill; this is the default policy) and `EXECUTION_POLICY_FOK` (Fill-Or-Kill, requires the accepted rate to satisfy the full requested amount). ([source](../../raw/api/api-docs/api/taproot-assets/portfolio-pilot/resolve-request.md))

The response fields are `accept` (an `AssetRate`, the accepted asset rate for the request), `reject` (a `RejectErr` with `code` and `message`) and `accepted_max_amount`, an optional fill quantity that caps the amount the responder is willing to accept. `accepted_max_amount` is only meaningful when `accept` is set; 0 means no fill cap (full request max), and the unit is asset units for a buy request and msat for a sell request. ([source](../../raw/api/api-docs/api/taproot-assets/portfolio-pilot/resolve-request.md))

The `RejectCode` values are `REJECT_CODE_UNSPECIFIED`, `REJECT_CODE_PRICE_ORACLE_UNAVAILABLE`, `REJECT_CODE_MIN_FILL_NOT_MET`, `REJECT_CODE_PRICE_BOUND_MISS`, `REJECT_CODE_FOK_NOT_VIABLE` and `REJECT_CODE_FILL_EXCEEDS_MAX`. ([source](../../raw/api/api-docs/api/taproot-assets/portfolio-pilot/resolve-request.md))

## VerifyAcceptQuote

VerifyAcceptQuote verifies that an accepted quote from a peer meets acceptable conditions. ([source](../../raw/api/api-docs/api/taproot-assets/portfolio-pilot/verify-accept-quote.md))

- gRPC: `rpc VerifyAcceptQuote (VerifyAcceptQuoteRequest) returns (VerifyAcceptQuoteResponse);`
- REST: none listed on the page
- Request message: `portfoliopilotrpc.VerifyAcceptQuoteRequest`
- Response message: `portfoliopilotrpc.VerifyAcceptQuoteResponse`

The request has one field, `accept`, an `AcceptedQuote` with `peer_id` (the 33-byte public key of the accepting peer), `accepted_rate`, `buy_request`, `sell_request` and `accepted_max_amount`. The response has one field, `status`, a `QuoteRespStatus`. ([source](../../raw/api/api-docs/api/taproot-assets/portfolio-pilot/verify-accept-quote.md))

The `QuoteRespStatus` values are `INVALID_ASSET_RATES`, `INVALID_EXPIRY`, `PRICE_ORACLE_QUERY_ERR`, `PORTFOLIO_PILOT_ERR`, `VALID_ACCEPT_QUOTE`, `MIN_FILL_NOT_MET`, `RATE_BOUND_MISS`, `FOK_NOT_VIABLE` and `FILL_EXCEEDS_MAX`. `VALID_ACCEPT_QUOTE` indicates that the accepted quote passed all validation checks successfully. ([source](../../raw/api/api-docs/api/taproot-assets/portfolio-pilot/verify-accept-quote.md))

## QueryAssetRates

QueryAssetRates returns current asset rate information for a given asset and direction. The page says this can be used for rate discovery, outgoing RFQ request construction, or general pricing information. ([source](../../raw/api/api-docs/api/taproot-assets/portfolio-pilot/query-asset-rates.md))

- gRPC: `rpc QueryAssetRates (QueryAssetRatesRequest) returns (QueryAssetRatesResponse);`
- REST: none listed on the page
- Request message: `portfoliopilotrpc.QueryAssetRatesRequest`
- Response message: `portfoliopilotrpc.QueryAssetRatesResponse`

The request fields are `asset_specifier`, `direction`, `intent`, `asset_amount`, `payment_amount`, `asset_rate_hint`, `price_oracle_metadata`, `peer_id`, `expiry_timestamp` and `payment_swap_amount`. `direction` is an `AssetTransferDirection` (`ASSET_TRANSFER_DIRECTION_UNSPECIFIED`, `ASSET_TRANSFER_DIRECTION_BUY`, `ASSET_TRANSFER_DIRECTION_SELL`). `asset_amount`, `payment_amount`, `expiry_timestamp` and `payment_swap_amount` are optional and considered unset when set to zero; `payment_amount` is in msat. ([source](../../raw/api/api-docs/api/taproot-assets/portfolio-pilot/query-asset-rates.md))

`intent` is an `Intent` with the values `INTENT_UNSPECIFIED`, `INTENT_PAY_INVOICE_HINT`, `INTENT_PAY_INVOICE`, `INTENT_PAY_INVOICE_QUALIFY`, `INTENT_RECV_PAYMENT_HINT`, `INTENT_RECV_PAYMENT` and `INTENT_RECV_PAYMENT_QUALIFY`. ([source](../../raw/api/api-docs/api/taproot-assets/portfolio-pilot/query-asset-rates.md))

The response has one field, `asset_rate`, an `AssetRate` with `rate` (the asset to BTC conversion rate represented as a fixed-point number, a `FixedPoint` with `coefficient` and `scale`) and `expiry_timestamp` (the Unix timestamp in seconds after which the rate is no longer valid). ([source](../../raw/api/api-docs/api/taproot-assets/portfolio-pilot/query-asset-rates.md))
