---
title: Loop
type: component
sources:
  - raw/docs/lightning-network-tools/loop.md
  - raw/docs/lightning-network-tools/loop/get-started.md
  - raw/docs/lightning-network-tools/loop/the-loop-cli.md
  - raw/docs/lightning-network-tools/loop/peer-with-loop.md
  - raw/docs/lightning-network-tools/loop/static-loop-in-addresses.md
  - raw/docs/lightning-network-tools/loop/instant-loop-outs.md
  - raw/docs/lightning-network-tools/loop/autoloop.md
  - raw/api/api-docs/api/loop.md
  - raw/api/api-docs/api/loop/rest-endpoints.md
  - raw/api/api-docs/api/loop/swap-client/loop-out.md
  - raw/api/api-docs/api/loop/debug/force-auto-loop.md
updated: 2026-11-14
---

# Loop

Lightning Loop is a service that allows users to make a Lightning transaction to an onchain Bitcoin address (Loop Out), or send on-chain Bitcoin directly into a Lightning channel (Loop In). It can help manage channel [[liquidity]], for example by emptying out a channel and acquiring [[inbound-capacity]], or by refilling a depleted channel. ([source](../../raw/docs/lightning-network-tools/loop.md))

Loop uses [[submarine-swaps]] to transact non-custodially, meaning that Loop is trustless. Loop Out transactions are batched to save on transaction fees. Loop uses L402s for authentication (see [[l402]]). ([source](../../raw/docs/lightning-network-tools/loop.md))

The API reference describes Loop as a non-custodial service offered by Lightning Labs to bridge on-chain and off-chain Bitcoin using submarine swaps, and lists these situations in which it can be used: acquiring inbound channel liquidity from arbitrary nodes on the Lightning network; depositing funds to a Bitcoin on-chain address without closing active channels; paying to on-chain fallback addresses in the case of insufficient route liquidity; refilling depleted channels with funds from cold-wallets or exchange withdrawals; servicing off-chain Lightning withdrawals using on-chain payments, with no funds in channels required; and as a failsafe payment method when channel liquidity along a route is insufficient. ([source](../../raw/api/api-docs/api/loop.md))

## Loop In and Loop Out

| | Loop Out | Loop In |
| --- | --- | --- |
| Direction | Lightning transaction to an onchain Bitcoin address | on-chain Bitcoin into a Lightning channel |
| Liquidity effect | empties out a channel, acquiring inbound capacity | refills a depleted channel |

([source](../../raw/docs/lightning-network-tools/loop.md))

In a Loop Out, the Loop server makes an on-chain transaction to an HTLC smart contract (see [[htlc]]) first; once the Lightning payment to Loop has been made, the client sweeps the funds from the contract using the secret obtained in the payment. In a Loop In, the client makes the on-chain transaction, and the off-chain payment arrives in a channel once that transaction has one confirmation. Commands, fees and a worked example are on [[using-loop]]. ([source](../../raw/docs/lightning-network-tools/loop/the-loop-cli.md))

Two swap variants have their own pages. A static Loop In Address allows the user to deposit funds onchain at any time before initiating the Loop In, see [[static-loop-in-addresses]]. ([source](../../raw/docs/lightning-network-tools/loop/static-loop-in-addresses.md)) Instant Loop Out is a form of submarine swap that uses pre-committed onchain funds, a pre-configured reservation in the form of an onchain commitment, to make Loop Outs immediately available once the offchain payment has been settled, see [[instant-loop-outs]]. ([source](../../raw/docs/lightning-network-tools/loop/instant-loop-outs.md)) Loop Out and Loop In swaps can also be dispatched automatically, according to a set of rules configured for the node's channels, within a budget of your choosing, see [[autoloop]]. ([source](../../raw/docs/lightning-network-tools/loop/autoloop.md))

## Relationship to lnd and litd

To run Loop you need to be running LND, either from the binary releases or compiled from source with `make install tags="signrpc walletrpc chainrpc invoicesrpc"`. See [[lnd]] and [[running-lnd]]. ([source](../../raw/docs/lightning-network-tools/loop/get-started.md))

