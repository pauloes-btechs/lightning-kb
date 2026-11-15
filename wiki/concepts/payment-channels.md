---
title: Payment channels and their lifecycle
type: concept
sources:
  - raw/docs/the-lightning-network/payment-channels.md
  - raw/docs/the-lightning-network/payment-channels/lifecycle-of-a-payment-channel.md
  - raw/docs/the-lightning-network/payment-channels/etymology.md
updated: 2026-11-14
---

# Payment channels and their lifecycle

Payment channels are multisignature contracts between peers. Payments are made inside these payment channels and can be settled on the Blockchain. The Lightning Network is made up of payment channels; each channel represents an UTXO on the Bitcoin Blockchain and is cooperatively controlled by two peers, who can transact through that channel as frequently as they want. ([source](../../raw/docs/the-lightning-network/payment-channels.md))

At its core, a payment channel is a 2-of-2 multisignature contract between two parties holding bitcoin. From the perspective of the Blockchain the bitcoin is held cooperatively by the two parties, but each party owns a portion of it and maintains a record of this ownership locally. The guide's example: a payment channel of over 1 million satoshis can represent 100,000 satoshis in the hands of Alice and 900,000 satoshis in the hands of Bob, and the two can update their balances as frequently as they like without an on-chain Bitcoin transaction or costs beyond the electricity and bandwidth they consume. ([source](../../raw/docs/the-lightning-network/payment-channels/lifecycle-of-a-payment-channel.md))

So that Alice and Bob do not have to trust each other, each payment channel is secured by a commitment transaction signed by both, which allows each of them to unilaterally exit the agreement at any time, spending their respective share of the funds back to their own wallet. Such an event is called a "force close". ([source](../../raw/docs/the-lightning-network/payment-channels/lifecycle-of-a-payment-channel.md))

This page is part of [[lightning-network-overview]]. See also: [[htlc]], [[sweeping]], [[watchtowers]], [[multihop-payments]].

## Opening a channel

To open a channel to Alice, her node needs to be reachable over the internet. Alice may also place restrictions on new channels, such as a minimum channel size or gating for specific peers. ([source](../../raw/docs/the-lightning-network/payment-channels/lifecycle-of-a-payment-channel.md))

For Bob to open the channel, he needs funds in the form of bitcoin on-chain, either in his Lightning node or another wallet he controls. Upon his command, his node connects to Alice and offers a channel. Alice and Bob combine their keys to generate a 2-of-2 multisignature contract, which acts as the channel's address. ([source](../../raw/docs/the-lightning-network/payment-channels/lifecycle-of-a-payment-channel.md))

To ensure his funds are never stuck in this contract, Bob creates his funding transaction but does not broadcast it. He creates an additional transaction, the commitment transaction, that spends his funds back to him, and asks Alice to co-sign it. Then Bob may broadcast the funding transaction and keep the refund transaction in memory. Alice cannot take his funds without his cooperation, and if she becomes unresponsive he can broadcast the commitment transaction. The payment channel is now open and available for use. ([source](../../raw/docs/the-lightning-network/payment-channels/lifecycle-of-a-payment-channel.md))

## Sending funds through a channel

The latest commitment transaction always represents the channel balances between Alice and Bob. They transfer balance to each other by updating their commitment transaction, as frequently as needed, in increments of one millisatoshi. Updates can be made in both directions, and there is no upper limit to how many updates can be made inside a single payment channel. As these payments are not announced to the network and the funds never move on-chain, they are only known to each party. ([source](../../raw/docs/the-lightning-network/payment-channels/lifecycle-of-a-payment-channel.md))

At each payment, Alice and Bob invalidate each other's previous commitment transaction, ensuring that only the most recent transaction can be used to recover their balance in the event of a non-cooperative channel closure. ([source](../../raw/docs/the-lightning-network/payment-channels/lifecycle-of-a-payment-channel.md))

## Closing a channel

There are two ways of closing a channel: cooperatively and non-cooperatively. ([source](../../raw/docs/the-lightning-network/payment-channels/lifecycle-of-a-payment-channel.md))

