---
title: Glossary
type: concept
sources:
  - raw/docs/community-resources/glossary.md
  - raw/docs/the-lightning-network/taproot-assets/glossary.md
updated: 2026-11-14
---

# Glossary

This page reproduces the definitions from the two glossaries in the Builder's Guide: the community Lightning Network glossary and the Taproot Assets glossary. Each entry is cited to the glossary it comes from; where both glossaries define a term, it appears once in each section. Inline cross-reference links and "Read more" pointers of the source pages are omitted. ([source](../../raw/docs/community-resources/glossary.md)) ([source](../../raw/docs/the-lightning-network/taproot-assets/glossary.md))

Concept pages that expand on these terms: [[lightning-network-overview]], [[payment-channels]], [[htlc]], [[multihop-payments]], [[pathfinding]], [[channel-fees]], [[multipath-payments]], [[liquidity]], [[inbound-capacity]], [[lightning-service-providers]], [[merchant-liquidity]], [[l402]], [[macaroons]], [[taproot-assets-protocol]], [[taproot-assets-on-lightning]].

## Lightning Network terms

**9735**: The default port used by Lightning nodes to advertise incoming peer-to-peer connections. ([source](../../raw/docs/community-resources/glossary.md))

**Aezeed**: Aezeed is the mechanism through which the private keys of a LND node are derived from a seed phrase. Unlike other popular seed phrase formats, it allows for versioning and wallet birth dates. ([source](../../raw/docs/community-resources/glossary.md))

**Anchor channel**: Anchor channels include up to two special outputs called anchors which are used for timely CPFP fee-bumping of force-closed channels. ([source](../../raw/docs/community-resources/glossary.md))

**Aperture**: Aperture is an implementation of a L402 proxy server developed by Lightning Labs. See [[aperture]]. ([source](../../raw/docs/community-resources/glossary.md))

**Asset merge**: If two assets of the same kind are combined, this is called an asset merge. ([source](../../raw/docs/community-resources/glossary.md))

**Asset split**: If an asset is divided into two parts, it is split. ([source](../../raw/docs/community-resources/glossary.md))

**Atomic**: Atomic refers to an action that is either completed in its entirety, or not at all. Lightning payments are atomic across routes, in that they either reach their destination or never leave their origin. Submarine swaps are atomic, in that either the swap succeeds or funds never leave their origin, and AMPs are atomic in that either all shards arrive at the destination, or none. ([source](../../raw/docs/community-resources/glossary.md))

**Atomic Multi-path Payments**: Atomic Multi-path Payments (AMP) is a payment standard that allows a payment to be made over multiple channels. Unlike MPP each individual shard has its own payment hash, which allows for payments being made atomically. AMP also allows for static invoices and to send funds solely using the recipient's public key, as well as attaching messages to these payments. See [[multipath-payments]]. ([source](../../raw/docs/community-resources/glossary.md))

**Autoloop**: Autoloop is a mechanism of Loop to automatically perform Loop In and Out based on predefined thresholds. It is used for liquidity management. See [[autoloop]]. ([source](../../raw/docs/community-resources/glossary.md))

**Base fee**: A Lightning node can charge a fee for each forwarded payment. This fee includes the base fee, which is a constant amount charged for each forward, typically 1 satoshi. See [[channel-fees]]. ([source](../../raw/docs/community-resources/glossary.md))

**Base58**: An encoding scheme for Bitcoin addresses conceived by Satoshi Nakamoto, consisting of both uppercase and lowercase letters and numbers. An example of a Base58 encoded address: 1JqDybm2nWTENrHvMyafbSXXtTk5Uv5QAn ([source](../../raw/docs/community-resources/glossary.md))

**Basics of Lightning Technology**: Basics of Lightning Technology (BOLT) is the name of the Lightning Network protocol standard. A given implementation of the Lightning Network needs to follow all rules laid out by the BOLT standard to be considered a full Lightning Node. ([source](../../raw/docs/community-resources/glossary.md))

**Bech32**: An encoding scheme for Bitcoin addresses and Lightning invoices, recognizable by either being all uppercase or lowercase. Example of a bech32 address: bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4 ([source](../../raw/docs/community-resources/glossary.md))

**BIP157**: BIP 157 is a standard that allows full Bitcoin nodes to serve Lightning Network light clients. It is often referred to as Neutrino. ([source](../../raw/docs/community-resources/glossary.md))

**Bitcoin**: Bitcoin is a network established in 2009 by Satoshi Nakamoto. It introduces the bitcoin currency, which is used in the Lightning Network for fast and cheap payments. ([source](../../raw/docs/community-resources/glossary.md))

**Bitcoin Core**: Popular software used as a backend for LND to look up on-chain balances and verify channel states. See also bitcoind. ([source](../../raw/docs/community-resources/glossary.md))

**bitcoind**: The Bitcoin Daemon (bitcoind) is the most popular software used to connect to the Bitcoin network, verify and broadcast payments. It commonly serves as a backend for LND. See also Bitcoin Core. ([source](../../raw/docs/community-resources/glossary.md))

**BoS**: Balance of Satoshis (BoS) is software developed by Alex Bosworth to assist a node operator with setting fees or circular rebalancing. ([source](../../raw/docs/community-resources/glossary.md))

