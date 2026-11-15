---
title: taproot-assets asset-wallet service
type: service
sources:
  - raw/api/api-docs/api/taproot-assets.md
  - raw/api/api-docs/api/taproot-assets/rest-endpoints.md
  - raw/api/api-docs/api/taproot-assets/asset-wallet/fund-virtual-psbt.md
  - raw/api/api-docs/api/taproot-assets/asset-wallet/sign-virtual-psbt.md
  - raw/api/api-docs/api/taproot-assets/asset-wallet/anchor-virtual-psbts.md
  - raw/api/api-docs/api/taproot-assets/asset-wallet/commit-virtual-psbts.md
  - raw/api/api-docs/api/taproot-assets/asset-wallet/publish-and-log-transfer.md
  - raw/api/api-docs/api/taproot-assets/asset-wallet/next-internal-key.md
  - raw/api/api-docs/api/taproot-assets/asset-wallet/next-script-key.md
  - raw/api/api-docs/api/taproot-assets/asset-wallet/query-internal-key.md
  - raw/api/api-docs/api/taproot-assets/asset-wallet/query-script-key.md
  - raw/api/api-docs/api/taproot-assets/asset-wallet/prove-asset-ownership.md
  - raw/api/api-docs/api/taproot-assets/asset-wallet/verify-asset-ownership.md
  - raw/api/api-docs/api/taproot-assets/asset-wallet/remove-u-t-x-o-lease.md
  - raw/api/api-docs/api/taproot-assets/asset-wallet/declare-script-key.md
  - raw/api/api-docs/api/taproot-assets/asset-wallet/export-asset-wallet-backup.md
  - raw/api/api-docs/api/taproot-assets/asset-wallet/import-assets-from-backup.md
updated: 2026-11-14
---

# taproot-assets asset-wallet service

The asset-wallet service is a gRPC service in the API reference of [[taproot-assets]]. The Taproot Assets overview page lists `assetwalletrpc/assetwallet.proto` among the `*.proto` files from which the gRPC documentation was generated, and says the reference was generated automatically against commit `14aa3fd90e6aace4d3b2cfc72a51d15ce4afd891` of the `lightninglabs/taproot-assets` repository. ([source](../../raw/api/api-docs/api/taproot-assets.md)) The "Source:" link on each RPC page of this service names `assetwalletrpc/assetwallet.proto`, and the request message on each page carries the `assetwalletrpc.` prefix. ([source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/fund-virtual-psbt.md), [source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/sign-virtual-psbt.md), [source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/anchor-virtual-psbts.md), [source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/commit-virtual-psbts.md), [source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/publish-and-log-transfer.md), [source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/next-internal-key.md), [source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/next-script-key.md), [source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/query-internal-key.md), [source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/query-script-key.md), [source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/prove-asset-ownership.md), [source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/verify-asset-ownership.md), [source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/remove-u-t-x-o-lease.md), [source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/declare-script-key.md), [source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/export-asset-wallet-backup.md), [source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/import-assets-from-backup.md))

The reference has fifteen RPCs for this service: FundVirtualPsbt, SignVirtualPsbt, AnchorVirtualPsbts, CommitVirtualPsbts, PublishAndLogTransfer, NextInternalKey, NextScriptKey, QueryInternalKey, QueryScriptKey, ProveAssetOwnership, VerifyAssetOwnership, RemoveUTXOLease, DeclareScriptKey, ExportAssetWalletBackup, ImportAssetsFromBackup. ([source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/fund-virtual-psbt.md), [source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/sign-virtual-psbt.md), [source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/anchor-virtual-psbts.md), [source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/commit-virtual-psbts.md), [source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/publish-and-log-transfer.md), [source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/next-internal-key.md), [source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/next-script-key.md), [source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/query-internal-key.md), [source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/query-script-key.md), [source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/prove-asset-ownership.md), [source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/verify-asset-ownership.md), [source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/remove-u-t-x-o-lease.md), [source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/declare-script-key.md), [source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/export-asset-wallet-backup.md), [source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/import-assets-from-backup.md))