**Cooperatively.** Both Alice and Bob are online, agree on their balance and on the terms of a channel closure (e.g. fees) proposed by either party. They both sign a new transaction that spends the funds back to their respective wallets immediately and no longer process transactions between them. As soon as the closure transaction is confirmed on the blockchain, they can use the funds to open new channels, move them elsewhere or leave them in their wallet. Cooperative channel closures are the norm in the Lightning Network. ([source](../../raw/docs/the-lightning-network/payment-channels/lifecycle-of-a-payment-channel.md))

**Non-cooperatively.** Either party may not be available, or may be unable or unwilling to sign the closure transaction. The party aiming to close the channel then has to publish their commitment transaction, which results in a non-cooperative close, also called a force close. ([source](../../raw/docs/the-lightning-network/payment-channels/lifecycle-of-a-payment-channel.md))

Commitment transactions are asymmetrical: they spend the balance of the peer initiating the force close to an arbitration contract, while the funds of the other party are sent to their wallet immediately. This allows the peer that is not initiating the force closure to contest it. ([source](../../raw/docs/the-lightning-network/payment-channels/lifecycle-of-a-payment-channel.md))

If one party attempts to "cheat" by publishing an older commitment transaction, their peer is able to use the previously exchanged revocation secret to claim the funds of the malicious actor. See [[watchtowers]] and [[sweeping]]. ([source](../../raw/docs/the-lightning-network/payment-channels/lifecycle-of-a-payment-channel.md))

## Channel terms (etymology)

All channels share the same core characteristics, but there may be subtle differences in how channels are created, announced, treated or closed. ([source](../../raw/docs/the-lightning-network/payment-channels/etymology.md))

**Payment channel.** A 2-of-2 multisignature account with a balance on the bitcoin blockchain. This balance is held cumulatively by both parties, making up the capacity of the channel. The channel also has two internal balances, known only to the two signatories. The internal balance can be settled on the blockchain either cooperatively, by both signatories signing a closing transaction, or unilaterally, by broadcasting a pre-negotiated force close transaction. ([source](../../raw/docs/the-lightning-network/payment-channels/etymology.md))

**Anchor channel.** An optional feature (feature bits `20`, `21`, `22` & `23`) for Lightning nodes such as LND. When an anchor channel is unilaterally closed, the fees of the closure transaction can be increased according to market requirements by joining an extra UTXO. When enabling anchor channels in LND, it is required to keep at least 10k satoshis per channel, with a maximum of 100k satoshis, in the on-chain wallet. ([source](../../raw/docs/the-lightning-network/payment-channels/etymology.md))

**Channel capacity.** A channel's total capacity is the amount of bitcoin you can send through it at once. Inbound capacity is the amount you can receive from your peer, limited by that party's local or outbound capacity. Outbound capacity is how many satoshis you can send through that channel to your peer. Inbound and outbound capacity add up to the channel's total capacity, as defined by the channel creation. See [[liquidity]] and [[inbound-capacity]]. ([source](../../raw/docs/the-lightning-network/payment-channels/etymology.md))

**Channel factories.** A proposed mechanism to open multiple channels with a single UTXO. Instead of 2-of-2 multisignature addresses, a number of users maintain a single UTXO through a n-of-n multisignature account, from which they can open and close channels with each other without additional transactions. They would need an on-chain transaction only to remove their capital from the channel factory. ([source](../../raw/docs/the-lightning-network/payment-channels/etymology.md))

**Commitment fee.** A commitment transaction needs to include an adequate network fee to ensure it gets confirmed when the channel is unilaterally closed. This fee is typically paid by the initiator of the transaction. Anchor channels allow this fee to be very small, as it can be increased later using additional UTXOs. ([source](../../raw/docs/the-lightning-network/payment-channels/etymology.md))

**Commitment transaction.** A regular Bitcoin transaction that spends the funds in a channel to its peers, ensuring that either party can redeem their funds even if the other party is no longer responsive or cooperative. It is created before a channel is funded, as part of the channel opening negotiation. Every time a payment is made inside the channel, a new commitment transaction is created and its predecessor invalidated. ([source](../../raw/docs/the-lightning-network/payment-channels/etymology.md))

