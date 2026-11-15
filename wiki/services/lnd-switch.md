---
title: lnd switch service
type: service
sources:
  - raw/api/api-docs/api/lnd.md
  - raw/api/api-docs/api/lnd/rest-endpoints.md
  - raw/api/api-docs/api/lnd/switch/build-onion.md
  - raw/api/api-docs/api/lnd/switch/delete-attempts.md
  - raw/api/api-docs/api/lnd/switch/disable-remote-router.md
  - raw/api/api-docs/api/lnd/switch/send-onion.md
  - raw/api/api-docs/api/lnd/switch/track-onion.md
updated: 2026-11-14
---

# lnd switch service (Switch)

The switch service of [[lnd]] is documented through the RPC pages summarised below. The SendOnion page describes SendOnion as "the primary entry point for a remote router" and gives `switchrpc/switch.proto` as its source. ([source](../../raw/api/api-docs/api/lnd/switch/send-onion.md))

The reference was generated automatically against commit `895118ac4ec59e78b2c14f5b0d31ac6f862434bb` of the `lightningnetwork/lnd` repository. ([source](../../raw/api/api-docs/api/lnd.md))

The REST endpoints page lists five `switchrpc` RPCs under `/v2/switch/`: BuildOnion, DeleteAttempts, DisableRemoteRouter, SendOnion and TrackOnion. ([source](../../raw/api/api-docs/api/lnd/rest-endpoints.md))

See also: [[lnd-router]], [[lnd-invoices]], [[lnd-lightning]], [[lnd-sending-payments]], [[htlc]], [[pathfinding]].

## BuildOnion

BuildOnion attempts to build an onion packet for the specified route. ([source](../../raw/api/api-docs/api/lnd/switch/build-onion.md))

- gRPC: `rpc BuildOnion (BuildOnionRequest) returns (BuildOnionResponse);`
- REST: `POST /v2/switch/build`
- Request message: `switchrpc.BuildOnionRequest`
- Response message: `switchrpc.BuildOnionResponse`

Request fields: `route` (an `lnrpc.Route`, the route for which the onion packet should be built), `payment_hash` (the payment hash associated with the HTLC) and `session_key` (a session key for onion packet construction; if not provided, a new one will be generated). Response fields: `onion_blob` (the constructed onion packet in bytes), `session_key` (the session key used for building the onion packet) and `hop_pubkeys` (the serialized public keys of all nodes along the route for the constructed onion). ([source](../../raw/api/api-docs/api/lnd/switch/build-onion.md))

## SendOnion

SendOnion provides an idempotent API for dispatching a pre-formed onion packet. To safely handle network failures, a client can and should retry this RPC after a timeout or disconnection, and retries MUST use the exact same `attempt_id` so the server can detect duplicate requests. ([source](../../raw/api/api-docs/api/lnd/switch/send-onion.md))

- gRPC: `rpc SendOnion (SendOnionRequest) returns (SendOnionResponse);`
- REST: `POST /v2/switch/onion`
- Request message: `switchrpc.SendOnionRequest`
- Response message: `switchrpc.SendOnionResponse` (no parameters)

A client must handle four categories of outcome, determined by the gRPC status code:

1. SUCCESS (gRPC code OK): a definitive confirmation that the HTLC has been successfully dispatched. The client can proceed to track the result via the TrackOnion RPC.
2. DUPLICATE ACKNOWLEDGMENT (gRPC code AlreadyExists): a request with the same `attempt_id` has already been successfully processed. A retrying client should interpret this as a success and proceed to tracking.
3. INDEFINITE FAILURE (gRPC code Unavailable or DeadlineExceeded): the state of the HTLC dispatch is unknown. The client MUST retry the exact same request and MUST NOT move on to a new attempt ID, which risks a duplicate in-flight HTLC.
4. DEFINITIVE FAILURE (gRPC code FailedPrecondition, InvalidArgument, etc.): the HTLC was not and will not be dispatched. The client should fail the attempt and may retry with a new route and/or `attempt_id`.

In the case of a FailedPrecondition or Unavailable failure, the gRPC error may include a SendOnionFailureDetails message with additional context for logging and pathfinding. ([source](../../raw/api/api-docs/api/lnd/switch/send-onion.md))

Request fields:

- `onion_blob`: the raw onion packet to be sent across the network.
- `attempt_id`: the attempt ID uniquely identifying this payment attempt.
- `first_hop_pubkey` and `first_hop_chan_id`: the first hop must be specified either by channel ID or public key.
- `amount`: the total amount in millisatoshis required to complete a payment over this route, including the cumulative fees at each hop.
- `timelock`: the absolute timelock or CLTV value that should be extended to the first hop in the route.
- `payment_hash`: the payment hash associated with the HTLC, needed for tracking and debugging purposes.
- `blinding_point`: the optional blinding point to use when constructing the HTLC.
- `custom_records`: optional custom TLV records to include in the UpdateAddHTLC message.
- `extra_data`: optional opaque extra data to attach to the UpdateAddHTLC message.

