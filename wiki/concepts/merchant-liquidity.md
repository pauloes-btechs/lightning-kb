---
title: Liquidity management for merchants
type: concept
sources:
  - raw/docs/the-lightning-network/liquidity/liquidity-management-for-lightning-merchants.md
updated: 2026-11-14
---

# Liquidity management for merchants

When a merchant runs their own node to receive payments, the obligation to manage channel liquidity falls onto the merchant. The guide notes there is tooling to integrate a Lightning node into other systems, naming BTCPay and LNbits as examples. ([source](../../raw/docs/the-lightning-network/liquidity/liquidity-management-for-lightning-merchants.md))

## Why it matters

A merchant wants payments to their node to be as reliable as possible. Due to the architecture of the Lightning Network, a merchant may not even know that users are having issues paying unless they file a report: failed payments are not easily distinguishable from payments that were never attempted. The guide therefore calls it critical to have sufficient liquidity in the right place at the right time. ([source](../../raw/docs/the-lightning-network/liquidity/liquidity-management-for-lightning-merchants.md))

Payments to the node should also be cheap, as excessive routing costs can make a service appear less valuable to the consumer. Payment failures and high fees typically go hand in hand for mismanaged nodes. ([source](../../raw/docs/the-lightning-network/liquidity/liquidity-management-for-lightning-merchants.md))

## Inbound liquidity

The size of a payment channel is fixed at the time of its creation, defining its total capacity; for instance, a 10 BTC channel can at maximum facilitate a transfer of 10 BTC. Inbound liquidity is the portion of that capacity that is held by your peer and can be forwarded to your side as part of a payment. ([source](../../raw/docs/the-lightning-network/liquidity/liquidity-management-for-lightning-merchants.md))

### Acquiring it

To be able to receive payments, a merchant has to acquire inbound liquidity. The guide lists three ways ([source](../../raw/docs/the-lightning-network/liquidity/liquidity-management-for-lightning-merchants.md)):

1. Ask your clients. The users most enthusiastic about Lightning payments might be able and willing to provide inbound capacity. ([source](../../raw/docs/the-lightning-network/liquidity/liquidity-management-for-lightning-merchants.md))
2. Buy channels. There are market places like Pool where channels can be purchased, as well as dedicated Lightning Service Providers specializing in liquidity services. ([source](../../raw/docs/the-lightning-network/liquidity/liquidity-management-for-lightning-merchants.md))
3. Push out payments. A merchant may open channels themselves, then acquire liquidity in them by swapping funds onchain, making Lightning payments, or selling Bitcoin on an exchange that supports Lightning Network deposits. The guide says this mechanism works best in the long run. ([source](../../raw/docs/the-lightning-network/liquidity/liquidity-management-for-lightning-merchants.md))

See [[inbound-capacity]], [[pool]] and [[lightning-service-providers]].

### How it shifts as payments arrive

When a payment is made through a channel, the balances of the channel shift. In the guide's example, Bob opens a channel to Alice over 10 million satoshis, or 0.1 BTC, and the total capacity of the channel will forever be 0.1 BTC. Once the channel is active, Alice at first has 10 million satoshis in inbound liquidity, which can be received as one payment or as 1 million payments of 10 satoshis. Eventually all funds have moved to Alice's side and she can no longer receive payments through this channel. ([source](../../raw/docs/the-lightning-network/liquidity/liquidity-management-for-lightning-merchants.md))

## Maintaining inbound liquidity

Repeatedly soliciting or buying new channels is costly, as channel peers expect to be compensated for their capital and the cost of opening and closing the channel. Ideally channels are reused, so the cost of opening them is amortized over a longer period of time. This is achieved by emptying channels: Alice needs to "push out" funds through her channel with Bob to be able to receive payments again. ([source](../../raw/docs/the-lightning-network/liquidity/liquidity-management-for-lightning-merchants.md))

The guide gives three main ways to push funds out ([source](../../raw/docs/the-lightning-network/liquidity/liquidity-management-for-lightning-merchants.md)):

1. Make Lightning payments, for example to suppliers or staff. When channels are used in both directions, fees tend to be the lowest. ([source](../../raw/docs/the-lightning-network/liquidity/liquidity-management-for-lightning-merchants.md))
2. Swap offchain funds for onchain funds, for instance using Lightning Loop. This is preferable if the funds are to be held in Bitcoin, for example as a reserve or savings account, and it can be automated using Autoloop in the Lightning Terminal UI. ([source](../../raw/docs/the-lightning-network/liquidity/liquidity-management-for-lightning-merchants.md))
3. If funds need to be converted to fiat currencies, do so through platforms that support Lightning Network deposits. This minimizes onchain fees and allows channels to be open longer. ([source](../../raw/docs/the-lightning-network/liquidity/liquidity-management-for-lightning-merchants.md))

See [[loop]], [[autoloop]], [[terminal-liquidity-tools]] and [[lightning-terminal]].

## Identifying good peers

Good peers are peers that most reliably and cheaply route payments to your node. As a rule of thumb, the channels that deplete the quickest belong to your best peers. ([source](../../raw/docs/the-lightning-network/liquidity/liquidity-management-for-lightning-merchants.md))

Another metric is the cost of pushing out payments. If a peer reliably routes payments to you but charges significantly more to push out payments than other peers, you may deprioritize maintenance on their channel. See [[routing-nodes]] and [[channel-fees]]. ([source](../../raw/docs/the-lightning-network/liquidity/liquidity-management-for-lightning-merchants.md))

## Summary from the guide

- Avoid closing channels unless peers are offline or funds cannot be pushed out through the Lightning Network. ([source](../../raw/docs/the-lightning-network/liquidity/liquidity-management-for-lightning-merchants.md))
- Identify your good peers and regularly push payments out through their channel, either by making Lightning payments yourself or by swapping funds into your onchain wallet with Loop or Autoloop. ([source](../../raw/docs/the-lightning-network/liquidity/liquidity-management-for-lightning-merchants.md))

See also: [[liquidity]], [[submarine-swaps]], [[glossary]].
