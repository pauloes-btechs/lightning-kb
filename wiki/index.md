# Lightning KB index

Every wiki page, one line each, grouped by folder. Maintained by the agent
(see `CLAUDE.md`). Empty until the first ingest.

## Components
- [[aperture]]: What Aperture is: an L402 and MPP reverse proxy, how it relates to lnd and LNC, install and admin interfaces.
- [[faraday]]: What Faraday is, its lnd and bitcoind requirements, bundling in litd, frcli and API ports.
- [[lightning-terminal]]: What Lightning Terminal (litd) is, the LNC privacy model, bundled products, port 8443 and litcli.
- [[loop]]: What Loop is, Loop In versus Loop Out, its relation to lnd and litd, install, CLI and API ports.
- [[pool]]: What Pool is, its requirements, how it relates to lnd, litd and Loop, the CLI and API ports.
- [[taproot-assets]]: What tapd is, its features, its link to lnd, ports and proto files.

## Services
- [[faraday-server]]: All nine Faraday RPCs: purpose, gRPC signature, REST path, messages and key fields.
- [[lit-accounts]]: The eight account RPCs for off-chain accounts with spending caps, with REST paths and litcli commands.
- [[lit-autopilot]]: The four Autopilot session RPCs, features and rule messages, and the litcli autopilot commands.
- [[lit-firewall]]: ListActions and PrivacyMapConversion, with their filters and litcli commands.
- [[lit-proxy]]: GetInfo, StopDaemon and BakeSuperMacaroon.
- [[lit-sessions]]: AddSession, ListSessions and RevokeSession; the Session message, session types and states.
- [[lit-status]]: The SubServerStatus RPC and its fields.
- [[loop-debug]]: The debug service's single RPC, ForceAutoLoop (testing only, not mainnet).
- [[loop-swap-client]]: All 33 swap-client RPCs: purpose, gRPC signature, REST path, messages and key fields.
- [[pool-channel-auctioneer]]: The 14 channel-auctioneer RPCs: accounts, orders, batch streams, terms and snapshots.
- [[pool-hash-mail]]: The four hash-mail cipher box stream RPCs.
- [[pool-trader]]: The 30 trader RPCs of poold: accounts, orders, batches, leases and sidecar tickets.
- [[tapd-asset-wallet]]: 15 RPCs: virtual PSBTs, keys, ownership proofs, leases and backup.
- [[tapd-mailbox]]: 4 RPCs: send, receive, info and remove.
- [[tapd-mint]]: The 7 mint RPCs for minting assets and managing batches.
- [[tapd-portfolio-pilot]]: 3 gRPC-only RPCs: ResolveRequest, VerifyAcceptQuote and QueryAssetRates.
- [[tapd-price-oracle]]: The QueryAssetRates RPC, its intents and version notes.
- [[tapd-rfq]]: 7 RPCs: buy and sell orders and offers, accepted quotes, events and forwarding history.
- [[tapd-tap-dev]]: 3 RPCs: the deprecated ImportProof and send and receive event subscriptions.
- [[tapd-taproot-asset-channels]]: 10 RPCs: FundChannel, SendPayment, AddInvoice, decoding and tracking.
- [[tapd-taproot-assets]]: All 26 taprpc RPCs: assets, balances, addresses, sending, burning and proofs.
- [[tapd-universe]]: All 26 universe RPCs: roots, leaves, proofs, sync, federation, stats and supply commitments.

