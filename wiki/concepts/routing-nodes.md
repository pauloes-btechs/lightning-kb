---
title: What makes a good routing node and good peers
type: concept
sources:
  - raw/docs/the-lightning-network/multihop-payments/what-makes-a-good-routing-node.md
  - raw/docs/the-lightning-network/the-gossip-network/identify-good-peers.md
  - raw/docs/the-lightning-network/payment-channels/etymology.md
updated: 2026-11-14
---

# What makes a good routing node and good peers

Every channel in the network has a total capacity, limited by the amount of bitcoin committed at its creation. This balance can be held by either side of the channel, which affects its ability to pass on payments. The total capacity is the sum of the local capacity of each channel peer, or the local and remote capacity of your channel. ([source](../../raw/docs/the-lightning-network/multihop-payments/what-makes-a-good-routing-node.md))

As a result, a route that worked for one payment might not work for the next. The network is also constantly changing, as balances shift, new channels are opened and old channels are closed. ([source](../../raw/docs/the-lightning-network/multihop-payments/what-makes-a-good-routing-node.md))

The guide says operating a good routing node does not require a highly specialized set of skills (you do not need to be a programmer or understand the details of cryptography or complex financial markets), but the node will require plenty of close attention, and a basic understanding of the command line is useful. ([source](../../raw/docs/the-lightning-network/multihop-payments/what-makes-a-good-routing-node.md))

See also: [[gossip-network]], [[pathfinding]], [[channel-fees]], [[liquidity]], [[inbound-capacity]], [[multihop-payments]], [[payment-channels]], [[lnd-routing-node-operations]], [[lnd-channel-fees]], [[faraday]].

## Criteria of a good routing node

1. **Availability.** A routing node needs to be running and maintain active channels with the network. To let others open channels with you, you also need to allow for incoming connections.
2. **Reliability.** The node needs enough channels to other good routing nodes in the network. Private channels are not announced to the network and therefore not counted. The source adds that private channels can present additional opportunities for routing when others open channels with them, creating what is referred to as a Gateway node.
3. **Active.** Ideally all of these channels are available and not disabled. Avoid peering publicly with non-routing nodes.
4. **Capitalization.** Channels need sufficient capacity, with enough incoming and outgoing liquidity, to route payments efficiently.
5. **Buffer.** Each channel needs to maintain some buffer capital, meaning a minimum balance of outgoing and incoming capacity, so that the channel is able to route at all times. Other nodes may no longer choose you as a hop if they experience routing failures due to low buffer capital.

([source](../../raw/docs/the-lightning-network/multihop-payments/what-makes-a-good-routing-node.md))

## Allocating capital

Generally, large channels are better for routing, but concentrating all capital into two or three large channels might be less desirable than having a greater number of small channels with the broader network. You also need to incentivize others, by payment or other means, to allocate capital towards your node and not to close channels that you created with them. ([source](../../raw/docs/the-lightning-network/multihop-payments/what-makes-a-good-routing-node.md))

Routing nodes provide a service to those sending and receiving payments. Node operators compete with each other over the payment channels they create, and also over the fees they demand. ([source](../../raw/docs/the-lightning-network/multihop-payments/what-makes-a-good-routing-node.md))

While it is possible to score nodes, the guide says it is incredibly difficult to create a score that accurately reflects a node's ability to route payments effectively. If such criteria were transparent and easily replicable, nodes would strive to converge to it, leaving the network homogeneous and possibly unable to function. ([source](../../raw/docs/the-lightning-network/multihop-payments/what-makes-a-good-routing-node.md))

## Identifying good peers

The guide says identifying good peers matters whether you primarily send or receive payments or run a routing node, and lists these factors one might consider:

- How well connected is the node?
- Is the node sufficiently capitalized?
- Does the node offer competitive fees for the service it provides?
- Has the peer been stable and active for a long period of time?
- Would creating a new channel to the node be mutually beneficial?
- Does the peer support newly available features?

([source](../../raw/docs/the-lightning-network/the-gossip-network/identify-good-peers.md))

**Node connectedness.** A good peer is well connected to the network, meaning they themselves have channels with other good peers. The total channel count is much less important than the channel count to good peers. Opening a channel with a well connected peer increases your chance of being able to route payments successfully. ([source](../../raw/docs/the-lightning-network/the-gossip-network/identify-good-peers.md))