**btcd**: BTCD is an implementation of the Bitcoin protocol written in go. It is a popular alternative to bitcoind for LND node operators ([source](../../raw/docs/community-resources/glossary.md))

**Chain**: The Bitcoin Blockchain contains all transactions ever made in Bitcoin. A LND node uses bitcoind or btcd to inspect the chain and verify payment channels, as well as payments that were sent and received on-chain. ([source](../../raw/docs/community-resources/glossary.md))

**Channel**: See Payment channel. ([source](../../raw/docs/community-resources/glossary.md))

**Channel breach**: When a peer publishes an invalid commitment transaction in an attempt to steal funds, this is considered a channel breach. Such breaches need to be detected within the time lock either by the node or a watchtower to be successfully contested. ([source](../../raw/docs/community-resources/glossary.md))

**Channel point**: The channel point is the transaction ID and output ID that establishes a Lightning channel. It is typically expressed by `<txid>:<output>`. ([source](../../raw/docs/community-resources/glossary.md))

**Channel stability**: A channel that is always online and able to route payments in both directions is considered stable. To be stable, a channel needs to have two stable peers that carefully manage their liquidity. ([source](../../raw/docs/community-resources/glossary.md))

**Chantools**: Chantools is a channel and fund recovery tool for Lightning nodes written by Oliver Gugger. ([source](../../raw/docs/community-resources/glossary.md))

**Circular Rebalance**: A circular rebalance is a payment from a node to itself through an external path, often used to shift balances from one channel to another. ([source](../../raw/docs/community-resources/glossary.md))

**C-Lightning**: C-Lightning is an implementation of a Lightning Network node written in C by Blockstream. ([source](../../raw/docs/community-resources/glossary.md))

**CLTV**: Check Lock-time Verify is a functionality in Bitcoin that allows us to lock Bitcoin for a period of time. It is an important part of the mechanism of a commitment transaction. Defined in BIP 65. ([source](../../raw/docs/community-resources/glossary.md))

**Clustering**: Clustering allows us to use multiple LND nodes to form a cluster, in which we can delegate specific tasks such as managing invoices or maintaining channels for performance or security purposes. ([source](../../raw/docs/community-resources/glossary.md))

**Commitment**: In the context of cryptography, committing refers to the act of proving that certain data exists at a point in time, without necessarily revealing the data. Typically, this is done with a hash of the data. Only an entity that knows about the full data would have been able to produce a hash of it, thus, proving its existence. ([source](../../raw/docs/community-resources/glossary.md))

**Commitment fee**: The commitment fee is the fee a commitment transaction pays to the Bitcoin miner. Since the commitment fee needs to be calculated well in advance, it can sometimes be larger than necessary. Anchor channels help alleviate this problem and better calculate this fee. ([source](../../raw/docs/community-resources/glossary.md))

**Commitment transaction**: The commitment transaction refunds you the balance in your Lightning channel in the event that your peer goes offline or becomes uncooperative. Also see force closure. ([source](../../raw/docs/community-resources/glossary.md))

**Check Sequence Verify**: Check Sequence Verify is a functionality in Bitcoin that allows us to lock Bitcoin relative to its input transaction. It is an important part of the mechanism of a sweep transaction. Defined in BIP 112. ([source](../../raw/docs/community-resources/glossary.md))

**CPFP**: Child Pays For Parent is a method of effectively increasing the fee of an unconfirmed on-chain transaction (parent) by spending one of its outputs with a fee high enough to cover both the parent and the child transaction. To collect the high fee of the child transaction, a miner now has to include both the child and the parent transaction into a block. Unlike RBF this mechanism can also be used by the recipient of a transaction. ([source](../../raw/docs/community-resources/glossary.md))

**Custodial Channel**: A custodial channel is a channel that is not committed on the Bitcoin blockchain. As such, all funds in it are in the custody of one party. ([source](../../raw/docs/community-resources/glossary.md))

**Eclair**: Eclair is an implementation of a Lightning Network node written in Scala by ACINQ. ([source](../../raw/docs/community-resources/glossary.md))

**Electrum**: Electrum is a popular Bitcoin wallet written in Python originally by Thomas Voegtlin. It features a Lightning Network node implementation. ([source](../../raw/docs/community-resources/glossary.md))

**Eltoo**: Eltoo (from L2) is a proposed upgrade to the Lightning Network, enabling new functionalities. ([source](../../raw/docs/community-resources/glossary.md))

**Explorer**: An explorer is software or a service that lets you inspect transactions, nodes, and network metrics. There are explorers focusing mainly on on-chain data as well as Lightning Network explorers. ([source](../../raw/docs/community-resources/glossary.md))

**Faraday**: Faraday is analytics software developed by Lightning Labs that can help identify liquidity needs and profitable channels in a Lightning node. See [[faraday]]. ([source](../../raw/docs/community-resources/glossary.md))

**Fee**: Fees might occur as part of on-chain fees, which are paid to miners, or off-chain fees, which are paid to peers in the part of base fees and the fee rate. See [[channel-fees]]. ([source](../../raw/docs/community-resources/glossary.md))

**Fee rate**: The fee rate is part of the fee that each forwarded payment is charged by a node. The fee rate is measured in parts per million (ppm) of the forwarded payment, unlike the base fee. See [[channel-fees]]. ([source](../../raw/docs/community-resources/glossary.md))

