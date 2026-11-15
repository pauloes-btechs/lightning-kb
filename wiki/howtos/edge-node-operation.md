---
title: Becoming an edge node
type: howto
sources:
  - raw/docs/lightning-network-tools/taproot-assets/become-an-edge-node.md
  - raw/docs/lightning-network-tools/taproot-assets/rfq.md
updated: 2026-11-14
---

# Becoming an edge node

What a routing node needs to add to act as an Edge node for Taproot Assets, and which software provides each part.

See also: [[taproot-assets]], [[taproot-assets-channels-guide]], [[tapd-rfq-guide]], [[tapd-operations]], [[tapd-getting-started]], [[tapd-rfq]], [[tapd-price-oracle]], [[taproot-assets-on-lightning]], [[lightning-terminal]].

## What an Edge node does

An Edge node routes payments between Taproot Asset channels and the larger Lightning Network. ([source](../../raw/docs/lightning-network-tools/taproot-assets/become-an-edge-node.md))

## The building blocks

| Part | Provided by (as labelled in the guide) |
|---|---|
| Existing routing node | LND |
| Assets | tapd |
| Taproot Asset channels | LND, tapd and litd |
| RFQ | "All litd nodes are able to use RFQ to communicate rates" |
| The Oracle | Requires external software |
| Hedging mechanisms | Requires external services |

([source](../../raw/docs/lightning-network-tools/taproot-assets/become-an-edge-node.md))

### Existing routing node

Building an Edge node requires both outgoing and incoming liquidity with the greater Lightning Network. The guide says this implies a mighty routing node, but might also be achieved with a few large channels to routing nodes (see [[liquidity]], [[routing-nodes]], [[lnd]]). ([source](../../raw/docs/lightning-network-tools/taproot-assets/become-an-edge-node.md))

### Assets

The decision of what assets an Edge node is willing to route depends on the asset's acceptance, liquidity and spreads. An Edge node could be affiliated directly with an issuer, but most likely acquires the assets on the open market. ([source](../../raw/docs/lightning-network-tools/taproot-assets/become-an-edge-node.md))

### Taproot Asset channels

An Edge node may both open Taproot Asset channels and accept them. It will advertise which assets it accepts channels for. It may restrict the channels it accepts by their minimum or maximum size, as it would for regular Bitcoin channels. Opening channels is covered on [[taproot-assets-channels-guide]]. ([source](../../raw/docs/lightning-network-tools/taproot-assets/become-an-edge-node.md))

### RFQ

Rates are communicated to peers directly via a process called "Request for Quote (RFQ)". The gRPC API allows any Taproot Assets node to request quotes and use them when constructing payment routes. Details are on [[tapd-rfq-guide]]. ([source](../../raw/docs/lightning-network-tools/taproot-assets/become-an-edge-node.md))

### The oracle

In the same way a routing node sets the rates at which it is willing to forward payments, an Edge node sets rates for each asset. These rates may change far more frequently and are not broadcast as part of regular gossip announcements. ([source](../../raw/docs/lightning-network-tools/taproot-assets/become-an-edge-node.md))

The oracle is software that aggregates or determines the rates, either based on an order book, reference rates or public order books. The oracle may determine a single rate on top of which the Edge node charges a fee, or separate bid and ask rates, separated by a spread. ([source](../../raw/docs/lightning-network-tools/taproot-assets/become-an-edge-node.md))

### Hedging mechanisms

Every forward shifts the balance of satoshis and assets in the Edge node. A sophisticated operator might want to hedge against price fluctuations, for example on a spot exchange. It is also conceivable that smaller Edge nodes use larger Edge nodes to hedge directly through Taproot Asset channels. ([source](../../raw/docs/lightning-network-tools/taproot-assets/become-an-edge-node.md))

## Conflicts

- **Who the RFQ process is between.** The Become an Edge Node guide says "The RFQ process is typically between the user and a price oracle" ([source](../../raw/docs/lightning-network-tools/taproot-assets/become-an-edge-node.md)); the RFQ guide says the user makes a Request for Quote "to the Edge Node" ([source](../../raw/docs/lightning-network-tools/taproot-assets/rfq.md)).
