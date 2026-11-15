---
title: The Taproot Assets protocol
type: concept
sources:
  - raw/docs/the-lightning-network/taproot-assets.md
  - raw/docs/the-lightning-network/taproot-assets/taproot-assets-protocol.md
  - raw/docs/the-lightning-network/taproot-assets/faq.md
updated: 2026-11-14
---

# The Taproot Assets protocol

Taproot Assets (formerly Taro) is a Taproot-powered protocol for issuing assets on the bitcoin blockchain that can be transferred over the Lightning Network for instant, high volume, low fee transactions. ([source](../../raw/docs/the-lightning-network/taproot-assets.md))

The guide summarises the protocol in four points: it allows assets to be issued on the bitcoin blockchain; it leverages taproot for privacy and scalability; assets can be deposited into Lightning channels; and assets can be transferred over the existing Lightning Network. ([source](../../raw/docs/the-lightning-network/taproot-assets.md))

Taproot Assets is primarily an on-chain protocol: assets are issued on the bitcoin blockchain using taproot transactions. This page covers the on-chain protocol. Channels, edge nodes and swaps are on [[taproot-assets-on-lightning]]; the daemon is on [[taproot-assets]]; terms are defined in the [[glossary]]. ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-protocol.md))

## Design in brief

Taproot Assets relies on Taproot for a tree structure that allows developers to embed arbitrary asset metadata within an existing output. It uses Schnorr signatures, and works with multi-hop transactions over Lightning. ([source](../../raw/docs/the-lightning-network/taproot-assets.md))

It uses a Sparse-Merkle Tree to enable fast, efficient, private retrieval and updates to the witness/transaction data, and a Merkle-Sum Tree to prove valid conservation/non-inflation. ([source](../../raw/docs/the-lightning-network/taproot-assets.md))

Participants in a Taproot Assets transfer bear the costs of verification and storage by storing witness data off-chain in local data stores or with information repositories termed "Universes" (akin to a git repository). To check an asset's validity, its lineage since its genesis output is verified, using a verification file of transaction data received through the Taproot Assets gossip layer. ([source](../../raw/docs/the-lightning-network/taproot-assets.md))

## Features and limitations listed by the guide

- Light client-friendly: low verification costs, needing only access to untrusted bitcoin transactions, and no knowledge of the entire blockchain. ([source](../../raw/docs/the-lightning-network/taproot-assets.md))
- Atomic swaps between assets and BTC. ([source](../../raw/docs/the-lightning-network/taproot-assets.md))
- Both unique and non-unique assets, as well as collections. ([source](../../raw/docs/the-lightning-network/taproot-assets.md))
- Creative multi-signature and co-signatory arrangements. ([source](../../raw/docs/the-lightning-network/taproot-assets.md))
- Taproot Assets channels can be created alongside BTC channels in the same utxo. For instance, Alice can create two channels with Bob in a single Bitcoin transaction, one containing an asset, the other BTC. ([source](../../raw/docs/the-lightning-network/taproot-assets.md))
- Future features may include confidential transactions and zero-knowledge proofs as part of Taproot Asset transfers. ([source](../../raw/docs/the-lightning-network/taproot-assets.md))

## Building blocks

### Taproot transactions

Taproot is a transaction type defined in BIP 341 and functional on Bitcoin mainnet as of November 2021. Its main difference from conventional Bitcoin transactions is that the scripts controlling coins are contained within a tree structure called the 'tapScript branch', which is privately committed into the transaction. The scripts do not need to be revealed if the KeySpend path is used to move the coins. ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-protocol.md))

If the keyspend path is infeasible, only the executed portion of the script is revealed on the blockchain; all other script paths can remain private or be selectively revealed off-chain. For Taproot Assets, this allows arbitrary data to be provably attached to a transaction without revealing the data on-chain. ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-protocol.md))

### Taptweak

A transaction that includes such arbitrary data is called a commitment. Once the transaction has been included in a block, the data is committed to and can no longer be changed or amended. ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-protocol.md))

To commit to data, the public key of the Taproot spending key is tweaked using a trick known as "Taptweak". It allows selectively revealing the data without revealing the private key, or spending the output without revealing the commitment ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-protocol.md)):

```
Q= P+H(P|c)G
```

where Q is the final Taproot public key, P the internal public key, and H(P|c) a hash of the internal public key and the commitment. To sign a transaction, the private key needs to be tweaked with the same hash H(P|c). ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-protocol.md))

### Sparse Merkle trees

A Sparse Merkle tree (SMT) is a data structure in which it can be proven that specific data does not exist within a merkle tree. It is an authenticated key-value store: the key, or location, of a leaf and the content of the leaf are bound to each other. ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-protocol.md))

The contents of the leaf are hashed, and the leaf's position corresponds to the bitmap of the hash digest. This requires a tree of 256 levels and 2^256 leaves. Generation is efficient despite the size because the overwhelming majority of branches contain empty leaves and can be represented with nil hashes. ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-protocol.md))

