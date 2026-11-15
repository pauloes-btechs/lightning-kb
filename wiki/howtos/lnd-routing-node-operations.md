---
title: Operating a routing node with lnd
type: howto
sources:
  - raw/docs/lightning-network-tools/lnd/optimal-configuration-of-a-routing-node.md
updated: 2026-11-14
---

# Operating a routing node with lnd

The Builder's Guide page "Configuration of a Routing Node" walks through [[lnd]] and `bitcoind` settings a routing node operator may change from the defaults. The guide states: "Unless otherwise stated, the below configuration options are highlighted with their default values"; lines marked `# (default: ...)` give the default alongside a different value ([source](../../raw/docs/lightning-network-tools/lnd/optimal-configuration-of-a-routing-node.md)).

`lnd.conf` should be in `~/.lnd`. With `litd` in integrated mode, all the options go in `lit.conf` in `~/.lit`, prefixed with `lnd.` (for example `lnd.listen=:9735` instead of `listen=:9735`) ([source](../../raw/docs/lightning-network-tools/lnd/optimal-configuration-of-a-routing-node.md)).

## Hardware

A performant routing node runs on hardware well above the minimum requirements, with continuous power and reliable internet. Consider separate partitions or SSDs for the OS, Bitcoin data and LND data, and RAID for sensitive data such as `~/.lnd` ([source](../../raw/docs/lightning-network-tools/lnd/optimal-configuration-of-a-routing-node.md)).

## Bitcoin backend (`bitcoin.conf`)

A routing node does not aggressively prune, may index the chain, and may put the Bitcoin backend behind Tor without listening ([source](../../raw/docs/lightning-network-tools/lnd/optimal-configuration-of-a-routing-node.md)):

```
txindex=1 # (default: 0)
listen=0 # (default: 1)
onlynet=onion # (default: any)
proxy=127.0.0.1:9050
maxmempool=300
```

## Tor and connections

Hybrid mode (reachable via Tor and clearnet, connecting out through either) "maximizes availability across networks while limiting latency" ([source](../../raw/docs/lightning-network-tools/lnd/optimal-configuration-of-a-routing-node.md)):

```
lnd.tor.skip-proxy-for-clearnet-targets=true # (default: false)
listen=:9735
externalip=<your IPv6>
externalip=<your IPv4>
stagger-initial-reconnect=true # (default: false)
```

With `stagger-initial-reconnect`, the node connects to 10 peers first on restart, then waits between 0s and 30s before connecting to others ([source](../../raw/docs/lightning-network-tools/lnd/optimal-configuration-of-a-routing-node.md)).

## Channel defaults

Default fees should be high enough that liquidity is not underpriced when a new channel opens. Each HTLC carries the risk of a channel closure, so the minimum HTLC size may be raised. A `timelockdelta` of 144 allows up to 24h to resolve node issues before HTLCs resolve on chain; fewer HTLCs per channel limit force-close fallout but can make a channel unusable when all slots are used ([source](../../raw/docs/lightning-network-tools/lnd/optimal-configuration-of-a-routing-node.md)):

```
bitcoin.basefee=1000
bitcoin.feerate=2000 # (default: 1)
bitcoin.minhtlc=1
bitcoin.minhtlcout=1000
bitcoin.timelockdelta=144 # (default: 80)
default-remote-max-htlcs=483
maxpendingchannels=1
bitcoin.defaultchanconfs=[3; 6]
minchansize=1000000 # (default: 20000)
protocol.wumbo-channels=true # (default: false)
max-cltv-expiry=2016
payments-expiration-grace-period=1h # (default: 0s)
```

## Database

By default LND runs with bbolt; the guide says SQLite will become the default in the future. Supported backends are bbolt, etcd, SQLite and Postgres, with bbolt and etcd to be phased out. Options are `db.backend=bolt` (default), `db.backend=etcd`, `db.backend=postgres` and `db.backend=sqlite` ([source](../../raw/docs/lightning-network-tools/lnd/optimal-configuration-of-a-routing-node.md)).

SQLite or Postgres users can enable the native SQL schema with `db.use-native-sql=true`, available for new nodes since v0.18.0 and for existing nodes from v0.19.0. From 0.19, setting it and restarting triggers an automatic migration from kvdb to native SQL at startup; `db.skip-native-sql-migration=true` abandons the migration and should only be used if the migration errors ([source](../../raw/docs/lightning-network-tools/lnd/optimal-configuration-of-a-routing-node.md)).

