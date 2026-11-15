---
title: taproot-assets universe service
type: service
sources:
  - raw/api/api-docs/api/taproot-assets.md
  - raw/api/api-docs/api/taproot-assets/rest-endpoints.md
  - raw/api/api-docs/api/taproot-assets/universe/info.md
  - raw/api/api-docs/api/taproot-assets/universe/multiverse-root.md
  - raw/api/api-docs/api/taproot-assets/universe/asset-roots.md
  - raw/api/api-docs/api/taproot-assets/universe/query-asset-roots.md
  - raw/api/api-docs/api/taproot-assets/universe/delete-asset-root.md
  - raw/api/api-docs/api/taproot-assets/universe/asset-leaf-keys.md
  - raw/api/api-docs/api/taproot-assets/universe/asset-leaves.md
  - raw/api/api-docs/api/taproot-assets/universe/delete-asset-leaf.md
  - raw/api/api-docs/api/taproot-assets/universe/query-proof.md
  - raw/api/api-docs/api/taproot-assets/universe/insert-proof.md
  - raw/api/api-docs/api/taproot-assets/universe/push-proof.md
  - raw/api/api-docs/api/taproot-assets/universe/sync-universe.md
  - raw/api/api-docs/api/taproot-assets/universe/sync-delta.md
  - raw/api/api-docs/api/taproot-assets/universe/list-federation-servers.md
  - raw/api/api-docs/api/taproot-assets/universe/add-federation-server.md
  - raw/api/api-docs/api/taproot-assets/universe/delete-federation-server.md
  - raw/api/api-docs/api/taproot-assets/universe/set-federation-sync-config.md
  - raw/api/api-docs/api/taproot-assets/universe/query-federation-sync-config.md
  - raw/api/api-docs/api/taproot-assets/universe/universe-stats.md
  - raw/api/api-docs/api/taproot-assets/universe/query-asset-stats.md
  - raw/api/api-docs/api/taproot-assets/universe/query-events.md
  - raw/api/api-docs/api/taproot-assets/universe/ignore-asset-out-point.md
  - raw/api/api-docs/api/taproot-assets/universe/update-supply-commit.md
  - raw/api/api-docs/api/taproot-assets/universe/fetch-supply-commit.md
  - raw/api/api-docs/api/taproot-assets/universe/fetch-supply-leaves.md
  - raw/api/api-docs/api/taproot-assets/universe/insert-supply-commit.md
updated: 2026-11-14
---

# taproot-assets universe service (Universe)

This page covers the universe service of [[taproot-assets]]. The Info page gives `universerpc/universe.proto` as the source of the RPC. ([source](../../raw/api/api-docs/api/taproot-assets/universe/info.md))

The reference was generated automatically against commit `14aa3fd90e6aace4d3b2cfc72a51d15ce4afd891` of the `lightninglabs/taproot-assets` repository. ([source](../../raw/api/api-docs/api/taproot-assets.md))

The REST endpoints page lists 26 `universerpc` RPCs, all under `/v1/taproot-assets/universe`: DeleteAssetRoot, DeleteFederationServer, AddFederationServer, ListFederationServers, Info, AssetLeafKeys, DeleteAssetLeaf, AssetLeaves, MultiverseRoot, QueryProof, InsertProof, PushProof, AssetRoots, QueryAssetRoots, UniverseStats, QueryAssetStats, QueryEvents, IgnoreAssetOutPoint, FetchSupplyLeaves, UpdateSupplyCommit, InsertSupplyCommit, FetchSupplyCommit, SyncUniverse, QueryFederationSyncConfig, SetFederationSyncConfig and SyncDelta. ([source](../../raw/api/api-docs/api/taproot-assets/rest-endpoints.md))

See also: [[tapd-mint]], [[tapd-taproot-assets]], [[tapd-universes-guide]], [[taproot-assets-protocol]].

## Shared messages

Many requests identify a universe with a `universerpc.ID`, which has `asset_id` (the 32-byte asset ID as raw bytes, gRPC only), `asset_id_str` (hex string, use this for REST), `group_key` (the 32-byte asset group key as raw bytes, gRPC only), `group_key_str` (hex string, use this for REST) and `proof_type`. `universerpc.ProofType` is one of `PROOF_TYPE_UNSPECIFIED`, `PROOF_TYPE_ISSUANCE`, `PROOF_TYPE_TRANSFER`. ([source](../../raw/api/api-docs/api/taproot-assets/universe/sync-universe.md))

