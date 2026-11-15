---
title: lnd wallet, PSBT and key import
type: howto
sources:
  - raw/docs/lightning-network-tools/lnd/wallet.md
  - raw/docs/lightning-network-tools/lnd/psbt.md
  - raw/docs/lightning-network-tools/lnd/bulk-psbt.md
  - raw/docs/lightning-network-tools/lnd/key_import.md
  - raw/docs/lightning-network-tools/lnd/lnd.conf.md
updated: 2026-11-14
---

# lnd wallet, PSBT and key import

How to create, unlock and protect the [[lnd]] wallet, build and sign Partially Signed Bitcoin Transactions (PSBTs), open single or batched channels with external funds, and import extended public keys as watch-only accounts. The RPCs referred to here are on [[lnd-wallet-kit]] and [[lnd-lightning]].

## The wallet

The `lnd` wallet is a database file in the data directory (for example `~/.lnd/data/chain/bitcoin/mainnet/wallet.db` on Linux) holding all addresses and private keys for on-chain and off-chain funds. It is independent of the chain backend (`bitcoind`, `btcd` or `neutrino`) and must be created as the first step after starting a fresh node. It is encrypted with a user-chosen "wallet password", which `lnd` does not store, so the wallet must be unlocked after every restart. ([source](../../raw/docs/lightning-network-tools/lnd/wallet.md))

**Create.** `lncli create` prompts for a wallet password and an optional cipher seed passphrase, then prints a 24 word cipher seed mnemonic to write down. `create` is also used to recover a node from an existing seed (see [[lnd-recovery]]). ([source](../../raw/docs/lightning-network-tools/lnd/wallet.md))

**Unlock.** On every fresh start (for example after a system restart or upgrade) the log shows a `LTND: Waiting for wallet encryption password.` message pointing to `lncli create`, `lncli unlock` and `lncli changepassword`. Run `lncli unlock` and type the password. ([source](../../raw/docs/lightning-network-tools/lnd/wallet.md))

**Auto-unlock.** From `v0.13.0-beta`, `--wallet-unlock-password-file=<path>` (or `wallet-unlock-password-file=` under `[Application Options]` in `lnd.conf`) reads the password from a file. It can only be activated after the wallet was created manually: start lnd without the flag, `lncli create`, `lncli stop`, write the password to a file readable only by your user (`chmod 0400`), then restart with the flag. The guide warns that a password file on the same disk as the wallet is not in itself more secure than an unencrypted database. A more secure variant uses a password manager (`pass` in the example) writing into a named pipe created with `mkfifo`, passed as the password file; this works only on Unix-like file systems. ([source](../../raw/docs/lightning-network-tools/lnd/wallet.md))

The sample config adds that when the password file is set, unlocking through RPC is not possible and lnd exits if no wallet exists or the password is wrong, unless `wallet-unlock-allow-create` is also set. ([source](../../raw/docs/lightning-network-tools/lnd/lnd.conf.md))

**Change password.** Only possible while the wallet is locked: after a restart run `lncli changepassword` instead of `unlock`. It asks for the old and new password, re-encrypts the database and unlocks the wallet. ([source](../../raw/docs/lightning-network-tools/lnd/wallet.md))

**Do not use `--noseedbackup` on mainnet.** With this flag a wallet is created automatically on first start, the seed is never shown (so a lost disk or deleted wallet file means the funds cannot be recovered), and the wallet is encrypted with a well-known default password, so anyone who copies the file can steal the funds. Use it only on testnet, regtest or simnet. ([source](../../raw/docs/lightning-network-tools/lnd/wallet.md))

## PSBT basics

`lnd`'s wallet can create, sign and fund channels with PSBTs (BIP174). To avoid malleability, all inputs to a funding transaction must be segwit spends; P2PKH and normal P2SH return an error. ([source](../../raw/docs/lightning-network-tools/lnd/psbt.md))

**Fund.** `lncli wallet psbt fund` selects inputs and adds a change output. It resembles `bitcoind`'s `walletcreatefundedpsbt`, but accepts a template PSBT, and `--outputs` amounts are in satoshis: ([source](../../raw/docs/lightning-network-tools/lnd/psbt.md))

