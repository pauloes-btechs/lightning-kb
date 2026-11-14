---
title: Aperture services and pricing
type: howto
sources:
  - raw/docs/lightning-network-tools/aperture/pricing.md
  - raw/docs/lightning-network-tools/aperture/step-by-step.md
  - raw/docs/lightning-network-tools/aperture/admin-services.md
updated: 2026-11-14
---

# Aperture services and pricing

How services are defined behind [[aperture]], how they are priced, and how the admin interfaces (CLI, MCP, REST API, dashboard) are enabled and used. Installation is on [[running-aperture]].

## User flow

In both fixed and dynamic pricing, the Aperture server acts as a proxy between the user and the content server. A user requesting the resource without the requisite L402 is served the HTTP error response "402 Payment Required", together with a Macaroon and a Lightning Network invoice. By paying the invoice the user obtains the preimage, which together with the Macaroon forms the valid L402 that is presented to Aperture to obtain the resource. The protocol is described on [[l402]] and [[macaroons]]. ([source](../../raw/docs/lightning-network-tools/aperture/pricing.md))

## Defining a service

Services are listed under `services:` in `aperture.yaml`. Requests are matched to the services in order, picking the first that satisfies `hostregexp` and (if set) `pathregexp`, so order is important. Regular expressions with special characters should be in single quotes to avoid YAML parsing errors. ([source](../../raw/docs/lightning-network-tools/aperture/step-by-step.md))

The step-by-step example defines one service:

```yaml
services:
    # The identifying name of the service. This will also be used to identify
    # which capabilities caveat (if any) corresponds to the service.
  - name: "l402proxy"
    # The regular expression used to match the service host.
    hostregexp: 'l402proxy.domain.com'
    # The regular expression used to match the path of the URL.
    pathregexp: '^/service.*$'
    # The host:port which the service can be reached at.
    address: "127.0.0.1:8080"
    # The HTTP protocol that should be used to connect to the service. Valid
    # options include: http, https.
    protocol: http
    # a caveat will be added that expires the L402 after this many seconds,
    # 31557600 = 1 year.
    timeout: 3600
    # The L402 value in satoshis for the service. It is ignored if
    # dynamicprice.enabled is set to true.
    price: 2
    # A list of regular expressions for path that are free of charge.
    authwhitelistpaths:
      - '^/service/free/*$'
```

([source](../../raw/docs/lightning-network-tools/aperture/step-by-step.md))

