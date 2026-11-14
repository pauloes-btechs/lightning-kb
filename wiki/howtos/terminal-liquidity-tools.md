---
title: 'Terminal liquidity tools: autofees, autoopen, reports'
type: howto
sources:
  - raw/docs/lightning-network-tools/lightning-terminal/channel-liquidity.md
  - raw/docs/lightning-network-tools/lightning-terminal/opening-channels.md
  - raw/docs/lightning-network-tools/lightning-terminal/recommended-channels.md
  - raw/docs/lightning-network-tools/lightning-terminal/health-checks.md
  - raw/docs/lightning-network-tools/lightning-terminal/ranking.md
  - raw/docs/lightning-network-tools/lightning-terminal/liquidity-report.md
  - raw/docs/lightning-network-tools/lightning-terminal/autofees.md
  - raw/docs/lightning-network-tools/lightning-terminal/autoopen.md
  - raw/docs/lightning-network-tools/lightning-terminal/loop.md
  - raw/docs/lightning-network-tools/lightning-terminal/loop-fees.md
  - raw/docs/lightning-network-tools/lightning-terminal/pool.md
updated: 2026-11-14
---

# Terminal liquidity tools: autofees, autoopen, reports

What the [[lightning-terminal]] interface offers a node operator for opening channels, judging node health, and managing liquidity: recommended channels, health checks, rankings, the liquidity report, Autofees, AutoOpen, and the graphical front ends for [[loop]] and [[pool]]. To get to these screens, first connect a node as described in [[running-litd]].

## Background: inbound and outbound liquidity

For a node to route a payment across the network, it must have channels with both inbound and outbound liquidity. Inbound liquidity is the ability to receive payments, outbound liquidity the ability to send; together they always equal the total capacity of the node. The guide's example: a newly funded 1,000,000 sat channel with Node A starts with 1,000,000 sats of outbound liquidity, and after a direct payment of 100,000 sats to Node A the outbound liquidity is 900,000 sats and the inbound liquidity 100,000 sats. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/channel-liquidity.md))

Users making payments need to regularly replenish outbound liquidity, merchants receiving payments need to regularly replenish inbound liquidity, and routing nodes need liquidity on both sides of their channels as balances shift; adjusting this is known as rebalancing. On Terminal, Loop and Pool are the tools offered for it. See also [[liquidity]] and [[inbound-capacity]]. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/channel-liquidity.md))

## Opening channels

Every active node must have at least one open channel to send or receive payments. The first step to opening a channel is identifying a good peer: a node that is well connected to the rest of the network and maintains a high level of uptime. In most cases, the number of channels a node has with good peers is more important than its total number of channels. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/opening-channels.md))

To open a channel you first need bitcoin; your Lightning node can provide an address to receive it. Once the node has been funded, Terminal can be used to open a channel with any other Lightning node on the network, as long as it is reachable and accepts the channel request. Most node solutions create a public node by default, one that can be viewed on the network graph and used as a routing node. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/opening-channels.md))

The guide notes that it is impossible to know exactly which channels are optimal for earning routing fees at any given time, and stresses trial and error; Terminal's channel recommendation feature is offered as a help in finding peers. See also [[payment-channels]] and [[routing-nodes]]. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/opening-channels.md))

### Recommended channels

A stable peer is one that passes five of six health checks, lacking only the check around the number of good peers. These stable peers are the ones listed as Recommended Channel options in Terminal; additional channels opened towards them can improve their health check status. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/recommended-channels.md))

The list is visible in Terminal as the whole channels card if you have no channels, or underneath your existing channels. If you are shown the list and also pass five of six health checks, your node is likely included in the list of peers suggested to other Terminal users. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/recommended-channels.md))

Opening a recommended channel does not guarantee passing the additional health check. It is also important to capitalize the channel sufficiently and to maintain sufficient incoming and outgoing capacity. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/recommended-channels.md))

## Health checks

