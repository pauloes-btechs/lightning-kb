---
title: Getting started with tapd
type: howto
sources:
  - raw/docs/lightning-network-tools/taproot-assets/get-tapd.md
  - raw/docs/lightning-network-tools/taproot-assets/first-steps.md
  - raw/docs/lightning-network-tools/taproot-assets/polar.md
  - raw/docs/lightning-network-tools/taproot-assets/universes.md
updated: 2026-11-14
---

# Getting started with tapd

How to install and run `tapd`, mint, send, receive and burn a first asset with `tapcli`, and prototype with Lightning Polar. Component page: [[taproot-assets]].

See also: [[minting-taproot-assets]], [[tapd-universes-guide]], [[taproot-assets-channels-guide]], [[tapd-rfq-guide]], [[edge-node-operation]], [[tapd-operations]], [[tapd-taproot-assets]], [[tapd-mint]], [[tapd-universe]], [[taproot-assets-protocol]].

## Install

The Taproot Assets Daemon `tapd` implements the Taproot Assets Protocol for issuing and transferring assets on the Bitcoin blockchain. The guide labels Taproot Assets as alpha software, to be used on mainnet at your own risk. ([source](../../raw/docs/lightning-network-tools/taproot-assets/get-tapd.md))

### Full feature set: litd in integrated mode

To make use of all Taproot Assets features, you must run `litd` in integrated mode, meaning all binaries, including LND and tapd, are running as part of one binary. Tapd is included in the Litd bundle, which lets you run LND and Tapd in the same process and removes the need to configure the two separately (see [[lightning-terminal]], [[running-litd]], [[litd-integration]]). ([source](../../raw/docs/lightning-network-tools/taproot-assets/get-tapd.md))

### Standalone

If you do not need to make use of Lightning channels, you may install `tapd` as a standalone binary with a connection to LND. If LND is compiled from source, it needs to be built using `tags=signrpc walletrpc chainrpc invoicesrpc` (see [[lnd]], [[running-lnd]]). ([source](../../raw/docs/lightning-network-tools/taproot-assets/get-tapd.md))

LND needs to be synced and running on the same bitcoin network as tapd. RPC connections need to be accepted and Macaroons need to be set. For onchain operations, this LND node should have some funds in its onchain wallet, but does not need open channels to mint, send and receive Taproot Assets on chain. ([source](../../raw/docs/lightning-network-tools/taproot-assets/get-tapd.md))

To compile from source, clone the taproot-assets repository. Go version 1.21 or higher is recommended (check with `go version`):

```
git clone https://github.com/lightninglabs/taproot-assets.git
cd taproot-assets
checkout <latest version>
make install
```

([source](../../raw/docs/lightning-network-tools/taproot-assets/get-tapd.md))

## Configuration

Optionally, create a Taproot Assets configuration file under `~/.tapd/tapd.conf` on Linux or BSD, `~/Library/Application Support/tapd/tapd.conf` in Mac OS or `$LOCALAPPDATA/Tapd/tap.conf` in Windows. Within the `tapd.conf` file you can permanently set your variables, such as directory, macaroon or other paths and how to connect to your LND. ([source](../../raw/docs/lightning-network-tools/taproot-assets/get-tapd.md))

As there is currently no migration path between the SQLite and Postgres backends, the backend needs to be configured when `tapd` is first initialized. ([source](../../raw/docs/lightning-network-tools/taproot-assets/get-tapd.md))

### Signet and regtest

According to the Get Started guide, Lightning Labs currently does not provide a Taproot Asset Universe on Signet. In addition to disabling the autopilot, users will have to configure a local or alternative universe (see [[tapd-universes-guide]]). To properly close channels, both peers will have to configure the same proof courier as well. In the `lit.conf`:

```
taproot-assets.proofcourieraddr=universerpc://universe.signet.laisee.org:8443
```

Using the command line:

```
tapcli universe federation add --universe_host universe.signet.laisee.org:8443
```

([source](../../raw/docs/lightning-network-tools/taproot-assets/get-tapd.md))

