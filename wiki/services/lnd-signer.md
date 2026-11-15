---
title: lnd signer service
type: service
sources:
  - raw/api/api-docs/api/lnd.md
  - raw/api/api-docs/api/lnd/rest-endpoints.md
  - raw/api/api-docs/api/lnd/signer/sign-output-raw.md
  - raw/api/api-docs/api/lnd/signer/compute-input-script.md
  - raw/api/api-docs/api/lnd/signer/sign-message.md
  - raw/api/api-docs/api/lnd/signer/verify-message.md
  - raw/api/api-docs/api/lnd/signer/derive-shared-key.md
  - raw/api/api-docs/api/lnd/signer/mu-sig2-combine-keys.md
  - raw/api/api-docs/api/lnd/signer/mu-sig2-create-session.md
  - raw/api/api-docs/api/lnd/signer/mu-sig2-register-nonces.md
  - raw/api/api-docs/api/lnd/signer/mu-sig2-register-combined-nonce.md
  - raw/api/api-docs/api/lnd/signer/mu-sig2-get-combined-nonce.md
  - raw/api/api-docs/api/lnd/signer/mu-sig2-sign.md
  - raw/api/api-docs/api/lnd/signer/mu-sig2-combine-sig.md
  - raw/api/api-docs/api/lnd/signer/mu-sig2-cleanup.md
updated: 2026-11-14
---

# lnd signer service

The Signer service of [[lnd]] (package `signrpc`) has 13 RPCs: SignOutputRaw, ComputeInputScript, SignMessage, VerifyMessage, DeriveSharedKey and eight MuSig2 RPCs (MuSig2CombineKeys, MuSig2CreateSession, MuSig2RegisterNonces, MuSig2RegisterCombinedNonce, MuSig2GetCombinedNonce, MuSig2Sign, MuSig2CombineSig, MuSig2Cleanup). All are `POST` under `/v2/signer/` ([source](../../raw/api/api-docs/api/lnd/rest-endpoints.md)).

It is defined in `signrpc/signer.proto`; the reference was generated from lnd commit `895118ac4ec59e78b2c14f5b0d31ac6f862434bb` ([source](../../raw/api/api-docs/api/lnd/signer/sign-output-raw.md)). The lnd API overview lists Service *Signer* (file `signrpc/signer.proto`) among the experimental services, which need a compile-time flag to be active (they are active in the official release binaries) ([source](../../raw/api/api-docs/api/lnd.md)).

## SignOutputRaw

Generates a signature for a set of inputs/outputs to a transaction. Each request specifies how the outputs should be signed, with which keys, and any optional tweaks. The return value is a fixed 64-byte signature; if lnd cannot sign with the specified keys an error is returned ([source](../../raw/api/api-docs/api/lnd/signer/sign-output-raw.md)).

- gRPC: `rpc SignOutputRaw (SignReq) returns (SignResp);`
- REST: `POST /v2/signer/signraw`
- Request `signrpc.SignReq`: `raw_tx_bytes`, `sign_descs` (`SignDescriptor[]`), `prev_outputs` (required when spending taproot outputs). Response `signrpc.SignResp`: `raw_sigs`.

([source](../../raw/api/api-docs/api/lnd/signer/sign-output-raw.md))

## ComputeInputScript

Generates a complete input script for the passed transaction with the signature defined in the passed SignDescriptor, for regular p2wkh/p2tr outputs and p2wkh nested in p2sh. For wallet inputs only `pkScript` and value in the TxOut field and the input index need to be populated ([source](../../raw/api/api-docs/api/lnd/signer/compute-input-script.md)).

- gRPC: `rpc ComputeInputScript (SignReq) returns (InputScriptResp);`
- REST: `POST /v2/signer/inputscript`
- Request `signrpc.SignReq`; response `signrpc.InputScriptResp`: `input_scripts`.

([source](../../raw/api/api-docs/api/lnd/signer/compute-input-script.md))

## SignMessage

Signs a message with the key specified in the key locator; the signature is fixed-size LN wire format encoded. Unlike SignMessage in the main RPC, a specific key is used instead of the node identity private key ([source](../../raw/api/api-docs/api/lnd/signer/sign-message.md)).

- gRPC: `rpc SignMessage (SignMessageReq) returns (SignMessageResp);`
- REST: `POST /v2/signer/signmessage`
- Request `signrpc.SignMessageReq`: `msg`, `key_loc`, `double_hash`, `compact_sig` (not with Schnorr), `schnorr_sig`, `schnorr_sig_tap_tweak`, `tag` (only with `schnorr_sig`). Response `signrpc.SignMessageResp`: `signature`.

