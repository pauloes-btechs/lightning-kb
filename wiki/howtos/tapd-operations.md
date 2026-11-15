---
title: "Operating tapd safely: multisig, debugging, tips"
type: howto
sources:
  - raw/docs/lightning-network-tools/taproot-assets/operational-safety-guidelines.md
  - raw/docs/lightning-network-tools/taproot-assets/multisignature.md
  - raw/docs/lightning-network-tools/taproot-assets/debugging-tapd.md
  - raw/docs/lightning-network-tools/taproot-assets/tips-and-tricks.md
  - raw/docs/lightning-network-tools/taproot-assets/get-tapd.md
updated: 2026-11-14
---

# Operating tapd safely: multisig, debugging, tips

Backups and loss-of-funds risks, which ports and flags to expose, multisignature options, how to debug `tapd` inside `litd`, and common payment errors.

See also: [[taproot-assets]], [[tapd-getting-started]], [[minting-taproot-assets]], [[tapd-universes-guide]], [[taproot-assets-channels-guide]], [[tapd-rfq-guide]], [[edge-node-operation]], [[lightning-terminal]], [[litd-troubleshooting]].

## Safety status

As of version `v0.3.0-alpha`, Taproot Assets can be used on Bitcoin's `mainnet` network. The guide says that in any version after `v0.3.0` there won't be any breaking changes and any assets minted with that version should be future-proof, but that signaling readiness for `mainnet` does not mean that there won't be any bugs or that all planned safety and backup measures are fully in place yet. Special care must be taken to avoid loss of funds, both assets and BTC. ([source](../../raw/docs/lightning-network-tools/taproot-assets/operational-safety-guidelines.md))

## Avoiding loss of funds

There is no recovery mechanism in place yet that allows you to recover assets from only the `lnd` seed. If you lose your `tapd`'s database, or it gets corrupted, you lose access to all assets minted or received by that `tapd`, and you also cannot spend the BTC used to carry/anchor the assets. ([source](../../raw/docs/lightning-network-tools/taproot-assets/operational-safety-guidelines.md))

To avoid loss of funds, back up your `/home/<user>/.tapd` folder regularly. If you are using a Postgres database as the database backend, it is enough to make backups of that database. You also need `lnd`'s seed phrase, which is what all private keys for all assets in a `tapd` instance are derived from. ([source](../../raw/docs/lightning-network-tools/taproot-assets/operational-safety-guidelines.md))

The reason: the Taproot Assets Protocol is an overlay or off-chain protocol, so data relevant to asset mints, transfers or burns is not stored in the Bitcoin blockchain itself. If access to that data is lost, the assets cannot be recovered by just using a wallet seed. Universes (public asset and proof databases) will help with storing and later retrieving that data, but the mechanisms to query all required data by just using `lnd`'s seed are not yet in place (the guide refers to taproot-assets issue #426). ([source](../../raw/docs/lightning-network-tools/taproot-assets/operational-safety-guidelines.md))

### What to back up

The guide says the following should be backed up regularly, e.g. hourly or even more frequently depending on the number of users/transactions of a system. ([source](../../raw/docs/lightning-network-tools/taproot-assets/operational-safety-guidelines.md))

- If the default SQLite database is used: all data is in the files at `<tapddir>/data/<network>/tapd.db*` (usually `tapd.db`, `tapd.db-wal` and `tapd.db-shm`).
- If a Postgres database is used: it is enough to create a backup of the database configured as `--postgres.dbname` flag or config option.
- Optionally, the copies of the proof files in `<tapddir>/data/<network>/proofs`. Those are also all contained in the SQLite or Postgres database and are only on the filesystem for faster access.

([source](../../raw/docs/lightning-network-tools/taproot-assets/operational-safety-guidelines.md))

The default `tapddir` by operating system, unless the `--tapddir` or `--datadir` flags or config options are set:

| System | Default `tapddir` |
|---|---|
| Linux/Unix | `~/.tapd` |
| MacOS | `~/Library/Application Support/Tapd` |
| Windows | `~/AppData/Roaming/Tapd` |
| Umbrel | `${APP_DATA_DIR}/data/.tapd` |

([source](../../raw/docs/lightning-network-tools/taproot-assets/operational-safety-guidelines.md))

### Where the private keys are

The `tapd` database does not store any private key material. It exclusively uses `lnd`'s wallet to derive keys for assets and their BTC anchoring transactions, and only stores the public key and derivation information. Two kinds of key are derived from `lnd`'s wallet: `internal_key`, the internal keys for BTC-level anchoring transaction outputs that carry asset commitments; and `script_key`, the raw key for asset ownership keys, by default used as BIP-0086 keys in the asset output. ([source](../../raw/docs/lightning-network-tools/taproot-assets/operational-safety-guidelines.md))

### Restoring an outdated backup

