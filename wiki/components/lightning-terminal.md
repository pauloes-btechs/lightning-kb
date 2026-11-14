---
title: Lightning Terminal (litd)
type: component
sources:
  - raw/docs/lightning-network-tools/lightning-terminal.md
  - raw/docs/lightning-network-tools/lightning-terminal/introduction.md
  - raw/api/api-docs/api/lit.md
  - raw/api/api-docs/api/lit/rest-endpoints.md
  - raw/api/api-docs/api/lit/accounts/account-info.md
  - raw/api/api-docs/api/lit/accounts/account-payments.md
  - raw/api/api-docs/api/lit/accounts/create-account.md
  - raw/api/api-docs/api/lit/accounts/credit-account.md
  - raw/api/api-docs/api/lit/accounts/debit-account.md
  - raw/api/api-docs/api/lit/accounts/list-accounts.md
  - raw/api/api-docs/api/lit/accounts/remove-account.md
  - raw/api/api-docs/api/lit/accounts/update-account.md
  - raw/api/api-docs/api/lit/autopilot/add-autopilot-session.md
  - raw/api/api-docs/api/lit/autopilot/list-autopilot-features.md
  - raw/api/api-docs/api/lit/autopilot/list-autopilot-sessions.md
  - raw/api/api-docs/api/lit/autopilot/revoke-autopilot-session.md
  - raw/api/api-docs/api/lit/firewall/list-actions.md
  - raw/api/api-docs/api/lit/firewall/privacy-map-conversion.md
  - raw/api/api-docs/api/lit/proxy/bake-super-macaroon.md
  - raw/api/api-docs/api/lit/proxy/get-info.md
  - raw/api/api-docs/api/lit/proxy/stop-daemon.md
  - raw/api/api-docs/api/lit/sessions/add-session.md
  - raw/api/api-docs/api/lit/sessions/list-sessions.md
  - raw/api/api-docs/api/lit/sessions/revoke-session.md
  - raw/api/api-docs/api/lit/status/sub-server-status.md
updated: 2026-11-14
---

# Lightning Terminal (litd)

## What it is

Lightning Terminal is a web-based dashboard for Lightning Labs products. Through Terminal, you can manage your Lightning node remotely, perform Loops, and buy and sell channels on Pool; you can monitor your node's health, channels and balances, open channels, and rebalance your liquidity. ([source](../../raw/docs/lightning-network-tools/lightning-terminal.md))

The API reference describes Lightning Terminal (LiT) as a browser-based interface for managing channel liquidity. Its listed features are: visualize your channels and balances; perform submarine swaps via the Lightning Loop service; classify channels according to your node's operating mode; run a single binary that integrates the `loopd`, `poold` and `faraday` daemons all in one; access a preview release of the Pool UI; and use Pool to earn sats by opening channels to those needing inbound liquidity. ([source](../../raw/api/api-docs/api/lit.md))

The guide uses two names. "Terminal" is the web dashboard at terminal.lightning.engineering, and `litd` is the Lightning Terminal daemon; bringing Terminal to the web delivers some of the features of `litd` to a web based, remote experience. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/introduction.md))

## What it is for

- Top performing nodes: Terminal ranks public Lightning nodes based on their centrality, stability and routing ability, to help decide who to peer and open channels with, and gives suggestions on peers that would complement your node or the network.
- Your node's information: your node's ranking, centrality and health assessments, recent transactions, a summary of fees earned and payments forwarded, and a user interface to monitor and manage the node, such as opening channels or observing their balances.
- Loop: initiate Loops, select which channel to deplete or fill, and monitor the status of ongoing swaps.
- Pool: place asks and bids through the web browser, see matched orders, calculate fees earned and spent, and monitor the channels opened through the platform.
- Taproot Assets: the guide lists the Taproot Assets Protocol and the Taproot Assets Daemon, `tapd`, among Terminal's features.

([source](../../raw/docs/lightning-network-tools/lightning-terminal/introduction.md))

## Privacy model

