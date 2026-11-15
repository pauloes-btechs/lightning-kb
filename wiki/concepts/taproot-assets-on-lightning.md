---
title: 'Taproot Assets on Lightning: edge nodes and trustless swaps'
type: concept
sources:
  - raw/docs/the-lightning-network/taproot-assets/taproot-assets-on-lightning.md
  - raw/docs/the-lightning-network/taproot-assets/edge-nodes.md
  - raw/docs/the-lightning-network/taproot-assets/trustless-swap.md
  - raw/docs/the-lightning-network/taproot-assets/faq.md
  - raw/docs/the-lightning-network/taproot-assets.md
updated: 2026-11-14
---

# Taproot Assets on Lightning: edge nodes and trustless swaps

Assets issued with the Taproot Assets Protocol can be deposited into Lightning Network payment channels and transacted instantly. This lets Lightning Network users hold a balance different from BTC, for instance a stablecoin, receive payments denominated in it, and use it to pay for goods and services over the Lightning Network. The protocol itself is described on [[taproot-assets-protocol]]. ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-on-lightning.md))

Bitcoin remains the backbone: payments through Taproot Assets can be routed over the existing Bitcoin Lightning Network without the need to upgrade or opt in. With Bitcoin providing the liquidity for payments denominated in other assets, the guide says Taproot Assets routing can deliver more routing fees paid in satoshis for routing node operators. ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-on-lightning.md))

## Taproot Assets channels

Taproot Asset channels can be created similarly to the way Bitcoin channels are created in the Lightning Network, and HTLCs can be constructed for transfers in them similarly to how bitcoin is transferred. Assets are transacted by creating a nested HTLC which, if needed, can be claimed by the recipient by revealing a preimage, or by the sender after a timeout period. See [[htlc]] and [[payment-channels]]. ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-on-lightning.md))

Taproot Assets channels can be created alongside BTC channels in the same utxo: Alice can create two channels with Bob in a single Bitcoin transaction, one containing an asset, the other BTC. ([source](../../raw/docs/the-lightning-network/taproot-assets.md))

Taproot Asset channels are not announced to the network, but are available as "private" channels to both channel partners. ([source](../../raw/docs/the-lightning-network/taproot-assets/edge-nodes.md))

## Multi-hop transfers

The guide frames the motivation as a bootstrapping problem: historically, any new asset needed an entirely new payment network. Taproot Assets instead lets the Lightning Network handle channels with any asset, with the ability to find routes across different assets. Where all participants along a route have liquidity with each other, they can opt to charge fees in BTC or in the transferred Taproot Assets. ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-on-lightning.md))

Even if no Taproot Assets route exists, a BTC route can take its place as long as the first node is willing to forward the Taproot Assets value in satoshis. This lets the Lightning Network facilitate exchange between bitcoin and Taproot Assets, and lets the recipient of a payment opt into receiving Taproot Assets instead of BTC. ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-on-lightning.md))

As a result, someone can receive a Taproot Asset but present the corresponding invoice to any other Lightning wallet, even one that does not opt into the Taproot Assets Protocol, which can pay the invoice using BTC. The Lightning invoice remains the standard scheme: an invoice ultimately settled in Taproot Assets can be paid by BTC or any other asset, and anyone with a Taproot Assets balance can pay any Lightning invoice. See [[lightning-invoices]] and [[multihop-payments]]. ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-on-lightning.md))

The FAQ puts it this way: when a route denominated in the relevant asset exists, the asset can be routed through it; otherwise it can be trustlessly swapped for BTC and its value routed to the destination, where it may be swapped back or into a different asset. ([source](../../raw/docs/the-lightning-network/taproot-assets/faq.md))

The owner of an asset does not need to own an equivalent amount of bitcoin to send or receive amounts denominated in their asset, but a route must exist between sender and receiver with sufficient liquidity, either in bitcoin or the asset. ([source](../../raw/docs/the-lightning-network/taproot-assets/faq.md))

## Exchange rates

The protocol gives integrators choice in how to handle exchange rates. Each peer in a channel performing swaps is responsible for determining their own exchange rate; they might use reference rates from liquid exchanges, or determine their own. Because the recipient generates the invoice themselves, the recipient receives the proper amount denominated in their desired asset. ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-on-lightning.md))

