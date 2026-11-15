---
title: Lightning service providers
type: concept
sources:
  - raw/docs/the-lightning-network/liquidity/lightning-service-provider.md
  - raw/docs/community-resources/glossary.md
updated: 2026-11-14
---

# Lightning service providers

A Lightning Service Provider (LSP) is an entity providing liquidity services on the Lightning Network on behalf of others. Channels in the Lightning Network are naturally constrained by their size, and capacity is further limited by local and remote balances. ([source](../../raw/docs/the-lightning-network/liquidity/lightning-service-provider.md))

The glossary describes an LSP as providing commercial liquidity and routing services on the Lightning Network; for example, an LSP might provide funds for automatic channel opening, inbound liquidity or routing information. ([source](../../raw/docs/community-resources/glossary.md))

## What an LSP does

LSPs typically help manage a user's liquidity by performing one of two tasks ([source](../../raw/docs/the-lightning-network/liquidity/lightning-service-provider.md)):

- Swapping on-chain funds for off-chain funds or vice versa. ([source](../../raw/docs/the-lightning-network/liquidity/lightning-service-provider.md))
- Opening channels to increase a user's inbound capacity or improve their position in the graph. ([source](../../raw/docs/the-lightning-network/liquidity/lightning-service-provider.md))

See [[inbound-capacity]] and [[pathfinding]].

## Custody

Ideally, an LSP interacts with its clients in a purely non-custodial way. Swaps can be constructed as Submarine Swaps to guarantee that the service provider cannot abscond with funds at any time (see [[submarine-swaps]]). When opening channels to peers, the LSP retains custody over its side of the channel and earns routing fees as it forwards payments. ([source](../../raw/docs/the-lightning-network/liquidity/lightning-service-provider.md))

## Channels for wallet users

LSPs are most commonly known for providing liquidity to users of non-custodial wallets in the form of channels. This lets users immediately receive Lightning payments to their wallets without requiring active channel management or ownership over a UTXO. ([source](../../raw/docs/the-lightning-network/liquidity/lightning-service-provider.md))

The LSP typically charges an upfront payment to compensate for mining fees and capital costs. These fees are often deducted directly from an incoming payment, but could also be charged upfront. It may be difficult for the LSP to assess how large a new channel to a user should be. ([source](../../raw/docs/the-lightning-network/liquidity/lightning-service-provider.md))

## Where the capital comes from

An LSP may borrow bitcoin for this task, or deploy its own funds. It is also possible for an LSP to buy such channels on the open market, such as Lightning Pool using sidecar channels, instead of opening them itself. See [[pool]] and [[sidecar-channels]]. ([source](../../raw/docs/the-lightning-network/liquidity/lightning-service-provider.md))

See also: [[liquidity]], [[merchant-liquidity]], [[glossary]].
