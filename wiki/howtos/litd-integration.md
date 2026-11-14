---
title: Integrating litd and its CLI
type: howto
sources:
  - raw/docs/lightning-network-tools/lightning-terminal/integrating-litd.md
  - raw/docs/lightning-network-tools/lightning-terminal/command-line-interface.md
  - raw/docs/lightning-network-tools/lightning-terminal/run-litd.md
  - raw/docs/lightning-network-tools/lightning-terminal/speedrun.md
  - raw/docs/lightning-network-tools/lightning-terminal/get-lit.md
  - raw/docs/lightning-network-tools/lightning-terminal/lnc-npm.md
updated: 2026-11-14
---

# Integrating litd and its CLI

This page covers moving an existing node into litd's integrated mode, going back to remote mode, and how the command line tools (`litcli`, `lncli`, `loop`, `pool`, `frcli`, `tapcli`) are pointed at litd. Installation and first-time configuration are in [[running-litd]]; the product overview is [[lightning-terminal]].

Integrated mode means litd, LND, Loop, Pool, Taproot Assets and Faraday are bundled into a single binary, which simplifies starting, stopping and upgrading them. The guide describes integration as easy, convenient and reversible at any time. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/integrating-litd.md))

## Evaluate

Consider which of litd, Loop, Pool and Faraday you run next to LND, and whether to integrate all of them or only some. Not integrating a specific service makes sense when you run custom code or pre-release software, or want more granular control over when to upgrade each service. If you run pre-release software, make sure you are not downgrading LND or any other service, as this might cause problems; the litd releases page shows which software is bundled with the latest release. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/integrating-litd.md))

## Integrate a service

1. Stop litd and the process you are integrating. If you are integrating LND, stop all processes.
2. Configure litd to integrate the service, for example by setting `lnd-mode=integrated` in your `lit.conf` file, or by passing `--lnd-mode=integrated` at startup. If your .lnd directory, macaroon and TLS certificate are in a non-standard location, specify these as well.
3. Migrate the `lnd.conf` configuration to `lit.conf`: copy all options over, prefixed with `lnd.`. For example, `bitcoin.active=1` becomes `lnd.bitcoin.active=1`.
4. Start litd with the command `litd`. This starts litd and all processes set to integrated mode. All remote processes have to be started separately.

([source](../../raw/docs/lightning-network-tools/lightning-terminal/integrating-litd.md))

## After integrating

When integrating LND, the service remains reachable with the same macaroon at the usual port, so no adjustments are necessary. The Loop, Pool and Faraday processes are reachable inside litd at port `8443` using the litd TLS certificate. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/integrating-litd.md))

## Going back to remote mode

It is always possible to go back to remote mode for any of the integrated services: stop the litd process, change its configuration and start the remote services separately before restarting litd in remote mode. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/integrating-litd.md))

## Command line interfaces

Litd comes with the command line interface `litcli`, primarily used to generate new sessions for [[lightning-node-connect]] and to interact with LND Accounts (see [[litd-accounts-guide]]). In addition, litd optionally bundles LND, Pool, Loop and Faraday with their command line interfaces. Compiling `litd` does not by default build `lncli`, `pool`, `loop` and `frcli`, as these might already be on your system; to compile them, run `make go-install-cli`. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/command-line-interface.md))

These CLIs by default point at their standalone clients, so when using litd in integrated mode the arguments have to be adjusted. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/command-line-interface.md))

### litcli

```
litcli sessions add --label="My LNC" --type admin
```

By default, a pairing phrase created with litcli is valid for 3 months and is set to "readonly", meaning invoices cannot be paid or created and channels cannot be opened. This can be changed with the `--expiry <seconds>` and `--type` flags. The services `litcli` talks to are described in [[lit-sessions]], [[lit-accounts]], [[lit-autopilot]], [[lit-firewall]], [[lit-proxy]] and [[lit-status]]. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/command-line-interface.md))

### Bundled CLIs in integrated mode

In integrated mode, all binaries including LND are run as one. The guide states that all of these services are exposed both via port 8443 and 10009, and that by default the TLS certificate can be found in `~/.lit/tls.cert`; in some cases this certificate path has to be specified for the connection to succeed. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/command-line-interface.md))

| Tool | Example from the guide |
|---|---|
| `loop` | `loop --tlscertpath ~/.lit/tls.cert --rpcserver=localhost:8443 terms in` |
| `pool` | `pool --tlscertpath ~/.lit/tls.cert --rpcserver=localhost:8443 accounts list` |
| `frcli` | `frcli --tlscertpath ~/.lit/tls.cert --rpcserver=localhost:8443 insights` |
| `tapcli` | `tapcli --tlscertpath ~/.lit/tls.cert --rpcserver=localhost:8443 --network=mainnet accounts list` |
| `lncli` | `lncli getinfo` |

([source](../../raw/docs/lightning-network-tools/lightning-terminal/command-line-interface.md))

In integrated mode, LND is available through the same port as when run as a standalone process, and its TLS certificate is stored in its expected location, so `lncli` calls need no modification. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/command-line-interface.md))

The products behind these tools have their own pages: [[loop]] and [[using-loop]], [[pool]], [[faraday]] and [[using-faraday]], [[taproot-assets]], and [[lnd]].

## Conflicts

- **Log location in integrated mode.** The integration guide says that in integrated mode "all logs are written to `~/.lnd/logs/bitcoin/mainnet/lnd.log`" ([source](../../raw/docs/lightning-network-tools/lightning-terminal/integrating-litd.md)). The speed run, which also uses integrated mode, follows the log with `tail -f ~/.lit/logs/mainnet/litd.log` ([source](../../raw/docs/lightning-network-tools/lightning-terminal/speedrun.md)).
- **What "remote mode" means.** The CLI guide says "In remote mode, `litd`, `loopd`, `poold`, `faraday` and `tapd` are run as part of the same binary by default, although each daemon may be run separately, or *remote*" ([source](../../raw/docs/lightning-network-tools/lightning-terminal/command-line-interface.md)). The run guide says "Remote mode refers to a litd installation that runs separately from LND" ([source](../../raw/docs/lightning-network-tools/lightning-terminal/run-litd.md)).
- **Ports for the bundled services.** The integration guide says Loop, Pool and Faraday are reachable inside litd at port `8443` ([source](../../raw/docs/lightning-network-tools/lightning-terminal/integrating-litd.md)). The CLI guide says all services are exposed via both port 8443 and 10009 ([source](../../raw/docs/lightning-network-tools/lightning-terminal/command-line-interface.md)).
- **litcli TLS flag.** The BTCPay instructions call `litcli --tlscertpath /root/.lit/tls.cert --rpcserver localhost:8443 status` ([source](../../raw/docs/lightning-network-tools/lightning-terminal/get-lit.md)). The LNC demo calls `litcli --lndtlscertpath ~/.lit/tls.cert sessions add --label="LNC Demo" --type admin` ([source](../../raw/docs/lightning-network-tools/lightning-terminal/lnc-npm.md)). The sources do not say whether both flags are accepted.
- **Which daemons are bundled.** The CLI guide's intro says litd optionally bundles "LND, Pool, Loop and Faraday", while the same page lists `tapd` among the daemons and gives a `tapcli` example ([source](../../raw/docs/lightning-network-tools/lightning-terminal/command-line-interface.md)); the integration guide includes Taproot Assets in the bundle ([source](../../raw/docs/lightning-network-tools/lightning-terminal/integrating-litd.md)).