Lightning Labs does not see or store your node's information. Using Lightning Node Connect (LNC), an end-to-end encrypted connection is established between your browser and your node, and private information such as HTLCs, private channels, or any other non-public information remains private; the LNC proxy server sees it only as encrypted blobs. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/introduction.md))

LNC makes use of LND's existing gRPC interface. The node makes an outgoing connection to a web proxy, to which the user navigates with their browser or application, and a password-authenticated key exchange (PAKE) makes the session end-to-end encrypted and authenticated between the user and their node. LNC is described as working even if the node is behind Tor or a NAT. Terminal Connect is implemented as part of Terminal and `litd 0.6`. See [[lightning-node-connect]] and [[terminal-privacy-and-security]]. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/introduction.md))

## Relation to the other products

- [[lnd]]: to make use of Terminal, you need to run `litd` together with `lnd`, either on the same or separate machines. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/introduction.md))
- [[loop]], [[pool]], [[faraday]]: Lightning Terminal's listed features include running a single binary that integrates the `loopd`, `poold` and `faraday` daemons all in one. ([source](../../raw/api/api-docs/api/lit.md))
- [[taproot-assets]]: listed as a Terminal feature in the guide introduction. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/introduction.md))

Lightning Terminal including Pool and Loop continues to be available as part of `litd` for those who prefer to self-host the application on their own device. It is currently not possible to see recommended channels, make and receive payments or see recent forwarded transactions through the interface of the self-hosted Lightning Terminal. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/introduction.md))

## Installing and running

The two pages in this page's scope say only that `litd` runs together with `lnd` (same or separate machines), after which you browse to terminal.lightning.engineering and initialize a session with Lightning Node Connect. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/introduction.md))

The guide's Lightning Terminal section lists pages titled "Get litd" and "Run litd". ([source](../../raw/docs/lightning-network-tools/lightning-terminal.md))

See also: [[running-litd]].

The API reference's code samples assume a local `litd` instance listening for both gRPC and REST connections on port `8443`. `LIT_DIR` denotes the base directory of the `litd` instance; by default this is `~/.lit` on Linux and `~/Library/Application Support/Lit` on macOS. Two things are needed to make a request to `litd`: a TLS/SSL connection and a macaroon used for RPC authentication. ([source](../../raw/api/api-docs/api/lit.md))

## CLI: litcli

The command line client is `litcli`; the API reference documents it alongside the Python and JavaScript clients. ([source](../../raw/api/api-docs/api/lit.md))

Commands shown on the RPC pages, with the RPC each page documents:

| Command | RPC | Service page |
| --- | --- | --- |
| `litcli getinfo` | GetInfo | [[lit-proxy]] |
| `litcli stop` | StopDaemon | [[lit-proxy]] |
| `litcli bakesupermacaroon` | BakeSuperMacaroon | [[lit-proxy]] |
| `litcli accounts create`, `update`, `update credit`, `update debit`, `list`, `info`, `remove`, `payments` | CreateAccount and the other account RPCs | [[lit-accounts]] |
| `litcli sessions add`, `list`, `revoke` | AddSession, ListSessions, RevokeSession | [[lit-sessions]] |
| `litcli autopilot features`, `add`, `list`, `revoke` | the Autopilot RPCs | [[lit-autopilot]] |
| `litcli actions` | ListActions | [[lit-firewall]] |
| `litcli privacy` | PrivacyMapConversion | [[lit-firewall]] |

