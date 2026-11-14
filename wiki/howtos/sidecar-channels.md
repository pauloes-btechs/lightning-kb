---
title: Sidecar channels
type: howto
sources:
  - raw/docs/lightning-network-tools/pool/sidecar_channels.md
  - raw/docs/lightning-network-tools/pool.md
  - raw/docs/lightning-network-tools/pool/overview.md
  - raw/docs/lightning-network-tools/pool/orders.md
  - raw/docs/lightning-network-tools/pool/zero-confirmation-channels.md
  - raw/docs/lightning-network-tools/pool/faq.md
updated: 2026-11-14
---

# Sidecar channels

Sidecar channels are channel lease bids in [[pool]] made on behalf of a third node, typically one without its own Pool account. They are a tool for Lightning Service Providers (see [[lightning-service-providers]]) to help bootstrap new nodes, for instance mobile wallets or merchants, who may not have their own Pool account, an existing channel or a UTXO. ([source](../../raw/docs/lightning-network-tools/pool.md))

Like other channels, sidecar channels can be opened with a local and a remote balance, which makes it easier and faster to bootstrap a node with balanced channels that can both send and receive from the start. See [[inbound-capacity]]. ([source](../../raw/docs/lightning-network-tools/pool.md))

The overview frames the problem this way: Alice is new to Bitcoin entirely; how can she join the Lightning Network without making any on-chain transactions herself? Pool lets a third party, Carol, purchase a channel for Alice, which includes starting outbound liquidity. ([source](../../raw/docs/lightning-network-tools/pool/overview.md))

## Participants

- **Alice:** a new user, possibly on a mobile wallet, with no UTXOs but a wallet app that has lnd and Pool integrated as part of a unified binary. She only runs the Pool daemon and does not need her own Pool account. ([source](../../raw/docs/lightning-network-tools/pool/sidecar_channels.md))
- **Charlie:** a wallet/service provider offering the sidecar bootstrap service for a fee. He has a well funded Pool account that can be used to pay for leases. ([source](../../raw/docs/lightning-network-tools/pool/sidecar_channels.md))
- **Bob:** an independent liquidity provider willing to open channels to new users. He has a well funded Pool account that can be used to open channels. ([source](../../raw/docs/lightning-network-tools/pool/sidecar_channels.md))

## Requirements

All three participants need to run a Pool client that implements the sidecar functionality. Alice must be able to register with the auctioneer by providing the multisig pubkey and be able to sign with it. Charlie must be able to submit an order that refers to a multisig pubkey of the receiver node. Bob must be able to accept orders that require setting a push amount when opening the channel. No new functionality in lnd is required. ([source](../../raw/docs/lightning-network-tools/pool/sidecar_channels.md))

## Flow with the `--auto` flag

Precondition: Alice and Charlie reach an agreement out-of-band. In the guide's example Charlie buys 10 units (1m satoshi) of capacity for Alice, of which 2 units are pushed to Alice so she gains outbound liquidity as well. The order submission fees, chain fees, the premium and the push amount are all paid from Charlie's Pool account (see [[pool-accounts]]); whether Alice reimburses Charlie is not part of the protocol. ([source](../../raw/docs/lightning-network-tools/pool/sidecar_channels.md))

**1. Charlie creates the offer.**

```
charlie$   pool sidecar offer --capacity 1000000 --self_chan_balance 200000 --auto <rest of order details>
{
  "sidecar_ticket": "sidecar15o1Y9oXtyKr3hs2UQho9YmJKbSmB...."
}
```

The sidecar ticket now contains Charlie's offer to buy a 1m satoshi channel with a 200k initial self channel balance (the push amount) for Alice. The `--auto` flag signals that the existing auctioneer infrastructure should be used to let both peers communicate in order to finalize the ticket negotiation, so each side only executes a single command and the rest happens in the background. If `auto` is present only the capacity and balance need to be specified; otherwise all other information needs to be specified when submitting a full order. ([source](../../raw/docs/lightning-network-tools/pool/sidecar_channels.md))

**2. Alice registers the ticket.**

```
alice$   pool sidecar register sidecar15o1Y9oXtyKr3hs2UQho9YmJKbSmB
{ 
  "sidecar_ticket": "sidecar15o1Y9oXtyKr3hs2UQho9YmJKbSmB...."
}
```

