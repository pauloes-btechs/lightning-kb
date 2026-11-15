---
title: Hash time-locked contracts (HTLCs)
type: concept
sources:
  - raw/docs/the-lightning-network/multihop-payments/hash-time-lock-contract-htlc.md
  - raw/docs/the-lightning-network/multihop-payments/etymology.md
updated: 2026-11-14
---

# Hash time-locked contracts (HTLCs)

A Hash Time-lock Contract (also sometimes Hashed Time-lock Contract) is central to the mechanism of a Lightning payment. A HTLC is a bitcoin transaction that can either be redeemed by producing a secret preimage represented by a hash, or by waiting for a predefined period of time. Lightning payments are made to this hash of the preimage, which the recipient has to reveal to claim the payment. If the payee does not reveal the preimage, the payment can be claimed back by the sender after a timeout period. ([source](../../raw/docs/the-lightning-network/multihop-payments/etymology.md))

While a Lightning Network channel is a 2-of-2 multisignature address with funds on the bitcoin blockchain, a HTLC is an output of an unconfirmed transaction to a separate "smart contract" address with the following properties:

1. The smart contract can be spent by revealing a "secret" together with a valid signature of the recipient.
2. The smart contract can be redeemed after a set amount of time together with a valid signature of the sender.

HTLCs with these two conditions also find application outside the Lightning Network. When used to transfer funds through a Lightning channel, a HTLC comes with a third condition:

3. The smart contract can be spent immediately by someone presenting a revocation key.

([source](../../raw/docs/the-lightning-network/multihop-payments/hash-time-lock-contract-htlc.md))

Ideally, this transaction never needs to be committed onto the blockchain. Instead, when the preimage is revealed by the recipient, the balances of the channel can be updated, creating a new commitment transaction and invalidating the previous one. ([source](../../raw/docs/the-lightning-network/multihop-payments/hash-time-lock-contract-htlc.md))

See also: [[multihop-payments]], [[payment-channels]], [[sweeping]], [[submarine-swaps]], [[lightning-invoices]], [[lnd-channel-fees]].

## Lifecycle of an HTLC

**1) The commitment transaction.** The commitment transaction of a regular payment channel contains a single input, which represents the channel point, or transaction ID of the channel. The transaction referenced by this input is recorded on the blockchain and can only be spent with a transaction signed by both Bob and Alice. The commitment transaction is signed by both and spends the channel balance according to their channel balances; in the source's example a 10 BTC channel pays 9 BTC to Alice and 1 BTC to Bob. ([source](../../raw/docs/the-lightning-network/multihop-payments/hash-time-lock-contract-htlc.md))

**2) A HTLC is created.** Alice is presented with an invoice over 1 BTC. She creates a new commitment transaction that reduces her balance to 8 BTC, keeps Bob's balance at 1 BTC, and adds a new output over 1 BTC. This output is the HTLC. The source says the script of this address might look like this:

```
IF <revocation pubkey>
ELSE IF <hash(preimage)>
    <recover pubkey>
ELSE CHECKLOCKTIME
    <sender pubkey>
```

([source](../../raw/docs/the-lightning-network/multihop-payments/hash-time-lock-contract-htlc.md))

The `revocation pubkey` is to prevent either Bob or Alice from stealing funds by publishing older channel state. The `recover pubkey` is Bob's key to claim the 1 BTC if he provides the `preimage` from the final receiver. The `sender pubkey` is Alice's key to claim the 1 BTC back after a certain time if Bob doesn't show the `preimage`. ([source](../../raw/docs/the-lightning-network/multihop-payments/hash-time-lock-contract-htlc.md))

Depending on the route chosen, Bob might now forward this HTLC by creating a new commitment transaction for one of his channels, removing 1 BTC from his channel balance. He commits it into a similar HTLC with the same preimage hash, with the recover pubkey of his channel peer and his own sender pubkey. ([source](../../raw/docs/the-lightning-network/multihop-payments/hash-time-lock-contract-htlc.md))

**3) A HTLC is consolidated.** Once the recipient of the payment sees a commitment transaction with an HTLC made to the hash of the preimage, they can safely reveal the preimage. The HTLC can then be consolidated back into the channel balance: Bob creates a new commitment transaction that removes the HTLC output and adds its balance to his channel balance. Alice, aware that Bob knows the preimage and could claim the HTLC on-chain, has an interest in co-signing it. The payment cycle is complete. ([source](../../raw/docs/the-lightning-network/multihop-payments/hash-time-lock-contract-htlc.md))

