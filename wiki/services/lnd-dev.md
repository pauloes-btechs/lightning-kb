---
title: lnd dev service
type: service
sources:
  - raw/api/api-docs/api/lnd.md
  - raw/api/api-docs/api/lnd/rest-endpoints.md
  - raw/api/api-docs/api/lnd/dev/create-offer.md
  - raw/api/api-docs/api/lnd/dev/import-graph.md
  - raw/api/api-docs/api/lnd/dev/quiesce.md
updated: 2026-11-14
---

# lnd dev service (Dev)

The Dev service of [[lnd]] is defined in `devrpc/dev.proto`, according to its RPC pages. ([source](../../raw/api/api-docs/api/lnd/dev/import-graph.md))

The lnd API overview lists `devrpc/dev.proto` among the proto files the reference was generated from, at commit `895118ac4ec59e78b2c14f5b0d31ac6f862434bb`. ([source](../../raw/api/api-docs/api/lnd.md))

The REST endpoints page lists three `devrpc` RPCs under `/v2/dev/`: CreateOffer, ImportGraph and Quiesce. ([source](../../raw/api/api-docs/api/lnd/rest-endpoints.md))

See also: [[lnd-lightning]], [[lnd-debugging-and-contributing]].

## ImportGraph

ImportGraph imports a ChannelGraph into the graph database. It should only be used for development. ([source](../../raw/api/api-docs/api/lnd/dev/import-graph.md))

- gRPC: `rpc ImportGraph (ChannelGraph) returns (ImportGraphResponse);`
- REST: `POST /v2/dev/importgraph`
- Request: `lnrpc.ChannelGraph`, fields `nodes` (`LightningNode[]`) and `edges` (`ChannelEdge[]`)
- Response: `devrpc.ImportGraphResponse` (no parameters)

([source](../../raw/api/api-docs/api/lnd/dev/import-graph.md))

## Quiesce

Quiesce instructs a channel to initiate the quiescence (stfu) protocol. The page says this RPC is for testing purposes only and that the commit that adds it will be removed once interop is confirmed. ([source](../../raw/api/api-docs/api/lnd/dev/quiesce.md))

- gRPC: `rpc Quiesce (QuiescenceRequest) returns (QuiescenceResponse);`
- REST: `POST /v2/dev/quiesce`
- Request: `devrpc.QuiescenceRequest`, field `chan_id` (an `lnrpc.ChannelPoint`: `funding_txid_bytes`, `funding_txid_str`, `output_index`)
- Response: `devrpc.QuiescenceResponse`, field `initiator` (whether this node holds the initiator role once the negotiation completes)

([source](../../raw/api/api-docs/api/lnd/dev/quiesce.md))

## CreateOffer

CreateOffer creates a new BOLT 12 offer. The offer is persisted in the offer store and the encoded offer string (lno1...) is returned. The node must run with `--protocol.bolt12-offers`. ([source](../../raw/api/api-docs/api/lnd/dev/create-offer.md))

- gRPC: `rpc CreateOffer (CreateOfferRequest) returns (CreateOfferResponse);`
- REST: `POST /v2/dev/createoffer`
- Request: `devrpc.CreateOfferRequest`, fields `description` (required when `amount_msat` is set), `amount_msat` (zero or unset means the payer chooses the amount), `absolute_expiry` (seconds since epoch; zero or unset means no expiry) and `quantity_max` (zero means unlimited; if not set, quantity selection is not supported)
- Response: `devrpc.CreateOfferResponse`, fields `offer` (the bech32-encoded offer string) and `offer_hash` (the SHA256 of the offer's TLV records)

([source](../../raw/api/api-docs/api/lnd/dev/create-offer.md))