A `universerpc.UniverseKey` has `id` (a `universerpc.ID`) and `leaf_key` (a `universerpc.AssetKey`); the QueryProof page describes it as composed of the Universe ID (asset_id/group_key) and a leaf key (outpoint || script_key). ([source](../../raw/api/api-docs/api/taproot-assets/universe/query-proof.md))

A `universerpc.AssetKey` has the fields `op_str`, `op`, `script_key_bytes` and `script_key_str`. ([source](../../raw/api/api-docs/api/taproot-assets/universe/asset-leaf-keys.md))

A `universerpc.AssetLeaf` has `asset` (the asset included in the leaf) and `proof` (the asset issuance or transfer proof, always an individual mint/transfer proof and never a proof file). ([source](../../raw/api/api-docs/api/taproot-assets/universe/asset-leaves.md))

A `universerpc.UniverseRoot` has `id`, `mssmt_root` (the merkle sum sparse merkle tree root associated with the universe ID), `asset_name` and `amounts_by_asset_id` (a map of hex encoded asset IDs to the number of units minted for that asset, with more than one entry only for grouped assets). ([source](../../raw/api/api-docs/api/taproot-assets/universe/asset-roots.md))

A `universerpc.MerkleSumNode` has `root_hash` (the MS-SMT root hash for the branch node) and `root_sum` (the root sum of the branch node, which represents the total known supply of the asset). ([source](../../raw/api/api-docs/api/taproot-assets/universe/insert-proof.md))

A `universerpc.UniverseFederationServer` has `host` (used to connect to the server to push proofs and sync new proofs) and `id` (the numeric ID used to identify existing servers when adding or deleting them from the federation). ([source](../../raw/api/api-docs/api/taproot-assets/universe/add-federation-server.md))

## Info

Info returns a set of information about the current state of the Universe and allows a caller to check that a universe server is reachable and configured correctly to allow proof courier access without macaroons. ([source](../../raw/api/api-docs/api/taproot-assets/universe/info.md))

- gRPC: `rpc Info (InfoRequest) returns (InfoResponse);`
- REST: `GET /v1/taproot-assets/universe/info`
- Request message: `universerpc.InfoRequest`
- Response message: `universerpc.InfoResponse`
- CLI: `tapcli universe info`

The request has no parameters. The response has `runtime_id`, a pseudo-random runtime ID for the current instance of the Universe server that changes with each restart and is mainly used to identify identical servers exposed under different hostnames/ports. ([source](../../raw/api/api-docs/api/taproot-assets/universe/info.md))

## MultiverseRoot

MultiverseRoot returns the root of the multiverse tree. This is useful to determine the equality of two multiverse trees, since the root can directly be compared to another multiverse root to find out if a sync is required. ([source](../../raw/api/api-docs/api/taproot-assets/universe/multiverse-root.md))

- gRPC: `rpc MultiverseRoot (MultiverseRootRequest) returns (MultiverseRootResponse);`
- REST: `POST /v1/taproot-assets/universe/multiverse`
- Request message: `universerpc.MultiverseRootRequest`
- Response message: `universerpc.MultiverseRootResponse`
- CLI: `tapcli universe multiverse`

Request fields: `proof_type`, the proof type to calculate the multiverse root for, and `specific_ids`, an optional list of universe IDs to include; if none are specified, all known universes of the given proof type are included, and the proof type within the IDs must either be unspecified or match `proof_type`. The response has `multiverse_root`, a `universerpc.MerkleSumNode`. The CLI option is `--proof_type`, either 'issuance' or 'transfer' (default: "issuance"). ([source](../../raw/api/api-docs/api/taproot-assets/universe/multiverse-root.md))

## AssetRoots

AssetRoots queries for the known Universe roots associated with each known asset. These roots represent the supply/audit state for each known asset. ([source](../../raw/api/api-docs/api/taproot-assets/universe/asset-roots.md))

- gRPC: `rpc AssetRoots (AssetRootRequest) returns (AssetRootResponse);`
- REST: `GET /v1/taproot-assets/universe/roots`
- Request message: `universerpc.AssetRootRequest`
- Response message: `universerpc.AssetRootResponse`
- CLI: `tapcli universe roots`

Request fields: `with_amounts_by_id` (if true, the response includes the amounts for each asset ID of grouped assets), `offset`, `limit` and `direction`. The response has `universe_roots`, a map of the known universe roots for each asset keyed by the 32-byte asset_id or group key hash, and `has_more`. The CLI options are `--asset_id`, `--group_key`, `--proof_type` (default: "issuance"), `--skip_amounts_by_id`, `--offset` (default: 0) and `--limit` (default: 512); the last three only apply if no asset ID or group key is specified. ([source](../../raw/api/api-docs/api/taproot-assets/universe/asset-roots.md))

