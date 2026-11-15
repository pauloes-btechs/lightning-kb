---
title: lnd invoices service
type: service
sources:
  - raw/api/api-docs/api/lnd.md
  - raw/api/api-docs/api/lnd/rest-endpoints.md
  - raw/api/api-docs/api/lnd/invoices/add-hold-invoice.md
  - raw/api/api-docs/api/lnd/invoices/cancel-invoice.md
  - raw/api/api-docs/api/lnd/invoices/htlc-modifier.md
  - raw/api/api-docs/api/lnd/invoices/lookup-invoice-v2.md
  - raw/api/api-docs/api/lnd/invoices/settle-invoice.md
  - raw/api/api-docs/api/lnd/invoices/subscribe-single-invoice.md
updated: 2026-11-14
---

# lnd invoices service (Invoices)

The invoices service of [[lnd]] is documented through the RPC pages summarised below. The AddHoldInvoice page gives `invoicesrpc/invoices.proto` as its source. ([source](../../raw/api/api-docs/api/lnd/invoices/add-hold-invoice.md))

The reference was generated automatically against commit `895118ac4ec59e78b2c14f5b0d31ac6f862434bb` of the `lightningnetwork/lnd` repository. The lnd overview lists Service *Invoices* (file: `invoicesrpc/invoices.proto`) among the services currently considered experimental: they are subject to change in the future and need to be enabled with a compile-time flag to be active, and they are active in the official release binaries. ([source](../../raw/api/api-docs/api/lnd.md))

The REST endpoints page lists six `invoicesrpc` RPCs under `/v2/invoices/`: CancelInvoice, AddHoldInvoice, HtlcModifier, LookupInvoiceV2, SettleInvoice and SubscribeSingleInvoice. ([source](../../raw/api/api-docs/api/lnd/rest-endpoints.md))

See also: [[lnd-router]], [[lnd-switch]], [[lnd-lightning]], [[lnd-interceptors]], [[lnd-receiving-payments]], [[lightning-invoices]], [[htlc]].

## AddHoldInvoice

AddHoldInvoice creates a hold invoice. It ties the invoice to the hash supplied in the request. ([source](../../raw/api/api-docs/api/lnd/invoices/add-hold-invoice.md))

- gRPC: `rpc AddHoldInvoice (AddHoldInvoiceRequest) returns (AddHoldInvoiceResp);`
- REST: `POST /v2/invoices/hodl`
- Request message: `invoicesrpc.AddHoldInvoiceRequest`
- Response message: `invoicesrpc.AddHoldInvoiceResp`

Request fields:

- `memo`: an optional memo to attach along with the invoice.
- `hash`: the hash of the preimage.
- `value` and `value_msat`: the value of the invoice in satoshis or millisatoshis; the two fields are mutually exclusive.
- `description_hash`: hash (SHA-256) of a description of the payment.
- `expiry`: payment request expiry time in seconds. Default is 86400 (24 hours).
- `fallback_addr`: fallback on-chain address.
- `cltv_expiry`: delta to use for the time-lock of the CLTV extended to the final hop.
- `route_hints`: route hints that can each be individually used to assist in reaching the invoice's destination.
- `private`: whether this invoice should include routing hints for private channels.

Response fields: `payment_request`, `add_index` (the "add" index of this invoice) and `payment_addr` (the payment address of the generated invoice, also called the payment secret in specifications, e.g. BOLT 11). ([source](../../raw/api/api-docs/api/lnd/invoices/add-hold-invoice.md))

## SettleInvoice

SettleInvoice settles an accepted invoice. If the invoice is already settled, this call will succeed. ([source](../../raw/api/api-docs/api/lnd/invoices/settle-invoice.md))

- gRPC: `rpc SettleInvoice (SettleInvoiceMsg) returns (SettleInvoiceResp);`
- REST: `POST /v2/invoices/settle`
- Request message: `invoicesrpc.SettleInvoiceMsg`
- Response message: `invoicesrpc.SettleInvoiceResp` (no parameters)

The request has one field, `preimage`: the externally discovered pre-image that should be used to settle the hold invoice. ([source](../../raw/api/api-docs/api/lnd/invoices/settle-invoice.md))

## CancelInvoice

CancelInvoice cancels a currently open invoice. If the invoice is already canceled, this call will succeed. If the invoice is already settled, it will fail. ([source](../../raw/api/api-docs/api/lnd/invoices/cancel-invoice.md))

- gRPC: `rpc CancelInvoice (CancelInvoiceMsg) returns (CancelInvoiceResp);`
- REST: `POST /v2/invoices/cancel`
- Request message: `invoicesrpc.CancelInvoiceMsg`
- Response message: `invoicesrpc.CancelInvoiceResp` (no parameters)

The request has one field, `payment_hash`: the hash corresponding to the (hold) invoice to cancel. When using REST, this field must be encoded as base64. ([source](../../raw/api/api-docs/api/lnd/invoices/cancel-invoice.md))

## LookupInvoiceV2

