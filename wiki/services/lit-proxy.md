---
title: lit proxy service
type: service
sources:
  - raw/api/api-docs/api/lit.md
  - raw/api/api-docs/api/lit/rest-endpoints.md
  - raw/api/api-docs/api/lit/proxy/get-info.md
  - raw/api/api-docs/api/lit/proxy/stop-daemon.md
  - raw/api/api-docs/api/lit/proxy/bake-super-macaroon.md
updated: 2026-11-14
---

# lit proxy service (Proxy)

The REST endpoints page of [[lightning-terminal]] lists three RPCs under `/v1/proxy`: GetInfo, StopDaemon and BakeSuperMacaroon. ([source](../../raw/api/api-docs/api/lit/rest-endpoints.md))

The GetInfo page gives `proxy.proto` as its source. ([source](../../raw/api/api-docs/api/lit/proxy/get-info.md))

The reference was generated automatically against commit `068c1bfa3ec8ada4f2dcdb4deab7e4cb20522dce` of the `lightninglabs/lightning-terminal` repository. ([source](../../raw/api/api-docs/api/lit.md))

See also: [[lit-status]], [[lit-sessions]].

## GetInfo

GetInfo returns general information concerning the LiTd node. ([source](../../raw/api/api-docs/api/lit/proxy/get-info.md))

- gRPC: `rpc GetInfo (GetInfoRequest) returns (GetInfoResponse);`
- REST: `GET /v1/proxy/info`
- Request message: `litrpc.GetInfoRequest`
- Response message: `litrpc.GetInfoResponse`

The request has no parameters. Response fields: `version` (the application version of the LiTd software running on the node, following Semantic Versioning 2.0.0) and `commit_hash` (the Git commit hash the LiTd binary build was based on; if the build had uncommitted changes, the most recent commit hash suffixed by "-dirty"). CLI: `litcli getinfo`. ([source](../../raw/api/api-docs/api/lit/proxy/get-info.md))

## StopDaemon

StopDaemon will send a shutdown request to the interrupt handler, triggering a graceful shutdown of the daemon. ([source](../../raw/api/api-docs/api/lit/proxy/stop-daemon.md))

- gRPC: `rpc StopDaemon (StopDaemonRequest) returns (StopDaemonResponse);`
- REST: `POST /v1/proxy/stop`
- Request message: `litrpc.StopDaemonRequest`
- Response message: `litrpc.StopDaemonResponse`

Neither the request nor the response has parameters. CLI: `litcli stop`. ([source](../../raw/api/api-docs/api/lit/proxy/stop-daemon.md))

## BakeSuperMacaroon

BakeSuperMacaroon bakes a new macaroon that includes permissions for all the active daemons that LiT is connected to. ([source](../../raw/api/api-docs/api/lit/proxy/bake-super-macaroon.md))

- gRPC: `rpc BakeSuperMacaroon (BakeSuperMacaroonRequest) returns (BakeSuperMacaroonResponse);`
- REST: `POST /v1/proxy/supermacaroon`
- Request message: `litrpc.BakeSuperMacaroonRequest`
- Response message: `litrpc.BakeSuperMacaroonResponse`

Request fields: `root_key_id_suffix` (the 4-byte suffix of the root key ID that will be used to create the macaroon) and `read_only` (whether the macaroon should only contain read permissions). The response has `macaroon`, the hex encoded macaroon. ([source](../../raw/api/api-docs/api/lit/proxy/bake-super-macaroon.md))

CLI: `litcli bakesupermacaroon`, with options `--root_key_suffix` (a hex string of at most 8 characters; if not provided, a random one will be generated), `--read_only` and `--save_to` (save the returned macaroon to this file). ([source](../../raw/api/api-docs/api/lit/proxy/bake-super-macaroon.md))