Lightning Terminal uses health checks to assess a node's ability to route payments. The guide describes them as a general measure for routing nodes rather than a concrete target: a node configured mainly for receiving or sending payments, such as a merchant's, might not pass them, and a high performing routing node serving the edges of the network might earn more routing fees than one ranked higher. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/health-checks.md))

The six checks:

| Check | What the guide says |
|---|---|
| Node is online | Your node has to be online. Many high performing routing nodes are able to be reachable via Tor. |
| Plenty of channels | Your node needs to have plenty of channels to be considered a good routing node. |
| Good routing capacity | Each channel should have enough capacity to route a reasonably sized Lightning payment in either direction; it does not need to be perfectly balanced. |
| Many healthy channels | Set a reasonably large minimum channel size for incoming connections, and close unused or inactive channels. Channels to merchants that are only periodically online, or from mobile clients, should be set to private. |
| Channel stability | Your channels should be online as much as possible; make sure they are active and monitor them regularly. |
| Many good peers | Your channels should be public and reach out to other good routing nodes. Connecting to other pending nodes can also be of advantage, as this elevates two nodes at once. |

([source](../../raw/docs/lightning-network-tools/lightning-terminal/health-checks.md))

No numeric thresholds for the checks are found in the sources. The guide says the checks are deliberately vague, because a strict and clear ranking mechanism would make nodes more homogenous and the network weaker. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/health-checks.md))

## Rankings

Lightning Terminal ranks nodes by their performance as observed from publicly available information. Important criteria include a node's position in the network graph, its capacity and the quality of its peers. To be considered for the ranking, a node needs to pass six health checks. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/ranking.md))

- **Peers:** for a peer to be considered a good peer, their channel must have sufficient liquidity to route payments.
- **Centrality:** "In-betweenness Centrality" measures how many hypothetical routes pass through your node; results are displayed by percentile.
- **Inbound:** for top nodes, Terminal classifies inbound efficiency, which expresses how easily a node can be reached in terms of cost and time by potential payers. The result is displayed by percentile; being in the 10th percentile means that 9 out of 10 nodes have better inbound capacity. Bright colors mean Terminal is confident about the result; grayed out results indicate low confidence.
- **Capacity:** the sum of the size of all the node's public channels.
- **Age:** determined through the oldest still active public channel of the node.

([source](../../raw/docs/lightning-network-tools/lightning-terminal/ranking.md))

The inbound classes are named as follows in the guide:

| Class | Percentile as written | Meaning |
|---|---|---|
| Hard to Reach | lowest 15 percentile | Cannot be paid easily; routes take time to find or are expensive. If it is your node, you might benefit from reducing your channel balance by making payments, using Loop Out or acquiring additional inbound capacity. |
| Reachable | 15 - 60 percentile | Can be reached in a reasonable amount of time and cost. |
| Easy to Reach | highest 60 percentile | Can easily receive payments at low cost. |

([source](../../raw/docs/lightning-network-tools/lightning-terminal/ranking.md))

## Liquidity report

In Lightning Terminal, navigate to "Loop" and click "Liquidity Report" on the top right side. For various simulated payment sizes, it shows the estimated fee somebody paying to your node would have to pay. The "Routable Liquidity" graph shows how many channels you can get paid through at several fee levels, as an ordinary or cumulative histogram. The "Routable Inbound" graph places your channels into fee buckets and shows for each bucket how many channels have liquidity available. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/liquidity-report.md))

Fee ranges marked in red ("Needs Attention") indicate that no channels in that fee range have sufficient inbound capacity left. You may empty these channels by pushing satoshis out, for example into cold storage using Lightning Loop, or alternatively close them. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/liquidity-report.md))

The guide's advice: attempt to free up additional capacity first, for instance through Loop, and only close channels that cannot be emptied otherwise; maximize the percentage of channels that have inbound capacity rather than the number of channels; keep channels open so their cost is amortized over multiple cycles. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/liquidity-report.md))

Limitation: for now the report only takes into account local information gathered directly from your node. It orders available inbound capacity by remote fee but does not take into account the quality of that capacity, for example where the peer itself lacks inbound capacity. See also [[merchant-liquidity]]. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/liquidity-report.md))

