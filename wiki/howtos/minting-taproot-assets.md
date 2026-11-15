---
title: Minting assets, metadata and collectibles
type: howto
sources:
  - raw/docs/lightning-network-tools/taproot-assets/asset-metadata.md
  - raw/docs/lightning-network-tools/taproot-assets/collectibles.md
  - raw/docs/lightning-network-tools/taproot-assets/decimal-display.md
  - raw/docs/lightning-network-tools/taproot-assets/minting-assets-with-an-external-signer.md
  - raw/docs/lightning-network-tools/taproot-assets/first-steps.md
updated: 2026-11-14
---

# Minting assets, metadata and collectibles

The parameters of a new Taproot Asset, its metadata, how to choose the decimal display, how to mint collectibles and collections, and which keys can be held on an external signer. The basic mint, finalize and send flow is on [[tapd-getting-started]].

See also: [[taproot-assets]], [[tapd-mint]], [[tapd-taproot-assets]], [[tapd-rfq-guide]], [[tapd-operations]], [[taproot-assets-protocol]].

## Parameters of a new asset

The Taproot Assets protocol itself places very few restrictions on what data can be associated with a new asset, and how that data should be structured. Additional information can be included as metadata, defined at the time of minting in the form of a json string or file. ([source](../../raw/docs/lightning-network-tools/taproot-assets/asset-metadata.md))

| Parameter | What the guide says |
|---|---|
| Type | An asset can be either set to normal or collectible. A normal asset is divisible into parts of equal value. |
| Name | An asset requires a name. Uniqueness cannot be enforced over this name, so it can't be used to uniquely identify the asset. |
| Supply | The total supply of the asset, including the decimal places. An asset with 1,000 units and three decimal places has a total supply of 1,000,000. |
| Decimal display | The number of decimal places the asset will have. Too few decimal places can result in rounding errors when transferring assets over the Lightning Network. You can choose up to 12 decimal places. |
| Grouped asset | For grouped assets the total supply can later be inflated, while ungrouped assets have a permanently fixed supply. |
| Meta data | Can be added as a string (`--meta_bytes`) or a file on disk (`--meta_file_path`), and be either in opaque or json form (`--meta_type`). |

([source](../../raw/docs/lightning-network-tools/taproot-assets/asset-metadata.md))

## Metadata

There are no formal restrictions on the metadata beyond a 1MB size limit. The guide recommends an emerging standard for stablecoin assets that is expected to maximize interoperability between assets and wallets. Its example json has the keys `spec` (`"stablecoin"`), `version` (`1`), `ticker`, `long_name`, `description` and `logo_image` (a `data:image/svg+xml;base64,...` value). The image is a square of at most 128 pixels, encoded in Base64. ([source](../../raw/docs/lightning-network-tools/taproot-assets/asset-metadata.md))

The metadata of a grouped asset can be updated each time a new tranche is issued. Wallets and explorers should display the metadata associated with the most recent mint. ([source](../../raw/docs/lightning-network-tools/taproot-assets/asset-metadata.md))

The decimal display should be defined through the CLI flag or API parameter. The `tapd` daemon will append it to the json metadata, from where wallets can interpret it. ([source](../../raw/docs/lightning-network-tools/taproot-assets/asset-metadata.md))

The Asset Metadata guide gives this command for retrieving the metadata of a given asset ID:

```
tapcli assets --asset_id <id> | jq -r '.data' | xxd -p -r | jq
```

([source](../../raw/docs/lightning-network-tools/taproot-assets/asset-metadata.md))

## Decimal display

Within the Taproot Assets Protocol, an asset's unit is an integer (`uint64`), so the protocol cannot represent fractions of an asset. An asset that represents a fiat currency therefore needs to issue assets equivalent to at least the smallest unit in use; for example, a US-Dollar asset would be minted so that one asset unit represents one USD cent. Beyond the smallest unit, additional breathing room should be added to ensure minimal precision loss during conversion arithmetic. ([source](../../raw/docs/lightning-network-tools/taproot-assets/decimal-display.md))

Because wallet user interfaces aren't expected to know what precision an asset represents, a field called `decimal_display` was added to the JSON metadata of new assets minted with `tapd v0.4.0-alpha` and later. The field is encoded in the metadata field as a JSON field, therefore it is only compatible with assets that have a JSON metadata field. ([source](../../raw/docs/lightning-network-tools/taproot-assets/decimal-display.md))

