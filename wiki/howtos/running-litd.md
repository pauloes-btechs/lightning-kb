---
title: Installing and running litd
type: howto
sources:
  - raw/docs/lightning-network-tools/lightning-terminal/get-lit.md
  - raw/docs/lightning-network-tools/lightning-terminal/run-litd.md
  - raw/docs/lightning-network-tools/lightning-terminal/speedrun.md
  - raw/docs/lightning-network-tools/lightning-terminal/connect.md
  - raw/docs/lightning-network-tools/lightning-terminal/testing-on-signet.md
updated: 2026-11-14
---

# Installing and running litd

This page covers installing `litd`, the daemon behind [[lightning-terminal]], configuring it in integrated or remote mode, a fresh-server walk-through, and connecting it to Lightning Terminal on the web. Litd gives a node access to features such as LND Accounts or LNC while bundling LND with Loop, Pool, Faraday, and Taproot Assets. You can point litd at an existing LND, Loop or Pool installation, or run LND as part of litd; the guide calls running the entire bundle as a single binary the most reliable and convenient option, with individual components still swappable, for example to apply patches or run pre-release software. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/get-lit.md))

Related pages: [[litd-integration]] (moving an existing node into integrated mode, and the CLIs), [[lightning-node-connect]] (how sessions and pairing phrases work), [[litd-accounts-guide]], [[terminal-liquidity-tools]], [[terminal-privacy-and-security]] and [[litd-troubleshooting]].

## Install litd

Litd can be installed from source or from the provided binary. If you run LND as part of a software bundle like Umbrel, litd might already be installed on your node. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/get-lit.md))

### Install the binary

Binaries and verification instructions for the latest release are on the GitHub releases page of `lightninglabs/lightning-terminal`. After downloading the binary for your operating system, verify and unpack it. The guide gives these examples:

```
tar -xvf lightning-terminal--alpha.tar.gz
```

Or on Windows:

```
tar -xvzf C:\path\lightning-temrinal-alpha.tar.gz -C C:\path\litd
```

You can then execute the program from its location, or place it where the system can find it, such as `/bin/litd` on Linux. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/get-lit.md))

### Install from source

Prerequisites:

1. Go version 1.19 or higher.
2. nodejs, which can be installed with `snap install node`.
3. yarn, which can be installed with `npm install --global yarn`.

([source](../../raw/docs/lightning-network-tools/lightning-terminal/get-lit.md))

Download the source and install:

```
git clone https://github.com/lightninglabs/lightning-terminal.git
cd lightning-terminal
git checkout <latest version>
make install
```

If you do not already have LND, Loop or Pool installed, you may run LND in integrated mode (one binary bundle), in which case you also have to install the CLI interfaces:

```
make go-install-cli
```

([source](../../raw/docs/lightning-network-tools/lightning-terminal/get-lit.md))

### Install in BTCPay Server

BTCPay contains an installation script for litd:

1. Set a password for the litd instance: `export LIT_PASSWD="YOUR PASSWORD HERE"`
2. Add the fragment to your configuration and run the installation script: `BTCPAYGEN_ADDITIONAL_FRAGMENTS="$BTCPAYGEN_ADDITIONAL_FRAGMENTS;opt-add-lightning-terminal"` then `. btcpay-setup.sh -i`
3. litd is then found under Server Settings > Services.
4. To use the command line, first enter the docker container of your BTCPay instance: `docker exec -it generated_lnd_lit_1 bash`
5. Then specify the TLS path and RPC port for your commands, e.g.:

```
loop --tlscertpath /root/.lit/tls.cert --rpcserver localhost:8443 getinfo
litcli --tlscertpath /root/.lit/tls.cert --rpcserver localhost:8443 status
tapcli --tlscertpath /root/.lit/tls.cert --rpcserver localhost:8443 getinfo
```

([source](../../raw/docs/lightning-network-tools/lightning-terminal/get-lit.md))

## Integrated mode

The run guide recommends integrated mode, which runs everything in a single binary. Litd lets you selectively switch between integrated and remote mode for each component, so that each can be upgraded, patched or replaced with your own fork separately. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/run-litd.md))

**Configure Bitcoin.** If you have not run LND on this machine before, you need to configure a Bitcoin backend (see [[running-lnd]]). If you intend to run with a Neutrino backend, no action is needed in this step. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/run-litd.md))

**Configure litd.** Create the `.lit` directory and a configuration file:

```
mkdir ~/.lit
nano ~/.lit/lit.conf
```

Place the following in the file:

```
lnd-mode=integrated
uipassword=<a random password of your choosing>
```

LND is configured in the same file. An existing LND configuration can be copied into `lit.conf`, with every option prefixed with `lnd.`, for instance:

```
lnd.bitcoin.active=1
lnd.bitcoin.node=bitcoind
lnd.bitcoind.rpchost=127.0.0.1
lnd.bitcoind.rpcuser=youruser
lnd.bitcoind.rpcpass=yourpass
lnd.bitcoind.zmqpubrawblock=tcp://127.0.0.1:28332
lnd.bitcoind.zmqpubrawtx=tcp://127.0.0.1:28333
```

([source](../../raw/docs/lightning-network-tools/lightning-terminal/run-litd.md))

**Run litd.** Executing `litd` runs litd, LND, Loop, Pool and Faraday together. You have to unlock LND with `lncli unlock`, or create a new wallet if this is the first time starting LND. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/run-litd.md))

## Remote mode

Remote mode refers to a litd installation that runs separately from LND. By default, such an installation does not need configuration beyond passing a UI password. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/run-litd.md))

**Configure LND.** To use litd's Accounts (see [[litd-accounts-guide]]) and Autofees (see [[terminal-liquidity-tools]]) features, the RPC Middleware interceptor (see [[lnd-interceptors]]) must be enabled by adding this line to `lnd.conf`:

```
rpcmiddleware.enable=true
```

([source](../../raw/docs/lightning-network-tools/lightning-terminal/run-litd.md))

**Run litd.** Start litd with:

```
litd --uipassword=<your secure and unique password>
```

If litd is unable to connect to LND, you might have to manually pass the location of the macaroon and RPC port, or generate a litd configuration file, `~/.lit/lit.conf`:

```
lnd-mode=remote
remote.lnd.rpcserver=127.0.0.1:10009
remote.lnd.macaroonpath=/home/user/.lnd/data/chain/bitcoin/mainnet/admin.macaroon
remote.lnd.tlscertpath=/home/user/.lnd/tls.cert
```

([source](../../raw/docs/lightning-network-tools/lightning-terminal/run-litd.md))

It is also possible to run `litd` in either integrated or remote mode and swap Loop, Pool or Faraday between remote and integrated mode, for example:

```
lnd-mode=remote
faraday-mode=integrated
loop-mode=integrated
pool-mode=remote
```

([source](../../raw/docs/lightning-network-tools/lightning-terminal/run-litd.md))

## Regtest and signet

According to the run guide, to run `litd` on regtest or signet the autopilot has to be disabled with `autopilot.disable=true`. See [[litd-troubleshooting]] for the signet guide, which gives a second option (recorded under Conflicts below). ([source](../../raw/docs/lightning-network-tools/lightning-terminal/run-litd.md))

## Access the litd user interface

Once litd is running, you should be able to navigate to `localhost:8443` and access its user interface. To access the interface from a remote machine, launch litd with the flag `--httpslisten=0.0.0.0:8443` or add `httpslisten=0.0.0.0:8443` to your `lit.conf` file. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/run-litd.md))

The wallet needs to be unlocked with `lncli unlock` before you can access the user interface. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/connect.md))

## Connect to Terminal

In your local installation of Terminal, click "Connect to Terminal" to be taken directly to Terminal on the web. Alternatively, scan the QR code with a smart phone or tablet to open a new session on another device. All existing sessions can be inspected and revoked under "Lightning Node Connect." ([source](../../raw/docs/lightning-network-tools/lightning-terminal/connect.md))

If you cannot access the machine running `litd` via the browser, or prefer to keep port `8443` closed, generate a new pairing phrase with `litcli`:

```
litcli sessions add --label="default" --type=admin
```

Then navigate to https://terminal.lightning.engineering and click 'Connect your Node.' You are asked for your 10-word pairing phrase; enter it and confirm. You then need to choose a secure and unique password; the guide recommends a password manager. Sessions are described in [[lightning-node-connect]] and the API behind `litcli sessions` in [[lit-sessions]]. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/connect.md))

## Speed run: a new node on a fresh server

Using `litd` in integrated mode and the Neutrino backend, the demo spins up a Lightning Network node, fully synced to chain and graph, within 15 minutes on a fresh Ubuntu Virtual Private Server. The hardware used is a VPS with 2GB of RAM and 1 vCPU running Ubuntu 22.04 LTS, with 20GB of space on an SSD, brought up to date with `sudo apt update` and `sudo apt upgrade`. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/speedrun.md))

