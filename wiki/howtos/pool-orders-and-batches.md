---
title: Pool orders and batch execution
type: howto
sources:
  - raw/docs/lightning-network-tools/pool/orders.md
  - raw/docs/lightning-network-tools/pool/batch_execution.md
  - raw/docs/lightning-network-tools/pool/quickstart.md
  - raw/docs/lightning-network-tools/pool/first-steps.md
  - raw/docs/lightning-network-tools/pool/zero-confirmation-channels.md
  - raw/docs/lightning-network-tools/pool/channel_leases.md
  - raw/docs/lightning-network-tools/pool/faq.md
updated: 2026-11-14
---

# Pool orders and batch execution

See also: [[pool]], [[pool-accounts]], [[pool-trader]], [[pool-channel-auctioneer]].

## Asks, bids and units

There are two types of orders: asks and bids. You submit an ask when you have coins you want to lease out as inbound liquidity for a period of time (expressed in blocks), at a fixed rate compounded per block. You submit a bid when you need to acquire inbound liquidity (ability to receive) for a given amount of time, paying a fixed rate that compounds per block. See [[inbound-capacity]]. ([source](../../raw/docs/lightning-network-tools/pool/orders.md))

The market trades units rather than satoshis. A unit is 100,000 satoshis and represents the smallest channel that can be bought or sold on the auction platform. ([source](../../raw/docs/lightning-network-tools/pool/orders.md))

In the alpha version of Lightning Pool, a single lump sum premium is paid after order execution. ([source](../../raw/docs/lightning-network-tools/pool/orders.md))

A trader can have multiple unfilled bids and asks. Partial matching is possible, so someone could purchase only 10 of the 100 units offered in an ask. ([source](../../raw/docs/lightning-network-tools/pool/orders.md))

## Submit an ask

The guide's example offers 10 million satoshis at 0.3% (30 bps) over a 2016 block period (approximately 2 weeks): ([source](../../raw/docs/lightning-network-tools/pool/orders.md))

```
pool orders submit ask 10000000 0288096be9917f8ebdfc6eb2701635fe658f4eae1e0274dcce41418b3fb5145732 --interest_rate_percent=0.3 --lease_duration_blocks=2016

-- Order Details --
Ask Amount: 0.1 BTC
Ask Duration: 2016
Total Premium (yield from taker): 0.00029998 BTC 
Rate Fixed: 1488
Rate Per Block: 0.000001488 (0.0001488%)
Execution Fee:  0.00010001 BTC
Max batch fee rate: 100 sat/vByte
Max chain fee: 0.0016325 BTC
Confirm order (yes/no): yes
{
        "accepted_order_nonce": "e3dbd57e8c22e895cbe705a4ec5ce65bdd766de4fc6d90c8bed404da8e7cbebc"
}
```

Leaving off the `--force` flag requests this break down so the details can be confirmed before the order is put through. The order nonce is used throughout the auction to identify orders and for authentication purposes. ([source](../../raw/docs/lightning-network-tools/pool/orders.md))

### How the premium is computed

```
premium = (rate_fixed / billion) * amount * blocks
29,998 = (1,488/1,000,000,000)*10,000,000*2,016
```

Internally a fixed rate per block is used to compute the final premium, but on the command line the final acceptable premium is given as a percentage. When submitting an order you enter the value you wish to receive or accept at the end of the lease period; the per block lease rate is computed from it and the order is submitted using that. Given the same amount and fixed rate, a maker earns more by leasing funds for a longer period, and a taker pays more for a longer period. ([source](../../raw/docs/lightning-network-tools/pool/orders.md))

## Submit a bid

A bid is submitted with `pool orders submit bid`. The quickstart names `interest_rate_percent`, `amt` and `acct_key` as the flags to be sure to add. The trader key for `--acct_key` can be obtained with `pool accounts list`. ([source](../../raw/docs/lightning-network-tools/pool/quickstart.md), [source](../../raw/docs/lightning-network-tools/pool/zero-confirmation-channels.md))