| Key | Meaning (from the example's comments) |
| --- | --- |
| `name` | The identifying name of the service; also used to identify which capabilities caveat (if any) corresponds to the service. |
| `hostregexp` | The regular expression used to match the service host. |
| `pathregexp` | The regular expression used to match the path of the URL. |
| `address` | The host:port which the service can be reached at. |
| `protocol` | The HTTP protocol used to connect to the service. Valid options include: http, https. |
| `timeout` | A caveat is added that expires the L402 after this many seconds; 31557600 = 1 year. |
| `price` | The L402 value in satoshis for the service. Ignored if `dynamicprice.enabled` is set to true. |
| `authwhitelistpaths` | A list of regular expressions for path that are free of charge. |

([source](../../raw/docs/lightning-network-tools/aperture/step-by-step.md))

## Fixed pricing

In fixed pricing, a resource is offered for a fixed price, expressed in satoshis. Multiple resources can be configured, each with their own price. The pricing page's example:

```
  - name: "service2"
	hostregexp: "service2.com:8083"
	pathregexp: '^/.*$'
	address: "123.456.789:8082"
	protocol: https
	constraints:
    	"valid_until": "2020-01-01"
	price: 1
```

([source](../../raw/docs/lightning-network-tools/aperture/pricing.md))

For each service, a valid L402 allows its holder to access unlimited resources on that service. To price each resource individually, dynamic pricing has to be used. ([source](../../raw/docs/lightning-network-tools/aperture/pricing.md))

## Dynamic pricing

For dynamic pricing, Aperture is configured to connect to a separate service over gRPC. The page says this allows, for example, resources to be priced in fiat currency, selling a large repository of items each with their own pricing, or adjusting prices based on demand. The pricing page's example:

```
  - name: "service3"
	hostregexp: "service3.com:8083"
	pathregexp: '^/.*$'
	address: "123.456.789:8082"
	protocol: https
	constraints:
    	"valid_until": "2020-01-01"
	dynamicprice:
  	enabled: true
  	grpcaddress: 123.456.789:8083
  	insecure: false
  	tlscertpath: "path-to-pricer-server-tls-cert/tls.cert"
```

([source](../../raw/docs/lightning-network-tools/aperture/pricing.md))

The gRPC interface the pricing service must implement is not found in sources; the page points to a demo repository, <https://github.com/ellemouton/aperture-demo>, and a video. ([source](../../raw/docs/lightning-network-tools/aperture/pricing.md))

## Admin services

### Enable

To enable the Aperture Admin Services, the application needs to be compiled with the dashboard:

```
make build-dashboard
make build-withdashboard
```

Then the admin mode is configured in the aperture.yaml, and takes effect upon restart:

```
admin:
	enabled: true
```

([source](../../raw/docs/lightning-network-tools/aperture/admin-services.md))

Aperture requires a macaroon to authenticate calls to the LND backend. The required permissions can be obtained with `lncli bakemacaroon invoices:read invoices:write offchain:write`; LND's standard `invoice.macaroon` is also sufficient. See [[lnd-macaroons]]. ([source](../../raw/docs/lightning-network-tools/aperture/admin-services.md))

### aperturecli

The CLI is available under the name `aperturecli`. If Aperture is running with a self-signed certificate, the path to the certificate has to be specified:

```
aperturecli --tls-cert .aperture/tls.cert info
```

Through the CLI you can check the server's `health`, get revenue statistics (`stats`), list and revoke L402 `tokens` and query past L402 `transactions`. ([source](../../raw/docs/lightning-network-tools/aperture/admin-services.md))

Pricing can be changed dynamically through the CLI:

```
aperturecli services update --name myapi --price 500
```

([source](../../raw/docs/lightning-network-tools/aperture/admin-services.md))

### Model Context Protocol

Aperture exposes an MCP interface for use with agents. It supports the same commands as the CLI and accepts requests in JSON format. To discover the structure and content of the json commands, append `--dry-run` to the CLI commands. The MCP server is started with `aperturecli mcp serve`. ([source](../../raw/docs/lightning-network-tools/aperture/admin-services.md))

### REST API

Aperture exposes a Rest API at port `8081`, at `/api/admin/<command>`, accepting all the commands from the CLI. Macaroon authentication is necessary, using the admin.macaroon placed on startup in `~/.aperture` or the working directory of your choice. ([source](../../raw/docs/lightning-network-tools/aperture/admin-services.md))

### Dashboard

When the admin interface is enabled, Aperture also exposes a dashboard on port `8081`. It is only exposed to requests from `localhost`, but care needs to be taken when Aperture sits behind another proxy. ([source](../../raw/docs/lightning-network-tools/aperture/admin-services.md))

## Conflicts

- Price in the step-by-step example. The prose says "Each L402 costs 21 satoshis", while the configuration file below it sets `price: 2` ([source](../../raw/docs/lightning-network-tools/aperture/step-by-step.md)).
- Expiry key. The step-by-step example expires the L402 with `timeout: 3600` ([source](../../raw/docs/lightning-network-tools/aperture/step-by-step.md)); the pricing examples instead use `constraints:` with `"valid_until": "2020-01-01"` and no `timeout` ([source](../../raw/docs/lightning-network-tools/aperture/pricing.md)). The sources do not explain how the two relate.

## Notes

Synthesis, not from a source: the pricing page's YAML examples are reproduced with their original mixed tab and space indentation, which is not valid YAML as printed. The step-by-step comment that `price` is ignored "if dynamicprice.enabled is set to true" indicates `enabled`, `grpcaddress`, `insecure` and `tlscertpath` are children of `dynamicprice`.