Because every item has its predetermined location, the tree's root hash does not depend on the order in which items are inserted. With a Sparse Merkle tree, data can be associated with public keys, and it can be proven that this data was deleted without revealing the entire tree. ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-protocol.md))

### Merkle sum trees

Merkle sum trees are a type of merkle tree that contains numeric values at each leaf, and each node also carries the sum of the values below it. The root carries the sum of total values in the tree. Merkle sum trees allow efficient verification of conservation (non-inflation) by committing to quantities associated with leaves. ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-protocol.md))

### Combined: sparse Merkle sum trees

Taproot Assets combines Sparse Merkle trees and Merkle sum trees into sparse Merkle sum trees. The root of this tree is added to a taproot tapscript, and together a taproot address is created. The FAQ names the structure a 'Merkle Sum, Sparse Merkle Tree (MS-SMT)'. ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-protocol.md)) ([source](../../raw/docs/the-lightning-network/taproot-assets/faq.md))

Instead of using its own blockchain, Taproot Assets issuers store sparse Merkle sum trees off-chain and issue proofs to asset holders out of band. Owners can independently verify that their account is included in the tree, is filled with the appropriate amount, and that the corresponding taproot transaction exists and is confirmed on the Bitcoin blockchain. ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-protocol.md))

## Issuing assets

### Asset ID

Issuing starts with creating the asset's identifier, a 32-byte asset ID produced by hashing three elements: the outpoint being spent to mint the asset, an asset tag of the minter's choice (e.g. a hash of a brand name), and meta information associated with the asset, such as links, images or documents ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-protocol.md)):

```
asset_id = sha256(genesis_outpoint || asset_tag || asset_meta)
```

Formula as given in the protocol guide. ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-protocol.md))

### Asset script and leaves

The asset script can have inputs and outputs, similar to a Bitcoin transaction. A newly created asset does not contain any Taproot Assets inputs, while an asset transfer does. The output of the asset script defines who the newly created assets are issued to, through a sparse Merkle sum tree in which each account is identified by its 256-bit key and the leaf for that key contains information about the amount the account holds. ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-protocol.md))

Multiple assets can be issued in one transaction, but each asset has its own asset script and, within it, sparse Merkle tree. Assets can be unique or non-unique. ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-protocol.md))

Each leaf contains a TLV (type, length, value) blob, akin to the TLV used in the Lightning Network, with information such as versions, asset id, amount, and data pertaining to previous transfers of the asset, such as signatures. ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-protocol.md))

### Commit and publish

Once the sparse Merkle sum tree and asset script are generated, the internal public key is tweaked to obtain the contract's address and the transaction is finalized. Once the transaction is published and confirmed on the bitcoin blockchain, the asset has been irreversibly created. To an observer the transaction looks like any other standard taproot transaction. ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-protocol.md))

### Asset proof

The issuer can selectively reveal what assets were created and to whom they were allotted. The issuer proves to a recipient that an asset has been transferred to them by revealing a specific asset proof, which contains the asset script and the path of the sparse Merkle sum tree with the recipient's account as the key. ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-protocol.md))

The recipient can verify the partial sparse Merkle sum tree to recreate the script, tweak the issuer's public key, and verify that the genesis transaction exists on the blockchain. The partial Merkle tree gives them assurance over the assets issued to them and the total number of assets issued. ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-protocol.md))

## Transferring assets on-chain

Taproot Assets can be transferred on-chain, or used to open Lightning Network channels. How individual account holders interact with each other is not prescribed by the protocol and can be application specific. ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-protocol.md))

The Asset Root Commitment commits to all assets held inside the tree as well as their sum. The asset_id is globally unique as it depends on the identifier of its genesis output. The overall root can comprise multiple asset_ids, whose conservation of funds is provided by verifying the asset_tree_root ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-protocol.md)):

```
asset_tree_root = sha256(asset_id || left_hash || right_hash || sum_value)
```

Formula as given in the protocol guide. ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-protocol.md))

### Addresses

Taproot Assets addresses are bech32m encoded identifiers of the asset ID, the asset script hash, the internal key of the sparse Merkle sum tree and an amount. The source gives the prefix as "Taproot Assets or `taptb1` (testnet)" and the encoding as ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-protocol.md)):

```
bech32(hrp=TapHrp, asset_id || asset_script_hash || internal_key || amt)
```

The address format can also be used to request a specific proof over the amounts held by the address. ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-protocol.md))

To send Taproot Assets to somebody, they first provide their Taproot Assets address, which contains information about the asset and the public keys necessary for holding it, as well as the requested amount. ([source](../../raw/docs/the-lightning-network/taproot-assets/faq.md))

### Moving assets inside the tree

To transfer, the recipient communicates their address to the current holder, who initiates the transfer. The sender generates a new sparse Merkle sum tree reflecting the new balances, reducing the balances of certain leafs and increasing others. The sparse Merkle sum tree guarantees that no new assets are created in such a transaction and that previous claims to the assets are fully relinquished. ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-protocol.md))

