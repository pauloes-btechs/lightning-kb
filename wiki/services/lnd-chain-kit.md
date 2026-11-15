---
title: lnd chain-kit service
type: service
sources:
  - raw/api/api-docs/api/lnd.md
  - raw/api/api-docs/api/lnd/rest-endpoints.md
  - raw/api/api-docs/api/lnd/chain-kit/get-best-block.md
  - raw/api/api-docs/api/lnd/chain-kit/get-block-hash.md
  - raw/api/api-docs/api/lnd/chain-kit/get-block-header.md
  - raw/api/api-docs/api/lnd/chain-kit/get-block.md
updated: 2026-11-14
---

# lnd chain-kit service (ChainKit)

This page covers the ChainKit service of [[lnd]]. GetBlock returns a block given the corresponding block hash, and its page gives `chainrpc/chainkit.proto` as its source. ([source](../../raw/api/api-docs/api/lnd/chain-kit/get-block.md))

The lnd API overview lists Service *ChainKit* (file: `chainrpc/chainkit.proto`) among the experimental services, which are subject to change and need a compile-time flag to be active (they are active in the official release binaries). The reference was generated against commit `895118ac4ec59e78b2c14f5b0d31ac6f862434bb`. ([source](../../raw/api/api-docs/api/lnd.md))

The REST endpoints page lists four `chainrpc` ChainKit RPCs under `/v2/chainkit/`: GetBestBlock, GetBlock, GetBlockHash and GetBlockHeader. ([source](../../raw/api/api-docs/api/lnd/rest-endpoints.md))

See also: [[lnd-chain-notifier]], [[lnd-neutrino-kit]].

## GetBlock

GetBlock returns a block given the corresponding block hash. ([source](../../raw/api/api-docs/api/lnd/chain-kit/get-block.md))

- gRPC: `rpc GetBlock (GetBlockRequest) returns (GetBlockResponse);`
- REST: `GET /v2/chainkit/block`
- Request: `chainrpc.GetBlockRequest`, field `block_hash` (query)
- Response: `chainrpc.GetBlockResponse`, field `raw_block` (the raw bytes of the requested block)

([source](../../raw/api/api-docs/api/lnd/chain-kit/get-block.md))

## GetBlockHeader

GetBlockHeader returns a block header with a particular block hash. ([source](../../raw/api/api-docs/api/lnd/chain-kit/get-block-header.md))

- gRPC: `rpc GetBlockHeader (GetBlockHeaderRequest) returns (GetBlockHeaderResponse);`
- REST: `GET /v2/chainkit/blockheader`
- Request: `chainrpc.GetBlockHeaderRequest`, field `block_hash` (query)
- Response: `chainrpc.GetBlockHeaderResponse`, field `raw_block_header`

([source](../../raw/api/api-docs/api/lnd/chain-kit/get-block-header.md))

## GetBestBlock

GetBestBlock returns the block hash and current height from the valid most-work chain. ([source](../../raw/api/api-docs/api/lnd/chain-kit/get-best-block.md))

- gRPC: `rpc GetBestBlock (GetBestBlockRequest) returns (GetBestBlockResponse);`
- REST: `GET /v2/chainkit/bestblock`
- Request: `chainrpc.GetBestBlockRequest` (no parameters)
- Response: `chainrpc.GetBestBlockResponse`, fields `block_hash` and `block_height`

([source](../../raw/api/api-docs/api/lnd/chain-kit/get-best-block.md))

## GetBlockHash

GetBlockHash returns the hash of the block in the best blockchain at the given height. ([source](../../raw/api/api-docs/api/lnd/chain-kit/get-block-hash.md))

- gRPC: `rpc GetBlockHash (GetBlockHashRequest) returns (GetBlockHashResponse);`
- REST: `GET /v2/chainkit/blockhash`
- Request: `chainrpc.GetBlockHashRequest`, field `block_height` (`int64`, query)
- Response: `chainrpc.GetBlockHashResponse`, field `block_hash`

([source](../../raw/api/api-docs/api/lnd/chain-kit/get-block-hash.md))
