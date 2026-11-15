---
title: Channel fees
type: concept
sources:
  - raw/docs/the-lightning-network/pathfinding/channel-fees.md
  - raw/docs/the-lightning-network/liquidity/manage-liquidity.md
  - raw/docs/the-lightning-network/liquidity/how-to-get-inbound-capacity-on-the-lightning-network.md
  - raw/docs/community-resources/faq.md
updated: 2026-11-14
---

# Channel fees

In the Lightning Network, routing nodes are able to charge a fee for forwarding payments, so-called Hash-Time-Locked-Contracts (HTLCs). The guide describes this compensation as necessary to incentivize the efficient allocation of capital in the network. ([source](../../raw/docs/the-lightning-network/pathfinding/channel-fees.md))

## How a fee is collected

On the HTLC level, channel fees are the difference between the HTLC sent to the routing node and the HTLC sent from the routing node onwards. For example, if you are presented a 1000 satoshis invoice from a node one hop away that charges 1 satoshi, you send an HTLC over 1001 satoshis to the routing node, which sends a 1000 satoshis HTLC to the final recipient. See [[htlc]]. ([source](../../raw/docs/the-lightning-network/pathfinding/channel-fees.md))

As fees are included in the payment, and all HTLCs are contingent on the same preimage, fees can only be charged for successful payments. ([source](../../raw/docs/the-lightning-network/pathfinding/channel-fees.md))

## Who charges the fee

Fees are applied only once per peer and per channel. Each peer can independently set their fee policies for all their channels, and the policies are applied to the capital in the outgoing channel in the event of a forward. As you push a payment to your neighbor node you are able to charge a fee, and as payments are pushed to you, your neighbor charges the fee, even if the channel was created by you. Another rule of thumb from the guide: when your capital in a channel is depleted, you get to charge the fee. ([source](../../raw/docs/the-lightning-network/pathfinding/channel-fees.md))

The liquidity guide states the same rule from the node operator's side: the fee policy is applied to all outgoing payments, so you only earn the fee as the payment is passed on, and the fee policy on the incoming channel is decided by that peer. As a rule of thumb, you decide on the fee policy of your capital. ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))

## The two kinds of fee

There are two kinds of fees, the base fee and the fee rate. ([source](../../raw/docs/the-lightning-network/pathfinding/channel-fees.md))

### Base fee

The base fee is a fixed sum that is charged on each forward, typically 1 satoshi. It may also be set higher or to 0, or to any amount of millisatoshis. ([source](../../raw/docs/the-lightning-network/pathfinding/channel-fees.md))

The base fee is meant to compensate for the computational power and storage each forward costs. For each new channel state the node has to keep a new revocation key on file; if a watchtower is used, this information has to be sent to and stored on the watchtower as well. Such information has to be stored until the channel is closed. See [[watchtowers]]. ([source](../../raw/docs/the-lightning-network/pathfinding/channel-fees.md))

### Fee rate

The fee rate is a proportion of the payment that is forwarded, typically measured in parts per million (ppm). It is meant to compensate for the capital committed to Lightning channels. ([source](../../raw/docs/the-lightning-network/pathfinding/channel-fees.md))

## A worked example from the liquidity guide

`lncli feereport` shows the fee policy for all your channels and a summary of how many satoshis you have earned in routing fees. The guide shows a policy that "may look something like this" by default ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md)):

```
{
"chan_id": "739918549049147393",
"channel_point": "3ebdb34f1fc1948b5b49d127b52b19d24549779661af03a691cf934aa3b86e3f:1",
"base_fee_msat": "1000",
"fee_per_mil": "1",
"fee_rate": 0.000001
}
```

With this policy the node charges 1,000 milli-satoshi (1 satoshi), plus 1 milli-satoshi per million milli-satoshi (`fee_rate` times one million equals `fee_per_mil`). When routing a payment of 10,000 satoshi, the node earns 1.01 satoshi in fees. ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))

Default fees can be set in the lnd.conf file with the entries `bitcoin.basefee=1000` (referring to `base_fee_msat`) and `bitcoin.feerate=1` (referring to `fee_per_mil`). Changing these values in the configuration file affects new channels. To change fee rates for existing channels, use `lncli updatechanpolicy`. ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))

The command follows the format `lncli updatechanpolicy [command options] base_fee_msat fee_rate time_lock_delta [--max_htlc_msat=N] [channel_point]`. Tips from the guide ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md)):

- The minimum and maximum payments you are willing to forward are set with the `--min_htlc_msat` and `--max_htlc_msat` arguments, defined in milli-satoshis. ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))
- Fees for all channels are updated at the same time by omitting the `channel_point` argument; otherwise fees are updated for each channel individually. ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))
- A custom Time Lock Delta is set with the `--time_lock_delta` flag, with the default being 40, meaning the node has 40 blocks to claim any forwarded HTLCs. If the node goes offline during that time it might be at risk of losing funds. If the Time Lock Delta is too long, the channel becomes less attractive for routing. ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))

Example usage given by the guide: `lncli updatechanpolicy base_fee_msat 100 fee_rate 0.00001` and `lncli updatechanpolicy base_fee_msat 1000 fee_rate 0.000001 --max_htlc_msat 100000000`. ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))

Updating channel fee policies frequently is not recommended, as this might make the node appear less reliable to its peers. Successfully forwarded payments are listed with `lncli fwdinghistory`, with optional `--start_time` and `--end_time` arguments. ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))

## Fees from the payer's point of view

For a payment that traverses multiple hops, the fee is levied multiple times, by each router. Fees are known in advance of attempting the payment, and the payer chooses the route also based on fees. Two parties with a direct channel can transact with each other at no cost. ([source](../../raw/docs/community-resources/faq.md))

## Routing fees versus on-chain fees

Opening a channel requires the initiator to pay a transaction fee to Bitcoin miners, while a Lightning transaction pays fees to routing nodes that forward the payment to its final destination. To account for the fees incurred in closing a channel, a small amount of the channel capacity is reserved, so it may not be possible to completely empty a Lightning channel using a Lightning transaction. ([source](../../raw/docs/the-lightning-network/liquidity/how-to-get-inbound-capacity-on-the-lightning-network.md))

See also: [[pathfinding]], [[liquidity]], [[routing-nodes]], [[lnd-channel-fees]], [[lnd-routing-node-operations]], [[glossary]].
