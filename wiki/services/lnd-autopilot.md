---
title: lnd autopilot service
type: service
sources:
  - raw/api/api-docs/api/lnd.md
  - raw/api/api-docs/api/lnd/rest-endpoints.md
  - raw/api/api-docs/api/lnd/autopilot/modify-status.md
  - raw/api/api-docs/api/lnd/autopilot/query-scores.md
  - raw/api/api-docs/api/lnd/autopilot/set-scores.md
  - raw/api/api-docs/api/lnd/autopilot/status.md
updated: 2026-11-14
---

# lnd autopilot service (Autopilot)

Status returns whether the daemon's autopilot agent is active. ([source](../../raw/api/api-docs/api/lnd/autopilot/status.md)) The lnd API overview lists "Automatic channel management (`autopilot`)" among the things `lnd` is capable of. ([source](../../raw/api/api-docs/api/lnd.md))

The overview lists Service *Autopilot* (file: `autopilotrpc/autopilot.proto`) among the experimental services, which are subject to change and need to be enabled with a compile-time flag (they are active in the official release binaries). The reference was generated against commit `895118ac4ec59e78b2c14f5b0d31ac6f862434bb` of `lightningnetwork/lnd`. ([source](../../raw/api/api-docs/api/lnd.md))

The REST endpoints page lists four `autopilotrpc` RPCs under `/v2/autopilot/`: ModifyStatus, SetScores, QueryScores and Status. ([source](../../raw/api/api-docs/api/lnd/rest-endpoints.md))

See also: [[lnd-lightning]], [[payment-channels]].

## Status

Status returns whether the daemon's autopilot agent is active. ([source](../../raw/api/api-docs/api/lnd/autopilot/status.md))

- gRPC: `rpc Status (StatusRequest) returns (StatusResponse);`
- REST: `GET /v2/autopilot/status`
- Request: `autopilotrpc.StatusRequest` (no parameters)
- Response: `autopilotrpc.StatusResponse`, field `active` (whether the autopilot is active or not)

([source](../../raw/api/api-docs/api/lnd/autopilot/status.md))

## ModifyStatus

ModifyStatus is used to modify the status of the autopilot agent, like enabling or disabling it. ([source](../../raw/api/api-docs/api/lnd/autopilot/modify-status.md))

- gRPC: `rpc ModifyStatus (ModifyStatusRequest) returns (ModifyStatusResponse);`
- REST: `POST /v2/autopilot/modify`
- Request: `autopilotrpc.ModifyStatusRequest`, field `enable` (whether the autopilot agent should be enabled or not)
- Response: `autopilotrpc.ModifyStatusResponse` (no parameters)

([source](../../raw/api/api-docs/api/lnd/autopilot/modify-status.md))

## QueryScores

QueryScores queries all available autopilot heuristics, in addition to any active combination of these heuristics, for the scores they would give to the given nodes. ([source](../../raw/api/api-docs/api/lnd/autopilot/query-scores.md))

- gRPC: `rpc QueryScores (QueryScoresRequest) returns (QueryScoresResponse);`
- REST: `GET /v2/autopilot/scores`
- Request: `autopilotrpc.QueryScoresRequest`, fields `pubkeys` and `ignore_local_state` (if set, local channel state is ignored when calculating scores)
- Response: `autopilotrpc.QueryScoresResponse`, field `results`, a list of `HeuristicResult` entries, each with `heuristic` and a `scores` map (`key` string, `value` double)

([source](../../raw/api/api-docs/api/lnd/autopilot/query-scores.md))

## SetScores

SetScores attempts to set the scores used by the running autopilot agent, if the external scoring heuristic is enabled. ([source](../../raw/api/api-docs/api/lnd/autopilot/set-scores.md))

- gRPC: `rpc SetScores (SetScoresRequest) returns (SetScoresResponse);`
- REST: `POST /v2/autopilot/scores`
- Request: `autopilotrpc.SetScoresRequest`, fields `heuristic` (the name of the heuristic to provide scores to) and `scores` (a map from hex-encoded public keys to scores; scores must be in the range [0.0, 1.0])
- Response: `autopilotrpc.SetScoresResponse` (no parameters)

([source](../../raw/api/api-docs/api/lnd/autopilot/set-scores.md))
