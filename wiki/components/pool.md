---
title: Pool
type: component
sources:
  - raw/docs/lightning-network-tools/pool.md
  - raw/docs/lightning-network-tools/pool/overview.md
  - raw/docs/lightning-network-tools/pool/install.md
  - raw/docs/lightning-network-tools/pool/quickstart.md
  - raw/docs/lightning-network-tools/pool/first-steps.md
  - raw/docs/lightning-network-tools/pool/orders.md
  - raw/docs/lightning-network-tools/pool/batch_execution.md
  - raw/docs/lightning-network-tools/pool/zero-confirmation-channels.md
  - raw/docs/lightning-network-tools/pool/account_recovery.md
  - raw/docs/lightning-network-tools/pool/sidecar_channels.md
  - raw/docs/lightning-network-tools/pool/faq.md
  - raw/api/api-docs/api/pool.md
  - raw/docs/lightning-network-tools/pool/channel_leases.md
updated: 2026-11-14
---

# Pool

Lightning Pool is a non-custodial marketplace for Lightning Network channel [[liquidity]], launched in November 2020. It allows participants to earn interest for liquidity they provide or pay to acquire liquidity, without giving up control of their funds. ([source](../../raw/docs/lightning-network-tools/pool.md))

More precisely, Pool is a non-custodial batched uniform clearing-price auction for Lightning Channel Leases (LCL). An LCL packages up inbound (or outbound) channel liquidity as a fixed incoming asset, earning interest over time, with a maturity date expressed in blocks. The maturity date is enforced by Bitcoin contracts, so that the funds of the maker (the party that sold the channel) can't be swept until the maturity height. All cleared orders are cleared in a single batched on-chain transaction. ([source](../../raw/docs/lightning-network-tools/pool/overview.md))

## What it is for

Pool can be used to buy or sell liquidity on the Lightning Network, for yourself or on behalf of others. The guide lists these uses for node operators: bootstrap a routing node through balanced channels; acquire more [[inbound-capacity]] instantly through zero-confirmation channels; onboard a new user to Lightning with a mobile wallet through Sidecar channels; earn fees for deploying funds to the Lightning Network completely non-custodially. See also [[routing-nodes]]. ([source](../../raw/docs/lightning-network-tools/pool.md))

The overview gives a non-exhaustive list of use cases: bootstrapping new users with side car channels (a third party purchases a channel for a new user, including starting outbound liquidity); demand fueled routing node channel selection (a market demand signal for autopilot agents); bootstrapping new services to Lightning (a merchant pays a small percentage of the liquidity allocated towards it, committed for a set period of time); and allowing users to instantly receive with a wallet (a wallet provider pays only a percentage of the funds allocated to a new user instead of committing funds 1:1). See [[lightning-service-providers]] and [[merchant-liquidity]]. ([source](../../raw/docs/lightning-network-tools/pool/overview.md))

As a pricing example, the overview says a node could acquire 100 million satoshis (1000 units) for 100,000 satoshis, or 0.1%, and that prices are ultimately determined by the open market place. ([source](../../raw/docs/lightning-network-tools/pool/overview.md))

## Core ideas

- **Accounts.** Funds in a Pool account are held in a 2-of-2 multisignature account between your node and Pool. The account has an expiration time of 90 days, after which the account owner can close it unilaterally; while active it can be closed cooperatively at any time. At no point does Pool or Lightning Labs take possession or control of the funds. See [[pool-accounts]]. ([source](../../raw/docs/lightning-network-tools/pool.md))
- **Markets.** Pool offers markets for both inbound and outbound liquidity, each divided into multiple time frames so bidders and askers can express preferences for varying channel durations. See [[pool-orders-and-batches]]. ([source](../../raw/docs/lightning-network-tools/pool.md))
- **Auction batches.** All markets clear in batches, at most once per ten minutes. Each auction clears at a uniform price, and each batch is executed in a single on-chain transaction to save its participants on fees. See [[pool-orders-and-batches]]. ([source](../../raw/docs/lightning-network-tools/pool.md))
- **Channel leases.** A matched order results in a channel lease; see [[pool-channel-leases]]. ([source](../../raw/docs/lightning-network-tools/pool/quickstart.md))
- **Sidecar channels.** Channel lease bids on behalf of a third node, typically one without its own Pool account. See [[sidecar-channels]]. ([source](../../raw/docs/lightning-network-tools/pool.md))
- **Zero-confirmation channels.** Because all channels sold through Pool are co-signed by Pool from a 2-of-2 multisignature account, they cannot be maliciously double-spent by their initiator, which makes it safe to accept them without waiting for on-chain confirmations. See [[pool-zero-conf-channels]]. ([source](../../raw/docs/lightning-network-tools/pool.md))
- **Units.** Rather than buying or selling satoshis, the market uses units. A unit is 100,000 satoshis and is the smallest channel that can be bought or sold. ([source](../../raw/docs/lightning-network-tools/pool/orders.md))