([source](../../raw/api/api-docs/api/lit/accounts/account-info.md), [source](../../raw/api/api-docs/api/lit/accounts/account-payments.md), [source](../../raw/api/api-docs/api/lit/accounts/create-account.md), [source](../../raw/api/api-docs/api/lit/accounts/credit-account.md), [source](../../raw/api/api-docs/api/lit/accounts/debit-account.md), [source](../../raw/api/api-docs/api/lit/accounts/list-accounts.md), [source](../../raw/api/api-docs/api/lit/accounts/remove-account.md), [source](../../raw/api/api-docs/api/lit/accounts/update-account.md), [source](../../raw/api/api-docs/api/lit/autopilot/add-autopilot-session.md), [source](../../raw/api/api-docs/api/lit/autopilot/list-autopilot-features.md), [source](../../raw/api/api-docs/api/lit/autopilot/list-autopilot-sessions.md), [source](../../raw/api/api-docs/api/lit/autopilot/revoke-autopilot-session.md), [source](../../raw/api/api-docs/api/lit/firewall/list-actions.md), [source](../../raw/api/api-docs/api/lit/firewall/privacy-map-conversion.md), [source](../../raw/api/api-docs/api/lit/proxy/bake-super-macaroon.md), [source](../../raw/api/api-docs/api/lit/proxy/get-info.md), [source](../../raw/api/api-docs/api/lit/proxy/stop-daemon.md), [source](../../raw/api/api-docs/api/lit/sessions/add-session.md), [source](../../raw/api/api-docs/api/lit/sessions/list-sessions.md), [source](../../raw/api/api-docs/api/lit/sessions/revoke-session.md))

See also: [[litd-integration]].

## API services

The gRPC reference was generated automatically against commit `068c1bfa3ec8ada4f2dcdb4deab7e4cb20522dce` of the `lightninglabs/lightning-terminal` repository, from six proto files under `litrpc/`: `firewall.proto`, `lit-accounts.proto`, `lit-autopilot.proto`, `lit-sessions.proto`, `lit-status.proto` and `proxy.proto`. ([source](../../raw/api/api-docs/api/lit.md))

| Service page | RPCs | REST prefix |
| --- | --- | --- |
| [[lit-accounts]] | CreateAccount, UpdateAccount, CreditAccount, DebitAccount, ListAccounts, AccountInfo, RemoveAccount, AccountPayments | `/v1/accounts` |
| [[lit-autopilot]] | ListAutopilotFeatures, AddAutopilotSession, ListAutopilotSessions, RevokeAutopilotSession | `/v1/autopilot` |
| [[lit-firewall]] | ListActions, PrivacyMapConversion | `/v1/firewall` |
| [[lit-proxy]] | GetInfo, StopDaemon, BakeSuperMacaroon | `/v1/proxy` |
| [[lit-sessions]] | AddSession, ListSessions, RevokeSession | `/v1/sessions` |
| [[lit-status]] | SubServerStatus | `/v1/status` |

The REST endpoints page lists 20 REST paths; every RPC above has one except AccountInfo, which does not appear in that listing and whose own page shows no REST path. ([source](../../raw/api/api-docs/api/lit/rest-endpoints.md), [source](../../raw/api/api-docs/api/lit/accounts/account-info.md), [source](../../raw/api/api-docs/api/lit/status/sub-server-status.md))

For REST, the `byte` field type must be set as the base64 encoded string representation of a raw byte array, and when used in a URL path the base64 string must use the URL and Filename Safe Alphabet: replace `+` with `-`, `/` with `_`, and keep the trailing `=` as is. Url encoding (ie. `%2F`) will not work. ([source](../../raw/api/api-docs/api/lit.md))

## How-to pages

- [[running-litd]]: Installing and running litd
- [[lightning-node-connect]]: Lightning Node Connect
- [[litd-accounts-guide]]: Using litd accounts
- [[terminal-liquidity-tools]]: Terminal liquidity tools: autofees, autoopen, reports
- [[litd-integration]]: Integrating litd and its CLI
- [[terminal-privacy-and-security]]: Terminal privacy and security
- [[litd-troubleshooting]]: Troubleshooting litd and testing on signet

The guide's Lightning Terminal section lists these sub-pages: What is Lightning Terminal?, Get litd, Run litd, Integrating litd, Demo: Litd Speed Run, Connect to Terminal, Recommended Channels, Rankings, Health Checks, Liquidity, Opening Lightning Network Channels, Managing Channel Liquidity, Autofees, AutoOpen, LND Accounts, Loop and Lightning Terminal, Loop Fees, Pool and Lightning Terminal, Command Line Interface, Troubleshooting, Lightning Node Connect: Under the hood, LNC Node Package, Privacy and Security, Privacy Policy, Terms of Use. ([source](../../raw/docs/lightning-network-tools/lightning-terminal.md))
