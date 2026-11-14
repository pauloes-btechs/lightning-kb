---
title: Using Faraday and frcli
type: howto
sources:
  - raw/docs/lightning-network-tools/faraday/get-started.md
  - raw/docs/lightning-network-tools/faraday/the-faraday-cli.md
  - raw/api/api-docs/api/faraday/faraday-server/channel-insights.md
  - raw/api/api-docs/api/faraday/faraday-server/node-audit.md
  - raw/api/api-docs/api/faraday/faraday-server/outlier-recommendations.md
  - raw/api/api-docs/api/faraday/faraday-server/threshold-recommendations.md
updated: 2026-11-14
---

# Using Faraday and frcli

How to install and run [[faraday]] and use its command line interface `frcli`. The RPCs behind the commands are on [[faraday-server]].

## Install

Faraday comes bundled in Lightning Terminal, so if Lightning Terminal is installed the installation step can be skipped (see [[running-litd]]). ([source](../../raw/docs/lightning-network-tools/faraday/get-started.md))

To run Faraday you need to be running LND from the binary releases, or compiled from source with `make install tags="signrpc walletrpc chainrpc invoicesrpc"` (see [[running-lnd]]). ([source](../../raw/docs/lightning-network-tools/faraday/get-started.md))

Faraday can be run directly from the binary releases, or compiled from source:

```
git clone https://github.com/lightninglabs/faraday.git
cd faraday
make && make install
```

([source](../../raw/docs/lightning-network-tools/faraday/get-started.md))

## Run Faraday

Faraday comes with two components: `faraday` itself and the command line interface `frcli`. ([source](../../raw/docs/lightning-network-tools/faraday/get-started.md))

To make full use of Faraday, connect it to your Bitcoin node, for example `bitcoind` or `btcd`:

```
faraday --connect_bitcoin --bitcoin.host=localhost:8332 --bitcoin.user=[the RPC username as defined in bitcoin.conf] --bitcoin.password=[the RPC password as defined in bitcoin.conf]
```

To run Faraday in the background, the output can be written to `/dev/null` by amending `&>/dev/null &` to the command. ([source](../../raw/docs/lightning-network-tools/faraday/get-started.md))

## Run inside Lightning Terminal

If Lightning Terminal is running, locally or remotely, Faraday is already running inside it. The port must then be specified every time `frcli` is run, using the flag `--rpcserver=localhost:8443`, for example `./frcli --rpcserver=localhost:8443 audit`. ([source](../../raw/docs/lightning-network-tools/faraday/get-started.md))

To avoid typing the flag or navigating to the binary each time, an entry can be added to the aliases file (e.g. `~/.bash_aliases`):

```
alias frcli=’~/path/to/lit/./frcli --rpcserver=localhost:8443’
```

You may have to manually move over your node's `tls.cert` to `~/.faraday/mainnet`. ([source](../../raw/docs/lightning-network-tools/faraday/get-started.md))

To use all of Faraday's features, Lightning Terminal is configured to connect to the Bitcoin node by amending these lines to `lit.conf`:

```
faraday.connect_bitcoin=1
faraday.bitcoin.host=[the ip or domain of our bitcoind node]:8332
faraday.bitcoin.user=[our bitcoind username, as specified in our bitcoin.conf]
faraday.bitcoin.password=[our bitcoind password, as specified in our bitcoin.conf]
```

([source](../../raw/docs/lightning-network-tools/faraday/get-started.md))

Typically bitcoind will not allow RPC connections from outside, although this can be configured with `rpcallowip=[IP of the machine you are running LiT on]`. If unsure about the security implications of opening up bitcoind's RPC calls, the guide suggests using faraday on the same machine as the bitcoin node. ([source](../../raw/docs/lightning-network-tools/faraday/get-started.md))

## Channel overview: frcli insights

`frcli insights` gives a list of all channels with detailed information about each. LND tracks the uptime of each channel since the last restart, so the output includes a calculated `uptime_ratio`. It also shows the age of the channel measured in blocks (confirmations), the total fees earned through the channel, and metrics for comparing channel activity. ([source](../../raw/docs/lightning-network-tools/faraday/the-faraday-cli.md))

The example output has the keys `chan_point`, `monitored_seconds`, `uptime_seconds`, `volume_incoming_msat`, `volume_outgoing_msat`, `fees_earned_msat`, `confirmations`, `uptime_ratio`, `revenue_per_conf_msat`, `volume_per_conf_msat`, `incoming_vol_per_conf_msat` and `outgoing_vol_per_conf_msat`. ([source](../../raw/docs/lightning-network-tools/faraday/the-faraday-cli.md))

## Revenue reports: frcli revenue

`frcli revenue` gives more detail. For each channel it returns pair reports, which show how many milli-satoshi (msat) were routed to and from each peer. Each report has a `target_channel` and a `pair_reports` map keyed by channel point, with `amount_outgoing_msat`, `fees_outgoing_msat`, `amount_incoming_msat` and `fees_incoming_msat`. ([source](../../raw/docs/lightning-network-tools/faraday/the-faraday-cli.md))

The guide says this information can be vital to deciding which channels to keep, which to rebalance and which to close, and can help identify bottlenecks such as channels that would route more payments if other channels were better balanced or had higher capacity. ([source](../../raw/docs/lightning-network-tools/faraday/the-faraday-cli.md))

The command can be narrowed to a specific channel (`--chan_points`) or to specific dates:

```
frcli --rpcserver=localhost:8443 revenue --chan_points=”b046a363855185962e0bd3b86beefa1480c6ac0d3f0c0b41f6eecf4acd6c0b1f:1” --start_time 1615680000 --end_time 1615766400
```