```
lncli wallet psbt fund --outputs='{"<address>":50000000}'
lncli wallet psbt fund --outputs='{"<address>":50000000}' \
    --inputs='["<txid>:<index>","<txid>:<index>"]'
```

The response contains `psbt`, `change_output_index` and `locks`. Selected UTXOs are locked and cannot be used by the internal wallet or other RPCs until the lock expires after 10 minutes or a transaction spending them is published. `lncli listunspent` lists UTXOs for manual coin selection. ([source](../../raw/docs/lightning-network-tools/lnd/psbt.md))

**Sign and finalize.** `lncli wallet psbt finalize <psbt>` signs and returns `psbt` and `final_tx`. Do not publish the final transaction manually if any output funds a channel. ([source](../../raw/docs/lightning-network-tools/lnd/psbt.md))

## Opening a channel with a PSBT

With the PSBT flow, `lnd` can open a channel with a wallet balance of `0`. Negotiation with the peer starts immediately (to get its multisig key) and pauses until a fully signed transaction is supplied. If the peer is an `lnd` node it forgets the pending channel after 10 minutes, so the whole process should take less than 10 minutes. ([source](../../raw/docs/lightning-network-tools/lnd/psbt.md))

> DO NOT PUBLISH the finished transaction yourself or with another tool. lnd must publish it in the proper funding flow order or the funds can be lost. ([source](../../raw/docs/lightning-network-tools/lnd/psbt.md))

1. Start the interactive flow: `lncli openchannel --node_key <pubkey> --local_amt 1234567 --psbt`. It prints a pending channel ID and the funding address and amount, with an example `bitcoin-cli walletcreatefundedpsbt` command, then waits for a base64 PSBT. Leave it running and use another shell.
2. Create the funding PSBT, either (a) with `bitcoin-cli walletcreatefundedpsbt [] '[{"<funding address>":0.01234567}]'`, or (b) from `v0.12.0`, with `lncli wallet psbt fund --outputs='{"<funding address>":1234567}'` on a watch-only `lnd` whose private keys live on a separate, hardened `lnd` instance.
3. Paste the unsigned PSBT into the prompt; lnd verifies it and asks for the fully signed version.
4. Sign it (for example `bitcoin-cli walletprocesspsbt <psbt>`, or `lncli wallet psbt finalize <psbt>` in the two-`lnd` model) and paste the signed PSBT. lnd publishes it and returns `funding_txid`.

([source](../../raw/docs/lightning-network-tools/lnd/psbt.md))

## Batch channel opens

The initial PSBT returned by `openchannel` can be fed into `--base_psbt` of the next `openchannel` to open several channels in one transaction; this does not work with `bitcoind`, which cannot take a partial PSBT, but `walletcreatefundedpsbt` can list several funding outputs in one call. Publishing a batch transaction too early can lose funds: if one peer times out after another channel's flow has published the shared transaction, the funds in the timed-out channel's 2-of-2 output are lost unless that peer cooperates. It is "imperative" to use `--no_publish` for every channel except the very last. ([source](../../raw/docs/lightning-network-tools/lnd/psbt.md))

The API version of the same flow: initiate the channel open with the OpenChan API (the guide links it to the OpenChannelSync reference page), specifically `lnrpc.OpenChannelRequest` (`local_funding_amount`, `node_pubkey`, `private`), a `funding_shim` of `lnrpc.PsbtShim` with an empty base PSBT and `no_publish` true. Pass each returned PSBT (`psbt_fund.psbt`) as `base_psbt` for the next channel, setting `no_publish` to false for the final one. Fund with FundPsbt, sign with signPsbt or an external wallet, then call fundingStateStep with `psbt_verify` and `skip_finalize` true for channels 1 to n-1 (each with its `pending_chan_id`), with `skip_finalize` false for the last, and finally `psbt_finalize` for the first channel with the latest PSBT. ([source](../../raw/docs/lightning-network-tools/lnd/bulk-psbt.md))

## Bulk on-chain transactions

