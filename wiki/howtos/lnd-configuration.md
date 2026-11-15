---
title: lnd configuration and lnd.conf
type: howto
sources:
  - raw/docs/lightning-network-tools/lnd/lnd.conf.md
  - raw/docs/lightning-network-tools/lnd/run-lnd.md
updated: 2026-11-14
---

# lnd configuration and lnd.conf

A map of the sample `lnd.conf` for [[lnd]]: where the file lives, how values are written, which sections it has, and the options the sample explains. Option names and defaults below are copied from the sample; it is not a complete list. For the minimum settings needed to start a node, see [[running-lnd]].

## The file

The configuration file is in the LND directory, typically `~/.lnd`. The guide's sample file is "purely for illustrative purposes" and is not a template for an ideal node (for that, see [[lnd-routing-node-operations]]). ([source](../../raw/docs/lightning-network-tools/lnd/lnd.conf.md))

Default locations are `~/.lnd/lnd.conf` on POSIX, `$LOCALAPPDATA/Lnd/lnd.conf` on Windows, `~/Library/Application Support/Lnd/lnd.conf` on Mac OS and `$home/lnd/lnd.conf` on Plan9; `--configfile=` overrides the location at startup. ([source](../../raw/docs/lightning-network-tools/lnd/lnd.conf.md))

Conventions stated in the sample: booleans may be `true`/`false` or `1`/`0` and default to false; when one value is shown for an option it is also the default; when several example values are shown the default is stated explicitly; an empty value after the equals sign means lnd has no default. ([source](../../raw/docs/lightning-network-tools/lnd/lnd.conf.md))

## Sections

The sample is divided into these sections: `[Application Options]`, `[fee]`, `[prometheus]`, `[Bitcoin]`, `[Btcd]`, `[Bitcoind]`, `[neutrino]`, `[autopilot]`, `[tor]`, `[logging]`, `[watchtower]`, `[wtclient]`, `[healthcheck]`, `[signrpc]`, `[walletrpc]`, `[chainrpc]`, `[routerrpc]`, `[workers]`, `[caches]`, `[protocol]`, `[db]`, `[etcd]`, `[postgres]`, `[sqlite]`, `[bolt]`, `[cluster]`, `[rpcmiddleware]`, `[remotesigner]`, `[gossip]`, `[invoices]`, `[routing]`, `[sweeper]`, `[sweeper.budget]`, `[htlcswitch]`, `[grpc]`, `[pprof]`. ([source](../../raw/docs/lightning-network-tools/lnd/lnd.conf.md))

## Application Options

