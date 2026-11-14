---
title: Channel leases
type: howto
sources:
  - raw/docs/lightning-network-tools/pool/channel_leases.md
  - raw/docs/lightning-network-tools/pool/batch_execution.md
  - raw/docs/lightning-network-tools/pool/orders.md
  - raw/docs/lightning-network-tools/pool/overview.md
  - raw/docs/lightning-network-tools/pool/faq.md
updated: 2026-11-14
---

# Channel leases

Once an order has been matched in an auction, a trader has purchased/sold channel leases to examine. ([source](../../raw/docs/lightning-network-tools/pool/channel_leases.md))

The lease duration is the duration of the contract that the maker (submitter of the ask order) and the taker (submitter of the bid order) enter when being matched by the auctioneer; the taker pays the premium for the whole duration upfront. ([source](../../raw/docs/lightning-network-tools/pool/orders.md))

See also: [[pool]], [[pool-orders-and-batches]].

## What a lease is

Pool's overview calls the product a Lightning Channel Lease (LCL): inbound (or outbound) channel liquidity packaged as a fixed incoming asset, earning interest over time, with a maturity date expressed in blocks. See [[liquidity]] and [[inbound-capacity]]. ([source](../../raw/docs/lightning-network-tools/pool/overview.md))

The maker must provide the offered liquidity at least for the selected number of blocks and is not allowed to close the channel before the agreed lease duration has elapsed. After that the maker may close the channel but is not obligated to; if the channel is economically viable, further routing fees might be collected by keeping it open. The taker is always allowed to close the channel, but pays the premium for the whole duration upfront. ([source](../../raw/docs/lightning-network-tools/pool/orders.md))

## Inspect your leases

Once an order has been matched in an auction, `pool auction leases` shows your current set of purchased/sold channel leases. ([source](../../raw/docs/lightning-network-tools/pool/channel_leases.md))

```
pool auction leases
{
        "leases": [
                {
                        "channel_point": "78cc6879c1dc1c00f22b29a06458f1335ed0fdb7d05c01b9077e3155e697bbb9:2",
                        "channel_amt_sat": 5000000,
                        "channel_duration_blocks": 144,
                        "premium_sat": 40000,
                        "execution_fee_sat": 5001,
                        "chain_fee_sat": 165,
                        "order_nonce": "eb972cd21cf1651e251c8b07d69e89c47294bae104fbdc9da26edf9aee335c9a",
                        "purchased": false
                }
        ],
        "total_amt_earned_sat": 40000,
        "total_amt_paid_sat": 5166
}
```

In this example a channel was sold for 40k satoshis, 5k satoshis were paid in chain and execution fees, and the yield was 35k satoshis. In the actual auction the numbers vary with the chain fee rate, market prices and execution fees. The chain fees paid can be constrained with the `--max_batch_fee_rate` argument when submitting orders. ([source](../../raw/docs/lightning-network-tools/pool/channel_leases.md))

The batch execution page shows a fuller lease record, which adds `channel_lease_expiry`, `channel_node_key`, `channel_node_tier` (for example `TIER_1`), `clearing_rate_price` and `order_fixed_rate` to the fields above. `purchased` is `false` for a channel the trader sold and `true` for one the trader bought. ([source](../../raw/docs/lightning-network-tools/pool/batch_execution.md))

Reading the two examples on that page: ([source](../../raw/docs/lightning-network-tools/pool/batch_execution.md))

- Sold: a 1,200,000 sat channel earned a premium of 59,998 sats; the trader paid an execution fee of 1201 sats and a chain fee of 165 sats, netting 59998-1201-165 = 58632 sats paid to its account.
- Bought: a 1,200,000 sat channel cost a premium of 11999 sats to the seller, plus the execution fee and chain fee, for a total cost of 11999+1201+165 = 13365 sats.

The output ends with a total tally, `total_amt_earned_sat` and `total_amt_paid_sat`. The command takes optional account and batch id arguments to filter the leases returned. ([source](../../raw/docs/lightning-network-tools/pool/batch_execution.md))

See also: [[pool-trader]].

## How the lease lifetime is enforced

In the alpha version of Pool, script level enforcement isn't yet implemented. Script level enforcement would lock the maker's funds in the channel for the lease period, so that the maker can't just collect the premium and close the channel instantly: they could still force close, but their funds would be unavailable until the maturity period has passed. ([source](../../raw/docs/lightning-network-tools/pool/channel_leases.md))

Instead, a feature in `lnd` prevents channels from being cooperatively closed by the maker until the expiry height, called the `thaw_height`. Additionally, if a force close by the maker of that channel is detected, the maker is banned from the market for a set period of time. See [[lnd]] and [[payment-channels]]. ([source](../../raw/docs/lightning-network-tools/pool/channel_leases.md))

The FAQ says the same from the buyer's side: if the lender force closes before the maturity date they will be banned from the market, and "This will not be possible in the future". ([source](../../raw/docs/lightning-network-tools/pool/faq.md))

## Life of a leased channel, per the FAQ

- The channel is opened automatically by the seller once the market clears. ([source](../../raw/docs/lightning-network-tools/pool/faq.md))
- It does not close at the maturity date; it remains open, but the seller has no obligation to keep it open beyond that date. ([source](../../raw/docs/lightning-network-tools/pool/faq.md))
- There are no limits on what the buyer can do with it; the channel behaves like a regular channel. ([source](../../raw/docs/lightning-network-tools/pool/faq.md))
- If the buyer cannot or does not want to move funds out of the channel off-chain, they can close the channel before the term limit with no penalties. ([source](../../raw/docs/lightning-network-tools/pool/faq.md))
- The seller earns the routing fees; the buyer can also earn fees if the new channel is used by a routing node. The seller can adjust their routing policy after opening, which the FAQ says "will be penalized in the future". See [[channel-fees]]. ([source](../../raw/docs/lightning-network-tools/pool/faq.md))
- On opening, the cost is split between buyer and seller. On closing, the initiator (in the Pool case the seller) pays the closing fee; with anchor output channels, the party initiating the force close pays the chain fee. ([source](../../raw/docs/lightning-network-tools/pool/faq.md))
- A minimum allowable channel size can be specified, which ensures you receive one or more inbound channels greater than or equal to that size. ([source](../../raw/docs/lightning-network-tools/pool/faq.md))

## Conflicts

- **Script enforcement.** The channel leases page says script level enforcement "isn't yet implemented" in the alpha version ([source](../../raw/docs/lightning-network-tools/pool/channel_leases.md)). The overview says the maturity date "is enforced by Bitcoin contracts, ensuring that the funds of the maker ... can't be swept until the maturity height" ([source](../../raw/docs/lightning-network-tools/pool/overview.md)), and the orders page offers a `script-enforced` value for `channel_type` ([source](../../raw/docs/lightning-network-tools/pool/orders.md)).
- **Command for viewing a bought channel.** The FAQ's "How do I see the channel I bought?" prints `accounts leases` ([source](../../raw/docs/lightning-network-tools/pool/faq.md)); the channel leases and batch execution pages use `pool auction leases` ([source](../../raw/docs/lightning-network-tools/pool/channel_leases.md), [source](../../raw/docs/lightning-network-tools/pool/batch_execution.md)).
- **Lease duration in examples.** The FAQ says a channel stays open for a minimum of 2016 blocks ([source](../../raw/docs/lightning-network-tools/pool/faq.md)); the channel leases example shows `"channel_duration_blocks": 144` ([source](../../raw/docs/lightning-network-tools/pool/channel_leases.md)).