SendMany sends one transaction with multiple outputs but cannot select inputs or be combined with a channel open. With PSBTs instead: FundPsbt with raw inputs and outputs in the `raw` field (and the `account` if spending from an external wallet or one of several imported accounts), then FinalizePsbt, signPsbt, and PublishTransaction with the raw transaction. ([source](../../raw/docs/lightning-network-tools/lnd/bulk-psbt.md))

## Key import (watch-only accounts)

As of `v0.13.0-beta`, `lnd` can import BIP-0049 and BIP-0084 extended public keys at the account path (`m/purpose'/coin_type'/account'`) or address index path as watch-only through the `WalletKit` APIs. This needs a build with the `walletrpc` tag, which release builds include by default. ([source](../../raw/docs/lightning-network-tools/lnd/key_import.md))

A new wallet has four default accounts: a custom BIP-0049 account (NP2WKH external addresses), a BIP-0084 account (P2WKH), and catch-all BIP-0049 and BIP-0084 accounts for imported keys. The catch-all accounts are named "imported" and are hidden until a key is imported into them; the spendable accounts are named "default". They are exposed through `ListAccounts`, `ImportAccount`, `ImportPublicKey` and `lncli wallet accounts` (subcommands `list`, `import`, `import-pubkey`). ([source](../../raw/docs/lightning-network-tools/lnd/key_import.md))

Account fields: `name`, `extended_public_key` (prefixes `xpub/tpub` as a catch-all, `ypub/upub` for BIP-0049, `zpub/vpub` for BIP-0084), `address_type` (`WITNESS_PUBKEY_HASH`, `NESTED_WITNESS_PUBKEY_HASH`, or `lnd`'s custom `HYBRID_NESTED_WITNESS_PUBKEY_HASH` with NP2WKH external and P2WKH change addresses), `master_key_fingerprint`, `derivation_path`, `external_key_count`, `internal_key_count` and `watch_only`. ([source](../../raw/docs/lightning-network-tools/lnd/key_import.md))

`ImportAccount` / `lncli wallet accounts import` takes `name` and `extended_public_key` (required), and optional `master_key_fingerprint`, `address_type` (only needed for legacy xpub/tpub keys) and `dry_run`, which returns the first 5 external and change addresses so you can check the derivation before importing. Events for imported keys are only detected if they happen after the import; rescans are not supported. ([source](../../raw/docs/lightning-network-tools/lnd/key_import.md))

The guide's example has a signer-only node (Alice) and a watch-only node (Bob):

```
lncli-alice wallet accounts list --name=default --address_type=p2wkh
lncli-bob wallet accounts import <vpub...> alice --dry_run
lncli-bob wallet accounts import <vpub...> alice
lncli-bob newaddress p2wkh --account=alice
lncli-bob wallet psbt fund --account=alice --outputs="{\"<address>\": 500000}" --sat_per_vbyte=1
lncli-alice wallet psbt finalize --funded_psbt="<psbt>"
```

Change addresses cannot be generated on demand; they are created when a transaction needs change. ([source](../../raw/docs/lightning-network-tools/lnd/key_import.md))

## Conflicts

- `bitcoin.active`: the wallet guide's auto-unlock examples start `lnd --bitcoin.active ...` and put `bitcoin.active=1` in the config ([source](../../raw/docs/lightning-network-tools/lnd/wallet.md)), while the sample `lnd.conf` marks `bitcoin.active` as "DEPRECATED ... This field is now ignored since only the Bitcoin chain is supported" ([source](../../raw/docs/lightning-network-tools/lnd/lnd.conf.md)).
- Imported BIP-0084 account: the key import guide describes "A catch-all BIP-0084 account where all imported BIP-0049 address keys (P2WKH addresses) exist within", naming BIP-0049 for the BIP-0084 account in the same sentence ([source](../../raw/docs/lightning-network-tools/lnd/key_import.md)).

See also: [[lnd-wallet-kit]], [[lnd-lightning]], [[lnd-signer]], [[running-lnd]], [[lnd-configuration]], [[lnd-recovery]], [[payment-channels]].