([source](../../raw/docs/lightning-network-tools/faraday/the-faraday-cli.md))

## Close recommendations by threshold: frcli threshold

Faraday can generate recommendations for channels that do not meet thresholds you set for their metrics. The thresholds for `frcli threshold` are:

| Flag | Meaning | Default |
| --- | --- | --- |
| `--uptime value` | Ratio of uptime to time monitored, expressed in [0;1]. | 0 |
| `--revenue value` | Threshold revenue (in msat) per confirmation beneath which channels will be identified for close. | 0 |
| `--incoming value` | Threshold incoming volume (in msat) per confirmation beneath which channels will be identified for close | 0 |
| `--outgoing value` | Threshold outgoing volume (in msat) per confirmation beneath which channels will be identified for close | 0 |
| `--volume value` | Threshold total volume (in msat) per confirmation beneath which channels will be identified for close | 0 |
| `--min_monitored value` | Amount of time in seconds a channel should be monitored for to be eligible for close | 2419200 |

([source](../../raw/docs/lightning-network-tools/faraday/the-faraday-cli.md))

## Close recommendations by outlier: frcli outliers

Faraday can also identify outliers, meaning channels that significantly underperform your average channel. The `--outlier_mult` flag sets the number of inter quartile ranges a channel should be from quartiles to be considered an outlier; the guide recommends values between 1.5 for aggressive recommendations and 3 for conservative ones. The recommendation is based on uptime, revenue or volume, using the same flags and defaults as `frcli threshold`. ([source](../../raw/docs/lightning-network-tools/faraday/the-faraday-cli.md))

```
frcli --rpcserver=localhost:8443 outliers --revenue --outlier_mult 2.5
```

([source](../../raw/docs/lightning-network-tools/faraday/the-faraday-cli.md))

## Closed channels: frcli closereport

First obtain the funding transaction IDs of closed channels from lnd with `lncli closedchannels`. Then request a report with `frcli closereport`, which requires a connection to your Bitcoin node and shows how the channel was closed and which fees were paid to close it. The guide gives two forms:

```
frcli closereport --funding_txid 4fc297d20fa41d62ccb2acecf2ed6cc0b1ce3c6f274c6cb661e0e97bb65a640f --output_index 1
frcli closereport 4fc297d20fa41d62ccb2acecf2ed6cc0b1ce3c6f274c6cb661e0e97bb65a640f 1
```

The example output has `channel_point`, `channel_initiator`, `close_type` (`"Cooperative"` in the example), `close_txid`, `open_fee` and `close_fee`. ([source](../../raw/docs/lightning-network-tools/faraday/the-faraday-cli.md))

## Full node report: frcli audit

`frcli audit` generates a full report of all activity on the node. It can be written to csv with the `--csv_path` flag, and it requires Faraday to be connected to your Bitcoin node. ([source](../../raw/docs/lightning-network-tools/faraday/the-faraday-cli.md))

The report can be narrowed with the `--start_time` and `--end_time` flags, expressed in unix time. [[loop]] and [[pool]] transactions can be identified in the output by including the flags `--loop-category` and `--pool-category`. For more granular insights a json array can be passed with the `--categories` flag. ([source](../../raw/docs/lightning-network-tools/faraday/the-faraday-cli.md))

## Fiat values: frcli fiat

`frcli fiat` converts milli-satoshi values into USD, including for historical values. The guide says the feature is also integrated into `frcli audit` when enabled with the `--enable_fiat` flag. ([source](../../raw/docs/lightning-network-tools/faraday/the-faraday-cli.md))

```
frcli --rpcserver=localhost:8443 fiat --amt_msat 21000000
```

([source](../../raw/docs/lightning-network-tools/faraday/the-faraday-cli.md))

## Conflicts

- Insights fields. The guide's example `frcli insights` output includes `uptime_ratio`, `revenue_per_conf_msat`, `volume_per_conf_msat`, `incoming_vol_per_conf_msat` and `outgoing_vol_per_conf_msat` and has no `private` key ([source](../../raw/docs/lightning-network-tools/faraday/the-faraday-cli.md)). The `frdrpc.ChannelInsight` message in the API reference has none of those five fields and does have `private` ([source](../../raw/api/api-docs/api/faraday/faraday-server/channel-insights.md)).
- Fiat in the audit. The guide says fiat conversion in `frcli audit` is enabled with `--enable_fiat` ([source](../../raw/docs/lightning-network-tools/faraday/the-faraday-cli.md)). The `frdrpc.NodeAuditRequest` message instead has a `disable_fiat` field, "Set to generate a report without conversion to fiat" ([source](../../raw/api/api-docs/api/faraday/faraday-server/node-audit.md)).
- Outlier flags. The guide says `frcli outliers` bases its recommendation on uptime, revenue or volume "using the same flags and defaults as above", that is, those of `frcli threshold` ([source](../../raw/docs/lightning-network-tools/faraday/the-faraday-cli.md)). The `frcli threshold --help` sample in the API reference lists `--incoming value` and `--outgoing value`, each with `(default: 0)` ([source](../../raw/api/api-docs/api/faraday/faraday-server/threshold-recommendations.md)), while the `frcli outliers --help` sample lists `--incoming_volume` and `--outgoing_volume`, and shows `--uptime`, `--revenue` and `--volume` without a value or default ([source](../../raw/api/api-docs/api/faraday/faraday-server/outlier-recommendations.md)).

## Notes

Synthesis, not from a single source: the first two items under Conflicts compare the CLI guide with the RPC reference, so they may reflect a difference between what `frcli` prints or accepts and what the RPC carries, or a guide that predates the referenced commit. The sources do not say which.