## Running tapd

Run Taproot Assets with the command `tapd`. Specify how Taproot Assets can reach LND and what bitcoin network to run with by passing additional flags:

```
tapd --network=signet --debuglevel=debug --lnd.host=localhost:10009 --lnd.macaroonpath=/home/ubuntu/.lnd/data/chain/bitcoin/signet/admin.macaroon --lnd.tlspath=/home/ubuntu/.lnd/tls.cert --tapddir=~/.tapd --rpclisten=127.0.0.1:10029 --restlisten=127.0.0.1:8089
```

([source](../../raw/docs/lightning-network-tools/taproot-assets/get-tapd.md))

You may run multiple tapd instances on the same machine, but you will also have to set up multiple LND instances. When doing so, set an alternate Taproot Assets directory and API endpoints, and specify these when calling `tapcli` as well. For example, a second instance is run with `tapd --tapddir=~/.tapd-2 --rpclisten=127.0.0.1:10030 --restlisten=127.0.0.1:8090` and addressed with `tapcli --rpcserver=127.0.0.1:10030 --tapddir=~/.tapd-2`. You can make use of `tapcli profiles` to make calls to separate `tapd` instances on the same machine. ([source](../../raw/docs/lightning-network-tools/taproot-assets/get-tapd.md))

## Using tapcli against litd

When running `tapd` as part of `litd` (integrated mode), you need to specify that you are connecting to the `litd` process when executing `tapcli` commands. This has to include the `tls.cert` and port `8443`. Unless you are running on mainnet, the network has to be specified as well:

```
tapcli --tlscertpath ~/.lit/tls.cert --rpcserver=localhost:8443 --network=signet assets list
```

The guide's later sample commands omit these details for simplicity, and so do the ones below. ([source](../../raw/docs/lightning-network-tools/taproot-assets/first-steps.md))

## Mint a first asset

Taproot Assets allows you to mint both collectible and normal assets; a normal asset is divisible into equal parts. The parameters to decide before minting are covered on [[minting-taproot-assets]]. ([source](../../raw/docs/lightning-network-tools/taproot-assets/first-steps.md))

The guide mints a normal asset whose supply can be increased in the future by setting the `--new_grouped_asset` flag. It describes the total supply as 1,000 units, each divisible into 1,000 sub-units. For the decimal display to take effect, the `meta_type` needs to be set to `json` and a json needs to be supplied, either as a file or as a string. As of now there is no "official" format for what this json should look like or contain.

```
tapcli assets mint --type normal --name beefbux --supply 1000000 --decimal_display 3 --meta_bytes '{"hello":true}' --meta_type json --new_grouped_asset
```

([source](../../raw/docs/lightning-network-tools/taproot-assets/first-steps.md))

This adds the asset to a minting queue called a batch, which allows multiple assets to be created in a single minting transaction, saving fees and conserving blockspace. To execute the batch and publish the mint transaction to the blockchain run:

```
tapcli assets mint finalize
```

You are given a `batch_txid`, which has to be included in a block before you can spend the newly created assets. You can inspect the newly created asset(s) with `tapcli assets list --show_unconfirmed_mints`. ([source](../../raw/docs/lightning-network-tools/taproot-assets/first-steps.md))

### Reading the asset listing

The guide explains the fields of the `tapcli assets list` output as follows. ([source](../../raw/docs/lightning-network-tools/taproot-assets/first-steps.md))

