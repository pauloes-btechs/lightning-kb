---
title: 'Liquidity: inbound, outbound and managing it'
type: concept
sources:
  - raw/docs/the-lightning-network/liquidity.md
  - raw/docs/the-lightning-network/liquidity/understanding-liquidity.md
  - raw/docs/the-lightning-network/liquidity/manage-liquidity.md
updated: 2026-11-14
---

# Liquidity: inbound, outbound and managing it

In business, liquidity usually refers to the ability to meet short-term obligations; in markets, to the ability to trade assets at a given price. In the Builder's Guide, liquidity refers to the ability to move funds, which is an important concept for routing payments in the Lightning Network. To route payments and collect routing fees, you want your funds to be as liquid as possible, or otherwise be compensated for the illiquidity. ([source](../../raw/docs/the-lightning-network/liquidity.md))

The same satoshis held in a node may provide liquidity to its owner while simultaneously consuming the liquidity of others, or vice versa. In general, a node should expect to be compensated for providing liquidity while paying others to provide it with liquidity. The guide calls appropriately pricing liquidity, and building a reliable and efficient market around it, one of the biggest challenges of the Lightning Network. ([source](../../raw/docs/the-lightning-network/liquidity/understanding-liquidity.md))

## Pages in this section

- [[inbound-capacity]]: Getting inbound capacity
- [[lightning-service-providers]]: Lightning service providers
- [[merchant-liquidity]]: Liquidity management for merchants

## On-chain liquidity

An on-chain bitcoin transaction can be moved at any time for a predictable, but varying fee. The proposed fee does not guarantee inclusion in a block; it is a bid in a perpetual auctioning process in which miners pick the highest fee paying ~2MB worth of transactions from the mempool. Blocks are created on average every 10 minutes. ([source](../../raw/docs/the-lightning-network/liquidity/understanding-liquidity.md))

On-chain bitcoin require multiple confirmations by the Bitcoin network to be considered settled. Unless they are 'locked' in special addresses, they can be spent at any time and confirmed within an hour if an appropriate fee is set. ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))

Unilateral channel closures (force closes) have their own liquidity properties. Typically, the party initiating the force close has to wait to spend their bitcoin, while the other side can spend their funds immediately. The length of the waiting period is defined when the channel is opened and can range from just a day to a few weeks. A force close may be the only way to retrieve funds from an "illiquid" channel if a peer has not been online for a while; it can also be requested by the peer in case of data loss, or be the result of an HTLC that has to be settled on-chain. ([source](../../raw/docs/the-lightning-network/liquidity/understanding-liquidity.md))

A Lightning node is able to receive and send on-chain bitcoin: `lncli newaddress` generates a new Bitcoin address, `lncli walletbalance` checks the balance, and `lncli sendcoins` sends Bitcoin from the wallet, in the format `lncli sendcoins [command options] addr amt`. ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))

Tips the guide gives for `lncli sendcoins` ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md)):

- The `amt` value is denominated in satoshi. One bitcoin equals 100 million satoshi. ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))
- To spend the entire balance, set the option `--sweepall` and omit the `amt` value. ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))
- The fee rate, in sat/vbyte, is defined with the option `--sat_per_byte` (`--sat_per_vbyte` from `lnd 0.13.0`). ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))
- Instead of a fee you can set `--conf_target`, the number of blocks within which you expect the transaction to be confirmed. ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))
- A memo for the transaction is recorded with the `--label` option. ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))

Example transactions from the guide ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md)):

```
lncli sendcoins --sat_per_byte 10 --label savings bc1qaxcxcpunn6ns3gpu6ywcy57tcmy2vsjzwdklxr 100000
lncli sendcoins --sweepall --conf_target 6 bc1qaxcxcpunn6ns3gpu6ywcy57tcmy2vsjzwdklxr
```

