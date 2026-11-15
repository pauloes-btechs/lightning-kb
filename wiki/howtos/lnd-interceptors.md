---
title: HTLC interceptor, RPC middleware and channel acceptor
type: howto
sources:
  - raw/docs/lightning-network-tools/lnd/htlc-interceptor.md
  - raw/docs/lightning-network-tools/lnd/rpc-middleware-interceptor.md
  - raw/docs/lightning-network-tools/lnd/channel-acceptor.md
  - raw/docs/lightning-network-tools/lnd/optimal-configuration-of-a-routing-node.md
updated: 2026-11-14
---

# HTLC interceptor, RPC middleware and channel acceptor

This page covers three [[lnd]] features. The HTLC Interceptor allows you to reject, resume and settle HTLCs flowing through your node. ([source](../../raw/docs/lightning-network-tools/lnd/htlc-interceptor.md)) The RPC middleware interceptor allows interception and modification of any RPC call made to LND. ([source](../../raw/docs/lightning-network-tools/lnd/rpc-middleware-interceptor.md)) The channel acceptor API allows you to enforce custom logic on whether an incoming channel should be accepted or not. ([source](../../raw/docs/lightning-network-tools/lnd/channel-acceptor.md))

## HTLC interceptor

The HTLC Interceptor is a service in LND that lets you inspect, approve, deny or settle all [[htlc]]s passing through your node. HTLCs terminating at the node (payments made to it) are not affected. Once registered, LND forwards information about every passing HTLC to the interceptor, which replies with Settle, Fail or Resume. When failing, the interceptor may respond with the appropriate error message as if it were the recipient ([source](../../raw/docs/lightning-network-tools/lnd/htlc-interceptor.md)).

Example use: in a high-performance cluster, several LND instances generate invoices but only one node receives payments. The invoicing nodes, each with its own public key and no public channels, include a hop hint from the settlement node in their invoices. The interceptor resumes HTLCs not destined for the invoicing nodes and settles the others with the preimage obtained from the invoicing nodes ([source](../../raw/docs/lightning-network-tools/lnd/htlc-interceptor.md)).

The guide's API link points to the router service's `htlc-interceptor` page. Its code examples (lnmux and lndclient) use `routerrpc.ForwardHtlcInterceptRequest` and `routerrpc.ForwardHtlcInterceptResponse`, the latter with `IncomingCircuitKey`, `Action`, `Preimage`, `FailureMessage` and `FailureCode`. lndclient defines the actions `InterceptorActionSettle`, `InterceptorActionFail` and `InterceptorActionResume`; a preimage must be set when settling ([source](../../raw/docs/lightning-network-tools/lnd/htlc-interceptor.md)).

## RPC middleware interceptor

Once enabled, the RPC middleware interceptor intercepts all incoming RPC requests to LND and forwards them so they can be inspected, validated and modified before being sent back to LND for execution. Lightning Terminal uses it for its Accounts feature, which virtually segregates funds in a node between accounts, enforced by macaroons ([source](../../raw/docs/lightning-network-tools/lnd/rpc-middleware-interceptor.md)).

Enable it in `lnd.conf` and restart ([source](../../raw/docs/lightning-network-tools/lnd/rpc-middleware-interceptor.md)):

```
rpcmiddleware.enable=true
```

The routing node guide lists the same option with `# (default: false)` and says Lightning Terminal needs it to run ([source](../../raw/docs/lightning-network-tools/lnd/optimal-configuration-of-a-routing-node.md)).

Middleware must authenticate to LND with a custom macaroon stating which caveats it is responsible for; only requests pertaining to those caveats are forwarded to it. Multiple middleware connections are possible, but when replacing calls each interceptor should be limited to its exclusive caveats, because each call can only be replaced once ([source](../../raw/docs/lightning-network-tools/lnd/rpc-middleware-interceptor.md)).

The API link points to the Lightning service's `register-r-p-c-middleware` page. The Lightning Terminal example handles `lnrpc.RPCMiddlewareRequest` with intercept types `RPCMiddlewareRequest_StreamAuth`, `RPCMiddlewareRequest_Request` and `RPCMiddlewareRequest_Response`, returning `lnrpc.RPCMiddlewareResponse`. lndclient exposes `RegisterRPCMiddleware(ctx, middlewareName, customCaveatName string, readOnly bool, timeout time.Duration, intercept InterceptFunction)` ([source](../../raw/docs/lightning-network-tools/lnd/rpc-middleware-interceptor.md)).

## Channel acceptor

The channel acceptor lets you define custom logic for whether an incoming channel is accepted, for example restricting opens to a list of nodes or a channel size, or accepting channels with a zero remote reserve or zero-confirmation channels. Pool uses it to ensure marketplace channels have the desired attributes ([source](../../raw/docs/lightning-network-tools/lnd/channel-acceptor.md)).

It does not need to be specifically enabled. Calling the API endpoint (RPC or REST) opens a bi-directional stream between LND and the client, through which all incoming channel requests are sent. The client answers TRUE or FALSE and may send a 500 character custom error message to the initiator. Multiple channel acceptors are possible; if any denies a request, LND denies it ([source](../../raw/docs/lightning-network-tools/lnd/channel-acceptor.md)).

When no channel acceptor is set, all incoming zero-confirmation channels are denied by default. To accept zero-conf channels, both initiator and respondent must set ([source](../../raw/docs/lightning-network-tools/lnd/channel-acceptor.md)):

```
protocol.option-scid-alias=true
protocol.zero-conf=true
```

In the Pool example, the response type `lndclient.AcceptorResponse` carries `Accept`, `Error`, `MinAcceptDepth` and `ZeroConf`, and the request carries fields such as `PendingChanID`, `PushAmt`, `CommitmentType`, `ChannelFlags` and `WantsZeroConf`. The lndclient comment says the client-side timeout should be strictly less than lnd's chanacceptor timeout parameter ([source](../../raw/docs/lightning-network-tools/lnd/channel-acceptor.md)).

See also: [[lnd-router]], [[lnd-lightning]], [[lnd-macaroons]], [[lnd-routing-node-operations]], [[pool-zero-conf-channels]], [[litd-accounts-guide]].