| Field | Meaning given in the guide |
|---|---|
| `version` | The asset protocol version with which this asset was created |
| `genesis_point` | The first input of the minting transaction |
| `name` | The name of the asset as defined at its creation |
| `meta_hash` | The metadata as defined at its creation |
| `asset_id` | A digest of the information found under asset_genesis in the format `sha256(genesis_outpoint \|\| asset_tag \|\| asset_meta \|\| output_index \|\| asset_type)` |
| `asset_type` | Whether an asset is "normal" or a collectible |
| `output_index` | The output of the minting transaction where the asset will be anchored; set to 0 while the transaction confirms |
| `amount` | The quantity of this asset held by you |
| `lock_time`, `relative_lock_time` | An asset can be locked in time, similar to a bitcoin script; relative locktime is analogous to bitcoin script |
| `script_key` | The script key associated with the asset |
| `script_key_is_local` | Whether you hold the key associated with this script |
| `raw_group_key` | If the asset belongs to an asset group, its key will be listed here |
| `tweaked_group_key` | The tweaked key is needed to later issue more assets of this group |
| `asset_witness` | The witness (e.g. signature) used to prove that this asset was issued by the owner of the group key |
| `anchor_tx` | The raw minting transaction |
| `anchor_block_hash` | The hash of the block that the minting transaction was included in; zeros while unconfirmed |
| `anchor_outpoint` | The outpoint on the bitcoin blockchain that holds the asset |
| `internal_key` | The Taproot key that holds the outpoint containing the asset |
| `merkle_root` | The merkle root of the tree that includes the asset |
| `tapscript_sibling` | The taproot leaf to the left or right of the leaf committing to the asset, used to calculate the merkle root |
| `prev_witnesses` | Signatures and data related to previous transfers of this asset |
| `is_spent` | Whether this asset has been spent |
| `lease_owner` | Similar to leased UTXOs in LND, tapd allows specific UTXOs to be "held" for a certain amount of time, which prevents the UTXO from being accidentally spent by another process |
| `lease_expiry` | When the UTXO becomes available again for spending |
| `is_burn` | Whether the asset has been burned |
| `script_key_declared_known`, `script_key_has_script_path` | Used for Lightning Network channels |
| `decimal_display` | The number of decimal places configured for this asset |

([source](../../raw/docs/lightning-network-tools/taproot-assets/first-steps.md))

### Minting more of a grouped asset

Assets minted with the flag `--new_grouped_asset` do not have a fixed supply. A new batch can be minted later so that the two assets are considered of the same asset group, and therefore fungible. Increasing the supply requires the asset's tweaked_group_key:

```
tapcli assets mint --type normal --name beefbux --supply 100000 --decimal_display 3 --grouped_asset --group_key 025234364112f83ea7ee8e35f061d625df82ee07e443835107947e3bb53e8e9bfc
tapcli assets mint finalize
```

You can specify a custom fee rate (in sat/vB) using the flag `--sat_per_vbyte`. ([source](../../raw/docs/lightning-network-tools/taproot-assets/first-steps.md))

`tapcli assets groups` lists groups, ordered by their tweaked group key. `tapcli assets balance` shows balances, and `tapcli assets balance --by_group` shows the cumulative balance across asset groups. ([source](../../raw/docs/lightning-network-tools/taproot-assets/first-steps.md))

## Synchronize with a universe

Taproot Assets uses universes to communicate information about which assets exist and where in the blockchain they are anchored. A universe can be thought of as a virtual mempool, an explorer, or a repository. Your node syncs with the universe whenever you create a new Taproot Assets address with an unknown asset ID, or when specifically instructed to; this requires an asset ID or a group key. ([source](../../raw/docs/lightning-network-tools/taproot-assets/first-steps.md))

```
tapcli universe sync --universe_host universe.lightning.finance:10029 --group_key 025234364112f83ea7ee8e35f061d625df82ee07e443835107947e3bb53e8e9bfc
```

Upon successful sync, information about existing assets should be retrieved, alongside their issuance proofs. More on universes: [[tapd-universes-guide]]. ([source](../../raw/docs/lightning-network-tools/taproot-assets/first-steps.md))

## Generate a Taproot Assets address

As soon as minted assets have one confirmation on the blockchain, you are able to transfer them. You first need the recipient's Taproot Assets address, which can be interactive or non-interactive. ([source](../../raw/docs/lightning-network-tools/taproot-assets/first-steps.md))

Interactive addresses are preferable where the asset ID is not known (for instance grouped assets), when the requested amount is flexible, or when the address is meant to be reusable. The sender and recipient both have to be online to negotiate the transaction, although the final transaction may be submitted to the blockchain only at a later point. Only the group key is required:

