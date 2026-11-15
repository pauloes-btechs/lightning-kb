---
title: Multihop payments, the payment cycle and timelocks
type: concept
sources:
  - raw/docs/the-lightning-network/multihop-payments.md
  - raw/docs/the-lightning-network/multihop-payments/the-payment-cycle.md
  - raw/docs/the-lightning-network/multihop-payments/etymology.md
  - raw/docs/the-lightning-network/multihop-payments/timelocks.md
updated: 2026-11-14
---

# Multihop payments, the payment cycle and timelocks

Individual payments are atomic, meaning they either arrive at their destination in full or they never leave the accounts of their sender. This is achieved through Hash Time-lock Contracts (HTLC), which make a payment to the recipient under the condition that the recipient produces the preimage, as identified by its hash. See [[htlc]]. ([source](../../raw/docs/the-lightning-network/multihop-payments.md))

All payments along the route are made to this hash and can only be claimed if the preimage is revealed. If the preimage is not revealed, the payment goes back to its sender. HTLCs can be settled on the blockchain, but generally are resolved between the peers whether they succeed or fail. ([source](../../raw/docs/the-lightning-network/multihop-payments.md))

See also: [[lightning-network-overview]], [[payment-channels]], [[lightning-invoices]], [[pathfinding]], [[multipath-payments]], [[routing-nodes]], [[submarine-swaps]], [[lnd-sending-payments]].

## A payment across three hops

The guide's example: Alice has a channel with Bob, who has a channel with Carol, who has a channel with Dave: `A<->B<->C<->D`. ([source](../../raw/docs/the-lightning-network/multihop-payments.md))

1. Alice notifies Dave that she wants to send him some money. To accept, Dave generates a random number `R`. He keeps `R` secret, but hashes it and gives the hash `H` to Alice.
2. Alice tells Bob: "I will pay you if you can produce the preimage of `H` within 3 days." She signs a transaction where, for the first three days after it is broadcast, only Bob can redeem it with knowledge of R, and afterwards it is redeemable only by Alice. This transaction is the HTLC. She gives it to Bob, but neither of them broadcasts it, because they expect to clear it out later.
3. Bob, knowing he can pull funds from Alice if he knows R, tells Carol: "I will pay you if you can produce the preimage of H within 2 days."
4. Carol does the same, making an HTLC that will pay Dave if Dave can produce R within 1 day. Dave does know R. Because Dave is able to pull the desired amount from Carol, he can consider the payment from Alice completed, and has no problem telling R to Carol and Bob so that they can collect their funds as well.
5. Everyone can now clear out. They have a guaranteed way to pull their funds by broadcasting these HTLCs on-chain, but prefer not to, since broadcasting on-chain is more expensive. Alice tells Bob: "I'll pay you, regardless of `R`, and in doing so we'll terminate the HTLC so we can forget about R." Bob does the same with Carol, and Carol with Dave.

([source](../../raw/docs/the-lightning-network/multihop-payments.md))

If Dave is uncooperative and refuses to give `R` to Bob and Carol, he must still broadcast the transaction from Carol within 1 day, and in doing so must reveal R to redeem the funds. Bob and Carol can look at the blockchain to determine what R is and settle off-chain as well. ([source](../../raw/docs/the-lightning-network/multihop-payments.md))

The guide concludes that a payment can be made across the Lightning Network using only off-chain transactions, without requiring direct channel links or trusting any intermediaries, as long as there is a path from the payer to the payee. It adds that once you don't have to trust the intermediaries you no longer care who they are, which it says allows Lightning nodes to be fully anonymous. ([source](../../raw/docs/the-lightning-network/multihop-payments.md))

## The payment cycle

Payments in the Lightning network require interaction between sender and receiver, meaning both parties need to be online at the same time. Sender and receiver must either be connected to each other with a payment channel, or a route through the wider network must exist that connects the two. ([source](../../raw/docs/the-lightning-network/multihop-payments/the-payment-cycle.md))

**Create invoice.** Upon agreeing on an amount, the recipient generates an invoice on their node, containing basic information such as amount, destination and validity. The recipient generates a preimage, a random number, and provides its hash as part of the invoice. All invoices are cryptographically signed. The source gives the command as:

```
lncli addinvoice –amt 10101 –memo “my first invoice”
```

([source](../../raw/docs/the-lightning-network/multihop-payments/the-payment-cycle.md))

The whole invoice is passed to the payer out of band, for example by displaying it on a website, on a smartphone, or a point of sale terminal. Invoices are commonly encoded as QR codes, but can also be transmitted by NFC or even sound. When creating an invoice, you may keep its payment hash (`r_hash`) to later check conveniently whether it has been paid. See [[lightning-invoices]]. ([source](../../raw/docs/the-lightning-network/multihop-payments/the-payment-cycle.md))