## Concepts
- [[channel-fees]]: Base fee and fee rate, who charges them, and the lncli fee policy commands.
- [[glossary]]: 176 terms from the two source glossaries, each cited.
- [[gossip-network]]: What gossip is for, the network graph, spam protection and announcement types.
- [[htlc]]: HTLC conditions and lifecycle from creation to on-chain settlement.
- [[inbound-capacity]]: What inbound capacity is and how to get it: spending, Loop Out, Pool.
- [[l402]]: The L402 flow, macaroon contents, wire format, security and implementations.
- [[lightning-invoices]]: BOLT 11 invoice structure, prefixes, amounts, tagged fields and LNURL.
- [[lightning-network-overview]]: What the Lightning Network is, its parts, and the products in the Builder's Guide.
- [[lightning-service-providers]]: What LSPs do, custody, wallet channels, fees and capital.
- [[liquidity]]: On-chain versus channel liquidity, node roles, and opening, rebalancing and closing.
- [[macaroons]]: Macaroons versus cookies, minting, caveats, delegation and revocation.
- [[merchant-liquidity]]: Acquiring, maintaining and pushing out inbound liquidity as a merchant.
- [[multihop-payments]]: A three-hop HTLC example, the payment cycle, and absolute and relative timelocks.
- [[multipath-payments]]: Why MPP exists, how parts are held and settled, MPP versus AMP.
- [[pathfinding]]: Payer-chosen onion routes, the graph, cost factors and lnd's routing.
- [[payment-channels]]: 2-of-2 channels: opening, updating, cooperative and force close.
- [[routing-nodes]]: Routing-node criteria, capital allocation and choosing peers.
- [[submarine-swaps]]: The on-chain/off-chain swap in three steps, the Loop contract, and instant swaps.
- [[sweeping]]: Which funds need sweeping, what each sweep requires, and the lncli sweep commands.
- [[taproot-assets-on-lightning]]: Asset channels, multi-hop transfers, exchange rates, edge nodes and trustless swaps.
- [[taproot-assets-protocol]]: Taptweak, sparse Merkle sum trees, issuance, transfers, addresses, proofs and universes.
- [[watchtowers]]: Channel breaches, the penalty mechanism and how watchtowers work.

## How-tos
- [[aperture-mailbox-and-lnc]]: Self-hosting the LNC mailbox and connecting Aperture to lnd over LNC.
- [[aperture-pricing-and-services]]: Service definitions, fixed and dynamic pricing, and enabling the admin services.
- [[autoloop]]: Automatic swap dispatch: easy autoloop, rules, fees, budget, and why swaps are disqualified.
- [[edge-node-operation]]: Edge node building blocks and the software that provides each.
- [[instant-loop-outs]]: Reservations, setup and the `loop instantout` flow.
- [[lightning-node-connect]]: How LNC works: pairing, handshakes, the mailbox proxy, the WASM client and lnc-web.
- [[litd-accounts-guide]]: Custodial accounts in practice: rules enforced, creating accounts, macaroons and LNC sessions.
- [[litd-integration]]: Moving services into and out of integrated mode, and CLI arguments per bundled tool.
- [[litd-troubleshooting]]: Connection fixes, Pool database and account recovery, and running the stack on signet.
- [[machine-payments-protocol]]: MPP compared with L402 and the aperture.yaml keys that enable it.
- [[minting-taproot-assets]]: Asset parameters, metadata, decimal display, collectibles and external-signer keys.
- [[pool-accounts]]: The account contract, creating, funding, withdrawing and closing accounts, and recovery.
- [[pool-channel-leases]]: Inspecting leases and how lease lifetime is enforced.
- [[pool-orders-and-batches]]: Asks and bids, order flags, fee formulas, lease durations, batch execution and snapshots.
- [[pool-setup]]: Installing the binaries, preparing lnd, running poold, remote lnd configuration and first commands.
- [[pool-zero-conf-channels]]: The zero-conf trust model, lnd.conf settings, and buying and selling zero-conf channels.
- [[running-aperture]]: Building Aperture, configuring aperture.yaml, obtaining a TLS certificate, starting and verifying.
- [[running-litd]]: Installing litd, integrated and remote configuration, reaching the UI, and connecting to Terminal.
- [[sidecar-channels]]: The sidecar ticket flow: offer, register, bid and expect-channel.
- [[static-loop-in-addresses]]: Static address design, deposit and swap flow, the `loop static` commands and related RPCs.
- [[tapd-getting-started]]: Installing and running tapd; minting, syncing, addresses, sending and burning with tapcli; Polar.
- [[tapd-operations]]: Backups, key storage, RPC exposure, multisig, debugging and payment error tips.
- [[tapd-rfq-guide]]: RFQ messages, order arithmetic, price oracle roles and configuration.
- [[tapd-universes-guide]]: Local and public universes, federations and syncing.
- [[taproot-assets-channels-guide]]: lit.conf options; opening, invoicing, paying and closing asset channels; Asset Loop Out.
- [[terminal-liquidity-tools]]: Channels, health checks, rankings, the liquidity report, Autofees, AutoOpen, and Loop and Pool in the UI.
- [[terminal-privacy-and-security]]: The security model, what the proxy can see, and the privacy policy and terms of use.
- [[using-faraday]]: Installing and running Faraday, litd configuration, and each frcli command with its flags.
- [[using-loop]]: Installing loopd, quotes, Loop In and Loop Out with the CLI, fees, and peering with Loop.

## Comparisons

## Questions