([source](../../raw/api/api-docs/api/lnd/switch/send-onion.md))

## TrackOnion

TrackOnion allows callers to query whether or not a payment dispatched via SendOnion succeeded or failed. It is designed to be called after a successful dispatch has been explicitly confirmed via the SendOnion RPC; it should not be used to determine whether an HTLC dispatch was received in an ambiguous network scenario, which must be resolved by retrying the idempotent SendOnion RPC. ([source](../../raw/api/api-docs/api/lnd/switch/track-onion.md))

- gRPC: `rpc TrackOnion (TrackOnionRequest) returns (TrackOnionResponse);`
- REST: `POST /v2/switch/track`
- Request message: `switchrpc.TrackOnionRequest`
- Response message: `switchrpc.TrackOnionResponse`

A client must handle three categories of outcome:

1. PAYMENT SUCCESS (gRPC code OK, `preimage` set): the payment settled successfully and the response contains the payment preimage.
2. PAYMENT FAILURE (gRPC code OK, `failure_details` set): the payment failed at the application level. The `failure_details` oneof describes the failure type: a ForwardingFailure from a remote hop, a LocalFailure from the local node, an UnreadableFailure if the error could not be decoded, or a SwitchError for other switch-level failures. When `encrypted_error_data` is populated, the client may perform its own decryption.
3. QUERY FAILURE (gRPC error status): the query itself could not be completed. NotFound indicates the payment ID is unknown, Unavailable signals the switch is shutting down, and Canceled or DeadlineExceeded reflects client-side timeouts. These are safe to retry.

Request fields: `payment_hash`, `attempt_id`, and the optional `session_key` and `hop_pubkeys`, which the server uses to decrypt any failure message. Response fields: `preimage` (if set, the payment succeeded) and `failure_details` (a `switchrpc.FailureDetails`; if set, the payment attempt failed). `switchrpc.FailureDetails` has the fields `error_message`, `local_failure`, `forwarding_failure`, `encrypted_error_data`, `unreadable_failure` and `switch_error`. In `switchrpc.ForwardingFailure`, `failure_source_index` is the 0-based index of the node within the payment route that reported the failure, where index 0 refers to the local node. ([source](../../raw/api/api-docs/api/lnd/switch/track-onion.md))

## DeleteAttempts

DeleteAttempts removes terminal (settled or failed) payment attempt records from the server's attempt store. The client explicitly names the attempt IDs to delete, enabling online garbage collection of completed attempt data. ([source](../../raw/api/api-docs/api/lnd/switch/delete-attempts.md))

- gRPC: `rpc DeleteAttempts (DeleteAttemptsRequest) returns (DeleteAttemptsResponse);`
- REST: `POST /v2/switch/deleteattempts`
- Request message: `switchrpc.DeleteAttemptsRequest`
- Response message: `switchrpc.DeleteAttemptsResponse`

The request has one field, `attempt_ids`. The response has one field, `results`, a list of `switchrpc.AttemptDeletionResult` (`attempt_id`, `status`) in the same order as the `attempt_ids` in the request. The server processes each attempt ID independently, and the overall RPC succeeds (gRPC OK) as long as the request could be processed, even if individual attempts were not deleted. The `switchrpc.AttemptDeletionStatus` values are:

- `DELETION_OK`: the attempt result was successfully deleted from the store.
- `DELETION_PENDING`: the attempt is still in-flight (pending) and cannot be safely deleted.
- `DELETION_NOT_FOUND`: the attempt ID was not found in the store.
- `DELETION_FAILED`: the attempt record exists but could not be processed (e.g. deserialization error); the record remains in the store.

Clients MUST only delete attempts whose outcome (settled or failed) has been durably recorded and will never need to be retried, because deleting an attempt removes the server's idempotency protection for that attempt ID. ([source](../../raw/api/api-docs/api/lnd/switch/delete-attempts.md))

## DisableRemoteRouter

DisableRemoteRouter marks the database as no longer being used by a remote router. This is useful for migrating from a remote router setup back to the default embedded router. The RPC will fail if there are any attempt entries remaining in the network result store. ([source](../../raw/api/api-docs/api/lnd/switch/disable-remote-router.md))

- gRPC: `rpc DisableRemoteRouter (DisableRemoteRouterRequest) returns (DisableRemoteRouterResponse);`
- REST: `POST /v2/switch/disableremoterouter`
- Request message: `switchrpc.DisableRemoteRouterRequest` (no parameters)
- Response message: `switchrpc.DisableRemoteRouterResponse` (no parameters)

([source](../../raw/api/api-docs/api/lnd/switch/disable-remote-router.md))
