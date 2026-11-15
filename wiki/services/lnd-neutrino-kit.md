---
title: lnd neutrino-kit service
type: service
sources:
  - raw/api/api-docs/api/lnd.md
  - raw/api/api-docs/api/lnd/rest-endpoints.md
  - raw/api/api-docs/api/lnd/neutrino-kit/add-peer.md
  - raw/api/api-docs/api/lnd/neutrino-kit/disconnect-peer.md
  - raw/api/api-docs/api/lnd/neutrino-kit/get-block-hash.md
  - raw/api/api-docs/api/lnd/neutrino-kit/get-block-header.md
  - raw/api/api-docs/api/lnd/neutrino-kit/get-block.md
  - raw/api/api-docs/api/lnd/neutrino-kit/get-c-filter.md
  - raw/api/api-docs/api/lnd/neutrino-kit/is-banned.md
  - raw/api/api-docs/api/lnd/neutrino-kit/status.md
updated: 2026-11-14
---

# lnd neutrino-kit service (NeutrinoKit)

The NeutrinoKit service of [[lnd]] exposes the light client neutrino instance. Its Status RPC returns the status of that instance, and its RPC pages give `neutrinorpc/neutrino.proto` as their source. ([source](../../raw/api/api-docs/api/lnd/neutrino-kit/status.md))

The lnd API overview names `neutrino` (described there as "a new experimental light client") as one of lnd's pluggable chain back-ends, alongside `btcd` and `bitcoind`. It lists Service *NeutrinoKit* (file: `neutrinorpc/neutrino.proto`) among the experimental services, which are subject to change and need a compile-time flag to be active (they are active in the official release binaries). The reference was generated against commit `895118ac4ec59e78b2c14f5b0d31ac6f862434bb`. ([source](../../raw/api/api-docs/api/lnd.md))

The REST endpoints page lists eight `neutrinorpc` RPCs under `/v2/neutrino/`: AddPeer, GetBlock, GetBlockHash, GetBlockHeader, GetCFilter, DisconnectPeer, IsBanned and Status. ([source](../../raw/api/api-docs/api/lnd/rest-endpoints.md))

See also: [[lnd-chain-kit]], [[lnd-configuration]].

## Status

Status returns the status of the light client neutrino instance, along with height and hash of the best block, and a list of connected peers. ([source](../../raw/api/api-docs/api/lnd/neutrino-kit/status.md))

- gRPC: `rpc Status (StatusRequest) returns (StatusResponse);`
- REST: `GET /v2/neutrino/status`
- Request: `neutrinorpc.StatusRequest` (no parameters)
- Response: `neutrinorpc.StatusResponse`, fields `active`, `synced`, `block_height`, `block_hash` and `peers`

([source](../../raw/api/api-docs/api/lnd/neutrino-kit/status.md))

## AddPeer

AddPeer adds a new peer that has already been connected to the server. ([source](../../raw/api/api-docs/api/lnd/neutrino-kit/add-peer.md))

- gRPC: `rpc AddPeer (AddPeerRequest) returns (AddPeerResponse);`
- REST: `POST /v2/neutrino/addpeer`
- Request: `neutrinorpc.AddPeerRequest`, field `peer_addrs`
- Response: `neutrinorpc.AddPeerResponse` (no parameters)

([source](../../raw/api/api-docs/api/lnd/neutrino-kit/add-peer.md))

## DisconnectPeer

DisconnectPeer disconnects a peer by target address. Both outbound and inbound nodes are searched for the target node, and an error is returned if the peer was not found. ([source](../../raw/api/api-docs/api/lnd/neutrino-kit/disconnect-peer.md))

- gRPC: `rpc DisconnectPeer (DisconnectPeerRequest) returns (DisconnectPeerResponse);`
- REST: `POST /v2/neutrino/disconnect`
- Request: `neutrinorpc.DisconnectPeerRequest`, field `peer_addrs`
- Response: `neutrinorpc.DisconnectPeerResponse` (no parameters)

([source](../../raw/api/api-docs/api/lnd/neutrino-kit/disconnect-peer.md))

## IsBanned

IsBanned returns true if the peer is banned, otherwise false. ([source](../../raw/api/api-docs/api/lnd/neutrino-kit/is-banned.md))

- gRPC: `rpc IsBanned (IsBannedRequest) returns (IsBannedResponse);`
- REST: `GET /v2/neutrino/isbanned`
- Request: `neutrinorpc.IsBannedRequest`, field `peer_addrs` (query)
- Response: `neutrinorpc.IsBannedResponse`, field `banned`

([source](../../raw/api/api-docs/api/lnd/neutrino-kit/is-banned.md))

## GetBlockHeader

GetBlockHeader returns a block header with a particular block hash. ([source](../../raw/api/api-docs/api/lnd/neutrino-kit/get-block-header.md))

- gRPC: `rpc GetBlockHeader (GetBlockHeaderRequest) returns (GetBlockHeaderResponse);`
- REST: `GET /v2/neutrino/blockheader/{hash}`
- Request: `neutrinorpc.GetBlockHeaderRequest`, field `hash` (block hash in hex notation, path)
- Response: `neutrinorpc.GetBlockHeaderResponse`, fields `hash`, `confirmations`, `stripped_size`, `size`, `weight`, `height`, `version`, `version_hex`, `merkleroot`, `time`, `nonce`, `bits`, `ntx`, `previous_block_hash`, `raw_hex`

([source](../../raw/api/api-docs/api/lnd/neutrino-kit/get-block-header.md))

## GetBlock

GetBlock returns a block with a particular block hash. ([source](../../raw/api/api-docs/api/lnd/neutrino-kit/get-block.md))

- gRPC: `rpc GetBlock (GetBlockRequest) returns (GetBlockResponse);`
- REST: `GET /v2/neutrino/block/{hash}`
- Request: `neutrinorpc.GetBlockRequest`, field `hash` (block hash in hex notation, path)
- Response: `neutrinorpc.GetBlockResponse`, the same fields as the header response plus `tx` (list of transaction ids)

([source](../../raw/api/api-docs/api/lnd/neutrino-kit/get-block.md))

## GetCFilter

GetCFilter returns a compact filter from a block. ([source](../../raw/api/api-docs/api/lnd/neutrino-kit/get-c-filter.md))

- gRPC: `rpc GetCFilter (GetCFilterRequest) returns (GetCFilterResponse);`
- REST: `GET /v2/neutrino/cfilter/{hash}`
- Request: `neutrinorpc.GetCFilterRequest`, field `hash` (block hash in hex notation, path)
- Response: `neutrinorpc.GetCFilterResponse`, field `filter` (GCS filter)

([source](../../raw/api/api-docs/api/lnd/neutrino-kit/get-c-filter.md))

## GetBlockHash (deprecated)

This RPC is deprecated and will be removed in a future version; the page says to use `chainrpc.GetBlockHash` instead (see [[lnd-chain-kit]]). GetBlockHash returns the header hash of a block at a given height. ([source](../../raw/api/api-docs/api/lnd/neutrino-kit/get-block-hash.md))

- gRPC: `rpc GetBlockHash (GetBlockHashRequest) returns (GetBlockHashResponse);`
- REST: `GET /v2/neutrino/blockhash/{height}`
- Request: `neutrinorpc.GetBlockHashRequest`, field `height` (`int32`, path)
- Response: `neutrinorpc.GetBlockHashResponse`, field `hash`

([source](../../raw/api/api-docs/api/lnd/neutrino-kit/get-block-hash.md))
