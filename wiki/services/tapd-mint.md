---
title: taproot-assets mint service
type: service
sources:
  - raw/api/api-docs/api/taproot-assets.md
  - raw/api/api-docs/api/taproot-assets/rest-endpoints.md
  - raw/api/api-docs/api/taproot-assets/mint/mint-asset.md
  - raw/api/api-docs/api/taproot-assets/mint/fund-batch.md
  - raw/api/api-docs/api/taproot-assets/mint/seal-batch.md
  - raw/api/api-docs/api/taproot-assets/mint/finalize-batch.md
  - raw/api/api-docs/api/taproot-assets/mint/cancel-batch.md
  - raw/api/api-docs/api/taproot-assets/mint/list-batches.md
  - raw/api/api-docs/api/taproot-assets/mint/subscribe-mint-events.md
updated: 2026-11-14
---

# taproot-assets mint service (Mint)

This page covers the mint service of [[taproot-assets]]. The MintAsset page gives `mintrpc/mint.proto` as the source of the RPC. ([source](../../raw/api/api-docs/api/taproot-assets/mint/mint-asset.md))

The reference was generated automatically against commit `14aa3fd90e6aace4d3b2cfc72a51d15ce4afd891` of the `lightninglabs/taproot-assets` repository. ([source](../../raw/api/api-docs/api/taproot-assets.md))

The REST endpoints page lists seven `mintrpc` RPCs: MintAsset, ListBatches, CancelBatch, FinalizeBatch, FundBatch, SealBatch and SubscribeMintEvents. ([source](../../raw/api/api-docs/api/taproot-assets/rest-endpoints.md))

See also: [[tapd-universe]], [[tapd-taproot-assets]], [[minting-taproot-assets]], [[taproot-assets-protocol]].

## MintAsset

MintAsset will attempt to mint the set of assets (async by default to ensure proper batching) specified in the request. The pending batch is returned that shows the other pending assets that are part of the next batch. The call blocks until the operation succeeds (asset is staged in the batch) or fails. ([source](../../raw/api/api-docs/api/taproot-assets/mint/mint-asset.md))

- gRPC: `rpc MintAsset (MintAssetRequest) returns (MintAssetResponse);`
- REST: `POST /v1/taproot-assets/assets`
- Request message: `mintrpc.MintAssetRequest`
- Response message: `mintrpc.MintAssetResponse`
- CLI: `tapcli assets mint`

The request has `asset` (a `mintrpc.MintAsset`, the asset to be minted) and `short_response` (if true, the assets currently in the batch are not returned in the response). The response has `pending_batch`, a `mintrpc.MintingBatch`: the pending batch the asset was added to. ([source](../../raw/api/api-docs/api/taproot-assets/mint/mint-asset.md))

Fields of `mintrpc.MintAsset`:

- `asset_version`: the version of asset to mint (`ASSET_VERSION_V0`, the default, or `ASSET_VERSION_V1`).
- `asset_type`: the type of the asset to be created (`NORMAL` or `COLLECTIBLE`).
- `name`: the name, or "tag" of the asset; this will affect the final asset ID.
- `asset_meta`: a `taprpc.AssetMeta` blob of metadata; this will affect the final asset ID. Its `data` is limited to 1MiB and its `type` is `META_TYPE_OPAQUE` or `META_TYPE_JSON`.
- `amount`: the total amount of units of the new asset; cannot be set if the AssetType is Collectible.
- `new_grouped_asset`: if true, the asset is created with a group key, which allows for future asset issuance.
- `grouped_asset`: if true, a group key or group anchor can be set to mint this asset into an existing asset group.
- `group_key`: the specific existing group key this asset should be minted with.
- `group_anchor`: the name of the asset in the batch that will anchor a new asset group; this asset is minted with the same group key as the anchor asset.
- `group_internal_key`: optional key used as the internal key for an asset group created with this asset. If set, `external_group_key` must be unset, and vice versa.
- `group_tapscript_root`: optional root of a Tapscript tree used when constructing a new asset group key, allowing future issuance authorized using a script witness. If an external group key is provided, the V1 scheme for group key script construction is used, which supports PSBT signing, and the final Tapscript root will differ from the one specified.
- `script_key`: optional script key for the new asset. If none is given, a BIP-86 key is derived from the underlying wallet.
- `decimal_display`: the number of decimal places to shift the amount to the left for display (with a value of 2 and 100 units, a wallet would display "1.00"). It has no impact on the behavior of the daemon or the protocol, is encoded in the MetaData field as a JSON field, and is therefore only compatible with assets that have a JSON MetaData field.
- `external_group_key`: optional `taprpc.ExternalKey` (`xpub`, `master_fingerprint`, `derivation_path`) specifying an external signing key for the group virtual transaction during minting.
- `enable_supply_commitments`: enables the supply commitments feature for a new asset group. When enabled, the batch must be a single asset group, and it is valid only for creating a new asset group (the first minting tranche).

