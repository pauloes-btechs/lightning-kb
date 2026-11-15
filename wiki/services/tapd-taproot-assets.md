---
title: taproot-assets taproot-assets service
type: service
sources:
  - raw/api/api-docs/api/taproot-assets.md
  - raw/api/api-docs/api/taproot-assets/rest-endpoints.md
  - raw/api/api-docs/api/taproot-assets/taproot-assets/addr-receives.md
  - raw/api/api-docs/api/taproot-assets/taproot-assets/bake-macaroon.md
  - raw/api/api-docs/api/taproot-assets/taproot-assets/burn-asset.md
  - raw/api/api-docs/api/taproot-assets/taproot-assets/debug-level.md
  - raw/api/api-docs/api/taproot-assets/taproot-assets/decode-addr.md
  - raw/api/api-docs/api/taproot-assets/taproot-assets/decode-proof.md
  - raw/api/api-docs/api/taproot-assets/taproot-assets/export-proof.md
  - raw/api/api-docs/api/taproot-assets/taproot-assets/fetch-asset-meta.md
  - raw/api/api-docs/api/taproot-assets/taproot-assets/fetch-asset.md
  - raw/api/api-docs/api/taproot-assets/taproot-assets/get-info.md
  - raw/api/api-docs/api/taproot-assets/taproot-assets/list-anchorings.md
  - raw/api/api-docs/api/taproot-assets/taproot-assets/list-assets.md
  - raw/api/api-docs/api/taproot-assets/taproot-assets/list-balances.md
  - raw/api/api-docs/api/taproot-assets/taproot-assets/list-burns.md
  - raw/api/api-docs/api/taproot-assets/taproot-assets/list-groups.md
  - raw/api/api-docs/api/taproot-assets/taproot-assets/list-transfers.md
  - raw/api/api-docs/api/taproot-assets/taproot-assets/list-utxos.md
  - raw/api/api-docs/api/taproot-assets/taproot-assets/new-addr.md
  - raw/api/api-docs/api/taproot-assets/taproot-assets/query-addrs.md
  - raw/api/api-docs/api/taproot-assets/taproot-assets/register-transfer.md
  - raw/api/api-docs/api/taproot-assets/taproot-assets/send-asset.md
  - raw/api/api-docs/api/taproot-assets/taproot-assets/stop-daemon.md
  - raw/api/api-docs/api/taproot-assets/taproot-assets/subscribe-receive-events.md
  - raw/api/api-docs/api/taproot-assets/taproot-assets/subscribe-send-events.md
  - raw/api/api-docs/api/taproot-assets/taproot-assets/unpack-proof-file.md
  - raw/api/api-docs/api/taproot-assets/taproot-assets/verify-proof.md
updated: 2026-11-14
---

# taproot-assets taproot-assets service

This page covers the RPCs that the REST endpoints page lists with the `taprpc.` prefix (see [[taproot-assets]]). ([source](../../raw/api/api-docs/api/taproot-assets/rest-endpoints.md))

The `GetInfo` page's "Source:" link names `taprootassets.proto` as its proto file, and the page names its messages with the `taprpc.` prefix (`taprpc.GetInfoRequest`, `taprpc.GetInfoResponse`). ([source](../../raw/api/api-docs/api/taproot-assets/taproot-assets/get-info.md))

The REST endpoint listing has 26 rows whose RPC is prefixed `taprpc.`: `QueryAddrs`, `NewAddr`, `DecodeAddr`, `AddrReceives`, `ListAnchorings`, `ListAssets`, `ListBalances`, `FetchAsset`, `ListGroups`, `FetchAssetMeta`, `ListTransfers`, `RegisterTransfer`, `ListUtxos`, `BurnAsset`, `ListBurns`, `DebugLevel`, `SubscribeReceiveEvents`, `SubscribeSendEvents`, `GetInfo`, `BakeMacaroon`, `DecodeProof`, `ExportProof`, `UnpackProofFile`, `VerifyProof`, `SendAsset` and `StopDaemon`. All REST paths of this service start with `/v1/taproot-assets/`. ([source](../../raw/api/api-docs/api/taproot-assets/rest-endpoints.md))

