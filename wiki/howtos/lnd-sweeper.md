---
title: The lnd sweeper and unconfirmed transactions
type: howto
sources:
  - raw/docs/lightning-network-tools/lnd/sweeper.md
  - raw/docs/lightning-network-tools/lnd/unconfirmed-bitcoin-transactions.md
updated: 2026-11-14
---

# The lnd sweeper and unconfirmed transactions

The Sweeper is an [[lnd]] subservice that handles funds sent from dispute resolution contracts to the internal wallet, and it underwent major adjustments in LND 0.18. The companion guide covers bumping fees of unconfirmed on-chain transactions with RBF and CPFP ([source](../../raw/docs/lightning-network-tools/lnd/sweeper.md), [source](../../raw/docs/lightning-network-tools/lnd/unconfirmed-bitcoin-transactions.md)).

## How the sweeper works

When channels are unilaterally closed, funds go into contracts that specify who can settle them, when and under what conditions; incoming and outgoing HTLCs also have to be swept. Some sweeps are time-sensitive, some are for convenience, and anchor sweeps bump the fee of the parent transaction ([source](../../raw/docs/lightning-network-tools/lnd/sweeper.md)).

Each sweep has a budget and a deadline. The budget can be set in the configuration file or passed per case through the RPC. Inputs with the same deadline are batched into a single sweeping transaction. While pending, the sweeper may bump with RBF until confirmed or the budget is exhausted; the Bumper raises the fee rate slightly every block, though RBF rules mean not every bump is published ([source](../../raw/docs/lightning-network-tools/lnd/sweeper.md)).

## Fee calculation

The fee function uses `(ending_fee_rate - starting_fee_rate) / deadline`. The starting fee comes from the backend estimate (`estimatesmartfee` in `bitcoind`, `estimatefee` in `btcd`, `feeurl`, or `--sat_per_vbyte`). The ending fee is the budget divided by the sweep transaction size, capped at `--sweeper.maxfeerate`, and can be overridden with `--budget` in `lncli wallet bumpfee` ([source](../../raw/docs/lightning-network-tools/lnd/sweeper.md)).

Worked example: deadline 1000 blocks, budget 200,000 sats, 500 vbytes. Starting fee rate 10 sat/vB (`estimatesmartfee 1000`), ending fee rate 400 sat/vB (`200,000/500`), fee rate delta 390 sat/kvB (`(400 - 10) / 1000 * 1000`) ([source](../../raw/docs/lightning-network-tools/lnd/sweeper.md)).

## Force close outputs and budgets

| Output | Deadline | Budget options |
|---|---|---|
| `to_local` (no time pressure) | default 1008 blocks, set with `--sweeper.nodeadlineconftarget` | `--sweeper.budget.tolocal` (sats) or `--sweeper.budget.tolocalratio` |
| Time-sensitive HTLCs | from CLTV | default 50% of HTLC value; `--sweeper.budget.deadlinehtlc`, `--sweeper.budget.deadlinehtlcratio` |
| Non-time-sensitive HTLCs | none | `--sweeper.budget.nodeadlinehtlc`, `--sweeper.budget.nodeadlinehtlcratio` |
| Anchor (CPFP) | closest HTLC deadline | default 50% of "value under protection"; `--sweeper.budget.anchorcpfp` (sats) or `--sweeper.budget.anchorcpfpratio` |

([source](../../raw/docs/lightning-network-tools/lnd/sweeper.md))

On a local force close, HTLCs are spent in two stages: first via pre-signed HTLC success/timeout transactions, then from those transactions. Stage-one incoming HTLCs take their deadline from their CLTV timeout path; stage-one outgoing HTLCs from the corresponding incoming HTLC's CLTV; stage-two outputs have no deadline. On a remote force close, HTLCs are spent directly from the commitment transaction and are all time-sensitive ([source](../../raw/docs/lightning-network-tools/lnd/sweeper.md)).

Anchors without HTLCs on the force close are generally uneconomical and ignored. With time-sensitive HTLCs, the anchor is swept to CPFP the close. The anchor itself (330 sats) is too small for a ratio budget, so the budget comes from "value under protection", the sum of HTLC outputs minus their budgets. Use `--immediate` on `lncli wallet bumpfee` or `lncli wallet bumpclosefee` to sweep an anchor as quickly as possible ([source](../../raw/docs/lightning-network-tools/lnd/sweeper.md)).

## Managing sweeps by hand

Sweeps are identified by outpoint (`txid:output`). List pending sweeps with `lncli wallet pendingsweeps`; `lncli pendingchannels` shows HTLCs and `to_local` outputs ([source](../../raw/docs/lightning-network-tools/lnd/sweeper.md)).