The first-steps guide's example bid for an incoming channel (copied as printed, including the en dashes before `amt` and `acct_key`): ([source](../../raw/docs/lightning-network-tools/pool/first-steps.md))

```
pool orders submit bid –amt 100000 –acct_key 0389f9aad3e08ae5065985049428eb8d862455060b429e2ad42fda52830673e3c1 --interest_rate_percent 2 --max_batch_fee_rate 7 --lease_duration_blocks 2016
```

The FAQ's "How do I buy a channel?" example, where `amt` is the total amount of inbound liquidity being bid on, the key is the "trader key" from "accounts list", and the max batch fee rate is what you want to pay as part of the channel creation (the buyer pays half of the open fees): ([source](../../raw/docs/lightning-network-tools/pool/faq.md))

```
orders submit bid --amt 100000000 --acct_key 03b5ef9a2ab19502fbb1f72d597d772eff1db1c9f8713fbe0685009a882f7c01b6 --max_batch_fee_rate 253 --interest_rate_percent 0.0001
```

## List and cancel orders

`pool orders list` shows submitted orders. In the guide's example the order `details` contain `trader_key`, `rate_fixed`, `amt`, `max_batch_fee_rate_sat_per_kw`, `order_nonce`, `state`, `units`, `units_unfulfilled`, `reserved_value_sat`, `creation_timestamp_ns`, `events` and `min_units_match`, next to `lease_duration_blocks` and `version`. An order that hasn't been cleared yet has state `ORDER_SUBMITTED`; the 10 million satoshi ask shows up as 100 units. ([source](../../raw/docs/lightning-network-tools/pool/orders.md))

To cancel an order, first get its `order_nonce` with the list command, then run: ([source](../../raw/docs/lightning-network-tools/pool/orders.md))

```
pool orders cancel order_nonce
```

## Order flags

The guide notes that the default values shown in the command line help differ from the actual defaults: a value of `0` on the command line means "no actual value set, use the internal default value". The tables below give the actual defaults. ([source](../../raw/docs/lightning-network-tools/pool/orders.md))

### `pool orders submit ask`

| Flag | Required | Default Value | Description |
| --- | --- | --- | --- |
| `interest_rate_percent` | Yes | n/a | The interest rate that should be earned over the total lease duration. |
| `amt` | Yes | n/a | The amount of liquidity to offer in satoshis. Must be a multiple of the base unit (100k sat). |
| `acct_key` | Yes | n/a | The account's trader key to use to pay for the offered liquidity, the order submission fee and chain fees. |
| `lease_duration_blocks` | No | `2016` | The minimum number of blocks the offered channels need to stay open for in order to satisfy the contract. Distinct markets are available for the different durations. |
| `min_chan_amt` | No | 10% of `amt` | The minimum size/capacity of any offered channel. Higher values reduce the match potential but decrease the potential total in chain fees that must be paid. Must be a multiple of the base unit (100k sat). |
| `max_batch_fee_rate` | No | `100` sat/vByte | The maximum on-chain fee rate at which this order should be eligible to be included in a batch. If the auctioneer estimates a higher fee rate, orders below will be skipped. |
| `force` | No | `false` | When set to `true`, no order details will be shown and no confirmation is required. |
| `channel_type` | No | `unknown` | Can be set to `unknown`, `legacy` or `script-enforced`. A script enforced channel type cannot be closed cooperatively by the other party before the lease is completed. By default it is set to `unknown`, meaning the Pool server decides. |
| `allowed_node_id` | No | n/a | A node ID that this order is allowed to be matched with. It can be called multiple times. If not set, the ask can be fulfilled by any node, unless `not_allowed_node` is set. |
| `not_allowed_node_id` | No | n/a | A node ID that this ask is not allowed to match with. It can be called multiple times. If not set, the ask can be fulfilled by any node unless `allowed_node_id` is set. |

