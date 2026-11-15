---
title: 'Sending with lnd: payments, AMP, keysend, probing'
type: howto
sources:
  - raw/docs/lightning-network-tools/lnd/payments.md
  - raw/docs/lightning-network-tools/lnd/amp.md
  - raw/docs/lightning-network-tools/lnd/send-messages-with-keysend.md
  - raw/docs/lightning-network-tools/lnd/probing-with-estimateroutefee.md
  - raw/docs/lightning-network-tools/lnd/pathfinding.md
  - raw/docs/lightning-network-tools/lnd/lnd.conf.md
updated: 2026-11-14
---

# Sending with lnd: payments, AMP, keysend, probing

How [[lnd]] finds routes and sends payments, how to tune pathfinding and mission control, how to send AMP and keysend payments (with messages), and how to estimate fees with probes. The RPCs mentioned are on [[lnd-router]] and [[lnd-lightning]]; background is on [[pathfinding]] and [[multipath-payments]].

## Routes and pathfinding

Payments travel over a route of one or more channels. They are source-routed to protect sender privacy, so the sending node finds the route, using a modified version of Dijkstra's algorithm optimising for low fees and timelock. Channel balances are not disclosed to the network, and the guide calls this lack of knowledge the primary reason payments fail: a channel may have the capacity but not the balance in the needed direction. ([source](../../raw/docs/lightning-network-tools/lnd/payments.md))

LND prioritises routes with a good tradeoff between success probability and low fees. Mission control (mc) is the core of pathfinding: it stores past successes and failures per node pair (timestamp and amount of the last success or failure) and holds the configuration. Inspect it with `lncli getmccfg` and `lncli querymc`. ([source](../../raw/docs/lightning-network-tools/lnd/pathfinding.md))

The tradeoff is expressed as a cost, considering only the most recent payment for the probability metric:

`Cost = base_fee + fee_rate * amt + (attemptcost + attemptcostppm * amt) / P`

Higher attempt costs favour routes known to succeed; setting them to zero optimises only for the cheapest fees. Defaults: `routerrpc.attemptcost=100`, `routerrpc.attemptcostppm=1000`. ([source](../../raw/docs/lightning-network-tools/lnd/pathfinding.md))

**A priori estimator.** The original metric. Each hop starts at a 60% success likelihood (adjustable with `routerrpc.apriori.hopprob`); after a success, smaller payments are expected to succeed with 95%; after a failure, larger payments are considered impossible through that hop. Failure probabilities converge back to 60% over time, and previous attempts also feed a reputational score per node. ([source](../../raw/docs/lightning-network-tools/lnd/pathfinding.md))

**Bimodal estimator.** Experimental, available from LND 0.16. It assumes most channels are skewed to one side. Without usable history it gives small payments (relative to a configurable scale) a high chance, medium payments about 50%, and payments near capacity low to zero. After a failure, future payments are expected to fail unless very small; after a success, payments are expected to succeed unless they exceed capacity. In practice bimodal payments are expected to be more likely to succeed but at higher fees. ([source](../../raw/docs/lightning-network-tools/lnd/pathfinding.md))

Select the estimator with `routerrpc.estimator=[apriori|bimodal]` in `lnd.conf`, `routerrpc.MissionControlConfig.ProbabilityModel` over RPC, or `lncli setmccfg --estimator apriori` / `lncli setmccfg --estimator bimodal`. ([source](../../raw/docs/lightning-network-tools/lnd/pathfinding.md))

Mission control parameters described in the Sending Payments guide: `routerrpc.minrtprob` (required route success probability, default 0.01 / 1%; no attempt is made if no route reaches it), the a priori hop probability (default 0.6), the a priori weight (in [0;1], default 0.5; 1 ignores history, 0 uses only history) and the penalty half life (time for a hop to recover to 50%, default 1 hour). ([source](../../raw/docs/lightning-network-tools/lnd/payments.md))

## Prepay probes

For best results the guide recommends a prepay probe: send a payment with the same amount and a strongly-random payment hash. If it reaches the destination it fails with `FAILURE_REASON_INCORRECT_PAYMENT_DETAILS`; any other error means the real payment is unlikely to succeed. Probes update mission control, give accurate fee information and reduce the likelihood of stuck payments. Downsides: they may limit the use of multi-part payments, and forwarding nodes are not compensated. ([source](../../raw/docs/lightning-network-tools/lnd/payments.md))

