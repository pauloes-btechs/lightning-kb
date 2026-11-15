---
title: Pathfinding and route selection
type: concept
sources:
  - raw/docs/the-lightning-network/pathfinding.md
  - raw/docs/the-lightning-network/pathfinding/finding-routes-in-the-lightning-network.md
updated: 2026-11-14
---

# Pathfinding and route selection

In the Lightning Network, the payer decides on the route their payment takes. Ideally they find a direct and cheap path quickly, but in some cases they might have to attempt multiple available routes with varying fees. Nodes may employ different strategies to find the most economical route quickly, and in some implementations nodes may outsource pathfinding to an external party. ([source](../../raw/docs/the-lightning-network/pathfinding.md))

Routes are onion encrypted, meaning only the sender sees the full route. All nodes along the route only see what channel a payment is coming from and going to. The recipient does not learn the origin of the payment, only its final hop. ([source](../../raw/docs/the-lightning-network/pathfinding.md))

## The graph

To decide on a route, the sender needs to know about all public nodes and channels, known as the graph. ([source](../../raw/docs/the-lightning-network/pathfinding/finding-routes-in-the-lightning-network.md))

Computing the most efficient path through a network of nodes is described by the guide as a well studied problem in mathematics known as graph theory. Pathfinding algorithms typically treat the graph like a map, with each route between nodes having a unique cost instead of a distance. ([source](../../raw/docs/the-lightning-network/pathfinding/finding-routes-in-the-lightning-network.md))

## What complicates pathfinding

In addition to two separate fee structures for each channel (base fee and fee rate), pathfinding in the Lightning Network is further complicated by the channels' capacity and their liquidity. In practice, this means a Lightning node will create multiple possible paths to its destination and try them successively. ([source](../../raw/docs/the-lightning-network/pathfinding/finding-routes-in-the-lightning-network.md))

## Pathfinding in LND

LND's routing algorithm is largely based on Dijkstra's algorithm. LND also ranks nodes it has successfully sent payments through to improve its pathfinding. ([source](../../raw/docs/the-lightning-network/pathfinding/finding-routes-in-the-lightning-network.md))

## Pages in this section

- [[channel-fees]]: Channel fees
- [[multipath-payments]]: Multipath payments (MPP)

See also: [[liquidity]], [[gossip-network]], [[multihop-payments]], [[routing-nodes]], [[lnd]], [[lnd-sending-payments]], [[glossary]].