Every one of these RPC pages has a REST section, and the REST Endpoints page lists the same paths under `/v1/taproot-assets/` against the `assetwalletrpc.` RPC names. ([source](../../raw/api/api-docs/api/taproot-assets/rest-endpoints.md), [source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/fund-virtual-psbt.md), [source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/sign-virtual-psbt.md), [source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/anchor-virtual-psbts.md), [source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/commit-virtual-psbts.md), [source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/publish-and-log-transfer.md), [source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/next-internal-key.md), [source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/next-script-key.md), [source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/query-internal-key.md), [source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/query-script-key.md), [source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/prove-asset-ownership.md), [source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/verify-asset-ownership.md), [source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/remove-u-t-x-o-lease.md), [source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/declare-script-key.md), [source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/export-asset-wallet-backup.md), [source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/import-assets-from-backup.md))

See also: [[tapd-taproot-assets]], [[tapd-universe]], [[tapd-mint]], [[tapd-mailbox]], [[tapd-tap-dev]].

## FundVirtualPsbt

FundVirtualPsbt selects inputs from the available asset commitments to fund a virtual transaction matching the template. ([source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/fund-virtual-psbt.md))

- gRPC: `rpc FundVirtualPsbt (FundVirtualPsbtRequest) returns (FundVirtualPsbtResponse);`
- REST: `POST /v1/taproot-assets/wallet/virtual-psbt/fund`
- Request message: `assetwalletrpc.FundVirtualPsbtRequest`
- Response message: `assetwalletrpc.FundVirtualPsbtResponse`

The request fields are `psbt` (use an existing PSBT packet as the template for the funded PSBT), `raw` (a `TxTemplate`: use the asset outputs and optional asset inputs from this raw template) and `coin_select_type`, which specifies the type of coins that should be selected and defaults to allowing both script trees and BIP-086 compliant inputs. The `CoinSelectType` values are `COIN_SELECT_DEFAULT`, `COIN_SELECT_BIP86_ONLY` and `COIN_SELECT_SCRIPT_TREES_ALLOWED`. ([source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/fund-virtual-psbt.md))

`TxTemplate` has `inputs`, `recipients` and `addresses_with_amounts`. `inputs` is an optional list in which every input must be an asset UTXO known to the wallet; if no inputs are specified, asset coin selection is performed instead. `recipients` is marked deprecated, and `recipients` and `addresses_with_amounts` are mutually exclusive. `addresses_with_amounts` must be used for V2 TAP addresses that don't specify an amount in the address itself. ([source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/fund-virtual-psbt.md))

The response fields are `funded_psbt` (the funded but not yet signed virtual PSBT packet), `change_output_index` (the index of the added change output or -1 if no change was left over) and `passive_asset_psbts`, the passive virtual transactions anchored in the same BTC level anchor transaction inputs as the funded "active" asset. The page says the passive assets can be ignored when using the AnchorVirtualPsbts RPC, but have to be included in the CommitVirtualPsbts RPC, which is used when custom BTC level anchor transactions are created. ([source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/fund-virtual-psbt.md))

## SignVirtualPsbt

SignVirtualPsbt signs the inputs of a virtual transaction and prepares the commitments of the inputs and outputs. ([source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/sign-virtual-psbt.md))

- gRPC: `rpc SignVirtualPsbt (SignVirtualPsbtRequest) returns (SignVirtualPsbtResponse);`
- REST: `POST /v1/taproot-assets/wallet/virtual-psbt/sign`
- Request message: `assetwalletrpc.SignVirtualPsbtRequest`
- Response message: `assetwalletrpc.SignVirtualPsbtResponse`

The request has one field, `funded_psbt`: the PSBT of the virtual transaction that should be signed, which must contain all required inputs, outputs, UTXO data and custom fields required to identify the signing key. The response fields are `signed_psbt` (the signed virtual transaction in PSBT format) and `signed_inputs` (the indices of signed inputs). ([source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/sign-virtual-psbt.md))

## AnchorVirtualPsbts

AnchorVirtualPsbts merges and then commits multiple virtual transactions in a single BTC level anchor transaction. The page says this RPC should be used if the BTC level anchor transaction of the assets to be spent are encumbered by a normal key and don't require any special spending conditions; for any custom spending conditions on the BTC level, the two RPCs CommitVirtualPsbts and PublishAndLogTransfer should be used instead, which in combination do the same as this RPC but allow for more flexibility. ([source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/anchor-virtual-psbts.md))

- gRPC: `rpc AnchorVirtualPsbts (AnchorVirtualPsbtsRequest) returns (SendAssetResponse);`
- REST: `POST /v1/taproot-assets/wallet/virtual-psbt/anchor`
- Request message: `assetwalletrpc.AnchorVirtualPsbtsRequest`
- Response message: `taprpc.SendAssetResponse`