**Make the payment.** The payer passes the invoice to their Lightning Network node and confirms the instructions to pay it. The node creates multiple routes to the destination node and attempts them. The more invoices you pay, the more your node learns about the reliability of its peers to pass on payments in certain directions.

```
lncli payinvoice <bolt 11 invoice>
```

([source](../../raw/docs/the-lightning-network/multihop-payments/the-payment-cycle.md))

To make the payment, the node creates an HTLC over the amount to be forwarded to one of its peers, who passes it on to the next peer, and so on until it reaches its destination. The recipient node releases the preimage to its peers, which is used to settle the HTLCs inside the channels. The sender can use the preimage together with the signed invoice to prove the payment was made. ([source](../../raw/docs/the-lightning-network/multihop-payments/the-payment-cycle.md))

Invoices can be decoded using any Lightning node, which makes their contents human readable:

```
lncli decodepayreq --pay_req=<bolt 11 invoice>
```

([source](../../raw/docs/the-lightning-network/multihop-payments/the-payment-cycle.md))

**Check the payment.** The recipient can look up whether the payment was made using the payment hash:

```
lncli lookupinvoice --rhash=<r_hash>
```

([source](../../raw/docs/the-lightning-network/multihop-payments/the-payment-cycle.md))

**Other payment types.** Lightning Network invoices also exist for situations where the payment amount is not known ahead of time, for example donations. It is also possible to create static invoices that can be reused multiple times using AMP. There are alternative proposals on how to handle Lightning Network payments, such as LNURL or BOLT12. It is also possible to attach messages to Lightning payments or send payments over multiple paths at once. ([source](../../raw/docs/the-lightning-network/multihop-payments/the-payment-cycle.md))

## Payment terms (etymology)

- **Atomic Multi-path Payments (AMP).** An implementation of multi-path payments, which allows a single payment to be routed in shards along different routes. AMP ensures that each payment shard cannot be claimed individually by the recipient; only the whole payment can be claimed. AMP also implements keysend and allows the creation of static invoices, which can safely be paid multiple times. See [[multipath-payments]]. ([source](../../raw/docs/the-lightning-network/multihop-payments/etymology.md))
- **Keysend.** The mechanism to make a Lightning payment knowing only the recipient's public key. The source says this enables streaming payments and donations, and removes the requirement of prior interaction between payee and payer. Keysend is also the name of an implementation of this idea; today the concept is implemented as part of AMP. ([source](../../raw/docs/the-lightning-network/multihop-payments/etymology.md))
- **Lightning address.** A standard to look up LNURL pay requests on a http server, which allows email addresses to be associated with LNURL pay requests and Lightning payments to be made to usernames. ([source](../../raw/docs/the-lightning-network/multihop-payments/etymology.md))
- **Lightning invoice.** A bech32 encoded string containing all vital information to make a Lightning payment, such as the amount, recipient, features and payment hints in the case of a private node. ([source](../../raw/docs/the-lightning-network/multihop-payments/etymology.md))
- **LNURL.** A bech32 encoded url through which a Lightning wallet can interact with a server in an automated way. LNURLs can be an alternative to static invoices, allow for the withdrawal or redemption of funds, open channels or authenticate users. ([source](../../raw/docs/the-lightning-network/multihop-payments/etymology.md))
- **Multi-path Payments (MPP).** The idea of routing a payment along multiple routes to its destination, which can make it easier to route larger payments and can help with costs and privacy. MPP is also the name of an implementation of this idea, which the source describes as "today superseded by AMP". ([source](../../raw/docs/the-lightning-network/multihop-payments/etymology.md))
- **Payment route.** The path a payment takes from the payer to the payee. Unless a direct channel with sufficient capacity exists between the two, payments need to be routed through the network, along multiple routing nodes with the use of HTLCs. A single payment can be routed through multiple channels in serial and also in parallel, using AMP. ([source](../../raw/docs/the-lightning-network/multihop-payments/etymology.md))
- **Static invoices.** An invoice that does not expire and can be safely paid multiple times. AMP allows for the creation of static invoices, as do other proposals. ([source](../../raw/docs/the-lightning-network/multihop-payments/etymology.md))

## Timelocks

A time-locked Bitcoin transaction is one that is only valid after a certain period of time. Timelocks are used extensively in the Lightning Network and fall under two categories, absolute timelocks and relative timelocks. ([source](../../raw/docs/the-lightning-network/multihop-payments/timelocks.md))