When creating an invoice, the recipient and their peer agree on a rate before the invoice is generated. They use the agreed price to generate a general Lightning Network invoice, including the hop hints and the channel policies, and pass it to the payer. Before releasing the preimage, the recipient's wallet can check whether it received the exact expected amount of the asset. ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-on-lightning.md))

When paying a satoshi-denominated invoice with an asset, the payer has to agree with their peer over the latest rates and fees. The payer passes the required amount of the asset plus fees, and the recipient only releases the preimage if they receive the amount of satoshis they expected. ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-on-lightning.md))

The protocol does not regulate or set rates. The FAQ likewise says the protocol does not prescribe how edge nodes and asset holders agree on a price; as long as both agree on a rate, any Taproot Asset can be swapped for BTC and its value transmitted through the broader Lightning Network. ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-on-lightning.md)) ([source](../../raw/docs/the-lightning-network/taproot-assets/faq.md))

## Edge nodes

An Edge Node is a Taproot Assets-aware Lightning Node that routes payments between Taproot Assets channels and Bitcoin channels. It is a specialized routing node with multiple public Bitcoin channels to the Lightning Network and unannounced Taproot Assets channels with its clients; it may have multiple channels per client, for example to handle multiple asset types. ([source](../../raw/docs/the-lightning-network/taproot-assets/edge-nodes.md))

What makes an Edge node different from an ordinary routing node is the ability to swap the Taproot Asset into BTC or vice versa, and route the value of the payment over the greater Lightning Network. This lets a Taproot Assets-aware wallet hold a Taproot Asset but pay to any Bolt 11/12 Lightning invoice, LNURL or Lightning address, and receive Taproot Assets for a payment made by any existing Lightning wallet. ([source](../../raw/docs/the-lightning-network/taproot-assets/edge-nodes.md))

As Edge nodes swap Taproot Assets to BTC through traditional HTLCs, they do not hold client assets or require custodial arrangements of any other kind. ([source](../../raw/docs/the-lightning-network/taproot-assets/edge-nodes.md))

Any Lightning Network node aware of Taproot Assets channels can potentially act as an edge node. Edge nodes compete with each other over the fees they collect from forwards and swaps: the routing fee, and a swap fee or alternatively a spread. If they fear abuse of their forwards, they have tools such as closing a channel, reducing the validity of invoices or increasing spreads. ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-on-lightning.md))

The FAQ uses the term edge liquidity for the concept that some Lightning Network nodes, with which you have Taproot Assets channels, may be willing to swap their value to BTC and back. ([source](../../raw/docs/the-lightning-network/taproot-assets/faq.md))

### What an Edge node does

- Open channels. An Edge node might be expected to open Taproot Asset channels to clients on demand, charging a fee or expecting revenue from future routing activity. ([source](../../raw/docs/the-lightning-network/taproot-assets/edge-nodes.md))
- Quote swap rates. Before a client swaps from Taproot Assets to Bitcoin it expects a quote from the Edge node, because Lightning invoices are denominated in Bitcoin. A quote is likewise needed to generate an invoice for an amount of an asset. When paying an invoice, quotes only need to be valid for a few seconds, while invoices require quotes for the period of their validity. A user may have channels to multiple Edge nodes and choose the most attractive quote. ([source](../../raw/docs/the-lightning-network/taproot-assets/edge-nodes.md))
- Route payments. An Edge node routes payments to and from its clients and the larger network, earning fees as any other routing node would. Payments are routed atomically through HTLCs. ([source](../../raw/docs/the-lightning-network/taproot-assets/edge-nodes.md))
- Hedge. An Edge node might hedge its trades on an exchange, and may also be used by others as a hedging mechanism, for example by allowing circular routes that let a client swap from and to a Taproot Asset. ([source](../../raw/docs/the-lightning-network/taproot-assets/edge-nodes.md))

### Finding and running an Edge node