The reference was generated against commit `14aa3fd90e6aace4d3b2cfc72a51d15ce4afd891` of the `lightninglabs/taproot-assets` repository. Its code samples assume a local `tapd` listening for gRPC on port `10029` and for REST on port `8089`; a request needs a TLS/SSL connection and a macaroon used for RPC authentication (see [[macaroons]]). In REST, a `byte` field must be set as the base64 encoded string representation of a raw byte array, and in a URL path the base64 string must use the URL and Filename Safe Alphabet. ([source](../../raw/api/api-docs/api/taproot-assets.md))

See also: [[taproot-assets]], [[tapd-asset-wallet]], [[tapd-mint]], [[tapd-universe]], [[tapd-mailbox]], [[tapd-rfq]], [[tapd-taproot-asset-channels]], [[tapd-getting-started]], [[tapd-operations]].

## Assets and balances

### ListAssets

ListAssets lists the set of assets owned by the target daemon.

- gRPC: `rpc ListAssets (ListAssetRequest) returns (ListAssetResponse);`
- REST: `GET /v1/taproot-assets/assets`
- Request `taprpc.ListAssetRequest`: filters `with_witness`, `include_spent`, `include_leased`, `include_unconfirmed_mints`, `min_amount`, `max_amount`, `group_key`, `script_key`, `anchor_outpoint`, `script_key_type`, and paging via `offset`, `limit` and `direction`. If `limit` is 0, a default of 512 is used; the maximum allowed value is 16384. `direction` sorts by asset primary key (creation order) and defaults to descending. If `script_key_type` is not set, only assets with a BIP-0086 script key are returned.
- Response `taprpc.ListAssetResponse`: `assets`, plus the counts `unconfirmed_transfers` (unconfirmed outgoing transfers, which do not appear as assets in this response) and `unconfirmed_mints`.

([source](../../raw/api/api-docs/api/taproot-assets/taproot-assets/list-assets.md))

### FetchAsset

FetchAsset fetches asset(s) by asset ID or group key, with optional filters. At least one of asset_id or group_key must be set in the asset_specifier.

- gRPC: `rpc FetchAsset (FetchAssetRequest) returns (FetchAssetResponse);`
- REST: `GET /v1/taproot-assets/assets/fetch/asset-id/{asset_specifier.asset_id_str}`
- Request `taprpc.FetchAssetRequest`: `asset_specifier` (a `taprpc.AssetSpecifier` with `asset_id`, `asset_id_str`, `group_key`, `group_key_str`; the `_str` variants are the ones to use for REST), `with_witness`, `include_spent`, `include_leased`, `include_unconfirmed_mints`, `script_key_type`.
- Response `taprpc.FetchAssetResponse`: `assets`.

([source](../../raw/api/api-docs/api/taproot-assets/taproot-assets/fetch-asset.md))

### ListUtxos

ListUtxos lists the UTXOs managed by the target daemon, and the assets they hold.

- gRPC: `rpc ListUtxos (ListUtxosRequest) returns (ListUtxosResponse);`
- REST: `GET /v1/taproot-assets/assets/utxos`
- Request `taprpc.ListUtxosRequest`: `include_leased`, `script_key_type`.
- Response `taprpc.ListUtxosResponse`: `managed_utxos`, a map of `taprpc.ManagedUtxo` entries with `out_point`, `amt_sat`, `internal_key`, `taproot_asset_root`, `merkle_root`, `assets`, `lease_owner` and `lease_expiry_unix`.

([source](../../raw/api/api-docs/api/taproot-assets/taproot-assets/list-utxos.md))

### ListGroups

ListGroups lists the asset groups known to the target daemon, and the assets held in each group.

- gRPC: `rpc ListGroups (ListGroupsRequest) returns (ListGroupsResponse);`
- REST: `GET /v1/taproot-assets/assets/groups`
- Request `taprpc.ListGroupsRequest`: no parameters.
- Response `taprpc.ListGroupsResponse`: `groups`, the set of assets with a group key.

([source](../../raw/api/api-docs/api/taproot-assets/taproot-assets/list-groups.md))

### ListBalances

ListBalances lists asset balances.

- gRPC: `rpc ListBalances (ListBalancesRequest) returns (ListBalancesResponse);`
- REST: `GET /v1/taproot-assets/assets/balance`
- Request `taprpc.ListBalancesRequest`: `asset_id` (bool, group results by asset IDs), `group_key` (bool, group results by group keys), `asset_filter`, `group_key_filter`, `include_leased`, `script_key_type`.
- Response `taprpc.ListBalancesResponse`: `asset_balances` (keyed by asset ID), `asset_group_balances` (keyed by group key) and `unconfirmed_transfers`. Unconfirmed transfers (and the change resulting from them) do not appear in the balance; the balance only represents confirmed assets that are owned by the daemon.