## QueryAssetRoots

QueryAssetRoots attempts to locate the current Universe root for a specific asset. This asset can be identified by its asset ID or group key. ([source](../../raw/api/api-docs/api/taproot-assets/universe/query-asset-roots.md))

- gRPC: `rpc QueryAssetRoots (AssetRootQuery) returns (QueryRootResponse);`
- REST: `GET /v1/taproot-assets/universe/roots/asset-id/{id.asset_id_str}`
- Request message: `universerpc.AssetRootQuery`
- Response message: `universerpc.QueryRootResponse`
- CLI: `tapcli universe roots`

The request has `id`, an ID value to uniquely identify a Universe root. The response has `issuance_root` and `transfer_root`, the issuance and transfer universe roots for the given asset ID or group key. ([source](../../raw/api/api-docs/api/taproot-assets/universe/query-asset-roots.md))

## DeleteAssetRoot

DeleteAssetRoot deletes the Universe root for a specific asset, including all associated universe keys, leaves, and events. ([source](../../raw/api/api-docs/api/taproot-assets/universe/delete-asset-root.md))

- gRPC: `rpc DeleteAssetRoot (DeleteRootQuery) returns (DeleteRootResponse);`
- REST: `DELETE /v1/taproot-assets/universe/delete`
- Request message: `universerpc.DeleteRootQuery`
- Response message: `universerpc.DeleteRootResponse`
- CLI: `tapcli universe delete`

The request has `id`, an ID value to uniquely identify a Universe root. The response has no parameters. The CLI options are `--asset_id`, `--group_key` and `--proof_type` (default: "issuance"). ([source](../../raw/api/api-docs/api/taproot-assets/universe/delete-asset-root.md))

## AssetLeafKeys

AssetLeafKeys queries for the set of Universe keys associated with a given asset_id or group_key. Each key takes the form (outpoint, script_key), where outpoint is an outpoint in the Bitcoin blockchain that anchors a valid Taproot Asset commitment, and script_key is the script_key of the asset within the Taproot Asset commitment for the given asset_id or group_key. ([source](../../raw/api/api-docs/api/taproot-assets/universe/asset-leaf-keys.md))

- gRPC: `rpc AssetLeafKeys (AssetLeafKeysRequest) returns (AssetLeafKeyResponse);`
- REST: `GET /v1/taproot-assets/universe/keys/asset-id/{id.asset_id_str}`
- Request message: `universerpc.AssetLeafKeysRequest`
- Response message: `universerpc.AssetLeafKeyResponse`
- CLI: `tapcli universe keys`

Request fields: `id`, `offset`, `limit` and `direction`. The response has `asset_keys` (deprecated, superseded by `entries`, and populated for peers whose readers predate `entries`), `has_more`, and `entries`, where each `universerpc.AssetLeafEntry` pairs an `asset_key` with `leaf_node_hash`, the 32-byte MS-SMT leaf node hash committing to the leaf's content. The CLI options are `--asset_id`, `--group_key` and `--proof_type` (default: "issuance"). ([source](../../raw/api/api-docs/api/taproot-assets/universe/asset-leaf-keys.md))

## AssetLeaves

AssetLeaves queries for the set of asset leaves (the values in the Universe MS-SMT tree) for a given asset_id or group_key. These represent either asset issuance events (they have a genesis witness) or asset transfers that took place on chain. The leaves contain a normal Taproot Asset proof, as well as details for the asset. ([source](../../raw/api/api-docs/api/taproot-assets/universe/asset-leaves.md))

- gRPC: `rpc AssetLeaves (AssetLeavesRequest) returns (AssetLeafResponse);`
- REST: `GET /v1/taproot-assets/universe/leaves/asset-id/{id.asset_id_str}`
- Request message: `universerpc.AssetLeavesRequest`
- Response message: `universerpc.AssetLeafResponse`
- CLI: `tapcli universe leaves`

Request fields: `id`, `offset`, `limit` and `direction`. The response has `leaves`, the set of asset leaves for the given asset ID or group key, and `has_more`. The CLI options are `--asset_id`, `--group_key` and `--proof_type` (default: "issuance"). ([source](../../raw/api/api-docs/api/taproot-assets/universe/asset-leaves.md))

## DeleteAssetLeaf

DeleteAssetLeaf deletes a single Universe leaf, identified by its universe ID and leaf key (outpoint + script key). ([source](../../raw/api/api-docs/api/taproot-assets/universe/delete-asset-leaf.md))

