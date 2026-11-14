---
title: Autoloop
type: howto
sources:
  - raw/docs/lightning-network-tools/loop/autoloop.md
  - raw/docs/lightning-network-tools/loop/the-loop-cli.md
  - raw/api/api-docs/api/loop/swap-client/get-liquidity-params.md
  - raw/api/api-docs/api/loop/swap-client/set-liquidity-params.md
  - raw/api/api-docs/api/loop/swap-client/suggest-swaps.md
  - raw/api/api-docs/api/loop/debug/force-auto-loop.md
updated: 2026-11-14
---

# Autoloop

Autoloop lets [[loop]] dispatch Loop Out and Loop In swaps automatically, according to a set of rules configured for your node's channels, within a budget of your choosing. It is disabled by default and is enabled with `loop setparams --autoloop=true`. It is a tool for managing [[liquidity]]; manual swaps are covered on [[using-loop]]. ([source](../../raw/docs/lightning-network-tools/loop/autoloop.md))

Autoloop parameters and rules are not persisted, so they must be set on restart. The guide recommends running `loopd` with `--debuglevel=debug` when using this feature. ([source](../../raw/docs/lightning-network-tools/loop/autoloop.md))

## Easy Autoloop

Easy Autoloop only requires the overall channel balance that you don't wish to exceed on your node. To keep the node's total channel balance below 1 million satoshis:

```
loop setparams --autoloop=true --easyautoloop=true --localbalancesat=1000000
```

This starts dispatching loop-outs whenever the total channel balance exceeds 1M sats. On first use it uses the default budget parameters. Easy Autoloop is currently only available for Loop Out, meaning any amount above `--localbalancesat` is expected for Loop Out. ([source](../../raw/docs/lightning-network-tools/loop/autoloop.md))

## Liquidity rules

Autoloop can be configured either to acquire incoming liquidity using Loop Out or to acquire outgoing liquidity using Loop In; it cannot support automated swaps in both directions. The type is set with `loop setparams --type=<in|out>`, and Autoloop performs loop out swaps by default. ([source](../../raw/docs/lightning-network-tools/loop/autoloop.md))

Swaps dispatched by Autoloop can be identified in the output of `ListSwaps` by their label field, which will contain `[reserved]: autoloop-out`. ([source](../../raw/docs/lightning-network-tools/loop/autoloop.md))

Even without enabling Autoloop, the client logs the actions it would have taken once the parameters are set. The `SuggestSwaps` rpc (`loop suggestswaps` on the CLI) provides the set of swaps that Autoloop currently recommends, which can be used to execute swaps manually. ([source](../../raw/docs/lightning-network-tools/loop/autoloop.md))

Targets: Autoloop can manage liquidity for individual channels, peers, or the node as a whole. Peer-level management examines the liquidity balance of all the channels you have with a peer; node-level management examines the balance of the entire node. ([source](../../raw/docs/lightning-network-tools/loop/autoloop.md))

Thresholds: the desired balance is expressed as threshold incoming and outgoing percentages of capacity. The incoming threshold is the minimum percentage of capacity that you would like in incoming capacity. The outgoing threshold reserves a percentage of your balance for outgoing capacity and may be set to zero. Autoloop performs swaps that push incoming capacity to at least the incoming threshold while reserving at least the outgoing threshold. ([source](../../raw/docs/lightning-network-tools/loop/autoloop.md))

```
loop setrule <short channel id/ peer pubkey> --incoming_threshold=<minimum % incoming> --outgoing_threshold=<minimum % outgoing>
loop setrule <short channel id/ peer pubkey> --clear
```

The first form sets a rule; the second clears it. ([source](../../raw/docs/lightning-network-tools/loop/autoloop.md))

## On-chain addresses

To avoid address reuse, Autoloop can conduct each swap into a new, previously unused on-chain address derived from an extended public key (xpub). The xpub of a wallet created with external software is first imported into LND as a watch-only wallet (any account name may be used instead of `my_loop_account`, and multiple extended public keys may be imported); the account can then be specified for individual Loop Outs or set in the Autoloop parameters. See also [[lnd-wallet-and-psbt]]. ([source](../../raw/docs/lightning-network-tools/loop/autoloop.md))

