---
title: taproot-assets taproot-asset-channels service
type: service
sources:
  - raw/api/api-docs/api/taproot-assets.md
  - raw/api/api-docs/api/taproot-assets/rest-endpoints.md
  - raw/api/api-docs/api/taproot-assets/taproot-asset-channels/fund-channel.md
  - raw/api/api-docs/api/taproot-assets/taproot-asset-channels/encode-custom-records.md
  - raw/api/api-docs/api/taproot-assets/taproot-asset-channels/send-payment.md
  - raw/api/api-docs/api/taproot-assets/taproot-asset-channels/add-invoice.md
  - raw/api/api-docs/api/taproot-assets/taproot-asset-channels/decode-asset-pay-req.md
  - raw/api/api-docs/api/taproot-assets/taproot-asset-channels/list-invoices.md
  - raw/api/api-docs/api/taproot-assets/taproot-asset-channels/list-payments.md
  - raw/api/api-docs/api/taproot-assets/taproot-asset-channels/subscribe-invoices.md
  - raw/api/api-docs/api/taproot-assets/taproot-asset-channels/subscribe-payments.md
  - raw/api/api-docs/api/taproot-assets/taproot-asset-channels/track-payment.md
updated: 2026-11-14
---

# taproot-assets taproot-asset-channels service

The taproot-asset-channels service is a gRPC service in the API reference of [[taproot-assets]]. The Taproot Assets overview page lists `tapchannelrpc/tapchannel.proto` among the `*.proto` files from which the gRPC documentation was generated, and says the reference was generated automatically against commit `14aa3fd90e6aace4d3b2cfc72a51d15ce4afd891` of the `lightninglabs/taproot-assets` repository. ([source](../../raw/api/api-docs/api/taproot-assets.md)) The "Source:" link on each RPC page of this service names `tapchannelrpc/tapchannel.proto`, and the request message on each page carries the `tapchannelrpc.` prefix. ([source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/fund-channel.md), [source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/encode-custom-records.md), [source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/send-payment.md), [source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/add-invoice.md), [source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/decode-asset-pay-req.md), [source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/list-invoices.md), [source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/list-payments.md), [source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/subscribe-invoices.md), [source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/subscribe-payments.md), [source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/track-payment.md))

The reference has ten RPCs for this service: FundChannel, EncodeCustomRecords, SendPayment, AddInvoice, DecodeAssetPayReq, ListInvoices, ListPayments, SubscribeInvoices, SubscribePayments, TrackPayment. ([source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/fund-channel.md), [source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/encode-custom-records.md), [source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/send-payment.md), [source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/add-invoice.md), [source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/decode-asset-pay-req.md), [source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/list-invoices.md), [source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/list-payments.md), [source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/subscribe-invoices.md), [source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/subscribe-payments.md), [source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/track-payment.md))

Every one of these RPC pages has a REST section, and the REST Endpoints page lists the same paths under `/v1/taproot-assets/` against the `tapchannelrpc.` RPC names. ([source](../../raw/api/api-docs/api/taproot-assets/rest-endpoints.md), [source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/fund-channel.md), [source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/encode-custom-records.md), [source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/send-payment.md), [source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/add-invoice.md), [source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/decode-asset-pay-req.md), [source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/list-invoices.md), [source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/list-payments.md), [source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/subscribe-invoices.md), [source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/subscribe-payments.md), [source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/track-payment.md))

See also: [[tapd-rfq]], [[tapd-price-oracle]], [[tapd-portfolio-pilot]], [[tapd-taproot-assets]], [[taproot-assets-channels-guide]], [[taproot-assets-on-lightning]], [[edge-node-operation]].

## FundChannel

FundChannel initiates the channel funding negotiation with a peer for the creation of a channel that contains a specified amount of a given asset. ([source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/fund-channel.md))

- gRPC: `rpc FundChannel (FundChannelRequest) returns (FundChannelResponse);`
- REST: `POST /v1/taproot-assets/channels/fund`
- Request message: `tapchannelrpc.FundChannelRequest`
- Response message: `tapchannelrpc.FundChannelResponse`

