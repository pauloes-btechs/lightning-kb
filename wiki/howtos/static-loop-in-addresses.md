---
title: Static Loop In addresses
type: howto
sources:
  - raw/docs/lightning-network-tools/loop/static-loop-in-addresses.md
  - raw/api/api-docs/api/loop/swap-client/new-static-address.md
  - raw/api/api-docs/api/loop/swap-client/list-unspent-deposits.md
  - raw/api/api-docs/api/loop/swap-client/list-static-address-deposits.md
  - raw/api/api-docs/api/loop/swap-client/list-static-address-swaps.md
  - raw/api/api-docs/api/loop/swap-client/list-static-address-withdrawals.md
  - raw/api/api-docs/api/loop/swap-client/get-static-address-summary.md
  - raw/api/api-docs/api/loop/swap-client/static-address-loop-in.md
  - raw/api/api-docs/api/loop/swap-client/static-open-channel.md
  - raw/api/api-docs/api/loop/swap-client/withdraw-deposits.md
updated: 2026-11-14
---

# Static Loop In addresses

A static Loop In Address is a special form of a timeout contract that backs a submarine swap. It is the timeout address that holds the funds of a new type of onchain to offchain submarine swap (see [[submarine-swaps]]), and it allows the on-chain transaction to occur independently of the off-chain transaction: the user can deposit funds on-chain at any time before initiating the Loop In. It is a feature of [[loop]]; the classic Loop In is on [[using-loop]]. ([source](../../raw/docs/lightning-network-tools/loop/static-loop-in-addresses.md))

Advantages the guide lists over a traditional swap, without compromising its trustless nature:

1. Lower onchain fees: fees may be set more conservatively, as inclusion in a block is not time sensitive.
2. Instant liquidity deployment: a Loop In from a static address no longer requires confirmations.
3. Flexible amounts: you may deposit any amount in multiple transactions and Loop In all or any combination of your deposits.
4. Change your mind: you may withdraw your on-chain funds from a Loop In Address at any time.
5. Send change to static addresses: to avoid small UTXOs you may send change to a Loop In Address, and channels may be cooperatively closed directly into one.

([source](../../raw/docs/lightning-network-tools/loop/static-loop-in-addresses.md))

The guide expects Static Addresses to become the default for performing Loop Ins. There is still a minimum swap size (currently 250,000 satoshis), but any UTXO held in a Loop In Address may be smaller. ([source](../../raw/docs/lightning-network-tools/loop/static-loop-in-addresses.md))

## Under the hood

Loop In Addresses are two-of-two multisignature taproot addresses: one key is held by the user, the other by Loop. They allow the user to recover their funds unilaterally after a pre-defined time-out, set at 14,400 blocks, or about 100 days. ([source](../../raw/docs/lightning-network-tools/loop/static-loop-in-addresses.md))

The swap flow as the guide describes it:

1. The user initiates a Loop In from the address for one or multiple UTXOs, which prompts the user to generate a Lightning invoice that is transmitted to the Loop service.
2. Before the invoice is paid, Loop requests the user to sign a transaction paying one or multiple UTXOs into a traditional submarine swap HTLC (see [[htlc]]). This HTLC transaction is held but not published by the Loop service.
3. Once it is signed, the Lightning invoice is paid. The user can recover their funds from the Loop In Address after a timeout if the invoice is not paid, and the service can recover the on-chain funds with the preimage obtained from paying the invoice.
4. To increase chain efficiency and reduce costs, the service then requests the user to sign a replacement transaction paying the funds directly into the on-chain wallet of the service. If successful, only this second transaction is published.

([source](../../raw/docs/lightning-network-tools/loop/static-loop-in-addresses.md))

The user may also request a withdrawal from their Loop In Address any time before its expiration. ([source](../../raw/docs/lightning-network-tools/loop/static-loop-in-addresses.md))

Warning from the guide: do not delete your L402 token (located in `~/.loop/mainnet`), as it is used to identify you to the service and is needed to perform Loop Ins or withdrawals. If the L402 token is lost, the only way to exit the contract is to wait for the timeout to pass. See [[l402]]. ([source](../../raw/docs/lightning-network-tools/loop/static-loop-in-addresses.md))