An issuer specifies `tapcli assets mint --decimal_display X` to set the number of decimal places the comma should be shifted to the left when displaying a sum of asset units. A USD asset choosing `--decimal_display 2` indicates that 100 units should be displayed as `$1.00` in the wallet UI; 1234 units would be displayed as `$12.34`. ([source](../../raw/docs/lightning-network-tools/taproot-assets/decimal-display.md))

For an owned asset, the decimal display can be viewed with `tapcli assets list`. If the `decimal_display` field is missing or showing as `"decimal_display": null`, the asset is using a value of 0 (no shift in decimal places). For an asset that isn't owned by the local node, but whose issuance information was synced from a universe server, the value can be retrieved from the asset's metadata:

```
tapcli assets meta --asset_id xyz | jq -r '.data' | xxd -p -r
```

([source](../../raw/docs/lightning-network-tools/taproot-assets/decimal-display.md))

### Why precision matters on Lightning

Due to the integer nature of Taproot Asset units, the smallest asset amount that can be transferred with a Lightning Network HTLC is one asset unit. If one unit represents significantly more than a couple of milli-satoshi or even a full satoshi, then due to integer division and rounding up, the user might end up spending noticeably more assets than necessary when paying an invoice (see [[htlc]]). ([source](../../raw/docs/lightning-network-tools/taproot-assets/decimal-display.md))

The guide's first example assumes one USD cent is roughly equivalent to 19 satoshi: a user holding USD cent units who pays a 1 satoshi invoice has to send a full cent, an overpayment of roughly `19x`. Its second example uses Multi-Part Payments with a `decimal_display` value of `2`: paying `1,000,000` satoshi in a single HTLC sends `52,632` units, overpaying by `0.4211` cents, while splitting into 16 parts sends `3290` cents per HTLC, a full `8.4211` cents of overpayment (see [[multipath-payments]]). ([source](../../raw/docs/lightning-network-tools/taproot-assets/decimal-display.md))

### Recommended values

The guide recommends a `decimal_display` value of `6` for currencies which use a smaller subunit with two decimal places (such as cents for USD or EUR, penny for GBP), and a value of `4` for currencies without smaller units (for example JPY or VND). ([source](../../raw/docs/lightning-network-tools/taproot-assets/decimal-display.md))

### Fixing a wrong decimal display

The `decimal_display` value is stored in the `asset_meta` field of the `genesis_asset` that creates a particular `group_key` (or `asset_id`). The value of the `asset_meta` determined the original `asset_id` and `group_key`, so these values are strongly bound. The only way to "fix" the value is to burn all the existing assets and create new assets with the proper decimal display value. This can be done in a single atomic transaction using the gRPC/REST interface; such a transaction would burn the referenced asset inputs and create new asset units under a new group key. ([source](../../raw/docs/lightning-network-tools/taproot-assets/decimal-display.md))

The same guide's sections on RFQ arithmetic and price oracles are summarised on [[tapd-rfq-guide]].

## Collectibles

In addition to fungible, "normal" assets, Taproot Assets supports the creation and transfer of collectible, non-fungible assets. The collectible itself may be referenced in the form of a hash or text, or may be directly embedded in the meta data. When minting, any kind of data can be passed via `--meta_bytes`, such as text, images, encoded data of any form or even a binary blob; alternatively, any file can be passed to tapd with the `--meta_file_path` flag. Meta data is limited to 1MB per asset. ([source](../../raw/docs/lightning-network-tools/taproot-assets/collectibles.md))

```
tapcli assets mint --type collectible --name theone --meta_bytes "One of a kind" --supply 1
tapcli assets mint finalize
```

([source](../../raw/docs/lightning-network-tools/taproot-assets/collectibles.md))

### Collections

Multiple collectibles can be grouped together into a collection. Each asset has its own asset ID, while the collection itself can be identified by its group key. According to the guide, the `--new_group_emission` flag has to be set to create the collection, and each subsequent collectible has to set the `--grouped_asset` flag as well as reference the first collectible by its name (the examples do so with `--group_anchor`). Multiple collectibles can be minted in a batch:

```
tapcli assets mint --type collectible --name member001 --meta_bytes 546170726f6f742041737365747320436c7562204d656d62657220303031 --supply 1 --new_group_emission
tapcli assets mint --type collectible --name member002 --meta_bytes 546170726f6f742041737365747320436c7562204d656d62657220303032 --grouped_asset --supply 1 --group_anchor member001
tapcli assets mint --type collectible --name member003 --meta_bytes 546170726f6f742041737365747320436c7562204d656d62657220303033 --grouped_asset --supply 1 --group_anchor member001
tapcli assets mint finalize
```