([source](../../raw/api/api-docs/api/taproot-assets/taproot-assets/list-balances.md))

### FetchAssetMeta

FetchAssetMeta allows a caller to fetch the reveal meta data for an asset either by the asset ID for that asset, or a meta hash.

- gRPC: `rpc FetchAssetMeta (FetchAssetMetaRequest) returns (FetchAssetMetaResponse);`
- REST: `GET /v1/taproot-assets/assets/meta/asset-id/{asset_id_str}`
- Request `taprpc.FetchAssetMetaRequest`: `asset_id`, `meta_hash`, `asset_id_str`, `meta_hash_str`.
- Response `taprpc.FetchAssetMetaResponse`: `data` (size limited to 1MiB), `type`, `meta_hash`, `unknown_odd_types`, `decimal_display`, `universe_commitments`, `canonical_universe_urls`, `delegation_key`.

([source](../../raw/api/api-docs/api/taproot-assets/taproot-assets/fetch-asset-meta.md))

## Addresses and receiving

### NewAddr

NewAddr makes a new address from the set of request params.

- gRPC: `rpc NewAddr (NewAddrRequest) returns (Addr);`
- REST: `POST /v1/taproot-assets/addrs`
- Request `taprpc.NewAddrRequest`: `asset_id` and `amt` (both required for V0 and V1 addresses, optional for V2 addresses), `script_key`, `internal_key` (these two should either both be set or both be empty), `tapscript_sibling`, `proof_courier_addr` (if unspecified, the daemon configured default address is used), `asset_version`, `address_version`, `group_key` (only for V2 addresses; if set, `asset_id` must be empty), `skip_proof_courier_conn_check`.
- Response `taprpc.Addr`: `encoded` (the bech32 encoded Taproot Asset address), `asset_id`, `asset_type`, `amount`, `group_key`, `script_key`, `internal_key`, `tapscript_sibling`, `taproot_output_key`, `proof_courier_addr`, `asset_version`, `address_version`. For V2 addresses the proof courier address is mandatory and must be a valid auth mailbox address (`authmailbox+universerpc://host:port`).

([source](../../raw/api/api-docs/api/taproot-assets/taproot-assets/new-addr.md))

### QueryAddrs

QueryAddrs queries the set of Taproot Asset addresses stored in the database.

- gRPC: `rpc QueryAddrs (QueryAddrRequest) returns (QueryAddrResponse);`
- REST: `GET /v1/taproot-assets/addrs`
- Request `taprpc.QueryAddrRequest`: `created_after`, `created_before`, `limit`, `offset`.
- Response `taprpc.QueryAddrResponse`: `addrs`.

([source](../../raw/api/api-docs/api/taproot-assets/taproot-assets/query-addrs.md))

### DecodeAddr

DecodeAddr decodes a Taproot Asset address into a partial asset message that represents the asset it wants to receive.

- gRPC: `rpc DecodeAddr (DecodeAddrRequest) returns (Addr);`
- REST: `POST /v1/taproot-assets/addrs/decode`
- Request `taprpc.DecodeAddrRequest`: `addr`, the bech32 encoded Taproot Asset address to decode.
- Response `taprpc.Addr`.

([source](../../raw/api/api-docs/api/taproot-assets/taproot-assets/decode-addr.md))

### AddrReceives

List all receives for incoming asset transfers for addresses that were created previously.

- gRPC: `rpc AddrReceives (AddrReceivesRequest) returns (AddrReceivesResponse);`
- REST: `POST /v1/taproot-assets/addrs/receives`
- Request `taprpc.AddrReceivesRequest`: `filter_addr`, `filter_status`, `start_timestamp`, `end_timestamp`, `offset`, `limit`, `direction`.
- Response `taprpc.AddrReceivesResponse`: `events`, a list of `taprpc.AddrEvent` (`creation_time_unix_seconds`, `addr`, `status`, `outpoint`, `utxo_amt_sat`, `taproot_sibling`, `confirmation_height`, `has_proof`). The `taprpc.AddrEventStatus` values are `ADDR_EVENT_STATUS_UNKNOWN`, `ADDR_EVENT_STATUS_TRANSACTION_DETECTED`, `ADDR_EVENT_STATUS_TRANSACTION_CONFIRMED`, `ADDR_EVENT_STATUS_PROOF_RECEIVED` and `ADDR_EVENT_STATUS_COMPLETED`.

