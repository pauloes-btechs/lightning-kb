---
title: Installing and starting Pool
type: howto
sources:
  - raw/docs/lightning-network-tools/pool/install.md
  - raw/docs/lightning-network-tools/pool/quickstart.md
  - raw/docs/lightning-network-tools/pool/first-steps.md
  - raw/docs/lightning-network-tools/pool/accounts.md
  - raw/docs/lightning-network-tools/pool/zero-confirmation-channels.md
  - raw/docs/lightning-network-tools/pool/faq.md
  - raw/api/api-docs/api/pool.md
updated: 2026-11-14
---

# Installing and starting Pool

See also: [[pool]], [[lnd]], [[pool-accounts]], [[pool-orders-and-batches]].

## 1. Get the binaries

Pool has two binaries: the trader daemon `poold`, which runs constantly in the background, and the command line tool `pool`, which interacts with the daemon. `poold` can be run as a standalone binary connected to a compatible `lnd` node or integrated into Lightning Terminal (LiT). ([source](../../raw/docs/lightning-network-tools/pool/install.md))

- **Standalone binaries:** download the latest official release from `https://github.com/lightninglabs/pool/releases`. ([source](../../raw/docs/lightning-network-tools/pool/install.md))
- **As part of LiT:** download the latest release of LiT from `https://github.com/lightninglabs/lightning-terminal/releases` and follow LiT's installation instructions. See [[lightning-terminal]] and [[running-litd]]. ([source](../../raw/docs/lightning-network-tools/pool/install.md))
- **From source:** at least `go 1.14` and `make` must be installed. Then run the commands below, which install the binaries into `$GOPATH/bin`. ([source](../../raw/docs/lightning-network-tools/pool/install.md))

```
git clone https://github.com/lightninglabs/pool
cd pool
make install
```

## 2. Prepare lnd

Pool needs to be connected to an `lnd` node version `v0.11.1-beta` or later. An official release binary of `lnd` is recommended. Installing `lnd` from source is possible but must be done with all sub-server build flags enabled: `make install tags="signrpc walletrpc chainrpc invoicesrpc"`. See [[running-lnd]]. ([source](../../raw/docs/lightning-network-tools/pool/install.md))

The `lnd` node must have at least one active channel and must be able to pay a 1000 satoshi LSAT fee (see [[l402]]). The first-steps guide puts it as: some funds in LND's on-chain wallet and at least one channel with enough outgoing capacity to pay 1000 satoshis for API access to Pool. ([source](../../raw/docs/lightning-network-tools/pool/quickstart.md), [source](../../raw/docs/lightning-network-tools/pool/first-steps.md))

The FAQ says this 1000 satoshi payment is a one time payment to obtain an LSAT token to communicate with the auction server, and that the token currently does not expire. ([source](../../raw/docs/lightning-network-tools/pool/faq.md))

## 3. Run poold

If `lnd` is configured with the default values and is running on the same machine, `poold` connects to it automatically. Mainnet is the default network; testnet has to be specified. ([source](../../raw/docs/lightning-network-tools/pool/install.md))

```
$ poold

# Or if you want to do everything in the same terminal and run poold in the
# background:
$ poold &

# For testnet mode, you'll need to specify the network as mainnet is the
# default:
$ poold --network=testnet
```

If you are using Lightning Terminal, run `litd` instead. ([source](../../raw/docs/lightning-network-tools/pool/quickstart.md))

### lnd on a remote node

When `lnd` runs on a remote node, the `tls.cert` and the `admin.macaroon` files from the `lnd` data directory need to be copied to the machine where `poold` is running. The daemon is then pointed at the remote node with these flags. ([source](../../raw/docs/lightning-network-tools/pool/install.md))

```
$ poold --lnd.host=<the_remote_host_IP_address>:10009 \
        --lnd.macaroonpath=/some/directory/with/lnd/data/macaroons/admin.macaroon \
        --lnd.tlspath=/some/directory/with/lnd/data/tls.cert
```

To persist the configuration, the same values can be written to a configuration file located in `~/.pool/<network>/poold.conf`, for example `~/.pool/mainnet/poold.conf`. ([source](../../raw/docs/lightning-network-tools/pool/install.md))

```
lnd.host=<the_remote_host_IP_address>:10009
lnd.macaroonpath=/some/directory/with/lnd/data/macaroons/admin.macaroon
lnd.tlspath=/some/directory/with/lnd/data/tls.cert
```

### Configuration options

