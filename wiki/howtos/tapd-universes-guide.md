---
title: Working with universes
type: howto
sources:
  - raw/docs/lightning-network-tools/taproot-assets/universes.md
updated: 2026-11-14
---

# Working with universes

How to run a universe with `tapd`, use the default universe, manage a federation and sync assets.

See also: [[taproot-assets]], [[tapd-universe]], [[tapd-getting-started]], [[tapd-operations]], [[taproot-assets-protocol]].

## What a universe is

In the context of Taproot Assets, a universe is a service that acts as a repository for publicly minted assets. It contains knowledge of assets, mints, metadata, public transfers and their proofs. A universe is required for users to fetch data necessary to validate transfers, and may be public or private. Anyone may run a universe, or use one or multiple universes provided by others, such as Lightning Labs. ([source](../../raw/docs/lightning-network-tools/taproot-assets/universes.md))

## Your local universe

When running `tapd`, you run a private universe by default. In this mode, all RPC calls to the universe require authentication using the tapd macaroon. To disable macaroon authentication for the `QueryProof` and `InsertProof` RPC calls, set:

```
allow-public-uni-proof-courier=true
```

To further open up the local universe to serve the `QueryAssetStats`, `UniverseStats` and `QueryEvents` RPC calls, set:

```
allow-public-stats=true
```

You may do this to operate a public universe, or make it easier for other applications to reach your API endpoints. ([source](../../raw/docs/lightning-network-tools/taproot-assets/universes.md))

## Running a public universe

Running a universe is as simple as running `tapd` and amending your configuration file. You may run a universe over RPC or REST. By default, `tapd` is expected to listen on gRPC TCP port `10029` and REST TCP port `8089`, so that port has to be open on your machine if you would like others to connect to you. Being publicly reachable is not a requirement for a universe; it may only serve resources on a private network, or be otherwise restricted. ([source](../../raw/docs/lightning-network-tools/taproot-assets/universes.md))

When running `tapd` as part of `litd`, you may also use port `8443` or define your own port. As the REST universe is also usable through a browser over HTTPS, you may configure it over port `443` or set up a proxy (see [[lightning-terminal]]). ([source](../../raw/docs/lightning-network-tools/taproot-assets/universes.md))

Sample `tapd.conf` file:

```
rpclisten=0.0.0.0:10029
restlisten=0.0.0.0:8089
allow-public-uni-proof-courier=true
allow-public-stats=true
universe.public-access=rw
```

([source](../../raw/docs/lightning-network-tools/taproot-assets/universes.md))

You can verify whether your universe is accepting proofs with `tapcli universe federation config info`. The sample output has a `global_sync_configs` list with one entry each for `PROOF_TYPE_ISSUANCE` and `PROOF_TYPE_TRANSFER`, each carrying `allow_sync_insert` and `allow_sync_export`, plus an `asset_sync_configs` list. The configuration can be changed from the CLI with `tapcli universe federation config global --proof_type issuance --allow_insert true`, and again with the `--proof_type transfer` flag. ([source](../../raw/docs/lightning-network-tools/taproot-assets/universes.md))

## The default universe

By default, `tapd` connects to the default universe, for instance `signet.universe.lightning.finance:10029` for signet, or `universe.lightning.finance:10029` on mainnet. The contents of the default universe are also available via a public REST API (`https://universe.lightning.finance/v1/taproot-assets/universe/roots`) and through the UI at `https://terminal.lightning.engineering/assets/`. ([source](../../raw/docs/lightning-network-tools/taproot-assets/universes.md))

## Federations

A federation is a list of universes your `tapd` node connects to. You can see it with `tapcli universe federation list`. At first, the federation consists only of the default universe. If you don't want to use the default universe, set `universe.no-default-federation=true` in `tapd.conf` so that it isn't automatically added to your federation list. ([source](../../raw/docs/lightning-network-tools/taproot-assets/universes.md))

You can manually add universes to the federation that your `tapd` node pushes to and pulls from, and remove them again:

```
tapcli universe federation add --universe_host <universe_ip:port>
tapcli universe federation del --universe_host <universe_ip>:port
```

([source](../../raw/docs/lightning-network-tools/taproot-assets/universes.md))

## Syncing to a universe

By default, `tapd` syncs to the universes configured in your local federation, and only for assets which you either hold or have created a taproot address for. You may also manually sync specific asset IDs or group keys:

```
tapcli universe sync --universe_host <universe_ip:port> --group_key <group key>
```

([source](../../raw/docs/lightning-network-tools/taproot-assets/universes.md))

To configure `tapd` to regularly sync to other asset IDs or group keys, use the universe federation configuration. The `config global` options apply to all assets, while the `config local` options only apply to specific assets:

```
tapcli universe federation config global --proof_type issuance --allow_insert true
tapcli universe federation config local --proof_type transfer --allow_insert true --group_key <group key>
```

([source](../../raw/docs/lightning-network-tools/taproot-assets/universes.md))

## The Universe APIs

A Taproot Asset Universe is available over gRPC and REST on the default ports. You may run your own universe or interact with a public universe. Public universes are unauthenticated; the macaroon checks are skipped. ([source](../../raw/docs/lightning-network-tools/taproot-assets/universes.md))

For instance, when making a transfer, the proofs may be pushed to one or multiple universes using the REST API. The guide says this requires the asset ID, the leaf key index and script key, and gives the path:

```
/v1/taproot-assets/universe/proofs/asset-id/{key.id.asset_id_str}/{key.leaf_key.op.hash_str}/{key.leaf_key.op.index}/{key.leaf_key.script_key_str}
```

The RPC reference for the universe service is on [[tapd-universe]]. ([source](../../raw/docs/lightning-network-tools/taproot-assets/universes.md))