**Download and verify.** The demo uses release `v0.11.0-alpha`; the guide says to check the release page for the latest version, manifest, gpg signatures and the key used to sign them.

```
gpg --keyserver hkps://keyserver.ubuntu.com --recv-keys 187F6ADD93AE3B0CF335AA6AB984570980684DCC
wget https://github.com/lightninglabs/lightning-terminal/releases/download/v0.11.0-alpha/lightning-terminal-linux-amd64-v0.11.0-alpha.tar.gz
wget https://github.com/lightninglabs/lightning-terminal/releases/download/v0.11.0-alpha/manifest-v0.11.0-alpha.sig
wget https://github.com/lightninglabs/lightning-terminal/releases/download/v0.11.0-alpha/manifest-v0.11.0-alpha.txt
```

Then verify that the manifest is properly signed and that the sha256 sum in the manifest matches the one you calculate:

```
gpg --verify manifest-v0.11.0-alpha.sig manifest-v0.11.0-alpha.txt
cat manifest-v0.11.0-alpha.txt
sha256sum lightning-terminal-linux-amd64-v0.11.0-alpha.tar.gz
```

([source](../../raw/docs/lightning-network-tools/lightning-terminal/speedrun.md))

**Install.** Move the binaries to a location where the operating system can find them:

```
cd lightning-terminal-linux-amd64-v0.11.0-alpha/
sudo mv * /usr/local/bin
```

([source](../../raw/docs/lightning-network-tools/lightning-terminal/speedrun.md))

**Configure.** Create `~/.lit` and `~/.lit/lit.conf`. The sample configuration (the guide stresses creating a new password) is:

```
httpslisten=0.0.0.0:8443
uipassword=dont use this password you will use all your coins
lnd-mode=integrated
lnd.bitcoin.active=1
lnd.bitcoin.mainnet=1
lnd.bitcoin.node=neutrino
lnd.feeurl=https://nodes.lightning.computer/fees/v1/btc-fee-estimates.json
lnd.protocol.option-scid-alias=true
lnd.protocol.zero-conf=true
```

([source](../../raw/docs/lightning-network-tools/lightning-terminal/speedrun.md))

**Start.** Start with the command `litd`, or use `nohup` to push the process into the background and observe its logs:

```
nohup litd > /dev/null 2> /home/ubuntu/.lit/err.log &
tail -f ~/.lit/logs/mainnet/litd.log
```

([source](../../raw/docs/lightning-network-tools/lightning-terminal/speedrun.md))

**Create a wallet and sync.** Create a new wallet with `lncli create`, and write the new seed phrase down securely. Then wait for `litd` to sync, checking progress with `lncli getinfo` and `lncli getnetworkinfo` until "synced to chain" and "synced to graph" both appear as `true`. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/speedrun.md))

**Connect.** Navigate to the node's IP address at port `8443` to access the litd UI and connect to Lightning Terminal. This requires the configured UI password, as well as a second, new password generated with your password manager. The node is then ready to receive funds, open channels and make payments. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/speedrun.md))

## Conflicts

- **Is Taproot Assets bundled?** The install guide says litd bundles "LND with Loop, Pool, Faraday, and Taproot Assets" ([source](../../raw/docs/lightning-network-tools/lightning-terminal/get-lit.md)). The run guide says integrated mode runs "LND, Loop, Pool, Faraday and in the future, Taproot Assets" ([source](../../raw/docs/lightning-network-tools/lightning-terminal/run-litd.md)).
- **Autopilot on signet.** The run guide says the autopilot "has to be disabled" on regtest or signet ([source](../../raw/docs/lightning-network-tools/lightning-terminal/run-litd.md)). The signet guide says autopilot has to be either disengaged or pointed at a separate host with `autopilot.address=signet.autopilot.lightning.finance:12010` ([source](../../raw/docs/lightning-network-tools/lightning-terminal/testing-on-signet.md)). See [[litd-troubleshooting]].
- **UI scheme.** The connect guide's text says to navigate to `http://127.0.0.1:8443`, while the caption of its screenshot says `https://127.0.0.1:8443` ([source](../../raw/docs/lightning-network-tools/lightning-terminal/connect.md)). The configuration option for the listener is named `httpslisten` ([source](../../raw/docs/lightning-network-tools/lightning-terminal/run-litd.md)).
- **Configuration file name.** The speed run creates `~/.lit/lit.conf` but later refers to "the password set in the `litd.conf` file" ([source](../../raw/docs/lightning-network-tools/lightning-terminal/speedrun.md)).