```
lncli wallet accounts import <xpub...> my_loop_account --address_type p2tr --master_key_fingerprint <fingerprint>
loop setparams --autoloop=true --account=my_loop_account --account_addr_type=p2tr
```

([source](../../raw/docs/lightning-network-tools/loop/autoloop.md))

## Fees

The fees an automatically dispatched swap consumes can be limited to a percentage of the swap amount with `loop setparams --feepercent=<percentage of swap amount>`. For finer control there are separate settings, all expressed per swap rather than as an overall budget:

| Setting | Command | What it limits |
| --- | --- | --- |
| Sweep confirmation target | `loop setparams --sweepconf=<target in blocks>` | the number of blocks within which the HTLC is swept back to your wallet, used to estimate on-chain fees |
| Sweep fee limit | `loop setparams --sweeplimit=<limit in sat/vbyte>` | Autoloop only dispatches when the fee estimate for the sweep is below this limit |
| Miner fee | `loop setparams --maxminer=<limit in satoshis>` | cap on the amount paid for the sweep if fees spike after dispatch |
| Swap fee | `loop setparams --maxswapfee=<percentage of swap volume>` | the server's fee for facilitating the swap |
| No-show fee | `loop setparams --maxprepay=<limit in satoshis>` | the fee the server charges to recoup its on-chain costs in case of a no-show |
| Prepayment routing fee | `loop setparams --maxprepayfee=<percentage of prepay amount>` | off-chain fees for the swap prepayment |
| Swap routing fee | `loop setparams --maxroutingfee=<percentage of swap amount>` | off-chain fees for the swap payment |

([source](../../raw/docs/lightning-network-tools/loop/autoloop.md))

The time to acquire incoming liquidity does not depend on the sweep confirmation time, so the guide recommends a very large sweep confirmation target (up to 250 blocks) so that the sweep can go through with very low fees. ([source](../../raw/docs/lightning-network-tools/loop/autoloop.md))

The no-show fee is only charged if the client goes offline for a long period after the server has published an on-chain HTLC and never completes the swap, or if it decides to abort the swap due to high on-chain fees. ([source](../../raw/docs/lightning-network-tools/loop/autoloop.md))

The loop client dispatches two off-chain payments to the loop server, one for the swap prepayment and one for the swap itself. ([source](../../raw/docs/lightning-network-tools/loop/autoloop.md))

## Budget

Autoloop operates within a set budget and stops executing swaps when the budget is reached. The budget includes the fees paid to the swap server, on-chain sweep costs and off-chain routing fees; it does not include the swap amount itself. It is expressed in satoshis and refreshed on a configurable interval:

```
loop setparams --autobudget=<budget in satoshis>
loop setparams --autobudgetrefreshperiod=<duration in seconds>s
loop setparams --autobudget=100000 --autobudgetrefreshperiod=604800s
```

The last line is the guide's example of a budget of 100k sats per 7 days (604800 seconds). A used-up budget can be topped up by increasing the budget amount or by decreasing the refresh interval. ([source](../../raw/docs/lightning-network-tools/loop/autoloop.md))

## Dispatch control

In flight limit: the number of swaps Autoloop dispatches at a time is controlled by the `autoinflight` parameter, whose default value is 1, for example `loop setparams --autoinflight=2`. Autoloop waits for a swap to fully complete, including the sweep confirming, before it dispatches another. ([source](../../raw/docs/lightning-network-tools/loop/autoloop.md))

Failure backoff: Loop Out swaps sometimes fail because they cannot find an off-chain route to the server. These attempts cost nothing, but a backoff period keeps Autoloop from continuously retrying a channel that cannot facilitate a swap. The guide gives the default as 24 hours; it is updated with `loop setparams --failurebackoff=<backoff in seconds>`. ([source](../../raw/docs/lightning-network-tools/loop/autoloop.md))

Swap size: by default, Autoloop executes a swap when the amount that needs to be rebalanced within a channel equals the swap server's minimum swap size. A larger minimum can be set with `loop setparams --minamt=<amount in satoshis>`, which performs fewer swaps but lets channels drop further below their threshold. Swaps are also limited to the server's maximum swap amount, which can be reduced with `loop setparams --maxamt=<amount in satoshis>`. Both values must be within the range the server supports, as shown by `loop terms`. ([source](../../raw/docs/lightning-network-tools/loop/autoloop.md))