([source](../../raw/api/api-docs/api/taproot-assets/taproot-assets/addr-receives.md))

### SubscribeReceiveEvents

SubscribeReceiveEvents allows a caller to subscribe to receive events for incoming asset transfers. This is a server-streaming RPC.

- gRPC: `rpc SubscribeReceiveEvents (SubscribeReceiveEventsRequest) returns (stream ReceiveEvent);`
- REST: `POST /v1/taproot-assets/events/asset-receive`
- Request `taprpc.SubscribeReceiveEventsRequest`: `filter_addr`, `start_timestamp` (Unix timestamp in microseconds; if not set, the daemon starts streaming events from the current time).
- Response stream of `taprpc.ReceiveEvent`: `timestamp`, `address`, `outpoint`, `status`, `confirmation_height`, `error`.

([source](../../raw/api/api-docs/api/taproot-assets/taproot-assets/subscribe-receive-events.md))

### RegisterTransfer

RegisterTransfer informs the daemon about a new inbound transfer that has happened. This is used for interactive transfers where no TAP address is involved and the recipient is aware of the transfer through an out-of-band protocol but the daemon hasn't been informed about the completion of the transfer. The proof must already be in the recipient's local universe (e.g. through the use of the universerpc.InsertProof RPC or the universe proof courier and universe sync mechanisms); this call simply instructs the daemon to detect the transfer as an asset it owns.

- gRPC: `rpc RegisterTransfer (RegisterTransferRequest) returns (RegisterTransferResponse);`
- REST: `POST /v1/taproot-assets/assets/transfers/register`
- Request `taprpc.RegisterTransferRequest`: `asset_id`, `group_key`, `script_key`, `outpoint`.
- Response `taprpc.RegisterTransferResponse`: `registered_asset`.

([source](../../raw/api/api-docs/api/taproot-assets/taproot-assets/register-transfer.md))

## Sending and burning

### SendAsset

SendAsset uses one or multiple passed Taproot Asset address(es) to attempt to complete an asset send. The method returns information w.r.t the on chain send, as well as the proof file information the receiver needs to fully receive the asset.

- gRPC: `rpc SendAsset (SendAssetRequest) returns (SendAssetResponse);`
- REST: `POST /v1/taproot-assets/send`
- Request `taprpc.SendAssetRequest`: `tap_addrs`, `fee_rate` (in sat/kw), `label`, `skip_proof_courier_ping_check`, `addresses_with_amounts` (a list of `taprpc.AddressWithAmount` with `tap_addr` and `amount`). `tap_addrs` and `addresses_with_amounts` are mutually exclusive; `addresses_with_amounts` must be used for V2 TAP addresses that don't specify an amount in the address itself.
- Response `taprpc.SendAssetResponse`: `transfer`, a `taprpc.AssetTransfer`.

([source](../../raw/api/api-docs/api/taproot-assets/taproot-assets/send-asset.md))

### ListTransfers

ListTransfers lists outbound asset transfers tracked by the target daemon.

- gRPC: `rpc ListTransfers (ListTransfersRequest) returns (ListTransfersResponse);`
- REST: `GET /v1/taproot-assets/assets/transfers`
- Request `taprpc.ListTransfersRequest`: `anchor_txid`, the hexadecimal encoded txid string of the anchor transaction for which to retrieve transfers; an empty value means the parameter is disregarded.
- Response `taprpc.ListTransfersResponse`: `transfers`, the unordered list of outgoing asset transfers.

([source](../../raw/api/api-docs/api/taproot-assets/taproot-assets/list-transfers.md))

### SubscribeSendEvents

SubscribeSendEvents allows a caller to subscribe to send events for outgoing asset transfers. This is a server-streaming RPC.

- gRPC: `rpc SubscribeSendEvents (SubscribeSendEventsRequest) returns (stream SendEvent);`
- REST: `POST /v1/taproot-assets/events/asset-send`
- Request `taprpc.SubscribeSendEventsRequest`: `filter_script_key`, `filter_label`, `start_timestamp`.
- Response stream of `taprpc.SendEvent`: `timestamp`, `send_state`, `parcel_type`, `addresses`, `virtual_packets`, `passive_virtual_packets`, `anchor_transaction`, `transfer`, `error`, `transfer_label`, `next_send_state`. The `taprpc.ParcelType` values are `PARCEL_TYPE_ADDRESS`, `PARCEL_TYPE_PRE_SIGNED`, `PARCEL_TYPE_PENDING` and `PARCEL_TYPE_PRE_ANCHORED`.

