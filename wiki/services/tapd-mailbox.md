---
title: taproot-assets mailbox service
type: service
sources:
  - raw/api/api-docs/api/taproot-assets.md
  - raw/api/api-docs/api/taproot-assets/rest-endpoints.md
  - raw/api/api-docs/api/taproot-assets/mailbox/send-message.md
  - raw/api/api-docs/api/taproot-assets/mailbox/receive-messages.md
  - raw/api/api-docs/api/taproot-assets/mailbox/mailbox-info.md
  - raw/api/api-docs/api/taproot-assets/mailbox/remove-message.md
updated: 2026-11-14
---

# taproot-assets mailbox service

The mailbox service is a gRPC service in the API reference of [[taproot-assets]]. The Taproot Assets overview page lists `authmailboxrpc/mailbox.proto` among the `*.proto` files from which the gRPC documentation was generated, and says the reference was generated automatically against commit `14aa3fd90e6aace4d3b2cfc72a51d15ce4afd891` of the `lightninglabs/taproot-assets` repository. ([source](../../raw/api/api-docs/api/taproot-assets.md)) The "Source:" link on each RPC page of this service names `authmailboxrpc/mailbox.proto`, and the request message on each page carries the `authmailboxrpc.` prefix. ([source](../../raw/api/api-docs/api/taproot-assets/mailbox/send-message.md), [source](../../raw/api/api-docs/api/taproot-assets/mailbox/receive-messages.md), [source](../../raw/api/api-docs/api/taproot-assets/mailbox/mailbox-info.md), [source](../../raw/api/api-docs/api/taproot-assets/mailbox/remove-message.md))

The reference has four RPCs for this service: SendMessage, ReceiveMessages, MailboxInfo, RemoveMessage. ([source](../../raw/api/api-docs/api/taproot-assets/mailbox/send-message.md), [source](../../raw/api/api-docs/api/taproot-assets/mailbox/receive-messages.md), [source](../../raw/api/api-docs/api/taproot-assets/mailbox/mailbox-info.md), [source](../../raw/api/api-docs/api/taproot-assets/mailbox/remove-message.md))

Every one of these RPC pages has a REST section, and the REST Endpoints page lists the same paths under `/v1/taproot-assets/` against the `authmailboxrpc.` RPC names. ([source](../../raw/api/api-docs/api/taproot-assets/rest-endpoints.md), [source](../../raw/api/api-docs/api/taproot-assets/mailbox/send-message.md), [source](../../raw/api/api-docs/api/taproot-assets/mailbox/receive-messages.md), [source](../../raw/api/api-docs/api/taproot-assets/mailbox/mailbox-info.md), [source](../../raw/api/api-docs/api/taproot-assets/mailbox/remove-message.md))

See also: [[tapd-asset-wallet]], [[tapd-taproot-assets]], [[tapd-universe]].

## SendMessage

SendMessage sends a single message to a receiver's mailbox. It requires a valid, unused Bitcoin P2TR transaction outpoint as proof of uniqueness, included in a block as proof of work. ([source](../../raw/api/api-docs/api/taproot-assets/mailbox/send-message.md))

- gRPC: `rpc SendMessage (SendMessageRequest) returns (SendMessageResponse);`
- REST: `POST /v1/taproot-assets/mailbox/send`
- Request message: `authmailboxrpc.SendMessageRequest`
- Response message: `authmailboxrpc.SendMessageResponse`

The request fields are `receiver_id` (the public key identifier of the intended receiver, encoded as the raw bytes of the compressed public key), `encrypted_payload` (the ECIES encrypted message payload) and `tx_proof`, a `BitcoinMerkleInclusionProof` used as the sender's authentication. The response has one field, `message_id`, the unique ID assigned to the stored message by the server. ([source](../../raw/api/api-docs/api/taproot-assets/mailbox/send-message.md))

The page says the server MUST perform full validation of `tx_proof`: verify claimed\_outpoint.txid\_hex matches hash(raw\_tx\_data); verify claimed\_outpoint.index is valid for the transaction; verify merkle\_proof connects the transaction hash to the raw\_block\_header\_data's Merkle root; verify block\_header validity (e.g., PoW, potentially chain context); and ensure the claimed\_outpoint has not been used previously (check used\_proofs table). ([source](../../raw/api/api-docs/api/taproot-assets/mailbox/send-message.md))

`BitcoinMerkleInclusionProof` has the fields `raw_tx_data`, `raw_block_header_data`, `block_height`, `merkle_proof`, `claimed_outpoint`, `internal_key` and `merkle_root`. The output at the claimed index must be a P2TR output. If `merkle_root` is not provided (empty or nil), a BIP-0086 construction is assumed. `MerkleProof` has `sibling_hashes` and `bits`. ([source](../../raw/api/api-docs/api/taproot-assets/mailbox/send-message.md))

## ReceiveMessages