- gRPC: `rpc DeleteAssetLeaf (DeleteAssetLeafRequest) returns (DeleteAssetLeafResponse);`
- REST: `DELETE /v1/taproot-assets/universe/leaf`
- Request message: `universerpc.DeleteAssetLeafRequest`
- Response message: `universerpc.DeleteAssetLeafResponse`
- CLI: `tapcli universe delete-leaf`

The request has `key`, the `universerpc.UniverseKey` identifying the leaf to delete. The response has no parameters. The CLI help adds that if it is the last leaf, the entire universe is removed; its options are `--asset_id`, `--group_key`, `--outpoint`, `--script_key` and `--proof_type` (default: "issuance"). ([source](../../raw/api/api-docs/api/taproot-assets/universe/delete-asset-leaf.md))

## QueryProof

QueryProof attempts to query for an issuance or transfer proof for a given asset based on its UniverseKey. If found, the issuance proof is returned that includes an inclusion proof to the known Universe root, as well as a Taproot Asset state transition or issuance proof for the said asset. ([source](../../raw/api/api-docs/api/taproot-assets/universe/query-proof.md))

- gRPC: `rpc QueryProof (UniverseKey) returns (AssetProofResponse);`
- REST: `GET /v1/taproot-assets/universe/proofs/asset-id/{id.asset_id_str}/{leaf_key.op.hash_str}/{leaf_key.op.index}/{leaf_key.script_key_str}`
- Request message: `universerpc.UniverseKey`
- Response message: `universerpc.AssetProofResponse`
- CLI: `tapcli universe proofs query`

The request has `id` and `leaf_key`. The response has `req` (the original request), `universe_root` (the Universe root that includes this asset leaf), `universe_inclusion_proof`, `asset_leaf`, `multiverse_root`, `multiverse_inclusion_proof` and `issuance_data` (the issuance related data for an issuance asset leaf, empty for any other type of asset leaf). The CLI options are `--asset_id`, `--group_key`, `--outpoint`, `--script_key` and `--proof_type` (default: "issuance"). ([source](../../raw/api/api-docs/api/taproot-assets/universe/query-proof.md))

## InsertProof

InsertProof attempts to insert a new issuance or transfer proof into the Universe tree specified by the UniverseKey. If valid, the proof is inserted into the database, with a new Universe root returned for the updated asset_id/group_key. ([source](../../raw/api/api-docs/api/taproot-assets/universe/insert-proof.md))

- gRPC: `rpc InsertProof (AssetProof) returns (AssetProofResponse);`
- REST: `POST /v1/taproot-assets/universe/proofs/asset-id/{key.id.asset_id_str}/{key.leaf_key.op.hash_str}/{key.leaf_key.op.index}/{key.leaf_key.script_key_str}`
- Request message: `universerpc.AssetProof`
- Response message: `universerpc.AssetProofResponse`
- CLI: `tapcli universe proofs insert`

The request has `key` (a `universerpc.UniverseKey`) and `asset_leaf`, the asset leaf to insert into the Universe tree. The response is the same `universerpc.AssetProofResponse` message that QueryProof returns. Per the CLI help, the proof can be accepted via a file argument (proof_file), via stdin, or via a hex encoded string; the options are `--asset_id`, `--group_key`, `--outpoint`, `--script_key`, `--proof_type` (default: "issuance") and `--proof_file`. ([source](../../raw/api/api-docs/api/taproot-assets/universe/insert-proof.md))

## PushProof

PushProof attempts to query the local universe for a proof specified by a UniverseKey. If found, a connection is made to a remote Universe server to attempt to upload the asset leaf. ([source](../../raw/api/api-docs/api/taproot-assets/universe/push-proof.md))

- gRPC: `rpc PushProof (PushProofRequest) returns (PushProofResponse);`
- REST: `POST /v1/taproot-assets/universe/proofs/push/asset-id/{key.id.asset_id_str}/{key.leaf_key.op.hash_str}/{key.leaf_key.op.index}/{key.leaf_key.script_key_str}`
- Request message: `universerpc.PushProofRequest`
- Response message: `universerpc.PushProofResponse`
- CLI: `tapcli universe proofs push`

The request has `key` (the ID of the asset to push the proof for) and `server` (the universe server to push the proof to). The response has `key`, the ID of the asset a push was requested for. The CLI options are `--asset_id`, `--group_key`, `--outpoint`, `--script_key`, `--proof_type` (default: "issuance"), `--universe_host` and `--server_id` (default: 0). ([source](../../raw/api/api-docs/api/taproot-assets/universe/push-proof.md))

## SyncUniverse