([source](../../raw/docs/lightning-network-tools/pool/orders.md))

The zero-confirmation guide additionally uses `--announcement_constraints` on an ask (`1` only announced channels, `2` only unannounced channels, `0` no preference); see [[pool-zero-conf-channels]]. ([source](../../raw/docs/lightning-network-tools/pool/zero-confirmation-channels.md))

### `pool orders submit bid`

| Flag | Required | Default Value | Description |
| --- | --- | --- | --- |
| `interest_rate_percent` | Yes | n/a | The maximum interest rate that should be paid for leasing a channel, calculated over the total lease duration. |
| `amt` | Yes | n/a | The amount of liquidity to lease in satoshis. Must be a multiple of the base unit (100k sat). |
| `acct_key` | Yes | n/a | The account's trader key to use to pay for the lease premium, order submission fee and chain fees. |
| `lease_duration_blocks` | No | `2016` | The minimum number of blocks the leased channels must stay open for in order to satisfy the contract. Distinct markets are available for the different durations. |
| `min_chan_amt` | No | 10% of `amt` | The minimum size/capacity of any leased channel. Higher values reduce the match potential but decrease the potential total in chain fees that must be paid. Must be a multiple of the base unit (100k sat). |
| `min_node_tier` | No | `1` | The minimum quality of node this bid should be matched with. The default is "Tier 1", meaning the bid is only matched with asks from nodes that are considered "good". With `--min_node_tier=0`, asks from all nodes should be considered, regardless of their "quality". |
| `max_batch_fee_rate` | No | `100` sat/vByte | The maximum on-chain fee rate at which this order should be eligible to be included in a batch. If the auctioneer estimates a higher fee rate, orders below will be skipped. |
| `force` | No | `false` | When set to `true`, no order details will be shown and no confirmation is required. |
| `self_chan_balance` | No | 0 | When set, the channel is created with a local balance funded by your account. Can be used to create up to 50/50 balanced channels. |
| `sidecar_ticket` | No | n/a | Used to redeem a sidecar channel. This option will override `amt`, `min_chan_amt`, `lease_duration_blocks` and `self_chan_balance` flags. See [[sidecar-channels]]. |
| `channel_type` | No | `unknown` | Can be set to `unknown`, `legacy` or `script-enforced`. A script enforced channel type cannot be closed cooperatively by the other party before the lease is completed. By default it is set to `unknown`, meaning the Pool server decides. |
| `allowed_node_id` | No | n/a | A node ID that this order is allowed to be matched with. It can be called multiple times. If not set, the ask can be fulfilled by any node, unless `not_allowed_node_id` is set. |
| `not_allowed_node_id` | No | n/a | A node ID that this bid is not allowed to match with. It can be called multiple times. If not set, the bid fulfils any node unless `allowed_node_id` is set. |

([source](../../raw/docs/lightning-network-tools/pool/orders.md))

The source's bid table lists `max_batch_fee_rate` a second time, with default `100` and the description "The maximum fee rate in sat/vB used for transaction batching." ([source](../../raw/docs/lightning-network-tools/pool/orders.md))

Bid flags that appear in other guide pages but not in this table: `--unannounced_channel` (first steps), and `--auction_type outbound` and `--zero_conf_channel` (zero-confirmation guide, see [[pool-zero-conf-channels]]). ([source](../../raw/docs/lightning-network-tools/pool/first-steps.md), [source](../../raw/docs/lightning-network-tools/pool/zero-confirmation-channels.md))

## Lease duration

The lease duration is the duration of the contract the maker (submitter of the ask) and the taker (submitter of the bid) enter when matched by the auctioneer. The maker must provide the offered liquidity at least for the selected number of blocks and is not allowed to close the channel before that. The maker may close the channel after the duration is over but is not obligated to. The taker is always allowed to close the channel; they pay the premium for the whole duration upfront, so closing early is to their own disadvantage. More on enforcement is on [[pool-channel-leases]]. ([source](../../raw/docs/lightning-network-tools/pool/orders.md))