**Force close**: When a channel peer is unreachable, or when there is a fundamental disagreement over the state of a channel, the channel needs to be force closed by either party. A force close broadcasts the commitment transaction. ([source](../../raw/docs/community-resources/glossary.md))

**Fuzzing**: Fuzz testing is the methodology of feeding invalid data to software with the intention of finding bugs and vulnerabilities. ([source](../../raw/docs/community-resources/glossary.md))

**Gossip network**: The Lightning gossip network is used to broadcast information about channels and peers. See [[gossip-network]]. ([source](../../raw/docs/community-resources/glossary.md))

**Graph**: The Lightning Network graph contains information about all peers and their public channels, including fees and channel points. See [[pathfinding]]. ([source](../../raw/docs/community-resources/glossary.md))

**gRPC**: gRPC is a Remote Procedure Call tool developed by Google, used in LND for remote calls. ([source](../../raw/docs/community-resources/glossary.md))

**Hash Time-lock Contract**: A Hash Time-lock Contract (HTLC) is a Bitcoin transaction that either pays to a peer revealing a preimage secret or allows the sender to claim the funds back after a CSV certain period. The Lightning Network uses HTLCs to guarantee payments between peers. See [[htlc]]. ([source](../../raw/docs/community-resources/glossary.md))

**Hidden Service**: See also Onion Service. ([source](../../raw/docs/community-resources/glossary.md))

**Hodl invoice**: A hodl invoice (also: hold invoice) is a regular Lightning invoice, but the recipient will "hold" the preimage. Hodl invoices are used for refundable deposits, for example in auctions. ([source](../../raw/docs/community-resources/glossary.md))

**Inbound capacity**: Inbound capacity is the amount of satoshis a node is able to receive through a given channel or all channels together. A channel's inbound capacity and outbound capacity together define a channel's total capacity, as defined at its creation. See [[inbound-capacity]]. ([source](../../raw/docs/community-resources/glossary.md))

**Invoice**: To receive Lightning payments, the recipient typically issues an invoice containing information such as public key, payment hash or an invoice amount and label. Invoices are defined in BOLT 11. See [[lightning-invoices]]. ([source](../../raw/docs/community-resources/glossary.md))

**Keysend**: Keysend allows users of the Lightning Network to send funds to a node's public key. ([source](../../raw/docs/community-resources/glossary.md))

**Leaf**: A leaf is the part of a Merkle tree that carries the data that the tree attests to. ([source](../../raw/docs/community-resources/glossary.md))

**Lightning Labs**: A private company helping to maintain LND. Lightning Labs also develops tools like Lightning Loop, Pool, Faraday, Lightning Terminal, and more. ([source](../../raw/docs/community-resources/glossary.md))

**Lightning Network**: The Lightning Network is a payment network built on top of Bitcoin. It uses Lightning Channels to route payments secured by HTLCs backed on the Bitcoin Blockchain. See [[lightning-network-overview]]. ([source](../../raw/docs/community-resources/glossary.md))

**Lightning Network node**: A Lightning Network node is software that allows you to join the Lightning Network, make, receive and route payments. The full specification of a Lightning Node is laid out in BOLT. ([source](../../raw/docs/community-resources/glossary.md))

**Lightning Node Connect**: Lightning Node Connect (LNC) is a protocol to connect remotely to your Lightning node through a proxy. See [[lightning-node-connect]]. ([source](../../raw/docs/community-resources/glossary.md))

**The Lightning Network Daemon**: The Lightning Network Daemon (LND) is a popular implementation of the Lightning Network written in Go and developed by Lightning Labs. See [[lnd]]. ([source](../../raw/docs/community-resources/glossary.md))

**Lightning Service Provider**: A Lightning Service Provider (LSP) provides commercial liquidity and routing services on the Lightning Network. For example, a LSP might provide funds for automatic channel opening, inbound liquidity or routing information. See [[lightning-service-providers]]. ([source](../../raw/docs/community-resources/glossary.md))

**Lightning Terminal**: A web-based graphical interface and utility tool for Lightning nodes. Runs litd and uses Lightning Node Connect. See [[lightning-terminal]]. ([source](../../raw/docs/community-resources/glossary.md))

**Liquidity management**: Liquidity management is the process of allocating funds to where they are needed or most productive. Liquidity management includes opening and closing channels, circular rebalances as well as transactions on Lightning Loop and Pool. See [[liquidity]]. ([source](../../raw/docs/community-resources/glossary.md))

**litd**: The Lightning Terminal Daemon (litd) bundles Lightning Loop, Lightning Pool and Faraday in a UI. It is run locally and allows for remote access to Lightning Terminal via Lightning Node Connect. See [[lightning-terminal]]. ([source](../../raw/docs/community-resources/glossary.md))

**LNCLI**: The Lightning Node Command Line Interface (LNCLI) is part of the Lightning Network Daemon (LND). It is used to maintain a Lightning Node with RPC calls. ([source](../../raw/docs/community-resources/glossary.md))

**LNURL**: A Lightning Node URL is a URL encoded in bech32 with the prefix `lnurl`. It is commonly used to make payments, withdrawals and even authentication. ([source](../../raw/docs/community-resources/glossary.md))