Moving the backend from bbolt to SQLite or Postgres is done with the lndinit migration script, which keeps the kvdb structure. Migrating to Postgres with this tool is currently not recommended because the key-value schema can perform poorly there ([source](../../raw/docs/lightning-network-tools/lnd/optimal-configuration-of-a-routing-node.md)).

For node management, the guide says Bolt is significantly slower to start up, so a postgres or etcd backend restarts much quicker (`db.backend=postgres # (default: bolt)`). Bolt users can compact regularly ([source](../../raw/docs/lightning-network-tools/lnd/optimal-configuration-of-a-routing-node.md)):

```
db.bolt.auto-compact=true # (default: false)
db.bolt.auto-compact-min-age=168h
gc-canceled-invoices-on-startup=true # (default: false)
gc-canceled-invoices-on-the-fly=true # (default: false)
blockcachesize=20971520
```

## Rebalancing and routing

Rebalancing requires allowing circular routes. For a node that mainly pays to rebalance, the Router RPC settings below lower the chance of finding a path quickly but raise the chance of eventually finding a cheap route ([source](../../raw/docs/lightning-network-tools/lnd/optimal-configuration-of-a-routing-node.md)):

```
allow-circular-route=true # (default: false)
routerrpc.attemptcost=100
routerrpc.attemptcostppm=1000
routerrpc.apriori.hopprob=0.6
routerrpc.apriori.weight=0.5
routerrpc.apriori.penaltyhalflife=1h
routerrpc.apriori.capacityfraction=0.9999
```

`routing.strictgraphpruning=true # (default: false)` prunes a channel if only a single edge marked it inactive; the guide also lists `ignore-historical-gossip-filters=true # (default: false)` ([source](../../raw/docs/lightning-network-tools/lnd/optimal-configuration-of-a-routing-node.md)).

## High fee environment

These settings reduce on-chain cost at the risk of slower confirmation: choose the largest UTXOs, economical fee estimates, a high coop-close target, a higher anchor commit fee so commitment transactions propagate, a fee allocation cap, and a longer sweeper batch window with a lower max fee rate ([source](../../raw/docs/lightning-network-tools/lnd/optimal-configuration-of-a-routing-node.md)):

```
coin-selection-strategy=largest # (default: random)
bitcoind.estimatemode=ECONOMICAL # (default: CONSERVATIVE)
coop-close-target-confs=1000
max-commit-fee-rate-anchors=100 # (default: 10)
max-channel-fee-allocation=0.5
sweeper.batchwindowduration=30s
sweeper.maxfeerate=1000
```

## Communication, Terminal and Pool

To receive keysend messages from other operators: `accept-keysend=true # (default: false)` and `accept-amp=true # (default: false)`. Lightning Terminal needs `rpcmiddleware.enable=true # (default: false)`. Zero-confirmation channels bought or sold through Pool, or manually accepted through the channel acceptor, need `protocol.option-scid-alias=true` and `protocol.zero-conf=true` (both `# (default: false)`) ([source](../../raw/docs/lightning-network-tools/lnd/optimal-configuration-of-a-routing-node.md)).

## DDoS protection

To use a CDN, configure the node with a domain name, add it to the TLS certificate and advertise it instead of an IP: `tlsextradomain=my-node-domain.com` and `externalhosts=my-node-domain.com`. Not all CDNs support non-HTTPS data or non-standard ports by default. During an attack you may close ports, change IP, or remain reachable only via Tor; outgoing connections still work unless the network or your peers are also attacked. Linux qdisc can help, e.g. `sudo tc qdisc replace dev wg0 root cake bandwidth 300mbit nat` ([source](../../raw/docs/lightning-network-tools/lnd/optimal-configuration-of-a-routing-node.md)).

## Management tools

The guide lists Lightning Terminal (forwards, fees, balances, Autofees, Loop, Pool), Balance of Satoshis (balanced channels, probes, alerts, rebalancing) and LNDg (a GUI for LND data and automated rebalancing) ([source](../../raw/docs/lightning-network-tools/lnd/optimal-configuration-of-a-routing-node.md)).

## LND 0.19.2 gossip settings

If you see fluctuating peer counts, stable peers repeatedly disconnecting, or excessive bandwidth, the guide suggests ([source](../../raw/docs/lightning-network-tools/lnd/optimal-configuration-of-a-routing-node.md)):

```
gossip.msg-rate-bytes=524288
gossip.msg-burst-bytes=1048576
num-restricted-slots=200
```

See also: [[routing-nodes]], [[lnd-configuration]], [[lnd-channel-fees]], [[lnd-tor-and-networking]], [[lnd-interceptors]], [[lnd-sweeper]], [[liquidity]].
