---
title: lnd macaroons
type: howto
sources:
  - raw/docs/lightning-network-tools/lnd/macaroons.md
  - raw/docs/lightning-network-tools/lnd/lnd.conf.md
  - raw/docs/lightning-network-tools/lnd/probing-with-estimateroutefee.md
updated: 2026-11-14
---

# lnd macaroons

How to inspect, bake, constrain, revoke and use macaroons with [[lnd]], how to avoid writing macaroon files to disk, and which RPCs each permission action covers. The general concept is on [[macaroons]].

## What they are

LND, Loop, Pool and litd all use macaroons to authenticate RPC calls. Like cookies they are bearer instruments, but the server can verify them with HMACs and a root key alone, and both server and user can attenuate them, down to individual RPC calls. ([source](../../raw/docs/lightning-network-tools/lnd/macaroons.md))

## Default macaroons

LND generates eight macaroons by default. Inspect any of them with `lncli printmacaroon --macaroon_file ~/path/to/macaroon`. ([source](../../raw/docs/lightning-network-tools/lnd/macaroons.md))

| Macaroon | Permissions |
|---|---|
| `admin.macaroon` | all |
| `chainnotifier.macaroon` | onchain: read |
| `invoices.macaroon` | invoices: read & write |
| `invoice.macaroon` | address, invoice: read & write; onchain: read |
| `readonly.macaroon` | address, info, invoices, macaroon, message, offchain, onchain, peers, signer: read |
| `router.macaroon` | offchain: read & write |
| `signer.macaroon` | signer: generate & read |
| `walletkit.macaroon` | address, onchain: read & write |

([source](../../raw/docs/lightning-network-tools/lnd/macaroons.md))

Their locations are configurable in `lnd.conf`: `adminmacaroonpath`, `readonlymacaroonpath`, `invoicemacaroonpath` (defaulting to `~/.lnd/data/chain/bitcoin/${network}/`), `signrpc.signermacaroonpath`, `walletrpc.walletkitmacaroonpath`, `chainrpc.notifiermacaroonpath` and `routerrpc.routermacaroonpath`. The sample notes that any application able to read the admin macaroon file gains admin access, and that `no-macaroons=true` disables macaroon authentication. See [[lnd-configuration]]. ([source](../../raw/docs/lightning-network-tools/lnd/lnd.conf.md))

## Baking custom macaroons

Creating a macaroon is "baking", done with `lncli bakemacaroon`: ([source](../../raw/docs/lightning-network-tools/lnd/macaroons.md))

```
lncli bakemacaroon peers:read peers:write
lncli bakemacaroon uri:/lnrpc.Lightning/GetInfo uri:/verrpc.Versioner/GetVersion
```

`lncli listpermissions` lists all available restrictions. New macaroons use root key 0 by default; `--root_key_id` picks another (even one that does not yet exist). `--save_to` writes to a file instead of returning hex. Macaroons can also be bound to an IP address, and `--allow_external_permissions` adds permissions LND does not itself understand. To get a file's hex value, use `xxd -ps -u -c 1000 /path/to.macaroon`. ([source](../../raw/docs/lightning-network-tools/lnd/macaroons.md))

For example, a probing-only macaroon for EstimateRouteFee is baked with `lncli bakemacaroon offchain:read` (see [[lnd-sending-payments]]). ([source](../../raw/docs/lightning-network-tools/lnd/probing-with-estimateroutefee.md))

## Constraining and revoking

Any existing macaroon can be restrained further, even one you did not issue. For example, this limits the admin macaroon to calls made from localhost and takes away its authority to perform on-chain actions:

```
lncli constrainmacaroon --ip_address 127.0.0.1 --custom_caveat_name onchain --custom_caveat_condition read admin.macaroon constrained.macaroon
lncli printmacaroon --macaroon_file constrained.macaroon
```

The printed result shows `root_key_id`, `permissions` and `caveats` such as `ipaddr 127.0.0.1` and `lnd-custom onchain read`. ([source](../../raw/docs/lightning-network-tools/lnd/macaroons.md))