The request has one field, `virtual_psbts`: the list of virtual transactions that should be merged and committed to in the BTC level anchor transaction. The response has one field, `transfer`, a `taprpc.AssetTransfer` whose fields include `transfer_timestamp`, `anchor_tx_hash`, `anchor_tx_height_hint`, `anchor_tx_chain_fees`, `inputs`, `outputs`, `anchor_tx_block_hash`, `anchor_tx_block_height`, `label` and `anchor_tx`. ([source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/anchor-virtual-psbts.md))

## CommitVirtualPsbts

CommitVirtualPsbts creates the output commitments and proofs for the given virtual transactions by committing them to the BTC level anchor transaction. In addition, the BTC level anchor transaction is funded and prepared up to the point where it is ready to be signed. ([source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/commit-virtual-psbts.md))

- gRPC: `rpc CommitVirtualPsbts (CommitVirtualPsbtsRequest) returns (CommitVirtualPsbtsResponse);`
- REST: `POST /v1/taproot-assets/wallet/virtual-psbt/commit`
- Request message: `assetwalletrpc.CommitVirtualPsbtsRequest`
- Response message: `assetwalletrpc.CommitVirtualPsbtsResponse`

The request fields are `virtual_psbts`, `passive_asset_psbts`, `anchor_psbt`, `existing_output_index`, `add`, `target_conf`, `sat_per_vbyte`, `custom_lock_id`, `lock_expiration_seconds`, `skip_funding` and `transition_proof_version`. `anchor_psbt` is the template of the BTC level anchor transaction that the virtual transactions should be mapped to. `existing_output_index` uses the existing output within the anchor PSBT with the specified index as the change output, and `add` adds a new P2TR change output to the PSBT if required. ([source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/commit-virtual-psbts.md))

If `custom_lock_id` is left empty, LND's default lock ID is used; if `lock_expiration_seconds` is unset, LND's default lock expiration of 10 minutes is applied. If `skip_funding` is set, the psbt funding step is skipped, which the page says is useful if the intent is to create a zero-fee transaction. If `transition_proof_version` is unset, the daemon's default proof version is used; the `TransitionProofVersion` values are `TRANSITION_PROOF_VERSION_V0` and `TRANSITION_PROOF_VERSION_V1`, the latter adding spent transaction output (STXO) inclusion and exclusion proofs. ([source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/commit-virtual-psbts.md))

The response fields are `anchor_psbt` (the funded BTC level anchor transaction with all outputs updated to commit to the virtual transactions given), `virtual_psbts`, `passive_asset_psbts`, `change_output_index` (the index of the (added) change output or -1 if no change was left over) and `lnd_locked_utxos` (the UTXO lock leases acquired for the inputs in the funded PSBT packet from lnd). ([source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/commit-virtual-psbts.md))

## PublishAndLogTransfer

PublishAndLogTransfer accepts a fully committed and signed anchor transaction and publishes it to the Bitcoin network. It also logs the transfer of the given active and passive assets in the database and ships any outgoing proofs to the counterparties. If `sign_anchor_inputs` is set, tapd first signs the anchor inputs it owns. ([source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/publish-and-log-transfer.md))

- gRPC: `rpc PublishAndLogTransfer (PublishAndLogRequest) returns (SendAssetResponse);`
- REST: `POST /v1/taproot-assets/wallet/virtual-psbt/log-transfer`
- Request message: `assetwalletrpc.PublishAndLogRequest`
- Response message: `taprpc.SendAssetResponse`

The request fields are `anchor_psbt`, `virtual_psbts`, `passive_asset_psbts`, `change_output_index`, `lnd_locked_utxos`, `skip_anchor_tx_broadcast`, `label`, `sign_anchor_inputs` and `input_proof_files`. If `skip_anchor_tx_broadcast` is set, the anchor transaction will not be broadcast to the network. `label` is an optional short label for the transfer. `input_proof_files` carries the proof files of asset inputs that this daemon's wallet holds no proof for; the daemon verifies each file and stores it in its proof archive. The response has one field, `transfer`. ([source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/publish-and-log-transfer.md))

## NextInternalKey

NextInternalKey derives the next internal key for the given key family and stores it as an internal key in the database to make sure it is identified as a local key later on when importing proofs. The page says that while an internal key can also be used as the internal key of a script key, it is recommended to use the NextScriptKey RPC instead, to make sure the tweaked Taproot output key is also recognized as a local key. ([source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/next-internal-key.md))

