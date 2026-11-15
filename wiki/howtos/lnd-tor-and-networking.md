---
title: Tor, NAT traversal and node security
type: howto
sources:
  - raw/docs/lightning-network-tools/lnd/configuring_tor.md
  - raw/docs/lightning-network-tools/lnd/quick-tor-setup.md
  - raw/docs/lightning-network-tools/lnd/nat_traversal.md
  - raw/docs/lightning-network-tools/lnd/secure-your-lightning-network-node.md
  - raw/docs/lightning-network-tools/lnd/optimal-configuration-of-a-routing-node.md
updated: 2026-11-14
---

# Tor, NAT traversal and node security

This page covers how [[lnd]] reaches and is reached by peers (Tor, hybrid mode, NAT traversal) and the security practices the Builder's Guide recommends for a node.

## Why Tor

`lnd` supports Lightning over Tor. Routing nodes no longer need to expose their location through an advertised IP address, and leaf nodes can protect their location by using Tor to establish connections. Onion services also let nodes accept inbound connections when they are behind a NAT. The guide states that `lnd` supports both v2 and v3 onion services, and that v3 onion services require Tor version 0.3.3.6 or later ([source](../../raw/docs/lightning-network-tools/lnd/configuring_tor.md)).

The Tor configuration only tunnels `lnd`'s Lightning protocol traffic. A Bitcoin full node running alongside must be proxied over Tor separately; with the `neutrino` backend, `lnd` defaults to Tor automatically when Tor is active ([source](../../raw/docs/lightning-network-tools/lnd/configuring_tor.md)).

The quick setup guide compares three modes ([source](../../raw/docs/lightning-network-tools/lnd/quick-tor-setup.md)):

| Mode | Can reach | Reachable by |
|---|---|---|
| Tor | all nodes | only Tor nodes |
| IPv4/6 | only IPv4/6 nodes | all nodes |
| Hybrid | all nodes | all nodes |

Tor-only is recommended if you are behind a NAT and do not want to disclose your node's IP address. Hybrid mode is available starting with `lnd 0.14.0`, and the guide states that "Hybrid mode is not a privacy tool" ([source](../../raw/docs/lightning-network-tools/lnd/quick-tor-setup.md)).

## Start Tor

Run `tor` locally before starting `lnd`. The example `torrc` used in the guide is ([source](../../raw/docs/lightning-network-tools/lnd/configuring_tor.md)):

```
SOCKSPort 9050
Log notice stdout
ControlPort 9051
CookieAuthentication 1
```

Wait until the Tor log shows `Bootstrapped 100%: Done` before starting `lnd` ([source](../../raw/docs/lightning-network-tools/lnd/configuring_tor.md)).

## Tor flags

The `lnd -h` output lists these Tor options ([source](../../raw/docs/lightning-network-tools/lnd/configuring_tor.md)):

| Flag | Description / default |
|---|---|
| `--tor.active` | Allow outbound and inbound connections to be routed through Tor |
| `--tor.socks=` | Tor's SOCKS5 proxy (default: `localhost:9050`) |
| `--tor.dns=` | DNS server for SRV queries, must have TCP resolution enabled (default: `soa.nodes.lightning.directory:53`) |
| `--tor.streamisolation` | Randomize user credentials for each connection |
| `--tor.control=` | Tor control port (default: `localhost:9051`) |
| `--tor.targetipaddress=` | IP address Tor should use as the target of the hidden service |
| `--tor.password=` | Password for HASHEDPASSWORD auth instead of SAFECOOKIE |
| `--tor.v2` | Automatically set up a v2 onion service |
| `--tor.v3` | Automatically set up a v3 onion service |
| `--tor.privatekeypath=` | Path to the onion service private key |

`--tor.dns` is needed to bootstrap peer connections automatically, because the Tor daemon does not proxy `SRV` queries; `lnd` connects directly to the authoritative DNS server over TCP instead ([source](../../raw/docs/lightning-network-tools/lnd/configuring_tor.md)).

Common invocations ([source](../../raw/docs/lightning-network-tools/lnd/configuring_tor.md)):

```
./lnd --tor.active --tor.v3                       # outbound and inbound over Tor
./lnd --tor.active                                # outbound only; listening is disabled
./lnd --tor.active --tor.streamisolation          # new circuit per connection
./lnd --tor.active --tor.v3 --listen=localhost    # inbound via onion service, no leaks
```

To listen for inbound connections over Tor without leaking identifying information, the guide says `listen=localhost` is also necessary. `lnd` saves the onion private key as `v2_onion_private_key` or `v3_onion_private_key` in its base directory so it can recreate the same hidden service on restart; delete the file to get a new onion service ([source](../../raw/docs/lightning-network-tools/lnd/configuring_tor.md)).

## lnd.conf setup (quick guide)

The quick setup uses these `lnd.conf` lines ([source](../../raw/docs/lightning-network-tools/lnd/quick-tor-setup.md)):

```
tor.active=true
tor.dns=nodes.lightning.directory
tor.socks=127.0.0.1:9050
tor.streamisolation=true
```

Set `tor.streamisolation` to `false` if you have many channels or prefer channels to come online quickly rather than privately ([source](../../raw/docs/lightning-network-tools/lnd/quick-tor-setup.md)).

For hybrid mode, add `tor.skip-proxy-for-clearnet-targets=1`. To be reachable on clearnet as well, add `externalip=<your IP here>` ([source](../../raw/docs/lightning-network-tools/lnd/quick-tor-setup.md)).