## Commands

| Command | What it does, per the guide |
| --- | --- |
| `loop static new` | generates a Loop In Address |
| `loop static listunspent` | shows all Loop In Address deposits that are still unspent |
| `loop static listdeposits` | shows all available and completed Loop In actions with sufficient confirmations |
| `loop static withdraw` | spends any amounts to a specified address |
| `loop static in` | performs the swap into your Lightning channel balance |
| `loop static listswaps` | shows all swaps |
| `loop static summary` | shows the number of deposits, the timelock and your static address |

([source](../../raw/docs/lightning-network-tools/loop/static-loop-in-addresses.md))

`loop static listunspent` returns `utxos`, each with `static_address`, `amount_sat`, `outpoint` and `confirmations`. ([source](../../raw/docs/lightning-network-tools/loop/static-loop-in-addresses.md))

A deposit shows up in `loop static listdeposits` once it has six confirmations on the Bitcoin blockchain. Withdrawn or expired deposits, completed Loop Ins and various error messages also appear there. Each entry of `filtered_deposits` has `id`, `state` (for example `DEPOSITED`), `outpoint`, `value`, `confirmation_height` and `blocks_until_expiry`. ([source](../../raw/docs/lightning-network-tools/loop/static-loop-in-addresses.md))

A static Loop In Address can also be used as a regular on-chain wallet: any static address deposit is just a pay-to-taproot output, so transactions from these addresses are not more or less expensive than transactions from the internal LND wallet. ([source](../../raw/docs/lightning-network-tools/loop/static-loop-in-addresses.md))

With `loop static in` you can select which UTXOs to swap, how much to swap and optionally which channel the payment should arrive in. The guide's example output has `swap_hash`, `state` (`SignHtlcTx`), `amount`, `htlc_cltv`, `quoted_swap_fee_satoshis`, `max_swap_fee_satoshis`, `initiation_height`, `protocol_version` (`V0`), `label`, `initiator` (`loop-cli`) and `payment_timeout_seconds` (60). ([source](../../raw/docs/lightning-network-tools/loop/static-loop-in-addresses.md))

`loop static listswaps` lists `swaps` with `swap_hash`, `deposit_outpoints`, `state`, `swap_amount_satoshis` and `payment_request_amount_satoshis`. In the guide's example a swap of 300000 satoshis in state `SUCCEEDED` has a payment request amount of 298550, and its `quoted_swap_fee_satoshis` was 1450. ([source](../../raw/docs/lightning-network-tools/loop/static-loop-in-addresses.md))

`loop static summary` returns `static_address`, `relative_expiry_blocks`, `total_num_deposits`, `value_unconfirmed_satoshis`, `value_deposited_satoshis`, `value_expired_satoshis`, `value_withdrawn_satoshis`, `value_looped_in_satoshis` and `value_htlc_timeout_sweeps_satoshis`. ([source](../../raw/docs/lightning-network-tools/loop/static-loop-in-addresses.md))

The guide closes by saying that at this point in time only one static Loop In Address is available per user, and that Loop will expand its offerings in the future to allow for multiple static addresses and channel opens. ([source](../../raw/docs/lightning-network-tools/loop/static-loop-in-addresses.md))

## RPCs

All of these are on [[loop-swap-client]].

| RPC | REST | Purpose |
| --- | --- | --- |
| NewStaticAddress | `POST` `/v1/staticaddr` | requests a new static address for loop-ins from the server |
| ListUnspentDeposits | `GET` `/v1/staticaddr/deposits/unspent` | returns a list of utxos deposited at a static address |
| ListStaticAddressDeposits | `GET` `/v1/staticaddr/deposits` | returns a list of filtered static address deposits |
| WithdrawDeposits | `POST` `/v1/staticaddr/withdraw` | withdraws a selection or all deposits of a static address |
| ListStaticAddressWithdrawals | `GET` `/v1/staticaddr/withdrawals` | returns a list of static address withdrawals |
| StaticAddressLoopIn | `POST` `/v1/staticaddr/loopin` | initiates a static address loop-in swap |
| ListStaticAddressSwaps | `GET` `/v1/staticaddr/swaps` | returns a list of filtered static address swaps |
| GetStaticAddressSummary | `GET` `/v1/staticaddr/summary` | returns a summary of static address related statistics |
| StaticOpenChannel | none listed on the page | opens a channel funded by selected static address deposits |

