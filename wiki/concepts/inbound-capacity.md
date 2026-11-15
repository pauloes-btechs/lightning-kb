---
title: Getting inbound capacity
type: concept
sources:
  - raw/docs/the-lightning-network/liquidity/how-to-get-inbound-capacity-on-the-lightning-network.md
  - raw/docs/the-lightning-network/liquidity/manage-liquidity.md
  - raw/docs/community-resources/glossary.md
updated: 2026-11-14
---

# Getting inbound capacity

To receive payments on the Lightning Network, a node needs inbound capacity. The ability to send and receive depends on the existence of channels, as well as their capacity. ([source](../../raw/docs/the-lightning-network/liquidity/how-to-get-inbound-capacity-on-the-lightning-network.md))

The glossary defines inbound capacity as the amount of satoshis a node is able to receive through a given channel or all channels together, and outbound capacity as the amount a node is able to send through a single channel or all channels together. A channel's inbound and outbound capacity together define the channel's total capacity, as defined at its creation. ([source](../../raw/docs/community-resources/glossary.md))

## Capacity

Bitcoin exists in the form of UTXOs, unspent transaction outputs, each with an amount. 100 million satoshis (SAT) equals 1 bitcoin (BTC). On-chain, you can only spend up to the total sum of all UTXOs for which you have the key, but there are no limitations on how many UTXOs you can receive. ([source](../../raw/docs/the-lightning-network/liquidity/how-to-get-inbound-capacity-on-the-lightning-network.md))

On the Lightning Network, each channel is such a UTXO held in a 2-of-2 multi-signature contract between two parties. The value of the UTXO defines the channel capacity, the largest possible payment that can be handled by this channel. The capacity limits not only the size of each payment through the channel, but also the balance held by either party in it. See [[payment-channels]]. ([source](../../raw/docs/the-lightning-network/liquidity/how-to-get-inbound-capacity-on-the-lightning-network.md))

When a channel is opened, the party opening it typically defines its overall capacity and initially contributes this capacity as their own capital. The other party may communicate limits, such as a minimum channel size, before the channel is opened. ([source](../../raw/docs/the-lightning-network/liquidity/how-to-get-inbound-capacity-on-the-lightning-network.md))

### Total, inbound and outbound capacity: the Alice and Bob example

Alice has 1 million satoshis in her wallet and opens a channel with Bob for her entire balance using `lncli openchannel 021c97a90a411ff2b10dc2a8e32de2f29d2fa49d41bfbb52bd416e460db0747d0d 1000000`. The overall capacity of the channel is now 1 million satoshis, all belonging to Alice. Her outbound capacity is 1 million satoshis. Her inbound capacity is zero, as receiving a single satoshi would push her balance over the total capacity of the channel. Conversely, Bob's inbound capacity is 1 million satoshis. ([source](../../raw/docs/the-lightning-network/liquidity/how-to-get-inbound-capacity-on-the-lightning-network.md))

Alice then pays 300,000 satoshis to Bob. Her balance is now 700,000 satoshis, but the total capacity of the channel is unchanged, so Alice can now receive up to 300,000 satoshis: this is her inbound capacity. Bob's inbound capacity has shrunk to 700,000 while his outbound capacity has increased to 300,000 satoshis. The total capacity of the channel does not change unless another on-chain transaction is made. ([source](../../raw/docs/the-lightning-network/liquidity/how-to-get-inbound-capacity-on-the-lightning-network.md))

In short: Alice's inbound capacity = Bob's outbound capacity, and Alice's outbound capacity = Bob's inbound capacity. ([source](../../raw/docs/the-lightning-network/liquidity/how-to-get-inbound-capacity-on-the-lightning-network.md))

## Acquiring outbound capacity first

Starting from a node with zero channels, outbound liquidity requires a UTXO, which is used to open a channel with a good peer on the network. Ideally this peer has perfect uptime, good connections and a good amount of capital (see [[routing-nodes]]). ([source](../../raw/docs/the-lightning-network/liquidity/how-to-get-inbound-capacity-on-the-lightning-network.md))

A channel is opened with `lncli openchannel [node key] local-amt`. Optionally, a target for how quickly the channel should be ready is set with `--conf_target`, or the fee is set manually with `--sat_per_byte`. A node used purely for making and receiving payments may keep its channels unannounced by opening them with the `--private` option. A channel typically requires the funding transaction to have three confirmations on the blockchain to become active. ([source](../../raw/docs/the-lightning-network/liquidity/how-to-get-inbound-capacity-on-the-lightning-network.md))