**Loop**: Loop is a non-custodial service by Lightning Labs to perform Submarine Swaps between on-chain and off-chain bitcoin. See [[loop]]. ([source](../../raw/docs/community-resources/glossary.md))

**Loop In**: Loop In is the process of sending on-chain bitcoin and receiving the equivalent (minus fees) in your Lightning channel using Lightning Loop. See [[using-loop]]. ([source](../../raw/docs/community-resources/glossary.md))

**Loop Out**: Loop Out is the process of making a Lightning payment and receiving an equivalent amount (minus fees) in your on-chain Bitcoin wallet using Lightning Loop. See [[using-loop]]. ([source](../../raw/docs/community-resources/glossary.md))

**L402**: The L402 protocol combines Macaroons with preimages as proof of payment to create tickets for paid APIs or other services that require authentication and payment. It is named after the HTTP 402 error code. See [[l402]]. ([source](../../raw/docs/community-resources/glossary.md))

**Macaroon**: Macaroons are bearer credentials that allow for detailed attenuation as well as delegation. See [[macaroons]]. ([source](../../raw/docs/community-resources/glossary.md))

**Merkle Sum Tree**: A Merkle Sum tree is a type of Merkle tree in which each node not only carries the hash of the nodes or leaves underneath, but also the sum of their values. In such a tree, the Merkle tree root will carry the total sum of all values in the Merkle tree. ([source](../../raw/docs/community-resources/glossary.md))

**Merkle tree**: A Merkle tree is a data structure that commits to multiple sets of data using a single identifying hash, the Merkle tree root. The data that the tree commits to lies at the leaves. Two leaves are hashed into a node, two nodes are hashed into a higher level node. The top node makes up the root. ([source](../../raw/docs/community-resources/glossary.md))

**Merkle tree node**: A Merkle tree node is a hash of either two leaves, or two nodes of a lower level. ([source](../../raw/docs/community-resources/glossary.md))

**Merkle tree root**: The Merkle tree root is a single hash that identifies all data in a Merkle tree. If a single bit in the tree changes, the root changes too. ([source](../../raw/docs/community-resources/glossary.md))

**Millibitcoin**: A millibitcoin is a thousandth of a bitcoin, or 0.001 BTC. ([source](../../raw/docs/community-resources/glossary.md))

**Millisatoshi**: A millisatoshi is a thousandth of a satoshi, or a 100 billionth of a bitcoin. ([source](../../raw/docs/community-resources/glossary.md))

**Multi-path Payments**: A Multi-path Payment is a Lightning payment that reaches its destination through multiple routes in parallel. MPP and AMP are both an implementation of this idea. See [[multipath-payments]]. ([source](../../raw/docs/community-resources/glossary.md))

**Multisignature address**: A multisignature bitcoin address is an address from which bitcoin can only be spent with multiple signatures. A multisignature address can be m of n, meaning that n keys exist, and m signatures need to be present. Lightning channels use 2-of-2 multisignature accounts. ([source](../../raw/docs/community-resources/glossary.md))

**NAT**: Network Address Translation is used to operate multiple networked devices behind a single IP address, for instance at home behind a router. NAT can pose a challenge to running Lightning nodes at home, requiring instead tools such as Tor and LNC. ([source](../../raw/docs/community-resources/glossary.md))

**Neutrino**: Neutrino is a technology that allows a LND node to use a remote Bitcoin node as a back end, making it possible to run a Lightning node on a low-powered device such as a phone. See also BIP 157. ([source](../../raw/docs/community-resources/glossary.md))

**Noise**: Noise is the encryption protocol used to establish and authenticate communications between Lightning nodes. ([source](../../raw/docs/community-resources/glossary.md))

**np2wkh**: A 'nested pay to witness key hash' is a segwit address encoded similarly to a legacy address in Base58. They begin with '3'. ([source](../../raw/docs/community-resources/glossary.md))

**Off-chain**: Off-chain is any transfer or action taken on the Lightning Network. Such transactions are not settled directly on the Bitcoin blockchain. ([source](../../raw/docs/community-resources/glossary.md))

**On-chain**: On-chain transactions and actions are those settled directly on the Bitcoin blockchain, for instance a traditional Bitcoin transaction made to a Bitcoin address. ([source](../../raw/docs/community-resources/glossary.md))

**Onion address**: An onion address is an identifier, similar to a url, pointing to a onion service. It usually comes in the form of a long, all-lowercase string ending in .onion. ([source](../../raw/docs/community-resources/glossary.md))

**Onion routing**: Onion routing describes the methodology of encrypting messages inside of encrypted messages, which are passed from hop to hop. Each hop is only able to decipher messages intended for itself, not any predecessor or successor. Onion routing is used to transfer data in the Tor Network as well as to pass on payments and messages in the Lightning Network using Sphinx. ([source](../../raw/docs/community-resources/glossary.md))

**Onion Service**: An Onion Service is a HTTP endpoint available only through the Tor Network. Lightning Nodes often use Onion Services to hide their location or make themselves available behind a NAT. Onion Services typically end in .onion. ([source](../../raw/docs/community-resources/glossary.md))

**Outbound capacity**: Outbound capacity describes the amount of satoshi a node is able to send through a single channel, or all channels together. See [[liquidity]]. ([source](../../raw/docs/community-resources/glossary.md))

