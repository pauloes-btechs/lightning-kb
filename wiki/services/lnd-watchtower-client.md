---
title: lnd watchtower-client service
type: service
sources:
  - raw/api/api-docs/api/lnd.md
  - raw/api/api-docs/api/lnd/rest-endpoints.md
  - raw/api/api-docs/api/lnd/watchtower-client/add-tower.md
  - raw/api/api-docs/api/lnd/watchtower-client/deactivate-tower.md
  - raw/api/api-docs/api/lnd/watchtower-client/get-tower-info.md
  - raw/api/api-docs/api/lnd/watchtower-client/list-towers.md
  - raw/api/api-docs/api/lnd/watchtower-client/policy.md
  - raw/api/api-docs/api/lnd/watchtower-client/remove-tower.md
  - raw/api/api-docs/api/lnd/watchtower-client/stats.md
  - raw/api/api-docs/api/lnd/watchtower-client/terminate-session.md
updated: 2026-11-14
---

# lnd watchtower-client service (WatchtowerClient)

The watchtower-client service of [[lnd]] manages the watchtowers a node backs up to and its sessions with them. Its RPC pages give `wtclientrpc/wtclient.proto` as their source. ([source](../../raw/api/api-docs/api/lnd/watchtower-client/add-tower.md))

The REST endpoints page lists eight `wtclientrpc` RPCs under `/v2/watchtower/client`: AddTower, ListTowers, GetTowerInfo, Policy, TerminateSession, Stats, DeactivateTower and RemoveTower. ([source](../../raw/api/api-docs/api/lnd/rest-endpoints.md))

The reference was generated against commit `895118ac4ec59e78b2c14f5b0d31ac6f862434bb`. ([source](../../raw/api/api-docs/api/lnd.md))

See also: [[lnd-watchtower]], [[watchtowers]], [[lnd-watchtower-setup]].

## AddTower

AddTower adds a new watchtower reachable at the given address and considers it for new sessions. If the watchtower already exists, any new addresses included will be considered when dialing it for session negotiations and backups. ([source](../../raw/api/api-docs/api/lnd/watchtower-client/add-tower.md))

- gRPC: `rpc AddTower (AddTowerRequest) returns (AddTowerResponse);`
- REST: `POST /v2/watchtower/client`
- Request: `wtclientrpc.AddTowerRequest`, fields `pubkey` and `address`
- Response: `wtclientrpc.AddTowerResponse` (no parameters)

([source](../../raw/api/api-docs/api/lnd/watchtower-client/add-tower.md))

## RemoveTower

RemoveTower removes a watchtower from being considered for future session negotiations and from being used for any subsequent backups until it's added again. If an address is provided, the RPC only removes that address from the watchtower. ([source](../../raw/api/api-docs/api/lnd/watchtower-client/remove-tower.md))

- gRPC: `rpc RemoveTower (RemoveTowerRequest) returns (RemoveTowerResponse);`
- REST: `DELETE /v2/watchtower/client/{pubkey}`
- Request: `wtclientrpc.RemoveTowerRequest`, fields `pubkey` (path) and `address` (query)
- Response: `wtclientrpc.RemoveTowerResponse` (no parameters)

([source](../../raw/api/api-docs/api/lnd/watchtower-client/remove-tower.md))

## DeactivateTower

DeactivateTower sets the given tower's status to inactive so that it is not considered for session negotiation. Its sessions will also not be used while the tower is inactive. ([source](../../raw/api/api-docs/api/lnd/watchtower-client/deactivate-tower.md))

- gRPC: `rpc DeactivateTower (DeactivateTowerRequest) returns (DeactivateTowerResponse);`
- REST: `POST /v2/watchtower/client/tower/deactivate/{pubkey}`
- Request: `wtclientrpc.DeactivateTowerRequest`, field `pubkey` (path)
- Response: `wtclientrpc.DeactivateTowerResponse`, field `status` (a string describing the action that took place)

([source](../../raw/api/api-docs/api/lnd/watchtower-client/deactivate-tower.md))