## Requirements

To participate you need a Lightning node with at least one public channel, some outgoing capacity and on-chain bitcoin, and you need to run the pool daemon, either as a standalone binary or as part of litd. To earn fees for providing outbound liquidity through Pool, your node must be ranked, meaning it must pass all six health checks in Lightning Terminal. ([source](../../raw/docs/lightning-network-tools/pool.md))

The `lnd` node must have at least one active channel and must be able to pay a 1000 satoshi LSAT fee. The FAQ describes this as a one time payment required to obtain an LSAT token to communicate with the auction server; the token currently does not expire. ([source](../../raw/docs/lightning-network-tools/pool/quickstart.md), [source](../../raw/docs/lightning-network-tools/pool/faq.md))

## Relationship to other products

- **lnd.** Pool needs to be connected to an `lnd` node version `v0.11.1-beta` or later. If lnd is built from source it needs all sub-server build flags: `make install tags="signrpc walletrpc chainrpc invoicesrpc"`. Account funds are pulled from the `lnd` wallet. See [[lnd]] and [[running-lnd]]. ([source](../../raw/docs/lightning-network-tools/pool/install.md), [source](../../raw/docs/lightning-network-tools/pool/quickstart.md))
- **Chain backends.** The API reference says the Pool client depends on lnd, and that all of lnd's supported chain backends are fully supported when using the Pool client: Neutrino, Bitcoin Core, and btcd. ([source](../../raw/api/api-docs/api/pool.md))
- **litd.** Pool is included in the litd bundle and may already be installed and running on your node. With Lightning Terminal you run `litd` instead of `poold`. See [[lightning-terminal]] and [[running-litd]]. ([source](../../raw/docs/lightning-network-tools/pool.md), [source](../../raw/docs/lightning-network-tools/pool/quickstart.md))
- **Loop.** The install guide describes Pool as built very similarly to Lightning Loop: a constantly running background daemon plus a command line tool. See [[loop]]. ([source](../../raw/docs/lightning-network-tools/pool/install.md))
- **L402.** Pool uses L402s to authenticate its users. L402s are Macaroons that include a proof of payment. See [[l402]]. ([source](../../raw/docs/lightning-network-tools/pool.md))

## Install and run

Pool consists of the trader daemon, `poold`, and a command line tool to interact with it, called `pool`. `poold` can be run as a standalone binary connected to a compatible `lnd` node or integrated into Lightning Terminal (LiT). Binaries come from the GitHub releases page `https://github.com/lightninglabs/pool/releases`, or are built from source with `make install`. Full steps, remote-lnd flags and the configuration file are on [[pool-setup]]. ([source](../../raw/docs/lightning-network-tools/pool/install.md))

The gRPC and REST connections of `poold` are encrypted with TLS and secured with macaroon authentication the same way `lnd` is. Pool's macaroons are independent from `lnd`'s; the same macaroon cannot be used for both. See [[macaroons]]. ([source](../../raw/docs/lightning-network-tools/pool/install.md))

## The pool CLI

Commands that appear in the guide:

| Command | Purpose as the guide describes it | Page |
| --- | --- | --- |
| `pool accounts new` | create an account | [[pool-accounts]] |
| `pool accounts list` | view account details | [[pool-accounts]] |
| `pool accounts deposit` | add funds to an account | [[pool-accounts]] |
| `pool accounts withdraw` | withdraw from an account | [[pool-accounts]] |
| `pool accounts close` | close an account | [[pool-accounts]] |
| `pool accounts recover` | recover accounts after data loss with the help of the auctioneer ([source](../../raw/docs/lightning-network-tools/pool/account_recovery.md)) | [[pool-accounts]] |
| `pool orders submit ask` / `pool orders submit bid` | submit an order | [[pool-orders-and-batches]] |
| `pool orders list` | check submitted orders | [[pool-orders-and-batches]] |
| `pool orders cancel` | cancel an order by its nonce | [[pool-orders-and-batches]] |
| `pool auction leasedurations` | list the possible lease durations | [[pool-orders-and-batches]] |
| `pool auction fee` | query the current order execution fee | [[pool-orders-and-batches]] |
| `pool auction snapshot` | browse cleared batches | [[pool-orders-and-batches]] |
| `pool auction leases` | examine purchased/sold channel leases ([source](../../raw/docs/lightning-network-tools/pool/channel_leases.md)) | [[pool-channel-leases]] |
| `pool sidecar offer` | returns a sidecar ticket which can be passed on to the recipient of the channel ([source](../../raw/docs/lightning-network-tools/pool/zero-confirmation-channels.md)) | [[sidecar-channels]] |
| `pool sidecar register` | redeem a sidecar ticket ([source](../../raw/docs/lightning-network-tools/pool/zero-confirmation-channels.md)) | [[sidecar-channels]] |
| `pool sidecar expect-channel` | instruct the recipient's node to start expecting a channel ([source](../../raw/docs/lightning-network-tools/pool/sidecar_channels.md)) | [[sidecar-channels]] |