| | Absolute Timelock | Relative Timelock |
|---|---|---|
| Transaction Level | nLockTime | nSequence |
| UTXO Level (or Script Level) | CheckLockTimeVerify (CLTV) | CheckSequenceVerify (CSV) |

([source](../../raw/docs/the-lightning-network/multihop-payments/timelocks.md))

### Absolute timelocks

Absolute timelocks restrict a transaction to only be valid after a certain point in time, for instance a time stamp or a block height. Today, block height is primarily used. ([source](../../raw/docs/the-lightning-network/multihop-payments/timelocks.md))

**nLocktime.** The source calls nLocktime the most commonly used timelock and says it has been a feature of bitcoin since its inception. Each bitcoin transaction specifies a nLocktime close to the most recently mined bitcoin block, meaning a miner cannot include the transaction as part of a block reorg concerning previous blocks. The source says it only began to be widely used around 2016, when it was included in Bitcoin Core 0.11. ([source](../../raw/docs/the-lightning-network/multihop-payments/timelocks.md))

**Check-locktime verify (CLTV).** CLTV is the timelock used in HTLCs. It is an absolute timelock that uses block height to determine when transactions become valid. Differences between the timelocks of incoming and outgoing HTLCs, called CLTV deltas, ensure that an incoming HTLC that is resolved on-chain can also be resolved in time in the outgoing channel. ([source](../../raw/docs/the-lightning-network/multihop-payments/timelocks.md))

CLTV enforces the timelock on the script level, while the nLocktime timelock is enforced at the time of the signature. So while nLocktime can be added when spending any coin, a CLTV condition has to be defined at the time the address is created, and the owner cannot alter it anymore. CLTV was introduced with BIP65 and activated through a soft fork in 2015. In addition to block height, the protocol also allows CLTVs to use timestamps. There is no limit to how far in the future a CLTV transaction can be locked. ([source](../../raw/docs/the-lightning-network/multihop-payments/timelocks.md))

### Relative timelocks

A relative timelock describes a period after which a transaction becomes valid, rather than a fixed timestamp or block height. The period refers to the number of blocks or seconds between inputs being confirmed on the blockchain and the outputs being valid. ([source](../../raw/docs/the-lightning-network/multihop-payments/timelocks.md))

**nSequence.** Analogous to nLocktime, nSequence is enforced at the transaction level rather than the script level. That means information about the minimum number of blocks that need to have passed since the input was confirmed can be added when signing the transaction that spends it. ([source](../../raw/docs/the-lightning-network/multihop-payments/timelocks.md))

**Check Sequence Verify (CSV).** The source calls CSV the main timelock in use today; it was activated in 2016 as BIP68, BIP112 and BIP113. It defines the sequence delay as part of the script, meaning it cannot be changed when the coins are spent. ([source](../../raw/docs/the-lightning-network/multihop-payments/timelocks.md))

CSV is used in commitment transactions, ensuring that the funds from a non-cooperative closure can only be recovered a certain number of blocks after the force closure has been initiated. The source describes CSV as the key component of allowing Lightning Network channels to exist indefinitely, rather than for a limited time. See [[payment-channels]] and [[watchtowers]]. ([source](../../raw/docs/the-lightning-network/multihop-payments/timelocks.md))

The "CSV Delay", defined at a channel's creation, is dependent on its size. It can also be configured manually with the `–max_local_csv` flag (printed with that dash in the source) of `lncli openchannel`. It expresses the number of blocks that need to pass before the initiator of a force close can spend their side of the balance, while the other party can always spend their funds immediately. ([source](../../raw/docs/the-lightning-network/multihop-payments/timelocks.md))

Relative timelocks can also be used to prevent transactions having unconfirmed parents, or pinning attacks, in which a transaction is prevented from being confirmed by submitting large, low-paying descendants. Unlike CLTV, CSV can only be defined for up to 65535 blocks (about 15 months). ([source](../../raw/docs/the-lightning-network/multihop-payments/timelocks.md))

No timelocks exist that make a transaction invalid after a certain time. The source says this follows a design principle of bitcoin that transactions can only become more permissible over time, not more restrictive, which is supposed to prevent funds being destroyed by becoming locked forever. ([source](../../raw/docs/the-lightning-network/multihop-payments/timelocks.md))

## Notes

Editor's notes, not from the sources: the `lncli addinvoice` line above is copied as the guide prints it, with typographic dashes and quotation marks (`–amt`, `–memo`, `“…”`) rather than ASCII `--` and `"`; the timelocks page likewise prints the CSV flag with a typographic dash, while the HTLC page (see [[htlc]]) writes it as `--max_local_csv`. Check [[lnd-receiving-payments]] or the lnd API reference before running these commands.