The possible lease durations are fixed and defined by the auctioneer, so that distinct premium rates can form over different durations. The current list is queried with: ([source](../../raw/docs/lightning-network-tools/pool/orders.md))

```
pool auction leasedurations

{
      "lease_durations": {
              "2016": true,
              "4032": false,
      }
}
```

The integer is the lease duration in blocks. The boolean says whether matchmaking in that duration market is currently enabled; when adding a new lease duration the auctioneer might not enable matchmaking right away, to wait for the order book to be populated first. ([source](../../raw/docs/lightning-network-tools/pool/orders.md))

## Fees

### Order execution fee

An order execution fee is paid to the auctioneer server for every successfully executed (partial) match. It has a static part (the base fee, in satoshis), independent of the matched size, and a dynamic part (the fee rate, in parts per million), calculated on the number of matched units. The fee is set by the server and can change with demand, chain fee climate or other operational costs. ([source](../../raw/docs/lightning-network-tools/pool/orders.md))

```
pool auction fee

{
        "execution_fee": {
                "base_fee": "123",
                "fee_rate": "1234"
        }
}
```

With these example values, a matched order of 7 units (700k satoshis) would be charged an execution fee of 986 satoshis: ([source](../../raw/docs/lightning-network-tools/pool/orders.md))

```
execution_fee = base_fee + (fee_rate / million) * match_amount
986.8 = 123 + (1,234 / 1,000,000) * 700,000
```

The FAQ says buyers and sellers of channels should expect service charges of 5-25 basis points each. ([source](../../raw/docs/lightning-network-tools/pool/faq.md))

### Chain fees

Each successfully executed order results in at least one channel output in the batch transaction. Because an account must be spent for an order to be executed, an input per involved account is added, and if there is a remaining balance the change goes to a newly created output for that account. Each trader is charged fully for the transaction weight of their account inputs and outputs; the cost of the new channel output is split in half between maker and taker. ([source](../../raw/docs/lightning-network-tools/pool/orders.md))

For a bid over 5 units (500k satoshis) and an account 10 times that size, the guide computes 162 virtual bytes, which at an estimated network fee rate of 34 sat/vByte costs `162 * 34 = 5,508` satoshi in chain fees: ([source](../../raw/docs/lightning-network-tools/pool/orders.md))

```
size_vBytes = acct_input_size + 0.5 * chan_output_size + acct_output_size
162 ~= ~98 + 0.5 * 43 + 43
```

`--max_batch_fee_rate` tells the auctioneer that the order shouldn't be considered for matching if the current fee estimation is higher than that rate. If your desired chain fee is below the current proposed batch chain fee, the order won't be eligible for execution until chain fees come down. ([source](../../raw/docs/lightning-network-tools/pool/orders.md))

### The "Max chain fee" line

The `Max chain fee` value in the order summary is the absolute worst-case fee. It is calculated from how many potential partial matches an order could go through (assuming it always matches only the minimum match size or minimum channel size), applying the chain fee calculation above to each with the given `Max batch fee rate`. The guide calls it quite unlikely that the maximum is ever required. ([source](../../raw/docs/lightning-network-tools/pool/orders.md))

Two flags reduce this worst-case estimate: ([source](../../raw/docs/lightning-network-tools/pool/orders.md))

- `--min_chan_amt`: the minimum match size or minimum channel size. By default 10% of the full order amount. Increasing it makes a match less likely but reduces the number of times chain fees have to be paid. Setting it to 100% of the order amount is equivalent to a "kill-or-fill" order.
- `--max_batch_fee_rate`: the maximum network fee rate the order should be considered for. Setting it too low might result in orders not being executed at all, or only when the mempools are almost empty.