## Autofees

Autofees sets fees for your channels based on how much they earn. It is available starting with litd v0.8.6 and the accompanying Lightning Terminal web release. By opting in, you give Terminal permission to remotely read some information from your node and use it to programmatically set outbound fees, for all channels or only some. Once enabled, the node automatically creates a new dedicated [[lightning-node-connect]] session with its own macaroon through which fees are set. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/autofees.md))

### The algorithm

- Terminal uses the forwarded traffic of the top five earning peers over 60 days as a reference for the entire node, to determine a target throughput per peer.
- If a channel's forwarded traffic is lower than the target throughput, Terminal lowers fees; if it is higher, fees are increased.
- Each adjustment is made in small increments once every three days, a tradeoff to limit gossip data on the network.
- As a channel sees 7/8th of its liquidity depleted, fees are mildly raised to signal scarcity.
- It runs purely on historical forwarding data, current channel balancedness, and charged relative routing fees provided by LND, without a state or database on the litd side.

([source](../../raw/docs/lightning-network-tools/lightning-terminal/autofees.md))

### Security and privacy

Enabling Autofees creates an additional session with the Autofees server that is only allowed to access forwarding data, channel balances, and fee rate policies, with write permissions limited to setting new fee policies. The session is visible in litd and can be revoked at any time. Rules enforced by litd limit access to forwarding data to 60 days into the past, limit the feature to a predetermined frequency, and cap algorithmically set fee rates with maximum values. The APIs involved are described in [[lit-autopilot]] and [[lit-firewall]]. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/autofees.md))

Channel ids, channel points and node pubkeys are obfuscated by `litd` through a system called the "Privacy Mapper"; amounts and timestamps in forwarding data are randomly obfuscated, and channel details only include randomized balance information. Per-peer aggregated forwarding data is stored to improve the algorithm in the future. The privacy mapper can be used manually for debugging: `litcli privacy` can convert both strings and uint64 to the pseudo counterpart and back. More in [[terminal-privacy-and-security]]. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/autofees.md))

Warning from the guide: enabling Autofees will set your channels' CLTV delta to 100. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/autofees.md))

### Configuration

Add the following to your `lnd.conf` file to enable the RPC middleware interceptor (see [[lnd-interceptors]]):

```
rpcmiddleware.enable=true
```

Then enable Autofees in Lightning Terminal under Liquidity -> Loop. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/autofees.md))

The guide's recommendations for using it well:

- Set default high fee rates, so they can be lowered later without risk of seeing a channel depleted without adequate compensation (suggested value `bitcoin.feerate=2500` in your lnd.conf). See [[lnd-channel-fees]].
- Only enable Autofees for peers you do not know an accurate price of. For some peers, for example Loop, you can keep manually set fees.
- Manual intervention in fee setting is possible.
- Avoid restarting Autofees, as a new session is created every time and there may be false double accounting for overlapping periods.

([source](../../raw/docs/lightning-network-tools/lightning-terminal/autofees.md))

## AutoOpen

AutoOpen opens new channels for the node runner, and together with Autofees is part of Lightning Terminal's Autopilot feature. When enabled, it lets a node runner assign a budget, specify a time preference, define a minimum and maximum channel size, and optionally pass node pubkeys of preferred peers. It then targets a suitable point in time to batch open channels to save on fees. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/autoopen.md))

To use it, connect to Lightning Terminal and navigate to Autopilot under the Loop menu. The "speed" selector defines how sensitive AutoOpen should be to high onchain fees. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/autoopen.md))

How it chooses:

- New channels are selected to improve the node's reach into the network, measured with betweenness centrality: how many paths between any two other nodes go through the node in question.
- It looks at the node's channel size distribution and whether it overlaps with that of the new peer. The channel size is determined using your node's channel size, your peer's channel sizes and your specified limits.
- It looks for low fee next block targets, compared to long term block fee history, to decide when to open.
- It sets the initial outbound fees for the new channel, using the fee rates of the new peer.
- It does not close channels.