Deleting a macaroon file does not revoke it; its root key must be deleted. Find the root key with `lncli printmacaroon`, then run `lncli deletemacaroonid root_key_id`. ([source](../../raw/docs/lightning-network-tools/lnd/macaroons.md))

## Using macaroons with gRPC and REST

Over the wire a macaroon is hex-encoded and passed as gRPC metadata. Over REST the header is `Grpc-Metadata-macaroon: <macaroon>`, for example: ([source](../../raw/docs/lightning-network-tools/lnd/macaroons.md))

```
curl --insecure --header "Grpc-Metadata-macaroon: $(xxd -ps -u -c 1000  $HOME/.lnd/data/chain/bitcoin/simnet/admin.macaroon)" https://localhost:8080/v1/getinfo
```

([source](../../raw/docs/lightning-network-tools/lnd/macaroons.md))

## Stateless initialization

The default macaroon files are unencrypted, and `admin.macaroon` gives full access, which is a risk in an untrusted environment; the wallet file and the macaroon database holding the root key are always encrypted. With stateless initialization, `lncli create`, `unlock` and `changepassword` take `--stateless_init`, which tells the daemon not to create `*.macaroon` files. `create` and `changepassword` return the admin macaroon in the RPC response (printed, or saved with `--save_to=some_file.macaroon`). By default lnd creates the macaroon files during `unlock`, so use the flag for all three commands. ([source](../../raw/docs/lightning-network-tools/lnd/macaroons.md))

`changepassword` by default only re-encrypts the root key, so earlier macaroons stay valid; add `--new_mac_root_key` to invalidate all previously created macaroons. ([source](../../raw/docs/lightning-network-tools/lnd/macaroons.md))

```
lncli create --stateless_init --save_to=/safe/location/admin.macaroon
lncli unlock --stateless_init
lncli --macaroonpath=/safe/location/admin.macaroon getinfo
```

([source](../../raw/docs/lightning-network-tools/lnd/macaroons.md))

See [[lnd-wallet-and-psbt]] for the wallet commands themselves.

## Actions and RPC permissions

The guide maps each action to `lnrpc.Lightning` RPCs (abridged here; the guide lists them all): ([source](../../raw/docs/lightning-network-tools/lnd/macaroons.md))

| Action | Examples of RPCs covered |
|---|---|
| `onchain` | `SendCoins`, `ListUnspent`, `SendMany`, `OpenChannel`, `BatchOpenChannel`, `CloseChannel`, `WalletBalance`, `ChannelBalance`, `GetTransactions`, `ChannelAcceptor`, `FundingStateStep` |
| `address` | `NewAddress` |
| `message` | `SignMessage`, `VerifyMessage` |
| `peers` | `ConnectPeer`, `DisconnectPeer`, `ListPeers`, `SubscribePeerEvents` |
| `offchain` | `ListChannels`, `PendingChannels`, `SendPayment`, `SendToRoute`, `ListPayments`, `DecodePayReq`, `UpdateChannelPolicy`, `ForwardingHistory`, `ExportAllChannelBackups`, `SendCustomMessage`, `ListAliases` |
| `info` | `GetInfo`, `DescribeGraph`, `GetChanInfo`, `GetNodeInfo`, `QueryRoutes`, `StopDaemon`, `DebugLevel`, `FeeReport`, `ListPermissions` |
| `invoices` | `AddInvoice`, `LookupInvoice`, `ListInvoices`, `SubscribeInvoices` |
| `macaroon` | `BakeMacaroon`, `ListMacaroonIDs`, `DeleteMacaroonID`, `CheckMacaroonPermissions`, `/lnrpc.RegisterRPCMiddlewareURI` |

([source](../../raw/docs/lightning-network-tools/lnd/macaroons.md))

## Conflicts

- Number of actions: the guide says macaroons "may refer to one of seven actions" and then lists eight: `onchain`, `address`, `message`, `peers`, `offchain`, `info`, `invoices` and `macaroon` ([source](../../raw/docs/lightning-network-tools/lnd/macaroons.md)).

See also: [[macaroons]], [[lnd-lightning]], [[lnd-configuration]], [[lnd-interceptors]], [[running-lnd]].