Creating assets requires a single on-chain taproot transaction, with no limit on how many assets can be minted or how many accounts can hold them. Transferring assets requires reorganizing the Merkle tree and publishing a new on-chain transaction, with no limit to how many internal Taproot Assets transactions are reflected in that single on-chain transaction. The ability to make such internal transfers is limited to the owner of the internal taproot private key(s). ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-protocol.md))

### Asset split and merge

Assets may be transferred internally within the asset's sparse Merkle tree, or sent to another taproot key holder, which the guide refers to as an asset split. The sender updates the sparse Merkle sum tree of their own taproot output, adjusting the balance(s) and recalculating the Merkle root; in the case of a merge, the root sum also changes. A second sparse Merkle sum tree, calculated by the recipient, is committed to a new taproot output. ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-protocol.md))

To verify that an asset split has taken place, the operator of the new Universe needs proof that ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-protocol.md)):

- assets were created at transaction zero (t0); ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-protocol.md))
- assets existed on a leaf in the original Merkle tree at t0; ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-protocol.md))
- the balance of this leaf was set to zero at t1; ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-protocol.md))
- the assets existed on a leaf of the new Merkle tree at t1. ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-protocol.md))

Each proof before the split always needs to include the Issuance proof for provenance verification. Asset proofs grow linearly with each new on-chain transaction, and every asset transaction needs to be audited back to its Genesis output. An asset proof is only valid as long as the output it references is unspent on the blockchain. ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-protocol.md))

### Invalidating (burning) assets

An asset is considered invalid as soon as its output has been spent without committing to a new sparse merkle sum tree. This is not obvious to a third party observer, so in some instances it may be preferable to spend outputs to a new empty merkle tree to prove that assets were destroyed, invalidated, or "burned". ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-protocol.md))

## Universes

A Universe is a service that provides information about assets as well as proofs for asset holders. It acts similarly to a bitcoin block explorer, but showcases Taproot Assets transaction data, which is stored off-chain with Taproot Assets clients. ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-protocol.md))

A Universe may be run by the asset issuer or appointed by an issuer; community-run Universes that aggregate information submitted by asset holders are also conceivable. Given a known asset ID, a Universe may for example provide information about its Genesis output and current meta information such as documentation, asset scripts or total coins in circulation. A service may also know about multiple assets (Multiverse) or only about a single output (Pocket Universe). ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-protocol.md))

A Universe has no privileges within the Taproot Assets Protocol. It produces transaction data validated against the bitcoin blockchain, and an adversarial Universe could only refrain from returning data requested by clients. ([source](../../raw/docs/the-lightning-network/taproot-assets/taproot-assets-protocol.md))

The FAQ describes a pocket universe as a single party (or federation) maintaining a Taproot Assets commitment that includes assets they cannot unilaterally move themselves: it controls the Taproot key to a UTXO, but not the keys to the Taproot Assets held in that UTXO. Asset holders can use it to batch their transactions efficiently, and grouped transactions can share on-chain fees. ([source](../../raw/docs/the-lightning-network/taproot-assets/faq.md))

### Custody matrix

The FAQ's custody table has four cases. User holds both the keys to the taproot UTXO and the asset keys: full self-custody. User holds the asset keys but not the UTXO keys: the user is using a pocket universe. User holds the UTXO keys but not the asset keys: the user is operating a pocket universe. User holds neither: an entirely custodial relationship. ([source](../../raw/docs/the-lightning-network/taproot-assets/faq.md))

## On-chain questions from the FAQ

- What assets can represent: both collectible and fungible (often called normal) assets can be issued, with no technical limits to what they represent; Lightning Labs is focused on stablecoins' use cases first. ([source](../../raw/docs/the-lightning-network/taproot-assets/faq.md))
- Blockchain requirements: a client does not need to keep or scan the entire blockchain; it only requires proofs about specific transactions relating to its assets, which can be obtained in 'Neutrino' mode, also known as BIP157. ([source](../../raw/docs/the-lightning-network/taproot-assets/faq.md))
- Bitcoin requirements: issuing and transacting require bitcoin transactions, which generally require fees paid in BTC, and each output needs to carry a small number of satoshis to be valid. ([source](../../raw/docs/the-lightning-network/taproot-assets/faq.md))
- Issuing: anyone can issue assets using `tapd` on Bitcoin; once the genesis transaction is confirmed, the asset is live and can be transferred. ([source](../../raw/docs/the-lightning-network/taproot-assets/faq.md))
- Supply: the minter defines the asset's rules, and can limit the total supply or leave it uncapped to create additional assets later. ([source](../../raw/docs/the-lightning-network/taproot-assets/faq.md))
- Wallets: a wallet needs to store Taproot keys as well as Taproot Assets keys, plus the knowledge of which assets are held in which UTXOs. If a user loses their asset proof information, a Universe can serve the proof back. ([source](../../raw/docs/the-lightning-network/taproot-assets/faq.md))
- Licence: the Taproot Assets Protocol is released under the BSD-2-Clause license. ([source](../../raw/docs/the-lightning-network/taproot-assets/faq.md))

See also: [[tapd-getting-started]], [[tapd-universes-guide]], [[tapd-universe]], [[tapd-mint]].