([source](../../raw/docs/lightning-network-tools/lightning-terminal/autoopen.md))

Data shared: when enabling AutoOpen you share your node's public key as well as your current and past channels. This lets AutoOpen determine your position in the graph and avoid peering you with nodes you previously had channels with. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/autoopen.md))

## Loop in Terminal

Terminal offers a graphical interface for [[loop]]: Loop Out makes a Lightning transaction to an on-chain Bitcoin address, Loop In sends on-chain Bitcoin directly into a Lightning channel. The command-line equivalents are in [[using-loop]], and the mechanism in [[submarine-swaps]]. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/loop.md))

Clicking 'Loop' at the top of Terminal shows an overview of your channels and their balances. Sliding the bar to the left decreases the Lightning balance in return for onchain funds (Loop Out); a Loop In refills channels from the onchain balance. Individual channels can be selected, and a warning appears if the minimum swap size is not met. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/loop.md))

For a one-off swap choose *Loop*. A summary shows a breakdown of the fees, including the expected onchain fee and the Loop fee. For Loop Outs, a prepayment of 30,000 satoshis is required. In the additional options you can choose the confirmation speed (in blocks; more blocks meaning lower fees) and enter an external address, for example for cold storage. Clicking "Submit" submits the Loop. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/loop.md))

- **Loop In:** the Loop server probes whether it can make an off-chain payment of the selected size to your node. If the probe succeeds, Terminal instructs your node to send on-chain funds to the swap address; once this is confirmed, the off-chain payment is made to your node.
- **Loop Out:** your node probes whether it can reach the Loop node with a payment of the chosen size. If so, the Loop server sends the funds to a 2-of-2 multisignature contract. Once confirmed, Terminal instructs your node to make the off-chain payment; when it succeeds and Terminal has the preimage, your node automatically sweeps the funds from the contract.

([source](../../raw/docs/lightning-network-tools/lightning-terminal/loop.md))

After a Loop Out, the Dashboard shows three new transactions: the 30,000 satoshi prepayment (forfeited if the off-chain transaction is not made), one over the full amount, and a third on-chain transaction sending the funds to your wallet, or to the external address if one was specified. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/loop.md))

### Loop status and failures

| Status | Meaning |
|---|---|
| Initiated | Your node or Loop verifies it can make an off-chain payment to the other side. Swaps most commonly fail here, due to lack of liquidity along the route. If a swap fails at this stage, you are not charged any fees. |
| Preimage revealed | The on-chain transaction is made to the swap contract; once confirmed, the recipient of the off-chain payment reveals the preimage and claims the off-chain funds. If the Loop fails at this stage, the sender of the on-chain funds has to sweep them back: for a Loop In this costs you transaction fees, for a Loop Out you are charged a fee by Loop through a Lightning payment. This most commonly happens if the user goes offline or turns off litd or loopd during the swap. |
| Success | Both parties have received their funds. |

([source](../../raw/docs/lightning-network-tools/lightning-terminal/loop.md))

Loops primarily fail because of missing liquidity between you and the Loop node. On failure, try a different channel or a lower amount. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/loop.md))

### Autoloop in Terminal

Autoloops can be configured for specific peers or the node as a whole: after moving the slider at the top (or on a specific channel), select Autoloop. You can set a minimum Loop size, a maximum fee per swap measured in BPS (1 BPS = 100 PPM = 0.01%), and a maximum budget per day, week or month. Loop Outs can be sent to an external address. Once configured, previous Loops and the current status appear under the channel for which it has been activated, where the rule can also be removed. The CLI version is covered in [[autoloop]]. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/loop.md))

### Loop fees

The fee guide applies equally to Loop through the command line. The Loop service charges a fee on top of the on-chain and off-chain fees the transactions incur naturally. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/loop-fees.md))

Loop Out, estimated before confirming:

| Item | Description |
|---|---|
| L402 | On your first Loop your node purchases an [[l402]]. It does not expire and costs 1 satoshi. |
| Estimated on-chain fee | Miner fee to claim your bitcoin from the HTLC address into your wallet. Based on current conditions; larger transaction sizes do not increase it, but faster desired confirmation times do. |
| Loop service fee | Charged by the Loop service for the swap; depends on current on-chain fees. |
| No show penalty | A pre-payment of 30,000 sats, counted towards the Loop Out and forfeited if the final payment is not made. |

([source](../../raw/docs/lightning-network-tools/lightning-terminal/loop-fees.md))

In the guide's Loop Out example of 300,000 satoshis, the estimate was 1,312 satoshis. The actual fees seen under History were: off-chain routing fees of 1,088 + 65 = 1153 sat on the two outgoing payments (one over 30,000 satoshis, the other over the remaining swap amount plus the Loop service fee), 416 sat on-chain to sweep the HTLC, and 500 sat to Loop. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/loop-fees.md))

Loop In, estimated before confirming: the estimated on-chain fee to publish your transaction (which can be significantly higher if the wallet has to bundle multiple utxos), and the Loop service fee, which includes the on-chain fees to sweep the HTLC and the off-chain fees for Loop's payment to you. In the guide's example the Loop service fee came to 1,456 sats. If a Loop In fails after the on-chain transaction is confirmed, you have to make another on-chain transaction to sweep the HTLC yourself. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/loop-fees.md))

## Pool in Terminal

Terminal offers a graphical interface for [[pool]], a non-custodial marketplace for channels, to buy, sell or redeem channels. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/pool.md))

**Open an account.** Navigate into Pool and click 'Open an Account' on the left bar; this needs funds in LND's on-chain wallet. You define how much to commit, how long to lock the funds up, and how fast to open the account. To sell channels, the account must cover the capacity of the channels you intend to sell; to only buy, it only needs to cover the fees. To authenticate the account to the Pool server, the node purchases an LSAT for 1000 satoshis over the Lightning Network. See [[pool-accounts]]. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/pool.md))

**Custody.** The Pool account is a 2-of-2 multisignature contract on the Bitcoin blockchain. It is time-locked: after a pre-determined time you can withdraw unilaterally, and it can be closed cooperatively anytime before. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/pool.md))

**The auction.** Pool performs a batched, uniform clearing-price auction: all bids and asks are collected every ten minutes and cleared at the same price. A batch can happen at most once per block, but not every block needs to have a batch in it. Bids made in the Pool UI are private by default, while bids made with Pool Lite or the CLI can be private or public. See [[pool-orders-and-batches]]. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/pool.md))

**Bids and asks.** A bid offers to pay for inbound liquidity; an ask sells a channel lease to earn yield. For each you define the liquidity, the fee, on-chain fees and minimum channel size; for bids you can also specify whether to accept channels from nodes not ranked on Lightning Terminal. To sell liquidity you need to be 'ranked,' meaning considered a Tier 1 (T1) node; the node tier is shown in the top right corner. Orders appear in the 'Orders' list and filled leases under 'Filled channel leases.' The guide warns not to close leased channels before their duration has elapsed. See [[pool-channel-leases]]. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/pool.md))

**Sidecar channels.** It is not yet possible to buy sidecar channels through Terminal, but those ordered for you by others can be redeemed: click 'Loop,' then "Add Liquidity," and use 'Register a Sidecar channel' on the right to enter the sidecar ticket. See [[sidecar-channels]]. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/pool.md))

**Pool Lite.** A simplified order book that visualizes the current market and lets you match with specific public orders ("Order Book", then Buy/Sell) or submit public and private bids. It needs a regular Pool account. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/pool.md))

## Conflicts

- **Inbound percentile bands.** The ranking guide labels "Reachable" as "15 - 60 percentile" and "Easy to Reach" as "highest 60 percentile", which taken literally overlap; the same page defines the scale by saying the 10th percentile means 9 out of 10 nodes have better inbound capacity ([source](../../raw/docs/lightning-network-tools/lightning-terminal/ranking.md)).