## Probing with EstimateRouteFee

EstimateRouteFee sends an HTLC with a random payment hash that the destination can never settle; an `INCORRECT_PAYMENT_DETAILS` error indicates a successful probe, and the probed fee and timelock become the estimate. Nodes with public channels need only a destination public key and amount; nodes with private channels need a BOLT 11 invoice: ([source](../../raw/docs/lightning-network-tools/lnd/probing-with-estimateroutefee.md))

```
lncli estimateroutefee --dest <pubkey> --amt 50000
lncli estimateroutefee --pay_req lnbc500u1p... --timeout 30s
```

The response has `routing_fee_msat`, `time_lock_delay` and `failure_reason`. If `failure_reason` is anything other than `FAILURE_REASON_NONE`, no usable route was found and the fee fields are zero. `--timeout` defaults to 60 seconds; the guide suggests 15–30 seconds for interactive UIs. Cancelling the RPC call does not cancel the probe, and `routing_fee_msat` is a lower bound. Common codes: `FAILURE_REASON_NONE`, `FAILURE_REASON_NO_ROUTE`, `FAILURE_REASON_TIMEOUT`, `FAILURE_REASON_INSUFFICIENT_BALANCE`. ([source](../../raw/docs/lightning-network-tools/lnd/probing-with-estimateroutefee.md))

EstimateRouteFee needs only the `offchain:read` macaroon permission, because its HTLCs cannot settle. Bake a probing macaroon with `lncli bakemacaroon offchain:read` (see [[lnd-macaroons]]). The config option `routerrpc.fee-estimation-timeout=1m` caps how long probing fee estimation may take. ([source](../../raw/docs/lightning-network-tools/lnd/probing-with-estimateroutefee.md)) ([source](../../raw/docs/lightning-network-tools/lnd/lnd.conf.md))

## Dispatching payments

*SendPaymentV2* finds a route and dispatches the payment; *QueryRoutes* plus *SendToRouteV2* do it manually, which the guide recommends only for advanced users. Useful SendPaymentV2 parameters: `timeout_seconds` (maximum time spent trying to dispatch, not total settlement time), `max_parts` (default 1; above 1 makes it a Multi-Part-Payment), `outgoing_chan_ids` (restrict which of your channels are used) and `fee_limit_msat`. ([source](../../raw/docs/lightning-network-tools/lnd/payments.md))

Fees are paid per hop on multi-hop payments; policies have a base fee per forwarded HTLC and a fee rate on the amount. MPP helps around capacity bottlenecks but pays more base fees. See [[lnd-channel-fees]]. ([source](../../raw/docs/lightning-network-tools/lnd/payments.md))

**Invoice vs keysend.** An invoice must be obtained from the destination, is BOLT 11 and accepted by all implementations, and the recipient sets the preimage, giving proof of payment. Keysend needs no interaction, requires Feature Bit 9 (TLV Onion) at the destination, and the sender sets the preimage, so there is no proof of payment. Keysend needs `amt_msat` and `dest`. ([source](../../raw/docs/lightning-network-tools/lnd/payments.md))

## Monitoring payments

A payment is first locked in as HTLCs along the route, then settled with the preimage. Failure in the first stage (offline node, insufficient balance) is safe to retry. Once HTLCs are locked in, the payment must resolve; if the receiver never releases the preimage or a hop goes offline, it resolves only on timeout (a "stuck payment") and cannot be retried. *TrackPaymentV2* streams the payment state (In Flight, Succeeded, Failed) and terminates when the state is final, so it doubles as a lookup. ([source](../../raw/docs/lightning-network-tools/lnd/payments.md))

## Atomic Multi-path Payments (AMP)

AMP was implemented in lnd v0.13.0-beta and only sender and receiver need to support it. Unlike MPP, where all shards share one payment hash and can be partially settled, AMP shards each carry their own hash and the payment settles in full or not at all. The sender creates a preimage and adds random values per shard; the receiver recovers it by XOR only once all HTLCs are locked in. AMP needs only the recipient's node ID, requires TLV Onion, and allows static, reusable invoices (for example subscriptions or donation QR codes). ([source](../../raw/docs/lightning-network-tools/lnd/amp.md))

To receive spontaneous AMPs, set `accept-amp=1` in `lnd.conf` (payments to AMP invoices are accepted regardless of `accept-amp`, per the sample config). ([source](../../raw/docs/lightning-network-tools/lnd/amp.md)) ([source](../../raw/docs/lightning-network-tools/lnd/lnd.conf.md))

