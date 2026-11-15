---
title: Sweeping
type: concept
sources:
  - raw/docs/the-lightning-network/payment-channels/understanding-sweeping.md
updated: 2026-11-14
---

# Sweeping

Sweeps are transactions from specialized scripts back into your main wallet. In the context of running a Lightning Network node, sweeping refers to transferring Bitcoin from specialized scripts into the node's main on-chain wallet. ([source](../../raw/docs/the-lightning-network/payment-channels/understanding-sweeping.md))

The primary need for sweeping arises from timeouts in scripts used in the Lightning Network: funds have to be moved within a certain amount of time, or else they may be swept by the channel peer. In addition, not all addresses are hierarchically generated, so not all addresses can be recovered using the node's seed phrase alone. To prevent funds from being unrecoverable after data loss, they are swept to an address that can be recovered purely from the seed phrase. ([source](../../raw/docs/the-lightning-network/payment-channels/understanding-sweeping.md))

See also: [[payment-channels]], [[htlc]], [[multihop-payments]], [[submarine-swaps]], [[watchtowers]], [[lnd-sweeper]].

## Types of funds that need to be swept

| Situation | What happens | What the sweep requires |
|---|---|---|
| Local force closure | When your node publishes the commitment transaction for a channel, the local balance is sent to an arbitration contract, from where your node can sweep the funds after a minimum amount of time has passed. | Your node's signature |
| Remote force closure | When a peer force closes on you, your funds can be swept after the force closure transaction is included in a block. | Your node's signature |
| Remote force closure with an invalid commitment transaction | You are able to sweep the peer's balance into your wallet within the pre-defined arbitration period using a revocation key. | Your node's signature and the revocation key |
| Incoming HTLCs | When your peer force closes your channel and the closure transaction contains an HTLC paid to you for which you have the preimage, you need to claim these funds by sweeping the HTLC within a predefined arbitration period. | Your node's signature and the preimage of the HTLC |
| Outgoing HTLCs | See below. | Your node's signature |
| Loop In | If a Loop In fails, for example because the off-chain funds couldn't be delivered to the destination node, the funds have to be swept back into your on-chain wallet after a timeout. | Your node's signature |
| Loop Out | The swap contract has to be swept by the recipient of the on-chain funds using the preimage of the off-chain payment. | Your node's signature and the preimage of the offchain payment |

([source](../../raw/docs/the-lightning-network/payment-channels/understanding-sweeping.md))

**Anchors.** When an anchor channel is force-closed, an anchor of 330 satoshis is created for each channel party that has a non-dust balance. These anchors can be swept within 16 blocks by you, or by anyone else afterwards, to prevent the UTXO set from bloating. The main purpose of the anchors is to give either party an opportunity to increase the fee of the commitment transaction using CPFP (Child Pays for Parent). Before 16 blocks the sweep requires your node's signature; after 16 blocks it does not require any signature, meaning others can sweep your anchors too. ([source](../../raw/docs/the-lightning-network/payment-channels/understanding-sweeping.md))

**Outgoing HTLCs.** If your node closes a channel by publishing a commitment transaction that contains an outgoing HTLC, your peer has the opportunity to claim this HTLC using the preimage. If the peer does not possess the preimage, or does not respond within the CLTV time limit, your node uses a pre-signed transaction to move the HTLC into another address, from where your peer gets the opportunity to claim the funds using the revocation key in case your node is publishing a breaching force closure transaction. After this "second stage" (which the source labels CLTV) expires, your node can finally sweep the funds back into its main wallet. ([source](../../raw/docs/the-lightning-network/payment-channels/understanding-sweeping.md))

See also: [[loop]], [[using-loop]], [[submarine-swaps]].

## Batch sweeping

Sweeps can be batched to save on on-chain fees. The source says that if your node needs to frequently perform sweeps you may increase the following setting to something higher, for instance an hour:

```
sweeper.batchwindowduration=10m
```

([source](../../raw/docs/the-lightning-network/payment-channels/understanding-sweeping.md))

## lncli

Pending sweeps can be inspected with `lncli wallet pendingsweeps`, and all performed sweeps with `lncli wallet listsweeps`. ([source](../../raw/docs/the-lightning-network/payment-channels/understanding-sweeping.md))

Not all sweeps are economical. Where the sweep amount is smaller than the sweep fees, LND will not attempt the sweep right away and instead waits for fees to go down. ([source](../../raw/docs/the-lightning-network/payment-channels/understanding-sweeping.md))
