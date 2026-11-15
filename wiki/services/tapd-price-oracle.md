---
title: taproot-assets price-oracle service
type: service
sources:
  - raw/api/api-docs/api/taproot-assets.md
  - raw/api/api-docs/api/taproot-assets/rest-endpoints.md
  - raw/api/api-docs/api/taproot-assets/price-oracle/query-asset-rates.md
  - raw/api/api-docs/api/taproot-assets/portfolio-pilot/query-asset-rates.md
updated: 2026-11-14
---

# taproot-assets price-oracle service

The price-oracle service is a gRPC service in the API reference of [[taproot-assets]]. The Taproot Assets overview page lists `priceoraclerpc/price_oracle.proto` among the `*.proto` files from which the gRPC documentation was generated, and says the reference was generated automatically against commit `14aa3fd90e6aace4d3b2cfc72a51d15ce4afd891` of the `lightninglabs/taproot-assets` repository. ([source](../../raw/api/api-docs/api/taproot-assets.md)) The "Source:" link on each RPC page of this service names `priceoraclerpc/price_oracle.proto`, and the request message on each page carries the `priceoraclerpc.` prefix. ([source](../../raw/api/api-docs/api/taproot-assets/price-oracle/query-asset-rates.md))

The reference has one RPC for this service: QueryAssetRates. ([source](../../raw/api/api-docs/api/taproot-assets/price-oracle/query-asset-rates.md))

None of these RPC pages has a REST section. ([source](../../raw/api/api-docs/api/taproot-assets/price-oracle/query-asset-rates.md))

The REST Endpoints page for Taproot Assets lists no path for a `priceoraclerpc.` RPC. ([source](../../raw/api/api-docs/api/taproot-assets/rest-endpoints.md))

The portfolio-pilot service of [[tapd-portfolio-pilot]] also has an RPC named QueryAssetRates, with its own `portfoliopilotrpc.` messages. ([source](../../raw/api/api-docs/api/taproot-assets/portfolio-pilot/query-asset-rates.md))

See also: [[tapd-rfq]], [[tapd-portfolio-pilot]], [[tapd-taproot-asset-channels]], [[tapd-rfq-guide]], [[edge-node-operation]].

## QueryAssetRates

QueryAssetRates retrieves the exchange rate between a tap asset and BTC for a specified transaction type, subject asset, and payment asset. The page says the asset rate represents the number of tap asset units per BTC. ([source](../../raw/api/api-docs/api/taproot-assets/price-oracle/query-asset-rates.md))

- gRPC: `rpc QueryAssetRates (QueryAssetRatesRequest) returns (QueryAssetRatesResponse);`
- REST: none listed on the page
- Request message: `priceoraclerpc.QueryAssetRatesRequest`
- Response message: `priceoraclerpc.QueryAssetRatesResponse`

The request fields are `transaction_type`, `subject_asset`, `subject_asset_max_amount`, `payment_asset`, `payment_asset_max_amount`, `asset_rates_hint`, `intent`, `counterparty_id`, `metadata`, `node_id` and `payment_asset_swap_amount`. ([source](../../raw/api/api-docs/api/taproot-assets/price-oracle/query-asset-rates.md))

`transaction_type` is a `TransactionType` (`PURCHASE` or `SALE`) indicating whether the transaction is a purchase or a sale. `subject_asset` is the asset to be priced for purchase or sale, and `subject_asset_max_amount` is the maximum amount of the subject asset that could be involved in the transaction. `payment_asset` is the asset used for purchasing or receiving from a sale; the page notes that an asset ID of all zeros indicates that the payment asset is BTC. `payment_asset_max_amount` is optional and considered unset if set to zero. `asset_rates_hint` is an optional suggestion of asset rates for the transaction. ([source](../../raw/api/api-docs/api/taproot-assets/price-oracle/query-asset-rates.md))

`intent` informs the price oracle about the stage of the payment flow that lead to the price rate query, and the page says it will only be set by tapd v0.7.0 and later. Its `Intent` values are `INTENT_UNSPECIFIED`, `INTENT_PAY_INVOICE_HINT`, `INTENT_PAY_INVOICE`, `INTENT_PAY_INVOICE_QUALIFY`, `INTENT_RECV_PAYMENT_HINT`, `INTENT_RECV_PAYMENT` and `INTENT_RECV_PAYMENT_QUALIFY`. The page describes `INTENT_UNSPECIFIED` as the fallback default value that should not be used in production code. ([source](../../raw/api/api-docs/api/taproot-assets/price-oracle/query-asset-rates.md))

`counterparty_id` is the 33-byte public key of the peer that is on the opposite side of the transaction; the page says it will only be set by tapd v0.7.0 and later and only if the user initiating the transaction opted in to sharing their peer ID with the price oracle. `node_id` is the 33-byte public key of the local node making the request to the price oracle; it is set by default and can be disabled via the `--experimental.rfq.priceoracledisablenodeid` configuration option. ([source](../../raw/api/api-docs/api/taproot-assets/price-oracle/query-asset-rates.md))

`metadata` is an optional text field for additional metadata about the transaction. The page says that, though not verified or enforced by tapd, the suggested format is a JSON string, that the maximum length of this field is 32'768 bytes, and that the field will only be set by tapd v0.7.0 and later. ([source](../../raw/api/api-docs/api/taproot-assets/price-oracle/query-asset-rates.md))

`payment_asset_swap_amount` is the amount of the payment asset that the requesting party actually intends to swap, excluding any routing fee budget. For a pay-invoice flow this is the invoice amount, while `payment_asset_max_amount` is the invoice amount plus the fee limit of the payment. The field is optional, is considered unset if set to zero, and will only be set by tapd v0.9.0 and later. ([source](../../raw/api/api-docs/api/taproot-assets/price-oracle/query-asset-rates.md))

The response fields are `ok` (a `QueryAssetRatesOkResponse`, the successful response to the query) and `error` (a `QueryAssetRatesErrResponse`, the error response to the query). `QueryAssetRatesOkResponse` has one field, `asset_rates`. `QueryAssetRatesErrResponse` has `message` and `code`, an `ErrorCode` with the values `UNSPECIFIED_ORACLE_ERROR_CODE` and `UNSUPPORTED_ASSET_ORACLE_ERROR_CODE` (the asset is not supported). ([source](../../raw/api/api-docs/api/taproot-assets/price-oracle/query-asset-rates.md))

`AssetRates` has `subjectAssetRate`, `paymentAssetRate` and `expiry_timestamp`. `subjectAssetRate` is the number of subject asset units per BTC represented as a fixed-point number, and `paymentAssetRate` is the number of payment asset units per BTC represented as a fixed-point number. When the subject or payment asset is BTC, the corresponding field should be set to 100 billion, as one BTC is equivalent to 100 billion msats. `expiry_timestamp` is the Unix timestamp in seconds after which the asset rates are no longer valid. `FixedPoint` has `coefficient` and `scale`. ([source](../../raw/api/api-docs/api/taproot-assets/price-oracle/query-asset-rates.md))

## Conflicts

The QueryAssetRates page states the unit of the rate in two ways. Its description says "The asset rate represents the number of tap asset units per BTC", and `subjectAssetRate` and `paymentAssetRate` are both described as asset units per BTC. The note on the `payment_asset` field of the same page says that when the payment asset is BTC (an asset ID of all zeros) "the asset rate will be given as milli-satoshi per asset unit". ([source](../../raw/api/api-docs/api/taproot-assets/price-oracle/query-asset-rates.md))