**Force close.** A unilateral close in which one participant closes a channel without the cooperation of the other, performed by broadcasting a "commitment transaction", a transaction that commits to a previous channel state that the participants have agreed upon. ([source](../../raw/docs/the-lightning-network/payment-channels/etymology.md))

**Hosted channel (custodial channel, virtual channel).** A channel that has not been committed on the blockchain. Its funds are not secured by the blockchain but held in custody by a third party. Creating or closing these channels does not carry a cost, but requires trust in the host not to misappropriate the funds. Depending on the implementation, a hosted channel can be converted into a regular channel or UTXO if the custodian is not responsive. ([source](../../raw/docs/the-lightning-network/payment-channels/etymology.md))

**Inbound/outbound channel.** The term inbound channel refers to inbound and outbound liquidity, although in some contexts it might refer to a channel opened by another node to you, as opposed to a channel opened by you. Which side opens a channel carries little significance in the Lightning Network and is unobservable for a third party. ([source](../../raw/docs/the-lightning-network/payment-channels/etymology.md))

**Private channel.** A channel that is not announced to the Lightning Network and so is not included in the network graph. The source says a private channel therefore cannot be used for routing payments and should be the default channel type for all nodes that are not configured for routing payments, such as mobile wallets or wallets primarily used for personal spending and receiving. To receive payments into a private channel, the channel's existence and policies are revealed to the payer through routing hints embedded in the invoice (see [[lightning-invoices]]). Third-party observers may have other opportunities to reveal the existence of private channels, such as on-chain heuristics and coin tracing. ([source](../../raw/docs/the-lightning-network/payment-channels/etymology.md))

**Public channel.** A channel announced together with its policies and peers to the wider network as part of the network graph (see [[gossip-network]]). ([source](../../raw/docs/the-lightning-network/payment-channels/etymology.md))

**Sidecar channels.** Lightning Pool is a marketplace for liquidity in the Lightning Network, where participants can place bids to buy and provision channels to other peers, including third parties. A sidecar channel is a channel opened by party A on behalf of party B to party C. The source says this is useful for services that want to onboard users and merchants onto the Lightning Network without providing capital themselves, and that sidecar channels may also be deployed as Turbo channels. See [[pool]] and [[sidecar-channels]]. ([source](../../raw/docs/the-lightning-network/payment-channels/etymology.md))

**Taproot channels.** Channels anchored in a Taproot output rather than a Segwit output. This allows Taproot Assets to be deposited into Lightning Network channels, and eventually becomes a prerequisite for Point Time Locked Contracts (PTLCs). Taproot channels are more private and more efficient when closed cooperatively than existing channels, but require a new gossip protocol to be announced to the graph. Unannounced ("private") Taproot channels are available in LND from version 0.17. See [[taproot-assets-on-lightning]]. ([source](../../raw/docs/the-lightning-network/payment-channels/etymology.md))

**Turbo channels (zero-conf channels).** A channel that is accepted without confirmations on the bitcoin blockchain. This requires trust in the party opening the channel not to double-spend the channel opening transaction. That trust may be gained by opening the channel from a 2-of-2 multisignature address held by the opening party and a co-signer trusted with not signing a double-spend transaction. Turbo channels are commonly used in mobile wallets and merchant services. See [[pool-zero-conf-channels]]. ([source](../../raw/docs/the-lightning-network/payment-channels/etymology.md))

**Zombie channels.** A channel that is not expected to be active again, for example because the peer has suffered a failure or is no longer active. As zombie channels bind capital and cannot be used for routing, the source says they should be closed once it becomes unlikely the channel becomes active again. See [[lnd-recovery]]. ([source](../../raw/docs/the-lightning-network/payment-channels/etymology.md))

**Wumbo channel.** In the early days of the Lightning Network, nodes accepted only channels of at most 16,777,215 (2^24 -1) satoshis, which the source gives as 0.168 BTC. Later, implementations gave users the option to accept channels of up to 10 BTC; these large channels are called Wumbo channels. ([source](../../raw/docs/the-lightning-network/payment-channels/etymology.md))