`loopd` may run on a separate machine and network from LND. In `loopd.conf` this is configured with `lnd.host=<ip>:10009`, `lnd.macaroonpath=/path/to/admin.macaroon` and `lnd.tlspath=/path/to/tls.cert`; the LND side may need `lnd.rpclisten=0.0.0.0:10009` and `tlsextraip=`. Details are on [[using-loop]]. ([source](../../raw/docs/lightning-network-tools/loop/get-started.md))

Loop comes bundled with Lightning Terminal (`litd`). If you are already running `litd`, you can access Loop through the command line or the Lightning Terminal UI and may skip the standalone installation. See [[lightning-terminal]] and [[running-litd]]. ([source](../../raw/docs/lightning-network-tools/loop/get-started.md))

## Install and run

Loop can be run directly from the binary releases at `https://github.com/lightninglabs/loop/releases`, or compiled from source, which requires Golang: `git clone https://github.com/lightninglabs/loop.git`, `cd loop`, `make && make install`. ([source](../../raw/docs/lightning-network-tools/loop/get-started.md))

By default, the `loopd.conf` is placed in `~/.loop/mainnet/`. When starting `loopd` on another network (e.g. `loopd --network=signet`), the configuration file is expected in the relevant directory (e.g. `~/.loop/signet`). A custom directory may be passed with the `--configfile=` flag. ([source](../../raw/docs/lightning-network-tools/loop/get-started.md))

## The loop CLI

As soon as Loop is running, the CLI is available, either by typing `loop` or by navigating to where the binaries are stored and executing `./loop`. Commands named in the guide include `loop terms`, `loop getparams`, `loop quote in`, `loop quote out`, `loop in`, `loop out`, `loop monitor`, `loop setparams`, `loop listswaps` and `loop swapinfo <swap id>`. They are walked through on [[using-loop]]. ([source](../../raw/docs/lightning-network-tools/loop/the-loop-cli.md))

## API

The API reference documents the `loop` CLI and gRPC and REST access to a local `loopd` instance. Its code samples assume gRPC on port `11010` and REST on port `8081`, and a request needs a TLS/SSL connection and a macaroon (see [[macaroons]]). The reference was generated against commit `9158aed2a8347d78585faa2e7a89a08f66692a09`. ([source](../../raw/api/api-docs/api/loop.md))

The gRPC documentation was generated from two proto files, `looprpc/client.proto` and `looprpc/debug.proto`. ([source](../../raw/api/api-docs/api/loop.md)) The RPC pages of [[loop-swap-client]] give `looprpc/client.proto` as their source, for example LoopOut. ([source](../../raw/api/api-docs/api/loop/swap-client/loop-out.md)) ForceAutoLoop, the RPC of [[loop-debug]], gives `looprpc/debug.proto` as its source. ([source](../../raw/api/api-docs/api/loop/debug/force-auto-loop.md))

All REST paths start with `/v1/`, for example `/v1/loop/out`, `/v1/loop/in`, `/v1/loop/swaps` and `/v1/liquidity/params`; the full list is on [[loop-swap-client]]. ([source](../../raw/api/api-docs/api/loop/rest-endpoints.md))

## Peering with the Loop node

The Loop Lightning Network node is publicly reachable and accepts incoming channels, and routing node operators can earn routing fees by routing Loop Out payments to it. Requirements and node addresses are on [[using-loop]]; see also [[routing-nodes]]. ([source](../../raw/docs/lightning-network-tools/loop/peer-with-loop.md))

## Pages in this section

- [[using-loop]]: getting started, Loop Out and Loop In with the CLI, peering with Loop
- [[autoloop]]: automatic dispatch of swaps by rules and budget
- [[static-loop-in-addresses]]: static Loop In addresses
- [[instant-loop-outs]]: Instant Loop Outs and reservations
- [[loop-swap-client]]: the swap-client gRPC service
- [[loop-debug]]: the debug gRPC service