SyncUniverse takes host information for a remote Universe server, then attempts to synchronize either only the set of specified asset_ids, or all assets if none are specified. The sync process will attempt to query for the latest known root for each asset, performing tree based reconciliation to arrive at a new shared root. ([source](../../raw/api/api-docs/api/taproot-assets/universe/sync-universe.md))

- gRPC: `rpc SyncUniverse (SyncRequest) returns (SyncResponse);`
- REST: `POST /v1/taproot-assets/universe/sync`
- Request message: `universerpc.SyncRequest`
- Response message: `universerpc.SyncResponse`
- CLI: `tapcli universe sync`

Request fields: `universe_host`; `sync_mode`, which determines what type of proofs are synced (`SYNC_ISSUANCE_ONLY`, only new asset creation (minting) proofs, or `SYNC_FULL`, all asset proofs including normal transfers); and `sync_targets`, the set of assets to sync (all assets if none are specified). The response has `synced_universes`, each a `universerpc.SyncedUniverse` with `old_asset_root`, `new_asset_root` and `new_asset_leaves`. The CLI options are `--universe_host`, `--asset_id`, `--group_key` and `--proof_type` (default: "issuance"). ([source](../../raw/api/api-docs/api/taproot-assets/universe/sync-universe.md))

## SyncDelta

SyncDelta returns the universe leaves inserted on this server after the given sequence number, in insertion order. A federation peer that tracks a per-server cursor can fetch exactly the leaves it hasn't seen yet, instead of enumerating all leaf keys to compute a set difference. The response carries the current roots of every universe touched by the delta so the caller can verify convergence after applying it. ([source](../../raw/api/api-docs/api/taproot-assets/universe/sync-delta.md))

- gRPC: `rpc SyncDelta (SyncDeltaRequest) returns (SyncDeltaResponse);`
- REST: `GET /v1/taproot-assets/universe/sync/delta`
- Request message: `universerpc.SyncDeltaRequest`
- Response message: `universerpc.SyncDeltaResponse`

