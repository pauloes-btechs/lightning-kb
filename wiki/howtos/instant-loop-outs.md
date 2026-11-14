---
title: Instant Loop Outs
type: howto
sources:
  - raw/docs/lightning-network-tools/loop/instant-loop-outs.md
  - raw/api/api-docs/api/loop/swap-client/list-reservations.md
  - raw/api/api-docs/api/loop/swap-client/instant-out.md
  - raw/api/api-docs/api/loop/swap-client/instant-out-quote.md
  - raw/api/api-docs/api/loop/swap-client/list-instant-outs.md
  - raw/api/api-docs/api/loop/swap-client/fetch-l402-token.md
  - raw/api/api-docs/api/loop/swap-client/loop-out.md
updated: 2026-11-14
---

# Instant Loop Outs

Instant Loop Out is a form of submarine swap that uses pre-committed on-chain funds to make Loop Outs immediately available once the off-chain payment has been settled (see [[submarine-swaps]]). It is a feature of [[loop]] available from `version 0.28`; the regular Loop Out is on [[using-loop]]. ([source](../../raw/docs/lightning-network-tools/loop/instant-loop-outs.md))

It lets users swap off-chain to on-chain funds immediately, without waiting for on-chain confirmations, through a pre-configured reservation in the form of an on-chain commitment. The funds can then be sent to any other on-chain address within a set number of blocks of the creation of the reservation; funds not sent out in that time frame are swept into the LND node's internal wallet. The guide says these optimizations allow for better fee estimations, expression of time preference, and liquidity management (see [[liquidity]]). ([source](../../raw/docs/lightning-network-tools/loop/instant-loop-outs.md))

## Availability and setup

Select users are able to use Instant Loop Outs. The service will be rolled out slowly and requires some manual intervention on both the server and client side. ([source](../../raw/docs/lightning-network-tools/loop/instant-loop-outs.md))

Configuration: run `loopd version 0.28` and add `experimental=true` to the `loopd.conf` file under `~/.loop/mainnet`, or start Loop with the `--experimental` flag. ([source](../../raw/docs/lightning-network-tools/loop/instant-loop-outs.md))

To be invited, reach out to `support@lightning.engineering` and be prepared to share your L402, which the guide says can be obtained from `loop listauth` (the `id`) or in the Lightning Terminal dropdown menu. For now, reservations are done manually upon request and are valid for 1000 blocks. See [[l402]] and [[lightning-terminal]]. ([source](../../raw/docs/lightning-network-tools/loop/instant-loop-outs.md))

## Inspect reservations

Once a reservation is made, it can be inspected with `loop reservations list`. Each entry has `reservation_id`, `state` (`Confirmed` in the guide's example), `amount`, `tx_id`, `vout` and `expiry`. The `expiry` shows the block height at which the reservation can be swept back by the Loop service; the Loop Out should be completed before this block height. ([source](../../raw/docs/lightning-network-tools/loop/instant-loop-outs.md))

## Perform an Instant Loop Out

As of now, Instant Loop Outs can only be completed with the full amount of the reservation. Run `loop instantout`; it shows the available reservations and lets you select one or multiple (for example `1,2,3`, or `ALL`). ([source](../../raw/docs/lightning-network-tools/loop/instant-loop-outs.md))

In the guide's example, one reservation of 250000 is selected, the CLI shows `Estimated on-chain fee: 112 sat` and `Service fee: 500 sat`, asks `CONTINUE SWAP? (y/n)`, and then reports the swap ID, the state `WaitForSweeplessSweepConfirmed` and a "Sweepless sweep tx id". ([source](../../raw/docs/lightning-network-tools/loop/instant-loop-outs.md))

`loop listinstantouts` lists completed swaps: each entry of `swaps` has `swap_hash`, `state` (`FinishedSweeplessSweep` in the example), `amount`, `reservation_ids` and `sweep_tx_id`. ([source](../../raw/docs/lightning-network-tools/loop/instant-loop-outs.md))

When Loop runs as part of `litd`, the guide points to the Lightning Terminal command line interface documentation for how to invoke the CLI (see [[running-litd]]). ([source](../../raw/docs/lightning-network-tools/loop/instant-loop-outs.md))

## RPCs

All of these are on [[loop-swap-client]].

| RPC | REST | Purpose |
| --- | --- | --- |
| ListReservations | `GET` `/v1/instantout/reservations` | returns a list of all reservations the server opened to us |
| InstantOutQuote | `POST` `/v1/instantout/quote` | returns a quote for an instant out swap with the provided parameters |
| InstantOut | `POST` `/v1/instantout` | initiates an instant out swap with the given parameters |
| ListInstantOuts | `GET` `/v1/instantout/swaps` | returns a list of all currently known instant out swaps and their current status |

Sources, in table order: ([source](../../raw/api/api-docs/api/loop/swap-client/list-reservations.md)) ([source](../../raw/api/api-docs/api/loop/swap-client/instant-out-quote.md)) ([source](../../raw/api/api-docs/api/loop/swap-client/instant-out.md)) ([source](../../raw/api/api-docs/api/loop/swap-client/list-instant-outs.md))

`InstantOutRequest` takes `reservation_ids`, `outgoing_chan_set`, `dest_addr` (optional; if not set, the funds are swept to the wallet's internal address) and `max_swap_fee_sat`, which must be set; an explicitly set value of zero rejects any positive swap fee. The response has `instant_out_hash`, `sweep_tx_id` and `state`. ([source](../../raw/api/api-docs/api/loop/swap-client/instant-out.md))

`InstantOutQuoteResponse` has `service_fee_sat`, the fee the swap service is charging, and `sweep_fee_sat`, the estimated on-chain fee that needs to be paid to publish the Sweepless Sweep. ([source](../../raw/api/api-docs/api/loop/swap-client/instant-out-quote.md))

FetchL402Token fetches an L402 token from the server, which is required in order to receive reservation notifications from the server. ([source](../../raw/api/api-docs/api/loop/swap-client/fetch-l402-token.md))

The regular LoopOut RPC also has a `reservation_ids` field: if it is set, loop will try to use the instant out flow using the given reservations; if the reservations are not sufficient the swap will fail, and the swap amount must be equal to the sum of the amounts of the reservations. ([source](../../raw/api/api-docs/api/loop/swap-client/loop-out.md))

## Notes

Synthesis: the guide writes the invitation step as "obtain under id under loop listauth"; this page reads that as the `id` shown by `loop listauth`. The API reference describes `loop listauth` as a client of the deprecated GetLsatTokens RPC, whose token message has an `id` field (see [[loop-swap-client]]).
