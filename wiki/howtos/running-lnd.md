---
title: Installing, running and first steps with lnd
type: howto
sources:
  - raw/docs/lightning-network-tools/lnd/run-lnd.md
  - raw/docs/lightning-network-tools/lnd/first-steps-with-lnd.md
  - raw/docs/lightning-network-tools/lnd/enable-neutrino-mode-in-bitcoin-core.md
updated: 2026-11-14
---

# Installing, running and first steps with lnd

How to install [[lnd]], connect it to a Bitcoin backend, start it, upgrade it, and then fund a wallet, open a channel, pay and receive. The full configuration file is covered on [[lnd-configuration]].

## Prerequisites

LND runs on Windows or Mac OS X, but Unix operating systems are recommended (the guide's examples use Debian/Ubuntu). A 64-bit architecture is required because files grow larger than 2GB. The minimum machine is 2GB RAM, a 1 GHz quad core and at least 5GB of storage; because LND reads and writes frequently, the guide says not to use an SD card but a good quality SSD. ([source](../../raw/docs/lightning-network-tools/lnd/run-lnd.md))

A Bitcoin backend is not required, since LND can run in Neutrino mode, but for performance the guide recommends Bitcoin Core or btcd on the same machine or network. The Bitcoin node may be pruned, though aggressive pruning may impact performance. LND's taproot functionality needs at least bitcoind v0.21 or btcd v0.23.1. ([source](../../raw/docs/lightning-network-tools/lnd/run-lnd.md))

## Install

**Binaries (recommended for production).** Download a release from `https://github.com/lightningnetwork/lnd/releases`. Each release is signed by multiple developers whose keys are in the LND repository under `scripts/keys`. Import the keys, verify the signature, then check the tarball hash against the manifest (the output should print "OK" for each matching sum): ([source](../../raw/docs/lightning-network-tools/lnd/run-lnd.md))

```
gpg --import key.asc
gpg --verify manifest-v[latest]-beta.txt.sig manifest-v[latest]-beta.txt
echo "$(cat manifest-v[latest version].txt)" | sha256sum -c --ignore-missing
tar -xvf lnd.tar.gz
mv lnd /usr/local/bin
```

([source](../../raw/docs/lightning-network-tools/lnd/run-lnd.md))

The guide links a sample `lnd.service` file for running LND with systemd. ([source](../../raw/docs/lightning-network-tools/lnd/run-lnd.md))

**From source (recommended for development or testnet).** This needs Go version 1.18 or higher, with `/usr/local/go/bin` and `$GOPATH/bin` on the `PATH`. Starting with lnd 0.15 all important subsystems are built by default: autopilotrpc, signrpc, walletrpc, chainrpc, invoicesrpc, neutrinorpc, routerrpc, watchtowerrpc, monitoring, peersrpc, kvdb_postrgres and kvdb_etcd. ([source](../../raw/docs/lightning-network-tools/lnd/run-lnd.md))

```
git clone https://github.com/lightningnetwork/lnd
cd lnd
git checkout <most recent version>
make install
```

([source](../../raw/docs/lightning-network-tools/lnd/run-lnd.md))

**Docker.** Building needs docker, make and bash. The guide builds with `docker build --build-arg checkout=<latest-release> -t lnd:<latest-release> .` and runs with `docker run -d --name lnd -v ~/.lnd:/root/.lnd -p 9735:9735 -p 10009:10009 lnd:v0.20.0-beta`. Images are also on Docker Hub: `docker pull lightninglabs/lnd:<latest release>` then `docker run lightninglabs/lnd [command-line options]`. ([source](../../raw/docs/lightning-network-tools/lnd/run-lnd.md))

**Third-party platforms.** LND can also be installed inside BTCPay Server, RaspiBlitz, myNode or Umbrel. ([source](../../raw/docs/lightning-network-tools/lnd/run-lnd.md))

## Configure the Bitcoin backend

**bitcoind.** Bitcoin Core needs RPC enabled in `bitcoin.conf`, either with `rpcauth=[user]:[password hash]` or with `rpcuser=` and `rpcpassword=`. To get the latest block data, enable ZMQ with `zmqpubrawblock=tcp://127.0.0.1:28332` and `zmqpubrawtx=tcp://127.0.0.1:28333`. The experimental "rpcpolling" option can make ZMQ obsolete, allowing multiple LND nodes per bitcoind backend or multiple backends behind a load balancer. On a full, unpruned node, `txindex=1` gives small performance improvements. ([source](../../raw/docs/lightning-network-tools/lnd/run-lnd.md))

**btcd.** btcd needs RPC enabled with `rpcuser=` and `rpcpass=`. ([source](../../raw/docs/lightning-network-tools/lnd/run-lnd.md))

**Serving Neutrino clients from Bitcoin Core.** Since Bitcoin Core 0.21.0 (BIP157), a Bitcoin node can serve block data to remote LND nodes. Add `blockfilterindex=1` and `peerblockfilters=1` to `bitcoin.conf`; after a restart the node resyncs and builds the `blockfilterindex`, which may take a while. Bitcoin Core will then advertise itself to the network if you have set this in your configuration; to disable discovery, set `discover=0` in `bitcoin.conf`. ([source](../../raw/docs/lightning-network-tools/lnd/enable-neutrino-mode-in-bitcoin-core.md))

## Configure LND

`lnd.conf` is found in `~/.lnd` on Linux, `~/Library/Application Support/Lnd` on Mac OS X and `$LOCALAPPDATA/Lnd` on Windows. It must say which backend to use and how to connect to it. The guide's settings: ([source](../../raw/docs/lightning-network-tools/lnd/run-lnd.md))

| Backend | Settings |
|---|---|
| General | `bitcoin.mainnet=true` |
| Neutrino | `bitcoin.node=neutrino`, `feeurl=https://nodes.lightning.computer/fees/v1/btc-fee-estimates.json` |
| bitcoind | `bitcoin.node=bitcoind`, `bitcoind.rpcuser=`, `bitcoind.rpcpass=`, `bitcoind.zmqpubrawblock=tcp://127.0.0.1:28332`, `bitcoind.zmqpubrawtx=tcp://127.0.0.1:28333`; or `bitcoind.rpcpolling` if ZMQ is omitted |
| btcd | `bitcoin.node=btcd`, `btcd.rpcuser=`, `btcd.rpcpass=`, `btcd.rpccert=` |

([source](../../raw/docs/lightning-network-tools/lnd/run-lnd.md))

To point a Neutrino-mode LND at your own Bitcoin Core node, set `bitcoin.node=neutrino` and `neutrino.addpeer=<your Bitcoin node's IP address>:<p2p port>` (repeatable for uptime), or `neutrino.connect=<your Bitcoin node's IP address>:<p2p port>` to connect exclusively to a single node. ([source](../../raw/docs/lightning-network-tools/lnd/enable-neutrino-mode-in-bitcoin-core.md))

Recommended: `rpcmiddleware.enable=true`, which enables the RPC middleware interceptor needed for Autofees and LND Accounts. Popular: `db.bolt.auto-compact=true` and `alias=<choose a name for your node>`. ([source](../../raw/docs/lightning-network-tools/lnd/run-lnd.md))

## Run and upgrade

Start the daemon with `lnd` and interact with it through `lncli`, which passes commands to lnd and returns information. ([source](../../raw/docs/lightning-network-tools/lnd/run-lnd.md))

The guide recommends upgrading to the latest release whenever available, and if a release was missed, upgrading directly to the latest. In every method, shut down gracefully first with `lncli stop` (this may take a minute), and afterwards start LND, unlock the wallet and check `lncli version`. ([source](../../raw/docs/lightning-network-tools/lnd/run-lnd.md))

- Binaries: download, verify and unpack as for installation, then overwrite the previous binary.
- Source: `git pull`, `git checkout <latest release>`, `make clean && make && make install`.
- Docker: in the local lnd repository, `git pull`, `git checkout <latest release>`, `make docker-release tag=<latest release>`.

([source](../../raw/docs/lightning-network-tools/lnd/run-lnd.md))

## First steps

**Check sync.** `lncli getinfo` shows whether the node is running and synced to chain and graph; if the command fails entirely, LND may not be running. ([source](../../raw/docs/lightning-network-tools/lnd/first-steps-with-lnd.md))

**Deposit bitcoin.** Generate a taproot address with `lncli newaddress p2tr`, or use `np2wkh` (legacy segwit) or `p2wkh` (native segwit) if the sender does not support taproot. `lncli walletbalance` shows the unconfirmed balance. ([source](../../raw/docs/lightning-network-tools/lnd/first-steps-with-lnd.md))

**Open a channel.** You need the peer's public key and IP or onion address, and a capacity. You may not be able to use the full wallet balance because of on-chain fees and anchor reserves: for each channel the node keeps 10,000 satoshis on-chain, up to a total of 100,000 satoshis. Some peers impose minimum channel sizes, which you are told about when you try to open. The channel must confirm within two weeks or the peer might forget it; an unconfirmed balance can only be used by setting `min_confs` to zero. ([source](../../raw/docs/lightning-network-tools/lnd/first-steps-with-lnd.md))

```
lncli openchannel --node_key <pubkey> --connect <host>.onion:9735 --local_amt 1000000 --sat_per_vbyte 1 --min_confs 0
```

Typically a channel takes three confirmations to be open and usable. Channels can also be funded externally with PSBTs (see [[lnd-wallet-and-psbt]]). ([source](../../raw/docs/lightning-network-tools/lnd/first-steps-with-lnd.md))

**Pay.** `lncli payinvoice <invoice>` pays an invoice and shows the route and fee. More options are on [[lnd-sending-payments]]. ([source](../../raw/docs/lightning-network-tools/lnd/first-steps-with-lnd.md))

**Get inbound capacity.** Options listed: make many outgoing payments, Loop Out, or ask a friend to open a channel or buy one with Lightning Pool. `lncli listchannels` shows local and remote balances. ([source](../../raw/docs/lightning-network-tools/lnd/first-steps-with-lnd.md))

**Receive.** `lncli addinvoice` creates an invoice. Popular options: `--memo`, `--amt` (satoshis), `--expiry` (seconds; default 3600, 1h) and `--amp` (an AMP invoice that can be paid multiple times). See [[lnd-receiving-payments]]. ([source](../../raw/docs/lightning-network-tools/lnd/first-steps-with-lnd.md))

See also: [[lnd]], [[lnd-configuration]], [[lnd-tor-and-networking]], [[lnd-routing-node-operations]], [[payment-channels]], [[inbound-capacity]], [[loop]], [[pool]], [[lightning-terminal]].
