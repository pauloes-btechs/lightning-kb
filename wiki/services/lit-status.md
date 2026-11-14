---
title: lit status service
type: service
sources:
  - raw/api/api-docs/api/lit.md
  - raw/api/api-docs/api/lit/rest-endpoints.md
  - raw/api/api-docs/api/lit/status/sub-server-status.md
updated: 2026-11-14
---

# lit status service (Status)

The status service of [[lightning-terminal]] is documented through the SubServerStatus RPC, whose response is a map of sub-server names to their status. The SubServerStatus page gives `lit-status.proto` as its source. ([source](../../raw/api/api-docs/api/lit/status/sub-server-status.md))

The reference was generated automatically against commit `068c1bfa3ec8ada4f2dcdb4deab7e4cb20522dce` of the `lightninglabs/lightning-terminal` repository. ([source](../../raw/api/api-docs/api/lit.md))

The REST endpoints page lists one RPC under `/v1/status`, SubServerStatus. ([source](../../raw/api/api-docs/api/lit/rest-endpoints.md))

## SubServerStatus

The page gives no description for this RPC. ([source](../../raw/api/api-docs/api/lit/status/sub-server-status.md))

- gRPC: `rpc SubServerStatus (SubServerStatusReq) returns (SubServerStatusResp);`
- REST: `GET /v1/status`
- Request message: `litrpc.SubServerStatusReq`
- Response message: `litrpc.SubServerStatusResp`

The request has no parameters. The response has one field, `sub_servers`, a map of sub-server names to their status. Each value is a `litrpc.SubServerStatus` with these fields:

- `disabled`: true if the sub-server is available in the LiT package but has explicitly been disabled.
- `running`: true if the sub-server is currently running.
- `error`: describes an error that might have resulted in the sub-server not starting up properly.
- `custom_status`: details a custom state that the sub-server has entered, which is unique to the sub-server, and which is not the standard disabled, running or errored state.

The page shows no `litcli` command for this RPC, and the sub-server names used as map keys are not found in sources. ([source](../../raw/api/api-docs/api/lit/status/sub-server-status.md))

See also: [[lit-proxy]], [[litd-troubleshooting]].