`poold --help` prints the full list of options, including logging behaviour and the directories where `poold` stores its data. The install guide lists one flag that affects match making or business behaviour. ([source](../../raw/docs/lightning-network-tools/pool/install.md))

| Flag | Required | Default Value | Description |
| --- | --- | --- | --- |
| `newnodesonly` | No | `false` | If set to `true` the daemon will only buy channels from nodes it does not yet have channels with |

([source](../../raw/docs/lightning-network-tools/pool/install.md))

## 4. Authentication, ports and directories

The gRPC and REST connections of `poold` are encrypted with TLS and secured with macaroon authentication the same way `lnd` is. If no custom base directory is set, the TLS certificate is stored in `~/.pool/<network>/tls.cert` and the base macaroon in `~/.pool/<network>/pool.macaroon`. Pool's macaroons are independent from `lnd`'s: the same macaroon cannot be used for both `poold` and `lnd`. See [[macaroons]]. ([source](../../raw/docs/lightning-network-tools/pool/install.md))

The `pool` command picks up these files automatically on mainnet if no custom base directory is used. For other networks it should be sufficient to add the `--network` flag so the CLI knows which sub directory to look in. ([source](../../raw/docs/lightning-network-tools/pool/install.md))

The API reference's samples assume `poold` listens for gRPC on port `12010` and for REST on port `8281`, with a base directory of `~/.pool` on Linux and `~/Library/Application Support/Pool` on macOS. The gRPC services are described on [[pool-trader]], [[pool-channel-auctioneer]] and [[pool-hash-mail]]. ([source](../../raw/api/api-docs/api/pool.md))

Depending on the setup, you may have to tell the `pool` CLI where the `tls.cert` is and which RPC port to use so that it talks to the intended daemon. The guide's examples: ([source](../../raw/docs/lightning-network-tools/pool/zero-confirmation-channels.md))

```
litd:  pool --rpcserver=localhost:8443 --tlscertpath ~/.lit/tls.cert
poold: pool --rpcserver=localhost:12010 --tlscertpath ~/.pool/mainnet/tls.cert
```

## 5. First commands

Once the daemon is running, the quickstart sequence is: ([source](../../raw/docs/lightning-network-tools/pool/quickstart.md))

1. Create an account: `pool accounts new --amt=50000000 --expiry_height=1773394 --conf_target=6`. The funds are pulled from your `lnd` wallet.
2. View it: `pool accounts list`.
3. Submit an order: `pool orders submit bid`, with at least the `interest_rate_percent`, `amt` and `acct_key` flags.
4. Check the order: `pool orders list`.
5. After a match, inspect the result: `pool auction leases`.

The first-steps guide walks the same path with a concrete bid for an incoming channel, and mentions `--self_chan_balance` (to create balanced channels, with the balance coming out of the Pool account) and `--unannounced_channel` (when not interested in routing payments). ([source](../../raw/docs/lightning-network-tools/pool/first-steps.md))

```
pool orders submit bid –amt 100000 –acct_key 0389f9aad3e08ae5065985049428eb8d862455060b429e2ad42fda52830673e3c1 --interest_rate_percent 2 --max_batch_fee_rate 7 --lease_duration_blocks 2016
```

The command above is copied as the source prints it, including the en dashes in front of `amt` and `acct_key`. ([source](../../raw/docs/lightning-network-tools/pool/first-steps.md))

Details for each step: [[pool-accounts]], [[pool-orders-and-batches]], [[pool-channel-leases]]. The first-steps guide covers the command line and links elsewhere for using Pool "as part of the Lightning Pool user interface"; see [[terminal-liquidity-tools]]. ([source](../../raw/docs/lightning-network-tools/pool/first-steps.md))

## Conflicts

- **Confirmations before an account is usable.** The first-steps guide says "We will have to wait for two confirmations for the account to be open" ([source](../../raw/docs/lightning-network-tools/pool/first-steps.md)). The quickstart and the accounts page say "Once at least 3 blocks have passed (in the alpha), the account will be confirmed and ready for use" ([source](../../raw/docs/lightning-network-tools/pool/quickstart.md), [source](../../raw/docs/lightning-network-tools/pool/accounts.md)).
- **How the amount is passed to `pool accounts new`.** The first-steps guide uses a positional amount, `pool accounts new 5000000 --expiry_blocks 12960 --conf_target 12` ([source](../../raw/docs/lightning-network-tools/pool/first-steps.md)). The quickstart uses a flag, `pool accounts new --amt=50000000 --expiry_height=1773394 --conf_target=6` ([source](../../raw/docs/lightning-network-tools/pool/quickstart.md)).
