---
title: Faraday
type: component
sources:
  - raw/docs/lightning-network-tools/faraday.md
  - raw/docs/lightning-network-tools/faraday/get-started.md
  - raw/docs/lightning-network-tools/faraday/the-faraday-cli.md
  - raw/api/api-docs/api/faraday.md
  - raw/api/api-docs/api/faraday/rest-endpoints.md
  - raw/api/api-docs/api/faraday/faraday-server/channel-insights.md
updated: 2026-11-14
---

# Faraday

Faraday is a suite of tools built to help node operators and businesses run lnd (see [[lnd]]). Its tools decrease the operational overhead of running a Lightning node. It is developed by Lightning Labs to extract analytics and insights from an LND node. ([source](../../raw/docs/lightning-network-tools/faraday.md))

Faraday primarily helps users understand how capital is flowing through their node, which is useful to identify underperforming or drained channels and where to deploy capital most efficiently (see [[routing-nodes]] and [[liquidity]]). ([source](../../raw/docs/lightning-network-tools/faraday.md))

The API reference adds that the current features in the Faraday suite provide insight into node channel performance and support for accounting with both on-chain and off-chain reports for lnd. ([source](../../raw/api/api-docs/api/faraday.md))

## Relationship to other products

Faraday comes bundled in Lightning Terminal: if Lightning Terminal is installed, Faraday is already running inside it and can be accessed through the command line. When running Lightning Terminal, the port must be specified every time `frcli` is run, using the flag `--rpcserver=localhost:8443`. See [[lightning-terminal]] and [[running-litd]]. ([source](../../raw/docs/lightning-network-tools/faraday/get-started.md))

To run Faraday you need to be running LND from the binary releases, or compiled from source with `make install tags="signrpc walletrpc chainrpc invoicesrpc"`. See [[running-lnd]]. ([source](../../raw/docs/lightning-network-tools/faraday/get-started.md))

To make full use of Faraday it must also be connected to a Bitcoin node, for example `bitcoind` or `btcd`. The close report and the node audit require this connection. ([source](../../raw/docs/lightning-network-tools/faraday/get-started.md), [source](../../raw/docs/lightning-network-tools/faraday/the-faraday-cli.md))

The node audit can identify [[loop]] and [[pool]] transactions when run with the flags `--loop-category` and `--pool-category`. ([source](../../raw/docs/lightning-network-tools/faraday/the-faraday-cli.md))

## Install and run

Faraday can be run directly from the binary releases, or compiled from source with `git clone https://github.com/lightninglabs/faraday.git`, `cd faraday`, `make && make install`. It comes with two components: the daemon `faraday` and the command line interface `frcli`. The full procedure, including the Bitcoin node connection and the Lightning Terminal configuration, is on [[using-faraday]]. ([source](../../raw/docs/lightning-network-tools/faraday/get-started.md))

## CLI: frcli

`frcli` can be used as soon as Faraday is running, either by typing `frcli` or by navigating to where the binaries are stored and executing `./frcli`. The commands covered by the guide are `frcli insights`, `frcli revenue`, `frcli threshold`, `frcli outliers`, `frcli closereport`, `frcli audit` and `frcli fiat`; each is described on [[using-faraday]]. ([source](../../raw/docs/lightning-network-tools/faraday/the-faraday-cli.md))

## API

Faraday exposes one gRPC service, documented on [[faraday-server]]. The API reference was generated against commit `7226d871511a1995cd1aa08467b469809a36e508` of the faraday repository, from `faraday.proto` and `faraday.swagger.json` in `frdrpc/`. ([source](../../raw/api/api-docs/api/faraday.md))

The reference's code samples assume a local `faraday` instance listening for gRPC connections on port `8465` and for REST connections on port `8082`. The base directory, denoted `FARADAY_DIR`, is by default `~/.faraday` on Linux and `~/Library/Application Support/Faraday` on macOS. ([source](../../raw/api/api-docs/api/faraday.md))

Two things are needed to make a gRPC or HTTP request to a `faraday` instance: a TLS/SSL connection and a macaroon used for RPC authentication (see [[macaroons]]). ([source](../../raw/api/api-docs/api/faraday.md))

For REST, the `byte` field type must be set as the base64 encoded string representation of a raw byte array. When used in a URL path the base64 string must use the URL and Filename Safe Alphabet: replace `+` with `-`, `/` with `_`, and keep the trailing `=` as is. Url encoding (ie. `%2F`) will not work. ([source](../../raw/api/api-docs/api/faraday.md))

The REST endpoints listing has eight paths, all under `/v1/faraday/`: `closereport`, `exchangerate`, `getchannelevents`, `insights`, `nodeaudit`, `outliers/{rec_request.metric}`, `revenue` and `threshold/{rec_request.metric}`. All are `GET` except `/v1/faraday/getchannelevents`, which is `POST`. ([source](../../raw/api/api-docs/api/faraday/rest-endpoints.md))

## Pages for this product

- [[faraday-server]]: faraday faraday-server service
- [[using-faraday]]: Using Faraday and frcli

## Conflicts

- REST port. The API overview says the code samples assume REST connections on port `8082` ([source](../../raw/api/api-docs/api/faraday.md)), while the example requests on the individual RPC pages use port 8466, for example `http://localhost:8466/v1/faraday/insights` ([source](../../raw/api/api-docs/api/faraday/faraday-server/channel-insights.md)). See [[faraday-server]].