The request fields are `asset_amount`, `asset_id`, `peer_pubkey`, `fee_rate_sat_per_vbyte`, `push_sat` and `group_key`. `asset_amount` is the asset amount to fund the channel with; the page says the BTC amount is fixed and cannot be customized (for now). `peer_pubkey` is the public key of the peer to open the channel with, and the node must already be connected to this peer. `fee_rate_sat_per_vbyte` is the channel funding fee rate in sat/vByte. `push_sat` is the number of satoshis to give the remote side as part of the initial commitment state. `group_key` can be used instead of `asset_id` to allow assets from a fungible group to be used for the channel funding instead of just assets from a single minting tranche. ([source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/fund-channel.md))

The response fields are `txid` (the channel funding transaction ID) and `output_index` (the index of the channel funding output in the funding transaction). ([source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/fund-channel.md))

## EncodeCustomRecords

The page marks this RPC as deprecated and says it will be removed in a future version. EncodeCustomRecords allows RPC users to encode Taproot Asset channel related data into the TLV format that is used in the custom records of the lnd payment or other channel related RPCs. The RPC is completely stateless and does not perform any checks on the data provided, other than pure format validation. ([source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/encode-custom-records.md))

- gRPC: `rpc EncodeCustomRecords (EncodeCustomRecordsRequest) returns (EncodeCustomRecordsResponse);`
- REST: `POST /v1/taproot-assets/channels/encode-custom-data`
- Request message: `tapchannelrpc.EncodeCustomRecordsRequest`
- Response message: `tapchannelrpc.EncodeCustomRecordsResponse`