**Output ID**: See Transaction ID. ([source](../../raw/docs/community-resources/glossary.md))

**p2wkh**: Pay to witness key hash is a Bitcoin address format. They are encoded with Bech32, start with bc1q and are also referred to as "native segwit" addresses. ([source](../../raw/docs/community-resources/glossary.md))

**Pairing phrase**: A pairing phrase looks similar to a seed phrase and is used in Lightning Node Connect to authenticate and secure a remote connection. ([source](../../raw/docs/community-resources/glossary.md))

**Partially Signed Bitcoin Transactions**: Partially signed Bitcoin transactions (PSBT) are a standard on how to pass incomplete, or partially signed transactions between wallets. This can be useful for multi-signature wallets and complex scripts and is used in LND to handle watch-only wallets. ([source](../../raw/docs/community-resources/glossary.md))

**Passive assets**: Passive assets describes the Taproot Assets which are retained by the user when other assets are being sent from their asset tree. The "passive" assets are those which the sender retains custody. While "active" assets are those actively being sent to a new user, or those being recustodied. ([source](../../raw/docs/community-resources/glossary.md))

**Pathfinding**: The process of finding a route for a payment. This is typically done by the payer, who might have to compute and try multiple routes before the payment succeeds. See [[pathfinding]]. ([source](../../raw/docs/community-resources/glossary.md))

**Payment channel**: Payments channels are 2-of-2 multisignature accounts held cooperatively by two peers, secured by commitment transactions. Payment channels make up the Lightning Network. See [[payment-channels]]. ([source](../../raw/docs/community-resources/glossary.md))

**Payment hash**: A payment hash is the hash of the preimage. A Lightning payment is made to this hash and can be claimed once the preimage is revealed. ([source](../../raw/docs/community-resources/glossary.md))

**Peer**: In the Lightning Network, a peer is another node you connect to, possibly open a channel and routing payments through them. Anyone can start a node and become a peer, making Lightning a peer-to-peer network. See [[routing-nodes]]. ([source](../../raw/docs/community-resources/glossary.md))

**Peer-to-peer**: A peer-to-peer network is any system not relying on a leader, in which connections are made directly between peers without intermediaries. ([source](../../raw/docs/community-resources/glossary.md))

**Polar**: Polar makes it easy to locally simulate the Lightning Network for testing purposes. Developed by Jamal James. ([source](../../raw/docs/community-resources/glossary.md))

**Pool**: Lightning Pool is a marketplace for channel liquidity run by Lightning Labs. Through auctions, participants can signal a need for liquidity or offer to open channels to others for a fee. See [[pool]]. ([source](../../raw/docs/community-resources/glossary.md))

**Preimage**: A preimage is a random number generated by the payee, hashed and passed to the payer as part of the invoice. The preimage is revealed upon successful receipt of the payment, allowing each participant along the route to claim their funds as part of the HTLCs. ([source](../../raw/docs/community-resources/glossary.md))

**Private Channel**: A private channel is a channel that is not announced to the network. As such it cannot be used for routing, and when receiving payments through a private channel its information needs to be included in the invoice. ([source](../../raw/docs/community-resources/glossary.md))

**Probing**: Probing is the act of attempting payments through the Lightning Network without settling them in an attempt to discover routes or reveal channel capacity. ([source](../../raw/docs/community-resources/glossary.md))

**PTLC**: Point Time-locked Contracts (PTLCs) are a proposed improvement on HTLCs. It uses homomorphic one-way functions instead of hashes. When using PTLCs, there is no single preimage across a payment route, but instead each hop calculates its own secret. Using unique secrets per hop reduces the ability of an intermediary to trace the route a payment takes in the Lightning Network. ([source](../../raw/docs/community-resources/glossary.md))

**Public key**: In cryptography, a public key can be used to verify signed data, as well as encrypt data for a recipient. In the Lightning Network each node is identified by its public key. This key is used to handle Onion routing, keysend messages, peer-to-peer communications and other data. ([source](../../raw/docs/community-resources/glossary.md))

**RBF**: Replace by Fee is a mechanism that allows the sender of an unconfirmed on-chain Bitcoin transaction to replace the transaction with a higher fee transaction in the hope of getting it included into a block sooner. ([source](../../raw/docs/community-resources/glossary.md))

**REST**: "Representational State Transfer" or REST is a software architecture style developed for the world wide web. LND offers a RESTful API, which follows the constraints set out in that standard. ([source](../../raw/docs/community-resources/glossary.md))

**RevokeAndAck**: RevokeAndAck is the process of revoking a previous commitment transaction and acknowledging a new state in a channel. It's a fundamental piece of how payments are forwarded and canceled in the Lightning Network. ([source](../../raw/docs/community-resources/glossary.md))

**Route**: The path a Lightning payment is taking from payer to payee. In the Lightning Network, the payer chooses the route, encrypts it and passes the payment on to the first peer, who passes it onto the next peer. ([source](../../raw/docs/community-resources/glossary.md))

**RPC**: Remote Procedure Calls are a popular way of interfacing with LND. Specifically, LND supports the gRPC interface. ([source](../../raw/docs/community-resources/glossary.md))

