---
title: Aperture
type: component
sources:
  - raw/docs/lightning-network-tools/aperture.md
  - raw/docs/lightning-network-tools/aperture/get-aperture.md
  - raw/docs/lightning-network-tools/aperture/step-by-step.md
  - raw/docs/lightning-network-tools/aperture/admin-services.md
  - raw/docs/lightning-network-tools/aperture/machine-payments-protocol.md
  - raw/docs/lightning-network-tools/aperture/lnc-backend.md
  - raw/docs/lightning-network-tools/aperture/mailbox.md
  - raw/docs/lightning-network-tools/aperture/pricing.md
updated: 2026-11-14
---

# Aperture

Aperture is an implementation of L402s as a reverse HTTP proxy. It acts as a payment and authentication gateway for Lightning Network powered APIs, and can handle gRPC requests over HTTP/2 as well as REST over HTTP/1 and 2. The protocol itself is described on [[l402]]. ([source](../../raw/docs/lightning-network-tools/aperture.md))

Aperture receives incoming connections, verifies the validity of the L402 and either forwards the request to the appropriate end point, or obtains a Macaroon and sends it together with a Lightning invoice and the HTTP status code 402 Payment Required. See [[macaroons]]. ([source](../../raw/docs/lightning-network-tools/aperture.md))

Aperture implements both the L402 and the MPP specifications; MPP is covered on [[machine-payments-protocol]]. ([source](../../raw/docs/lightning-network-tools/aperture.md))

## What it is for

Aperture can gate any HTTP or gRPC request by a L402 paywall. It fetches Lightning Network invoices from LND and issues new macaroons to all new incoming unauthenticated requests. To authenticate incoming requests it does not need to communicate with the Lightning node. ([source](../../raw/docs/lightning-network-tools/aperture/step-by-step.md))

Aperture can be configured to price resources, such as files or API access, with either fixed or dynamic pricing. See [[aperture-pricing-and-services]]. ([source](../../raw/docs/lightning-network-tools/aperture/pricing.md))

## Relationship to other products

Aperture is currently used in production in Lightning [[loop]] and [[pool]]. ([source](../../raw/docs/lightning-network-tools/aperture.md))

Aperture uses an LND node (see [[lnd]]) to generate payment requests. In the step-by-step setup the node's port 10009 must be reachable, and Aperture is given the node's TLS certificate and macaroon directory. It requires a macaroon to authenticate calls to the LND backend; LND's standard `invoice.macaroon` is sufficient. ([source](../../raw/docs/lightning-network-tools/aperture/step-by-step.md), [source](../../raw/docs/lightning-network-tools/aperture/admin-services.md))

From version 0.2 aperture supports connecting to its LND backend over Lightning Node Connect (LNC), without opening ports or configuring Tor or NAT. See [[aperture-mailbox-and-lnc]] and [[lightning-node-connect]]. ([source](../../raw/docs/lightning-network-tools/aperture/lnc-backend.md))

The LNC mailbox proxy, which LNC uses to traverse firewalls and NAT, is part of the open-source aperture and can be installed by anybody. A self-hosted mailbox can be used to connect an LND node running litd to Lightning Terminal (see [[lightning-terminal]]). ([source](../../raw/docs/lightning-network-tools/aperture/mailbox.md))

## Install and run

Aperture is built from source: `git clone https://github.com/lightninglabs/aperture.git`, `cd aperture`, `make install`; the stated requirement is go 1.19 or later. It is configured through `~/.aperture/aperture.yaml`, which can be started from the repository's `sample-conf.yaml`, and it is started with the command `aperture`. By default Aperture uses port 8081, which needs to be reachable from the outside. Full steps are on [[running-aperture]]. ([source](../../raw/docs/lightning-network-tools/aperture/get-aperture.md))

Aperture will create a TLS key and self-signed certificate. To run in production it needs a valid TLS certificate for the domain it is running on. ([source](../../raw/docs/lightning-network-tools/aperture/get-aperture.md))

## CLI and admin interfaces

Aperture comes bundled with a Command Line Interface (CLI), an admin API over REST and gRPC, a dashboard, and a Model Context Protocol (MCP) server. They can be used to retrieve information about the performance of the gateway and manage its pricing dynamically. ([source](../../raw/docs/lightning-network-tools/aperture/admin-services.md))

The CLI is available under the name `aperturecli`. Through it you can check the server's `health`, get revenue statistics (`stats`), list and revoke L402 `tokens`, query past L402 `transactions`, and change pricing, for example `aperturecli services update --name myapi --price 500`. The MCP server is started with `aperturecli mcp serve`. Enabling and using these interfaces is covered on [[aperture-pricing-and-services]]. ([source](../../raw/docs/lightning-network-tools/aperture/admin-services.md))

The sources in scope contain no generated gRPC API reference for Aperture, so there is no service page for it.

## Pages for this product

- [[running-aperture]]: Installing and running Aperture
- [[aperture-pricing-and-services]]: Aperture services and pricing
- [[aperture-mailbox-and-lnc]]: Aperture as LNC mailbox and backend
- [[machine-payments-protocol]]: Machine Payments Protocol
