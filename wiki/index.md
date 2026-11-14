# Lightning KB index

Every wiki page, one line each, grouped by folder. Maintained by the agent
(see `CLAUDE.md`). Empty until the first ingest.

## Components
- [[aperture]]: What Aperture is: an L402 and MPP reverse proxy, how it relates to lnd and LNC, install and admin interfaces.
- [[faraday]]: What Faraday is, its lnd and bitcoind requirements, bundling in litd, frcli and API ports.
- [[lightning-terminal]]: What Lightning Terminal (litd) is, the LNC privacy model, bundled products, port 8443 and litcli.
- [[loop]]: What Loop is, Loop In versus Loop Out, its relation to lnd and litd, install, CLI and API ports.

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

## Concepts

## How-tos
- [[aperture-mailbox-and-lnc]]: Self-hosting the LNC mailbox and connecting Aperture to lnd over LNC.
- [[aperture-pricing-and-services]]: Service definitions, fixed and dynamic pricing, and enabling the admin services.
- [[autoloop]]: Automatic swap dispatch: easy autoloop, rules, fees, budget, and why swaps are disqualified.
- [[instant-loop-outs]]: Reservations, setup and the `loop instantout` flow.
- [[lightning-node-connect]]: How LNC works: pairing, handshakes, the mailbox proxy, the WASM client and lnc-web.
- [[litd-accounts-guide]]: Custodial accounts in practice: rules enforced, creating accounts, macaroons and LNC sessions.
- [[litd-integration]]: Moving services into and out of integrated mode, and CLI arguments per bundled tool.
- [[litd-troubleshooting]]: Connection fixes, Pool database and account recovery, and running the stack on signet.
- [[machine-payments-protocol]]: MPP compared with L402 and the aperture.yaml keys that enable it.
- [[running-aperture]]: Building Aperture, configuring aperture.yaml, obtaining a TLS certificate, starting and verifying.
- [[running-litd]]: Installing litd, integrated and remote configuration, reaching the UI, and connecting to Terminal.
- [[static-loop-in-addresses]]: Static address design, deposit and swap flow, the `loop static` commands and related RPCs.
- [[terminal-liquidity-tools]]: Channels, health checks, rankings, the liquidity report, Autofees, AutoOpen, and Loop and Pool in the UI.
- [[terminal-privacy-and-security]]: The security model, what the proxy can see, and the privacy policy and terms of use.
- [[using-faraday]]: Installing and running Faraday, litd configuration, and each frcli command with its flags.
- [[using-loop]]: Installing loopd, quotes, Loop In and Loop Out with the CLI, fees, and peering with Loop.

## Comparisons

## Questions