```
tapcli addrs new --group_key 02875ce409b587a6656357639d099ad9eb08396d0dfea8930a45e742c81d6fc782
```

([source](../../raw/docs/lightning-network-tools/taproot-assets/first-steps.md))

Non-interactive addresses are specific to an asset and amount, so the recipient needs to know an asset's `asset_id` and be synced to the issuer's universe. Reuse of non-interactive addresses should be avoided. This type of transfer is ideal when the asset ID is known and the amount is fixed; the recipient does not need to be online during the transfer:

```
tapcli addrs new --asset_id b9ae86f52dcbdee7ea78e86b26320819c44c2f4f8a91b9c055ca0af4c4d1b22b --amt 21
```

([source](../../raw/docs/lightning-network-tools/taproot-assets/first-steps.md))

The address fields are explained in the guide as: `encoded` (the bech32 encoded Taproot Assets address), `asset_id`, `asset_type` (fungible or collectible), `amount` (the requested amount), `group_key` (if set, the asset is part of an asset group, meaning the issuer can expand its supply), `script_key` (identifies the script that defines how an asset may be transferred), `internal_key` (the key that holds the asset), `taproot_output_key` (the key that is going to hold the Taproot output once it is received), `proof_courier_addr` (the mailbox over which the asset proofs are being delivered) and `asset_version`. An address can be inspected again anytime with `tapcli addrs query`. ([source](../../raw/docs/lightning-network-tools/taproot-assets/first-steps.md))

## Send an asset

In the interactive flow, the sender uses `tapcli assets send` with the generated address and the amount, separated by a colon, in the `--addr_with_amount` flag (form: `tapcli assets send --addr_with_amount <address>:100`). For this type of send, address reuse is acceptable or even encouraged, but both the sender and the receiver are expected to be online simultaneously. ([source](../../raw/docs/lightning-network-tools/taproot-assets/first-steps.md))

