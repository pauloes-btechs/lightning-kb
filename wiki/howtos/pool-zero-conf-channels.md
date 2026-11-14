---
title: Zero-confirmation channels in Pool
type: howto
sources:
  - raw/docs/lightning-network-tools/pool/zero-confirmation-channels.md
  - raw/docs/lightning-network-tools/pool.md
updated: 2026-11-14
---

# Zero-confirmation channels in Pool

A zero-confirmation ("zero-conf") channel is a Lightning Network payment channel that can send and receive immediately after the channel opening transaction is published, before the funding transaction is included in a block. [[pool]] supports buying and selling such channels. See also [[payment-channels]]. ([source](../../raw/docs/lightning-network-tools/pool/zero-confirmation-channels.md))

## Why Pool can offer them

When a channel is opened, the initiator's funds are locked in a 2-of-2 multisignature contract controlled by both channel peers. Before the funding transaction is included in a block it is vulnerable to being replaced by another transaction spending the funds back to the initiator, which is why one normally waits for a confirmation. A node that accepts a channel without confirmation trusts that it will eventually confirm and not be double-spent. ([source](../../raw/docs/lightning-network-tools/pool/zero-confirmation-channels.md))

That trust can be minimized by opening the channel from a 2-of-2 multisignature contract between the initiator and a known third party that can credibly assure not to collude with the initiator: Lightning Pool. The guide's reasoning: ([source](../../raw/docs/lightning-network-tools/pool/zero-confirmation-channels.md))

- The initiator is unable to double-spend the channel as they lack the second key to spend their UTXO.
- Lightning Pool is unable to take funds for themselves, as they lack the first key to spend the UTXO.
- The recipient only accepts channels co-signed by Pool.
- Pool is incentivized to not collude with initiators against recipients.
- Breaches of this assurance are inevitably publicly known and verifiable.

The landing page states the same: all channels sold through Pool are co-signed by Pool from a 2-of-2 multisignature account (see [[pool-accounts]]), so they cannot be maliciously double-spent by their initiator. ([source](../../raw/docs/lightning-network-tools/pool.md))

## Use cases

Zero-conf channels are valuable for users or Lightning Service Providers who want to immediately send and receive funds, such as merchants or users who lack sufficient inbound capacity to receive payments. They can request a new incoming channel and immediately receive and spend funds. See [[lightning-service-providers]], [[merchant-liquidity]] and [[inbound-capacity]]. ([source](../../raw/docs/lightning-network-tools/pool/zero-confirmation-channels.md))

A user may also want to spend funds held in their Pool account or deploy them on the Lightning Network: they can open a channel directly from their pool account to a node supporting zero-conf channels and spend the funds right away, or earn fees through routing. ([source](../../raw/docs/lightning-network-tools/pool/zero-confirmation-channels.md))

## 1. Enable zero-conf on lnd

Zero-confirmation channels need to be explicitly enabled on your node, and short channel ID aliases must be set as well. Amend `lnd.conf` with: ([source](../../raw/docs/lightning-network-tools/pool/zero-confirmation-channels.md))

```
protocol.option-scid-alias=true
protocol.zero-conf=true
```

This setting does not make the node accept all incoming zero-confirmation channels. Only channels co-signed by Lightning Pool will be accepted. You need to run Pool or Lightning Terminal to accept such channels, or build your own tooling to selectively accept incoming zero-conf channels opened outside of Pool. See [[lnd-configuration]] and [[lightning-terminal]]. ([source](../../raw/docs/lightning-network-tools/pool/zero-confirmation-channels.md))

## 2. Point the CLI at the right daemon

`poold` can be run standalone or bundled with `litd`. Depending on the setup you may have to specify the location of your `tls.cert` and the RPC port so the `pool` CLI talks to the intended daemon. More on this is on [[pool-setup]]. ([source](../../raw/docs/lightning-network-tools/pool/zero-confirmation-channels.md))

```
litd:  pool --rpcserver=localhost:8443 --tlscertpath ~/.lit/tls.cert
poold: pool --rpcserver=localhost:12010 --tlscertpath ~/.pool/mainnet/tls.cert
```

## Get zero-conf outbound liquidity

The auction type "outbound" can be used to open outbound zero-confirmation channels: ([source](../../raw/docs/lightning-network-tools/pool/zero-confirmation-channels.md))

```
pool orders submit bid --amt 100000 --self_chan_balance 100000 --interest_rate_percent 0.1 --auction_type outbound --zero_conf_channel --lease_duration_blocks 2016 --channel_type script-enforced --acct_key <your account key>
```