ReceiveMessages initiates a bidirectional stream to receive messages for a specific receiver. The stream implements the challenge-response handshake required for receiver authentication before messages are delivered. The page marks it as a bidirectional-streaming RPC. ([source](../../raw/api/api-docs/api/taproot-assets/mailbox/receive-messages.md))

- gRPC: `rpc ReceiveMessages (stream ReceiveMessagesRequest) returns (stream ReceiveMessagesResponse);`
- REST: `POST /v1/taproot-assets/mailbox/receive`
- Request message: `authmailboxrpc.ReceiveMessagesRequest`
- Response message: `authmailboxrpc.ReceiveMessagesResponse`

The expected flow given on the page is the following. ([source](../../raw/api/api-docs/api/taproot-assets/mailbox/receive-messages.md))

1. Client -> Server: ReceiveMessagesRequest(init = InitReceive{...})
2. Server -> Client: ReceiveMessagesResponse(challenge = Challenge{...})
3. Client -> Server: ReceiveMessagesRequest(auth\_sig = AuthSignature{...})
4. Server -> Client: [Stream of ReceiveMessagesResponse(message = MailboxMessage{...})]
5. Server -> Client: ReceiveMessagesResponse(eos = EndOfStream{}) ([source](../../raw/api/api-docs/api/taproot-assets/mailbox/receive-messages.md))

The request fields are `init` (an `InitReceive`, the initial parameters sent by the client to start receiving messages) and `auth_sig` (an `AuthSignature`, the client's signature in response to the server's challenge; its `signature` field is the client's Schnorr signature over the challenge hash provided by the server). ([source](../../raw/api/api-docs/api/taproot-assets/mailbox/receive-messages.md))

`InitReceive` has `receiver_id`, `start_message_id_exclusive`, `start_block_height_inclusive` and `start_timestamp_exclusive`. The page states that one of `start_message_id_exclusive`, `start_block_height_inclusive` or `start_timestamp_exclusive` must be at their non-default values for any existing messages to be returned. ([source](../../raw/api/api-docs/api/taproot-assets/mailbox/receive-messages.md))

The response fields are `challenge` (a `Challenge` with `challenge_hash`, which the client must sign to prove ownership of the receiver's public key), `auth_success`, `messages` (a `MailboxMessages`, a list of `MailboxMessage`) and `eos` (an `EndOfStream` message indicating that the server is shutting down). `MailboxMessage` has `message_id`, `encrypted_payload` (the ECIES encrypted message payload, intended for the receiver) and `arrival_timestamp`. ([source](../../raw/api/api-docs/api/taproot-assets/mailbox/receive-messages.md))

## MailboxInfo

MailboxInfo returns basic server information. ([source](../../raw/api/api-docs/api/taproot-assets/mailbox/mailbox-info.md))

- gRPC: `rpc MailboxInfo (MailboxInfoRequest) returns (MailboxInfoResponse);`
- REST: `GET /v1/taproot-assets/mailbox/info`
- Request message: `authmailboxrpc.MailboxInfoRequest`
- Response message: `authmailboxrpc.MailboxInfoResponse`

The request has no parameters. The response fields are `server_time` (the current server time in Unix epoch seconds) and `message_count` (the number of messages currently stored on the server). ([source](../../raw/api/api-docs/api/taproot-assets/mailbox/mailbox-info.md))

## RemoveMessage

RemoveMessage removes one or more messages from the mailbox. The caller must prove ownership of the receiver key by providing a Schnorr signature over SHA256(receiver\_id || big-endian uint64 message\_id\_1 || ...). Only messages that belong to the authenticated receiver are deleted. ([source](../../raw/api/api-docs/api/taproot-assets/mailbox/remove-message.md))

- gRPC: `rpc RemoveMessage (RemoveMessageRequest) returns (RemoveMessageResponse);`
- REST: `POST /v1/taproot-assets/mailbox/remove`
- Request message: `authmailboxrpc.RemoveMessageRequest`
- Response message: `authmailboxrpc.RemoveMessageResponse`

The request fields are `receiver_id` (the same key used when subscribing for messages via ReceiveMessages), `message_ids` and `signature`. IDs that don't exist or belong to a different receiver are silently skipped. The response has one field, `num_removed`, the number of messages that were actually removed. ([source](../../raw/api/api-docs/api/taproot-assets/mailbox/remove-message.md))

## Conflicts

On the ReceiveMessages page, step 4 of the expected flow writes the streamed response as `ReceiveMessagesResponse(message = MailboxMessage{...})`, while the `ReceiveMessagesResponse` field table on the same page has no `message` field; it lists `messages`, of type `MailboxMessages`. ([source](../../raw/api/api-docs/api/taproot-assets/mailbox/receive-messages.md))

On the same page, the description of `start_message_id_exclusive` calls it "the exclusive start message ID" and continues "meaning messages with this ID or higher will be included in the response". The two halves of that sentence disagree on whether the message with the given ID is included. ([source](../../raw/api/api-docs/api/taproot-assets/mailbox/receive-messages.md))
