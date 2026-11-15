---
title: Channel fees and inbound fees in lnd
type: howto
sources:
  - raw/docs/lightning-network-tools/lnd/channel-fees.md
  - raw/docs/lightning-network-tools/lnd/inbound-channel-fees.md
  - raw/docs/lightning-network-tools/lnd/lnd.conf.md
updated: 2026-11-14
---

# Channel fees and inbound fees in lnd

How to set, inspect and update forwarding fees on an [[lnd]] node, including inbound (discount) fees. Concept background is on [[channel-fees]]; routing-node strategy is on [[lnd-routing-node-operations]].

## How fees work

Routing nodes charge a fee for forwarding HTLCs. At the HTLC level the fee is the difference between the HTLC sent to the routing node and the one it sends onward: to pay a 1000 satoshi invoice one hop away through a node charging 1 satoshi, you send 1001 satoshis. Because fees are part of the payment and all HTLCs depend on the same preimage, fees are only earned on successful payments. ([source](../../raw/docs/lightning-network-tools/lnd/channel-fees.md))

Each peer sets its own policy, applied to the outgoing channel of a forward, so you charge when you push a payment to your neighbour and your neighbour charges when it pushes to you, even on a channel you opened. Fees set too high may stop payments flowing; too low and the channel's liquidity may be depleted immediately. ([source](../../raw/docs/lightning-network-tools/lnd/channel-fees.md))

Fees can be set as defaults in `lnd.conf`, at channel open with `lncli openchannel`, or later with `lncli updatechanpolicy`. ([source](../../raw/docs/lightning-network-tools/lnd/channel-fees.md))

## Base fee and fee rate

**Base fee**: charged per forwarded HTLC regardless of size, in milli-satoshi; called `base_fee_msat` and `bitcoin.basefee` in LND. ([source](../../raw/docs/lightning-network-tools/lnd/channel-fees.md))

```
lncli openchannel --base_fee_msat 1000 <node pubkey> --local_amt 31000000
lncli updatechanpolicy --base_fee_msat 1000 <channel point>
bitcoin.basefee=1000
```

([source](../../raw/docs/lightning-network-tools/lnd/channel-fees.md))

**Fee rate**: proportional to the forwarded amount, typically in parts per million, although the `--fee_rate` flag uses decimal places. ([source](../../raw/docs/lightning-network-tools/lnd/channel-fees.md))

```
lncli openchannel --fee_rate_ppm 300 <node pubkey> --local_amt 31000000
lncli updatechanpolicy --fee_rate_ppm 0.000300 <channel point>
bitcoin.feerate=300
```

([source](../../raw/docs/lightning-network-tools/lnd/channel-fees.md))

The sample config's defaults are `bitcoin.basefee=1000` and `bitcoin.feerate=1`, with total fee `basefee + (amount * feerate / 1000000)`. ([source](../../raw/docs/lightning-network-tools/lnd/lnd.conf.md))

## Inspecting fees

`lncli feereport` lists your channels with `chan_id`, `channel_point`, `base_fee_msat`, `fee_per_mil` and the decimal `fee_rate`, plus fees earned per day, week and month. In the guide's example, `base_fee_msat` 1000 and `fee_per_mil` 500 means a 1 million satoshi HTLC earns 501 satoshi. ([source](../../raw/docs/lightning-network-tools/lnd/channel-fees.md))

`lncli getchaninfo <chan_id>` shows both sides' policies (`node1_policy`, `node2_policy` with `time_lock_delta`, `min_htlc`, `fee_base_msat`, `fee_rate_milli_msat`, `disabled`, `max_htlc_msat`). `lncli describegraph` returns all channels and policies across the network. ([source](../../raw/docs/lightning-network-tools/lnd/channel-fees.md))

## Setting fees at open

From LND 0.16 fees can be set when opening, so capacity does not drain before the fee is adjusted:

```
lncli openchannel --base_fee_msat 1000 --fee_rate_ppm 100 --min_htlc_msat 1000 --node_key <pubkey> --local_amt 21000000
```

([source](../../raw/docs/lightning-network-tools/lnd/channel-fees.md))

## Updating fees

The guide does not recommend changing fees frequently, since peers may have opened channels expecting a certain fee level. ([source](../../raw/docs/lightning-network-tools/lnd/channel-fees.md))

```
lncli updatechanpolicy --base_fee_msat 1000 --fee_rate 0.000001 --time_lock_delta 500 --min_htlc_msat 1000 --chan_point <channel point>
```

Defaults go in `lnd.conf` as `bitcoin.basefee=1000` (milli-satoshi) and `bitcoin.feerate=1` (ppm). Adding these lines for the first time updates the policies of all existing channels except those updated manually before. To change only new channels, first run `lncli updatechanpolicy --base_fee_msat 1000 --fee_rate 0.000001` with the existing parameters on all channels, then edit the config and restart. ([source](../../raw/docs/lightning-network-tools/lnd/channel-fees.md))

Lightning Terminal's Autofees can change channel fees every three days based on past earnings (see [[lightning-terminal]]). ([source](../../raw/docs/lightning-network-tools/lnd/channel-fees.md))

## Inbound fees

Inbound fees are charged on the incoming channel of a payment, not only the outgoing one. Raising outbound fees can limit flow to a peer but not from a peer; inbound fees address "outbound drains", nodes that open a channel to you, push funds out through you and close, leaving you without outbound liquidity or compensation. ([source](../../raw/docs/lightning-network-tools/lnd/inbound-channel-fees.md))

They are available as negative fees, a discount on the outgoing fee, for backwards compatibility: nodes that do not understand them can still use the channel without the discount. The discount only applies while the total fee is larger than the combined fee of incoming and outgoing channel, so funds cannot be lost through routing. Inbound fees are propagated in gossip. ([source](../../raw/docs/lightning-network-tools/lnd/inbound-channel-fees.md))

Positive inbound fees are possible with `accept-positive-inbound-fees=true` in `lnd.conf`, but are risky because only upgraded nodes understand them, which can cause routing failures. The sample config marks the option experimental and defaults it to false. ([source](../../raw/docs/lightning-network-tools/lnd/inbound-channel-fees.md)) ([source](../../raw/docs/lightning-network-tools/lnd/lnd.conf.md))

Inbound fees have a base fee (milli-satoshis) and a rate (ppm), can currently only be set with `updatechanpolicy`, should for now be zero or negative, and require all other policy values on every call. Success returns an empty array. ([source](../../raw/docs/lightning-network-tools/lnd/inbound-channel-fees.md))

```
lncli updatechanpolicy --base_fee_msat 100 --fee_rate 1000 --time_lock_delta 80 --inbound_base_fee_msat -1000 --inbound_fee_rate_ppm -100 --chan_point <channel point>
```

([source](../../raw/docs/lightning-network-tools/lnd/inbound-channel-fees.md))

## Conflicts

- Fee rate flag units: the Channel Fees guide says the rate is in ppm while "the flag `--fee_rate` uses decimal places", but its `updatechanpolicy` example passes a decimal to the ppm flag, `--fee_rate_ppm 0.000300` ([source](../../raw/docs/lightning-network-tools/lnd/channel-fees.md)). The Inbound Channel Fees example passes `--fee_rate 1000` to the decimal flag ([source](../../raw/docs/lightning-network-tools/lnd/inbound-channel-fees.md)). The intended units for these examples are not resolved in the sources.

See also: [[channel-fees]], [[lnd-routing-node-operations]], [[lnd-configuration]], [[lnd-lightning]], [[lnd-sending-payments]].
