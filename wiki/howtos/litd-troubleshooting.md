---
title: Troubleshooting litd and testing on signet
type: howto
sources:
  - raw/docs/lightning-network-tools/lightning-terminal/troubleshooting.md
  - raw/docs/lightning-network-tools/lightning-terminal/testing-on-signet.md
  - raw/docs/lightning-network-tools/lightning-terminal/run-litd.md
updated: 2026-11-14
---

# Troubleshooting litd and testing on signet

Fixes the guide gives for common problems with [[lightning-terminal]] and its bundled products, followed by how to run the stack on Bitcoin signet. For installation and normal start-up see [[running-litd]]; for CLI arguments in integrated mode see [[litd-integration]]. The troubleshooting guide points to the Lightning Labs Slack for anything not covered. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/troubleshooting.md))

## Unable to connect

If you cannot connect to your node, especially after the browser has been idle for a while or was recently restarted, the guide lists these options:

- Attempt to reload the page asking for your password.
- Click on "use a pairing phrase," then reload the page and attempt again.
- Generate a new pairing phrase (see [[running-litd]]), delete the browser cache, reload the page and connect again.
- Delete the `session.db` in `~/.lit/mainnet`, restart `litd` and generate a new pairing phrase.
- Delete the `admin.macaroon` in `~/.lnd/data/chain/bitcoin/mainnet/` and restart LND and litd.

([source](../../raw/docs/lightning-network-tools/lightning-terminal/troubleshooting.md))

How sessions and pairing phrases work is explained in [[lightning-node-connect]].

## Pool account is not synced

If you cannot connect to [[pool]] due to a synchronization error:

1. Shut down `litd` with `kill -s INT $(pidof litd)`
2. Remove or rename your `pool.db`
3. Start `litd`
4. Run the Pool account recovery described below. This cancels any active orders; after recovering the account, the orders can be re-created manually.

([source](../../raw/docs/lightning-network-tools/lightning-terminal/troubleshooting.md))

The `pool.db` file is generally in `~/.pool/mainnet`. In Umbrel: `~/.pool/mainnet/`. In BTCPay Server: `/var/lib/docker/volumes/generated_lnd_lit_1/_data` or `/root/.pool/mainnet`. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/troubleshooting.md))

## Pool account recovery

If Lightning Terminal has been improperly deleted or is otherwise corrupted, funds can be recovered using `pool accounts recover`. Depending on the installation, the command may need additional arguments:

```
pool --tlscertpath ~/.lit/tls.cert --rpcserver=localhost:8443 accounts recover
```

([source](../../raw/docs/lightning-network-tools/lightning-terminal/troubleshooting.md))

**Umbrel:** find the docker process (lightning-terminal) with `docker ps`, open the pool container with `docker exec -it 340a5b0839f1 /bin/bash` (the container ID is the guide's example), then recover the account:

```
pool --rpcserver=localhost:8443 --tlscertpath=/.lit/tls.cert --macaroonpath=/.pool/mainnet/pool.macaroon accounts recover
```

([source](../../raw/docs/lightning-network-tools/lightning-terminal/troubleshooting.md))

**BTCPay:** after `cd btcpayserver-docker`:

```
pool --rpcserver=localhost:8443 --macaroonpath /root/.pool/mainnet/pool.macaroon --tlscertpath /root/.lit/tls.cert accounts recover
```

([source](../../raw/docs/lightning-network-tools/lightning-terminal/troubleshooting.md))

Pool account recovery in general is covered in [[pool-accounts]].

## Pool is unable to resume account

The error looks like this:

```
[ERR] LITD: Could not start subservers: unable to start account manager: unable to resume account X: unable to subscribe for account updates: checking pending batch failed: error removing pending batch artifacts: error abandoning channels from previous pending batch: error locating channel outpoint: no channel output found in batch tx for matched order Y
```

In this case you have to rename your `pool.db` file and recover your account. For Umbrel the guide gives these instructions, reproduced as written:

```
ssh umbrel@umbrel.local
cd ~/umbrel ./scripts/app
stop lightning-terminal
cd /umbrel/app-data/lightning-terminal/data/.pool/mainnet
mv pool.db pool.db.bak
cd /umbrel ./scripts/app
start lightning-terminal
docker exec -it lightning-terminal_web_1 bash
pool --rpcserver=localhost:8443 --tlscertpath=/.lit/tls.cert --macaroonpath=/.pool/mainnet/pool.macaroon accounts recover
```

([source](../../raw/docs/lightning-network-tools/lightning-terminal/troubleshooting.md))

## Testing on signet

Signet is a privately run Bitcoin test network. Unlike testnet, signet cannot be mined, so all coins must be obtained from the maintainers. The guide says signet runs reliably at one block every ~10 minutes with stable fees and predictable rules, and that for Lightning it is often preferred because it allows a durable, public network under realistic network conditions. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/testing-on-signet.md))