## TerminateSession

The page describes it as: "Terminate terminates the given session and marks it as terminal so that it is not used for backups anymore." ([source](../../raw/api/api-docs/api/lnd/watchtower-client/terminate-session.md))

- gRPC: `rpc TerminateSession (TerminateSessionRequest) returns (TerminateSessionResponse);`
- REST: `POST /v2/watchtower/client/sessions/terminate/{session_id}`
- Request: `wtclientrpc.TerminateSessionRequest`, field `session_id` (path)
- Response: `wtclientrpc.TerminateSessionResponse`, field `status`

([source](../../raw/api/api-docs/api/lnd/watchtower-client/terminate-session.md))

## ListTowers

ListTowers returns the list of watchtowers registered with the client. ([source](../../raw/api/api-docs/api/lnd/watchtower-client/list-towers.md))

- gRPC: `rpc ListTowers (ListTowersRequest) returns (ListTowersResponse);`
- REST: `GET /v2/watchtower/client`
- Request: `wtclientrpc.ListTowersRequest`, fields `include_sessions` and `exclude_exhausted_sessions` (only meaningful if `include_sessions` is true), both query
- Response: `wtclientrpc.ListTowersResponse`, field `towers` (`Tower[]`)

The `wtclientrpc.Tower` message has `pubkey`, `addresses`, `session_info` (`TowerSessionInfo[]`) and the deprecated `active_session_candidate`, `num_sessions` and `sessions` fields. Each `TowerSessionInfo` carries `active_session_candidate`, `num_sessions`, `sessions` and `policy_type` (`LEGACY` `0`, `ANCHOR` `1`, `TAPROOT` `2`). ([source](../../raw/api/api-docs/api/lnd/watchtower-client/list-towers.md))

## GetTowerInfo

GetTowerInfo retrieves information for a registered watchtower. ([source](../../raw/api/api-docs/api/lnd/watchtower-client/get-tower-info.md))

- gRPC: `rpc GetTowerInfo (GetTowerInfoRequest) returns (Tower);`
- REST: `GET /v2/watchtower/client/info/{pubkey}`
- Request: `wtclientrpc.GetTowerInfoRequest`, fields `pubkey` (path), `include_sessions` and `exclude_exhausted_sessions` (query)
- Response: `wtclientrpc.Tower`

Each `TowerSession` reports `num_backups`, `num_pending_backups`, `max_backups`, `sweep_sat_per_vbyte` (the fee rate the watchtower will use for the justice transaction in the event of a channel breach), the deprecated `sweep_sat_per_byte`, and `id`. ([source](../../raw/api/api-docs/api/lnd/watchtower-client/get-tower-info.md))

## Stats

Stats returns the in-memory statistics of the client since startup. ([source](../../raw/api/api-docs/api/lnd/watchtower-client/stats.md))

- gRPC: `rpc Stats (StatsRequest) returns (StatsResponse);`
- REST: `GET /v2/watchtower/client/stats`
- Request: `wtclientrpc.StatsRequest` (no parameters)
- Response: `wtclientrpc.StatsResponse`, fields `num_backups`, `num_pending_backups`, `num_failed_backups`, `num_sessions_acquired` and `num_sessions_exhausted`

([source](../../raw/api/api-docs/api/lnd/watchtower-client/stats.md))

## Policy

Policy returns the active watchtower client policy configuration. ([source](../../raw/api/api-docs/api/lnd/watchtower-client/policy.md))

- gRPC: `rpc Policy (PolicyRequest) returns (PolicyResponse);`
- REST: `GET /v2/watchtower/client/policy`
- Request: `wtclientrpc.PolicyRequest`, field `policy_type` (the client type from which to retrieve the active offering policy; query)
- Response: `wtclientrpc.PolicyResponse`, fields `max_updates` (the maximum number of updates each negotiated session should allow), `sweep_sat_per_vbyte` and the deprecated `sweep_sat_per_byte`

([source](../../raw/api/api-docs/api/lnd/watchtower-client/policy.md))