To create a hidden service: uncomment `ControlPort 9051` in `torrc`, set `tor.password=<password>` in `lnd.conf`, hash it with `tor --hash-password <password>`, add `HashedControlPassword <hash>` under ControlPort in `torrc`, then set `tor.v3=true`. Optional settings are `tor.control=localhost:9051`, `tor.targetipaddress=`, `tor.privatekeypath=/path/to/torkey` and `tor.watchtowerkeypath=/other/path/`. By default the keys are placed in `~/.lnd` ([source](../../raw/docs/lightning-network-tools/lnd/quick-tor-setup.md)).

## Tor control authentication

`lnd` supports these Tor control authentication methods, listed from most to least secure ([source](../../raw/docs/lightning-network-tools/lnd/configuring_tor.md)):

- `SAFECOOKIE`: relies on a cookie stored by the Tor daemon; the default when `torrc` has `CookieAuthentication 1`.
- `HASHEDPASSWORD`: stateless; useful when Tor runs on a separate host. Generate the hash with `tor --hash-password PASSWORD`, put it in `torrc` as `HashedControlPassword`, and pass the password with `--tor.password`.
- `NULL`: no authentication and no extra flags.

## NAT traversal

`lnd` supports UPnP and NAT-PMP, enabled with the `--nat` flag (`lnd ... --nat`). On startup `lnd` tries each technique until one works with your hardware. These techniques rely on system-specific binaries to detect the gateway address; if they are missing, `lnd` exits with an error. `lnd` also runs a background thread that detects IP address changes and propagates the new address to the network ([source](../../raw/docs/lightning-network-tools/lnd/nat_traversal.md)).

## Securing the node

**Device and platform.** Know who can physically access the device, or check the trustworthiness of a server provider. Keep the OS and services such as OpenSSH updated. Use a firewall: opening port 9735 is not required but recommended to accept incoming connections and inbound channels; REST and RPC (default ports 8080 and 10009) only need to be exposed when an external application requires them. Consider SSH or VPN-only access and key-only authentication ([source](../../raw/docs/lightning-network-tools/lnd/secure-your-lightning-network-node.md)).

**lnd binaries.** Verify binaries or source with PGP and `git verify-tag`, including dependencies such as Go, and update regularly. When updating from source the guide gives ([source](../../raw/docs/lightning-network-tools/lnd/secure-your-lightning-network-node.md)):

```
git pull
make clean && make && make install tags="autopilotrpc chainrpc invoicesrpc routerrpc signrpc walletrpc watchtowerrpc wtclientrpc"
```

**Wallet.** `lncli create` gives a 24-word "aezeed" seed that can recover on-chain funds. Store it on paper or in encrypted storage. Never run two separate LND nodes with the same seed. The private key is in `wallet.db`; the wallet database and macaroon database are encrypted with the wallet password, and a lost password can be worked around by recreating the wallet and macaroon database from the seed ([source](../../raw/docs/lightning-network-tools/lnd/secure-your-lightning-network-node.md)).

**Macaroons.** Deleting a macaroon file does not invalidate it. The guide says the macaroon database has to be deleted entirely, or a specific macaroon invalidated with `lncli deletemacaroonid` and its macaroon ID. Default macaroons are `admin.macaroon`, `invoice.macaroon`, `readonly.macaroon` and `router.macaroon` in `<lnddir>/data/chain/bitcoin/mainnet/` ([source](../../raw/docs/lightning-network-tools/lnd/secure-your-lightning-network-node.md)).

**Channels.** Back up `channel.backup` (typically `~/.lnd/data/chain/bitcoin/mainnet/channel.backup`) whenever a channel is opened. `channel.db` is not suitable for backups and may lose funds if restored from an outdated copy; it can only be used when migrating ([source](../../raw/docs/lightning-network-tools/lnd/secure-your-lightning-network-node.md)).

**Operational safety.** Do not interrupt `lncli` commands that alter `channel.db`: `openchannel`, `closechannel`, `closeallchannels`, `abandonchannel`, `updatechanpolicy`, `restorechanbackup`. Shut down with `lncli stop` ([source](../../raw/docs/lightning-network-tools/lnd/secure-your-lightning-network-node.md)).

## Conflicts

- **Macaroon database file name.** The secure-your-node guide calls it `macaroons.db` in its Macaroons section and `macaroon.db` in its External applications section ([source](../../raw/docs/lightning-network-tools/lnd/secure-your-lightning-network-node.md)).
- **Hybrid mode option.** The quick Tor guide gives `tor.skip-proxy-for-clearnet-targets=1` ([source](../../raw/docs/lightning-network-tools/lnd/quick-tor-setup.md)); the routing node guide gives `lnd.tor.skip-proxy-for-clearnet-targets=true # (default: false)`, in a context where the `lnd.` prefix is for `lit.conf` ([source](../../raw/docs/lightning-network-tools/lnd/optimal-configuration-of-a-routing-node.md)).
- **Tor DNS value.** `lnd -h` shows the `--tor.dns` default as `soa.nodes.lightning.directory:53` ([source](../../raw/docs/lightning-network-tools/lnd/configuring_tor.md)); the quick guide's example sets `tor.dns=nodes.lightning.directory` ([source](../../raw/docs/lightning-network-tools/lnd/quick-tor-setup.md)).

See also: [[lnd-configuration]], [[lnd-macaroons]], [[lnd-recovery]], [[lnd-routing-node-operations]], [[lnd-watchtower-setup]], [[running-lnd]].
