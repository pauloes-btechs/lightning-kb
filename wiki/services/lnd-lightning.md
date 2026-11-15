---
title: lnd lightning service
type: service
sources:
  - raw/api/api-docs/api/lnd.md
  - raw/api/api-docs/api/lnd/rest-endpoints.md
  - raw/api/api-docs/api/lnd/lightning/abandon-channel.md
  - raw/api/api-docs/api/lnd/lightning/add-invoice.md
  - raw/api/api-docs/api/lnd/lightning/bake-macaroon.md
  - raw/api/api-docs/api/lnd/lightning/batch-open-channel.md
  - raw/api/api-docs/api/lnd/lightning/channel-acceptor.md
  - raw/api/api-docs/api/lnd/lightning/channel-balance.md
  - raw/api/api-docs/api/lnd/lightning/check-macaroon-permissions.md
  - raw/api/api-docs/api/lnd/lightning/close-channel.md
  - raw/api/api-docs/api/lnd/lightning/closed-channels.md
  - raw/api/api-docs/api/lnd/lightning/connect-peer.md
  - raw/api/api-docs/api/lnd/lightning/debug-level.md
  - raw/api/api-docs/api/lnd/lightning/decode-pay-req.md
  - raw/api/api-docs/api/lnd/lightning/delete-all-payments.md
  - raw/api/api-docs/api/lnd/lightning/delete-canceled-invoice.md
  - raw/api/api-docs/api/lnd/lightning/delete-macaroon-i-d.md
  - raw/api/api-docs/api/lnd/lightning/delete-payment.md
  - raw/api/api-docs/api/lnd/lightning/describe-graph.md
  - raw/api/api-docs/api/lnd/lightning/disconnect-peer.md
  - raw/api/api-docs/api/lnd/lightning/estimate-fee.md
  - raw/api/api-docs/api/lnd/lightning/export-all-channel-backups.md
  - raw/api/api-docs/api/lnd/lightning/export-channel-backup.md
  - raw/api/api-docs/api/lnd/lightning/fee-report.md
  - raw/api/api-docs/api/lnd/lightning/forwarding-history.md
  - raw/api/api-docs/api/lnd/lightning/funding-state-step.md
  - raw/api/api-docs/api/lnd/lightning/get-chan-info.md
  - raw/api/api-docs/api/lnd/lightning/get-debug-info.md
  - raw/api/api-docs/api/lnd/lightning/get-info.md
  - raw/api/api-docs/api/lnd/lightning/get-network-info.md
  - raw/api/api-docs/api/lnd/lightning/get-node-info.md
  - raw/api/api-docs/api/lnd/lightning/get-node-metrics.md
  - raw/api/api-docs/api/lnd/lightning/get-recovery-info.md
  - raw/api/api-docs/api/lnd/lightning/get-transactions.md
  - raw/api/api-docs/api/lnd/lightning/list-aliases.md
  - raw/api/api-docs/api/lnd/lightning/list-channels.md
  - raw/api/api-docs/api/lnd/lightning/list-invoices.md
  - raw/api/api-docs/api/lnd/lightning/list-macaroon-i-ds.md
  - raw/api/api-docs/api/lnd/lightning/list-payments.md
  - raw/api/api-docs/api/lnd/lightning/list-peers.md
  - raw/api/api-docs/api/lnd/lightning/list-permissions.md
  - raw/api/api-docs/api/lnd/lightning/list-unspent.md
  - raw/api/api-docs/api/lnd/lightning/lookup-htlc-resolution.md
  - raw/api/api-docs/api/lnd/lightning/lookup-invoice.md
  - raw/api/api-docs/api/lnd/lightning/new-address.md
  - raw/api/api-docs/api/lnd/lightning/open-channel.md
  - raw/api/api-docs/api/lnd/lightning/open-channel-sync.md
  - raw/api/api-docs/api/lnd/lightning/pending-channels.md
  - raw/api/api-docs/api/lnd/lightning/query-routes.md
  - raw/api/api-docs/api/lnd/lightning/register-r-p-c-middleware.md
  - raw/api/api-docs/api/lnd/lightning/restore-channel-backups.md
  - raw/api/api-docs/api/lnd/lightning/send-coins.md
  - raw/api/api-docs/api/lnd/lightning/send-custom-message.md
  - raw/api/api-docs/api/lnd/lightning/send-many.md
  - raw/api/api-docs/api/lnd/lightning/send-onion-message.md
  - raw/api/api-docs/api/lnd/lightning/sign-message.md
  - raw/api/api-docs/api/lnd/lightning/stop-daemon.md
  - raw/api/api-docs/api/lnd/lightning/subscribe-channel-backups.md
  - raw/api/api-docs/api/lnd/lightning/subscribe-channel-events.md
  - raw/api/api-docs/api/lnd/lightning/subscribe-channel-graph.md
  - raw/api/api-docs/api/lnd/lightning/subscribe-custom-messages.md
  - raw/api/api-docs/api/lnd/lightning/subscribe-invoices.md
  - raw/api/api-docs/api/lnd/lightning/subscribe-onion-messages.md
  - raw/api/api-docs/api/lnd/lightning/subscribe-peer-events.md
  - raw/api/api-docs/api/lnd/lightning/subscribe-transactions.md
  - raw/api/api-docs/api/lnd/lightning/update-channel-policy.md
  - raw/api/api-docs/api/lnd/lightning/verify-chan-backup.md
  - raw/api/api-docs/api/lnd/lightning/verify-message.md
  - raw/api/api-docs/api/lnd/lightning/wallet-balance.md
updated: 2026-11-14
---

# lnd lightning service (Lightning)

This page covers the Lightning service of [[lnd]]. The REST endpoints page lists 67 RPCs whose links point into the reference's `lightning` section, each named `lnrpc.<RPC>` with a REST path and method. ([source](../../raw/api/api-docs/api/lnd/rest-endpoints.md))

The RPC pages give `lightning.proto` as their source, for example the GetInfo page. ([source](../../raw/api/api-docs/api/lnd/lightning/get-info.md))

The reference was generated automatically against commit `895118ac4ec59e78b2c14f5b0d31ac6f862434bb` of the `lightningnetwork/lnd` repository. Its code samples assume a local `lnd` instance listening for gRPC connections on port `10009` and for REST connections on port `8080`, and a request needs a TLS/SSL connection and a macaroon used for RPC authentication. When using REST, a `byte` field must be set as the base64 encoded string representation of a raw byte array, and when used in a URL path the base64 string must use the URL and Filename Safe Alphabet (replace `+` with `-`, `/` with `_`, keep the trailing `=`). ([source](../../raw/api/api-docs/api/lnd.md))

See also: [[lnd-router]], [[lnd-invoices]], [[lnd-wallet-kit]], [[lnd-wallet-unlocker]], [[lnd-peers]], [[lnd-state]], [[payment-channels]], [[lightning-invoices]], [[channel-fees]], [[pathfinding]], [[macaroons]].

## Node information and control

### GetInfo

- gRPC: `rpc GetInfo (GetInfoRequest) returns (GetInfoResponse);`
- REST: `GET /v1/getinfo`
- Request message: `lnrpc.GetInfoRequest`
- Response message: `lnrpc.GetInfoResponse`