LookupInvoiceV2 attempts to look up an invoice (the page's wording is "look up at invoice"). An invoice can be referenced using either its payment hash, payment address, or set ID. ([source](../../raw/api/api-docs/api/lnd/invoices/lookup-invoice-v2.md))

- gRPC: `rpc LookupInvoiceV2 (LookupInvoiceMsg) returns (Invoice);`
- REST: `GET /v2/invoices/lookup`
- Request message: `invoicesrpc.LookupInvoiceMsg`
- Response message: `lnrpc.Invoice`

Request fields, all placed in the REST query: `payment_hash` (when using REST, must be encoded as base64), `payment_addr`, `set_id` and `lookup_modifier`. The `invoicesrpc.LookupModifier` values are:

- `DEFAULT`: the default look up modifier, no look up behavior is changed.
- `HTLC_SET_ONLY`: when a look up is done based on a `set_id`, only the set of HTLCs related to that set ID should be returned.
- `HTLC_SET_BLANK`: when a look up is done using a `payment_addr`, no HTLCs related to the `payment_addr` should be returned.

The response is an `lnrpc.Invoice`. Its `state` field is an `lnrpc.Invoice.InvoiceState` with the values `OPEN`, `SETTLED`, `CANCELED`, `ACCEPTED` and `PENDING_SETTLE`. `PENDING_SETTLE` means an ordinary invoice released its preimage but at least one HTLC still awaits its final outcome, so its value must not yet be credited; AMP invoices do not enter this state. For a `CANCELED` ordinary invoice the page says to check `preimage_released`, because CANCELED alone does not mean the secret was never released. The `settled` and `amt_paid` fields are marked deprecated in favour of `state` and `amt_paid_sat` or `amt_paid_msat`. ([source](../../raw/api/api-docs/api/lnd/invoices/lookup-invoice-v2.md))

## SubscribeSingleInvoice

SubscribeSingleInvoice returns a uni-directional stream (server -> client) to notify the client of state transitions of the specified invoice. Initially the current invoice state is always sent out. The page marks it as a server-streaming RPC. ([source](../../raw/api/api-docs/api/lnd/invoices/subscribe-single-invoice.md))

- gRPC: `rpc SubscribeSingleInvoice (SubscribeSingleInvoiceRequest) returns (stream Invoice);`
- REST: `GET /v2/invoices/subscribe/{r_hash}`
- Request message: `invoicesrpc.SubscribeSingleInvoiceRequest`
- Response message: stream of `lnrpc.Invoice`

The request has one field, `r_hash`: the hash corresponding to the (hold) invoice to subscribe to. When using REST, this field must be encoded as base64url. ([source](../../raw/api/api-docs/api/lnd/invoices/subscribe-single-invoice.md))

## HtlcModifier

HtlcModifier is a bidirectional streaming RPC that allows a client to intercept and modify the HTLCs that attempt to settle the given invoice. The server will send HTLCs of invoices to the client and the client can modify some aspects of the HTLC in order to pass the invoice acceptance tests. ([source](../../raw/api/api-docs/api/lnd/invoices/htlc-modifier.md))

- gRPC: `rpc HtlcModifier (stream HtlcModifyResponse) returns (stream HtlcModifyRequest);`
- REST: `POST /v2/invoices/htlcmodifier`
- Message sent by the client: `invoicesrpc.HtlcModifyResponse`
- Message sent by the server: `invoicesrpc.HtlcModifyRequest`

`invoicesrpc.HtlcModifyRequest` (server to client) fields:

- `invoice`: the invoice the intercepted HTLC is attempting to settle. The HTLCs in the invoice are only HTLCs that have already been accepted or settled, not including the current intercepted HTLC.
- `exit_htlc_circuit_key`: the unique identifier of the HTLC of this intercepted HTLC, an `invoicesrpc.CircuitKey` (`chan_id`, `htlc_id`).
- `exit_htlc_amt`: the amount in milli-satoshi that the exit HTLC is attempting to pay.
- `exit_htlc_expiry`: the absolute expiry height of the exit HTLC.
- `current_height`: the current block height.
- `exit_htlc_wire_custom_records`: the wire message custom records of the exit HTLC.

`invoicesrpc.HtlcModifyResponse` (client to server) fields:

- `circuit_key`: the circuit key of the HTLC that the client wants to modify.
- `amt_paid`: the modified amount in milli-satoshi that the exit HTLC is paying. This value can be different from the actual on-chain HTLC amount, in case the HTLC carries other valuable items, as can be the case with custom channel types.
- `cancel_set`: indicates whether the HTLCs associated with the invoices should be cancelled. Setting this will ignore the `amt_paid` field.

([source](../../raw/api/api-docs/api/lnd/invoices/htlc-modifier.md))

## Conflicts

- On the LookupInvoiceV2 page, the "Source:" line of the `lnrpc.Invoice` message is labelled `lightning.proto` while its link target is `lnrpc/invoicesrpc/invoices.proto`. The page does not say which proto file defines the message. ([source](../../raw/api/api-docs/api/lnd/invoices/lookup-invoice-v2.md))
- The SubscribeSingleInvoice page has the same mismatch for `lnrpc.Invoice`. ([source](../../raw/api/api-docs/api/lnd/invoices/subscribe-single-invoice.md))