**Satoshi**: A satoshi is 1/100 millionth of a Bitcoin. In the Lightning Network a satoshi is further divisible into 1000 pieces (millisatoshi). It is named after Bitcoin's creator, Satoshi Nakamoto. ([source](../../raw/docs/community-resources/glossary.md))

**Satoshi Nakamoto**: Satoshi Nakamoto is the pseudonym behind the creator(s) of Bitcoin. ([source](../../raw/docs/community-resources/glossary.md))

**SCB**: Static channel backups (SCB) contain information about each channel peer and how to reach them. They are encrypted with a node's public key and can be used to request a remote force closure of a channel in the event of a catastrophic failure. ([source](../../raw/docs/community-resources/glossary.md))

**Seed phrase**: A seed phrase is a collection of typically 12 to 24 words from which cryptographic keys are derived. This makes it possible to back up a series of private keys, for instance for multiple bitcoin addresses in a wallet with a single piece of static information. LND uses aezeed to derive private keys from a seed phrase. ([source](../../raw/docs/community-resources/glossary.md))

**Shard**: A shard is a splinter of glass. In the context of the Lightning Network, a shard is a part of a Multi-path payment, such as MPP or AMP. ([source](../../raw/docs/community-resources/glossary.md))

**Sidecar channel**: A sidecar channel refers to a channel purchased on Lightning Pool for a third party. Sidecar channels allow an auction participant to buy channels for others, for example mobile wallets that are not participating in the auction process directly. See [[sidecar-channels]]. ([source](../../raw/docs/community-resources/glossary.md))

**Sidecar ticket**: A sidecar ticket allows the recipient of a Sidecar channel purchased on Pool to redeem the channel. The seller will then open the channel to the ticket holder. ([source](../../raw/docs/community-resources/glossary.md))

**Sparse Merkle Sum Tree**: A Sparse Merkle Sum tree (SMST) combines the properties of a Sparse Merkle tree and a Merkle Sum tree. ([source](../../raw/docs/community-resources/glossary.md))

**Sparse Merkle Tree**: A Sparse Merkle Tree (SMT) is a data structure that, in addition to a normal Merkle-tree's ability to produce inclusion proofs, is able to provide non-inclusion proofs. This is achieved by placing an object at a leaf location defined by the binary expression of the SHA256 digest of that data. Each bit, of the digest, expresses the left-right traversal in a binary tree to locate the object. When the contents of many of the leaves are empty, many of the branches are null, leading to efficient computation during SMT generation and modification. ([source](../../raw/docs/community-resources/glossary.md))

**Sphinx**: Sphinx is the name of the protocol by which the Lightning Network implements onion routing. ([source](../../raw/docs/community-resources/glossary.md))

**Submarine swap**: A submarine swap is a type of atomic swap in which on-chain bitcoin are swapped for off-chain bitcoin without either party assuming custody of the other's funds. See [[submarine-swaps]]. ([source](../../raw/docs/community-resources/glossary.md))

**Sweep**: Funds held in some types of addresses have to be sweeped, meaning they have to be spent as soon as possible and sent to the user's main wallet. Mainly, this is done because they might otherwise not be recoverable in the event of data loss. See [[sweeping]]. ([source](../../raw/docs/community-resources/glossary.md))

**Taproot**: Taproot is a bitcoin transaction type introduced in November 2021 that allows for more advanced scripts, with major efficiency improvements relevant for the Lightning Network. ([source](../../raw/docs/community-resources/glossary.md))

**Taproot Assets**: Taproot Assets is a protocol for issuing assets on Bitcoin. It uses Merkle Sum trees and Sparse Merkle trees to commit assets to the Bitcoin Blockchain. Assets can be committed to Lightning channels to instant transfers. See [[taproot-assets-protocol]]. ([source](../../raw/docs/community-resources/glossary.md))

**Time Lock Delta**: Time lock deltas such as CSV and CLTV are used in the Lightning Network to lock funds for a period of time, for example for arbitration purposes. ([source](../../raw/docs/community-resources/glossary.md))

**Tor**: The Onion Router (Tor) is a public relay network primarily built to hide the origin and destination of packets on the internet. It is popular among Lightning Node operators to make their nodes accessible through Tor to avoid NAT barriers. ([source](../../raw/docs/community-resources/glossary.md))

**Transaction ID**: The transaction ID (txid) is the hash of a bitcoin transaction. Channels are identified by the transaction id of their funding transaction, see channel point. ([source](../../raw/docs/community-resources/glossary.md))

**Turbo channel**: A Turbo channel is a channel accepted as valid with zero confirmations on the Bitcoin blockchain. It requires some trust in the initiator. ([source](../../raw/docs/community-resources/glossary.md))

**Tweak**: In the context of Taproot, to tweak refers to the possibility of adding any data to the public key, in a way that anyone with the public key is able to verify the existence of this data. This is useful when committing to data, such as a Merkle tree root. ([source](../../raw/docs/community-resources/glossary.md))

**Unique assets**: A unique asset is an asset that is not divisible, and cannot be exchanged for another asset of the same kind. This is contrary to fungible assets, such as money. ([source](../../raw/docs/community-resources/glossary.md))

**Universe**: A universe is a repository for Taro assets. It serves information such as metadata and proofs to prospective and existing users and holders of such assets. See [[taproot-assets-protocol]]. ([source](../../raw/docs/community-resources/glossary.md))