([source](../../raw/api/api-docs/api/lnd/signer/sign-message.md))

## VerifyMessage

Verifies a fixed-size LN wire format signature over a message using the provided public key. Unlike VerifyMessage in the main RPC, the key does not have to belong to a node known to the network ([source](../../raw/api/api-docs/api/lnd/signer/verify-message.md)).

- gRPC: `rpc VerifyMessage (VerifyMessageReq) returns (VerifyMessageResp);`
- REST: `POST /v2/signer/verifymessage`
- Request `signrpc.VerifyMessageReq`: `msg`, `signature`, `pubkey` (32-byte x-only when `is_schnorr_sig` is true), `is_schnorr_sig`, `tag`. Response `signrpc.VerifyMessageResp`: `valid`.

([source](../../raw/api/api-docs/api/lnd/signer/verify-message.md))

## DeriveSharedKey

Returns a shared secret by Diffie-Hellman between the request's ephemeral public key and the node key given in `key_desc` (defaults to the node identity private key). The shared public key is serialized compressed and hashed with sha256, giving a 256-bit key ([source](../../raw/api/api-docs/api/lnd/signer/derive-shared-key.md)).

- gRPC: `rpc DeriveSharedKey (SharedKeyRequest) returns (SharedKeyResponse);`
- REST: `POST /v2/signer/sharedkey`
- Request `signrpc.SharedKeyRequest`: `ephemeral_pubkey`, `key_loc` (deprecated), `key_desc`. Response `signrpc.SharedKeyResponse`: `shared_key`.

([source](../../raw/api/api-docs/api/lnd/signer/derive-shared-key.md))

## MuSig2 RPCs

Each MuSig2 RPC page carries the note that the MuSig2 BIP is not final, so the API must be considered HIGHLY EXPERIMENTAL and backward compatibility is not guaranteed ([1](../../raw/api/api-docs/api/lnd/signer/mu-sig2-combine-keys.md), [2](../../raw/api/api-docs/api/lnd/signer/mu-sig2-create-session.md), [3](../../raw/api/api-docs/api/lnd/signer/mu-sig2-register-nonces.md), [4](../../raw/api/api-docs/api/lnd/signer/mu-sig2-register-combined-nonce.md), [5](../../raw/api/api-docs/api/lnd/signer/mu-sig2-get-combined-nonce.md), [6](../../raw/api/api-docs/api/lnd/signer/mu-sig2-sign.md), [7](../../raw/api/api-docs/api/lnd/signer/mu-sig2-combine-sig.md), [8](../../raw/api/api-docs/api/lnd/signer/mu-sig2-cleanup.md)).

### MuSig2CombineKeys

A stateless, deterministic helper that calculates the combined MuSig2 public key from all signers' public keys without creating a signing session, e.g. to determine the Taproot key for an on-chain output ([source](../../raw/api/api-docs/api/lnd/signer/mu-sig2-combine-keys.md)).

- gRPC: `rpc MuSig2CombineKeys (MuSig2CombineKeysRequest) returns (MuSig2CombineKeysResponse);`
- REST: `POST /v2/signer/musig2/combinekeys`
- Request: `all_signer_pubkeys`, `tweaks`, `taproot_tweak`, `version` (mandatory). Response: `combined_key`, `taproot_internal_key`, `version`.

([source](../../raw/api/api-docs/api/lnd/signer/mu-sig2-combine-keys.md))

### MuSig2CreateSession

Creates a new MuSig2 signing session using the local key identified by the key locator. All signers' public keys, including the local one, must be provided; known nonces of other parties can be submitted too ([source](../../raw/api/api-docs/api/lnd/signer/mu-sig2-create-session.md)).

- gRPC: `rpc MuSig2CreateSession (MuSig2SessionRequest) returns (MuSig2SessionResponse);`
- REST: `POST /v2/signer/musig2/createsession`
- Request `signrpc.MuSig2SessionRequest`: `key_loc`, `all_signer_pubkeys`, `other_signer_public_nonces`, `tweaks`, `taproot_tweak`, `version`, `pregenerated_local_nonce` (optional, must be 97 bytes). Response `signrpc.MuSig2SessionResponse`: `session_id` (a session produces a signature a single time), `combined_key`, `taproot_internal_key`, `local_public_nonces` (66 bytes), `have_all_nonces`, `version`.