- gRPC: `rpc NextInternalKey (NextInternalKeyRequest) returns (NextInternalKeyResponse);`
- REST: `POST /v1/taproot-assets/wallet/internal-key/next`
- Request message: `assetwalletrpc.NextInternalKeyRequest`
- Response message: `assetwalletrpc.NextInternalKeyResponse`

The request has one field, `key_family` (the key family to derive the next internal key for). The response has one field, `internal_key`, a `taprpc.KeyDescriptor` with `raw_key_bytes` and `key_loc`. ([source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/next-internal-key.md))

## NextScriptKey

NextScriptKey derives the next script key (and its corresponding internal key) and stores them both in the database to make sure they are identified as local keys later on when importing proofs. ([source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/next-script-key.md))

- gRPC: `rpc NextScriptKey (NextScriptKeyRequest) returns (NextScriptKeyResponse);`
- REST: `POST /v1/taproot-assets/wallet/script-key/next`
- Request message: `assetwalletrpc.NextScriptKeyRequest`
- Response message: `assetwalletrpc.NextScriptKeyResponse`

The request has one field, `key_family`. The response has one field, `script_key`, a `taprpc.ScriptKey` with `pub_key`, `key_desc`, `tap_tweak` and `type`. ([source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/next-script-key.md))

## QueryInternalKey

QueryInternalKey returns the key descriptor for the given internal key. ([source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/query-internal-key.md))

- gRPC: `rpc QueryInternalKey (QueryInternalKeyRequest) returns (QueryInternalKeyResponse);`
- REST: `GET /v1/taproot-assets/wallet/internal-key/{internal_key}`
- Request message: `assetwalletrpc.QueryInternalKeyRequest`
- Response message: `assetwalletrpc.QueryInternalKeyResponse`

The request field `internal_key` can either be the 32-byte x-only raw internal key or the 33-byte raw internal key with the parity byte; its REST placement is `path`. The response has one field, `internal_key`, the full key descriptor of the internal key that was queried. ([source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/query-internal-key.md))

## QueryScriptKey

QueryScriptKey returns the full script key descriptor for the given tweaked script key. ([source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/query-script-key.md))

- gRPC: `rpc QueryScriptKey (QueryScriptKeyRequest) returns (QueryScriptKeyResponse);`
- REST: `GET /v1/taproot-assets/wallet/script-key/{tweaked_script_key}`
- Request message: `assetwalletrpc.QueryScriptKeyRequest`
- Response message: `assetwalletrpc.QueryScriptKeyResponse`

The request field `tweaked_script_key` can either be the 32-byte x-only tweaked script key or the 33-byte tweaked script key with the parity byte; its REST placement is `path`. The response has one field, `script_key`, the full script key information that was queried, including the internal key and the tweaked script key. ([source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/query-script-key.md))

## ProveAssetOwnership

ProveAssetOwnership creates an ownership proof embedded in an asset transition proof. That ownership proof is a signed virtual transaction spending the asset with a valid witness to prove the prover owns the keys that can spend the asset. ([source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/prove-asset-ownership.md))

- gRPC: `rpc ProveAssetOwnership (ProveAssetOwnershipRequest) returns (ProveAssetOwnershipResponse);`
- REST: `POST /v1/taproot-assets/wallet/ownership/prove`
- Request message: `assetwalletrpc.ProveAssetOwnershipRequest`
- Response message: `assetwalletrpc.ProveAssetOwnershipResponse`

The request fields are `asset_id`, `script_key`, `outpoint` and `challenge`. `challenge` is an optional 32-byte challenge that may be used to bind the generated proof, and it needs to be also presented on the VerifyAssetOwnership RPC in order to check the proof against it. The response has one field, `proof_with_witness`. ([source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/prove-asset-ownership.md))

## VerifyAssetOwnership

VerifyAssetOwnership verifies the asset ownership proof embedded in the given transition proof of an asset and returns true if the proof is valid. ([source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/verify-asset-ownership.md))

- gRPC: `rpc VerifyAssetOwnership (VerifyAssetOwnershipRequest) returns (VerifyAssetOwnershipResponse);`
- REST: `POST /v1/taproot-assets/wallet/ownership/verify`
- Request message: `assetwalletrpc.VerifyAssetOwnershipRequest`
- Response message: `assetwalletrpc.VerifyAssetOwnershipResponse`

The request fields are `proof_with_witness` (the full ownership proof that was generated, including the witness data that contains the proving signature) and `challenge`, an optional 32-byte challenge that must match the one the prover used on the ProveAssetOwnership RPC. The response fields are `valid_proof`, `outpoint`, `outpoint_str`, `block_hash`, `block_hash_str` and `block_height`. ([source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/verify-asset-ownership.md))

