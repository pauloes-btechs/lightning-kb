---
title: The gossip network
type: concept
sources:
  - raw/docs/the-lightning-network/the-gossip-network.md
updated: 2026-11-14
---

# The gossip network

Lightning Network nodes announce themselves and their public channels to the broader network using a peer-to-peer gossip network. The gossip network also carries information on how to reach specific nodes and what fees they expect to forward funds. ([source](../../raw/docs/the-lightning-network/the-gossip-network.md))

The messages passed through the gossip network include information about a peer's alias, the features they support and how to reach them. The network also contains information about each channel, how it can be verified on the blockchain, and what fees its peers charge. ([source](../../raw/docs/the-lightning-network/the-gossip-network.md))

See also: [[lightning-network-overview]], [[routing-nodes]], [[pathfinding]], [[channel-fees]], [[payment-channels]], [[lnd-lightning]].

## The network graph

Your node uses the gossip network to assemble the network graph, which is necessary to calculate routes for payments. The source adds that "a pure routing node may not need this information, for example". You can query the graph on your own node with:

```
lncli describegraph
```

([source](../../raw/docs/the-lightning-network/the-gossip-network.md))

There is no consensus over what the graph looks like. A new node might not hear about an older node's update that has since dropped off the network, while another node might still have its information. A node may also remove channels from the graph if it believes its peers are no longer available or haven't been heard of in a while. ([source](../../raw/docs/the-lightning-network/the-gossip-network.md))

Peers often update their fees frequently, and each update has to be announced through the gossip network. The source says this can make the gossip network appear very noisy and resource consuming. ([source](../../raw/docs/the-lightning-network/the-gossip-network.md))

From the information gathered in the graph, basic statistics can be calculated, such as the total number of public nodes, their channels and capacity:

```
lncli getnetworkinfo
```

([source](../../raw/docs/the-lightning-network/the-gossip-network.md))

## Centrality

Calculations can also be performed over the graph, such as each node's centrality. Centrality is a measure of how many random routes in the network pass through a given node: the more central a node, the more hypothetical routes pass through it. While good routing nodes are often centrally located in the graph, the source says optimizing your node for centrality is often not considered an ideal strategy, as it is not a perfect proxy for routing fees. Your node calculates centrality scores for other nodes in the graph, which you can obtain with `lncli getnodemetrics`. See [[routing-nodes]]. ([source](../../raw/docs/the-lightning-network/the-gossip-network.md))

## Spam protection

To protect against spam attacks, Lightning nodes only relay gossip messages from nodes that have at least one public channel, which means owning bitcoin and paying on-chain transaction fees. ([source](../../raw/docs/the-lightning-network/the-gossip-network.md))

## Announcement types

There are three notable types of announcements made by nodes. These announcements are signed and forwarded to the announcer's peers, validated, and passed on until they reach the entire network. ([source](../../raw/docs/the-lightning-network/the-gossip-network.md))

- `channel_announcement`: the initial channel announcement is made cooperatively by both peers. It proves that the channel exists on the blockchain and establishes which nodes it belongs to.
- `channel_update`: once a channel has been announced cooperatively, it can be updated unilaterally by each party. This allows the parties to adjust terms with minimal effort, or to disable a channel when its peer is offline. Information relayed in this update includes fees and HTLC rules.
- `node_announcement`: can only be made by nodes that have previously announced a channel. It includes information such as the node's alias, how to reach it and what features it supports.

([source](../../raw/docs/the-lightning-network/the-gossip-network.md))

The source points to the specification "BOLT 7 - P2P Node and Channel Discovery". ([source](../../raw/docs/the-lightning-network/the-gossip-network.md))