## Restricting who you match with

`allowed_node_id` matches with a specific node or limits matches to a set of nodes; `not_allowed_node_id` names nodes you do not want to match with. The guide's example: ([source](../../raw/docs/lightning-network-tools/pool/orders.md))

```
pool order submit bid --not_allowed_node_id 021c97a90a411ff2b10dc2a8e32de2f29d2fa49d41bfbb52bd416e460db0747d0d
```

The global `--newnodesonly` daemon flag causes the trader daemon to reject any matches with nodes its connected `lnd` node already has channels with (see [[pool-setup]]). Takers can influence the "quality" of the nodes their bids are matched against with `--min_node_tier`. ([source](../../raw/docs/lightning-network-tools/pool/orders.md))

A version field was added to the order submission protocol from the beginning, so that trader and auctioneer always know which fields an order is supposed to have set and therefore which fields are covered by the trader's order signature. ([source](../../raw/docs/lightning-network-tools/pool/orders.md))

## How a batch is executed

Pool conducts a discrete batch auction every 10 minutes; orders are only cleared at that interval rather than continuously. If after the interval a market can't be made (supply and demand didn't cross), nothing happens and the next batch is awaited. ([source](../../raw/docs/lightning-network-tools/pool/batch_execution.md))

1. **Matchmaking.** The auctioneer looks at the current fee climate and decides what fee rate the final Batch Execution Transaction (BET) should use to confirm in a timely manner. Orders whose `max_batch_fee_rate` is lower than the chosen rate are ignored this time around and reconsidered if the fee climate changes before the next auction. The auctioneer then matches asks with bids that pay at least the desired rate, assembles the unsigned BET and presents it to all matched traders, along with information about the node they matched with. ([source](../../raw/docs/lightning-network-tools/pool/batch_execution.md))
2. **Batch signing.** The trader's client checks every part of the BET that affects the trader: that the premium paid to the maker matches the batch clearing price, that the chain fee deducted from the account doesn't violate the max fee rate the trader agreed to, and that each channel output is well formed and of the expected amount. It then connects to the node on the other side of the match and starts the channel opening process, by setting up a funding shim with the backing `lnd` node. Only when all checks pass and the funding shim is set up does the trader sign its input to the batch transaction and respond to the auctioneer. ([source](../../raw/docs/lightning-network-tools/pool/batch_execution.md))
3. **Rejection.** The trader can reject signing the batch for any reason, even when the BET is well formed, for instance when connecting to the channel peer fails. Matchmaking can then start over, making sure the trader won't be matched with that channel peer again. ([source](../../raw/docs/lightning-network-tools/pool/batch_execution.md))
4. **Batch publication.** When all participating traders have signed their inputs, the auctioneer signs the final input and broadcasts the transaction. Participating traders only pay chain fees for their own inputs and outputs. ([source](../../raw/docs/lightning-network-tools/pool/batch_execution.md))

The FAQ adds that the seller has to be online when the batch clears or the match won't be included, and that a channel is opened as soon as the batch transaction has received a sufficient number of confirmations. ([source](../../raw/docs/lightning-network-tools/pool/faq.md))

## Uniform-price clearing

A uniform-clearing price algorithm gives all traders in the batch the same interest rate. The guide says this is the same mechanism used by the U.S Treasury for its bonds, and that your order will only be matched with a price better than your initial ask/bid. ([source](../../raw/docs/lightning-network-tools/pool/batch_execution.md))

Example: a bid to buy 100 million satoshis (1 BTC, 1000 units) for 2 weeks (2016 blocks) at 5%, when the market clearing price is 1%, ends up paying the clearing price. The rule of thumb: when I submit a bid, I'll either pay that amount or less; when I submit an ask, I'll either receive that amount or more. ([source](../../raw/docs/lightning-network-tools/pool/batch_execution.md))

