---
title: Taproot Assets (tapd)
type: component
sources:
  - raw/docs/lightning-network-tools/taproot-assets.md
  - raw/api/api-docs/api/taproot-assets.md
  - raw/api/api-docs/api/taproot-assets/rest-endpoints.md
  - raw/api/api-docs/api/taproot-assets/taproot-assets/get-info.md
updated: 2026-11-14
---

# Taproot Assets (tapd)

The Taproot Assets Daemon `tapd` implements the Taproot Assets protocol (formerly Taro) for issuing assets on the Bitcoin blockchain. Taproot Assets leverages Taproot transactions to commit to newly created assets and their transfers in an efficient and scalable manner. Multiple assets can be created and transferred in a single bitcoin UTXO, while witness data is transacted and kept off-chain. See [[taproot-assets-protocol]] and [[taproot-assets-on-lightning]]. ([source](../../raw/docs/lightning-network-tools/taproot-assets.md))

## What it is for

The API reference lists these features of the daemon: mint assets; synchronize to universes; send and receive assets; export and import Taproot Asset proofs; create and manage CLI profiles. ([source](../../raw/api/api-docs/api/taproot-assets.md))

The Builder's Guide section on Taproot Assets is introduced as "Learn how to install Taproot Assets, mint and transfer assets" and has these sub-pages: Get Started, First Steps, Taproot Assets Channels, Asset Decimal Display, RFQ, Collectibles, Universes, Asset Loop, Debugging Tapd, Lightning Polar and Operational Safety Guidelines. ([source](../../raw/docs/lightning-network-tools/taproot-assets.md))

## Relationship to other products

- **lnd.** `tapd` is connected to an LND node: its `GetInfo` response reports `lnd_version`, `lnd_identity_pubkey` and `node_alias` of "the LND node that this daemon is connected to", and the block height and hash "as seen by the LND node". See [[lnd]] and [[tapd-taproot-assets]]. ([source](../../raw/api/api-docs/api/taproot-assets/taproot-assets/get-info.md))
- **Loop.** The guide section has a sub-page titled "Asset Loop". See [[loop]]. ([source](../../raw/docs/lightning-network-tools/taproot-assets.md))
## Install and run

Installation steps are not given on the pages this page draws on; the guide landing page points to its "Get Started" and "First Steps" sub-pages. See [[tapd-getting-started]]. ([source](../../raw/docs/lightning-network-tools/taproot-assets.md))

The base directory of a `tapd` instance is by default `~/.taproot-assets` on Linux and `~/Library/Application Support/TaprootAssets` on macOS. ([source](../../raw/api/api-docs/api/taproot-assets.md))

## CLI

The command line tool is `tapcli`; the API reference site features the documentation for `tapcli` (CLI) alongside the API documentation for Python and JavaScript clients. ([source](../../raw/api/api-docs/api/taproot-assets.md))

The `GetInfo` reference page includes a `tapcli getinfo --help` sample, which gives the usage `tapcli getinfo [arguments...]` and the description "Returns basic information related to the active daemon." See [[tapd-getting-started]] and [[tapd-taproot-assets]]. ([source](../../raw/api/api-docs/api/taproot-assets/taproot-assets/get-info.md))

## API

The reference's code samples assume a local `tapd` instance listening for gRPC connections on port `10029` and for REST connections on port `8089`. Two things are needed to make a gRPC or HTTP request to a `tapd` instance: a TLS/SSL connection and a macaroon used for RPC authentication. See [[macaroons]]. ([source](../../raw/api/api-docs/api/taproot-assets.md))

The gRPC documentation was generated from these `*.proto` files: `assetwalletrpc/assetwallet.proto`, `authmailboxrpc/mailbox.proto`, `mintrpc/mint.proto`, `portfoliopilotrpc/portfolio_pilot.proto`, `priceoraclerpc/price_oracle.proto`, `rfqrpc/rfq.proto`, `tapchannelrpc/tapchannel.proto`, `tapcommon.proto`, `tapdevrpc/tapdev.proto`, `taprootassets.proto` and `universerpc/universe.proto`. The documentation was generated automatically against commit `14aa3fd90e6aace4d3b2cfc72a51d15ce4afd891` of `lightninglabs/taproot-assets`. ([source](../../raw/api/api-docs/api/taproot-assets.md))

For REST, the `byte` field type must be set as the base64 encoded string representation of a raw byte array. When it is used in a URL path, the base64 string must be encoded using the URL and Filename Safe Alphabet: replace `+` with `-`, `/` with `_`, and keep the trailing `=` as is. Url encoding (ie. `%2F`) will not work. ([source](../../raw/api/api-docs/api/taproot-assets.md))

All paths in the REST endpoint listing start with `/v1/taproot-assets/`. The RPCs in the listing carry the package prefixes `taprpc`, `mintrpc`, `tapchannelrpc`, `authmailboxrpc`, `rfqrpc`, `universerpc` and `assetwalletrpc`. ([source](../../raw/api/api-docs/api/taproot-assets/rest-endpoints.md))

## Service pages

- [[tapd-taproot-assets]]: taproot-assets taproot-assets service
- [[tapd-asset-wallet]]: taproot-assets asset-wallet service
- [[tapd-mailbox]]: taproot-assets mailbox service
- [[tapd-mint]]: taproot-assets mint service
- [[tapd-portfolio-pilot]]: taproot-assets portfolio-pilot service
- [[tapd-price-oracle]]: taproot-assets price-oracle service
- [[tapd-rfq]]: taproot-assets rfq service
- [[tapd-tap-dev]]: taproot-assets tap-dev service
- [[tapd-taproot-asset-channels]]: taproot-assets taproot-asset-channels service
- [[tapd-universe]]: taproot-assets universe service

## How-to pages

- [[tapd-getting-started]]: Getting started with tapd
- [[minting-taproot-assets]]: Minting assets, metadata and collectibles
- [[tapd-universes-guide]]: Working with universes
- [[taproot-assets-channels-guide]]: Taproot Assets channels in practice
- [[tapd-rfq-guide]]: RFQ and price oracles in practice
- [[edge-node-operation]]: Becoming an edge node
- [[tapd-operations]]: Operating tapd safely: multisig, debugging, tips

## Concept pages

- [[taproot-assets-protocol]]
- [[taproot-assets-on-lightning]]
