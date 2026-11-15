---
title: Submarine swaps
type: concept
sources:
  - raw/docs/the-lightning-network/multihop-payments/understanding-submarine-swaps.md
  - raw/docs/the-lightning-network/multihop-payments/instant-submarine-swaps.md
updated: 2026-11-14
---

# Submarine swaps

A submarine swap is a trade between on-chain and off-chain digital assets, i.e. between Bitcoin held on-chain and Bitcoin on the Lightning network. Submarine swaps are a specific kind of atomic swap that can be performed without custody or counterparty risk. ([source](../../raw/docs/the-lightning-network/multihop-payments/understanding-submarine-swaps.md))

Either the two parties successfully swap their assets or the swap fails; at no point is either side able to walk away with the other party's funds. The source says that, without counterparty risk, submarine swaps can be performed without additional barriers such as background checks or contractual arrangements. ([source](../../raw/docs/the-lightning-network/multihop-payments/understanding-submarine-swaps.md))

To achieve these trustless properties, the on-chain transaction makes use of the same hash time-locked contracts (HTLC) as the Lightning Network (see [[htlc]]). Before on-chain BTC are transferred, the recipient of the Lightning transaction generates a preimage, a random 32-byte secret. This preimage is hashed and used to construct the HTLCs for both the on- and off-chain payments. ([source](../../raw/docs/the-lightning-network/multihop-payments/understanding-submarine-swaps.md))

See also: [[loop]], [[using-loop]], [[instant-loop-outs]], [[sweeping]], [[multihop-payments]], [[liquidity]], [[inbound-capacity]].

## The three steps

### 1. Generate a bitcoin smart contract

The sender of the on-chain payment knows the hash of the preimage and, after an exchange of public keys with the receiver, can generate a Bitcoin address with the following properties: for a limited time, the funds held in that contract can be swept knowing the preimage and a valid signature from the receiver; after that, they can be claimed using just the signature of the sender. ([source](../../raw/docs/the-lightning-network/multihop-payments/understanding-submarine-swaps.md))

Both the sender of the on-chain transaction and the recipient are able to generate and verify this script. The sender can then safely move BTC to this contract, knowing they will either receive satoshis off-chain or, if it fails, be able to claim their BTC back. Depending on the exact arrangement, the sender might also ask for a non-refundable Lightning payment upfront, which can be used to cover the transaction fees from entering and exiting the smart contract and to compensate for the opportunity cost of funds being locked up. ([source](../../raw/docs/the-lightning-network/multihop-payments/understanding-submarine-swaps.md))

The source gives this as an example of a typical bitcoin smart contract used in Loop:

```
OP_SIZE 32 OP_EQUAL
OP_IF
OP_HASH160 <ripemd160(swapHash)> OP_EQUALVERIFY
<receiverHtlcKey>
OP_ELSE
OP_DROP
<cltv timeout> OP_CHECKLOCKTIMEVERIFY OP_DROP
<senderHtlcKey>
OP_ENDIF
OP_CHECKSIG
```

([source](../../raw/docs/the-lightning-network/multihop-payments/understanding-submarine-swaps.md))

### 2. Generate and pay a Lightning invoice

The sender of the on-chain funds generates a Lightning Network invoice using the same preimage from the smart contract in step 1. The amount of the invoice might be equal to the BTC sent, or it might include or deduct a fee; this depends on the arrangement of the two parties and should be agreed on in advance. ([source](../../raw/docs/the-lightning-network/multihop-payments/understanding-submarine-swaps.md))

To reduce the likelihood of the transaction failing, the Lightning invoice might also be presented in advance, so that the recipient of the on-chain funds can determine whether they are capable of sending the payment, and at what cost. ([source](../../raw/docs/the-lightning-network/multihop-payments/understanding-submarine-swaps.md))

After funds have been confirmed to be settled in the smart contract, it is safe to pay the Lightning invoice. To claim this Lightning payment, the sender of the on-chain funds has to publicize the preimage, which the recipient can now use to claim the funds from the bitcoin smart contract. ([source](../../raw/docs/the-lightning-network/multihop-payments/understanding-submarine-swaps.md))

### 3. Claim bitcoin from the smart contract

The off-chain funds are now in the Lightning wallet of the sender of the on-chain payment, while the on-chain funds are still held in the smart contract. Using their signature and the preimage obtained from the Lightning payment, the recipient can claim the on-chain funds. The claim needs to be confirmed before the HTLC expires, or else there is the risk the sender can claim their funds back as well. The source says that, generally, replace-by-fee can be used to attempt to sweep the funds at a low fee in the beginning, with the fee gradually increased as the deadline gets closer. See [[sweeping]]. ([source](../../raw/docs/the-lightning-network/multihop-payments/understanding-submarine-swaps.md))

## What submarine swaps are good for

Submarine swaps make it easier to manage the liquidity of a Lightning node. The source says they might help with getting inbound liquidity or emptying out the day's earnings into cold storage, and can also be used to refill channels if their capacity is exhausted. ([source](../../raw/docs/the-lightning-network/multihop-payments/understanding-submarine-swaps.md))

Loop is described by the source as "our liquidity service that makes it easy to swap off-chain satoshis for an on-chain payment (Loop Out), or vice versa (Loop In)", useful to get inbound liquidity or to make on-chain payments from a Lightning node without closing a channel. See [[loop]] and [[using-loop]]. ([source](../../raw/docs/the-lightning-network/multihop-payments/understanding-submarine-swaps.md))

## Instant submarine swaps

Instant submarine swaps are a form of atomic swap that makes onchain funds immediately available without needing to wait for block confirmations. Traditional submarine swaps, such as those used by Loop, require the recipient of the onchain funds to wait for block confirmations before they can take control over their funds. ([source](../../raw/docs/the-lightning-network/multihop-payments/instant-submarine-swaps.md))

Instant submarine swaps are described as more chain efficient, making funds available immediately once the Lightning payment has been completed and the preimage obtained, without introducing trust into the procedure. ([source](../../raw/docs/the-lightning-network/multihop-payments/instant-submarine-swaps.md))

This is done by making a reservation ahead of time of the desired amount to be swapped. This gives the submarine swap provider more time to batch reservations and get the transaction confirmed at a lower fee. Each reservation is an output similar to an ordinary submarine HTLC. ([source](../../raw/docs/the-lightning-network/multihop-payments/instant-submarine-swaps.md))

The provider is able to retrieve their funds after a certain timeout has been reached, limiting their risk to the costs of the onchain transaction and the opportunity costs of funds locked. The user is able to retrieve their funds using the preimage, which they can obtain through an invoice created at the time of the Instant Loop Out. ([source](../../raw/docs/the-lightning-network/multihop-payments/instant-submarine-swaps.md))

To make the process more efficient, the output of the reservation can be made spendable with a two-of-two MuSig2 schnorr signature. Both the provider and the user originally hold their own unique keys. Upon successful completion of the swap, the provider can co-sign transactions initiated by the user, allowing the user to spend their funds without publicly revealing the preimage or paying more than the minimal onchain fees. See [[instant-loop-outs]]. ([source](../../raw/docs/the-lightning-network/multihop-payments/instant-submarine-swaps.md))
