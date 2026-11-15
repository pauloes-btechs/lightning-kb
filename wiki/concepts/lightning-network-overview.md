---
title: 'The Lightning Network: overview'
type: concept
sources:
  - raw/docs/the-lightning-network/overview.md
  - raw/docs/readme.md
updated: 2026-11-14
---

# The Lightning Network: overview

The Lightning Network is a peer-to-peer payment network. It leverages payment channels anchored on the Bitcoin blockchain to enable near instant and low-cost settlement of bitcoin between participants. Multiple such payment channels are chained together to deliver payments to anyone in the network without requiring trust in participants. ([source](../../raw/docs/the-lightning-network/overview.md))

The guides assume basic knowledge of Bitcoin, specifically the UTXO model, unconfirmed transactions and their confirmation on the Blockchain. ([source](../../raw/docs/the-lightning-network/overview.md))

## The parts, in the order the guide introduces them

- Payment channels: the overview says that to understand the Lightning Network in its entirety, one should begin by learning about payment channels. See [[payment-channels]]. ([source](../../raw/docs/the-lightning-network/overview.md))
- Invoices: Lightning Network invoices are used by the recipient of a payment to specify amounts, features and the recipient's location in the network. See [[lightning-invoices]]. ([source](../../raw/docs/the-lightning-network/overview.md))
- Gossip: the entirety of all payment channels forms the Lightning Network, and information about channels and participants is relayed through a gossip network between peers. See [[gossip-network]]. ([source](../../raw/docs/the-lightning-network/overview.md))
- Routing: when making payments, the sender has to find a route from their node through routing nodes to the recipient. Nodes and their channels are known, but whether an individual node is available and has the liquidity to route the payment is not; in practice that means constructing multiple theoretical routes and attempting them one by one. See [[pathfinding]] and [[routing-nodes]]. ([source](../../raw/docs/the-lightning-network/overview.md))
- Atomic payments: each Lightning payment is atomic, meaning it is either completed or failed in full. This is achieved through Hash Time-lock Contracts (HTLC), which allow individual payments to be settled on-chain in situations where a routing node were to become unresponsive or acts maliciously. See [[htlc]] and [[multihop-payments]]. ([source](../../raw/docs/the-lightning-network/overview.md))
- Liquidity: nodes and channels are constrained by the capital they hold. The overview says one must also understand how liquidity affects the reliability of payments, and how a routing node operator can earn fees by effectively deploying capital where it is most needed. See [[liquidity]]. ([source](../../raw/docs/the-lightning-network/overview.md))

The overview's list of sub-sections also includes "L402: Lightning HTTP 402 Protocol" and "Taproot Assets". See [[l402]] and [[taproot-assets-protocol]]. ([source](../../raw/docs/the-lightning-network/overview.md))

## The Builder's Guide and the products it covers

The Builder's Guide describes itself as a home for those looking to learn about the Lightning Network, use and build on LND, Lightning Terminal, Loop, Pool, as well as those developing their own LAPPS. ([source](../../raw/docs/readme.md))

The guide's welcome page describes the products as follows:

- LND: the section to look at "if you're getting started with LND, want to configure it optimally or learn how to integrate LND into your production environment". See [[lnd]].
- Lightning Terminal: a browser-based, self-hosted dashboard for Lightning Labs products. See [[lightning-terminal]].
- Loop: a service that makes it easier to send and receive funds on Lightning, serving as an on and off ramp between the Lightning Network and the Bitcoin blockchain. See [[loop]].
- Pool: a non-custodial marketplace where users can buy inbound liquidity from node operators. See [[pool]].
- Taproot Assets: a protocol for issuing assets on the bitcoin blockchain that can be transferred over the Lightning Network for instant, high volume, low fee transactions. See [[taproot-assets]].
- L402: tokens that combine the capabilities of macaroons with that of a Lightning payment, making it easy to charge satoshis for API requests. See [[l402]] and [[macaroons]].

([source](../../raw/docs/readme.md))

The welcome page also lists external resources: a Developer Slack, the `lightninglabs` Github organization, and API documentation "including LND, Loop, Pool, Faraday & Taproot Assets". ([source](../../raw/docs/readme.md))

## Pages in this section

- [[payment-channels]]: Payment channels and their lifecycle
- [[sweeping]]: Sweeping
- [[watchtowers]]: Watchtowers
- [[htlc]]: Hash time-locked contracts (HTLCs)
- [[multihop-payments]]: Multihop payments, the payment cycle and timelocks
- [[submarine-swaps]]: Submarine swaps
- [[routing-nodes]]: What makes a good routing node and good peers
- [[lightning-invoices]]: Lightning invoices and the payment lifecycle
- [[gossip-network]]: The gossip network
