---
title: Taproot Assets channels in practice
type: howto
sources:
  - raw/docs/lightning-network-tools/taproot-assets/taproot-assets-channels.md
  - raw/docs/lightning-network-tools/taproot-assets/asset-loop.md
  - raw/docs/lightning-network-tools/taproot-assets/polar.md
updated: 2026-11-14
---

# Taproot Assets channels in practice

How to configure `litd` for Taproot Assets channels, open a channel, create and pay asset invoices, close the channel, and Loop Out an asset channel balance.

See also: [[taproot-assets]], [[tapd-taproot-asset-channels]], [[tapd-rfq-guide]], [[edge-node-operation]], [[tapd-operations]], [[tapd-getting-started]], [[taproot-assets-on-lightning]], [[lightning-terminal]], [[loop]], [[using-loop]].

## Requirements

Taproot Assets can be deposited into Lightning Network channels, where they can be transferred instantly at low fees. While `tapd` is used to mint and transfer Taproot Assets on the Bitcoin blockchain, `lnd` is used to open channels and handle Lightning Network payments. To communicate between `tapd` and `lnd`, `litd` is required. For the moment, `litd` needs to be run in integrated mode, meaning `lnd`, `tapd` and `litd` are run as a single binary (see [[litd-integration]]). ([source](../../raw/docs/lightning-network-tools/taproot-assets/taproot-assets-channels.md))

The following configuration options are needed as part of `lit.conf`:

```
lnd.protocol.option-scid-alias=true
lnd.protocol.zero-conf=true
lnd.protocol.simple-taproot-chans=true
lnd.protocol.simple-taproot-overlay-chans=true
lnd.protocol.custom-message=17
lnd.accept-keysend=true
```

([source](../../raw/docs/lightning-network-tools/taproot-assets/taproot-assets-channels.md))

You need a recently minted Taproot Asset held by your tapd (see [[tapd-getting-started]]) and two separate `litd` nodes, which may share the same Bitcoin Core backend (using RPC polling). ([source](../../raw/docs/lightning-network-tools/taproot-assets/taproot-assets-channels.md))

## Which CLI to use

With litd integrated mode, all applications run as part of the litd binary, but the regular CLIs are still used: `lncli` to interact with LND and `tapcli` to interact with onchain Taproot Assets. When opening, closing, or maintaining Taproot Assets channels or making Taproot Assets payments, `litcli` is used. ([source](../../raw/docs/lightning-network-tools/taproot-assets/taproot-assets-channels.md))

The guide's wording on networks is: "Unless you are running `litd` on any other network than mainnet, you will have to specify the network you are running every time you invoke `litcli`", with the example `litcli --network=signet status`. The following commands omit this detail. ([source](../../raw/docs/lightning-network-tools/taproot-assets/taproot-assets-channels.md))

## Open a channel

Identify the asset to deposit. `tapcli assets list` shows the group keys of the Taproot Assets you hold; opening the channel needs the `tweaked_group_key` and how many of these assets to deposit. Specifying a fee rate for the channel opening transaction helps getting the transaction confirmed in time. ([source](../../raw/docs/lightning-network-tools/taproot-assets/taproot-assets-channels.md))

You need a peer that supports Taproot Assets. Ideally you or this peer is willing to act as an edge node, meaning they are willing to swap the asset in question for satoshis on the Lightning Network (see [[edge-node-operation]]).

```
litcli ln fundchannel --node_key 03e347d089c071c27680e26299223e80a740cf3e3fc4b4237fa219bb67121a670b --sat_per_vbyte 16 --asset_amount 1000 --group_key 2875ce409b587a6656357639d099ad9eb08396d0dfea8930a45e742c81d6fc782
```

([source](../../raw/docs/lightning-network-tools/taproot-assets/taproot-assets-channels.md))

The Polar guide opens a channel with the same `litcli ln fundchannel` command but identifies the asset with `--asset_id` instead of `--group_key`. ([source](../../raw/docs/lightning-network-tools/taproot-assets/polar.md))

As the channel is opening, you see the channel `txid`. The channel details are visible immediately with `lncli pendingchannels` and, once confirmed, with `lncli listchannels`. In the guide's sample `listchannels` output the channel has `"capacity": "100000"`, `"private": true` and `"commitment_type": "SIMPLE_TAPROOT_OVERLAY"`, and carries a `custom_channel_data` object with `funding_assets`, `local_assets`, `remote_assets`, `outgoing_htlcs`, `incoming_htlcs`, `capacity`, `group_key`, `local_balance`, `remote_balance`, `outgoing_htlc_balance` and `incoming_htlc_balance`. ([source](../../raw/docs/lightning-network-tools/taproot-assets/taproot-assets-channels.md))

## Generate invoices

To generate invoices, you must have a channel with a remote balance for the asset you are requesting. Your peer also needs to be configured for RFQ (request for quote); see [[tapd-rfq-guide]]. The invoice generation format follows that of LND:

```
litcli ln addinvoice --memo "my first taproot asset transfer" --group_key 02875ce409b587a6656357639d099ad9eb08396d0dfea8930a45e742c81d6fc782 --asset_amount 10000000
```

([source](../../raw/docs/lightning-network-tools/taproot-assets/taproot-assets-channels.md))

## Make payments

Pay by passing the invoice to `litcli` on the sender's node. The guide says the invoice needs to be passed together with the asset ID; its example command passes `--group_key`:

```
litcli ln payinvoice --pay_req <invoice> --group_key 02875ce409b587a6656357639d099ad9eb08396d0dfea8930a45e742c81d6fc782
```

([source](../../raw/docs/lightning-network-tools/taproot-assets/taproot-assets-channels.md))

As the payment succeeds, a small amount of satoshis also gets pushed to the remote side. Satoshis are needed to anchor the taproot asset in an HTLC (see [[htlc]]). In a testing environment it may make sense to balance the bitcoin in the channel using keysend in order to be able to send and receive smoothly:

```
lncli sendpayment --dest 03e347d089c071c27680e26299223e80a740cf3e3fc4b4237fa219bb67121a670b --outgoing_chan_id 3152442773369192448 --amt 50000 --keysend
```

([source](../../raw/docs/lightning-network-tools/taproot-assets/taproot-assets-channels.md))

## Routing through an edge node

In a testing environment, the guide suggests creating multihop routes that involve a Taproot Assets channel: `litd (A) <-> litd (B) <-> any Lightning node implementation (C)`. This simulates a user (A) holding Taproot Assets in a Lightning Network channel with an Edge Node (B). User (A) is able to pay generic Bolt11 Lightning Network invoices presented by node (C), and to request assets by generating invoices that are payable by node (C), regardless of whether node (C) has knowledge of Taproot Assets. ([source](../../raw/docs/lightning-network-tools/taproot-assets/taproot-assets-channels.md))

## Close a channel

Channels are closed using `lncli` as if they were normal channels. It is preferable to close channels cooperatively, but if the peer cannot be reached, it may be necessary to unilaterally close a channel with the `--force` flag:

```
lncli closechannel --chan_point 3596bc22e11333b5c06ea9b4b05ced089acd545df4d1125dca8346b1b5fc64b5:0
```

([source](../../raw/docs/lightning-network-tools/taproot-assets/taproot-assets-channels.md))

## Asset Loop: Loop Out from an asset channel

Starting from Loop v0.30-beta it is possible to perform a Loop Out directly using a Taproot Asset channel balance. Loop performs an offchain payment to the Loop service via your Edge node, and Loop sends BTC onchain to you. The guide presents this as a way to free up inbound liquidity (see [[loop]], [[using-loop]]). ([source](../../raw/docs/lightning-network-tools/taproot-assets/asset-loop.md))

You need Taproot Assets in a channel with a peer performing edge node services, and this peer needs outbound liquidity to the wider Lightning Network. ([source](../../raw/docs/lightning-network-tools/taproot-assets/asset-loop.md))

The `loop out` command needs the amount you expect to receive onchain in satoshis, the asset ID of the asset to be dispensed and the public key of the edge node. At this point it is only possible to Loop Out assets from a single channel:

```
loop out --amt 250000 --asset_id c5dc35d9ffa03abcbd22d2d2801d10813970875029843039bf4f99d543d15fef --asset_edge_node 0312bddcf146394bf0805feef967e8485b8648c66065fe7345c4bc97eac8312df7
```

([source](../../raw/docs/lightning-network-tools/taproot-assets/asset-loop.md))

Loop displays the quote received from your edge node as an estimate of how many Taproot Asset units you are expected to pay. The sample output has the lines `Send off-chain`, `Exchange rate`, `Limit Send off-chain`, `Receive on-chain` and `Estimated total fee`, asks `CONTINUE SWAP? (y/n)`, and after confirmation prints the swap `ID` and `HTLC address` and suggests running `loop monitor` to monitor progress. ([source](../../raw/docs/lightning-network-tools/taproot-assets/asset-loop.md))

The feature is available on mainnet, testnet and signet. The usual Loop Out minimums and maximums apply. At this point the Loop node itself does not accept Taproot Asset channels. ([source](../../raw/docs/lightning-network-tools/taproot-assets/asset-loop.md))

### Easy Autoloop with assets

Autoloop can also be configured with Taproot Assets. The `loop setparams` command can be configured for multiple Asset IDs, and the settings apply to all channels with these assets. The guide states that it is not necessary to run `loopd` as part of `litd` for easy Autoloop to work (see [[autoloop]]).

```
loop setparams --asset_easyautoloop --asset_id c5dc35d9ffa03abcbd22d2d2801d10813970875029843039bf4f99d543d15fef --asset_localbalance 100000000
```

([source](../../raw/docs/lightning-network-tools/taproot-assets/asset-loop.md))

## Conflicts

- **Group key value.** Within the channels guide, the `fundchannel` example passes `--group_key 2875ce40...6fc782` (64 hex characters) while the `addinvoice` and `payinvoice` examples and the sample `listchannels` output show `02875ce40...6fc782` (66 hex characters, with a leading `02`). ([source](../../raw/docs/lightning-network-tools/taproot-assets/taproot-assets-channels.md))
- **Asset ID or group key when paying.** The channels guide's text says the invoice "needs to be passed together with the asset ID", but the command it shows passes `--group_key`. ([source](../../raw/docs/lightning-network-tools/taproot-assets/taproot-assets-channels.md))
- **When to pass `--network`.** The channels guide's sentence reads "Unless you are running `litd` on any other network than mainnet, you will have to specify the network", while its example specifies a non-mainnet network (`litcli --network=signet status`). ([source](../../raw/docs/lightning-network-tools/taproot-assets/taproot-assets-channels.md))