([source](../../raw/api/api-docs/api/taproot-assets/mint/mint-asset.md))

`tapcli assets mint` takes these options: `--type` (must be either normal or collectible), `--name`, `--supply` (default: 0), `--decimal_display` (default: 0), `--asset_version` (default: 0), `--meta_bytes`, `--meta_file_path`, `--meta_type` (opaque or json, default: "opaque"), `--new_grouped_asset`, `--grouped_asset`, `--group_key`, `--group_anchor`, `--short`, `--group_key_xpub`, `--group_key_derivation_path`, `--group_key_fingerprint` and `--enable_supply_commitments`. Its help lists the subcommands `batches, b`, `fund`, `finalize` and `cancel, c`. ([source](../../raw/api/api-docs/api/taproot-assets/mint/mint-asset.md))

## FundBatch

FundBatch will attempt to fund the current pending batch with a genesis input, or create a new funded batch if no batch exists yet. This RPC is only needed if a custom witness is needed to finalize the batch; otherwise FinalizeBatch can be called directly. ([source](../../raw/api/api-docs/api/taproot-assets/mint/fund-batch.md))

- gRPC: `rpc FundBatch (FundBatchRequest) returns (FundBatchResponse);`
- REST: `POST /v1/taproot-assets/assets/mint/fund`
- Request message: `mintrpc.FundBatchRequest`
- Response message: `mintrpc.FundBatchResponse`
- CLI: tapcli `assets mint fund`

Request fields: `short_response`; `fee_rate`, the optional fee rate to use for the minting transaction, in sat/kw; `full_tree`, an ordered list of TapLeafs used to construct a Tapscript tree; and `branch`, a TapBranch that represents a Tapscript tree managed externally. The response has `batch`, the funded batch as a `mintrpc.VerboseBatch`, which holds `batch` (the minting batch, without any assets) and `unsealed_assets` (each a `mintrpc.UnsealedAsset` with `asset`, `group_key_request`, `group_virtual_tx` and `group_virtual_psbt`). ([source](../../raw/api/api-docs/api/taproot-assets/mint/fund-batch.md))

## SealBatch

SealBatch will attempt to seal the current pending batch by creating and validating asset group witness for all assets in the batch. If a witness is not provided, a signature will be derived to serve as the witness. This RPC is only needed if any assets in the batch have a custom asset group key that require an external signer; otherwise FinalizeBatch can be called directly. ([source](../../raw/api/api-docs/api/taproot-assets/mint/seal-batch.md))

- gRPC: `rpc SealBatch (SealBatchRequest) returns (SealBatchResponse);`
- REST: `POST /v1/taproot-assets/assets/mint/seal`
- Request message: `mintrpc.SealBatchRequest`
- Response message: `mintrpc.SealBatchResponse`
- CLI: tapcli `assets mint seal`

Request fields: `short_response`; `group_witnesses`, the assetID, witness pairs that authorize asset membership in a group (each `taprpc.GroupWitness` has `genesis_id` and `witness`); and `signed_group_virtual_psbts`, the base64 encoded signed group virtual PSBTs. `group_witnesses` and `signed_group_virtual_psbts` should not be used in conjunction; use one or the other. The response has `batch`, the sealed batch as a `mintrpc.MintingBatch`. ([source](../../raw/api/api-docs/api/taproot-assets/mint/seal-batch.md))

## FinalizeBatch

FinalizeBatch will attempt to finalize the current pending batch. ([source](../../raw/api/api-docs/api/taproot-assets/mint/finalize-batch.md))

- gRPC: `rpc FinalizeBatch (FinalizeBatchRequest) returns (FinalizeBatchResponse);`
- REST: `POST /v1/taproot-assets/assets/mint/finalize`
- Request message: `mintrpc.FinalizeBatchRequest`
- Response message: `mintrpc.FinalizeBatchResponse`
- CLI: `tapcli assets mint finalize`

Request fields: `short_response`; `fee_rate`, the optional fee rate to use for the minting transaction, in sat/kw; `full_tree`, an ordered list of TapLeafs used to construct a Tapscript tree; and `branch`, a TapBranch that represents a Tapscript tree managed externally. The response has `batch`, the finalized batch as a `mintrpc.MintingBatch`. The CLI options are `--short` and `--sat_per_vbyte`, the fee rate in sat/vB to use for the minting transaction (default: 0). ([source](../../raw/api/api-docs/api/taproot-assets/mint/finalize-batch.md))