How Edge nodes become discoverable is not fully determined and ultimately up to the market; they may be popularly known, or affiliated with wallets, exchanges or brokers. Eventually, Edge nodes may offer their liquidity services through a marketplace like Pool (see [[pool]]). ([source](../../raw/docs/the-lightning-network/taproot-assets/edge-nodes.md))

To run an Edge node, the guide recommends getting started with a regular LND routing node, and running litd in integrated mode so the node has access to Loop, Pool and Taproot Assets from the beginning. The Edge node also needs access to the Taproot Assets it wants to offer its clients, and its own custom logic for providing quotes and hedging its trades. See [[edge-node-operation]], [[tapd-rfq-guide]], [[lightning-terminal]] and [[routing-nodes]]. ([source](../../raw/docs/the-lightning-network/taproot-assets/edge-nodes.md))

### Optionality

The FAQ says Edge nodes' liquidity has some optionality properties, but this optionality will be priced by the market. Nodes offering it can decline to facilitate the quoted swap, and users can avoid nodes which do not perform adequately. It concludes that Taproot Assets does not have a "free option problem" of the kind that can exist in cross-chain atomic swaps. ([source](../../raw/docs/the-lightning-network/taproot-assets/faq.md))

## Trustless on-chain swaps

Taproot Assets can be swapped for Bitcoin or other assets through swaps that do not require the two parties to trust each other. Atomic swaps either complete in full or reverse back to their initial stage, which removes the "first mover problem". ([source](../../raw/docs/the-lightning-network/taproot-assets/trustless-swap.md))

Using Partially Signed Bitcoin Transactions (PSBTs), the swap can be performed in a single onchain transaction with minimal interaction between the swap partners and without an external coordinator. ([source](../../raw/docs/the-lightning-network/taproot-assets/trustless-swap.md))

The steps the guide describes ([source](../../raw/docs/the-lightning-network/taproot-assets/trustless-swap.md)):

1. The seller of the Taproot Asset creates a PSBT that proves their ownership over the asset while also allowing anybody who fulfills the PSBT to claim ownership over it (OP_TRUE). ([source](../../raw/docs/the-lightning-network/taproot-assets/trustless-swap.md))
2. The PSBT defines the Taproot Asset as an input, and the desired BTC amount as an output (22 million sats in the guide's example). To make the PSBT valid, somebody needs to add an input with at least that many sats. ([source](../../raw/docs/the-lightning-network/taproot-assets/trustless-swap.md))
3. To effectively "buy" the asset, the buyer also includes an anchor output for the Taproot Asset and, if needed, a change output for their BTC. ([source](../../raw/docs/the-lightning-network/taproot-assets/trustless-swap.md))
4. As the anchor input cannot be double-spent on the Bitcoin blockchain, only the winner of this auction can claim the Taproot Asset, and all competing transactions become invalid once a bid is confirmed on the blockchain. ([source](../../raw/docs/the-lightning-network/taproot-assets/trustless-swap.md))

## Fees and scaling, from the FAQ

A Taproot Assets transaction typically carries on-chain fees paid to bitcoin miners. When transacting Taproot Assets off-chain, you may pay routing fees to Lightning Network nodes instead. ([source](../../raw/docs/the-lightning-network/taproot-assets/faq.md))

Taproot Assets minimizes its on-chain footprint by storing all necessary metadata off-chain, allows multiple assets to be controlled by the same output, and aggregates multiple transactions into a single UTXO. ([source](../../raw/docs/the-lightning-network/taproot-assets/faq.md))

## Conflicts

- Whether assets can be put into Lightning channels today. The FAQ, under "How do I issue assets with Taproot Assets?", says "In the future it will be possible to also deploy this asset into a Lightning Network channel." ([source](../../raw/docs/the-lightning-network/taproot-assets/faq.md)) The Taproot Assets on Lightning page states in the present tense that these assets "can be deposited into Lightning Network payment channels and transacted instantly". ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-on-lightning.md)) The FAQ also speaks of the time "once the protocol is released". ([source](../../raw/docs/the-lightning-network/taproot-assets/faq.md))

See also: [[taproot-assets]], [[taproot-assets-channels-guide]], [[tapd-taproot-asset-channels]], [[tapd-rfq]], [[submarine-swaps]], [[glossary]].