Sources, in table order: ([source](../../raw/api/api-docs/api/loop/swap-client/new-static-address.md)) ([source](../../raw/api/api-docs/api/loop/swap-client/list-unspent-deposits.md)) ([source](../../raw/api/api-docs/api/loop/swap-client/list-static-address-deposits.md)) ([source](../../raw/api/api-docs/api/loop/swap-client/withdraw-deposits.md)) ([source](../../raw/api/api-docs/api/loop/swap-client/list-static-address-withdrawals.md)) ([source](../../raw/api/api-docs/api/loop/swap-client/static-address-loop-in.md)) ([source](../../raw/api/api-docs/api/loop/swap-client/list-static-address-swaps.md)) ([source](../../raw/api/api-docs/api/loop/swap-client/get-static-address-summary.md)) ([source](../../raw/api/api-docs/api/loop/swap-client/static-open-channel.md))

NewStaticAddress takes `client_key`, the client's public key for the 2-of-2 MuSig2 taproot static address, and returns `address` and `expiry`, the CSV expiry of the static address. ([source](../../raw/api/api-docs/api/loop/swap-client/new-static-address.md))

In StaticAddressLoopIn, `amount` is optional. Provided with `outpoints`, the client takes this amount from the sum of the outpoints and sends the change back to the static address. Provided without outpoints, the client selects deposits automatically, sorting available deposits in descending order by amount (equal amounts in ascending order of blocks until expiry) and selecting the largest first until the amount is reached. ([source](../../raw/api/api-docs/api/loop/swap-client/static-address-loop-in.md))

In WithdrawDeposits, if there is change it is sent back to the static address, and the fees for the transaction are taken from the change output; if the change is below the dust limit there is no change output and the dust goes towards fees. ([source](../../raw/api/api-docs/api/loop/swap-client/withdraw-deposits.md))

A deposit's `state` is a `DepositState`; `DEPOSITED` indicates that the deposit has been sufficiently confirmed on chain, `LOOPED_IN` that it was used in a static address loop-in swap, `WITHDRAWN` that it has been withdrawn and `EXPIRED` that it has expired and the sweep transaction has been sufficiently confirmed. ([source](../../raw/api/api-docs/api/loop/swap-client/list-static-address-deposits.md))

## Conflicts

- Timeout length: the guide says the time-out is "set at 14,400 blocks, or about 100 days" and elsewhere that waiting for timeouts "may take up to three months", while its example `loop static summary` output shows `"relative_expiry_blocks": "1500"` (the example addresses start with `tb1`). ([source](../../raw/docs/lightning-network-tools/loop/static-loop-in-addresses.md))
- Number of addresses: the guide says "You may generate one or multiple Loop In Addresses" with `loop static new`, and later "At this point in time only one static Loop In Address is available per user". ([source](../../raw/docs/lightning-network-tools/loop/static-loop-in-addresses.md))
- Channel opens: the guide says Loop "will expand its offerings in the future to allow for ... channel opens" ([source](../../raw/docs/lightning-network-tools/loop/static-loop-in-addresses.md)), while the API reference already lists a StaticOpenChannel RPC tagged loop:`static openchannel` ([source](../../raw/api/api-docs/api/loop/swap-client/static-open-channel.md)).
- CLI names: the guide uses `loop static listdeposits` and `loop static listswaps` ([source](../../raw/docs/lightning-network-tools/loop/static-loop-in-addresses.md)), while the API pages tag the RPCs loop:`listdeposits` ([source](../../raw/api/api-docs/api/loop/swap-client/list-static-address-deposits.md)) and loop:`listswaps` ([source](../../raw/api/api-docs/api/loop/swap-client/list-static-address-swaps.md)), without the `static` prefix that other pages such as loop:`static summary` carry ([source](../../raw/api/api-docs/api/loop/swap-client/get-static-address-summary.md)).

## Notes

Synthesis: the API reference is stamped with a specific commit and the guide carries no version, so the guide may describe an earlier state of the feature than the API reference; the sources do not say this explicitly.