## RemoveUTXOLease

RemoveUTXOLease removes the lease/lock/reservation of the given managed UTXO. The page gives the CLI command as `tapcli: assets removelease`. ([source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/remove-u-t-x-o-lease.md))

- gRPC: `rpc RemoveUTXOLease (RemoveUTXOLeaseRequest) returns (RemoveUTXOLeaseResponse);`
- REST: `POST /v1/taproot-assets/wallet/utxo-lease/delete`
- Request message: `assetwalletrpc.RemoveUTXOLeaseRequest`
- Response message: `assetwalletrpc.RemoveUTXOLeaseResponse`

The request has one field, `outpoint` (the outpoint of the UTXO to remove the lease for). The response has no parameters. ([source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/remove-u-t-x-o-lease.md))

## DeclareScriptKey

DeclareScriptKey declares a new script key to the wallet. The page says this is useful when the script key contains scripts, which would mean it wouldn't be recognized by the wallet automatically, and that declaring a script key will make any assets sent to the script key be recognized as being local assets. ([source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/declare-script-key.md))

- gRPC: `rpc DeclareScriptKey (DeclareScriptKeyRequest) returns (DeclareScriptKeyResponse);`
- REST: `POST /v1/taproot-assets/wallet/script-key/declare`
- Request message: `assetwalletrpc.DeclareScriptKeyRequest`
- Response message: `assetwalletrpc.DeclareScriptKeyResponse`

The request has one field, `script_key` (the script key the wallet should be informed about). The response has one field, `script_key`, the script key that was declared, including the internal key and the tweaked script key. ([source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/declare-script-key.md))

## ExportAssetWalletBackup

ExportAssetWalletBackup exports a backup of all active assets in the wallet. The backup includes all data necessary to restore the assets in case of database or system failure. ([source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/export-asset-wallet-backup.md))

- gRPC: `rpc ExportAssetWalletBackup (ExportAssetWalletBackupRequest) returns (ExportAssetWalletBackupResponse);`
- REST: `POST /v1/taproot-assets/wallet/backup/export`
- Request message: `assetwalletrpc.ExportAssetWalletBackupRequest`
- Response message: `assetwalletrpc.ExportAssetWalletBackupResponse`

The request has one field, `mode`, a `BackupMode`. If not set, it defaults to RAW (the protobuf zero value); the page adds that the CLI defaults to COMPACT for smaller backups, and that callers that want compact mode should set this explicitly. `RAW` exports a full backup with complete proof data (v1). `COMPACT` strips blockchain-derivable fields from proofs, which are reconstructed from the blockchain on import (v2). `OPTIMISTIC` stores no proof data; proofs are fetched from a universe server on import, which requires a reachable universe server during restore (v3). The response has one field, `backup`, the binary backup blob. ([source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/export-asset-wallet-backup.md))

## ImportAssetsFromBackup

ImportAssetsFromBackup imports assets from a backup blob that was previously created using ExportAssetWalletBackup. The page says this can be used to restore assets after database loss or to migrate assets to a new wallet. ([source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/import-assets-from-backup.md))

- gRPC: `rpc ImportAssetsFromBackup (ImportAssetsFromBackupRequest) returns (ImportAssetsFromBackupResponse);`
- REST: `POST /v1/taproot-assets/wallet/backup/import`
- Request message: `assetwalletrpc.ImportAssetsFromBackupRequest`
- Response message: `assetwalletrpc.ImportAssetsFromBackupResponse`

The request has one field, `backup`. The response fields are `num_imported` (the number of assets that were successfully imported) and `num_skipped` (the number of assets that were skipped due to errors during import; details are logged server-side). ([source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/import-assets-from-backup.md))

## Conflicts

On the AnchorVirtualPsbts page, the "Source:" line under the `taprpc.SendAssetResponse` message shows the link text `taprootassets.proto`, while the link target is `taprpc/assetwalletrpc/assetwallet.proto`. The page does not resolve which file defines the message. ([source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/anchor-virtual-psbts.md))

The PublishAndLogTransfer page has the same mismatch for `taprpc.SendAssetResponse`: link text `taprootassets.proto`, link target `taprpc/assetwalletrpc/assetwallet.proto`. ([source](../../raw/api/api-docs/api/taproot-assets/asset-wallet/publish-and-log-transfer.md))