([source](../../raw/api/api-docs/api/lnd/signer/mu-sig2-create-session.md))

### MuSig2RegisterNonces

Registers one or more public nonces of other participants for a session; can be called repeatedly until all nonces are registered ([source](../../raw/api/api-docs/api/lnd/signer/mu-sig2-register-nonces.md)).

- gRPC: `rpc MuSig2RegisterNonces (MuSig2RegisterNoncesRequest) returns (MuSig2RegisterNoncesResponse);`
- REST: `POST /v2/signer/musig2/registernonces`
- Request: `session_id`, `other_signer_public_nonces`. Response: `have_all_nonces`.

([source](../../raw/api/api-docs/api/lnd/signer/mu-sig2-register-nonces.md))

### MuSig2RegisterCombinedNonce

Registers a pre-aggregated combined nonce for a session, as an alternative to MuSig2RegisterNonces when a coordinator has already aggregated all nonces. It is mutually exclusive with MuSig2RegisterNonces for the same session ([source](../../raw/api/api-docs/api/lnd/signer/mu-sig2-register-combined-nonce.md)).

- gRPC: `rpc MuSig2RegisterCombinedNonce (MuSig2RegisterCombinedNonceRequest) returns (MuSig2RegisterCombinedNonceResponse);`
- REST: `POST /v2/signer/musig2/registercombinednonce`
- Request: `session_id`, `combined_public_nonce` (66 bytes, R1 || R2). Response: no parameters.

([source](../../raw/api/api-docs/api/lnd/signer/mu-sig2-register-combined-nonce.md))

### MuSig2GetCombinedNonce

Retrieves the combined nonce for a session, available once all nonces were registered via MuSig2RegisterNonces or a combined nonce via MuSig2RegisterCombinedNonce ([source](../../raw/api/api-docs/api/lnd/signer/mu-sig2-get-combined-nonce.md)).

- gRPC: `rpc MuSig2GetCombinedNonce (MuSig2GetCombinedNonceRequest) returns (MuSig2GetCombinedNonceResponse);`
- REST: `POST /v2/signer/musig2/getcombinednonce`
- Request: `session_id`. Response: `combined_public_nonce`.

([source](../../raw/api/api-docs/api/lnd/signer/mu-sig2-get-combined-nonce.md))

### MuSig2Sign

Creates a partial signature with the session's local key; only callable once all participants' nonces are registered. If this node does not combine the partial signatures, set the cleanup flag so the session can be removed after signing ([source](../../raw/api/api-docs/api/lnd/signer/mu-sig2-sign.md)).

- gRPC: `rpc MuSig2Sign (MuSig2SignRequest) returns (MuSig2SignResponse);`
- REST: `POST /v2/signer/musig2/sign`
- Request: `session_id`, `message_digest` (32-byte SHA256), `cleanup`. Response: `local_partial_signature`.

([source](../../raw/api/api-docs/api/lnd/signer/mu-sig2-sign.md))

### MuSig2CombineSig

Combines the given partial signature(s) with the local one; once all participants' partial signatures are registered, the final signature is returned ([source](../../raw/api/api-docs/api/lnd/signer/mu-sig2-combine-sig.md)).

- gRPC: `rpc MuSig2CombineSig (MuSig2CombineSigRequest) returns (MuSig2CombineSigResponse);`
- REST: `POST /v2/signer/musig2/combinesig`
- Request: `session_id`, `other_partial_signatures`. Response: `have_all_signatures`, `final_signature`.

([source](../../raw/api/api-docs/api/lnd/signer/mu-sig2-combine-sig.md))

### MuSig2Cleanup

Cleans up a session early when it will clearly not succeed, releasing its resources ([source](../../raw/api/api-docs/api/lnd/signer/mu-sig2-cleanup.md)).

- gRPC: `rpc MuSig2Cleanup (MuSig2CleanupRequest) returns (MuSig2CleanupResponse);`
- REST: `POST /v2/signer/musig2/cleanup`
- Request: `session_id`. Response: no parameters.

([source](../../raw/api/api-docs/api/lnd/signer/mu-sig2-cleanup.md))

## Related

See also: [[lnd]], [[lnd-lightning]], [[lnd-wallet-kit]], [[lnd-watch-only]], [[lnd-wallet-and-psbt]].