Rows without their own citation: ([source](../../raw/docs/lightning-network-tools/pool/first-steps.md), [source](../../raw/docs/lightning-network-tools/pool/orders.md), [source](../../raw/docs/lightning-network-tools/pool/batch_execution.md))

Depending on the setup, the CLI may need the location of the `tls.cert` and the RPC port to talk to the intended daemon. The guide's examples are `pool --rpcserver=localhost:8443 --tlscertpath ~/.lit/tls.cert` for litd and `pool --rpcserver=localhost:12010 --tlscertpath ~/.pool/mainnet/tls.cert` for poold. ([source](../../raw/docs/lightning-network-tools/pool/zero-confirmation-channels.md))

## API

The API reference documents the `pool` CLI and gRPC and REST access to a local `poold` instance. Its code samples assume gRPC on port `12010` and REST on port `8281`. The base directory of `poold` is by default `~/.pool` on Linux and `~/Library/Application Support/Pool` on macOS. A request needs a TLS/SSL connection and a macaroon used for RPC authentication. The reference was generated against commit `561c94bda9d5816e51205b5a7b15dce66520f39b`. ([source](../../raw/api/api-docs/api/pool.md))

The gRPC documentation is generated from three proto files, each with its own service page here: `poolrpc/trader.proto` ([[pool-trader]]), `auctioneerrpc/auctioneer.proto` ([[pool-channel-auctioneer]]) and `auctioneerrpc/hashmail.proto` ([[pool-hash-mail]]). ([source](../../raw/api/api-docs/api/pool.md))

## Fees at a glance

Buyers and sellers of channels should expect service charges of 5-25 basis points each, plus the one time 1000 satoshi LSAT payment. When the channel is opened, the cost of opening it is split between buyer and seller. The execution-fee and chain-fee formulas are on [[pool-orders-and-batches]]; see also [[channel-fees]] for routing fees in general. ([source](../../raw/docs/lightning-network-tools/pool/faq.md))

## Pages in this section

- [[pool-setup]]: Installing and starting Pool
- [[pool-accounts]]: Pool accounts and recovery
- [[pool-orders-and-batches]]: Pool orders and batch execution
- [[pool-channel-leases]]: Channel leases
- [[sidecar-channels]]: Sidecar channels
- [[pool-zero-conf-channels]]: Zero-confirmation channels in Pool
- [[pool-trader]]: pool trader service
- [[pool-channel-auctioneer]]: pool channel-auctioneer service
- [[pool-hash-mail]]: pool hash-mail service

## Conflicts

- **How often batches clear.** The Pool landing page says markets clear "at most once per ten minutes" ([source](../../raw/docs/lightning-network-tools/pool.md)); the batch execution page says Pool conducts a discrete batch auction "every 10 minutes" ([source](../../raw/docs/lightning-network-tools/pool/batch_execution.md)); the FAQ says batches are processed "whenever the market clears or approximately every 10 minutes or whichever is longer" ([source](../../raw/docs/lightning-network-tools/pool/faq.md)).
- **Sealed or public bids.** The landing page says a bid "can be set to public or remain sealed" ([source](../../raw/docs/lightning-network-tools/pool.md)); the batch execution page says orders are sealed-bid, meaning other traders are unable to see what others have bid ([source](../../raw/docs/lightning-network-tools/pool/batch_execution.md)).
- **Who is eligible to sell.** The landing page says a node must be ranked by passing all six health checks in Lightning Terminal ([source](../../raw/docs/lightning-network-tools/pool.md)); the FAQ says by default only well-connected nodes on the Bos Score List are eligible to sell liquidity ([source](../../raw/docs/lightning-network-tools/pool/faq.md)).
- **Buying for someone else.** The FAQ answers "Can I buy a channel for someone else?" with "Not at this time" ([source](../../raw/docs/lightning-network-tools/pool/faq.md)); the landing page describes sidecar channels as channel lease bids on behalf of a third node ([source](../../raw/docs/lightning-network-tools/pool.md)).