Fields of `mintrpc.MintingBatch`:

- `batch_key`: a public key serialized in compressed format that uniquely identifies a pending minting batch. Responses that share the same key will be batched into the same minting transaction.
- `batch_txid`: the transaction ID of the batch; only populated if the batch has been committed.
- `state`: a `mintrpc.BatchState`, one of `BATCH_STATE_UNKNOWN`, `BATCH_STATE_PENDING`, `BATCH_STATE_FROZEN`, `BATCH_STATE_COMMITTED`, `BATCH_STATE_BROADCAST`, `BATCH_STATE_CONFIRMED`, `BATCH_STATE_FINALIZED`, `BATCH_STATE_SEEDLING_CANCELLED`, `BATCH_STATE_SPROUT_CANCELLED`.
- `assets`: the assets that are part of the batch, as `mintrpc.PendingAsset` entries.
- `created_at`: the time the batch was created as a Unix timestamp (in seconds).
- `height_hint`: the current height of the block chain at the time of the batch creation.
- `batch_psbt`: the genesis transaction as a PSBT packet; only populated if the batch has been committed.

([source](../../raw/api/api-docs/api/taproot-assets/mint/finalize-batch.md))

## CancelBatch

CancelBatch will attempt to cancel the current pending batch. ([source](../../raw/api/api-docs/api/taproot-assets/mint/cancel-batch.md))

- gRPC: `rpc CancelBatch (CancelBatchRequest) returns (CancelBatchResponse);`
- REST: `POST /v1/taproot-assets/assets/mint/cancel`
- Request message: `mintrpc.CancelBatchRequest`
- Response message: `mintrpc.CancelBatchResponse`
- CLI: `tapcli assets mint cancel`

The request has no parameters. The response has `batch_key`, the internal public key of the batch. ([source](../../raw/api/api-docs/api/taproot-assets/mint/cancel-batch.md))

## ListBatches

ListBatches lists the set of batches submitted to the daemon, including pending and cancelled batches. ([source](../../raw/api/api-docs/api/taproot-assets/mint/list-batches.md))

- gRPC: `rpc ListBatches (ListBatchRequest) returns (ListBatchResponse);`
- REST: `GET /v1/taproot-assets/assets/mint/batches/{batch_key}`
- Request message: `mintrpc.ListBatchRequest`
- Response message: `mintrpc.ListBatchResponse`
- CLI: `tapcli assets mint batches`

Request fields: `batch_key`, the optional batch key of the batch to list as raw bytes (gRPC only); `batch_key_str`, the same key as a hex encoded string (use this for REST); and `verbose`, which if true includes pending asset group details for any funded, non-empty pending batch, while unfunded or empty batches are excluded. The response has `batches`, a list of `mintrpc.VerboseBatch`. The CLI options are `--batch_key` and `--verbose`. ([source](../../raw/api/api-docs/api/taproot-assets/mint/list-batches.md))

## SubscribeMintEvents

SubscribeMintEvents allows a caller to subscribe to mint events for asset creation batches. It is a server-streaming RPC. ([source](../../raw/api/api-docs/api/taproot-assets/mint/subscribe-mint-events.md))

- gRPC: `rpc SubscribeMintEvents (SubscribeMintEventsRequest) returns (stream MintEvent);`
- REST: `POST /v1/taproot-assets/events/asset-mint`
- Request message: `mintrpc.SubscribeMintEventsRequest`
- Response message: `mintrpc.MintEvent` (stream)
- CLI: `tapcli events mint`

The request has `short_response`: if true, the assets currently in the batch are not returned in the event's batch. Each `mintrpc.MintEvent` has `timestamp` (execute timestamp, Unix timestamp in microseconds), `batch_state` (the last state of the batch that was successfully executed; if `error` is set, it is the state that lead to the error during its execution), `batch` (the batch that the event is for) and `error` (an optional error, indicating that executing the batch_state failed). The CLI command blocks until aborted manually by hitting Ctrl+C and has one option, `--short`. ([source](../../raw/api/api-docs/api/taproot-assets/mint/subscribe-mint-events.md))

## Conflicts

- The SealBatch page gives its CLI command as tapcli `assets mint seal` ([source](../../raw/api/api-docs/api/taproot-assets/mint/seal-batch.md)), but the `tapcli assets mint --help` output on the MintAsset page lists only the subcommands `batches, b`, `fund`, `finalize` and `cancel, c`, with no `seal` ([source](../../raw/api/api-docs/api/taproot-assets/mint/mint-asset.md)).