([source](../../raw/api/api-docs/api/taproot-assets/taproot-assets/subscribe-send-events.md))

### BurnAsset

BurnAsset burns the given number of units of a given asset by sending them to a provably un-spendable script key. Burning means irrevocably destroying a certain number of assets, reducing the total supply of the asset. Because burning is such a destructive and non-reversible operation, some specific values need to be set in the request to avoid accidental burns.

- gRPC: `rpc BurnAsset (BurnAssetRequest) returns (BurnAssetResponse);`
- REST: `POST /v1/taproot-assets/burn`
- Request `taprpc.BurnAssetRequest`: `asset_id` and `asset_id_str` (both deprecated in favour of `asset_specifier`), `amount_to_burn` (must be greater than zero), `confirmation_text` (must be set to the value "assets will be destroyed" for the burn to succeed), `note`, `asset_specifier` (supports both asset ID and group key).
- Response `taprpc.BurnAssetResponse`: `burn_transfer`, `burn_proof` (deprecated: use `burn_proofs`), `burn_proofs`.

([source](../../raw/api/api-docs/api/taproot-assets/taproot-assets/burn-asset.md))

### ListBurns

ListBurns lists the asset burns that this wallet has performed. These assets are not recoverable in any way. Filters may be applied to return more specific results.

- gRPC: `rpc ListBurns (ListBurnsRequest) returns (ListBurnsResponse);`
- REST: `GET /v1/taproot-assets/burns`
- Request `taprpc.ListBurnsRequest`: `asset_id`, `tweaked_group_key`, `anchor_txid`.
- Response `taprpc.ListBurnsResponse`: `burns`, a list of `taprpc.AssetBurn` (`note`, `asset_id`, `tweaked_group_key`, `amount`, `anchor_txid`, `asset_type`).

([source](../../raw/api/api-docs/api/taproot-assets/taproot-assets/list-burns.md))

## Proofs

### ExportProof

ExportProof exports the latest raw proof file anchored at the specified script_key.

- gRPC: `rpc ExportProof (ExportProofRequest) returns (ProofFile);`
- REST: `POST /v1/taproot-assets/proofs/export`
- Request `taprpc.ExportProofRequest`: `asset_id`, `script_key`, `outpoint`.
- Response `taprpc.ProofFile`: `raw_proof_file`, `genesis_point`.

([source](../../raw/api/api-docs/api/taproot-assets/taproot-assets/export-proof.md))

### VerifyProof

VerifyProof attempts to verify a given proof file that claims to be anchored at the specified genesis point.

- gRPC: `rpc VerifyProof (ProofFile) returns (VerifyProofResponse);`
- REST: `POST /v1/taproot-assets/proofs/verify`
- Request `taprpc.ProofFile`: `raw_proof_file` (must be a file and not just an individual mint/transfer proof), `genesis_point`.
- Response `taprpc.VerifyProofResponse`: `valid`, `decoded_proof` (the decoded last proof in the file if the proof file was valid).

([source](../../raw/api/api-docs/api/taproot-assets/taproot-assets/verify-proof.md))

### DecodeProof

DecodeProof attempts to decode a given proof file into human readable format.

- gRPC: `rpc DecodeProof (DecodeProofRequest) returns (DecodeProofResponse);`
- REST: `POST /v1/taproot-assets/proofs/decode`
- Request `taprpc.DecodeProofRequest`: `raw_proof` (a full proof file or a single mint/transition proof), `proof_at_depth` (0 being the latest proof), `with_prev_witnesses`, `with_meta_reveal`.
- Response `taprpc.DecodeProofResponse`: `decoded_proof`.

([source](../../raw/api/api-docs/api/taproot-assets/taproot-assets/decode-proof.md))

### UnpackProofFile

UnpackProofFile unpacks a proof file into a list of the individual raw proofs in the proof chain.

- gRPC: `rpc UnpackProofFile (UnpackProofFileRequest) returns (UnpackProofFileResponse);`
- REST: `POST /v1/taproot-assets/proofs/unpack-file`
- Request `taprpc.UnpackProofFileRequest`: `raw_proof_file`.
- Response `taprpc.UnpackProofFileResponse`: `raw_proofs`, ordered by their appearance within the file (issuance proof first, last known transfer last).