The ticket now contains the `Recipient` field, which encodes Alice's node pubkey and the pubkey that will be used for the channel funding. Alice will be counter-signing the commitment transactions for the new channel, so she needs the private key for her 2-of-2 multisig channel funding key; it is derived from her keychain. ([source](../../raw/docs/lightning-network-tools/pool/sidecar_channels.md))

If the `auto` flag was set in the initial ticket, that is all: both sides wait for the next batch to be executed, which results in a new sidecar channel being created. Batches are described on [[pool-orders-and-batches]]. ([source](../../raw/docs/lightning-network-tools/pool/sidecar_channels.md))

## Flow without `--auto`

Without `auto`, Alice and Charlie carry out another round of communication after steps 1 and 2. ([source](../../raw/docs/lightning-network-tools/pool/sidecar_channels.md))

**3. Charlie submits the bid with the updated ticket he got from Alice.**

```
charlie$  pool orders submit bid --acct_key <charlie-key> \
  --interest_rate_percent xxx --sidecar_ticket  sidecarAAQgHBgUEAwIBAAMB...
{
   "order_nonce": "0011223344...",
  "sidecar_ticket": "sidecar15o1Y9oXtyKr3hs2UQho9YmJKbSmB...."
}
```

The ticket now contains the order's nonce in the `Order` part, and Charlie gives this final version of the ticket back to Alice. ([source](../../raw/docs/lightning-network-tools/pool/sidecar_channels.md))

The `sidecar_ticket` bid flag is described in the orders page as "Used to redeem a sidecar channel", and it overrides the `amt`, `min_chan_amt`, `lease_duration_blocks` and `self_chan_balance` flags. ([source](../../raw/docs/lightning-network-tools/pool/orders.md))

**4. Alice instructs her node to start expecting a channel.**

```
alice$  pool sidecar expect-channel sidecarAAQgHBgUEAwIBAAMBYwUBAg...
```

([source](../../raw/docs/lightning-network-tools/pool/sidecar_channels.md))

## Variations

The guide's example assumes Alice is aware of the onboarding costs and pays for them herself, out of band from the perspective of the Pool server. It notes that a wallet provider could also implement the flow so that it covers the full costs and "gifts" the channel and the balance to Alice. ([source](../../raw/docs/lightning-network-tools/pool/sidecar_channels.md))

Sidecar channels can also be zero-confirmation channels; the offer and register commands for that case are on [[pool-zero-conf-channels]]. ([source](../../raw/docs/lightning-network-tools/pool/zero-confirmation-channels.md))

See also: [[pool-trader]], [[pool-channel-auctioneer]].

## Conflicts

- **Whether buying for someone else is possible.** The FAQ answers "Can I buy a channel for someone else?" with "Not at this time but this is something we plan to add in the future" ([source](../../raw/docs/lightning-network-tools/pool/faq.md)), and the orders page's "Extensibility" section lists sidecar channels among restrictions that "will likely be implemented" in the future ([source](../../raw/docs/lightning-network-tools/pool/orders.md)). The sidecar channels page gives a working command line flow ([source](../../raw/docs/lightning-network-tools/pool/sidecar_channels.md)).
- **Size flag on `pool sidecar offer`.** The sidecar channels page uses `--capacity 1000000` ([source](../../raw/docs/lightning-network-tools/pool/sidecar_channels.md)); the zero-confirmation page uses `--amt 100000 --min_chan_amt 100000` ([source](../../raw/docs/lightning-network-tools/pool/zero-confirmation-channels.md)).
- **Name of the ticket field in the offer response.** `"sidecar_ticket"` on the sidecar channels page ([source](../../raw/docs/lightning-network-tools/pool/sidecar_channels.md)); `"ticket"` in the zero-confirmation page's example ([source](../../raw/docs/lightning-network-tools/pool/zero-confirmation-channels.md)).
- **What `--auto` requires.** The sidecar channels page says that with `auto` "only the capacity and balance need to be specified" ([source](../../raw/docs/lightning-network-tools/pool/sidecar_channels.md)); the zero-confirmation page's `--auto` example also passes `--interest_rate_percent`, `--channel_type` and `--acct_key` ([source](../../raw/docs/lightning-network-tools/pool/zero-confirmation-channels.md)).
- **Name of the third party.** The overview calls the purchaser Carol ([source](../../raw/docs/lightning-network-tools/pool/overview.md)); the sidecar channels page calls the provider Charlie ([source](../../raw/docs/lightning-network-tools/pool/sidecar_channels.md)).