## Ways to acquire inbound capacity

### Spend satoshis

The guide calls spending the channel balance the easiest and most obvious way to acquire inbound capacity, for example paying for things or exchanging the balance for cash at an exchange that supports Lightning deposits. For every satoshi spent, one satoshi of inbound capacity is gained, until the channel is empty and its total capacity is inbound capacity. ([source](../../raw/docs/the-lightning-network/liquidity/how-to-get-inbound-capacity-on-the-lightning-network.md))

For a node that only sends and receives payments, this single channel might be all that is needed. But the Lightning channel balance cannot exceed the capacity of the channel, so receiving more requires increasing inbound capacity further. ([source](../../raw/docs/the-lightning-network/liquidity/how-to-get-inbound-capacity-on-the-lightning-network.md))

For a routing node, spending turns local balance into remote balance and gives the ability to route payments. Some services also allow 'parking' satoshis on their node by making a deposit, which increases inbound liquidity but may be an inefficient allocation of capital. ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))

### Loop Out

Using Loop Out, a node can increase its inbound capacity beyond its initial capital. The guide describes Lightning Loop as a marketplace that allows users to engage in Submarine Swaps, which make two transactions conditional on each other: transaction A and B either execute together, or not at all. See [[loop]] and [[submarine-swaps]]. ([source](../../raw/docs/the-lightning-network/liquidity/how-to-get-inbound-capacity-on-the-lightning-network.md))

For inbound capacity, the swap is between an outbound Lightning transaction and an inbound on-chain transaction. The existing channel balance limits the size of the Loop transaction. As each channel needs to maintain a small reserve, the guide suggests spending about 80-90% of the channel balance on the swap. ([source](../../raw/docs/the-lightning-network/liquidity/how-to-get-inbound-capacity-on-the-lightning-network.md))

After the Lightning payment to Loop, the balance comes back as an on-chain transaction minus fees. That new UTXO can be used to open a second channel with a different node. The result, per the guide: the original capital (minus fees), about 80-90% more total capacity across the two channels, and about 40-45% of total channel capacity available for receiving Lightning payments. ([source](../../raw/docs/the-lightning-network/liquidity/how-to-get-inbound-capacity-on-the-lightning-network.md))

The liquidity management guide describes the same technique: Loop Out empties a Lightning channel into a bitcoin address, and the new UTXO opens a new channel; after two channel openings the node is left with both inbound and outbound capacity and the ability to route payments. It also notes Loop Out is useful for sending earnings to cold storage. Day-to-day use is on [[using-loop]] and [[autoloop]]. ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))

### Buy a channel on Lightning Pool

Inbound capacity can also be acquired by signaling a need for it and incentivizing others to open channels using their capital. Lightning Pool is a marketplace where bidders can pay well capitalized and connected nodes to open channels with them. These nodes are compensated for opening the channels and commit to maintaining them for a specified period of time. ([source](../../raw/docs/the-lightning-network/liquidity/how-to-get-inbound-capacity-on-the-lightning-network.md))

The guide calls Pool a convenient way of acquiring large amounts of inbound liquidity quickly, and the option of choice for node operators that depend on being able to receive Lightning transactions seamlessly, especially from a large group of users that might make deposits or payments. See [[pool]] and [[pool-channel-leases]]. ([source](../../raw/docs/the-lightning-network/liquidity/how-to-get-inbound-capacity-on-the-lightning-network.md))

### Signal a need

Others can be convinced to open a channel by signalling a need for inbound capacity; other routing nodes might be enticed by the outlook of routing payments to you and collecting the routing fees. For a merchant it might be well worth publicizing the need for inbound liquidity (see [[merchant-liquidity]]). ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))

## Reserve and fees

To account for the fees incurred in closing a channel, a small amount of the channel capacity is reserved. It may therefore not be possible to completely empty a Lightning channel using a Lightning transaction, and the channel balance may appear slightly smaller than the overall channel capacity. See [[channel-fees]]. ([source](../../raw/docs/the-lightning-network/liquidity/how-to-get-inbound-capacity-on-the-lightning-network.md))

See also: [[liquidity]], [[lightning-service-providers]], [[sidecar-channels]], [[glossary]].
