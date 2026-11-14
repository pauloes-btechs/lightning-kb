---
title: pool hash-mail service
type: service
sources:
  - raw/api/api-docs/api/pool.md
  - raw/api/api-docs/api/pool/rest-endpoints.md
  - raw/api/api-docs/api/pool/hash-mail/del-cipher-box.md
  - raw/api/api-docs/api/pool/hash-mail/new-cipher-box.md
  - raw/api/api-docs/api/pool/hash-mail/recv-stream.md
  - raw/api/api-docs/api/pool/hash-mail/send-stream.md
updated: 2026-11-14
---

# pool hash-mail service

The hash-mail service is a gRPC service in the API reference of [[pool]]. The Pool overview page lists three `*.proto` files from which the gRPC documentation was generated, `auctioneerrpc/auctioneer.proto`, `auctioneerrpc/hashmail.proto` and `poolrpc/trader.proto`, and says the reference was generated automatically against commit `561c94bda9d5816e51205b5a7b15dce66520f39b` of the `lightninglabs/pool` repository. ([source](../../raw/api/api-docs/api/pool.md)) The "Source:" link on each of the four RPC pages names `auctioneerrpc/hashmail.proto`. ([source](../../raw/api/api-docs/api/pool/hash-mail/new-cipher-box.md), [source](../../raw/api/api-docs/api/pool/hash-mail/del-cipher-box.md), [source](../../raw/api/api-docs/api/pool/hash-mail/send-stream.md), [source](../../raw/api/api-docs/api/pool/hash-mail/recv-stream.md))

See also: [[pool-trader]], [[pool-channel-auctioneer]].

The service has four RPCs that create, tear down, write to and read from a "cipher box" pipe/stream: NewCipherBox, DelCipherBox, SendStream and RecvStream. ([source](../../raw/api/api-docs/api/pool/hash-mail/new-cipher-box.md), [source](../../raw/api/api-docs/api/pool/hash-mail/del-cipher-box.md), [source](../../raw/api/api-docs/api/pool/hash-mail/send-stream.md), [source](../../raw/api/api-docs/api/pool/hash-mail/recv-stream.md))

None of the four RPC pages has a REST section. ([source](../../raw/api/api-docs/api/pool/hash-mail/new-cipher-box.md), [source](../../raw/api/api-docs/api/pool/hash-mail/del-cipher-box.md), [source](../../raw/api/api-docs/api/pool/hash-mail/send-stream.md), [source](../../raw/api/api-docs/api/pool/hash-mail/recv-stream.md))

The REST Endpoints page for Pool lists no path for these RPCs. ([source](../../raw/api/api-docs/api/pool/rest-endpoints.md))

## NewCipherBox

NewCipherBox creates a new cipher box pipe/stream given a valid authentication mechanism. If the authentication mechanism has been revoked, or needs to be changed, then a CipherChallenge message is returned. Otherwise the method will either be accepted or rejected. ([source](../../raw/api/api-docs/api/pool/hash-mail/new-cipher-box.md))

- gRPC: `rpc NewCipherBox (CipherBoxAuth) returns (CipherInitResp);`
- REST: none listed on the page
- Request message: `poolrpc.CipherBoxAuth`
- Response message: `poolrpc.CipherInitResp`

The request fields are `desc`, a `CipherBoxDesc` (field `stream_id`) describing the stream one is attempting to initialize, `acct_auth` and `sidecar_auth`. `acct_auth` is a `PoolAccountAuth` with `acct_key`, the account key being used to authenticate, and `stream_sig`, a valid signature over the stream ID being used. `sidecar_auth` is a `SidecarAuth` with `ticket`, a valid sidecar ticket that has been signed (offered) by a Pool account in the active state. ([source](../../raw/api/api-docs/api/pool/hash-mail/new-cipher-box.md))

The response fields are `success` (CipherSuccess is returned if the initialization of the cipher box was successful), `challenge` (CipherChallenge is returned if the authentication mechanism was revoked or needs to be refreshed) and `error` (CipherError is returned if the authentication mechanism failed to validate). `CipherSuccess` has a `desc` field; `CipherChallenge` and `CipherError` have no parameters. ([source](../../raw/api/api-docs/api/pool/hash-mail/new-cipher-box.md))

## DelCipherBox

DelCipherBox attempts to tear down an existing cipher box pipe. The same authentication mechanism used to initially create the stream MUST be specified. ([source](../../raw/api/api-docs/api/pool/hash-mail/del-cipher-box.md))

- gRPC: `rpc DelCipherBox (CipherBoxAuth) returns (DelCipherBoxResp);`
- REST: none listed on the page
- Request message: `poolrpc.CipherBoxAuth`
- Response message: `poolrpc.DelCipherBoxResp` (no parameters)

The request is the same `CipherBoxAuth` message as for NewCipherBox, with `desc`, `acct_auth` and `sidecar_auth`. ([source](../../raw/api/api-docs/api/pool/hash-mail/del-cipher-box.md))

## SendStream

SendStream opens up the write side of the passed CipherBox pipe. Writes will be non-blocking up to the buffer size of the pipe. Beyond that writes will block until completed. ([source](../../raw/api/api-docs/api/pool/hash-mail/send-stream.md))

- gRPC (client-streaming): `rpc SendStream (stream CipherBox) returns (CipherBoxDesc);`
- REST: none listed on the page
- Request message: `poolrpc.CipherBox`
- Response message: `poolrpc.CipherBoxDesc`

Each `CipherBox` has `desc` (a `CipherBoxDesc`) and `msg` (bytes). The response has the single field `stream_id`. ([source](../../raw/api/api-docs/api/pool/hash-mail/send-stream.md))

## RecvStream

RecvStream opens up the read side of the passed CipherBox pipe. This method will block until a full message has been read as this is a message based pipe/stream abstraction. ([source](../../raw/api/api-docs/api/pool/hash-mail/recv-stream.md))

- gRPC (server-streaming): `rpc RecvStream (CipherBoxDesc) returns (stream CipherBox);`
- REST: none listed on the page
- Request message: `poolrpc.CipherBoxDesc`
- Response message: `poolrpc.CipherBox`

The request has the single field `stream_id`; each streamed `CipherBox` has `desc` and `msg`. ([source](../../raw/api/api-docs/api/pool/hash-mail/recv-stream.md))

## Notes

These are editorial observations, not statements from the sources.

- The reference pages do not say what the cipher box streams are used for or who runs this service. The only hints are the two authentication options: a Pool account key (see [[pool-accounts]]) or a sidecar ticket (see [[sidecar-channels]] and the sidecar RPCs on [[pool-trader]]).
- The Pool overview page lists an `auctioneerrpc/hashmail.swagger.json` file, but no REST path for this service appears in the reference.
