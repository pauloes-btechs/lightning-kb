---
title: lnd
type: component
sources:
  - raw/docs/lightning-network-tools/lnd.md
  - raw/api/api-docs/api/lnd.md
  - raw/api/api-docs/api/lnd/rest-endpoints.md
updated: 2026-11-14
---

# lnd

The Lightning Network Daemon (LND) is Lightning Labs' implementation of a Lightning Network node. ([source](../../raw/docs/lightning-network-tools/lnd.md))

The API reference describes `lnd` as a complete implementation of a Lightning Network node with several pluggable back-end chain services: `btcd` (a full-node), `bitcoind`, and `neutrino` (described as "a new experimental light client"). The codebase uses the btcsuite set of Bitcoin libraries and exports a large set of isolated re-usable Lightning Network related libraries. ([source](../../raw/api/api-docs/api/lnd.md))

See also: [[lightning-network-overview]], [[payment-channels]], [[macaroons]].

## What lnd can do

According to the API overview, `lnd` is capable of: creating channels; closing channels; completely managing all channel states (including the exceptional ones); maintaining a fully authenticated and validated channel graph; performing path finding within the network and passively forwarding incoming payments; sending outgoing onion-encrypted payments through the network; updating advertised fee schedules; and automatic channel management (`autopilot`). ([source](../../raw/api/api-docs/api/lnd.md))

## Interfaces: lncli, gRPC and REST

The API reference covers `lncli` (CLI), Python and JavaScript, for communicating with a local `lnd` instance through gRPC and REST. Its code samples assume `lnd` listens for gRPC connections on port `10009` and for REST connections on port `8080`. `LND_DIR` denotes the base directory of the instance, by default `~/.lnd` on Linux and `~/Library/Application Support/Lnd` on macOS. A gRPC or HTTP request needs a TLS/SSL connection and a macaroon used for RPC authentication. ([source](../../raw/api/api-docs/api/lnd.md))

For REST, a `byte` field must be set as the base64-encoded string of the raw bytes; when used in a URL path the base64 string must use the URL and Filename Safe Alphabet (replace `+` with `-` and `/` with `_`, keep the trailing `=`); URL encoding such as `%2F` will not work. ([source](../../raw/api/api-docs/api/lnd.md))

The reference was generated automatically against commit `895118ac4ec59e78b2c14f5b0d31ac6f862434bb` of `lightningnetwork/lnd`, from these proto files: `autopilotrpc/autopilot.proto`, `chainrpc/chainkit.proto`, `chainrpc/chainnotifier.proto`, `devrpc/dev.proto`, `invoicesrpc/invoices.proto`, `lightning.proto`, `lnclipb/lncli.proto`, `neutrinorpc/neutrino.proto`, `peersrpc/peers.proto`, `routerrpc/router.proto`, `signrpc/signer.proto`, `stateservice.proto`, `switchrpc/switch.proto`, `verrpc/verrpc.proto`, `walletrpc/walletkit.proto`, `walletunlocker.proto`, `watchonlyrpc/watchonly.proto`, `watchtowerrpc/watchtower.proto` and `wtclientrpc/wtclient.proto`. ([source](../../raw/api/api-docs/api/lnd.md))

The overview marks these services as experimental: subject to change, and needing a compile-time flag to be active (they are active in the official release binaries): Autopilot, ChainKit, ChainNotifier, Invoices, NeutrinoKit, Peers, Signer, WalletKit and Watchtower. ([source](../../raw/api/api-docs/api/lnd.md))

The REST endpoints page lists every REST path: `lnrpc` RPCs are served under `/v1/` (for example `GET /v1/getinfo` for `lnrpc.GetInfo` and `GET /v1/state` for `lnrpc.GetState`), and sub-server RPCs under `/v2/` (for example `/v2/router/`, `/v2/invoices/`, `/v2/wallet/`, `/v2/signer/`, `/v2/switch/`, `/v2/chainkit/`, `/v2/chainnotifier/`, `/v2/neutrino/`, `/v2/autopilot/`, `/v2/dev/`, `/v2/peers/`, `/v2/versioner/`, `/v2/watchtower/client` and `/v2/watchtower/server`). ([source](../../raw/api/api-docs/api/lnd/rest-endpoints.md))

## Installing and running

The API overview points to the Builder's Guide for how to install, configure and use LND. The guide's LND section has pages including Get Started, lnd.conf, First Steps With LND, Wallet Management, Sending Payments, Atomic Multi-path Payments (AMP), Receiving Payments, Partially Signed Bitcoin Transactions, Unconfirmed Bitcoin Transactions, Channel Fees, Macaroons, Configuring Watchtowers, Key Import, Secure Your Lightning Network Node, Quick Tor Setup, Configuring Tor, Enable 'Neutrino mode' in Bitcoin Core, Send Messages With Keysend, Debugging LND, Fuzzing LND, Channel Acceptor, RPC Middleware Interceptor, NAT Traversal, Recovery: Planning for Failure, Migrating LND and Disaster recovery. ([source](../../raw/docs/lightning-network-tools/lnd.md), [source](../../raw/api/api-docs/api/lnd.md))

## Services

- [[lnd-lightning]]: lnd lightning service
- [[lnd-router]]: lnd router service
- [[lnd-invoices]]: lnd invoices service
- [[lnd-switch]]: lnd switch service
- [[lnd-wallet-kit]]: lnd wallet-kit service
- [[lnd-signer]]: lnd signer service
- [[lnd-wallet-unlocker]]: lnd wallet-unlocker service
- [[lnd-watch-only]]: lnd watch-only service
- [[lnd-state]]: lnd state service
- [[lnd-versioner]]: lnd versioner service
- [[lnd-autopilot]]: lnd autopilot service
- [[lnd-chain-kit]]: lnd chain-kit service
- [[lnd-chain-notifier]]: lnd chain-notifier service
- [[lnd-neutrino-kit]]: lnd neutrino-kit service
- [[lnd-peers]]: lnd peers service
- [[lnd-dev]]: lnd dev service
- [[lnd-watchtower]]: lnd watchtower service
- [[lnd-watchtower-client]]: lnd watchtower-client service

## How-to pages

- [[running-lnd]]: Installing, running and first steps with lnd
- [[lnd-configuration]]: lnd configuration and lnd.conf
- [[lnd-wallet-and-psbt]]: lnd wallet, PSBT and key import
- [[lnd-sending-payments]]: Sending with lnd: payments, AMP, keysend, probing
- [[lnd-receiving-payments]]: Receiving with lnd: invoices and blinded paths
- [[lnd-channel-fees]]: Channel fees and inbound fees in lnd
- [[lnd-macaroons]]: lnd macaroons
- [[lnd-tor-and-networking]]: Tor, NAT traversal and node security
- [[lnd-recovery]]: Disaster recovery and migration
- [[lnd-interceptors]]: HTLC interceptor, RPC middleware and channel acceptor
- [[lnd-routing-node-operations]]: Operating a routing node with lnd
- [[lnd-sweeper]]: The lnd sweeper and unconfirmed transactions
- [[lnd-watchtower-setup]]: Setting up watchtowers
- [[lnd-debugging-and-contributing]]: Debugging, fuzzing and contributing to lnd

## Related concepts

See also: [[watchtowers]], [[macaroons]], [[payment-channels]], [[lightning-network-overview]].