Restoring from an outdated database backup is safe: since there is no penalty mechanism involved as in Lightning, there is no additional risk. But if the backup is out of date, it might not contain the latest assets and access to those could still be lost. ([source](../../raw/docs/lightning-network-tools/taproot-assets/operational-safety-guidelines.md))

### Umbrel and node-in-a-box users

If you are using Taproot Assets as part of the "Lightning Terminal" app inside Umbrel (or any comparable node-in-a-box solution), do not uninstall or re-install the "Lightning Terminal" app without first making a manual backup of all local data of `tapd`. Uninstalling any app on Umbrel deletes that app's data, which here contains information needed to spend both the Taproot Assets and the bitcoin that carry the assets. Just having the `lnd` seed phrase is not enough to restore assets minted or received. ([source](../../raw/docs/lightning-network-tools/taproot-assets/operational-safety-guidelines.md))

## Exposing the RPC port

There is normally no need to open the `tapd` RPC port (10029 by default) to the internet, unless the intention is to run a public Universe server, in which case that is the port to expose (see [[tapd-universes-guide]]). By default, all RPC methods (except for some non-sensitive Universe related calls) are protected by macaroon credentials. ([source](../../raw/docs/lightning-network-tools/taproot-assets/operational-safety-guidelines.md))

Three flags/config options should be evaluated:

- `--allow-public-uni-proof-courier`: if set, access to the Universe based proof courier methods is allowed without a macaroon, so any other nodes can use this `tapd` instance to transmit transfer proofs from sender to receiver without needing any permission credential.
- `--allow-public-stats`: if set, access to Universe statistics RPC calls is allowed without a macaroon. This can be useful to pull statistics over the REST interface into any website.
- `--universe.public-access`: if set, proofs can be inserted and synced by other nodes. This flag controls whether remote proofs should be allowed in general, while `--allow-public-uni-proof-courier` controls whether one needs an authentication token to do so.

([source](../../raw/docs/lightning-network-tools/taproot-assets/operational-safety-guidelines.md))

## Multisignature

Taproot Assets and their balances are recorded offchain in Taproot outputs. Analogous to Bitcoin, Taproot Assets are held in outputs which are locked through scripts, called Taproot Asset Outputs, and the Bitcoin-level UTXO commits to this merkle tree, anchoring the assets to a Bitcoin UTXO. ([source](../../raw/docs/lightning-network-tools/taproot-assets/multisignature.md))

To spend a Taproot Asset vUTXO, two conditions need to be met. First, the Taproot Assets-level vUTXO script needs to be satisfied: the signature(s) to the Taproot Asset need to be valid and an eventual timelock needs to be satisfied. Second, the Bitcoin-level UTXO script needs to be satisfied: for a single signer or cooperative signatories this is a valid Schnorr signature, and Taproot transactions additionally allow for multiple alternative spending conditions. ([source](../../raw/docs/lightning-network-tools/taproot-assets/multisignature.md))

The guide describes four places where multiple keys can be applied. ([source](../../raw/docs/lightning-network-tools/taproot-assets/multisignature.md))

- **At the Taproot Asset level.** Each individual Taproot Asset can be secured with multisig, either on the vUTXO level through Schnorr signatures (MuSig2, e.g. N-of-N) or on the script level. As a MuSig2 signature can only be N-of-N, a K-of-N contract can use a tree of MuSig2 to produce the various key combinations. To prevent the internal Taproot key from being used, the key is set to the NUMS key: a deterministic public key for which it can be proven that no private key exists. Multisig at the tapleaf layer level means the owner of the Taproot Asset does not have to control the internal Taproot key, e.g. when using a pocket universe.
- **At the internal Taproot key.** All Taproot Assets are held by a Taproot UTXO, allowing use of Taproot's native MuSig2 feature to require multiple parties to sign off on every transaction. These arrangements are limited to n-of-n MuSig2.
- **At the Bitcoin-level script.** n-of-m multisignature schemes make use of Bitcoin script, similar to how multisignature schemes work in Segwit addresses. This can be used in addition to MuSig2, for example to perform key recovery, or instead of it, for example to introduce additional restrictions such as timelocks.
- **The asset group key.** Grouped assets do not have a fixed supply, and new assets can be issued anytime using the asset group key, so its integrity is crucial for an issuer. The key is a 32 byte Schnorr key, similar to those used for the internal key of a Taproot transaction, which allows for N-of-N MuSig2 using the same tools and mechanisms used to secure the internal Taproot key.

([source](../../raw/docs/lightning-network-tools/taproot-assets/multisignature.md))

Holding the group key on an external signing device is covered on [[minting-taproot-assets]].

## Debugging tapd inside litd

The debugging guide is written for running `litd` with `tapd` in integrated mode. Taproot Assets runs as part of `litd`, and it may not be apparent when `tapd` fails to start as part of the wider bundle. Check which subsystems are enabled and running with:

```
litcli status
```

([source](../../raw/docs/lightning-network-tools/taproot-assets/debugging-tapd.md))