## Inspecting batches

`pool auction snapshot` shows the latest cleared batch. The example output has `version`, `batch_id`, `prev_batch_id`, `clearing_price_rate`, a `matched_orders` list (each with `ask`, `bid`, `matching_rate`, `total_sats_cleared` and `units_matched`), `batch_tx_id` and `batch_tx`. ([source](../../raw/docs/lightning-network-tools/pool/batch_execution.md))

The command accepts a target `batch_id`; using the `prev_batch_id` of one batch walks back to the prior one: ([source](../../raw/docs/lightning-network-tools/pool/batch_execution.md))

```
pool auction snapshot --batch_id=03687baa3c7414e800ddba37edacb3281999739303b7290a69bd457f428ecd9b2c
```

There is no explicit "market buy" function. The guide suggests using the snapshot's `clearing_price_rate` to see the past market clearing price and submitting a bid/ask at a similar rate to be close to where demand in the market is. ([source](../../raw/docs/lightning-network-tools/pool/batch_execution.md))

After a batch, `pool auction leases` gives the overview of premiums, execution fees and chain fees per match; it is covered on [[pool-channel-leases]]. ([source](../../raw/docs/lightning-network-tools/pool/batch_execution.md))

## Conflicts

- **Choosing counterparties.** The FAQ says "You are not able to choose who to buy from" and "A seller cannot avoid selling to a specific peer. All peers on the network are valid buyers" ([source](../../raw/docs/lightning-network-tools/pool/faq.md)). The orders page documents `allowed_node_id` and `not_allowed_node_id` on both asks and bids ([source](../../raw/docs/lightning-network-tools/pool/orders.md)).
- **Matching restrictions, within the orders page.** Its "Extensibility" section says "At the moment there are only two restrictions" (`--newnodesonly` and `--min_node_tier`) and lists a concrete list of node public keys and sidecar channels as future work, while the same page's flag tables and "Match with specific nodes" section document `allowed_node_id`, `not_allowed_node_id` and `sidecar_ticket` ([source](../../raw/docs/lightning-network-tools/pool/orders.md)).
- **Script enforcement.** The orders page offers `channel_type` `script-enforced` ([source](../../raw/docs/lightning-network-tools/pool/orders.md)); the channel leases page says that in the alpha version of Pool script level enforcement isn't yet implemented ([source](../../raw/docs/lightning-network-tools/pool/channel_leases.md)).
- **Lease length.** The FAQ speaks of "a set duration of time (2016 blocks)" and a minimum of 2016 blocks ([source](../../raw/docs/lightning-network-tools/pool/faq.md)); the orders page describes multiple duration markets queried with `pool auction leasedurations`, with `2016` as the default ([source](../../raw/docs/lightning-network-tools/pool/orders.md)).
- **Price paid on a match.** The FAQ says "you will pay the lower of the two prices between the bid and the ask" ([source](../../raw/docs/lightning-network-tools/pool/faq.md)); the batch execution page says all traders in a batch get the same uniform clearing price, and its snapshot example shows an ask at `rate_fixed` 1488 and a bid at 1636 with `matching_rate` 1636 ([source](../../raw/docs/lightning-network-tools/pool/batch_execution.md)).
- **Command spelling.** The node-matching example is printed as `pool order submit bid` (singular `order`), whereas every other example uses `pool orders submit` ([source](../../raw/docs/lightning-network-tools/pool/orders.md)).
- **Positional or flag arguments.** The ask example passes amount and account key positionally (`pool orders submit ask 10000000 0288...`), while the flag table lists `amt` and `acct_key` as required flags ([source](../../raw/docs/lightning-network-tools/pool/orders.md)).
- **Trader key in the example outputs.** The ask is submitted with account key `0288096b...` and the `pool orders list` example shows `trader_key` `024010a5...` ([source](../../raw/docs/lightning-network-tools/pool/orders.md)).