The trader key for `--acct_key` can be obtained with `pool accounts list`. Once the bid is matched with an appropriate ask, the new peer opens a channel to you with the requested balance on your side. ([source](../../raw/docs/lightning-network-tools/pool/zero-confirmation-channels.md))

In the guide's listing of the resulting bid, the order details include `"channel_type": "ORDER_CHANNEL_TYPE_SCRIPT_ENFORCED"`, `"auction_type": "AUCTION_TYPE_BTC_OUTBOUND_LIQUIDITY"` and `"is_public": true`, and the bid itself has `"version": 5`, `"min_node_tier": "TIER_1"`, `"self_chan_balance": "100000"`, `"unannounced_channel": false` and `"zero_conf_channel": true`. ([source](../../raw/docs/lightning-network-tools/pool/zero-confirmation-channels.md))

## Sell zero-conf channels

To sell zero-confirmation channels, submit an ask. The channel type must be set to "script-enforced", as zero-confirmation channels are only available as anchor channels. ([source](../../raw/docs/lightning-network-tools/pool/zero-confirmation-channels.md))

```
pool orders submit ask --amt 21000000 --interest_rate_percent 0.5 --channel_type script-enforced --announcement_constraints 0 --acct_key <your trader key>
```

The `--announcement_constraints` flag expresses a preference when submitting the ask: ([source](../../raw/docs/lightning-network-tools/pool/zero-confirmation-channels.md))

| Value | Meaning |
| --- | --- |
| 1 | only announced channels |
| 2 | only unannounced channels |
| 0 | no preference |

Once the ask is submitted, it is ready to be matched with a corresponding bid. ([source](../../raw/docs/lightning-network-tools/pool/zero-confirmation-channels.md))

## Buy zero-conf inbound channels

The guide calls this the fastest way for a node to get inbound liquidity that can be used immediately. The command is copied as the source prints it, including the repeated `--acct_key`. ([source](../../raw/docs/lightning-network-tools/pool/zero-confirmation-channels.md))

```
pool orders submit bid --amt 1000000 --interest_rate_percent 0.5 --zero_conf_channel --channel_type script-enforced --acct_key --acct_key <your trader key>
```

This places a bid in the Pool marketplace; once it is matched with an ask, the new peer opens the channel to you. The confirmation prompt shows the bid amount, bid duration, total premium (paid to maker), rate fixed, rate per block, execution fee, max batch fee rate, max chain fee and an `Is public: true` line, and the response contains `accepted_order_nonce` and `updated_sidecar_ticket`. The general order flags and fee lines are explained on [[pool-orders-and-batches]]. ([source](../../raw/docs/lightning-network-tools/pool/zero-confirmation-channels.md))

## Zero-conf sidecar channels

Pool can be used to buy [[sidecar-channels]] for third parties as zero-confirmation channels. The guide describes this as a capital effective way of onboarding users, for instance when distributing a self-hosted payment processor or node, and as a tool for those reselling Pool's liquidity to the public. ([source](../../raw/docs/lightning-network-tools/pool/zero-confirmation-channels.md))

**Offer (the buyer):**

```
pool sidecar offer --amt 100000 --min_chan_amt 100000 --interest_rate_percent 0.5 --zero_conf_channel --channel_type script-enforced --auto --acct_key <your trader key>
```

After the order confirmation, this returns a sidecar ticket (in the example, a JSON object with a `ticket` field) which can be passed on to the recipient of the channel for redemption. ([source](../../raw/docs/lightning-network-tools/pool/zero-confirmation-channels.md))

**Register (the recipient):** to redeem the ticket, the recipient needs to have enabled zero-confirmation channels and SCID aliases on their LND node. ([source](../../raw/docs/lightning-network-tools/pool/zero-confirmation-channels.md))

```
pool sidecar register <sidecar ticket>
```

Once the next batch has cleared, the channel is available for use immediately to receive funds. Optionally, balanced channels can be created this way using the `--self_chan_balance` flag. ([source](../../raw/docs/lightning-network-tools/pool/zero-confirmation-channels.md))

## Closing zero-conf channels

Zero-confirmation channels can be closed non-cooperatively at any time, like other channel types. They can also be closed cooperatively while the original channel funding is still unconfirmed. If the channel opening fees were not high enough to get the channel confirmed, the channel closing fees have to be high enough to cover the difference to current market prices for the funds to be ultimately spendable again. ([source](../../raw/docs/lightning-network-tools/pool/zero-confirmation-channels.md))

All zero-confirmation channels must be anchor channels, to ensure that a child-pays-for-parent is always able to pay the fees necessary to get both the channel opening transaction and the commitment transaction confirmed in a reasonable amount of time. ([source](../../raw/docs/lightning-network-tools/pool/zero-confirmation-channels.md))

See also: [[pool-trader]].