**Node capitalization.** A good peer is well capitalized, meaning its channels have sufficient capacity to fulfill your payment needs. Generally, fewer channels with higher capacity will increase your routing chances over more channels with lower capacity. ([source](../../raw/docs/the-lightning-network/the-gossip-network/identify-good-peers.md))

Your own node's capitalization depends on your needs. If you primarily make payments, your node needs to be sufficiently capitalized for these payments, in channels to good and stable peers. To receive payments, your node does not need to carry much of its own capital, but it needs enough inbound liquidity to receive payments from the network (see [[inbound-capacity]]). ([source](../../raw/docs/the-lightning-network/the-gossip-network/identify-good-peers.md))

The overall capacity of a node is easy to assess; the quality of that capacity is not, and it is not easy to tell whether the capital is held as incoming or outgoing capacity. You can use `lncli getnodeinfo <node public key>` to probe a node's capacity and number of channels. ([source](../../raw/docs/the-lightning-network/the-gossip-network/identify-good-peers.md))

**Competitive fees.** Good peers offer competitive fees and, more importantly, keep these fees stable over time. You can probe a channel's fees with `lncli getchaninfo --chan_id <8-byte compact channel id>`. The source's example runs `lncli getchaninfo 743145615608774656` and shows a response with `channel_id`, `chan_point`, `last_update`, `node1_pub`, `node2_pub`, `capacity`, and a `node1_policy` and `node2_policy` each containing `time_lock_delta`, `min_htlc`, `fee_base_msat`, `fee_rate_milli_msat`, `disabled`, `max_htlc_msat` and `last_update`. Alternatively `lncli describegraph` returns all channels and their policies across the entire network. See [[channel-fees]]. ([source](../../raw/docs/the-lightning-network/the-gossip-network/identify-good-peers.md))

**Node stability.** Stability is measured by a peer's uptime, and also includes measurements like the age of their channels. A node with high uptime and old channels makes a stable peer. The guide says older channels are likely channels that have proven to be profitable for the operator. ([source](../../raw/docs/the-lightning-network/the-gossip-network/identify-good-peers.md))

**Routing needs.** A good peer will have a need for you to peer with them, for example because they route payments themselves. In that case, two nodes that already have a well capitalized, active channel to each other make for worse peers than two nodes that are not connected directly. It could also be a new node with few channels that needs inbound capacity, for example a merchant; by peering with such a node you might reliably earn routing fees to this peer, even though the node does not appear on lists of "good peers". ([source](../../raw/docs/the-lightning-network/the-gossip-network/identify-good-peers.md))

**Supported features.** A good peer will have important features enabled that make maintaining your channels easier. The source's examples are payment-addresses, multi-path payments or wumbo channels. ([source](../../raw/docs/the-lightning-network/the-gossip-network/identify-good-peers.md))

## Monitoring peers and channels

Once you have found good peers, you need to monitor these connections and judge which channels to keep and which to close. Frequently opening and closing channels might make you a poor peer in the eyes of some, but closing inactive channels or channels with unreliable peers might be important to be known as a reliable router, and generally contributes to efficient capital allocation. ([source](../../raw/docs/the-lightning-network/the-gossip-network/identify-good-peers.md))

Some nodes might want to open private channels with you for the purpose of making payments. Such peers may generate stable income through routing fees, but as they make payments through you, your incoming capacity with these peers shrinks, binding your capital in a node that cannot route and may be offline most of the time. If these private peers have a way of regularly refilling their channels, they can make for a good peer even if you aren't able to route payments through them. ([source](../../raw/docs/the-lightning-network/the-gossip-network/identify-good-peers.md))

## Conflicts

Private channels and routing. The channel etymology page says a private channel "cannot be used for routing payments". ([source](../../raw/docs/the-lightning-network/payment-channels/etymology.md)) The routing node page says "Private channels can present additional opportunities for routing when others open channels with them, creating what is referred to as a Gateway node." ([source](../../raw/docs/the-lightning-network/multihop-payments/what-makes-a-good-routing-node.md)) The sources do not reconcile the two statements.
