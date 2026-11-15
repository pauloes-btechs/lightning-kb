---
title: Watchtowers
type: concept
sources:
  - raw/docs/the-lightning-network/payment-channels/watchtowers.md
updated: 2026-11-14
---

# Watchtowers

Watchtowers help secure channels against breaches. In the Lightning Network, peers store a commitment transaction for each update to their channel. The latest commitment transaction can be used to unilaterally close the channel at any time, allowing both parties to regain access to their funds on-chain without consent or participation of the other side. This is called a force close. ([source](../../raw/docs/the-lightning-network/payment-channels/watchtowers.md))

See also: [[payment-channels]], [[sweeping]], [[multihop-payments]], [[lnd-watchtower-setup]], [[lnd-watchtower]], [[lnd-watchtower-client]].

## Channel breaches

A breach means publishing a previous, expired and revoked commitment transaction that awards the publisher a higher balance than the most recent one. To prevent this, the Lightning Network protocol introduces the concept of a penalty: whoever publishes a commitment transaction locks up their balance for a predetermined amount of time. In a regular unilateral closure the initiator has to wait to retrieve her side of the channel, while the other party can spend theirs as soon as the commitment transaction is confirmed. ([source](../../raw/docs/the-lightning-network/payment-channels/watchtowers.md))

For every new channel update, the previous commitment transaction is invalidated by both peers through the exchange of a penalty secret. While the breaching peer has to wait to retrieve their funds, the other node can retrieve their own funds immediately and also take the funds of the attacker, as long as they have this secret and are able to produce a valid signature. ([source](../../raw/docs/the-lightning-network/payment-channels/watchtowers.md))

The source says this principle makes channel breaches extremely rare. But to revoke a breached channel and claim the attacker's funds, the peer being breached needs to be online regularly and monitor every single transaction in every block for a breach before the arbitration time has elapsed. ([source](../../raw/docs/the-lightning-network/payment-channels/watchtowers.md))

## How a watchtower works

Watchtowers are other Lightning Network nodes that ideally run on a separate machine and network from the node they are watching over. They are required to almost always be online and watch every bitcoin block for potential breaches, ideally using their own bitcoin node. ([source](../../raw/docs/the-lightning-network/payment-channels/watchtowers.md))

For each commitment transaction of each remote peer, the routing or payment node preventatively creates a signed transaction revoking the channel breach. This transaction is encrypted with the transaction ID of the breach transaction before it is passed to the watchtower together with the first half of the transaction ID. ([source](../../raw/docs/the-lightning-network/payment-channels/watchtowers.md))

With this mechanism the watchtower knows what transaction IDs to look for, but cannot see the content of each commitment transaction, which shields balances from the watchtower. Only the frequency with which the channel is updated is revealed, and only channel breaches are revealed, not regular force closures. ([source](../../raw/docs/the-lightning-network/payment-channels/watchtowers.md))

Once the watchtower finds a relevant breach, it can decrypt the signed revocation transaction and publish it to the bitcoin network. The attacker forfeits their channel balance as punishment. ([source](../../raw/docs/the-lightning-network/payment-channels/watchtowers.md))

## Timelocks

The mechanism that makes this possible is a script that defines two conditions under which the locked up funds can be spent. The "Check Sequence Verify" (CSV) timelock measures the number of blocks that passed between the confirmation of the commitment transaction and the current block. See [[multihop-payments]]. ([source](../../raw/docs/the-lightning-network/payment-channels/watchtowers.md))

The CSV delay is typically dynamically scaled to the channel size, but can also be manually set. The source's example: a CSV delay of 144 blocks allows for about 24 hours of time to revoke a channel breach, which means a node or watchtower has to be online and synced at least once every 24h to safely monitor all channel closures. ([source](../../raw/docs/the-lightning-network/payment-channels/watchtowers.md))

## Altruism

At the moment, watchtowers are only implemented as altruistic watchtowers: they do not get compensated for successfully intervening in a channel breach. They run without compensation, or charge for providing their service without guarantee of success. ([source](../../raw/docs/the-lightning-network/payment-channels/watchtowers.md))

As such, a node operator who wishes to use a watchtower typically runs it themselves, ideally on a separate machine, network and geolocation than the node they are guarding. One node may make use of multiple watchtowers, and one watchtower may guard multiple nodes. ([source](../../raw/docs/the-lightning-network/payment-channels/watchtowers.md))