The request has one field, `router_send_payment`, a `RouterSendPaymentData` with `asset_amounts` (the string encoded asset ID to amount mapping) and `rfq_id` (the RFQ ID to use for the payment, which can be empty for a direct keysend payment that doesn't involve any conversion). The response has one field, `custom_records`, the encoded custom records in TLV format. ([source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/encode-custom-records.md))

## SendPayment

SendPayment is a wrapper around lnd's routerrpc.SendPaymentV2 RPC method with asset specific parameters. It allows RPC users to send asset keysend payments (direct payments) or payments to an invoice with a specified asset amount. The page marks it as a server-streaming RPC. ([source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/send-payment.md))

- gRPC: `rpc SendPayment (SendPaymentRequest) returns (stream SendPaymentResponse);`
- REST: `POST /v1/taproot-assets/channels/send-payment`
- Request message: `tapchannelrpc.SendPaymentRequest`
- Response message: `tapchannelrpc.SendPaymentResponse`

The request fields are `asset_id`, `asset_amount`, `peer_pubkey`, `payment_request`, `rfq_id`, `allow_overpay`, `group_key` and `price_oracle_metadata`. `asset_id` and `group_key` are mutually exclusive. `asset_amount` is the asset amount to send in a keysend payment; it is ignored for invoice payments, as the asset amount is negotiated through RFQ with the peer, depending on the invoice amount. If `peer_pubkey` is set, only a quote with this peer may be negotiated to carry out the payment. ([source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/send-payment.md))

`payment_request` is the full lnd payment request to send, whose fields behave the same way as they do for lnd's routerrpc.SendPaymentV2 RPC method. To send a keysend payment, `payment_request.dest_custom_records` must contain a valid keysend record (key 5482373484 and a 32-byte preimage that corresponds to the payment hash). If `rfq_id` is set, the payment is immediately dispatched, skipping the rfq negotiation phase. ([source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/send-payment.md))

By default, a payment of a small invoice that is below the amount that always needs to be sent out to carry a single asset unit is rejected; if `allow_overpay` is set, the payment is allowed to proceed even if it is uneconomical. The maximum length of `price_oracle_metadata` is 32'768 bytes. ([source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/send-payment.md))

The response fields are `accepted_sell_order`, `accepted_sell_orders` and `payment_result`. `accepted_sell_order` is marked deprecated and now only contains the first quote that was negotiated; the page says to use `accepted_sell_orders` (an `AcceptedSellQuotes`, a list of `PeerAcceptedSellQuote`) to retrieve all of them. `payment_result` is the payment result of a single payment attempt, and multiple attempts may be returned per payment request until either the payment succeeds or the payment times out. ([source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/send-payment.md))

## AddInvoice

AddInvoice is a wrapper around lnd's lnrpc.AddInvoice method with asset specific parameters. It allows RPC users to create invoices that correspond to the specified asset amount. If a peer pubkey is specified, then only that peer will be used for RFQ negotiations. If none is specified then RFQ quotes for all peers with suitable asset channels will be created. ([source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/add-invoice.md))

- gRPC: `rpc AddInvoice (AddInvoiceRequest) returns (AddInvoiceResponse);`
- REST: `POST /v1/taproot-assets/channels/invoice`
- Request message: `tapchannelrpc.AddInvoiceRequest`
- Response message: `tapchannelrpc.AddInvoiceResponse`

The request fields are `asset_id`, `asset_amount`, `peer_pubkey`, `invoice_request`, `hodl_invoice`, `group_key`, `price_oracle_metadata`, `asset_min_amt`, `asset_rate_limit` and `execution_policy`. `asset_id` and `group_key` are mutually exclusive; if `group_key` is set, any asset that belongs to this group may be accepted to settle the invoice. ([source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/add-invoice.md))

`invoice_request` is the full lnd invoice request to send. Only one of `asset_amount`/`value`/`value_msat` may be set to dictate the value of the invoice. When using `asset_amount`, the `value`/`value_msat` fields will be overwritten by the satoshi (or milli-satoshi) equivalent of the asset amount, after negotiating a quote with a peer that supports the given asset ID. If `value`/`value_msat` are used, assets are still received, but they will exactly evaluate to the defined amount in sats/msats. ([source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/add-invoice.md))

If `hodl_invoice` is set, the invoice created is a hodl invoice, which won't be settled automatically; users will need to use the invoicesrpc.SettleInvoice call to manually settle it. `HodlInvoice` has one field, `payment_hash`. `asset_min_amt`, `asset_rate_limit` and `execution_policy` are forwarded to AddAssetBuyOrder (see [[tapd-rfq]]). ([source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/add-invoice.md))

The response fields are `accepted_buy_quote` (a `PeerAcceptedBuyQuote`, the quote for the purchase of assets that was accepted by the peer) and `invoice_result` (the result of the invoice creation). ([source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/add-invoice.md))

## DecodeAssetPayReq

DecodeAssetPayReq is similar to lnd's lnrpc.DecodePayReq, but it accepts an asset ID or group key and returns the invoice amount expressed in asset units along side the normal information. ([source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/decode-asset-pay-req.md))

- gRPC: `rpc DecodeAssetPayReq (AssetPayReq) returns (AssetPayReqResponse);`
- REST: `POST /v1/taproot-assets/channels/invoice/decode`
- Request message: `tapchannelrpc.AssetPayReq`
- Response message: `tapchannelrpc.AssetPayReqResponse`

The request fields are `asset_id`, `pay_req_string`, `group_key` and `price_oracle_metadata`; `asset_id` and `group_key` are mutually exclusive. The response fields are `asset_amount` (the invoice amount, expressed in asset units), `decimal_display`, `asset_group`, `genesis_info` (always populated) and `pay_req` (the normal decoded payment request). ([source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/decode-asset-pay-req.md))

## ListInvoices

ListInvoices is a wrapper around lnd's lnrpc.ListInvoices method that only returns invoices that involve at least one Taproot Asset. The full lnd invoice is returned along with the decoded asset amounts that the invoice's HTLCs carry, so that callers don't need to parse the custom channel data themselves. ([source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/list-invoices.md))

- gRPC: `rpc ListInvoices (ListInvoicesRequest) returns (ListInvoicesResponse);`
- REST: `POST /v1/taproot-assets/channels/invoices`
- Request message: `tapchannelrpc.ListInvoicesRequest`
- Response message: `tapchannelrpc.ListInvoicesResponse`

The request has one field, `request`, the standard lnd invoice listing request. Pagination is performed by lnd over all invoices; the returned set is then filtered down to only those that involve assets, so a page may contain fewer asset invoices than the requested maximum. The response fields are `invoices` (a list of `AssetInvoice`), `last_index_offset` and `first_index_offset`. `AssetInvoice` has `invoice` and `asset_amounts`, the latter aggregated per asset ID across all of the invoice's HTLCs. `AssetAmount` has `asset_id`, `amount` and `group_key`. ([source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/list-invoices.md))

## ListPayments

ListPayments is a wrapper around lnd's lnrpc.ListPayments method that only returns payments that involve at least one Taproot Asset. The full lnd payment is returned along with the decoded asset amounts that the payment's HTLCs carry. ([source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/list-payments.md))

- gRPC: `rpc ListPayments (ListPaymentsRequest) returns (ListPaymentsResponse);`
- REST: `POST /v1/taproot-assets/channels/payments`
- Request message: `tapchannelrpc.ListPaymentsRequest`
- Response message: `tapchannelrpc.ListPaymentsResponse`

The request has one field, `request`, the standard lnd payment listing request. Pagination is performed by lnd over all payments; the returned set is then filtered down to only those that involve assets, so a page may contain fewer asset payments than the requested maximum. The response fields are `payments` (a list of `AssetPayment`), `first_index_offset` and `last_index_offset`. `AssetPayment` has `payment` and `asset_amounts`, the latter aggregated per asset ID across all non-failed HTLC attempts. ([source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/list-payments.md))

## SubscribeInvoices

SubscribeInvoices is a wrapper around lnd's lnrpc.SubscribeInvoices method that only streams invoices that involve at least one Taproot Asset. The page marks it as a server-streaming RPC. ([source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/subscribe-invoices.md))

- gRPC: `rpc SubscribeInvoices (SubscribeInvoicesRequest) returns (stream AssetInvoice);`
- REST: `POST /v1/taproot-assets/channels/invoices/subscribe`
- Request message: `tapchannelrpc.SubscribeInvoicesRequest`
- Response message: `tapchannelrpc.AssetInvoice`

The request has one field, `request`, the standard lnd invoice subscription request. Invoice index replay is performed by lnd over all invoices; the returned stream is then filtered down to only those that involve assets. Each streamed `AssetInvoice` has `invoice` and `asset_amounts`. ([source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/subscribe-invoices.md))

## SubscribePayments

SubscribePayments is a wrapper around lnd's routerrpc.TrackPayments method that only streams payment updates that involve at least one Taproot Asset. The page marks it as a server-streaming RPC. ([source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/subscribe-payments.md))

- gRPC: `rpc SubscribePayments (SubscribePaymentsRequest) returns (stream AssetPayment);`
- REST: `POST /v1/taproot-assets/channels/payments/subscribe`
- Request message: `tapchannelrpc.SubscribePaymentsRequest`
- Response message: `tapchannelrpc.AssetPayment`

The request has one field, `request`, the standard lnd payment tracking request. The payment update stream is produced by lnd over all active payments; the returned stream is then filtered down to only those that involve assets. Each streamed `AssetPayment` has `payment` and `asset_amounts`. ([source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/subscribe-payments.md))

## TrackPayment

TrackPayment is a wrapper around lnd's routerrpc.TrackPaymentV2 method that only streams payment updates that involve at least one Taproot Asset. The page marks it as a server-streaming RPC. ([source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/track-payment.md))

- gRPC: `rpc TrackPayment (TrackPaymentRequest) returns (stream AssetPayment);`
- REST: `POST /v1/taproot-assets/channels/payments/track`
- Request message: `tapchannelrpc.TrackPaymentRequest`
- Response message: `tapchannelrpc.AssetPayment`

The request has one field, `request`, the standard lnd payment tracking request. The payment update stream is produced by lnd for the requested payment; the returned stream is then filtered down to only updates that involve assets. Each streamed `AssetPayment` has `payment` and `asset_amounts`. ([source](../../raw/api/api-docs/api/taproot-assets/taproot-asset-channels/track-payment.md))