([source](../../raw/docs/lightning-network-tools/taproot-assets/collectibles.md))

At this point there is no option to "close" a batch or limit future emissions of that group. ([source](../../raw/docs/lightning-network-tools/taproot-assets/collectibles.md))

## Keys and external signers

There are three keys relevant to issuance of a Taproot Asset: the Bitcoin key controlling the UTXO anchoring the Taproot Asset on the Bitcoin level; the Asset Script key controlling the spending of the vUTXO on the Taproot Asset level; and the Group key that identifies a grouped asset and allows for the expansion of the asset supply. ([source](../../raw/docs/lightning-network-tools/taproot-assets/minting-assets-with-an-external-signer.md))

Each of these keys may be held separately. The group key is the most sensitive, as it can be used to reissue the asset and expand its supply without limits. It cannot be cycled and must be safe for the entire life-cycle of the asset. ([source](../../raw/docs/lightning-network-tools/taproot-assets/minting-assets-with-an-external-signer.md))

As of now, only the group key can be held on an external device. It is defined by a custom derivation path of a standard master key, generated using a general seed phrase. The seed phrase can act as a backup of the key, while the signing device is used to authorize initial and further issuance of the asset. The guide links two external documents in the taproot-assets repository, on generating the group key on an air-gapped machine using Chantools and on a specialized signing device; their contents are not in the sources. ([source](../../raw/docs/lightning-network-tools/taproot-assets/minting-assets-with-an-external-signer.md))

To also hold the Bitcoin key in a hardware wallet, additional work needs to be done to allow for signing of generic Taproot PSBTs. The Asset Script key could be held by a hardware wallet, but the hardware wallet would need some understanding of what it is signing, ideally information of the vPSBT and Bitcoin PSBT. ([source](../../raw/docs/lightning-network-tools/taproot-assets/minting-assets-with-an-external-signer.md))

### Keys involved in a transfer

For transfers, the Bitcoin key controlling the UTXO anchoring the Taproot Asset is held by LND, but LND cannot spend this UTXO alone, not even by accident. To spend the UTXO, and with it the Taproot Asset, the taptweak held by `tapd` is needed. The third key is the Asset Script key spending the vUTXO on the Taproot Asset level. While it is technically possible to keep either the Bitcoin key or the Asset Script key on a dedicated air-gapped or signing device, there is currently no mechanism equipped for that. ([source](../../raw/docs/lightning-network-tools/taproot-assets/minting-assets-with-an-external-signer.md))

A special case is that of pocket universes, where the Bitcoin key is held by a service, while the Asset Script key is held by the user. This allows for the efficient batching of potentially millions of asset transfers in a single Bitcoin transaction. The service does not control the assets of the users and cannot move them independently. ([source](../../raw/docs/lightning-network-tools/taproot-assets/minting-assets-with-an-external-signer.md))

Multisignature arrangements for these keys are on [[tapd-operations]].

## Conflicts

- **Command for reading metadata.** The Asset Metadata guide gives `tapcli assets --asset_id <id> | jq -r '.data' | xxd -p -r | jq` ([source](../../raw/docs/lightning-network-tools/taproot-assets/asset-metadata.md)); the Decimal Display guide gives `tapcli assets meta --asset_id xyz | jq -r '.data' | xxd -p -r` ([source](../../raw/docs/lightning-network-tools/taproot-assets/decimal-display.md)).
- **Flag that starts a new group.** The Collectibles guide uses `--new_group_emission` ([source](../../raw/docs/lightning-network-tools/taproot-assets/collectibles.md)); the First Steps guide uses `--new_grouped_asset` for a normal asset whose supply can be increased later ([source](../../raw/docs/lightning-network-tools/taproot-assets/first-steps.md)). The sources do not say whether both flags are accepted.
- **Adding to an existing group.** The Collectibles guide adds to a group with `--grouped_asset --group_anchor <name of first asset>` within the same batch ([source](../../raw/docs/lightning-network-tools/taproot-assets/collectibles.md)); the First Steps guide adds to a group in a later batch with `--grouped_asset --group_key <key>` ([source](../../raw/docs/lightning-network-tools/taproot-assets/first-steps.md)). These may be two different cases rather than a disagreement; the sources do not say.