Advanced users can send to many addresses at once with `lncli sendmany`, which takes a json string of the format `{"ExampleAddr": NumCoinsInSatoshis, "SecondAddr": NumCoins}`. ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))

## Liquidity in channels

Lightning channels are two-of-two multisignature contracts that hold a certain amount of bitcoin on the Bitcoin blockchain. They also include a refund transaction that can be broadcast by either party to close the channel at any time. See [[payment-channels]]. ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))

The guide speaks of outbound channels when the node in question initiated the channel, and inbound channels when another party opened it. This does not imply whether the funds in that channel are held by one peer or the other. ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))

Funds held in channels are in some ways more liquid than on-chain bitcoin, because they can be spent instantly and typically at a lower fee. However, if a channel is offline, the funds in it need to be retrieved through a non-cooperative close, which might make them unavailable, and illiquid, for a longer period of time. ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))

The liquidity of a channel balance can also depend on the peer. If you open a channel with node A, and that is the only channel node A has, the funds inside that channel can only be spent to node A and not to any other node in the network. The same can happen if node A has no funds of their own, e.g. only inbound channels. ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))

### Local and remote balance

Your local balance includes your reserve and the amount of satoshis you can spend, while your remote balance shows how much you can receive through that channel. Your local balance is your peer's remote balance, and vice versa. As you spend satoshis on the Lightning Network, your local balance becomes your remote balance. When routing payments, you receive on one channel while sending in another: remote balance in one channel becomes local balance, and vice versa in the other channel. ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))

The guide equates local balance with outbound capacity (your own funds, e.g. the bitcoin deposited into a new channel) and remote balance with inbound capacity (your ability to receive payments, or route incoming payments, in that channel). How to obtain the latter is covered on [[inbound-capacity]]. ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))

`lncli listchannels` lists all your channels; the list can be restricted with the arguments `--active_only`, `--inactive_only`, `--public_only`, `--private_only` or by `--peer` value. `lncli getchaninfo`, followed by the compact channel ID of the channel, gives information related to routing policies for a specific channel. The lifetime and uptime parameters in the output of `lncli listchannels` tell how long a channel has been online since the last restart of lnd. ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))

## Different nodes, different liquidity needs

Depending on the primary use case, a node may be optimized differently: primarily to make payments, to receive payments, or to earn fees by routing payments for other users. Liquidity needs differ based on that decision. ([source](../../raw/docs/the-lightning-network/liquidity/understanding-liquidity.md))

### Making payments

For someone primarily making payments, liquidity is largely a matter of whether funds are held in well-connected channels. It might make sense to open a channel with the entity you most frequently transact with, or to identify a good routing node that can reach those counterparties (see [[routing-nodes]]). ([source](../../raw/docs/the-lightning-network/liquidity/understanding-liquidity.md))

It might make sense to open fewer, larger channels rather than spreading funds across multiple smaller peers. On the other hand, if all funds are concentrated in a single channel, the satoshis could temporarily become illiquid if the peer goes offline or a channel is closed. ([source](../../raw/docs/the-lightning-network/liquidity/understanding-liquidity.md))

For a node solely used for making payments, it may be appropriate to open private channels, i.e. channels that are not announced to the network and therefore cannot be used for routing. ([source](../../raw/docs/the-lightning-network/liquidity/understanding-liquidity.md))

When channels need to be replenished, it might be most cost effective to fill them directly via the Lightning Network, for example by earning satoshis or withdrawing BTC from exchanges using Lightning. Alternatively, Lightning Loop is a service that allows you to send on-chain Bitcoin directly into a Lightning channel (Loop In); see [[loop]]. ([source](../../raw/docs/the-lightning-network/liquidity/understanding-liquidity.md))

### Receiving funds

