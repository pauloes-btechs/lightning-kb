---
title: lnd wallet-unlocker service
type: service
sources:
  - raw/api/api-docs/api/lnd.md
  - raw/api/api-docs/api/lnd/rest-endpoints.md
  - raw/api/api-docs/api/lnd/wallet-unlocker/gen-seed.md
  - raw/api/api-docs/api/lnd/wallet-unlocker/init-wallet.md
  - raw/api/api-docs/api/lnd/wallet-unlocker/unlock-wallet.md
  - raw/api/api-docs/api/lnd/wallet-unlocker/change-password.md
updated: 2026-11-14
---

# lnd wallet-unlocker service

This page covers the WalletUnlocker service of [[lnd]]. Its four RPCs are GenSeed, InitWallet, UnlockWallet and ChangePassword, all in package `lnrpc` and exposed over REST under `/v1/` ([source](../../raw/api/api-docs/api/lnd/rest-endpoints.md)).

The service is defined in `walletunlocker.proto`; the reference was generated from lnd commit `895118ac4ec59e78b2c14f5b0d31ac6f862434bb` ([source](../../raw/api/api-docs/api/lnd/wallet-unlocker/gen-seed.md)) ([source](../../raw/api/api-docs/api/lnd.md)).

## GenSeed

GenSeed is described as the first method that should be used to instantiate a new lnd instance. It generates a new aezeed cipher seed given an optional passphrase; once the user has verified the cipherseed, InitWallet should be used to commit it and create the wallet ([source](../../raw/api/api-docs/api/lnd/wallet-unlocker/gen-seed.md)).

- gRPC: `rpc GenSeed (GenSeedRequest) returns (GenSeedResponse);`
- REST: `GET /v1/genseed`
- Request `lnrpc.GenSeedRequest`: `aezeed_passphrase` (optional, base64 over REST) and `seed_entropy` (optional 16 bytes from a CSPRNG), both as query parameters.
- Response `lnrpc.GenSeedResponse`: `cipher_seed_mnemonic` (24-word mnemonic) and `enciphered_seed` (raw aezeed cipher seed bytes).

([source](../../raw/api/api-docs/api/lnd/wallet-unlocker/gen-seed.md))

## InitWallet

InitWallet is used when lnd starts for the first time to initialize the daemon and its internal wallet. At minimum a wallet password must be provided. In a recovery scenario the aezeed mnemonic and passphrase can be supplied so the daemon uses that prior state; alternatively the seed from GenSeed is fed in after the user verifies it ([source](../../raw/api/api-docs/api/lnd/wallet-unlocker/init-wallet.md)).

- gRPC: `rpc InitWallet (InitWalletRequest) returns (InitWalletResponse);`
- REST: `POST /v1/initwallet`
- Request `lnrpc.InitWalletRequest`: `wallet_password` (must be at least 8 chars), `cipher_seed_mnemonic`, `aezeed_passphrase`, `recovery_window` (address lookahead per BIP44 branch), `channel_backups` (`ChanBackupSnapshot`), `stateless_init`, `extended_master_key`, `extended_master_key_birthday_timestamp`, `watch_only` (`WatchOnly`), `macaroon_root_key` (optional 32 bytes).
- Response `lnrpc.InitWalletResponse`: `admin_macaroon`.

([source](../../raw/api/api-docs/api/lnd/wallet-unlocker/init-wallet.md))

Field notes from the page: `stateless_init` tells the daemon not to create any `*.macaroon` files, in which case the returned `admin_macaroon` is the only copy and must be stored by the caller. `extended_master_key` is an alternative to the aezeed fields; when the birthday is unknown, `extended_master_key_birthday_timestamp` should be left at 0 and lnd scans from the first SegWit block (481824 on mainnet). `watch_only` initializes a wallet from account xpubs only, which must be run with a remote signer holding the private keys ([source](../../raw/api/api-docs/api/lnd/wallet-unlocker/init-wallet.md)). See [[lnd-watch-only]] for the remote-signer stream.

## UnlockWallet

UnlockWallet is used at startup of lnd to provide a password to unlock the wallet database ([source](../../raw/api/api-docs/api/lnd/wallet-unlocker/unlock-wallet.md)).

- gRPC: `rpc UnlockWallet (UnlockWalletRequest) returns (UnlockWalletResponse);`
- REST: `POST /v1/unlockwallet`
- Request `lnrpc.UnlockWalletRequest`: `wallet_password`, `recovery_window`, `channel_backups`, `stateless_init`.
- Response `lnrpc.UnlockWalletResponse`: no parameters.

([source](../../raw/api/api-docs/api/lnd/wallet-unlocker/unlock-wallet.md))

## ChangePassword

ChangePassword changes the password of the encrypted wallet and automatically unlocks the wallet database if successful ([source](../../raw/api/api-docs/api/lnd/wallet-unlocker/change-password.md)).

- gRPC: `rpc ChangePassword (ChangePasswordRequest) returns (ChangePasswordResponse);`
- REST: `POST /v1/changepassword`
- Request `lnrpc.ChangePasswordRequest`: `current_password`, `new_password`, `stateless_init`, `new_macaroon_root_key` (rotates the macaroon root key, invalidating all previously generated macaroons).
- Response `lnrpc.ChangePasswordResponse`: `admin_macaroon`; if both `stateless_init` and `new_macaroon_root_key` were true, this is the only copy of the macaroon from the new root key.

([source](../../raw/api/api-docs/api/lnd/wallet-unlocker/change-password.md))

## Related

See also: [[lnd]], [[lnd-lightning]], [[lnd-recovery]], [[macaroons]], [[lnd-wallet-kit]], [[lnd-signer]], [[lnd-watch-only]].
