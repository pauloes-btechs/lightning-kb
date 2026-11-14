# Lightning KB index

Every wiki page, one line each, grouped by folder. Maintained by the agent
(see `CLAUDE.md`). Empty until the first ingest.

## Components
- [[aperture]]: What Aperture is: an L402 and MPP reverse proxy, how it relates to lnd and LNC, install and admin interfaces.
- [[faraday]]: What Faraday is, its lnd and bitcoind requirements, bundling in litd, frcli and API ports.
- [[loop]]: What Loop is, Loop In versus Loop Out, its relation to lnd and litd, install, CLI and API ports.

## Services
- [[faraday-server]]: All nine Faraday RPCs: purpose, gRPC signature, REST path, messages and key fields.
- [[loop-debug]]: The debug service's single RPC, ForceAutoLoop (testing only, not mainnet).
- [[loop-swap-client]]: All 33 swap-client RPCs: purpose, gRPC signature, REST path, messages and key fields.

## Concepts

## How-tos
- [[aperture-mailbox-and-lnc]]: Self-hosting the LNC mailbox and connecting Aperture to lnd over LNC.
- [[aperture-pricing-and-services]]: Service definitions, fixed and dynamic pricing, and enabling the admin services.
- [[autoloop]]: Automatic swap dispatch: easy autoloop, rules, fees, budget, and why swaps are disqualified.
- [[instant-loop-outs]]: Reservations, setup and the `loop instantout` flow.
- [[machine-payments-protocol]]: MPP compared with L402 and the aperture.yaml keys that enable it.
- [[running-aperture]]: Building Aperture, configuring aperture.yaml, obtaining a TLS certificate, starting and verifying.
- [[static-loop-in-addresses]]: Static address design, deposit and swap flow, the `loop static` commands and related RPCs.
- [[using-faraday]]: Installing and running Faraday, litd configuration, and each frcli command with its flags.
- [[using-loop]]: Installing loopd, quotes, Loop In and Loop Out with the CLI, fees, and peering with Loop.

## Comparisons

## Questions