An HTLC might also get consolidated because the payment could not be completed. In this case Alice creates a new commitment transaction that updates her balance back to its earlier state in step (1), and Bob, unable to claim the HTLC, has an interest in signing it to keep the channel alive. ([source](../../raw/docs/the-lightning-network/multihop-payments/hash-time-lock-contract-htlc.md))

**4) A HTLC is settled on-chain.** In some rare events the HTLC needs to be settled on-chain, for example when Alice does not co-sign the new commitment transaction because she has become unresponsive. Settling an HTLC on-chain causes a force-close of the channel and locks up its funds. Depending on whether the preimage is known, the HTLC can be redeemed immediately or once the waiting period has passed. If an old, revoked HTLC is committed to the chain, the revocation key can be used by the other party to take the funds. See [[sweeping]]. ([source](../../raw/docs/the-lightning-network/multihop-payments/hash-time-lock-contract-htlc.md))

**5) Multi-hop payments.** The main use of HTLCs is to safely enable payments through multiple channels. Payments can be made atomically, meaning they either fail entirely or succeed, and a routing node is not able to take funds at any point. To achieve this, all peers along a route construct their HTLCs from the same hash of the same secret preimage: for their outgoing peer to claim the funds they send, the preimage needs to be revealed, which lets them likewise claim their funds from their incoming peer. See [[multihop-payments]]. ([source](../../raw/docs/the-lightning-network/multihop-payments/hash-time-lock-contract-htlc.md))

To remove racing conditions, peers along a route want their HTLCs to expire in the order in which they can be redeemed. If an HTLC is settled on-chain by the ultimate recipient, the preimage revealed in that transaction becomes known to their channel peer, who can then claim their HTLC. ([source](../../raw/docs/the-lightning-network/multihop-payments/hash-time-lock-contract-htlc.md))

## HTLC constraints

**Asymmetry.** As with commitment transactions, depending on who attempts to commit the HTLC on chain, a different revocation key and waiting period is applied. ([source](../../raw/docs/the-lightning-network/multihop-payments/hash-time-lock-contract-htlc.md))

**Waiting period.** The waiting period can be defined individually for each channel at its creation using the `--max_local_csv` and `--remote_csv_delay` flags of `lncli openchannel`. A large waiting period makes it safer to recover from a failure, but also locks up funds for longer if a channel closes unilaterally. ([source](../../raw/docs/the-lightning-network/multihop-payments/hash-time-lock-contract-htlc.md))

**CLTV delta.** The timelock delta (or CLTV expiry delta) is the minimum difference between the expiration of an incoming and outgoing HTLC. It ensures there is always enough time to settle an HTLC, even if previous HTLCs are settled on-chain at the last minute. It can be set using the `--time_lock_delta` flag of `lncli updatechanpolicy` or in the configuration file, where the source shows:

```
bitcoin.timelockdelta=40
```

([source](../../raw/docs/the-lightning-network/multihop-payments/hash-time-lock-contract-htlc.md))

**HTLC size.** For each channel you can define the minimum and maximum HTLC size. The source says it might be rational to set a minimum HTLC size with `--min_htlc_msat`, to not risk a channel closure for a small HTLC or for a HTLC that cannot be settled on-chain due to the dust limit. ([source](../../raw/docs/the-lightning-network/multihop-payments/hash-time-lock-contract-htlc.md))

**Maximum value in flight.** The total number of satoshis that can be pending at any point in a channel can be limited using `--remote_max_value_in_flight_msat` at the channel opening. ([source](../../raw/docs/the-lightning-network/multihop-payments/hash-time-lock-contract-htlc.md))

**Multiple HTLCs.** Each channel can handle hundreds of HTLCs at once. The maximum limit of 483 is set as the default, and can be reduced in the configuration file:

```
default-remote-max-htlcs=483
```

([source](../../raw/docs/the-lightning-network/multihop-payments/hash-time-lock-contract-htlc.md))

Example usage given by the source:

```
lncli updatechanpolicy --base_fee_msat 100 --fee_rate 0.00001 --time_lock_delta 50 --min_htlc_msat 1000 --chan_point 17ec2d0ac18d953b1dfe2cafa116b0c118020cab4d80c4063fe98debda6df469:1
```

```
lncli openchannel --node_key 021c97a90a411ff2b10dc2a8e32de2f29d2fa49d41bfbb52bd416e460db0747d0d --connect 50.112.125.89:9735 --local_amt 210000000 --remote_max_value_in_flight_msat 105000000000 --max_local_csv 50
```

([source](../../raw/docs/the-lightning-network/multihop-payments/hash-time-lock-contract-htlc.md))