GetInfo returns general information concerning the lightning node, including its identity pubkey, alias, the chains it is connected to, and information concerning the number of open and pending channels. The request has no parameters. Response fields include `version`, `identity_pubkey`, `alias`, `block_height`, `synced_to_chain` (whether the wallet's view is synced to the main chain) and `synced_to_graph` (whether the node considers itself synced with the public channel graph); `testnet` is deprecated in favour of the network field. ([source](../../raw/api/api-docs/api/lnd/lightning/get-info.md))

### GetDebugInfo

- gRPC: `rpc GetDebugInfo (GetDebugInfoRequest) returns (GetDebugInfoResponse);`
- REST: `GET /v1/getdebuginfo`
- Request message: `lnrpc.GetDebugInfoRequest`
- Response message: `lnrpc.GetDebugInfoResponse`

GetDebugInfo returns debug information concerning the state of the daemon and its subsystems, including the full configuration and the latest log entries from the log file. The page gives the lncli command as `getdebuginfo`. If `include_log` is set to true the log file content is included in the response; by default only the config information is returned. The response fields are `config` and `log`. ([source](../../raw/api/api-docs/api/lnd/lightning/get-debug-info.md))

### GetRecoveryInfo

- gRPC: `rpc GetRecoveryInfo (GetRecoveryInfoRequest) returns (GetRecoveryInfoResponse);`
- REST: `GET /v1/getrecoveryinfo`
- Request message: `lnrpc.GetRecoveryInfoRequest`
- Response message: `lnrpc.GetRecoveryInfoResponse`

GetRecoveryInfo returns information concerning the recovery mode: whether the wallet is in a recovery mode, whether the recovery is finished, and the progress made so far. The request has no parameters. The response fields are `recovery_mode`, `recovery_finished` and `progress`, the last ranging from 0 to 1. ([source](../../raw/api/api-docs/api/lnd/lightning/get-recovery-info.md))

### DebugLevel

- gRPC: `rpc DebugLevel (DebugLevelRequest) returns (DebugLevelResponse);`
- REST: `POST /v1/debuglevel`
- Request message: `lnrpc.DebugLevelRequest`
- Response message: `lnrpc.DebugLevelResponse`

DebugLevel allows a caller to programmatically set the logging verbosity of lnd, either as a coarse daemon-wide logging level or in a granular fashion for a target sub-system. The request fields are `show` and `level_spec`; the response field is `sub_systems`. ([source](../../raw/api/api-docs/api/lnd/lightning/debug-level.md))

### StopDaemon

- gRPC: `rpc StopDaemon (StopRequest) returns (StopResponse);`
- REST: `POST /v1/stop`
- Request message: `lnrpc.StopRequest`
- Response message: `lnrpc.StopResponse`

StopDaemon sends a shutdown request to the interrupt handler, triggering a graceful shutdown of the daemon. The request has no parameters; the response has a `status` field with the status of the stop operation. ([source](../../raw/api/api-docs/api/lnd/lightning/stop-daemon.md))

### SignMessage

- gRPC: `rpc SignMessage (SignMessageRequest) returns (SignMessageResponse);`
- REST: `POST /v1/signmessage`
- Request message: `lnrpc.SignMessageRequest`
- Response message: `lnrpc.SignMessageResponse`

SignMessage signs a message with this node's private key. The returned signature string is `zbase32` encoded and pubkey recoverable, meaning that only the message digest and signature are needed for verification. The request takes `msg` (base64 when using REST) and `single_hash`, which uses one round of hashing instead of the default double-SHA256; the response field is `signature`. ([source](../../raw/api/api-docs/api/lnd/lightning/sign-message.md))

### VerifyMessage

- gRPC: `rpc VerifyMessage (VerifyMessageRequest) returns (VerifyMessageResponse);`
- REST: `POST /v1/verifymessage`
- Request message: `lnrpc.VerifyMessageRequest`
- Response message: `lnrpc.VerifyMessageResponse`

VerifyMessage verifies a signature over a message and recovers the signer's public key. The signature is only deemed valid if the recovered public key corresponds to a node key in the public Lightning network; it must be zbase32 encoded and signed by an active node in the resident node's channel database. The request fields are `msg` and `signature`; the response fields are `valid` and `pubkey`. ([source](../../raw/api/api-docs/api/lnd/lightning/verify-message.md))

## On-chain wallet

### WalletBalance

- gRPC: `rpc WalletBalance (WalletBalanceRequest) returns (WalletBalanceResponse);`
- REST: `GET /v1/balance/blockchain`
- Request message: `lnrpc.WalletBalanceRequest`
- Response message: `lnrpc.WalletBalanceResponse`

WalletBalance returns total unspent outputs (confirmed and unconfirmed), all confirmed unspent outputs and all unconfirmed unspent outputs under control of the wallet. The request takes `account` (if not specified, the balance of the "default" account is shown) and `min_confs` (if not specified, the default value of 1 is used). Response fields are `total_balance`, `confirmed_balance`, `unconfirmed_balance`, `locked_balance`, `reserved_balance_anchor_chan` and `account_balance`. ([source](../../raw/api/api-docs/api/lnd/lightning/wallet-balance.md))

### NewAddress

- gRPC: `rpc NewAddress (NewAddressRequest) returns (NewAddressResponse);`
- REST: `GET /v1/newaddress`
- Request message: `lnrpc.NewAddressRequest`
- Response message: `lnrpc.NewAddressResponse`

NewAddress creates a new address under control of the local wallet. The request takes `type`, an `lnrpc.AddressType` value (`WITNESS_PUBKEY_HASH`, `NESTED_PUBKEY_HASH`, `UNUSED_WITNESS_PUBKEY_HASH`, `UNUSED_NESTED_PUBKEY_HASH`, `TAPROOT_PUBKEY`, `UNUSED_TAPROOT_PUBKEY`), and `account`; if `account` is empty, the default wallet account is used. The response field is `address`. ([source](../../raw/api/api-docs/api/lnd/lightning/new-address.md))

### GetTransactions

- gRPC: `rpc GetTransactions (GetTransactionsRequest) returns (TransactionDetails);`
- REST: `GET /v1/transactions`
- Request message: `lnrpc.GetTransactionsRequest`
- Response message: `lnrpc.TransactionDetails`

GetTransactions returns a list describing all the known transactions relevant to the wallet. The request fields are `start_height`, `end_height`, `account`, `index_offset`, `max_transactions` and `reverse`. To include unconfirmed transactions `end_height` should be set to -1, which is also the default when no `end_height` is provided, and `max_transactions` should be set to 0 to return all transactions. The response carries `transactions`, `last_index` and `first_index`. ([source](../../raw/api/api-docs/api/lnd/lightning/get-transactions.md))

### SubscribeTransactions

- gRPC: `rpc SubscribeTransactions (GetTransactionsRequest) returns (stream Transaction);` (server-streaming RPC)
- REST: `GET /v1/transactions/subscribe`
- Request message: `lnrpc.GetTransactionsRequest`
- Response message: `lnrpc.Transaction`

SubscribeTransactions creates a uni-directional stream from the server to the client in which any newly discovered transactions relevant to the wallet are sent over. It takes the same request message as GetTransactions; the description of that message's `reverse` field says the flag only applies to GetTransactions and is ignored by SubscribeTransactions. Each streamed `lnrpc.Transaction` includes `tx_hash`, `amount`, `num_confirmations`, `block_height`, `total_fees`, `output_details` and `label`. ([source](../../raw/api/api-docs/api/lnd/lightning/subscribe-transactions.md))

### EstimateFee

- gRPC: `rpc EstimateFee (EstimateFeeRequest) returns (EstimateFeeResponse);`
- REST: `GET /v1/transactions/fee`
- Request message: `lnrpc.EstimateFeeRequest`
- Response message: `lnrpc.EstimateFeeResponse`

EstimateFee asks the chain backend to estimate the fee rate and total fees for a transaction that pays to multiple specified outputs. When using REST, the `AddrToAmount` map type can be set by appending `&AddrToAmount[<address>]=<amount_to_send>` to the URL; the page says this map type does not appear in the REST API documentation because of a bug in the grpc-gateway library. The response fields are `fee_sat`, `sat_per_vbyte`, `inputs` and the deprecated `feerate_sat_per_byte`. ([source](../../raw/api/api-docs/api/lnd/lightning/estimate-fee.md))

### SendCoins

- gRPC: `rpc SendCoins (SendCoinsRequest) returns (SendCoinsResponse);`
- REST: `POST /v1/transactions`
- Request message: `lnrpc.SendCoinsRequest`
- Response message: `lnrpc.SendCoinsResponse`

SendCoins executes a request to send coins to a particular address; unlike SendMany, it only allows creating a single output at a time. If neither `target_conf` nor `sat_per_vbyte` is set, the internal wallet consults its fee model to determine a fee for the default confirmation target. Other request fields include `addr`, `amount`, `send_all` (if set, the amount field should be unset), `label` (limited to 500 characters), `min_confs`, `spend_unconfirmed`, `coin_selection_strategy` and `outpoints`; `sat_per_byte` is deprecated in favour of `sat_per_vbyte`. The response field is `txid`. ([source](../../raw/api/api-docs/api/lnd/lightning/send-coins.md))

### SendMany

- gRPC: `rpc SendMany (SendManyRequest) returns (SendManyResponse);`
- REST: `POST /v1/transactions/many`
- Request message: `lnrpc.SendManyRequest`
- Response message: `lnrpc.SendManyResponse`

SendMany handles a request for a transaction that creates multiple specified outputs in parallel. If neither `target_conf` nor `sat_per_vbyte` is set, the internal wallet consults its fee model to determine a fee for the default confirmation target. The outputs are given in `AddrToAmount`, the map from addresses to amounts; the response field is `txid`. ([source](../../raw/api/api-docs/api/lnd/lightning/send-many.md))

### ListUnspent

- gRPC: `rpc ListUnspent (ListUnspentRequest) returns (ListUnspentResponse);`
- REST: `GET /v1/utxos`
- Request message: `lnrpc.ListUnspentRequest`
- Response message: `lnrpc.ListUnspentResponse`

ListUnspent returns a list of all utxos spendable by the wallet with a number of confirmations between the specified minimum and maximum. The page marks this RPC as deprecated, to be removed in a future version, and says to use walletrpc.ListUnspent instead. The request fields are `min_confs`, `max_confs` and `account`; the response field is `utxos`. ([source](../../raw/api/api-docs/api/lnd/lightning/list-unspent.md))

## Peers and peer messages

### ConnectPeer

- gRPC: `rpc ConnectPeer (ConnectPeerRequest) returns (ConnectPeerResponse);`
- REST: `POST /v1/peers`
- Request message: `lnrpc.ConnectPeerRequest`
- Response message: `lnrpc.ConnectPeerResponse`

ConnectPeer attempts to establish a connection to a remote peer. This is at the networking level, is used for communication between nodes, and is distinct from establishing a channel with a peer. The request takes `addr`, `perm` (if set, the daemon attempts to persistently connect to the target peer; otherwise the call is synchronous) and `timeout` (in seconds, for this request only). The response has a `status` field. ([source](../../raw/api/api-docs/api/lnd/lightning/connect-peer.md))

### DisconnectPeer

- gRPC: `rpc DisconnectPeer (DisconnectPeerRequest) returns (DisconnectPeerResponse);`
- REST: `DELETE /v1/peers/{pub_key}`
- Request message: `lnrpc.DisconnectPeerRequest`
- Response message: `lnrpc.DisconnectPeerResponse`

DisconnectPeer attempts to disconnect one peer from another, identified by a given pubKey. If there is currently a pending or active channel with the target peer, the action is not allowed. The request field is `pub_key`; the response has a `status` field. ([source](../../raw/api/api-docs/api/lnd/lightning/disconnect-peer.md))

### ListPeers

- gRPC: `rpc ListPeers (ListPeersRequest) returns (ListPeersResponse);`
- REST: `GET /v1/peers`
- Request message: `lnrpc.ListPeersRequest`
- Response message: `lnrpc.ListPeersResponse`

ListPeers returns a verbose listing of all currently active peers. If `latest_error` is true, only the last error the peer sent is returned with the peer's information rather than the full set of stored historic errors. The response field is `peers`. ([source](../../raw/api/api-docs/api/lnd/lightning/list-peers.md))

### SubscribePeerEvents

- gRPC: `rpc SubscribePeerEvents (PeerEventSubscription) returns (stream PeerEvent);` (server-streaming RPC)
- REST: `GET /v1/peers/subscribe`
- Request message: `lnrpc.PeerEventSubscription`
- Response message: `lnrpc.PeerEvent`

SubscribePeerEvents creates a uni-directional stream from the server to the client in which any events relevant to the state of peers are sent over, including peers going online and offline. The request has no parameters. Each `lnrpc.PeerEvent` has `pub_key` and `type`, whose `lnrpc.PeerEvent.EventType` values are `PEER_ONLINE` and `PEER_OFFLINE`. ([source](../../raw/api/api-docs/api/lnd/lightning/subscribe-peer-events.md))

### SendCustomMessage

- gRPC: `rpc SendCustomMessage (SendCustomMessageRequest) returns (SendCustomMessageResponse);`
- REST: `POST /v1/custommessage`
- Request message: `lnrpc.SendCustomMessageRequest`
- Response message: `lnrpc.SendCustomMessageResponse`

SendCustomMessage sends a custom peer message. The request fields are `peer`, `type` and `data`. `type` needs to be in the custom range (>= 32768); to send a type below the custom range, lnd needs to be compiled with the `dev` build tag and the message type to override specified in lnd's experimental protocol configuration. The response has a `status` field. ([source](../../raw/api/api-docs/api/lnd/lightning/send-custom-message.md))

### SubscribeCustomMessages

- gRPC: `rpc SubscribeCustomMessages (SubscribeCustomMessagesRequest) returns (stream CustomMessage);` (server-streaming RPC)
- REST: `GET /v1/custommessage/subscribe`
- Request message: `lnrpc.SubscribeCustomMessagesRequest`
- Response message: `lnrpc.CustomMessage`

SubscribeCustomMessages subscribes to a stream of incoming custom peer messages. To include messages with a type outside of the custom range (>= 32768), lnd needs to be compiled with the `dev` build tag and the message type to override specified in lnd's experimental protocol configuration. The request has no parameters; each `lnrpc.CustomMessage` has `peer`, `type` and `data`. ([source](../../raw/api/api-docs/api/lnd/lightning/subscribe-custom-messages.md))

### SendOnionMessage

- gRPC: `rpc SendOnionMessage (SendOnionMessageRequest) returns (SendOnionMessageResponse);`
- REST: `POST /v1/onionmessage`
- Request message: `lnrpc.SendOnionMessageRequest`
- Response message: `lnrpc.SendOnionMessageResponse`

SendOnionMessage sends an onion message to a peer. The request fields are `peer`, `path_key` and `onion`, the last being the serialized Sphinx onion packet (BOLT 4). The response has a `status` field. ([source](../../raw/api/api-docs/api/lnd/lightning/send-onion-message.md))

### SubscribeOnionMessages

- gRPC: `rpc SubscribeOnionMessages (SubscribeOnionMessagesRequest) returns (stream OnionMessageUpdate);` (server-streaming RPC)
- REST: `GET /v1/onionmessage/subscribe`
- Request message: `lnrpc.SubscribeOnionMessagesRequest`
- Response message: `lnrpc.OnionMessageUpdate`

SubscribeOnionMessages subscribes to a stream of incoming onion messages. The request has no parameters. Each `lnrpc.OnionMessageUpdate` has `peer`, `path_key`, `onion`, `reply_path`, `encrypted_recipient_data` and `custom_records`. ([source](../../raw/api/api-docs/api/lnd/lightning/subscribe-onion-messages.md))

## Channels

### ChannelBalance

- gRPC: `rpc ChannelBalance (ChannelBalanceRequest) returns (ChannelBalanceResponse);`
- REST: `GET /v1/balance/channels`
- Request message: `lnrpc.ChannelBalanceRequest`
- Response message: `lnrpc.ChannelBalanceResponse`

ChannelBalance returns a report on the total funds across all open channels, categorized in local/remote, pending local/remote and unsettled local/remote balances. The request has no parameters. Response fields are `local_balance`, `remote_balance`, `unsettled_local_balance`, `unsettled_remote_balance`, `pending_open_local_balance`, `pending_open_remote_balance` and `custom_channel_data`; `balance` and `pending_open_balance` are deprecated. ([source](../../raw/api/api-docs/api/lnd/lightning/channel-balance.md))

### ListChannels

- gRPC: `rpc ListChannels (ListChannelsRequest) returns (ListChannelsResponse);`
- REST: `GET /v1/channels`
- Request message: `lnrpc.ListChannelsRequest`
- Response message: `lnrpc.ListChannelsResponse`

ListChannels returns a description of all the open channels that this node is a participant in. Request filters are `active_only`, `inactive_only`, `public_only`, `private_only` and `peer`; if `peer` is empty, all channels are returned. `peer_alias_lookup` enables the peer alias lookup per channel and is turned off by default to avoid degrading performance for existing clients. The response field is `channels`. ([source](../../raw/api/api-docs/api/lnd/lightning/list-channels.md))

### PendingChannels

- gRPC: `rpc PendingChannels (PendingChannelsRequest) returns (PendingChannelsResponse);`
- REST: `GET /v1/channels/pending`
- Request message: `lnrpc.PendingChannelsRequest`
- Response message: `lnrpc.PendingChannelsResponse`

PendingChannels returns a list of all the channels that are currently considered "pending". A channel is pending if it has finished the funding workflow and is waiting for confirmations for the funding txn, or is in the process of closure, either initiated cooperatively or non-cooperatively. The request field `include_raw_tx` indicates whether to include the raw transaction hex for waiting\_close\_channels. Response fields are `total_limbo_balance`, `pending_open_channels`, `pending_force_closing_channels`, `waiting_close_channels` and the deprecated `pending_closing_channels`. ([source](../../raw/api/api-docs/api/lnd/lightning/pending-channels.md))

### ClosedChannels

- gRPC: `rpc ClosedChannels (ClosedChannelsRequest) returns (ClosedChannelsResponse);`
- REST: `GET /v1/channels/closed`
- Request message: `lnrpc.ClosedChannelsRequest`
- Response message: `lnrpc.ClosedChannelsResponse`

ClosedChannels returns a description of all the closed channels that this node was a participant in. The request fields are `cooperative`, `local_force`, `remote_force`, `breach`, `funding_canceled` and `abandoned`; the response field is `channels`. ([source](../../raw/api/api-docs/api/lnd/lightning/closed-channels.md))

### SubscribeChannelEvents

- gRPC: `rpc SubscribeChannelEvents (ChannelEventSubscription) returns (stream ChannelEventUpdate);` (server-streaming RPC)
- REST: `GET /v1/channels/subscribe`
- Request message: `lnrpc.ChannelEventSubscription`
- Response message: `lnrpc.ChannelEventUpdate`

SubscribeChannelEvents creates a uni-directional stream from the server to the client in which any updates relevant to the state of the channels are sent over. Events include new active channels, inactive channels, and closed channels. The request has no parameters. `lnrpc.ChannelEventUpdate` has the fields `open_channel`, `closed_channel`, `active_channel`, `inactive_channel`, `pending_open_channel`, `fully_resolved_channel`, `channel_funding_timeout`, `updated_channel` and `type`. ([source](../../raw/api/api-docs/api/lnd/lightning/subscribe-channel-events.md))

### OpenChannel

- gRPC: `rpc OpenChannel (OpenChannelRequest) returns (stream OpenStatusUpdate);` (server-streaming RPC)
- REST: `POST /v1/channels/stream`
- Request message: `lnrpc.OpenChannelRequest`
- Response message: `lnrpc.OpenStatusUpdate`

OpenChannel attempts to open a singly funded channel specified in the request to a remote peer. Users can specify a target number of blocks that the funding transaction should be confirmed in, or a manual fee rate for the funding transaction; if neither is specified, a lax block confirmation target is used. Each OpenStatusUpdate returns the pending channel ID of the in-progress channel, which, depending on the arguments in the OpenChannelRequest, can then be used to manually progress the channel funding flow. Request fields include `node_pubkey`, `local_funding_amount`, `push_sat`, `target_conf`, `sat_per_vbyte`, `private`, `close_address`, `funding_shim`, `commitment_type`, `zero_conf`, `scid_alias`, `base_fee`, `fee_rate`, `fund_max`, `memo` and `outpoints`. For `commitment_type`, if UNKNOWN, lnd selects a default from both peers' supported features, and LEGACY is rejected. `remote_chan_reserve_sat`, if specified, must be above the dust limit and below 20% of the channel capacity. `lnrpc.OpenStatusUpdate` has the fields `chan_pending`, `chan_open`, `psbt_fund` and `pending_chan_id`. ([source](../../raw/api/api-docs/api/lnd/lightning/open-channel.md))

### OpenChannelSync

- gRPC: `rpc OpenChannelSync (OpenChannelRequest) returns (ChannelPoint);`
- REST: `POST /v1/channels`
- Request message: `lnrpc.OpenChannelRequest`
- Response message: `lnrpc.ChannelPoint`

OpenChannelSync is a synchronous version of the OpenChannel RPC call, meant to be consumed by clients to the REST proxy. As with all other sync calls, all byte slices are intended to be populated as hex encoded strings. It takes the same `lnrpc.OpenChannelRequest` as OpenChannel and returns an `lnrpc.ChannelPoint` with the fields `funding_txid_bytes`, `funding_txid_str` and `output_index`. ([source](../../raw/api/api-docs/api/lnd/lightning/open-channel-sync.md))

### BatchOpenChannel

- gRPC: `rpc BatchOpenChannel (BatchOpenChannelRequest) returns (BatchOpenChannelResponse);`
- REST: `POST /v1/channels/batch`
- Request message: `lnrpc.BatchOpenChannelRequest`
- Response message: `lnrpc.BatchOpenChannelResponse`

BatchOpenChannel attempts to open multiple single-funded channels in a single transaction in an atomic way: either all channel open requests succeed at once or all attempts are aborted if any of them fail. The page calls this the safer variant of using PSBTs to manually fund a batch of channels through the OpenChannel RPC. Request fields are `channels`, `target_conf`, `sat_per_vbyte`, `min_confs`, `spend_unconfirmed`, `label` (limited to 500 characters) and `coin_selection_strategy`; the response field is `pending_channels`. ([source](../../raw/api/api-docs/api/lnd/lightning/batch-open-channel.md))

### FundingStateStep

- gRPC: `rpc FundingStateStep (FundingTransitionMsg) returns (FundingStateStepResp);`
- REST: `POST /v1/funding/step`
- Request message: `lnrpc.FundingTransitionMsg`
- Response message: `lnrpc.FundingStateStepResp`

FundingStateStep is an advanced funding related call that allows the caller to either execute some preparatory steps for a funding workflow or manually progress a funding workflow. The primary way a funding flow is identified is via its pending channel ID. It can be used to specify that a funding flow is expected for a particular pending channel ID with specific parameters, or to interactively drive PSBT signing for partially complete funding transactions. `lnrpc.FundingTransitionMsg` has the fields `shim_register`, `shim_cancel`, `psbt_verify` and `psbt_finalize`; the response has no parameters. ([source](../../raw/api/api-docs/api/lnd/lightning/funding-state-step.md))

### ChannelAcceptor

- gRPC: `rpc ChannelAcceptor (stream ChannelAcceptResponse) returns (stream ChannelAcceptRequest);` (bidirectional-streaming RPC)
- REST: `POST /v1/channels/acceptor`
- Request message: `lnrpc.ChannelAcceptResponse`
- Response message: `lnrpc.ChannelAcceptRequest`

ChannelAcceptor dispatches a bi-directional streaming RPC in which OpenChannel requests are sent to the client and the client responds with a boolean that tells LND whether or not to accept the channel. This allows node operators to specify their own criteria for accepting inbound channels through a single persistent connection. The client sends `lnrpc.ChannelAcceptResponse` messages, with fields including `accept`, `pending_chan_id`, `error`, `upfront_shutdown`, `csv_delay`, `reserve_sat`, `min_accept_depth` and `zero_conf`. `error` should only be set if `accept` is false and is limited to 500 characters. `zero_conf` fails if either side does not have the scid-alias feature bit set, and the minimum depth field must be zero if it is true. The server sends `lnrpc.ChannelAcceptRequest` messages, with fields including `node_pubkey`, `pending_chan_id`, `funding_amt`, `push_amt`, `commitment_type`, `wants_zero_conf` and `wants_scid_alias`. The page also documents the `lnrpc.CommitmentType` enum. ([source](../../raw/api/api-docs/api/lnd/lightning/channel-acceptor.md))

### CloseChannel

- gRPC: `rpc CloseChannel (CloseChannelRequest) returns (stream CloseStatusUpdate);` (server-streaming RPC)
- REST: `DELETE /v1/channels/{channel_point.funding_txid_str}/{channel_point.output_index}`
- Request message: `lnrpc.CloseChannelRequest`
- Response message: `lnrpc.CloseStatusUpdate`

CloseChannel attempts to close an active channel identified by its channel outpoint (ChannelPoint). The method can additionally be augmented to attempt a force close after a timeout period in the case of an inactive peer. For a non-force (cooperative) close the user can specify either a target number of blocks until the closure transaction is confirmed or a manual fee rate; if neither is specified, a default lax block confirmation target is used. Request fields are `channel_point`, `force`, `target_conf`, `sat_per_vbyte`, `delivery_address`, `max_fee_per_vbyte`, `no_wait` and the deprecated `sat_per_byte`. If `force` is true, the current commitment transaction is signed and broadcast. `max_fee_per_vbyte` is only respected if the node is the initiator of the channel. If `no_wait` is true the call does not block while it awaits a closing txid to be broadcast to the mempool. `lnrpc.CloseStatusUpdate` has the fields `close_pending`, `chan_close` and `close_instant`. ([source](../../raw/api/api-docs/api/lnd/lightning/close-channel.md))

### AbandonChannel

- gRPC: `rpc AbandonChannel (AbandonChannelRequest) returns (AbandonChannelResponse);`
- REST: `DELETE /v1/channels/abandon/{channel_point.funding_txid_str}/{channel_point.output_index}`
- Request message: `lnrpc.AbandonChannelRequest`
- Response message: `lnrpc.AbandonChannelResponse`

AbandonChannel removes all channel state from the database except for a close summary. It can be used to get rid of permanently unusable channels due to bugs fixed in newer versions of lnd, and to remove externally funded channels where the funding transaction was never broadcast. The page says it is only available for non-externally funded channels in dev build. Request fields are `channel_point`, `pending_funding_shim_only` and `i_know_what_i_am_doing`; the last overrides the requirement for being in dev mode and is described as a potential foot gun to lose funds if used on active channels. The response has a `status` field. ([source](../../raw/api/api-docs/api/lnd/lightning/abandon-channel.md))

### ListAliases

- gRPC: `rpc ListAliases (ListAliasesRequest) returns (ListAliasesResponse);`
- REST: `GET /v1/aliases/list`
- Request message: `lnrpc.ListAliasesRequest`
- Response message: `lnrpc.ListAliasesResponse`

ListAliases returns the set of all aliases that have ever existed with their confirmed SCID (if it exists) and/or the base SCID (in the case of zero conf). The request has no parameters; the response field is `alias_maps`. ([source](../../raw/api/api-docs/api/lnd/lightning/list-aliases.md))

### LookupHtlcResolution

- gRPC: `rpc LookupHtlcResolution (LookupHtlcResolutionRequest) returns (LookupHtlcResolutionResponse);`
- REST: `GET /v1/htlc-resolution/{chan_id}/{htlc_index}`
- Request message: `lnrpc.LookupHtlcResolutionRequest`
- Response message: `lnrpc.LookupHtlcResolutionResponse`

LookupHtlcResolution retrieves a final htlc resolution from the database. If the htlc has no final resolution yet, a NotFound grpc status code is returned. The request fields are `chan_id` and `htlc_index`. In the response, `settled` is true if the htlc was settled and false if it was failed, and `offchain` indicates whether the htlc was resolved off-chain or on-chain. ([source](../../raw/api/api-docs/api/lnd/lightning/lookup-htlc-resolution.md))

## Channel backups

### ExportChannelBackup

- gRPC: `rpc ExportChannelBackup (ExportChannelBackupRequest) returns (ChannelBackup);`
- REST: `GET /v1/channels/backup/{chan_point.funding_txid_str}/{chan_point.output_index}`
- Request message: `lnrpc.ExportChannelBackupRequest`
- Response message: `lnrpc.ChannelBackup`

ExportChannelBackup attempts to return an encrypted static channel backup for the target channel identified by its channel point. The backup is encrypted with a key generated from the aezeed seed of the user. The returned backup can either be restored using the RestoreChannelBackup method once lnd is running, or via the InitWallet and UnlockWallet methods from the WalletUnlocker service. The request field is `chan_point`; `lnrpc.ChannelBackup` has the fields `chan_point` and `chan_backup`. ([source](../../raw/api/api-docs/api/lnd/lightning/export-channel-backup.md))

### ExportAllChannelBackups

- gRPC: `rpc ExportAllChannelBackups (ChanBackupExportRequest) returns (ChanBackupSnapshot);`
- REST: `GET /v1/channels/backup`
- Request message: `lnrpc.ChanBackupExportRequest`
- Response message: `lnrpc.ChanBackupSnapshot`

ExportAllChannelBackups returns static channel backups for all existing channels known to lnd. A set of regular singular static channel backups for each channel is returned, and additionally a multi-channel backup, which contains a single encrypted blob containing the backups of each channel. The request has no parameters; `lnrpc.ChanBackupSnapshot` has the fields `single_chan_backups` and `multi_chan_backup`. ([source](../../raw/api/api-docs/api/lnd/lightning/export-all-channel-backups.md))

### VerifyChanBackup

- gRPC: `rpc VerifyChanBackup (ChanBackupSnapshot) returns (VerifyChanBackupResponse);`
- REST: `POST /v1/channels/backup/verify`
- Request message: `lnrpc.ChanBackupSnapshot`
- Response message: `lnrpc.VerifyChanBackupResponse`

VerifyChanBackup allows a caller to verify the integrity of a channel backup snapshot. The method accepts either a packed Single or a packed Multi; specifying both results in an error. The response field is `chan_points`. ([source](../../raw/api/api-docs/api/lnd/lightning/verify-chan-backup.md))

### RestoreChannelBackups

- gRPC: `rpc RestoreChannelBackups (RestoreChanBackupRequest) returns (RestoreBackupResponse);`
- REST: `POST /v1/channels/backup/restore`
- Request message: `lnrpc.RestoreChanBackupRequest`
- Response message: `lnrpc.RestoreBackupResponse`

RestoreChannelBackups accepts a set of singular channel backups, or a single encrypted multi-chan backup, and attempts to recover any funds remaining within the channel. If the backup can be unpacked, the new channel is shown under listchannels as well as pending channels. The request fields are `chan_backups` and `multi_chan_backup`; the response field `num_restored` is the number of channels successfully restored. ([source](../../raw/api/api-docs/api/lnd/lightning/restore-channel-backups.md))

### SubscribeChannelBackups

- gRPC: `rpc SubscribeChannelBackups (ChannelBackupSubscription) returns (stream ChanBackupSnapshot);` (server-streaming RPC)
- REST: `GET /v1/channels/backup/subscribe`
- Request message: `lnrpc.ChannelBackupSubscription`
- Response message: `lnrpc.ChanBackupSnapshot`

SubscribeChannelBackups allows a client to subscribe to the most up to date information concerning the state of all channel backups. Each time a new channel is added, the new set of channels is returned along with a multi-chan backup containing the backup info for all channels. Each time a channel is closed, a new update is sent with the updated set of encrypted multi-chan backups with the closed channel(s) removed. The request has no parameters. ([source](../../raw/api/api-docs/api/lnd/lightning/subscribe-channel-backups.md))

## Invoices and payments

### AddInvoice

- gRPC: `rpc AddInvoice (Invoice) returns (AddInvoiceResponse);`
- REST: `POST /v1/invoices`
- Request message: `lnrpc.Invoice`
- Response message: `lnrpc.AddInvoiceResponse`

AddInvoice attempts to add a new invoice to the invoice database. Any duplicated invoices are rejected, therefore all invoices must have a unique payment preimage. The request is an `lnrpc.Invoice`, whose settable fields include `memo`, `r_preimage`, `value`, `value_msat`, `description_hash`, `expiry`, `fallback_addr`, `cltv_expiry`, `route_hints`, `private`, `is_amp`, `is_blinded` and `blinded_path_config`. `value` and `value_msat` are mutually exclusive, and the default for `expiry` is 86400 (24 hours). Fields such as `r_hash`, `creation_date`, `settle_date`, `payment_request`, `state`, `htlcs` and `amt_paid_sat` are marked output only. `lnrpc.AddInvoiceResponse` has the fields `r_hash`, `payment_request`, `add_index` and `payment_addr`. ([source](../../raw/api/api-docs/api/lnd/lightning/add-invoice.md))

### LookupInvoice

- gRPC: `rpc LookupInvoice (PaymentHash) returns (Invoice);`
- REST: `GET /v1/invoice/{r_hash_str}`
- Request message: `lnrpc.PaymentHash`
- Response message: `lnrpc.Invoice`

LookupInvoice attempts to look up an invoice according to its payment hash. The passed payment hash must be exactly 32 bytes; if not, an error is returned. `lnrpc.PaymentHash` has the fields `r_hash` and the deprecated `r_hash_str`. In the returned `lnrpc.Invoice`, `settled` is deprecated in favour of `state`, and `amt_paid` is deprecated in favour of `amt_paid_sat` or `amt_paid_msat`. The `amt_paid_sat` description says that for ordinary invoices the aggregate can include accepted or PENDING\_SETTLE HTLCs, and to credit only the successful value of the relevant SETTLED HTLCs rather than the requested amount or this aggregate alone. ([source](../../raw/api/api-docs/api/lnd/lightning/lookup-invoice.md))

### ListInvoices

- gRPC: `rpc ListInvoices (ListInvoiceRequest) returns (ListInvoiceResponse);`
- REST: `GET /v1/invoices`
- Request message: `lnrpc.ListInvoiceRequest`
- Response message: `lnrpc.ListInvoiceResponse`

ListInvoices returns a list of all the invoices currently stored within the database; any active debug invoices are ignored. It supports paginated responses, allowing users to query for specific invoices through their add\_index, by using either the `first_index_offset` or `last_index_offset` field of the response as the `index_offset` of the next request. By default, the first 100 invoices created are returned, and backwards pagination is supported through the `reversed` flag. Other request fields are `pending_only`, `num_max_invoices`, `creation_date_start` and `creation_date_end`. The response fields are `invoices`, `last_index_offset` and `first_index_offset`. ([source](../../raw/api/api-docs/api/lnd/lightning/list-invoices.md))

### SubscribeInvoices

- gRPC: `rpc SubscribeInvoices (InvoiceSubscription) returns (stream Invoice);` (server-streaming RPC)
- REST: `GET /v1/invoices/subscribe`
- Request message: `lnrpc.InvoiceSubscription`
- Response message: `lnrpc.Invoice`

SubscribeInvoices returns a uni-directional stream (server -> client) for notifying the client of newly added/settled invoices. The caller can optionally specify `add_index` and/or `settle_index`: if `add_index` is specified, add invoice events are first sent for all invoices with an add\_index greater than the specified value, and if `settle_index` is specified, settle events are then sent for invoices with a settle\_index greater than the specified value. If no fields are set, only the latest add/settle events are sent. The stream carries `lnrpc.Invoice` messages. ([source](../../raw/api/api-docs/api/lnd/lightning/subscribe-invoices.md))

### DeleteCanceledInvoice

- gRPC: `rpc DeleteCanceledInvoice (DelCanceledInvoiceReq) returns (DelCanceledInvoiceResp);`
- REST: `DELETE /v1/invoices`
- Request message: `lnrpc.DelCanceledInvoiceReq`
- Response message: `lnrpc.DelCanceledInvoiceResp`

DeleteCanceledInvoice removes a canceled invoice from the database. If the invoice is not in the canceled state, an error is returned. Ordinary invoices whose preimage was released cannot be deleted, even if no funds were collected, so their release history is retained. The request field is `invoice_hash`; the response has a `status` field. ([source](../../raw/api/api-docs/api/lnd/lightning/delete-canceled-invoice.md))

### DecodePayReq

- gRPC: `rpc DecodePayReq (PayReqString) returns (PayReq);`
- REST: `GET /v1/payreq/{pay_req}`
- Request message: `lnrpc.PayReqString`
- Response message: `lnrpc.PayReq`

DecodePayReq takes an encoded payment request string and attempts to decode it, returning a full description of the conditions encoded within the payment request. The request field is `pay_req`. `lnrpc.PayReq` has the fields `destination`, `payment_hash`, `num_satoshis`, `timestamp`, `expiry`, `description`, `description_hash`, `fallback_addr`, `cltv_expiry`, `route_hints`, `payment_addr`, `num_msat`, `features` and `blinded_paths`. `num_satoshis` is 0 if the payment request does not specify an amount, and if the payment request omits the BOLT-11 `x` expiry field, the BOLT-11 default of 3600 seconds is returned in `expiry`. ([source](../../raw/api/api-docs/api/lnd/lightning/decode-pay-req.md))

### ListPayments

- gRPC: `rpc ListPayments (ListPaymentsRequest) returns (ListPaymentsResponse);`
- REST: `GET /v1/payments`
- Request message: `lnrpc.ListPaymentsRequest`
- Response message: `lnrpc.ListPaymentsResponse`

ListPayments returns a list of all outgoing payments. If `include_incomplete` is true, payments that have not yet fully completed are returned, so pending payments as well as failed payments show up. `index_offset` is exclusive, and `reversed` paginates backwards while the order of the returned payments is always oldest first. Other request fields are `max_payments`, `count_total_payments`, `creation_date_start`, `creation_date_end` and `omit_hops`. The response fields are `payments`, `first_index_offset`, `last_index_offset` and `total_num_payments`. ([source](../../raw/api/api-docs/api/lnd/lightning/list-payments.md))

### DeletePayment

- gRPC: `rpc DeletePayment (DeletePaymentRequest) returns (DeletePaymentResponse);`
- REST: `DELETE /v1/payment`
- Request message: `lnrpc.DeletePaymentRequest`
- Response message: `lnrpc.DeletePaymentResponse`

DeletePayment deletes an outgoing payment from DB. It does not attempt to delete an In-Flight payment, since that would be unsafe. The request fields are `payment_hash` and `failed_htlcs_only`, which deletes only failed HTLCs from the payment and not the payment itself. The response has a `status` field. ([source](../../raw/api/api-docs/api/lnd/lightning/delete-payment.md))

### DeleteAllPayments

- gRPC: `rpc DeleteAllPayments (DeleteAllPaymentsRequest) returns (DeleteAllPaymentsResponse);`
- REST: `DELETE /v1/payments`
- Request message: `lnrpc.DeleteAllPaymentsRequest`
- Response message: `lnrpc.DeleteAllPaymentsResponse`

DeleteAllPayments deletes all outgoing payments from DB. It does not attempt to delete In-Flight payments, since that would be unsafe. The request fields are `failed_payments_only`, `failed_htlcs_only` and `all_payments`; the page notes that `all_payments` requires careful consideration as it is a destructive operation. The response has a `status` field. ([source](../../raw/api/api-docs/api/lnd/lightning/delete-all-payments.md))

## Channel graph and route queries

### DescribeGraph

- gRPC: `rpc DescribeGraph (ChannelGraphRequest) returns (ChannelGraph);`
- REST: `GET /v1/graph`
- Request message: `lnrpc.ChannelGraphRequest`
- Response message: `lnrpc.ChannelGraph`

DescribeGraph returns a description of the latest graph state from the point of view of the node. The graph information is partitioned into two components: all the nodes/vertexes, and all the edges that connect the vertexes. As this is a directed graph, the edges also contain the node directional specific routing policy, which includes the time lock delta and fee information. If `include_unannounced` is set, unannounced channels are included; `include_auth_proof` includes announcements' signatures into ChannelEdge. `lnrpc.ChannelGraph` has the fields `nodes` and `edges`. ([source](../../raw/api/api-docs/api/lnd/lightning/describe-graph.md))

### GetChanInfo

- gRPC: `rpc GetChanInfo (ChanInfoRequest) returns (ChannelEdge);`
- REST: `GET /v1/graph/edge/{chan_id}`
- Request message: `lnrpc.ChanInfoRequest`
- Response message: `lnrpc.ChannelEdge`

GetChanInfo returns the latest authenticated network announcement for the given channel identified by its channel ID: an 8-byte integer which uniquely identifies the location of the transaction's funding output within the blockchain. The request fields are `chan_id`, `chan_point` (ignored if `chan_id` is specified) and `include_auth_proof`. `lnrpc.ChannelEdge` has the fields `channel_id`, `chan_point`, `last_update`, `node1_pub`, `node2_pub`, `capacity`, `node1_policy`, `node2_policy`, `custom_records` and `auth_proof`; `auth_proof` is not filled by default. ([source](../../raw/api/api-docs/api/lnd/lightning/get-chan-info.md))

### GetNodeInfo

- gRPC: `rpc GetNodeInfo (NodeInfoRequest) returns (NodeInfo);`
- REST: `GET /v1/graph/node/{pub_key}`
- Request message: `lnrpc.NodeInfoRequest`
- Response message: `lnrpc.NodeInfo`

GetNodeInfo returns the latest advertised, aggregated, and authenticated channel information for the specified node identified by its public key. The request fields are `pub_key`, `include_channels` and `include_auth_proof`, the last depending on `include_channels`. `lnrpc.NodeInfo` has the fields `node`, `num_channels`, `total_capacity` and `channels`. ([source](../../raw/api/api-docs/api/lnd/lightning/get-node-info.md))

### GetNodeMetrics

- gRPC: `rpc GetNodeMetrics (NodeMetricsRequest) returns (NodeMetricsResponse);`
- REST: `GET /v1/graph/nodemetrics`
- Request message: `lnrpc.NodeMetricsRequest`
- Response message: `lnrpc.NodeMetricsResponse`

GetNodeMetrics returns node metrics calculated from the graph. Currently the only supported metric is betweenness centrality of individual nodes. The request field is `types`; the response field is `betweenness_centrality`. ([source](../../raw/api/api-docs/api/lnd/lightning/get-node-metrics.md))

### GetNetworkInfo

- gRPC: `rpc GetNetworkInfo (NetworkInfoRequest) returns (NetworkInfo);`
- REST: `GET /v1/graph/info`
- Request message: `lnrpc.NetworkInfoRequest`
- Response message: `lnrpc.NetworkInfo`

GetNetworkInfo returns some basic stats about the known channel graph from the point of view of the node. The request has no parameters. `lnrpc.NetworkInfo` has the fields `graph_diameter`, `avg_out_degree`, `max_out_degree`, `num_nodes`, `num_channels`, `total_network_capacity`, `avg_channel_size`, `min_channel_size`, `max_channel_size`, `median_channel_size_sat` and `num_zombie_chans`. ([source](../../raw/api/api-docs/api/lnd/lightning/get-network-info.md))

### SubscribeChannelGraph

- gRPC: `rpc SubscribeChannelGraph (GraphTopologySubscription) returns (stream GraphTopologyUpdate);` (server-streaming RPC)
- REST: `GET /v1/graph/subscribe`
- Request message: `lnrpc.GraphTopologySubscription`
- Response message: `lnrpc.GraphTopologyUpdate`

SubscribeChannelGraph launches a streaming RPC that allows the caller to receive notifications upon any changes to the channel graph topology from the point of view of the responding node. Events notified include new nodes coming online, nodes updating their authenticated attributes, new channels being advertised, updates in the routing policy for a directional channel edge, and channels being closed on-chain. The request has no parameters; `lnrpc.GraphTopologyUpdate` has the fields `node_updates`, `channel_updates` and `closed_chans`. ([source](../../raw/api/api-docs/api/lnd/lightning/subscribe-channel-graph.md))

### QueryRoutes

- gRPC: `rpc QueryRoutes (QueryRoutesRequest) returns (QueryRoutesResponse);`
- REST: `GET /v1/graph/routes/{pub_key}/{amt}`
- Request message: `lnrpc.QueryRoutesRequest`
- Response message: `lnrpc.QueryRoutesResponse`

QueryRoutes attempts to query the daemon's Channel Router for a possible route to a target destination capable of carrying a specific amount of satoshis. The returned route contains the full details required to craft and send an HTLC, including the information that should be present within the Sphinx packet encapsulated within the HTLC. When using REST, the `dest_custom_records` map type can be set by appending `&dest_custom_records[<record_number>]=<record_data_base64_url_encoded>` to the URL. Request fields include `pub_key`, `amt`, `amt_msat`, `final_cltv_delta`, `fee_limit`, `ignored_nodes`, `source_pub_key`, `use_mission_control`, `ignored_pairs`, `cltv_limit`, `last_hop_pubkey`, `route_hints`, `blinded_payment_paths`, `time_pref` and `outgoing_chan_ids`. `amt` and `amt_msat` are mutually exclusive. If `fee_limit` is not specified, lnd uses a default value of 100% fees for small amounts (<=1k sat) or 5% fees for larger amounts. `time_pref` is set to -1 to optimize for fees only, to 1 to optimize for reliability only, or a value in between for a mix. The response fields are `routes` and `success_prob`. ([source](../../raw/api/api-docs/api/lnd/lightning/query-routes.md))

## Routing fees and forwarding history

### FeeReport

- gRPC: `rpc FeeReport (FeeReportRequest) returns (FeeReportResponse);`
- REST: `GET /v1/fees`
- Request message: `lnrpc.FeeReportRequest`
- Response message: `lnrpc.FeeReportResponse`

FeeReport allows the caller to obtain a report detailing the current fee schedule enforced by the node globally for each channel. The request has no parameters. The response fields are `channel_fees`, `day_fee_sum`, `week_fee_sum` and `month_fee_sum`, the sums being the fee revenue (in satoshis) the switch has collected over the past 24 hrs, 1 week and 1 month. ([source](../../raw/api/api-docs/api/lnd/lightning/fee-report.md))

### UpdateChannelPolicy

- gRPC: `rpc UpdateChannelPolicy (PolicyUpdateRequest) returns (PolicyUpdateResponse);`
- REST: `POST /v1/chanpolicy`
- Request message: `lnrpc.PolicyUpdateRequest`
- Response message: `lnrpc.PolicyUpdateResponse`

UpdateChannelPolicy allows the caller to update the fee schedule and channel policies for all channels globally, or a particular channel. The request fields are `global`, `chan_point`, `base_fee_msat`, `fee_rate`, `fee_rate_ppm`, `time_lock_delta`, `max_htlc_msat`, `min_htlc_msat`, `min_htlc_msat_specified`, `inbound_fee` and `create_missing_edge`. If `global` is set the update applies to all currently active channels, and if `chan_point` is set it targets a specific channel. `min_htlc_msat` is only applied if `min_htlc_msat_specified` is true. The response field `failed_updates` is the list of failed policy updates. ([source](../../raw/api/api-docs/api/lnd/lightning/update-channel-policy.md))

### ForwardingHistory

- gRPC: `rpc ForwardingHistory (ForwardingHistoryRequest) returns (ForwardingHistoryResponse);`
- REST: `POST /v1/switch`
- Request message: `lnrpc.ForwardingHistoryRequest`
- Response message: `lnrpc.ForwardingHistoryResponse`

ForwardingHistory allows the caller to query the htlcswitch for a record of all HTLCs forwarded within the target time range, and integer offset within that time range, for a maximum number of events. If no maximum number of events is specified, up to 100 events are returned; if no time-range is specified, events are returned in the order that they occurred. The page says each message can only contain 50k entries, and that each response has the index offset of the last entry, which can be provided to the request to skip a series of records. Request fields are `start_time`, `end_time`, `index_offset`, `num_max_events`, `peer_alias_lookup`, `incoming_chan_ids` and `outgoing_chan_ids`; response fields are `forwarding_events` and `last_offset_index`. ([source](../../raw/api/api-docs/api/lnd/lightning/forwarding-history.md))

## Macaroons and RPC middleware

### BakeMacaroon

- gRPC: `rpc BakeMacaroon (BakeMacaroonRequest) returns (BakeMacaroonResponse);`
- REST: `POST /v1/macaroon`
- Request message: `lnrpc.BakeMacaroonRequest`
- Response message: `lnrpc.BakeMacaroonResponse`

BakeMacaroon allows the creation of a new macaroon with custom read and write permissions. No first-party caveats are added since this can be done offline. The request fields are `permissions`, `root_key_id` (must be a positive integer) and `allow_external_permissions`; the response field `macaroon` is the hex encoded macaroon, serialized in binary format. ([source](../../raw/api/api-docs/api/lnd/lightning/bake-macaroon.md))

### ListMacaroonIDs

- gRPC: `rpc ListMacaroonIDs (ListMacaroonIDsRequest) returns (ListMacaroonIDsResponse);`
- REST: `GET /v1/macaroon/ids`
- Request message: `lnrpc.ListMacaroonIDsRequest`
- Response message: `lnrpc.ListMacaroonIDsResponse`

ListMacaroonIDs returns all root key IDs that are in use. The request has no parameters; the response field is `root_key_ids`. ([source](../../raw/api/api-docs/api/lnd/lightning/list-macaroon-i-ds.md))

### DeleteMacaroonID

- gRPC: `rpc DeleteMacaroonID (DeleteMacaroonIDRequest) returns (DeleteMacaroonIDResponse);`
- REST: `DELETE /v1/macaroon/{root_key_id}`
- Request message: `lnrpc.DeleteMacaroonIDRequest`
- Response message: `lnrpc.DeleteMacaroonIDResponse`

DeleteMacaroonID deletes the specified macaroon ID and invalidates all macaroons derived from that ID. The request field is `root_key_id`; the response field `deleted` is a boolean indicating that the deletion is successful. ([source](../../raw/api/api-docs/api/lnd/lightning/delete-macaroon-i-d.md))

### ListPermissions

- gRPC: `rpc ListPermissions (ListPermissionsRequest) returns (ListPermissionsResponse);`
- REST: `GET /v1/macaroon/permissions`
- Request message: `lnrpc.ListPermissionsRequest`
- Response message: `lnrpc.ListPermissionsResponse`

ListPermissions lists all RPC method URIs and their required macaroon permissions to access them. The request has no parameters; the response field is `method_permissions`. ([source](../../raw/api/api-docs/api/lnd/lightning/list-permissions.md))

### CheckMacaroonPermissions

- gRPC: `rpc CheckMacaroonPermissions (CheckMacPermRequest) returns (CheckMacPermResponse);`
- REST: `POST /v1/macaroon/checkpermissions`
- Request message: `lnrpc.CheckMacPermRequest`
- Response message: `lnrpc.CheckMacPermResponse`

CheckMacaroonPermissions checks whether the provided macaroon contains all the provided permissions. If the macaroon is valid (e.g. all caveats are satisfied) and all permissions provided in the request are met, the RPC returns true. The request fields are `macaroon`, `permissions`, `fullMethod` and `check_default_perms_from_full_method`. If the list of permissions given is empty, the macaroon is considered valid only based on issuance authority and caveat validity. If `check_default_perms_from_full_method` is true, the permissions list must be empty and the default permissions for the provided `fullMethod` are used. The response field is `valid`. ([source](../../raw/api/api-docs/api/lnd/lightning/check-macaroon-permissions.md))

### RegisterRPCMiddleware

- gRPC: `rpc RegisterRPCMiddleware (stream RPCMiddlewareResponse) returns (stream RPCMiddlewareRequest);` (bidirectional-streaming RPC)
- REST: `POST /v1/middleware`
- Request message: `lnrpc.RPCMiddlewareResponse`
- Response message: `lnrpc.RPCMiddlewareRequest`

RegisterRPCMiddleware adds a new gRPC middleware to the interceptor chain. The page describes a gRPC middleware as a software component external to lnd that adds business logic by observing/intercepting/validating incoming gRPC client requests and, if needed, replacing/overwriting outgoing messages before they are sent to the client. When registering, the middleware must identify itself and indicate what custom macaroon caveats it wants to be responsible for; only requests that contain a macaroon with that specific custom caveat are then sent to it for inspection. The other option is to register for the read-only mode, in which all requests/responses are forwarded to the middleware but it is not allowed to modify any responses. As a security measure, no middleware can modify responses for requests made with unencumbered macaroons. The client sends `lnrpc.RPCMiddlewareResponse` messages (`ref_msg_id`, `register`, `feedback`) and the server sends `lnrpc.RPCMiddlewareRequest` messages, with fields including `request_id`, `raw_macaroon`, `custom_caveat_condition`, `stream_auth`, `request`, `response`, `reg_complete` and `msg_id`. ([source](../../raw/api/api-docs/api/lnd/lightning/register-r-p-c-middleware.md))

## Notes

Writer's note (not from the sources): the nine group headings on this page are an editorial grouping of the 67 RPCs for readability; the reference itself lists them as one flat service. Field lists introduced with "include" are selections, not the full message definitions; the linked RPC pages have every field.
