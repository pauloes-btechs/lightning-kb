---
title: Pool accounts and recovery
type: howto
sources:
  - raw/docs/lightning-network-tools/pool.md
  - raw/docs/lightning-network-tools/pool/accounts.md
  - raw/docs/lightning-network-tools/pool/account_recovery.md
  - raw/docs/lightning-network-tools/pool/first-steps.md
  - raw/docs/lightning-network-tools/pool/quickstart.md
  - raw/docs/lightning-network-tools/pool/faq.md
updated: 2026-11-14
---

# Pool accounts and recovery

Before you can start trading, you need an account. ([source](../../raw/docs/lightning-network-tools/pool/accounts.md))

See also: [[pool]], [[pool-setup]], [[pool-orders-and-batches]], [[pool-trader]].

## What an account is

Accounts in Pool are special on-chain contracts. A user deposits funds into an account which has a set expiry. Committing funds in order to place orders ensures users are unable to spoof orders (place an order they can't fulfill), and adds a cost to attempting to sybil attack the venue. ([source](../../raw/docs/lightning-network-tools/pool/accounts.md))

Funds can be moved from the account in two ways: with a joint 2-of-2 signature by the auctioneer and the user, or unilaterally by the user after the expiration period has passed. The second clause ensures users can move their funds if the auctioneer is unavailable. ([source](../../raw/docs/lightning-network-tools/pool/accounts.md))

The Pool landing page states that the account has an expiration time of 90 days, that it can be closed cooperatively at any time while active, and that at no point does Pool or Lightning Labs take possession or control over the funds. ([source](../../raw/docs/lightning-network-tools/pool.md))

Many interactions are based around accounts: fees paid to the auctioneer are deducted from the account; fees gained by selling channels are credited to it; funds used to open channels to others are deducted from it. Because an account is just a UTXO, any time a batch is cleared the account is spent and re-created in the same transaction. ([source](../../raw/docs/lightning-network-tools/pool/accounts.md))

The FAQ explains that accounts expire so that users can recover funds if the servers were to go offline for a period of time, and that the account is debited whenever an order is fully or partially matched. ([source](../../raw/docs/lightning-network-tools/pool/faq.md))

## Create an account

Creating an account has two parameters: the size of the account and its expiry. Both can be adjusted later. The funds are pulled from your `lnd` wallet (see [[lnd]]). ([source](../../raw/docs/lightning-network-tools/pool/accounts.md), [source](../../raw/docs/lightning-network-tools/pool/quickstart.md))

```
pool accounts new --amt=50000000 --expiry_height=1773394 --conf_target=6
```

The response contains `trader_key` (used to sign orders), `outpoint`, `value`, `expiration_height`, `state` (here `PENDING_OPEN`, meaning unconfirmed) and `close_txid`. In the guide's example this creates an account with 0.5 BTC that expires at height `1773394`. ([source](../../raw/docs/lightning-network-tools/pool/accounts.md))

A relative expiry based on the current best block can be given with `--expiry_blocks` instead; for an account that expires in 2 weeks the guide passes `--expiry_blocks=2016`. ([source](../../raw/docs/lightning-network-tools/pool/accounts.md))

The first-steps guide uses this form, and says you are asked to confirm the opening of the account, including the amount and the miner fee, after which you receive your trader key and transaction ID. It also notes that orders typically can no longer be matched 144 blocks before the account's expiration time. ([source](../../raw/docs/lightning-network-tools/pool/first-steps.md))

```
pool accounts new 5000000 --expiry_blocks 12960 --conf_target 12
```

## Check an account

`pool accounts list` shows the available balance, the account expiration, the utxo the funds are currently held in and the state the account is in. The first-steps example output has the fields `trader_key`, `outpoint`, `value`, `available_balance`, `expiration_height`, `state`, `latest_txid` and `version` (with the value `ACCOUNT_VERSION_TAPROOT`). ([source](../../raw/docs/lightning-network-tools/pool/first-steps.md))

Account states that appear in the guide's example outputs are `PENDING_OPEN`, `OPEN` and `PENDING_UPDATE`. ([source](../../raw/docs/lightning-network-tools/pool/accounts.md))

## Deposit

`pool accounts deposit` adds funds to an account. The trader key is given explicitly because `poold` can manage multiple accounts. The funds come from the backing `lnd` node that `poold` is connected to. ([source](../../raw/docs/lightning-network-tools/pool/accounts.md))

```
pool accounts deposit --trader_key=0288096be9917f8ebdfc6eb2701635fe658f4eae1e0274dcce41418b3fb5145732 --amt=1000000 --sat_per_vbyte=5
```

The response shows the modified account, in state `PENDING_UPDATE`, alongside a `deposit_txid`. Once that transaction has confirmed the account can be used again. ([source](../../raw/docs/lightning-network-tools/pool/accounts.md))

You should never send coins directly to your account output, as it won't be picked up by the auctioneer. ([source](../../raw/docs/lightning-network-tools/pool/accounts.md))

A deposit is also an opportunity to extend the validity of the account; the first-steps example adds `--expiry_height 774774` to the deposit command. ([source](../../raw/docs/lightning-network-tools/pool/first-steps.md))

## Withdraw

Incrementally withdrawing from an account is supported, with a command similar to deposit plus a destination address. ([source](../../raw/docs/lightning-network-tools/pool/accounts.md))

```
pool accounts withdraw --trader_key=0288096be9917f8ebdfc6eb2701635fe658f4eae1e0274dcce41418b3fb5145732 --amt=1000000 --sat_per_vbyte=5 --addr=tb1qe3ueyx8jhlj4h0s6mgywmtl8vlwxqkgkgp3m3s
```

The response shows the account in state `PENDING_UPDATE` and a `withdraw_txid`. ([source](../../raw/docs/lightning-network-tools/pool/accounts.md))

## Close

To send all funds elsewhere, the account can be closed before the main expiration period. ([source](../../raw/docs/lightning-network-tools/pool/accounts.md))

```
pool accounts close --trader_key=0288096be9917f8ebdfc6eb2701635fe658f4eae1e0274dcce41418b3fb5145732 --sat_per_vbyte 11
```

If no address is specified, the funds are returned to the internal LND wallet. ([source](../../raw/docs/lightning-network-tools/pool/first-steps.md))

According to the FAQ, if an account expires you need to close it and then re-open it. ([source](../../raw/docs/lightning-network-tools/pool/faq.md))

## Recover an account after data loss

Account funds are locked to a 2-of-2 multi-sig output of the account owner and the Pool auctioneer until the account's expiration has been met, at which point the owner has full control of the funds. The expiration is included in the account output script, so it must be known in order to spend the account funds. ([source](../../raw/docs/lightning-network-tools/pool/account_recovery.md))

There are two possible ways to recover an account's funds after data corruption or loss: one that requires the Pool auctioneer's cooperation, which is the only method currently supported, and one without, which will require storage of an additional data blob similar to the Static Channel Backups in `lnd` (see [[lnd-recovery]]). ([source](../../raw/docs/lightning-network-tools/pool/account_recovery.md))

### Auctioneer-assisted recovery

An auctioneer-assisted recovery intent is issued through the `pool accounts recover` command or the `RecoverAccounts` RPC (see [[pool-trader]]). ([source](../../raw/docs/lightning-network-tools/pool/account_recovery.md))

```
pool accounts recover
```

How it works: the account owner sends a recovery intent to the auctioneer, along with a challenge response to prove ownership. The intent includes a set of keys derived by the account BIP-0043 derivation path `m/1017'/coin_type'/220'/0/index`, so the same `lnd` seed that was used to create the accounts must be used. The auctioneer verifies the challenge response, determines the validity of the account key, and provides the latest details of the account known to it. The owner can then continue using the account in the auction without performing any on-chain transactions, or close the account and withdraw. ([source](../../raw/docs/lightning-network-tools/pool/account_recovery.md))

Limits stated in the command's help text and the guide: ([source](../../raw/docs/lightning-network-tools/pool/account_recovery.md))

- Recovery is possible as long as the connected lnd node is running with the same seed as when the accounts were first created.
- The command should only be used after data loss; it will fail if there already are open accounts in the trader's database.
- All open or pending orders of any recovered account are canceled on the auctioneer's side and are not restored in the trader's database.

### Umbrel

On Umbrel, the guide gives this command for recovering an account: ([source](../../raw/docs/lightning-network-tools/pool/account_recovery.md))

```
docker exec -it lightning-terminal_web_1 pool --rpcserver=localhost:8443 --tlscertpath=~/.lit/tls.cert accounts recover
```

## Conflicts

- **Confirmations before an account is open.** First steps: "We will have to wait for two confirmations for the account to be open" ([source](../../raw/docs/lightning-network-tools/pool/first-steps.md)). Accounts page and quickstart: "Once at least 3 blocks have passed (in the alpha), the account will be confirmed and ready for use" ([source](../../raw/docs/lightning-network-tools/pool/accounts.md), [source](../../raw/docs/lightning-network-tools/pool/quickstart.md)).
- **Key flag on `pool accounts withdraw`.** The accounts page uses `--trader_key` ([source](../../raw/docs/lightning-network-tools/pool/accounts.md)). The first-steps page prints `pool accounts withdraw –amt 100000 –acct_key 0389f9aad3e08ae5065985049428eb8d862455060b429e2ad42fda52830673e3c1 --addr bc1qlrz7ehzn4fad3hhdzku6ucauzks8d0sa2ksmtl`, with `acct_key` and en dashes ([source](../../raw/docs/lightning-network-tools/pool/first-steps.md)).
- **Amount on `pool accounts new`.** Positional in first steps (`pool accounts new 5000000 ...`), a flag in the accounts page and quickstart (`--amt=50000000`). The first-steps example output also shows `"value": 500000` after a command that asks for `5000000` ([source](../../raw/docs/lightning-network-tools/pool/first-steps.md), [source](../../raw/docs/lightning-network-tools/pool/accounts.md), [source](../../raw/docs/lightning-network-tools/pool/quickstart.md)).
- **Extending an account.** The FAQ says an expired account must be closed and re-opened and "In the future we will enable account renewals" ([source](../../raw/docs/lightning-network-tools/pool/faq.md)). The first-steps page says a deposit "gives us also the opportunity to extend the validity of our account" and passes `--expiry_height` to `pool accounts deposit` ([source](../../raw/docs/lightning-network-tools/pool/first-steps.md)).
- **Account fields in example output.** The accounts page examples include `close_txid` and no `available_balance`, `latest_txid` or `version` ([source](../../raw/docs/lightning-network-tools/pool/accounts.md)); the first-steps example includes `available_balance`, `latest_txid` and `version` and no `close_txid` ([source](../../raw/docs/lightning-network-tools/pool/first-steps.md)).
