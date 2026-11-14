---
title: loop debug service
type: service
sources:
  - raw/api/api-docs/api/loop.md
  - raw/api/api-docs/api/loop/debug/force-auto-loop.md
updated: 2026-11-14
---

# loop debug service (Debug)

This page covers the RPC under `debug` in the API reference of [[loop]]; the other Loop RPCs are on [[loop-swap-client]]. The reference was generated automatically against commit `9158aed2a8347d78585faa2e7a89a08f66692a09` of the `lightninglabs/loop` repository. ([source](../../raw/api/api-docs/api/loop.md)) ForceAutoLoop gives `looprpc/debug.proto` as its source. ([source](../../raw/api/api-docs/api/loop/debug/force-auto-loop.md))

The reference lists one RPC for this service, ForceAutoLoop. ([source](../../raw/api/api-docs/api/loop/debug/force-auto-loop.md))

## ForceAutoLoop

ForceAutoLoop is intended for *testing purposes only* and will not work on mainnet. This endpoint ticks our autoloop timer, triggering automated dispatch of a swap if one is suggested. ([source](../../raw/api/api-docs/api/loop/debug/force-auto-loop.md))

- gRPC: `rpc ForceAutoLoop (ForceAutoLoopRequest) returns (ForceAutoLoopResponse);`
- REST: none listed on the page
- Request message: `looprpc.ForceAutoLoopRequest`
- Response message: `looprpc.ForceAutoLoopResponse`

Neither the request nor the response has parameters. ([source](../../raw/api/api-docs/api/loop/debug/force-auto-loop.md))

See [[autoloop]] for what the autoloop timer dispatches, and SuggestSwaps on [[loop-swap-client]] for the suggestions it acts on.