([source](../../raw/api/api-docs/api/taproot-assets/taproot-assets/unpack-proof-file.md))

## Daemon

### GetInfo

GetInfo returns the information for the node.

- gRPC: `rpc GetInfo (GetInfoRequest) returns (GetInfoResponse);`
- REST: `GET /v1/taproot-assets/getinfo`
- Request `taprpc.GetInfoRequest`: no parameters.
- Response `taprpc.GetInfoResponse`: `version`, `lnd_version`, `network`, `lnd_identity_pubkey`, `node_alias`, `block_height`, `block_hash`, `sync_to_chain`.

([source](../../raw/api/api-docs/api/taproot-assets/taproot-assets/get-info.md))

### ListAnchorings

ListAnchorings lists the re-org watcher's speculative anchorings: everything the daemon has staked on chain outcomes, the phase the chain has assigned to each stake, and the delivery state of the owning subsystem.

- gRPC: `rpc ListAnchorings (ListAnchoringsRequest) returns (ListAnchoringsResponse);`
- REST: `GET /v1/taproot-assets/anchorings`
- Request `taprpc.ListAnchoringsRequest`: `site`, `phase` (one of unwitnessed, witnessed, conflicted, buried, abandoned; any other value is an error), `stuck_only`, `limit` (at most 1000 per page; zero requests the default page size of 100), `offset`.
- Response `taprpc.ListAnchoringsResponse`: `anchorings`, a list of `taprpc.Anchoring` with, among others, `id`, `site`, `phase`, `delivered_phase`, `threshold`, `stuck`, `stuck_reason`, `delivery_attempts` and `witness_txid`.

([source](../../raw/api/api-docs/api/taproot-assets/taproot-assets/list-anchorings.md))

### DebugLevel

DebugLevel allows a caller to programmatically set the logging verbosity of tapd. The logging can be targeted according to a coarse daemon-wide logging level, or in a granular fashion to specify the logging for a target sub-system.

- gRPC: `rpc DebugLevel (DebugLevelRequest) returns (DebugLevelResponse);`
- REST: `POST /v1/taproot-assets/debuglevel`
- Request `taprpc.DebugLevelRequest`: `show` (if true, all the valid debug sub-systems are returned), `level_spec` (one of "trace", "debug", "info", "warn", "error", "critical", "off", optionally followed by a comma-separated list of sub-systems; the page's example is "debug,TADB=info,UNIV=warn").
- Response `taprpc.DebugLevelResponse`: `sub_systems`.

([source](../../raw/api/api-docs/api/taproot-assets/taproot-assets/debug-level.md))

### BakeMacaroon

BakeMacaroon allows the creation of a new macaroon with custom permissions. No first-party caveats are added since this can be done offline.

- gRPC: `rpc BakeMacaroon (BakeMacaroonRequest) returns (BakeMacaroonResponse);`
- REST: `POST /v1/taproot-assets/macaroon`
- Request `taprpc.BakeMacaroonRequest`: `permissions` (a list of `taprpc.MacaroonPermission` with `entity` and `action`), `root_key_id` (must be a non-negative integer), `allow_external_permissions`.
- Response `taprpc.BakeMacaroonResponse`: `macaroon`, the hex encoded macaroon, serialized in binary format.

([source](../../raw/api/api-docs/api/taproot-assets/taproot-assets/bake-macaroon.md))

### StopDaemon

StopDaemon will send a shutdown request to the interrupt handler, triggering a graceful shutdown of the daemon.

- gRPC: `rpc StopDaemon (StopRequest) returns (StopResponse);`
- REST: `POST /v1/taproot-assets/stop`
- Request `taprpc.StopRequest` and response `taprpc.StopResponse`: no parameters.

([source](../../raw/api/api-docs/api/taproot-assets/taproot-assets/stop-daemon.md))

## Notes

Editor's observations, not statements from the sources:

- The group headings on this page ("Assets and balances", "Proofs" and so on) are this wiki's own arrangement; the reference lists the RPCs without grouping.
- On the `ListBalances` page the response field descriptions refer to `group_by.asset_id` and `group_by.group_key`, while the request table on the same page lists the fields as plain `asset_id` and `group_key`.
- On the `BurnAsset` page the request field `asset_specifier` carries a "deprecated" marker even though its description says it supersedes the deprecated `asset_id`/`asset_id_str` fields.
- On the `SendAsset` page `fee_rate` is described as the fee rate "for the minting transaction".
