---
title: lnd watchtower service
type: service
sources:
  - raw/api/api-docs/api/lnd.md
  - raw/api/api-docs/api/lnd/rest-endpoints.md
  - raw/api/api-docs/api/lnd/watchtower/get-info.md
updated: 2026-11-14
---

# lnd watchtower service (Watchtower)

The REST endpoints page lists one `watchtowerrpc` RPC, GetInfo. ([source](../../raw/api/api-docs/api/lnd/rest-endpoints.md)) GetInfo returns general information concerning the companion watchtower, and its page gives `watchtowerrpc/watchtower.proto` as its source. ([source](../../raw/api/api-docs/api/lnd/watchtower/get-info.md))

The REST endpoints page lists one `watchtowerrpc` RPC, `watchtowerrpc.GetInfo` at `/v2/watchtower/server`. ([source](../../raw/api/api-docs/api/lnd/rest-endpoints.md))

The lnd API overview lists Service *Watchtower* (file: `watchtowerrpc/watchtower.proto`) among the experimental services, which are subject to change and need a compile-time flag to be active (they are active in the official release binaries). The reference was generated against commit `895118ac4ec59e78b2c14f5b0d31ac6f862434bb`. ([source](../../raw/api/api-docs/api/lnd.md))

See also: [[lnd-watchtower-client]], [[watchtowers]], [[lnd-watchtower-setup]].

## GetInfo

GetInfo returns general information concerning the companion watchtower, including its public key and URIs where the server is currently listening for clients. ([source](../../raw/api/api-docs/api/lnd/watchtower/get-info.md))

- gRPC: `rpc GetInfo (GetInfoRequest) returns (GetInfoResponse);`
- REST: `GET /v2/watchtower/server`
- Request: `watchtowerrpc.GetInfoRequest` (no parameters)
- Response: `watchtowerrpc.GetInfoResponse`, fields `pubkey`, `listeners` (the listening addresses) and `uris`

([source](../../raw/api/api-docs/api/lnd/watchtower/get-info.md))