### Logging

In integrated mode, all logs are written to `lnd.log`, typically located in `~/.lnd/logs/bitcoin/mainnet/lnd.log`. To adjust the debug level, run:

```
lncli debuglevel --level trace,SRVR=debug,PEER=info,BTCN=warn,GRPC=error
```

To set the debugging level permanently, add to `lit.conf`:

```
lnd.debuglevel=trace,SRVR=debug,PEER=info,BTCN=warn,GRPC=error
```

To increase the number of log files and their maximum size, so you can look further into the past:

```
lnd.maxlogfilesize=100
lnd.maxlogfiles=100
```

([source](../../raw/docs/lightning-network-tools/taproot-assets/debugging-tapd.md))

### Profiling

A go profile helps determine the state of a go program. Profiling can be enabled at any port, for example `lnd.profile=9736`, and the profile is then fetched with:

```
curl http://localhost:9736/debug/pprof/goroutine?debug=2 > goprofile.txt
```

([source](../../raw/docs/lightning-network-tools/taproot-assets/debugging-tapd.md))

### Filing issues

Issues may be filed on the project's Github repository (`https://github.com/lightninglabs/taproot-assets/issues`). The guide asks reporters to be as clear as possible and to include logs and a go profile. ([source](../../raw/docs/lightning-network-tools/taproot-assets/debugging-tapd.md))

## Payment errors and other tips

### `FAILURE_REASON_INCORRECT_PAYMENT_DETAILS`

When generating an invoice for Taproot Assets, the receiving node expects the payment to come through a channel that holds this specific asset. Such channels are not announced and cannot be found in the graph; instead, they are added as hop hints to the invoice. Not every sender might honor these hop hints, and may try to pay through any existing public channel instead. When paying to the wrong channel, the sender sees the "incorrect payment details" error. They can try again or force the payment to go through the hop hint by passing the `--last_hop` when paying the invoice. ([source](../../raw/docs/lightning-network-tools/taproot-assets/tips-and-tricks.md))

### `FAILURE_REASON_NO_ROUTE`

When a channel along the route is disabled or doesn't have liquidity, the sender might see the "no route" error. Check that your local channels are active and have enough capacity, both Taproot Assets capacity and satoshi capacity, as every HTLC that passes through a Taproot Asset channel still requires some satoshis. ([source](../../raw/docs/lightning-network-tools/taproot-assets/tips-and-tricks.md))

A typical Taproot Asset channel has a capacity of 100,000 satoshis, of which 1,000 are unspendable on each side as the channel reserve. Each open HTLC requires a balance of 345 satoshis, so at least 2035 satoshis are required as inbound capacity to have three pending incoming HTLCs. The 345 satoshis do not change owners once the HTLC settles. ([source](../../raw/docs/lightning-network-tools/taproot-assets/tips-and-tricks.md))

### Satoshi denomination

At the LND level, all transactions remain denominated in satoshis. At this point, the output of many RPC commands such as `lncli listinvoices` or `lncli fwdinghistory` shows only satoshi amounts for Taproot Asset events. ([source](../../raw/docs/lightning-network-tools/taproot-assets/tips-and-tricks.md))

## Conflicts

- **Default directory on Windows.** The Operational Safety Guidelines give the Windows default `tapddir` as `~/AppData/Roaming/Tapd` ([source](../../raw/docs/lightning-network-tools/taproot-assets/operational-safety-guidelines.md)); the Get Started guide places the Windows configuration file at `$LOCALAPPDATA/Tapd/tap.conf` ([source](../../raw/docs/lightning-network-tools/taproot-assets/get-tapd.md)).
- **Configuration file name.** The Get Started guide names the file `tapd.conf` on Linux/BSD and Mac OS but `tap.conf` in its Windows path. ([source](../../raw/docs/lightning-network-tools/taproot-assets/get-tapd.md))
- **Directory name on Mac OS.** `~/Library/Application Support/Tapd` in the Operational Safety Guidelines ([source](../../raw/docs/lightning-network-tools/taproot-assets/operational-safety-guidelines.md)) versus `~/Library/Application Support/tapd/tapd.conf` in the Get Started guide ([source](../../raw/docs/lightning-network-tools/taproot-assets/get-tapd.md)); they differ in capitalisation.
- **Alpha versus mainnet-ready.** The Get Started and Debugging guides call Taproot Assets "alpha software" ([source](../../raw/docs/lightning-network-tools/taproot-assets/get-tapd.md), [source](../../raw/docs/lightning-network-tools/taproot-assets/debugging-tapd.md)); the Operational Safety Guidelines say that as of `v0.3.0-alpha` it can be used on `mainnet` with no breaking changes after `v0.3.0` ([source](../../raw/docs/lightning-network-tools/taproot-assets/operational-safety-guidelines.md)). These statements can both hold; they are recorded here because they set different expectations.
