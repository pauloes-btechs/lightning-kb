---
title: Multipath payments (MPP)
type: concept
sources:
  - raw/docs/the-lightning-network/pathfinding/multipath-payments-mpp.md
  - raw/docs/community-resources/glossary.md
updated: 2026-11-14
---

# Multipath payments (MPP)

A multipath payment splits a payment into smaller parts and routes each part separately. `lnd` v0.10 introduced multi-path payments to the Lightning Network. ([source](../../raw/docs/the-lightning-network/pathfinding/multipath-payments-mpp.md))

## The problem MPP solves

Without MPP, a payment succeeds with exactly one successful HTLC. If a sender has enough liquidity in total to fulfill a payment, but split across multiple channels such that no single channel has the required liquidity, no single HTLC can succeed. ([source](../../raw/docs/the-lightning-network/pathfinding/multipath-payments-mpp.md))

A multi-path payment (MPP) can solve this by sending the payment in parts. In the guide's example, the first part consumes 20k sats in one channel and the second part uses 10k sats in the other channel. The highest payment amount is then defined by the sum of all channel balances rather than the maximum. ([source](../../raw/docs/the-lightning-network/pathfinding/multipath-payments-mpp.md))

## How the recipient settles

When the recipient receives the first part, they do not immediately settle the HTLC. Instead the HTLC is accepted and held, similar to how hodl invoice payments are accepted. The recipient waits for the second HTLC to arrive, concludes that the full amount has arrived, and at that point settles both HTLCs. ([source](../../raw/docs/the-lightning-network/pathfinding/multipath-payments-mpp.md))

The recipient could settle the first part because the preimage is known, but the guide gives two reasons this would not be rational. Settling right away would return the proof of payment to the sender while the full amount may never arrive, and with the proof of payment the sender could claim that the payment was made in full. Also, because all parts use the same payment hash, an intermediate node could use the now public preimage to settle the second HTLC without forwarding it at all. ([source](../../raw/docs/the-lightning-network/pathfinding/multipath-payments-mpp.md))

## MPP and AMP

The glossary defines a Multi-path Payment as a Lightning payment that reaches its destination through multiple routes in parallel, and says MPP and AMP are both an implementation of this idea. A part of a multi-path payment is called a shard. ([source](../../raw/docs/community-resources/glossary.md))

Atomic Multi-path Payments (AMP) is a payment standard that allows a payment to be made over multiple channels. Unlike MPP, each individual shard has its own payment hash, which allows for payments being made atomically. AMP also allows for static invoices, for sending funds solely using the recipient's public key, and for attaching messages to these payments. ([source](../../raw/docs/community-resources/glossary.md))

See also: [[pathfinding]], [[htlc]], [[liquidity]], [[lightning-invoices]], [[lnd-sending-payments]], [[glossary]].
