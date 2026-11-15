---
title: 'Receiving with lnd: invoices and blinded paths'
type: howto
sources:
  - raw/docs/lightning-network-tools/lnd/receiving.md
  - raw/docs/lightning-network-tools/lnd/blinded-paths.md
  - raw/docs/lightning-network-tools/lnd/first-steps-with-lnd.md
  - raw/docs/lightning-network-tools/lnd/lnd.conf.md
updated: 2026-11-14
---

# Receiving with lnd: invoices and blinded paths

How an [[lnd]] node receives payments with invoices or keysend, how to monitor invoices, and how to hide the last hops to your node with blinded paths. The invoice RPCs are on [[lnd-lightning]] and [[lnd-invoices]]; invoice background is on [[lightning-invoices]].

## Invoice or keysend

| | Invoice | Keysend |
|---|---|---|
| Interaction with payer | Payer must request an invoice from your service | None required |
| Support | BOLT 11 invoices payable by all implementations | Sender must understand Feature Bit 9, TLV Onion; lnd must run with `--accept-keysend` |
| Proof of payment | Recipient sets preimage, cryptographically verifiable | Sender sets preimage, no proof |
| Control of receive flow | Invoices can only be paid once; a node without an invoice cannot pay you | Any node can send, which may cause unexpected receipts |

([source](../../raw/docs/lightning-network-tools/lnd/receiving.md))

Before receiving you need inbound capacity; see [[running-lnd]] and [[inbound-capacity]]. ([source](../../raw/docs/lightning-network-tools/lnd/first-steps-with-lnd.md))

## Creating invoices

*AddInvoice* adds an invoice and returns its *add_index* and a payment request, which encodes everything a sender needs and can be put in a QR code. Useful parameters: `value_msat` (amount in millisatoshis; underpayment fails), `expiry`, `private` (include routing hints for private channels; must be set if the node only has private channels or payments will not succeed) and `memo` (a string describing the invoice which, in the guide's words, "will be shared with the payee"; need not be unique). ([source](../../raw/docs/lightning-network-tools/lnd/receiving.md))

From the command line, `lncli addinvoice` creates an invoice; popular options are `--memo`, `--amt` (satoshis), `--expiry` (seconds, default 3600) and `--amp` for an AMP invoice that can be paid multiple times (see [[lnd-sending-payments]]). ([source](../../raw/docs/lightning-network-tools/lnd/first-steps-with-lnd.md))

Related `lnd.conf` options: `accept-keysend=false`, `accept-amp=false`, `gc-canceled-invoices-on-startup=false`, `gc-canceled-invoices-on-the-fly=false`, and `invoices.holdexpirydelta=12`, the number of blocks before expiry at which lnd cancels hold invoices with accepted HTLCs to avoid force closes. See [[lnd-configuration]]. ([source](../../raw/docs/lightning-network-tools/lnd/lnd.conf.md))

## Monitoring invoices

lnd keeps two monotonically increasing indexes: the add index (order invoices were added) and the settle index (order they were settled). *SubscribeInvoices* streams new and settled invoices and supports historical streams from an `add_index` or settle index, which helps resync a program after restart. *SubscribeSingleInvoice* follows one invoice by payment hash. *ListInvoices* polls invoices, paginated by *add_index*, and can be queried in reverse to list most recent first. ([source](../../raw/docs/lightning-network-tools/lnd/receiving.md))

## Blinded paths

Blinded paths let the invoice creator specify the last hops a payment must take, included in the invoice in encrypted form. They are available from LND 0.18.3. An invoice created with `--blind` uses a new dummy destination pubkey and typically contains three alternative paths of three hops each; only the first hop, the "introduction node", is revealed. The payer routes to the introduction node and appends the binary blobs from the invoice. ([source](../../raw/docs/lightning-network-tools/lnd/blinded-paths.md))

Example: `lncli addinvoice 100 --blind`. The decoded invoice lists `blinded_paths`, each with `introduction_node`, `blinding_point`, `blinded_hops` (`blinded_node`, `encrypted_data`) and the path's `base_fee_msat`, `proportional_fee_rate`, `total_cltv_delta`, `htlc_min_msat` and `htlc_max_msat`; the features include `route-blinding` (25) and `bolt-11-blinded-paths` (262). ([source](../../raw/docs/lightning-network-tools/lnd/blinded-paths.md))

Flags: `--min_real_blinded_hops` (number of real hops), `--num_blinded_hops` (hops per path), `--max_blinded_paths` (maximum paths) and `--blinded_path_omit_node` (exclude a node). ([source](../../raw/docs/lightning-network-tools/lnd/blinded-paths.md))

The matching config defaults are `routing.blinding.min-num-real-hops=1`, `routing.blinding.num-hops=2` (not counting your own node; shorter paths are padded with dummy hops) and `routing.blinding.max-num-paths=3`, plus `routing.blinding.policy-increase-multiplier=1.1` and `routing.blinding.policy-decrease-multiplier=0.9`, which add a buffer to path policy values against probing. `protocol.no-route-blinding` disables blinded route forwarding. ([source](../../raw/docs/lightning-network-tools/lnd/lnd.conf.md))

Caveats: blinded-path invoices can be too long for traditional QR codes (limit the number of paths to shrink them), and when only a few short paths exist they may not be payable and the recipient may still be identifiable, for example by correlating fees of real channels near the introduction node with the blinded path's fees. ([source](../../raw/docs/lightning-network-tools/lnd/blinded-paths.md))

See also: [[lnd-invoices]], [[lnd-lightning]], [[lightning-invoices]], [[lnd-sending-payments]], [[lnd-interceptors]], [[running-lnd]].