For a node used mainly to receive funds, the term liquidity is synonymous with inbound capacity. It needs to maintain channels with well connected peers, but keep its balance in those channels to a minimum. This might require incentivizing others to open channels to it; the guide names buying inbound capacity through Lightning Pool, a non-custodial marketplace where users can purchase inbound liquidity from node operators, as the easiest way. See [[pool]] and [[inbound-capacity]]. ([source](../../raw/docs/the-lightning-network/liquidity/understanding-liquidity.md))

It may be advantageous to empty out existing channels rather than opening new ones, and as long as the node is not used for routing payments, its channels may be private. ([source](../../raw/docs/the-lightning-network/liquidity/understanding-liquidity.md))

### Routing

A routing node provides liquidity to others and, as such, is required to have both inbound and outbound capacity. Ideally, each channel has some inbound and some outbound capacity, each large enough for a reasonably large payment. ([source](../../raw/docs/the-lightning-network/liquidity/understanding-liquidity.md))

There need to be mechanisms, automated or manual, to analyze the capacity of the channels, assess the traffic to each channel, and rebalance these channels. This requires setting appropriate fees that make the rebalancing worthwhile; see [[channel-fees]]. ([source](../../raw/docs/the-lightning-network/liquidity/understanding-liquidity.md))

A routing node primarily has public channels, but it may also accept private channels from others who primarily use the Lightning Network to make and receive payments. Satoshis in such private channels with mobile nodes are liquid from the perspective of the private node, but highly illiquid for the routing node, and should not be counted towards the sending and receiving capacity of the routing node: it only has the option to force-close the channel or wait until the peer comes online for a cooperative close. Such private channels can however be a great source of routing income, especially when the peer both spends and receives regularly. ([source](../../raw/docs/the-lightning-network/liquidity/understanding-liquidity.md))

A channel to a node set up primarily to receive payments might appear unbalanced and consume significant capital, yet function as intended by providing the routing node with stable income from routing fees. Depending on the traffic to such a merchant, it may be appropriate to replace the channel with a larger or smaller one. ([source](../../raw/docs/the-lightning-network/liquidity/understanding-liquidity.md))

In addition to understanding the liquidity needs of your own node, the guide says it is important to understand the needs of your peers, such as whether they are primarily spending, receiving or routing funds. ([source](../../raw/docs/the-lightning-network/liquidity/understanding-liquidity.md))

## Managing channels with lnd

### Opening a channel

To open a channel you need bitcoin. Typically it is deposited into the Lightning node first, but it is also possible to fund a channel from a Partially Signed Bitcoin Transaction (PSBT)-compatible wallet or a raw signed transaction. A channel can be opened with any other Lightning node, as long as it is online and accepts the channel request. ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))

The command is `lncli openchannel`, in the format `lncli openchannel [command options] node-key local-amt push-amt`. Tips from the guide ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md)):

- Before opening a channel with a remote peer, you may connect to it using `lncli connect <pubkey>@<host>`. ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))
- The fee can optionally be set manually with `--sat_per_byte` or `--conf_target`. ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))
- `--local-amt` is typically used to define both your share of the channel and its full capacity. With `--push-amt` it is possible to send satoshis directly to the peer's node; this is equivalent to making a payment to the peer, and the guide does not recommend using the `--push-amt` flag. ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))
- The flag `--private` prevents a channel from being announced to the network. Funds cannot be routed through such a channel, but it can be used to send and receive satoshis. ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))
- When the `--close_address` option is set, bitcoin from a cooperative close is not sent to your internal wallet, which is useful when using an external wallet for funding. ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))
- The source says the `--pbst` argument can be used to create a channel directly from an external wallet. ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))

Example usage from the guide ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md)):

```
lncli openchannel 021c97a90a411ff2b10dc2a8e32de2f29d2fa49d41bfbb52bd416e460db0747d0d 1000000
lncli openchannel --sat_per_byte 21 --local-amt 800000 --close_address bc1qsltz4tt23k0825q76ylj5mt0gwenlm8wr7umkl 021c97a90a411ff2b10dc2a8e32de2f29d2fa49d41bfbb52bd416e460db0747d0d
```