Commands from the guide:

```
lncli sendpayment --amt <amount in satoshis> --dest <public key of receiver> --amp
lncli addinvoice --amt <amount in satoshis> --memo='my first amp' --amp
lncli payinvoice --pay_req <the amp invoice created by the receiver>
lncli payinvoice --pay_req <the amp invoice created by the receiver> --pay_addr <the sha256 hash of a random number>
lncli payinvoice --pay_req <the amp invoice created by the receiver> --amp-reuse
```

An AMP invoice matters for private nodes because it carries channel hints that `lncli sendpayment` cannot express. Static AMP invoices are paid repeatedly by switching the payment address, which `--pay_addr` sets manually; from `lnd 0.14.0` `--amp-reuse` is no longer needed. If an AMP invoice has no amount, pay with `lncli payinvoice <amp invoice>` and `--amt`. ([source](../../raw/docs/lightning-network-tools/lnd/amp.md))

To move from keysend to AMP, replace the keysend flag with `--amp` (`lncli sendpayment --dest <destination public key> --amt <amount> --amp`); over RPC, set the amp field and stop generating a preimage. ([source](../../raw/docs/lightning-network-tools/lnd/amp.md))

## Keysend and messages

Keysend sends directly to a public key, as long as the node has public channels and keysend enabled; no invoice is needed. LND implements it as `--keysend` and the newer `--amp`. To receive, add `accept-amp=true` and `accept-keysend=true` to `lnd.conf` and restart (`lncli stop`, then `lnd`). A node with only private channels can instead hand out an AMP invoice with routing hints (`lncli addinvoice --amp` with `--private`, optionally `--amt`, `--expiry`, `--memo`). ([source](../../raw/docs/lightning-network-tools/lnd/send-messages-with-keysend.md))

```
lncli sendpayment --dest <destination public key> --amt <amount> --keysend
lncli sendpayment --dest <destination public key> --amt <amount> --amp
```

The guide recommends the AMP form. ([source](../../raw/docs/lightning-network-tools/lnd/send-messages-with-keysend.md))

**Messages.** Attach data with `--data` in the form `<record_id>=<hex_value>,<record_id>=<hex_value>,..`. Messages typically use record ID `34349334`. The guide's example sends a hex-encoded message with 10 satoshis: `lncli sendpayment --dest <pubkey> --amt 10 --data 34349334=<hex> --keysend`; `--data` can also be added to `lncli payinvoice <invoice>` for AMP invoices. Over RPC (the guide's REST example posts to `v1/channels/transactions`), generate a random 32 byte preimage yourself and send it in custom record `5482373484` alongside its hash as `payment_hash`, using `dest_custom_records`. ([source](../../raw/docs/lightning-network-tools/lnd/send-messages-with-keysend.md))

## Conflicts

- Mission control option names: the Sending Payments guide lists `routerrpc.apriorihopprob`, `routerrpc.aprioriweight` and `penaltyhalflife` ([source](../../raw/docs/lightning-network-tools/lnd/payments.md)), while the sample `lnd.conf` names them `routerrpc.apriori.hopprob`, `routerrpc.apriori.weight` and `routerrpc.apriori.penaltyhalflife` ([source](../../raw/docs/lightning-network-tools/lnd/lnd.conf.md)), as does the Pathfinding guide for `routerrpc.apriori.hopprob` ([source](../../raw/docs/lightning-network-tools/lnd/pathfinding.md)).
- Keysend flag name: the AMP guide says to "replace the `--key_send` flag with a `--amp` flag", but its own "old" command and the keysend guide use `--keysend` ([source](../../raw/docs/lightning-network-tools/lnd/amp.md), [source](../../raw/docs/lightning-network-tools/lnd/send-messages-with-keysend.md)).
- `--amp-reuse`: the AMP guide says it is no longer necessary from `lnd 0.14.0`, yet still lists `lncli payinvoice ... --amp-reuse` among its example commands ([source](../../raw/docs/lightning-network-tools/lnd/amp.md)).

See also: [[lnd-router]], [[lnd-lightning]], [[pathfinding]], [[multipath-payments]], [[lnd-receiving-payments]], [[lnd-channel-fees]], [[lnd-macaroons]], [[running-lnd]].