**Unspent Transaction Outputs**: Unspent transaction outputs (unspent utxos) are funds available on-chain, for example to make on-chain payments or to open Lightning channels. ([source](../../raw/docs/community-resources/glossary.md))

**Watch-only wallet**: A wallet that is aware of balances and transactions, but does not possess the keys necessary to spend them. A watch-only wallet can create unsigned PSBTs which are then signed by the wallet holding the keys. ([source](../../raw/docs/community-resources/glossary.md))

**Watchtower**: A watchtower consists of a client and a server. The client will share information relevant to channel breaches with the server, which will intervene in case they observe a breach on-chain. Watchtowers are needed in case the client is offline and unable to observe the breach themselves. See [[watchtowers]]. ([source](../../raw/docs/community-resources/glossary.md))

**Wumbo channel**: In the early days of the Lightning Network, most clients would not allow opening channels larger than 16,777,215 (2^24 -1). Today, channels exceeding this limit are called Wumbo channels. ([source](../../raw/docs/community-resources/glossary.md))

**Zero-confirmation channel**: See also Turbo channel. ([source](../../raw/docs/community-resources/glossary.md))

**ZMQ**: ZeroMQ is a messaging library used by Bitcoin Core to inform other software, for example LND of new blocks and transactions. ([source](../../raw/docs/community-resources/glossary.md))

**Zombie channel**: A zombie channel is a channel that still exists on-chain and in the graph, but hasn't been active in a while and is unlikely to become active again. It is recommended to close such channels. See [[liquidity]]. ([source](../../raw/docs/community-resources/glossary.md))

## Taproot Assets terms

**Anchor**: The anchor transaction is the Bitcoin transaction that mints or transfers a Taproot Asset. ([source](../../raw/docs/the-lightning-network/taproot-assets/glossary.md))

**Asset group**: An asset group describes a series of assets, as identified by their asset ID, for which new assets can be added by the issuer. ([source](../../raw/docs/the-lightning-network/taproot-assets/glossary.md))

**Asset ID**: The asset ID is used to identify an asset. It is the hash of the genesis outpoint, the asset tag and the asset meta data. It is a globally unique identifier. If an asset is grouped, each minted series contains its own asset ID. See [[taproot-assets-protocol]]. ([source](../../raw/docs/the-lightning-network/taproot-assets/glossary.md))

**Asset tag**: The asset tag is equivalent to the name of an asset. Other information is collected as part of the meta data. ([source](../../raw/docs/the-lightning-network/taproot-assets/glossary.md))

**Batch**: A batch is a set of Taproot Asset mints or transfers that are contained in a single Bitcoin-level UTXO. ([source](../../raw/docs/the-lightning-network/taproot-assets/glossary.md))

**Burn**: Burning an asset means irrevocably removing it from the circulating supply. See [[taproot-assets-protocol]]. ([source](../../raw/docs/the-lightning-network/taproot-assets/glossary.md))

**Collectibles**: A collectible, unique or non-fungible asset, unlike a normal asset, cannot be divided or aggregated, as there are no other units of its kind. It can however be put into a collection with other similar collectibles. ([source](../../raw/docs/the-lightning-network/taproot-assets/glossary.md))

**Collections**: A collection is a group of collectibles. While every item in the collection is unique, they can still be identified as part of the same collection using the group key. ([source](../../raw/docs/the-lightning-network/taproot-assets/glossary.md))

**Commitment**: A commitment is typically the hash of data that is to be permanently recorded to have existed at a certain point in time, and in a certain utxo. ([source](../../raw/docs/the-lightning-network/taproot-assets/glossary.md))

**Fungible tokens**: See also normal assets. ([source](../../raw/docs/the-lightning-network/taproot-assets/glossary.md))

**Genesis point**: The genesis point is the first input of the transaction that mints a Taproot Asset. ([source](../../raw/docs/the-lightning-network/taproot-assets/glossary.md))

**Group key**: The group key identifies normal and collectible assets that do not have a fixed supply. When new assets of this group are minted, a signature using this key must be present. ([source](../../raw/docs/the-lightning-network/taproot-assets/glossary.md))

**Internal key**: The internal key is the key that is able to spend the Taproot Bitcoin UTXO. ([source](../../raw/docs/the-lightning-network/taproot-assets/glossary.md))

**Issuer**: The issuer of an asset is whoever creates and publishes the mint transaction. The issuer of a grouped asset is identified using the group key. ([source](../../raw/docs/the-lightning-network/taproot-assets/glossary.md))

**Leaf**: A leaf is the lowest level in a Merkle tree. They typically contain the data that the Merkle tree commits to. ([source](../../raw/docs/the-lightning-network/taproot-assets/glossary.md))

**Lightning Polar**: Lightning Polar is software that helps you simulate a regtest Lightning environment in which you can easily add multiple nodes. It can also be used to test Taproot Assets mints and transactions. ([source](../../raw/docs/the-lightning-network/taproot-assets/glossary.md))

**Merkle root**: The Merkle root is the hash at the very top of the Merkle tree. If a single value in the Merkle tree changes, the root also changes. ([source](../../raw/docs/the-lightning-network/taproot-assets/glossary.md))