## Manual swap interaction

Autoloop will not dispatch swaps over channels that are already included in manually dispatched swaps: for Loop Out, when the channel is specified in the outgoing channel swap, and for Loop In, when the channel's peer is specified as the last hop of an ongoing swap. ([source](../../raw/docs/lightning-network-tools/loop/autoloop.md))

## Disqualified swaps

A channel that is not eligible for a swap, or does not need one under the current rules, is listed in the `Disqualified` section of the output of the `SuggestSwaps` API with one of these reasons:

| Reason | Meaning |
| --- | --- |
| Budget not started | the start date for the budget is in the future |
| Budget elapsed | Autoloop has elapsed the budget assigned to it for fees |
| Sweep fees | the estimated chain fee rate for sweeping a loop out swap is higher than the current limit |
| In flight | the limit on the number of automatically dispatched swaps has been reached |
| Budget insufficient | there is budget remaining, but not enough to execute a specific swap, counting the amount reserved for in flight swaps |
| Swap fee | the fees advertised by the server are too high |
| Miner fee | the estimated on-chain fees for a swap are too high |
| Prepay | the no-show fee is too high |
| Backoff | an automatically dispatched swap has recently failed for the channel |
| Loop out | there is currently a loop out swap in-flight on the channel |
| Loop in | there is currently a loop in swap in-flight for the peer |
| Liquidity ok | the channel's liquidity balance is within the bound set by its rule; no action is required |
| Fee insufficient | the fees a swap will cost are more than the allowed percentage of the total swap amount |
| Loop in unreachable | the client node is unreachable by the server off-chain |

Further details for all of these reasons can be found in loopd's debug level logs. ([source](../../raw/docs/lightning-network-tools/loop/autoloop.md))

## API

The parameters are read with GetLiquidityParams and written with SetLiquidityParams on [[loop-swap-client]]; both are marked "[EXPERIMENTAL]: endpoint is subject to change". Both use the `LiquidityParameters` message, whose fields include `autoloop`, `autoloop_budget_sat`, `autoloop_budget_refresh_period_sec`, `auto_max_in_flight`, `failure_backoff_sec`, `easy_autoloop`, `easy_autoloop_local_target_sat`, `fee_ppm`, `min_swap_amount`, `max_swap_amount` and `rules`. ([source](../../raw/api/api-docs/api/loop/swap-client/get-liquidity-params.md))

SetLiquidityParams fully overwrites the existing parameters, so the full set of parameters must be provided on each call. ([source](../../raw/api/api-docs/api/loop/swap-client/set-liquidity-params.md))

SuggestSwaps returns a list of recommended swaps based on the current state of the node's channels and its liquidity manager parameters; its response has `loop_out`, `loop_in`, `static_loop_in` and `disqualified`. The page notes that only loop out suggestions are currently supported. ([source](../../raw/api/api-docs/api/loop/swap-client/suggest-swaps.md))

For testing, ForceAutoLoop on [[loop-debug]] ticks the autoloop timer, triggering automated dispatch of a swap if one is suggested; it will not work on mainnet. ([source](../../raw/api/api-docs/api/loop/debug/force-auto-loop.md))

## Conflicts

- Default failure backoff: the Autoloop guide says "The default value for this parameter is 24 hours" ([source](../../raw/docs/lightning-network-tools/loop/autoloop.md)), while the Loop CLI guide lists `--failurebackoff` with `(default: 0)` ([source](../../raw/docs/lightning-network-tools/loop/the-loop-cli.md)).
- Loop In suggestions: the Autoloop guide says Autoloop can be set to dispatch loop in swaps with `--type=<in|out>` ([source](../../raw/docs/lightning-network-tools/loop/autoloop.md)), while the SuggestSwaps page says "only loop out suggestions are currently supported" although its response has `loop_in` and `static_loop_in` fields ([source](../../raw/api/api-docs/api/loop/swap-client/suggest-swaps.md)).

## Notes

Synthesis: the guide's prose calls the sweep confirmation target `sweepconftarget` in one place, but the command it gives is `--sweepconf`. The guide expresses fee limits as percentages on the CLI, while the `LiquidityParameters` fields are named in parts per million (`fee_ppm`, `max_swap_fee_ppm`); the sources do not state how the CLI converts between them.