### Getting coins

The highest barrier is getting signet coins; faucet reliability and availability is not guaranteed. The guide lists Powcoins, a command line interface that lets you spend proof of work to obtain coins (https://github.com/ajtowns/powcoins), and the browser-based faucets https://signet257.bublina.eu.org/, https://signetfaucet.com/ and https://faucet.coinbin.org/. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/testing-on-signet.md))

### Bitcoin backend

To run Bitcoin Core or Btcd on signet, specify `signet=1` in the configuration file. If you cannot find any peers, the guide suggests:

```
bitcoin-cli addnode 170.75.165.5:8333 add
```

As of signet block 300,000, the blockchain consumes about ~19GB of space and may be pruned, plus 3.7GB for the UTXO set. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/testing-on-signet.md))

### LND

LND runs on signet by appending `network=signet` to your lnd.conf. Append `--network=signet` to your LND and Litd calls. An overview of the signet Lightning Network, with connection information for various nodes, is at https://mempool.space/signet/lightning. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/testing-on-signet.md))

### litd

Lightning Terminal runs on signet as on mainnet, with only `network=signet` as additional configuration. In integrated (LND) mode, `lnd.bitcoin.signet=1` also needs to be present. Autopilot (see [[lit-autopilot]]) has to either be disengaged on signet or pointed at a separate host, by setting in `lit.conf` either

```
autopilot.disable=true
```

or

```
autopilot.address=signet.autopilot.lightning.finance:12010
```

([source](../../raw/docs/lightning-network-tools/lightning-terminal/testing-on-signet.md))

### Loop, Pool and Taproot Assets

- **Loop:** all Loop features can be used on signet. To peer with the Loop signet node, connect to `022b9e44b3a8093d9512b61f5f83a72d5634201efc49718efd34f2ee851b3afa8e@50.112.25.211:9735`. See [[loop]].
- **Pool:** Pool is available on signet. To run `poold` on signet, pass the `network=signet` flag or add it to your configuration file. See [[pool]].
- **Taproot Assets:** to run `tapd` on signet, define network=signet on startup or as part of `tapd.conf`. A universe can be found at `signet.universe.lightning.finance:443`. See [[taproot-assets]].

([source](../../raw/docs/lightning-network-tools/lightning-terminal/testing-on-signet.md))

### Other resources

The guide also links the Bitcoin Wiki signet page (https://en.bitcoin.it/wiki/Signet), Electrum (which can be started on signet with the `--signet` flag), Blink's signet deployment guide (https://dev.blink.sv/self-host/deployment/signet) and an LNbits signet instance (https://signet.laisee.org/). ([source](../../raw/docs/lightning-network-tools/lightning-terminal/testing-on-signet.md))

## Conflicts

- **Autopilot on signet.** The run guide says that to run `litd` on regtest or signet "the autopilot has to be disabled" with `autopilot.disable=true` ([source](../../raw/docs/lightning-network-tools/lightning-terminal/run-litd.md)). The signet guide says autopilot has to be disengaged or pointed at a separate host with `autopilot.address=signet.autopilot.lightning.finance:12010` ([source](../../raw/docs/lightning-network-tools/lightning-terminal/testing-on-signet.md)).
- **Umbrel paths.** Within the troubleshooting guide, the Umbrel `pool.db` location is given as `~/.pool/mainnet/` in one section and as `/umbrel/app-data/lightning-terminal/data/.pool/mainnet` in the Umbrel instructions for the resume error; the Umbrel container is entered with `docker exec -it 340a5b0839f1 /bin/bash` in one section and `docker exec -it lightning-terminal_web_1 bash` in the other ([source](../../raw/docs/lightning-network-tools/lightning-terminal/troubleshooting.md)).