`lncli pendingchannels` shows whether a channel is pending confirmation. ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))

### Rebalancing

As a node routes payments, its channels may become unbalanced, meaning the local and remote balance become skewed. Channels are commonly balanced by making a payment to yourself through a circular path that spends local balance from channels with high balances to those with lower balances. ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))

Balancing channels is time intensive and comes at a cost. The guide advises making sure that rebalancing does not cost more than was earned routing through the channel since the last rebalancing. ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))

To balance manually, first identify the two channels: the one with a large local balance becomes the first channel in the route, and the one with a large remote balance becomes the last. Balancing can be done manually through the command line or with an external tool; the guide links to rebalance-lnd and balanceofsatoshis. ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))

### Monitoring with Faraday

Faraday is a tool to help identify non-productive channels and more efficiently allocate capital. It comes bundled with Lightning Terminal and can be installed separately, either on the same machine as the node or in a remote location. See [[faraday]], [[using-faraday]] and [[lightning-terminal]]. ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))

`frcli revenue` produces a revenue report for the channels, showing for each channel how many satoshis have been routed inbound or outbound. A significant imbalance means the channel has been drained and might need to be replenished, either through an incoming transaction, e.g. Loop In, or by rebalancing with another channel. The parameter `fees_incoming_msat` may help identify channels that contribute to routing earnings. The report is generated for each channel pair and can be narrowed down to an individual channel and a limited time frame. ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))

`frcli insights` gives a different report for each channel: how many satoshis have been routed through it, fees generated, and channel metrics comparisons measured in `per_conf`, meaning per block that the channel has been alive. ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))

### Closing channels

Reasons the guide gives for closing channels include deploying capital elsewhere, channels not routing enough payments, and capital tied up in channels that are frequently offline. `lncli closechannel` closes a channel in one of two ways: a cooperative close, where both peers are online at the time of closing, or a force close, which is unilateral and uncooperative. The format is `lncli closechannel [command options] funding_txid [output_index]`. ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))

In a cooperative close both nodes sign a new commitment transaction and publish it to the network. The resulting on-chain funds become available for a new channel opening almost immediately. The fee can be set with the `--conf_target` or `--sat_per_byte` arguments, and the destination address with `--delivery_addr` (unless it was already specified at the channel opening). ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))

In a force close, the funds are locked up for a period of time before they can be redeemed by the closer, while the other party can redeem their funds immediately. Unless an anchor channel was created, the transaction fee of the closing transaction cannot be changed. A force close uses the `--force` flag. ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))

`lncli closeallchannels` closes all channels at once and `lncli closedchannels` shows all closed channels. ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))

Example usage from the guide ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md)):

```
lncli closechannel --funding_txid 83b5a55b21255915dbc0d005230b2c026a004c839edaa716247b96b66490c66a --output_index 1 --sat_per_byte 20 --delivery_addr bc1q6tcemsjadwgt938gkrmcqyvt79wxla42js8r4l
```

Zombie channels are channels that have no activity. The guide suggests trying to disconnect from and reconnect to the peer, or double-checking their IP or onion address, and says it is advisable to close zombie channels, especially if they hold your funds. ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))

Private channels may also bind capital. They are typically created by payment-only nodes or mobile clients and are not used for routing, but they often present a reliable source of fee income. The guide advises considering how long such a channel has been inactive, and its chance of being used again, before force closing it. ([source](../../raw/docs/the-lightning-network/liquidity/manage-liquidity.md))

## Notes

Writer's note, not from the sources: the guide writes the PSBT funding flag as `--pbst`; the spelling is copied as it appears and has not been checked against lnd's own reference here.

See also: [[pathfinding]], [[channel-fees]], [[submarine-swaps]], [[autoloop]], [[using-loop]], [[terminal-liquidity-tools]], [[lnd-routing-node-operations]], [[glossary]].
