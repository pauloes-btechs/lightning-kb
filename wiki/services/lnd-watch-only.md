---
title: lnd watch-only service
type: service
sources:
  - raw/api/api-docs/api/lnd.md
  - raw/api/api-docs/api/lnd/rest-endpoints.md
  - raw/api/api-docs/api/lnd/watch-only/sign-coordinator-streams.md
  - raw/api/api-docs/api/lnd/wallet-unlocker/init-wallet.md
updated: 2026-11-14
---

# lnd watch-only service

The WatchOnly service of [[lnd]] has a single RPC, SignCoordinatorStreams, exposed over REST at `POST /v2/watchonly/stream` ([source](../../raw/api/api-docs/api/lnd/rest-endpoints.md)).

It is defined in `watchonlyrpc/watchonly.proto`; the reference was generated from lnd commit `895118ac4ec59e78b2c14f5b0d31ac6f862434bb` ([source](../../raw/api/api-docs/api/lnd/watch-only/sign-coordinator-streams.md)) ([source](../../raw/api/api-docs/api/lnd.md)).

A watch-only wallet is created through InitWallet's `watch_only` field by importing account xpubs only; such a wallet holds no private keys and needs to be run with a remote signer that has the corresponding private keys ([source](../../raw/api/api-docs/api/lnd/wallet-unlocker/init-wallet.md)). See [[lnd-wallet-unlocker]].

## SignCoordinatorStreams

SignCoordinatorStreams dispatches a bi-directional streaming RPC that allows a remote signer to connect to a watch-only node and remotely provide signatures and ECDH results on demand ([source](../../raw/api/api-docs/api/lnd/watch-only/sign-coordinator-streams.md)).

- gRPC (bidirectional streaming): `rpc SignCoordinatorStreams (stream SignCoordinatorResponse) returns (stream SignCoordinatorRequest);`
- REST: `POST /v2/watchonly/stream`
- Note the direction: the client (remote signer) streams `watchonlyrpc.SignCoordinatorResponse` messages and receives `watchonlyrpc.SignCoordinatorRequest` messages.

([source](../../raw/api/api-docs/api/lnd/watch-only/sign-coordinator-streams.md))

`watchonlyrpc.SignCoordinatorRequest` (sent by the watch-only lnd) carries `request_id` (request_id 1 is reserved for the handshake), `registration_response`, `ping`, and one request per signing operation: `shared_key_request`, `sign_message_req`, `mu_sig2_session_request`, `mu_sig2_register_nonces_request`, `mu_sig2_combined_nonces_req`, `mu_sig2_get_combined_nonces_req`, `mu_sig2_sign_request`, `mu_sig2_combine_sig_request`, `mu_sig2_cleanup_request`, `sign_psbt_request` ([source](../../raw/api/api-docs/api/lnd/watch-only/sign-coordinator-streams.md)).

`watchonlyrpc.SignCoordinatorResponse` (sent by the remote signer) carries `ref_request_id`, `signer_registration` (sent on connect to start the handshake), `pong`, the matching responses `shared_key_response`, `sign_message_resp`, `mu_sig2_session_response`, `mu_sig2_register_nonces_response`, `mu_sig2_comb_nonces_resp`, `mu_sig2_get_comb_nonces_resp`, `mu_sig2_sign_response`, `mu_sig2_combine_sig_response`, `mu_sig2_cleanup_response`, `sign_psbt_response`, and `signer_error` ([source](../../raw/api/api-docs/api/lnd/watch-only/sign-coordinator-streams.md)).

The nested payloads are `signrpc` messages (for example `SharedKeyRequest`, `SignMessageReq`, `MuSig2SessionRequest`) and `walletrpc.SignPsbtRequest` / `walletrpc.SignPsbtResponse` ([source](../../raw/api/api-docs/api/lnd/watch-only/sign-coordinator-streams.md)).
## Related

See also: [[lnd]], [[lnd-signer]], [[lnd-wallet-kit]], [[lnd-wallet-unlocker]].