**Merkle sum tree**: A merkle sum tree is a Merkle tree that for each leaf contains a numerical value, which is sumed up in each node. The sum at the Merkle root is equal to the sum of values at the leafs. ([source](../../raw/docs/the-lightning-network/taproot-assets/glossary.md))

**Merkle tree**: In a merkle tree a pair of items is hashed, the pair then hashed with other pairs until only a single hash is left, the Merkle root. This helps to cheaply commit to large amounts of arbitrary data and check whether anything has changed. ([source](../../raw/docs/the-lightning-network/taproot-assets/glossary.md))

**Meta data**: The asset meta data can be used to commit to any arbitrary data. Most commonly it describes the asset and its terms or represents the asset itself. ([source](../../raw/docs/the-lightning-network/taproot-assets/glossary.md))

**Mint**: The action of issuing an asset. Also see issuer. ([source](../../raw/docs/the-lightning-network/taproot-assets/glossary.md))

**Non-fungible token**: Also see collectibles. ([source](../../raw/docs/the-lightning-network/taproot-assets/glossary.md))

**Normal asset**: A normal or fungible asset is one that is divisible into a predefined set of units. Each unit is expected to be valued the same as any other unit of the same asset. Normal assets can be fixed in total supply, or be part of an asset group. ([source](../../raw/docs/the-lightning-network/taproot-assets/glossary.md))

**Proof file**: The proof file contains information about the asset, when and how it was minted as well as previous transfers. it is needed to verify ownership over an asset. ([source](../../raw/docs/the-lightning-network/taproot-assets/glossary.md))

**PSBT**: A partially signed Bitcoin transaction is a file format that lets two wallets communicate only specific details about a new transaction, for example only its inputs, or only its outputs. These PSBTs can be used to sign transactions with external signing devices, or allow multiple parties to contribute inputs to one transaction. ([source](../../raw/docs/the-lightning-network/taproot-assets/glossary.md))

**Sparse merkle tree**: A sparse merkle tree is a merkle tree over all numbers of a given space. A sparse merkle tree over 2^256 for example theoretically contains 2^256 leafs. It can be computed because by default all leafs are empty. Sparse merkle trees help with exclusion proofs, e.g. proving something is not present in a merkle tree. See [[taproot-assets-protocol]]. ([source](../../raw/docs/the-lightning-network/taproot-assets/glossary.md))

**Supply**: The supply of an asset is the total amount of units of that asset in circulation. For grouped assets, this supply can be increased later. For all assets, it can be reduced by burning a portion of the supply. ([source](../../raw/docs/the-lightning-network/taproot-assets/glossary.md))

**Tapd**: Taproot Assets Protocol Daemon is the reference implementation for Taproot Assets. See [[taproot-assets]]. ([source](../../raw/docs/the-lightning-network/taproot-assets/glossary.md))

**Taproot**: Taproot is a Bitcoin transaction type. Bitcoin sent to taproot scripts can be unlocked either using the internal key or a predefined set of conditions, the tapscript. ([source](../../raw/docs/the-lightning-network/taproot-assets/glossary.md))

**Taproot Asset address**: A Taproot Assets address is created by the recipient of an asset to be able to receive an asset. Such addresses are specific to an asset and an amount and should not be reused. See [[taproot-assets-protocol]]. ([source](../../raw/docs/the-lightning-network/taproot-assets/glossary.md))

**Taproot Assets**: Taproot Assets leverages Taproot transactions to commit to newly created assets and their transfers in an efficient and scalable manner. See [[taproot-assets-protocol]]. ([source](../../raw/docs/the-lightning-network/taproot-assets/glossary.md))

**Taproot Assets Channel**: Taproot Assets can be deposited into Lightning channels. These channels are referred to as Taproot Asset Channels. See [[taproot-assets-on-lightning]]. ([source](../../raw/docs/the-lightning-network/taproot-assets/glossary.md))

**Tapscript**: Tapscript is a feature of Taproot transactions that allows to create various conditional spending conditions. Taproot Assets and their merkle trees are stored in the Tapscript. ([source](../../raw/docs/the-lightning-network/taproot-assets/glossary.md))

**Tapscript sibling**: The Tapscript sibling is the hash in the leaf next to the data in question. The sibling is needed to compute the Merkle root. ([source](../../raw/docs/the-lightning-network/taproot-assets/glossary.md))

**Unique asset**: See also Collectibles. ([source](../../raw/docs/the-lightning-network/taproot-assets/glossary.md))

**Universe**: A universe is a server that serves information about assets and their transfers. Universes can also be used to transfer proof files between users. See [[taproot-assets-protocol]]. ([source](../../raw/docs/the-lightning-network/taproot-assets/glossary.md))

**vPSBT**: Virtual partially signed Bitcoin transactions achieve what PSBTs achieve, but on the Taproot Assets layer. Using vPSBTs, it becomes easier to batch Taproot Asset transactions, use external signing devices or assemble transactions between the Taproot asset and Bitcoin layer. ([source](../../raw/docs/the-lightning-network/taproot-assets/glossary.md))

**vUTXO**: A vUTXO is a Taproot Assets utxo. As the Taproot Assets themselves are not perfectly synonymous with the Bitcoin UTXO that they are anchored in, vUTXOs are used to reference them. ([source](../../raw/docs/the-lightning-network/taproot-assets/glossary.md))