Request fields: `since_seq` (return leaves inserted after this sequence number; zero means from the beginning) and `page_size` (the maximum number of leaves to return in one response, clamped server-side; callers should page until a response returns fewer items than requested and `latest_seq` stops advancing). The response has `items` (leaves whose universes have proof export disabled are omitted, but still advance `latest_seq`), `universe_roots` (the current roots of every universe that appears in items) and `latest_seq` (the cursor value the caller should persist once the page's items are applied and verified). Each `universerpc.SyncDeltaItem` has `universe_id`, `key`, `leaf`, `universe_inclusion_proof` and `seq`. The page shows no `tapcli` command for this RPC. ([source](../../raw/api/api-docs/api/taproot-assets/universe/sync-delta.md))

## ListFederationServers

ListFederationServers lists the set of servers that make up the federation of the local Universe server. These servers are used to push out new proofs, and also to periodically sync new proofs from the remote server. ([source](../../raw/api/api-docs/api/taproot-assets/universe/list-federation-servers.md))

- gRPC: `rpc ListFederationServers (ListFederationServersRequest) returns (ListFederationServersResponse);`
- REST: `GET /v1/taproot-assets/universe/federation`
- Request message: `universerpc.ListFederationServersRequest`
- Response message: `universerpc.ListFederationServersResponse`
- CLI: `tapcli universe federation list`

The request has no parameters. The response has `servers`, the list of federation servers that make up the local Universe federation. ([source](../../raw/api/api-docs/api/taproot-assets/universe/list-federation-servers.md))

## AddFederationServer

AddFederationServer adds a new server to the federation of the local Universe server. Once a server is added, this call can also optionally be used to trigger a sync of the remote server. ([source](../../raw/api/api-docs/api/taproot-assets/universe/add-federation-server.md))

- gRPC: `rpc AddFederationServer (AddFederationServerRequest) returns (AddFederationServerResponse);`
- REST: `POST /v1/taproot-assets/universe/federation`
- Request message: `universerpc.AddFederationServerRequest`
- Response message: `universerpc.AddFederationServerResponse`
- CLI: `tapcli universe federation add`

The request has `servers`, a list of `universerpc.UniverseFederationServer`. The response has no parameters. Per the CLI help, newly added servers will be synced automatically and will also be used to push out newly validated proofs; the option is `--universe_host`, the address for the universe server, eg: testnet.mydomain.com:10029, and the default port (10029) is used if none is provided. ([source](../../raw/api/api-docs/api/taproot-assets/universe/add-federation-server.md))

## DeleteFederationServer

DeleteFederationServer removes a server from the federation of the local Universe server. ([source](../../raw/api/api-docs/api/taproot-assets/universe/delete-federation-server.md))

- gRPC: `rpc DeleteFederationServer (DeleteFederationServerRequest) returns (DeleteFederationServerResponse);`
- REST: `DELETE /v1/taproot-assets/universe/federation`
- Request message: `universerpc.DeleteFederationServerRequest`
- Response message: `universerpc.DeleteFederationServerResponse`
- CLI: `tapcli universe federation del`

The request has `servers`, a list of `universerpc.UniverseFederationServer`. The response has no parameters. Per the CLI help, servers can be identified either via their ID or the server host; the options are `--universe_host` and `--server_id` (default: 0). ([source](../../raw/api/api-docs/api/taproot-assets/universe/delete-federation-server.md))

## SetFederationSyncConfig

SetFederationSyncConfig sets the configuration of the universe federation sync. ([source](../../raw/api/api-docs/api/taproot-assets/universe/set-federation-sync-config.md))

- gRPC: `rpc SetFederationSyncConfig (SetFederationSyncConfigRequest) returns (SetFederationSyncConfigResponse);`
- REST: `POST /v1/taproot-assets/universe/sync/config`
- Request message: `universerpc.SetFederationSyncConfigRequest`
- Response message: `universerpc.SetFederationSyncConfigResponse`

Request fields: `global_sync_configs`, the global federation sync configs for the given proof types (each `universerpc.GlobalFederationSyncConfig` has `proof_type`, `allow_sync_insert` and `allow_sync_export`), and `asset_sync_configs`, the asset federation sync configs for the given universe IDs (each `universerpc.AssetFederationSyncConfig` has `id`, `allow_sync_insert` and `allow_sync_export`). `allow_sync_insert` indicates whether leaves may be inserted via federation sync and `allow_sync_export` whether they may be exported via federation sync. The response has no parameters. The page shows no `tapcli` command for this RPC. ([source](../../raw/api/api-docs/api/taproot-assets/universe/set-federation-sync-config.md))

## QueryFederationSyncConfig

QueryFederationSyncConfig queries the universe federation sync configuration settings. ([source](../../raw/api/api-docs/api/taproot-assets/universe/query-federation-sync-config.md))

- gRPC: `rpc QueryFederationSyncConfig (QueryFederationSyncConfigRequest) returns (QueryFederationSyncConfigResponse);`
- REST: `GET /v1/taproot-assets/universe/sync/config`
- Request message: `universerpc.QueryFederationSyncConfigRequest`
- Response message: `universerpc.QueryFederationSyncConfigResponse`
- CLI: `tapcli universe federation config info`

The request has `id`, the target universe ID(s). The response has `global_sync_configs` and `asset_sync_configs`. Per the CLI help, the settings are defined by the proof type (issuance or transfer), the sync behavior (insert from remote Universe or export to remote Universe), and the scope (all assets or specific assets); the options are `--config_scope` (global or local), `--asset_id` and `--group_key`. ([source](../../raw/api/api-docs/api/taproot-assets/universe/query-federation-sync-config.md))

## UniverseStats

UniverseStats returns a set of aggregate statistics for the current state of the Universe. Stats returned include: total number of syncs, total number of proofs, and total number of known assets. ([source](../../raw/api/api-docs/api/taproot-assets/universe/universe-stats.md))

- gRPC: `rpc UniverseStats (StatsRequest) returns (StatsResponse);`
- REST: `GET /v1/taproot-assets/universe/stats`
- Request message: `universerpc.StatsRequest`
- Response message: `universerpc.StatsResponse`
- CLI: `tapcli universe stats`

The request has no parameters. The response fields are `num_total_assets`, `num_total_groups`, `num_total_syncs` and `num_total_proofs`. The CLI help lists the subcommands `assets, a` and `events, e`. ([source](../../raw/api/api-docs/api/taproot-assets/universe/universe-stats.md))

## QueryAssetStats

QueryAssetStats returns a set of statistics for a given set of assets. Stats can be queried for all assets, or based on the asset ID, name, or asset type. Pagination is supported via the offset and limit params, and results can be sorted based on any of the main query params. ([source](../../raw/api/api-docs/api/taproot-assets/universe/query-asset-stats.md))

- gRPC: `rpc QueryAssetStats (AssetStatsQuery) returns (UniverseAssetStats);`
- REST: `GET /v1/taproot-assets/universe/stats/assets`
- Request message: `universerpc.AssetStatsQuery`
- Response message: `universerpc.UniverseAssetStats`
- CLI: `tapcli universe stats assets`

Request fields: `asset_name_filter`, `asset_id_filter`, `asset_type_filter` (`FILTER_ASSET_NONE`, `FILTER_ASSET_NORMAL`, `FILTER_ASSET_COLLECTIBLE`), `sort_by` (`SORT_BY_NONE`, `SORT_BY_ASSET_NAME`, `SORT_BY_ASSET_ID`, `SORT_BY_ASSET_TYPE`, `SORT_BY_TOTAL_SYNCS`, `SORT_BY_TOTAL_PROOFS`, `SORT_BY_GENESIS_HEIGHT`, `SORT_BY_TOTAL_SUPPLY`), `offset`, `limit` and `direction`. The response has `asset_stats` and `has_more`; each `universerpc.AssetStatsSnapshot` has `group_key`, `group_supply`, `group_anchor`, `asset`, `total_syncs` and `total_proofs`. The CLI options are `--asset_name`, `--asset_type`, `--asset_id`, `--sort_by` (`[--sort_by=asset_name|asset_type|asset_id]`), `--limit` (default: 0) and `--offset` (default: 0). ([source](../../raw/api/api-docs/api/taproot-assets/universe/query-asset-stats.md))

## QueryEvents

QueryEvents returns the number of sync and proof events for a given time period, grouped by day. ([source](../../raw/api/api-docs/api/taproot-assets/universe/query-events.md))

- gRPC: `rpc QueryEvents (QueryEventsRequest) returns (QueryEventsResponse);`
- REST: `GET /v1/taproot-assets/universe/stats/events`
- Request message: `universerpc.QueryEventsRequest`
- Response message: `universerpc.QueryEventsResponse`
- CLI: `tapcli universe stats events`

Request fields: `start_timestamp` and `end_timestamp`, both in Unix epoch time (seconds). The response has `events`, where each `universerpc.GroupedUniverseEvents` entry represents a day with `date` (formatted as YYYY-MM-DD), `sync_events` and `new_proof_events`. The CLI options are `--start_time` (optional; if not specified, queries from the last 30 days by default) and `--offset` (optional; described as the unix timestamp to end querying from, and if not specified, queries until now by default). ([source](../../raw/api/api-docs/api/taproot-assets/universe/query-events.md))

## IgnoreAssetOutPoint

IgnoreAssetOutPoint allows an asset issuer to mark a specific asset outpoint as ignored. An ignored outpoint will be included in the next universe supply commitment transaction that is published. ([source](../../raw/api/api-docs/api/taproot-assets/universe/ignore-asset-out-point.md))

- gRPC: `rpc IgnoreAssetOutPoint (IgnoreAssetOutPointRequest) returns (IgnoreAssetOutPointResponse);`
- REST: `POST /v1/taproot-assets/universe/supply/ignore`
- Request message: `universerpc.IgnoreAssetOutPointRequest`
- Response message: `universerpc.IgnoreAssetOutPointResponse`

Request fields: `asset_out_point`, the outpoint of the asset to ignore (a `taprpc.AssetOutPoint` with `anchor_out_point`, `asset_id` and `script_key`), and `amount`, the amount of asset units at the associated asset outpoint. The response has `leaf_key`, the key identifying the signed ignore outpoint leaf in the ignore supply commitment subtree, and `leaf`, the signed ignore outpoint leaf itself. The page shows no `tapcli` command for this RPC. ([source](../../raw/api/api-docs/api/taproot-assets/universe/ignore-asset-out-point.md))

## UpdateSupplyCommit

UpdateSupplyCommit updates the on-chain supply commitment for a specific asset group. ([source](../../raw/api/api-docs/api/taproot-assets/universe/update-supply-commit.md))

- gRPC: `rpc UpdateSupplyCommit (UpdateSupplyCommitRequest) returns (UpdateSupplyCommitResponse);`
- REST: `POST /v1/taproot-assets/universe/supply/update/{group_key_str}`
- Request message: `universerpc.UpdateSupplyCommitRequest`
- Response message: `universerpc.UpdateSupplyCommitResponse`

Request fields: `group_key_bytes`, the 32-byte asset group key as raw bytes (gRPC only), and `group_key_str`, the same key encoded as hex string (use this for REST). The response has no parameters. The page shows no `tapcli` command for this RPC. ([source](../../raw/api/api-docs/api/taproot-assets/universe/update-supply-commit.md))

## FetchSupplyCommit

FetchSupplyCommit fetches the on-chain supply commitment for a specific asset group. ([source](../../raw/api/api-docs/api/taproot-assets/universe/fetch-supply-commit.md))

- gRPC: `rpc FetchSupplyCommit (FetchSupplyCommitRequest) returns (FetchSupplyCommitResponse);`
- REST: `GET /v1/taproot-assets/universe/supply/{group_key_str}`
- Request message: `universerpc.FetchSupplyCommitRequest`
- Response message: `universerpc.FetchSupplyCommitResponse`

Request fields:

- `group_key_bytes` / `group_key_str`: the 32-byte asset group key as raw bytes (gRPC only) or hex string (use this for REST).
- `commit_outpoint`: fetch the supply commitment that created this new commitment output on chain.
- `spent_commit_outpoint`: fetch the supply commitment that spent the specified commitment output on chain to create a new supply commitment; this can be used to traverse the chain of supply commitments.
- `very_first`: fetch the very first supply commitment for the asset group, the one that spent the pre-commitment output of the very first asset mint of a grouped asset (also known as the group anchor).
- `latest`: fetch the latest supply commitment for the asset group, the most recent one anchored on chain.

([source](../../raw/api/api-docs/api/taproot-assets/universe/fetch-supply-commit.md))

Response fields: `chain_data` (a `universerpc.SupplyCommitChainData` holding both the commitment and chain proof information), `tx_chain_fees_sats`, `issuance_subtree_root`, `burn_subtree_root`, `ignore_subtree_root`, `issuance_leaves`, `burn_leaves`, `ignore_leaves` (each only the leaves added by this supply commitment), `total_outstanding_supply` (after applying all the supply changes included in this supply commitment), `spent_commitment_outpoint` (must be set unless this is the very first supply commitment of a grouped asset) and `block_headers` (a map of block height to supply leaf block header). The page shows no `tapcli` command for this RPC. ([source](../../raw/api/api-docs/api/taproot-assets/universe/fetch-supply-commit.md))

## FetchSupplyLeaves

FetchSupplyLeaves fetches the supply leaves for a specific asset group within a specified block height range. The leaves include issuance, burn, and ignore leaves, which represent the supply changes for the asset group. ([source](../../raw/api/api-docs/api/taproot-assets/universe/fetch-supply-leaves.md))

- gRPC: `rpc FetchSupplyLeaves (FetchSupplyLeavesRequest) returns (FetchSupplyLeavesResponse);`
- REST: `GET /v1/taproot-assets/universe/supply/leaves/{group_key_str}`
- Request message: `universerpc.FetchSupplyLeavesRequest`
- Response message: `universerpc.FetchSupplyLeavesResponse`

Request fields: `group_key_bytes`, `group_key_str`, `block_height_start`, `block_height_end`, and the optional `issuance_leaf_keys`, `burn_leaf_keys` and `ignore_leaf_keys`; for each key in those lists the endpoint generates and returns an inclusion proof. The response has `issuance_leaves`, `burn_leaves`, `ignore_leaves`, `issuance_leaf_inclusion_proofs`, `burn_leaf_inclusion_proofs`, `ignore_leaf_inclusion_proofs` (each entry corresponds to the key at the same index in the matching request list) and `block_headers`. The page shows no `tapcli` command for this RPC. ([source](../../raw/api/api-docs/api/taproot-assets/universe/fetch-supply-leaves.md))

## InsertSupplyCommit

InsertSupplyCommit inserts a supply commitment for a specific asset group. This includes the commitment details, supply leaves (issuance, burn, and ignore), and chain proof that proves the commitment has been mined. ([source](../../raw/api/api-docs/api/taproot-assets/universe/insert-supply-commit.md))

- gRPC: `rpc InsertSupplyCommit (InsertSupplyCommitRequest) returns (InsertSupplyCommitResponse);`
- REST: `POST /v1/taproot-assets/universe/supply/{group_key_str}`
- Request message: `universerpc.InsertSupplyCommitRequest`
- Response message: `universerpc.InsertSupplyCommitResponse`

Request fields: `group_key_bytes`, `group_key_str`, `chain_data` (the supply commitment chain data that contains both the commitment and chain proof information), `spent_commitment_outpoint` (must be set unless this is the very first supply commitment of a grouped asset), `issuance_leaves`, `burn_leaves` and `ignore_leaves`. The response has no parameters. The page shows no `tapcli` command for this RPC. ([source](../../raw/api/api-docs/api/taproot-assets/universe/insert-supply-commit.md))

## Notes

Writer's observations, not statements from the sources:

- The `tapcli universe stats` help text refers to a "'universe stats asset' sub-command", while the same help lists the subcommand as `assets, a`.
- The `tapcli universe stats events` option that sets the end of the queried period is named `--offset`, while the RPC field is `end_timestamp`.
