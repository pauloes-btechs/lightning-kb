---
title: lnd versioner service
type: service
sources:
  - raw/api/api-docs/api/lnd.md
  - raw/api/api-docs/api/lnd/rest-endpoints.md
  - raw/api/api-docs/api/lnd/versioner/get-version.md
updated: 2026-11-14
---

# lnd versioner service (Versioner)

The REST endpoints page lists one `verrpc` RPC, GetVersion. ([source](../../raw/api/api-docs/api/lnd/rest-endpoints.md)) Its page gives `verrpc/verrpc.proto` as its source. ([source](../../raw/api/api-docs/api/lnd/versioner/get-version.md))

The REST endpoints page lists one `verrpc` RPC, `verrpc.GetVersion` at `/v2/versioner/version`. ([source](../../raw/api/api-docs/api/lnd/rest-endpoints.md))

The reference was generated against commit `895118ac4ec59e78b2c14f5b0d31ac6f862434bb`. ([source](../../raw/api/api-docs/api/lnd.md))

See also: [[lnd-state]], [[lnd-lightning]].

## GetVersion

GetVersion returns the current version and build information of the running daemon. ([source](../../raw/api/api-docs/api/lnd/versioner/get-version.md))

- gRPC: `rpc GetVersion (VersionRequest) returns (Version);`
- REST: `GET /v2/versioner/version`
- Request: `verrpc.VersionRequest` (no parameters)
- Response: `verrpc.Version`, fields `commit`, `commit_hash` (the SHA1 commit hash the daemon is compiled with), `version` (the semantic version), `app_major`, `app_minor`, `app_patch`, `app_pre_release`, `build_tags` (build tags supplied during compilation) and `go_version`

([source](../../raw/api/api-docs/api/lnd/versioner/get-version.md))