```
# slow down (budget is total fees, not a fee rate; ~135 vB for one-in-one-out)
lncli wallet bumpfee --conf_target=10000 --budget=3000 <outpoint>

# speed up and publish now
lncli wallet bumpfee --conf_target=10 --budget=21000 <outpoint> --immediate

# consolidate: same conf_target for each outpoint, within the same block
lncli wallet bumpfee --conf_target=10 --budget=700 <outpoint 1>
lncli wallet bumpfee --conf_target=10 --budget=700 <outpoint 2>
lncli wallet bumpfee --conf_target=10 --budget=700 <outpoint 3>
```

For consolidation, `--budget` is still per UTXO; as a rule of thumb allow 120vB for the output and about 70vB per swept outpoint. After the next block LND creates one transaction sweeping all outpoints into a single UTXO ([source](../../raw/docs/lightning-network-tools/lnd/sweeper.md)).

## Unconfirmed on-chain transactions

Channel openings need to be confirmed within two weeks of initiation, otherwise the peer may disregard the channel and you will have to force close to recover funds ([source](../../raw/docs/lightning-network-tools/lnd/unconfirmed-bitcoin-transactions.md)).

**Outgoing (RBF).** Find unconfirmed transactions with `lncli listchaintxns --start_height <current height> --end_height -1`, then bump with `lncli wallet bumpfee`. The outpoint given is an input of the transaction you want confirmed, not the transaction itself. `--force` includes an input even if sweeping it costs more than it is worth ([source](../../raw/docs/lightning-network-tools/lnd/unconfirmed-bitcoin-transactions.md)):

```
lncli listchaintxns --start_height 818181 --end_height -1
lncli wallet bumpfee --conf_target 6 --force 38a64ad629960b0100e6954801a035c484df64f6efa783c33508054d8f2cfe95:0
```

**Incoming (CPFP).** Use `lncli wallet bumpfee` on the unconfirmed incoming transaction's output that belongs to your wallet. Alternatively send to a new address (`lncli newaddress p2wkh`) with `lncli sendcoins --min_confs 0`, e.g. `lncli sendcoins --addr bc1q8wymjatcv5xpfm4uav2pwtw534t4u0tfup2xgg --min_confs 0 --amt 2000000 --sat_per_vbyte 40`, or open a channel directly with `lncli openchannel --psbt` ([source](../../raw/docs/lightning-network-tools/lnd/unconfirmed-bitcoin-transactions.md)).

**Channel opens (CPFP on change).** The funding transaction cannot be RBF-bumped. Find the `channel_point` with `lncli pendingchannels`; the change output has the same txid and the other index (`0` or `1`). Without a change output, CPFP is impossible. With `--sat_per_byte` or `--sat_per_vbyte` (instead of `--conf_target`), LND sets the child fee so parent and child together hit that rate. Example: `lncli wallet bumpfee --sat_per_vbyte 40 5f97234af4df23881ca5e994bf42956c9af53bf83cb63687d1d0adfcd3ece18a:0`. There is no way to speed up a channel opened to your node. If you get `the passed output does not belong to the wallet`, restart LND or retrieve the transaction with `lncli listchaintxns` ([source](../../raw/docs/lightning-network-tools/lnd/unconfirmed-bitcoin-transactions.md)).

**Channel closes.** For cooperative closes, CPFP your own closing output with `lncli wallet bumpfee`. For force closes of anchor channels, use `lncli wallet bumpclosefee` with the channel point; from 0.18 the bump is queued for the next batch unless `--immediate` is given, and `--budget` and `--conf_target` override budget and deadline. From LND 0.19, cooperative closes can be RBF-bumped if both peers set `protocol.rbf-coop-close=true` (only for channels opened after the flag was applied): rerun `lncli closechannel` with a higher fee or lower confirmation target. The closing party pays, and whoever initiates a bump pays the full fee. This is incompatible with simple taproot channels ([source](../../raw/docs/lightning-network-tools/lnd/unconfirmed-bitcoin-transactions.md)).

## Rebroadcasting

Restarting LND rebroadcasts all unconfirmed transactions. Retrieve wallet transactions with `lncli listchaintxns --end_height -1` and republish the `raw_tx_hex` with `bitcoin-cli sendrawtransaction "hexstring"`; for force closes and some sweeps try `bitcoin-cli getrawtransaction "txid"`. If needed, raise `maxmempool` in `bitcoin.conf`; `maxmempool=600` doubles the default ([source](../../raw/docs/lightning-network-tools/lnd/unconfirmed-bitcoin-transactions.md)).

Out-of-band acceleration services exist, but there is often no way to prove the provider can actually get the transaction mined ([source](../../raw/docs/lightning-network-tools/lnd/unconfirmed-bitcoin-transactions.md)).

See also: [[sweeping]], [[lnd-wallet-kit]], [[lnd-wallet-and-psbt]], [[lnd-routing-node-operations]], [[lnd-recovery]], [[payment-channels]].