To send to a non-interactive address, run `tapcli assets send --addr <address> --sat_per_vbyte 16` (the guide's example fee rate) from the sender's `tapd` instance. This generates the appropriate Merkle trees for the recipient and their change outputs, signs the Taproot Assets transaction with their internal Taproot Assets key and publishes the Bitcoin transaction. You cannot send unconfirmed assets. ([source](../../raw/docs/lightning-network-tools/taproot-assets/first-steps.md))

Once the transaction is confirmed on the Bitcoin blockchain the sender attempts to make the proofs available to the recipient via an end-to-end encrypted mailbox, similar to Lightning Node Connect (LNC) (see [[lightning-node-connect]]). By default, this mailbox is set to your default universe, but you can run your own mailbox through aperture (see [[aperture-mailbox-and-lnc]]) and configure `tapd` to use it by specifying the `--hashmailcourier.addr=` flag at startup. ([source](../../raw/docs/lightning-network-tools/taproot-assets/first-steps.md))

## Burn assets

Burning assets works by sending assets to a provably unspendable address. The command asks for confirmation of the destructive action, showing the asset ID, the current available balance and the amount to burn, and expects 'yes' or 'no':

```
tapcli assets burn --asset_id b9ae86f52dcbdee7ea78e86b26320819c44c2f4f8a91b9c055ca0af4c4d1b22b --amount 50
```

([source](../../raw/docs/lightning-network-tools/taproot-assets/first-steps.md))

## Prototype with Lightning Polar

Lightning Polar is an application that lets you quickly spin up a local testing environment for your Lightning Network node and applications, including Taproot Assets. It supports Litd, LND, CLN and Eclair, with a Bitcoin Core backend on regtest. ([source](../../raw/docs/lightning-network-tools/taproot-assets/polar.md))

Polar requires Docker: Docker Desktop on Windows and Mac OS, while on Linux Docker Engine is recommended. Polar can be downloaded from the official website (`https://lightningpolar.com/`), from Github, or built from source. ([source](../../raw/docs/lightning-network-tools/taproot-assets/polar.md))

The guide's sample network has two Litd nodes, each with their own Bitcoin Core backend. One Litd node (Alice) acts as the user, the other (Edgar) acts as the edge node. The edge node is connected to a CLN, Eclair and LND node, representing the broader Lightning Network. ([source](../../raw/docs/lightning-network-tools/taproot-assets/polar.md))

Clicking "Start" on the top right corner loads the Bitcoin and Lightning nodes. Once they are running, click on a Lightning node and deposit funds into it; this triggers the regtest Bitcoin node to mine regtest-Bitcoin in the background and transfer them to the internal wallet of the node. ([source](../../raw/docs/lightning-network-tools/taproot-assets/polar.md))

The Litd nodes include all the functionality necessary to mint Taproot Assets and open Taproot Assets channels. In a terminal for the Edge node, the guide mints an asset and finalizes the batch, then mines a few blocks to get the transaction confirmed:

```
tapcli assets mint --type normal --name lollar --supply 1000000000 --decimal_display 3 --meta_bytes '{"hello":true}' --meta_type json --new_grouped_asset
tapcli assets mint batches finalize
```

([source](../../raw/docs/lightning-network-tools/taproot-assets/polar.md))

Before the asset can be used to open a channel it has to be synced to Alice's node. The guide calls the Polar UI the easiest way: "creating an Asset address", then "sync assets from Edgar's node", then clicking "generate" to make sure the synchronization process is completed. ([source](../../raw/docs/lightning-network-tools/taproot-assets/polar.md))

A Taproot Asset channel is then opened with the command below, substituting Alice's node key and the asset ID of the minted asset. Ordinary Lightning Network channels can be created using the Polar UI. Channel usage is covered on [[taproot-assets-channels-guide]].

```
litcli --macaroonpath ~/.lnd/data/chain/bitcoin/regtest/admin.macaroon ln fundchannel --node_key 03d30bdaa3f44dd0a5ae7ed7cb1ad1c0ddd13b8db979b719cd963b65508815c4f1 --asset_amount 1000000 --asset_id b7e048c449feebb898138f1a7f340cc210ab2a04304b5595f20715a8a6e0ba34 --sat_per_vbyte 10
```

([source](../../raw/docs/lightning-network-tools/taproot-assets/polar.md))

Polar can also simulate environments in which assets are sent through two separate edge nodes: in the guide's example Alice and Alfred send their assets to Zara and Zane, using Edgar and Eda as the edge nodes, while Elen and Cora represent the wider Lightning Network. Polar exposes the connection information for all Bitcoin, LND and Taproot Assets clients; you can launch a terminal to interact with them directly, or right-click on any node to see its logs. ([source](../../raw/docs/lightning-network-tools/taproot-assets/polar.md))

## Conflicts

- **Finalize command.** The First Steps guide finalizes a batch with `tapcli assets mint finalize` ([source](../../raw/docs/lightning-network-tools/taproot-assets/first-steps.md)); the Polar guide uses `tapcli assets mint batches finalize` ([source](../../raw/docs/lightning-network-tools/taproot-assets/polar.md)).
- **Signet universe.** The Get Started guide says Lightning Labs currently does not provide a Taproot Asset Universe on Signet and configures `universe.signet.laisee.org:8443` ([source](../../raw/docs/lightning-network-tools/taproot-assets/get-tapd.md)). The First Steps guide says "On signet, you can use `signet.universe.lightning.finance:10029.`" ([source](../../raw/docs/lightning-network-tools/taproot-assets/first-steps.md)), and the Universes guide names `signet.universe.lightning.finance:10029` as the default universe for signet ([source](../../raw/docs/lightning-network-tools/taproot-assets/universes.md)).
- **First Steps mint example.** The text describes 1,000 units each divisible into 1,000 sub-units and the command passes `--supply 1000000 --decimal_display 3`, but the sample `tapcli assets list` output printed beneath it shows `"amount": "1000000000000"` and `"decimal_display": 6`. ([source](../../raw/docs/lightning-network-tools/taproot-assets/first-steps.md))