**Directories and TLS.** `datadir=~/.lnd/data`, `logdir=~/.lnd/logs` (logs auto-rotate and rotated logs are compressed). `tlscertpath=~/.lnd/tls.cert` and `tlskeypath=~/.lnd/tls.key` are the TLS files for the RPC and REST services; `tlsextraip=` and `tlsextradomain=` add entries to the certificate (old TLS files must be deleted if changed); `tlsautorefresh=false`, `tlscertduration=10080h` (about 14 months), `tlsdisableautofill=false`, and `tlsencryptkey=false` (encrypt the TLS key to the node's seed). Let's Encrypt is configured with `letsencryptdir`, `letsencryptlisten` (default `:80`) and `letsencryptdomain`. ([source](../../raw/docs/lightning-network-tools/lnd/lnd.conf.md))

**Macaroons.** `no-macaroons=false` disables macaroon authentication when set to true. `adminmacaroonpath`, `readonlymacaroonpath` and `invoicemacaroonpath` default to `~/.lnd/data/chain/bitcoin/${network}/admin.macaroon`, `readonly.macaroon` and `invoice.macaroon`. Sub-server macaroon paths are set in their own sections: `signrpc.signermacaroonpath`, `walletrpc.walletkitmacaroonpath`, `chainrpc.notifiermacaroonpath`, `routerrpc.routermacaroonpath`. See [[lnd-macaroons]]. ([source](../../raw/docs/lightning-network-tools/lnd/lnd.conf.md))

**Listeners.** P2P: `listen=:9735` by default, `nolisten=false`. gRPC: `rpclisten=localhost:10009` by default (a Unix socket such as `unix:///var/run/lnd/lnd-rpclistener.sock` is also allowed). REST: `restlisten=localhost:8080` by default, `restcors=` for allowed CORS origins, `norest=false`, `no-rest-tls=false`. `externalip=` advertises the node (port 9735 is added unless given); `nat=false` enables UPnP or NAT-PMP instead; `externalhosts=` lists domains to resolve and advertise. See [[lnd-tor-and-networking]]. ([source](../../raw/docs/lightning-network-tools/lnd/lnd.conf.md))

**Logging.** `debuglevel=info` by default; valid levels are `trace, debug, info, warn, error, critical`, and per-subsystem levels can be given like `debuglevel=debug,PEER=info` (list subsystems with `lncli debuglevel --show`). `maxlogfiles` and `maxlogfilesize` are deprecated in favour of `logging.file.max-files` (10) and `logging.file.max-file-size` (20 MB). The CPU/HTTP profiling options `cpuprofile`, `profile`, `blockingprofile`, `mutexprofile` are deprecated in favour of the `pprof.*` options. ([source](../../raw/docs/lightning-network-tools/lnd/lnd.conf.md))

**Wallet.** `coin-selection-strategy=largest` (options `largest`, `random`). `noseedbackup=false`: if true no seed is ever exposed and the wallet uses the default passphrase; the sample says it is only for testing and must never be used on mainnet. `wallet-unlock-password-file=` unlocks from a file and disables RPC unlocking; `wallet-unlock-allow-create=false` allows wallet creation through RPC when no wallet exists, which the sample does not recommend for high-security systems because the creation RPC is unauthenticated. `reset-wallet-transactions=false` drops on-chain transaction history and forces a rescan from the wallet birthday. ([source](../../raw/docs/lightning-network-tools/lnd/lnd.conf.md))

**Channels.** `minchansize=20000`; `maxchansize` defaults to 16777215 satoshis for non-wumbo and 1,000,000,000 satoshis for wumbo channels; `maxpendingchannels=1`; `coop-close-target-confs=6`; `default-remote-max-htlcs=483` (the maximum possible); `chan-enable-timeout=19m`, `chan-disable-timeout=20m`, `chan-status-sample-interval=1m`; `rejectpush=false`; `max-channel-fee-allocation=0.5`; `max-commit-fee-rate-anchors=10`; `channel-max-fee-exposure=500000` (replaces the deprecated `dust-threshold`; the sample warns that setting it too low might cause force closes); `enable-upfront-shutdown=false`; `backupfilepath` defaults to `~/.lnd/data/chain/bitcoin/${network}/channel.backup`, and `no-backup-archive=false` archives old backups. ([source](../../raw/docs/lightning-network-tools/lnd/lnd.conf.md))

**Forwarding and payments.** `rejecthtlc=false` (if true, lnd does not forward but still sends and receives); `requireinterceptor=false` (hold all HTLCs until an interceptor handles them, see [[lnd-interceptors]]); `accept-positive-inbound-fees=false` (by default only negative inbound fees are allowed, see [[lnd-channel-fees]]); `max-cltv-expiry=2016`; `allow-circular-route=false`; `payments-expiration-grace-period=0s`; `keep-failed-payment-attempts=false`. ([source](../../raw/docs/lightning-network-tools/lnd/lnd.conf.md))

**Spontaneous payments and invoices.** `accept-keysend=false`; `keysend-hold-time=0s` (experimental: accept keysend but do not settle immediately); `accept-amp=false` (spontaneous AMP; payments to AMP invoices are accepted regardless); `gc-canceled-invoices-on-startup=false` and `gc-canceled-invoices-on-the-fly=false`. See [[lnd-sending-payments]] and [[lnd-receiving-payments]]. ([source](../../raw/docs/lightning-network-tools/lnd/lnd.conf.md))

**Gossip and identity.** `nobootstrap=false`, `numgraphsyncpeers=3`, `historicalsyncinterval=1h`, `trickledelay=90000` (ms), `alias=` (up to 32 UTF-8 characters), `color=#3399FF`. Other defaults: `blockcachesize=20971520` (20 MB), `num-restricted-slots=30`, `acceptortimeout=15s`. ([source](../../raw/docs/lightning-network-tools/lnd/lnd.conf.md))

## Chain backend

`[Bitcoin]` selects the network (`bitcoin.mainnet`, `bitcoin.testnet`, `bitcoin.testnet4`, `bitcoin.simnet`, `bitcoin.regtest`, `bitcoin.signet`, all false by default) and the backend with `bitcoin.node`, whose options are `btcd`, `bitcoind` and `neutrino` (default `btcd`). The sample notes that switching between a full backend and neutrino is not supported. `bitcoin.active` is deprecated and ignored. ([source](../../raw/docs/lightning-network-tools/lnd/lnd.conf.md))

`[Bitcoin]` also holds channel defaults: `bitcoin.defaultchanconfs` (scaled between 3 and 6 by channel size if unset), `bitcoin.defaultremotedelay` (scaled between 144 and 2016), `bitcoin.maxlocaldelay=2016`, `bitcoin.minhtlc=1` and `bitcoin.minhtlcout=1000` (msat), and the forwarding policy `bitcoin.basefee=1000` (msat), `bitcoin.feerate=1` and `bitcoin.timelockdelta=80`. The total fee is `basefee + (amount * feerate / 1000000)`. ([source](../../raw/docs/lightning-network-tools/lnd/lnd.conf.md))

`[Bitcoind]` options include `bitcoind.dir`, `bitcoind.config`, `bitcoind.rpccookie`, `bitcoind.rpchost`, `bitcoind.rpcuser`, `bitcoind.rpcpass`, `bitcoind.zmqpubrawblock`, `bitcoind.zmqpubrawtx`, `bitcoind.zmqreaddeadline=5s`, `bitcoind.rpcpolling=false` (with `bitcoind.blockpollinginterval` and `bitcoind.txpollinginterval`), `bitcoind.estimatemode=CONSERVATIVE` and `bitcoind.pruned-node-max-peers=4`. lnd tries to obtain credentials and ZMQ settings automatically, so they mainly need setting for a remote bitcoind. `[Btcd]` has `btcd.dir`, `btcd.rpchost`, `btcd.rpcuser`, `btcd.rpcpass`, `btcd.rpccert` and `btcd.rawrpccert`. ([source](../../raw/docs/lightning-network-tools/lnd/lnd.conf.md))

`[neutrino]` has `neutrino.connect`, `neutrino.addpeer`, `neutrino.maxpeers=8`, `neutrino.assertfilterheader`, `neutrino.broadcasttimeout`, `neutrino.persistfilters=false` and `neutrino.validatechannels=false` (channel validation is off by default for Neutrino for graph sync performance). `[fee]` has `fee.url` (must be set for neutrino on mainnet), `fee.min-update-timeout=5m` and `fee.max-update-timeout=20m`. ([source](../../raw/docs/lightning-network-tools/lnd/lnd.conf.md))

## Other sections

| Section | Options the sample explains |
|---|---|
| `[prometheus]` | `prometheus.enable=false` (needs a build with `tags=monitoring`), `prometheus.listen=127.0.0.1:8989`, `prometheus.perfhistograms=false` |
| `[autopilot]` | `autopilot.active=false`, `autopilot.maxchannels=5`, `autopilot.allocation=0.6`, `autopilot.heuristic={top_centrality:1}`, `autopilot.minchansize=20000`, `autopilot.maxchansize=16777215` |
| `[tor]` | `tor.active=false`, `tor.socks=localhost:9050`, `tor.control=localhost:9051`, `tor.v3=false`, `tor.streamisolation=false`, `tor.skip-proxy-for-clearnet-targets=false`, `tor.encryptkey=false` |
| `[logging]` | `logging.console.disable`, `logging.file.disable`, `logging.file.max-files=10`, `logging.file.max-file-size=20`, `logging.file.compressor=gzip` |
| `[watchtower]` | `watchtower.active=false` (listens on :9911 by default), `watchtower.listen`, `watchtower.externalip`, `watchtower.towerdir` |
| `[wtclient]` | `wtclient.active=false`, `wtclient.sweep-fee-rate=10` (sat/vbyte), `wtclient.max-updates=1024` |
| `[healthcheck]` | chain backend, disk space, TLS, Tor, remote signer and leader checks, each with `attempts`, `timeout`, `backoff`, `interval` |
| `[routerrpc]` | `routerrpc.estimator=apriori` (or experimental `bimodal`), `routerrpc.minrtprob=0.01`, `routerrpc.attemptcost=100`, `routerrpc.attemptcostppm=1000`, `routerrpc.apriori.*`, `routerrpc.bimodal.*`, `routerrpc.fee-estimation-timeout=1m` |
| `[protocol]` | `protocol.wumbo-channels=false`, `protocol.no-anchors=false`, `protocol.option-scid-alias=false`, `protocol.zero-conf=false` (requires option-scid-alias), `protocol.simple-taproot-chans=false`, `protocol.no-route-blinding=false`, `protocol.custom-message` |
| `[db]` | `db.backend=bolt` (experimental etcd, postgres and sqlite), `db.no-graph-cache=false`, `db.use-native-sql=false`; backend options under `db.etcd.*`, `db.postgres.*`, `db.sqlite.*`, `db.bolt.*` (including `db.bolt.auto-compact=false`, `db.bolt.auto-compact-min-age=168h`) |
| `[cluster]` | `cluster.enable-leader-election=false`, `cluster.leader-elector=etcd`, `cluster.leader-session-ttl=90` |
| `[rpcmiddleware]` | `rpcmiddleware.enable=false`, `rpcmiddleware.intercepttimeout=2s`, `rpcmiddleware.addmandatory` |
| `[remotesigner]` | `remotesigner.enable=false`, `remotesigner.rpchost`, `remotesigner.macaroonpath`, `remotesigner.tlscertpath`, `remotesigner.timeout=5s`, `remotesigner.migrate-wallet-to-watch-only=false` |
| `[gossip]` | `gossip.pinned-syncers`, `gossip.max-channel-update-burst=10`, `gossip.channel-update-interval=1m`, `gossip.announcement-conf=6` |
| `[invoices]` | `invoices.holdexpirydelta=12` |
| `[routing]` | `routing.strictgraphpruning=false`, `routing.blinding.min-num-real-hops=1`, `routing.blinding.num-hops=2`, `routing.blinding.max-num-paths=3` |
| `[sweeper]`, `[sweeper.budget]` | `sweeper.maxfeerate=1000`, `sweeper.nodeadlineconftarget=1008`, budget ratios such as `sweeper.budget.tolocalratio=0.5` |
| `[htlcswitch]`, `[grpc]`, `[pprof]` | `htlcswitch.mailboxdeliverytimeout=1m`; gRPC keepalive options; `pprof.profile`, `pprof.cpuprofile`, `pprof.blockingprofile`, `pprof.mutexprofile` |

([source](../../raw/docs/lightning-network-tools/lnd/lnd.conf.md))

The `[remotesigner]` section says a remote signer is only recommended if the local wallet is watch-only, and that `remotesigner.migrate-wallet-to-watch-only` cannot be undone and purges all private keys after the first unlock. See [[lnd-wallet-and-psbt]]. ([source](../../raw/docs/lightning-network-tools/lnd/lnd.conf.md))

## Settings the Get Started guide highlights

The Get Started guide recommends `rpcmiddleware.enable=true` (needed for Autofees and LND Accounts) and lists `db.bolt.auto-compact=true` and `alias=` as popular settings. ([source](../../raw/docs/lightning-network-tools/lnd/run-lnd.md))

## Conflicts

- Fee URL option name: the Get Started guide configures Neutrino with `feeurl=https://nodes.lightning.computer/fees/v1/btc-fee-estimates.json` ([source](../../raw/docs/lightning-network-tools/lnd/run-lnd.md)), while the sample `lnd.conf` marks `feeurl` as "DEPRECATED: Use 'fee.url' option" ([source](../../raw/docs/lightning-network-tools/lnd/lnd.conf.md)).
- Blinded path option name: the comment on `routing.blinding.num-hops` refers to "invoices.blinding.min-num-real-hops", but the option defined just above it in the same file is `routing.blinding.min-num-real-hops` ([source](../../raw/docs/lightning-network-tools/lnd/lnd.conf.md)).

See also: [[lnd]], [[running-lnd]], [[lnd-macaroons]], [[lnd-tor-and-networking]], [[lnd-watchtower-setup]], [[lnd-sweeper]], [[lnd-debugging-and-contributing]], [[lnd-routing-node-operations]].
