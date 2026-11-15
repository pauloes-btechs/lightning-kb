---
title: lnd wallet-kit service
type: service
sources:
  - raw/api/api-docs/api/lnd.md
  - raw/api/api-docs/api/lnd/rest-endpoints.md
  - raw/api/api-docs/api/lnd/wallet-kit/bump-fee.md
  - raw/api/api-docs/api/lnd/wallet-kit/bump-force-close-fee.md
  - raw/api/api-docs/api/lnd/wallet-kit/derive-key.md
  - raw/api/api-docs/api/lnd/wallet-kit/derive-next-key.md
  - raw/api/api-docs/api/lnd/wallet-kit/estimate-fee.md
  - raw/api/api-docs/api/lnd/wallet-kit/finalize-psbt.md
  - raw/api/api-docs/api/lnd/wallet-kit/fund-psbt.md
  - raw/api/api-docs/api/lnd/wallet-kit/get-transaction.md
  - raw/api/api-docs/api/lnd/wallet-kit/import-account.md
  - raw/api/api-docs/api/lnd/wallet-kit/import-public-key.md
  - raw/api/api-docs/api/lnd/wallet-kit/import-tapscript.md
  - raw/api/api-docs/api/lnd/wallet-kit/label-transaction.md
  - raw/api/api-docs/api/lnd/wallet-kit/lease-output.md
  - raw/api/api-docs/api/lnd/wallet-kit/list-accounts.md
  - raw/api/api-docs/api/lnd/wallet-kit/list-addresses.md
  - raw/api/api-docs/api/lnd/wallet-kit/list-leases.md
  - raw/api/api-docs/api/lnd/wallet-kit/list-sweeps.md
  - raw/api/api-docs/api/lnd/wallet-kit/list-unspent.md
  - raw/api/api-docs/api/lnd/wallet-kit/next-addr.md
  - raw/api/api-docs/api/lnd/wallet-kit/pending-sweeps.md
  - raw/api/api-docs/api/lnd/wallet-kit/publish-transaction.md
  - raw/api/api-docs/api/lnd/wallet-kit/release-output.md
  - raw/api/api-docs/api/lnd/wallet-kit/remove-transaction.md
  - raw/api/api-docs/api/lnd/wallet-kit/required-reserve.md
  - raw/api/api-docs/api/lnd/wallet-kit/send-outputs.md
  - raw/api/api-docs/api/lnd/wallet-kit/sign-message-with-addr.md
  - raw/api/api-docs/api/lnd/wallet-kit/sign-psbt.md
  - raw/api/api-docs/api/lnd/wallet-kit/submit-package.md
  - raw/api/api-docs/api/lnd/wallet-kit/verify-message-with-addr.md
  - raw/api/api-docs/api/lnd/wallet-kit/x-create-account.md
updated: 2026-11-14
---

# lnd wallet-kit service

The WalletKit service of [[lnd]] (package `walletrpc`) is documented below one RPC per section, grouped by topic. The REST endpoints page lists 30 WalletKit RPCs, all under `/v2/wallet/` ([source](../../raw/api/api-docs/api/lnd/rest-endpoints.md)).

It is defined in `walletrpc/walletkit.proto`; the reference was generated from lnd commit `895118ac4ec59e78b2c14f5b0d31ac6f862434bb` ([source](../../raw/api/api-docs/api/lnd/wallet-kit/next-addr.md)). The lnd API overview lists Service *WalletKit* (file `walletrpc/walletkit.proto`) among the experimental services, which need a compile-time flag to be active (they are active in the official release binaries) ([source](../../raw/api/api-docs/api/lnd.md)).

## Keys and addresses

### DeriveNextKey

Derives the *next* key within the given key family (account in BIP43), returning the next external child in that branch ([source](../../raw/api/api-docs/api/lnd/wallet-kit/derive-next-key.md)).

- gRPC: `rpc DeriveNextKey (KeyReq) returns (KeyDescriptor);` REST: `POST /v2/wallet/key/next`
- Request `walletrpc.KeyReq`: `key_finger_print`, `key_family`. Response `signrpc.KeyDescriptor`: `raw_key_bytes`, `key_loc`.

([source](../../raw/api/api-docs/api/lnd/wallet-kit/derive-next-key.md))

### DeriveKey

Derives an arbitrary key specified by the passed KeyLocator ([source](../../raw/api/api-docs/api/lnd/wallet-kit/derive-key.md)).

- gRPC: `rpc DeriveKey (KeyLocator) returns (KeyDescriptor);` REST: `POST /v2/wallet/key`
- Request `signrpc.KeyLocator`: `key_family`, `key_index`. Response `signrpc.KeyDescriptor`.

([source](../../raw/api/api-docs/api/lnd/wallet-kit/derive-key.md))

### NextAddr

Returns the next unused address within the wallet ([source](../../raw/api/api-docs/api/lnd/wallet-kit/next-addr.md)).

- gRPC: `rpc NextAddr (AddrRequest) returns (AddrResponse);` REST: `POST /v2/wallet/address/next`
- Request `walletrpc.AddrRequest`: `account` (default account if empty), `type` (`walletrpc.AddressType`: `UNKNOWN`, `WITNESS_PUBKEY_HASH`, `NESTED_WITNESS_PUBKEY_HASH`, `HYBRID_NESTED_WITNESS_PUBKEY_HASH`, `TAPROOT_PUBKEY`), `change`. Response `walletrpc.AddrResponse`: `addr` (bech32).

([source](../../raw/api/api-docs/api/lnd/wallet-kit/next-addr.md))

### ListAddresses

Retrieves all addresses with their balance, optionally filtered by account name ([source](../../raw/api/api-docs/api/lnd/wallet-kit/list-addresses.md)).

- gRPC: `rpc ListAddresses (ListAddressesRequest) returns (ListAddressesResponse);` REST: `GET /v2/wallet/addresses`
- Request: `account_name`, `show_custom_accounts` (returns LND's custom accounts, Purpose=1017). Response: `account_with_addresses`.

([source](../../raw/api/api-docs/api/lnd/wallet-kit/list-addresses.md))

### ImportPublicKey

Imports a public key as watch-only; it is converted into a simple address of the given type and watched on chain. For Taproot keys only the BIP-0086 style output script is watched; ImportTapscript handles more advanced outputs. Events are only detected if they happen after the import ([source](../../raw/api/api-docs/api/lnd/wallet-kit/import-public-key.md)).

- gRPC: `rpc ImportPublicKey (ImportPublicKeyRequest) returns (ImportPublicKeyResponse);` REST: `POST /v2/wallet/key/import`
- Request: `public_key`, `address_type`. Response: `status`.

([source](../../raw/api/api-docs/api/lnd/wallet-kit/import-public-key.md))

### ImportTapscript

Imports a Taproot script and internal key and adds the resulting Taproot output key as a watch-only output script. Keys imported this way currently cannot be used for funding PSBTs; only balance and UTXO tracking is supported ([source](../../raw/api/api-docs/api/lnd/wallet-kit/import-tapscript.md)).

- gRPC: `rpc ImportTapscript (ImportTapscriptRequest) returns (ImportTapscriptResponse);` REST: `POST /v2/wallet/tapscript/import`
- Request: `internal_public_key` plus one of `full_tree`, `partial_reveal`, `root_hash_only`, `full_key_only`. Response: `p2tr_address`.

([source](../../raw/api/api-docs/api/lnd/wallet-kit/import-tapscript.md))

## Accounts

### ListAccounts

Retrieves all wallet accounts, optionally filtered by name and key scope ([source](../../raw/api/api-docs/api/lnd/wallet-kit/list-accounts.md)).

- gRPC: `rpc ListAccounts (ListAccountsRequest) returns (ListAccountsResponse);` REST: `GET /v2/wallet/accounts`
- Request: `name`, `address_type`. Response: `accounts` (`Account[]`).

([source](../../raw/api/api-docs/api/lnd/wallet-kit/list-accounts.md))

### ImportAccount

Imports an account backed by an account extended public key. For BIP-0044 and BIP-0049 keys an address type must be specified. Events for derived keys are only detected if they happen after the import ([source](../../raw/api/api-docs/api/lnd/wallet-kit/import-account.md)).

- gRPC: `rpc ImportAccount (ImportAccountRequest) returns (ImportAccountResponse);` REST: `POST /v2/wallet/accounts/import`
- Request: `name`, `extended_public_key` (path form m/purpose'/coin_type'/account'), `master_key_fingerprint`, `address_type`, `dry_run`. Response: `account`, `dry_run_external_addrs`, `dry_run_internal_addrs`.

([source](../../raw/api/api-docs/api/lnd/wallet-kit/import-account.md))

### XCreateAccount

An experimental API that creates a new named account whose keys are derived from the wallet's master key; unlike ImportAccount the account is fully owned by the wallet and can sign for its outputs. It requires `i_know_what_i_am_doing` on release builds because a seed-only restore does not rediscover its funds, the wallet must be unlocked, and the call is not idempotent (check ListAccounts before retrying). Restoring requires the recorded key scope, account index and number of issued addresses, then a rescan with `--reset-wallet-transactions` ([source](../../raw/api/api-docs/api/lnd/wallet-kit/x-create-account.md)).

- gRPC: `rpc XCreateAccount (XCreateAccountRequest) returns (XCreateAccountResponse);` REST: `POST /v2/wallet/accounts/create`
- Request: `name` ("default" and "imported" are reserved), `address_type` (taproot if unset; `NESTED_WITNESS_PUBKEY_HASH` not accepted), `i_know_what_i_am_doing`. Response: `account`.

([source](../../raw/api/api-docs/api/lnd/wallet-kit/x-create-account.md))

## UTXOs and leases

### ListUnspent

Lists all wallet-spendable UTXOs with confirmations between the given minimum and maximum; by default all are listed, and `unconfirmed_only` lists only unconfirmed ones ([source](../../raw/api/api-docs/api/lnd/wallet-kit/list-unspent.md)).

- gRPC: `rpc ListUnspent (ListUnspentRequest) returns (ListUnspentResponse);` REST: `POST /v2/wallet/utxos`
- Request: `min_confs`, `max_confs`, `account`, `unconfirmed_only` (default: false). Response: `utxos`.

([source](../../raw/api/api-docs/api/lnd/wallet-kit/list-unspent.md))

### LeaseOutput

Locks an output to the given ID so it is unavailable for coin selection and returns the absolute expiration; repeated calls extend the lock, and `ReleaseOutput` unlocks early. `no_expiry` reserves an unused output without a timeout until owner release or its first confirmed spend ([source](../../raw/api/api-docs/api/lnd/wallet-kit/lease-output.md)).

- gRPC: `rpc LeaseOutput (LeaseOutputRequest) returns (LeaseOutputResponse);` REST: `POST /v2/wallet/utxos/lease`
- Request: `id` (32 random bytes, unique per application), `outpoint`, `expiration_seconds` (zero uses the default duration), `no_expiry`. Response: `expiration`, `no_expiry`.

([source](../../raw/api/api-docs/api/lnd/wallet-kit/lease-output.md))

### ReleaseOutput

Unlocks an output so it is available for coin selection if still unspent; the ID must match the one used to lock it ([source](../../raw/api/api-docs/api/lnd/wallet-kit/release-output.md)).

- gRPC: `rpc ReleaseOutput (ReleaseOutputRequest) returns (ReleaseOutputResponse);` REST: `POST /v2/wallet/utxos/release`
- Request: `id`, `outpoint`. Response: `status`.

([source](../../raw/api/api-docs/api/lnd/wallet-kit/release-output.md))

### ListLeases

Lists all currently locked UTXOs ([source](../../raw/api/api-docs/api/lnd/wallet-kit/list-leases.md)).

- gRPC: `rpc ListLeases (ListLeasesRequest) returns (ListLeasesResponse);` REST: `POST /v2/wallet/utxos/leases`
- Request: no parameters. Response: `locked_utxos` (`UtxoLease[]`).

([source](../../raw/api/api-docs/api/lnd/wallet-kit/list-leases.md))

### RequiredReserve

Returns the minimum satoshis to keep in the wallet to fee bump anchor channels; it scales with the number of public anchor channels but is capped ([source](../../raw/api/api-docs/api/lnd/wallet-kit/required-reserve.md)).

- gRPC: `rpc RequiredReserve (RequiredReserveRequest) returns (RequiredReserveResponse);` REST: `GET /v2/wallet/reserve`
- Request: `additional_public_channels`. Response: `required_reserve`.

([source](../../raw/api/api-docs/api/lnd/wallet-kit/required-reserve.md))

## Transactions

### SendOutputs

Similar to bitcoind's sendmany: creates a transaction that sends to several outputs at once ([source](../../raw/api/api-docs/api/lnd/wallet-kit/send-outputs.md)).

- gRPC: `rpc SendOutputs (SendOutputsRequest) returns (SendOutputsResponse);` REST: `POST /v2/wallet/send`
- Request: `sat_per_kw`, `outputs`, `label` (max 500 characters), `min_confs`, `spend_unconfirmed`, `coin_selection_strategy`. Response: `raw_tx`.

([source](../../raw/api/api-docs/api/lnd/wallet-kit/send-outputs.md))

### PublishTransaction

Publishes the passed transaction; once it returns without error, the wallet keeps re-broadcasting it on start up until it confirms ([source](../../raw/api/api-docs/api/lnd/wallet-kit/publish-transaction.md)).

- gRPC: `rpc PublishTransaction (Transaction) returns (PublishResponse);` REST: `POST /v2/wallet/tx`
- Request `walletrpc.Transaction`: `tx_hex` (despite the name, raw bytes, base64 over REST, not hex), `label`. Response: `publish_error` (blank on success).

([source](../../raw/api/api-docs/api/lnd/wallet-kit/publish-transaction.md))

### SubmitPackage

Submits a topologically sorted package of related transactions (parents first, child last) for atomic validation. Real package submission is only done by the bitcoind backend via `submitpackage`; btcd returns an error; neutrino broadcasts individually and returns an unverified result ([source](../../raw/api/api-docs/api/lnd/wallet-kit/submit-package.md)).

- gRPC: `rpc SubmitPackage (SubmitPackageRequest) returns (SubmitPackageResponse);` REST: `POST /v2/wallet/tx/package`
- Request: `raw_txs`, `sat_per_vbyte` (fee-rate ceiling; explicit 0 means no limit). Response: `package_msg`, `tx_results`, `replaced_transactions`.

([source](../../raw/api/api-docs/api/lnd/wallet-kit/submit-package.md))

### GetTransaction

Returns details for a transaction found in the wallet ([source](../../raw/api/api-docs/api/lnd/wallet-kit/get-transaction.md)).

- gRPC: `rpc GetTransaction (GetTransactionRequest) returns (Transaction);` REST: `GET /v2/wallet/tx`
- Request: `txid` (query). Response `lnrpc.Transaction`: `tx_hash`, `amount`, `num_confirmations`, `block_hash`, `block_height`, `time_stamp`, `total_fees`, `output_details`, `raw_tx_hex`, `label`, `previous_outpoints` and others.

([source](../../raw/api/api-docs/api/lnd/wallet-kit/get-transaction.md))

### RemoveTransaction

Removes the provided transaction from the wallet's internal transaction store ([source](../../raw/api/api-docs/api/lnd/wallet-kit/remove-transaction.md)).

- gRPC: `rpc RemoveTransaction (GetTransactionRequest) returns (RemoveTransactionResponse);` REST: `POST /v2/wallet/removetx`
- Request: `txid`. Response: `status`.

([source](../../raw/api/api-docs/api/lnd/wallet-kit/remove-transaction.md))

### LabelTransaction

Adds a label to a transaction; fails if one exists unless `overwrite` is set. Labels must not be empty and cannot exceed 500 characters ([source](../../raw/api/api-docs/api/lnd/wallet-kit/label-transaction.md)).

- gRPC: `rpc LabelTransaction (LabelTransactionRequest) returns (LabelTransactionResponse);` REST: `POST /v2/wallet/tx/label`
- Request: `txid` (little-endian bytes over gRPC), `label`, `overwrite`. Response: `status`.

([source](../../raw/api/api-docs/api/lnd/wallet-kit/label-transaction.md))

## PSBTs

### FundPsbt

Creates a fully populated PSBT with enough inputs to fund the template's outputs. The template is given as `psbt` (legacy, no coin selection when inputs are present), `coin_select` (coin selection even with inputs) or `raw`. Selected inputs are locked with an internal app ID; the caller must spend or release them ([source](../../raw/api/api-docs/api/lnd/wallet-kit/fund-psbt.md)).

- gRPC: `rpc FundPsbt (FundPsbtRequest) returns (FundPsbtResponse);` REST: `POST /v2/wallet/psbt/fund`
- Request: `psbt` / `raw` / `coin_select`, `target_conf`, `sat_per_vbyte`, `sat_per_kw`, `account`, `min_confs`, `spend_unconfirmed`, `change_type`, `coin_selection_strategy`, `max_fee_ratio`, `custom_lock_id` (exactly 32 bytes), `lock_expiration_seconds`, `input_lease_no_expiry`. Response: `funded_psbt`, `change_output_index` (-1 if no change), `locked_utxos`.

([source](../../raw/api/api-docs/api/lnd/wallet-kit/fund-psbt.md))

### SignPsbt

Signs all unsigned inputs that have the required fields; incomplete inputs are skipped. It does no coin selection, UTXO locking, validation or finalization ([source](../../raw/api/api-docs/api/lnd/wallet-kit/sign-psbt.md)).

- gRPC: `rpc SignPsbt (SignPsbtRequest) returns (SignPsbtResponse);` REST: `POST /v2/wallet/psbt/sign`
- Request: `funded_psbt`. Response: `signed_psbt`, `signed_inputs`.

([source](../../raw/api/api-docs/api/lnd/wallet-kit/sign-psbt.md))

### FinalizePsbt

Signs all wallet inputs of a fully declared PSBT; lnd must be the last signer. It does NOT publish the transaction; the caller publishes it or releases locked UTXOs on error ([source](../../raw/api/api-docs/api/lnd/wallet-kit/finalize-psbt.md)).

- gRPC: `rpc FinalizePsbt (FinalizePsbtRequest) returns (FinalizePsbtResponse);` REST: `POST /v2/wallet/psbt/finalize`
- Request: `funded_psbt`, `account`. Response: `signed_psbt`, `raw_final_tx`.

([source](../../raw/api/api-docs/api/lnd/wallet-kit/finalize-psbt.md))

## Fees and sweeps

### EstimateFee

Queries the wallet's internal fee estimator for the fee (in sat/kw) needed to reach a confirmation target ([source](../../raw/api/api-docs/api/lnd/wallet-kit/estimate-fee.md)).

- gRPC: `rpc EstimateFee (EstimateFeeRequest) returns (EstimateFeeResponse);` REST: `GET /v2/wallet/estimatefee/{conf_target}`
- Request: `conf_target` (path). Response: `sat_per_kw`, `min_relay_fee_sat_per_kw`.

([source](../../raw/api/api-docs/api/lnd/wallet-kit/estimate-fee.md))

### PendingSweeps

Returns the on-chain outputs lnd is currently trying to sweep in its central batching engine; outputs with similar fee rates are batched. Some request fields are not guaranteed to remain supported ([source](../../raw/api/api-docs/api/lnd/wallet-kit/pending-sweeps.md)).

- gRPC: `rpc PendingSweeps (PendingSweepsRequest) returns (PendingSweepsResponse);` REST: `GET /v2/wallet/sweeps/pending`
- Request: no parameters. Response: `pending_sweeps` (`PendingSweep[]`).

([source](../../raw/api/api-docs/api/lnd/wallet-kit/pending-sweeps.md))

### ListSweeps

Lists sweep transactions the node has produced; they are recorded on broadcast, so may be unconfirmed ([source](../../raw/api/api-docs/api/lnd/wallet-kit/list-sweeps.md)).

- gRPC: `rpc ListSweeps (ListSweepsRequest) returns (ListSweepsResponse);` REST: `GET /v2/wallet/sweeps`
- Request: `verbose`, `start_height` (0 = earliest, -1 = only unconfirmed). Response: `transaction_details` or `transaction_ids`.

([source](../../raw/api/api-docs/api/lnd/wallet-kit/list-sweeps.md))

### BumpFee

Sends an outpoint of an unconfirmed transaction to lnd's sweeper for fee bumping, as RBF if the input is already registered with the sweeper or CPFP if not. It can override fee rate, budget, deadline and immediacy; calling `ListSweeps` first is recommended ([source](../../raw/api/api-docs/api/lnd/wallet-kit/bump-fee.md)).

- gRPC: `rpc BumpFee (BumpFeeRequest) returns (BumpFeeResponse);` REST: `POST /v2/wallet/bumpfee`
- Request: `outpoint`, `target_conf`, `sat_per_byte` (deprecated), `force` (deprecated), `sat_per_vbyte`, `immediate`, `budget` (if unset for new inputs, 50% of the input's value), `deadline_delta`. Response: `status`.

([source](../../raw/api/api-docs/api/lnd/wallet-kit/bump-fee.md))

### BumpForceCloseFee

Bumps the fee of a channel force close; only works for channels with option_anchors ([source](../../raw/api/api-docs/api/lnd/wallet-kit/bump-force-close-fee.md)).

- gRPC: `rpc BumpForceCloseFee (BumpForceCloseFeeRequest) returns (BumpForceCloseFeeResponse);` REST: `POST /v2/wallet/BumpForceCloseFee`
- Request: `chan_point`, `deadline_delta`, `starting_feerate`, `immediate`, `budget`, `target_conf`. Response: `status`.

([source](../../raw/api/api-docs/api/lnd/wallet-kit/bump-force-close-fee.md))

## Message signing with addresses

### SignMessageWithAddr

Returns a base64 compact signature made with the private key of the given address, which must be a pure public-key lock. Supports P2WKH, NP2WKH and P2TR in addition to legacy; for P2TR an ECDSA compact signature is used ([source](../../raw/api/api-docs/api/lnd/wallet-kit/sign-message-with-addr.md)).

- gRPC: `rpc SignMessageWithAddr (SignMessageWithAddrRequest) returns (SignMessageWithAddrResponse);` REST: `POST /v2/wallet/address/signmessage`
- Request: `msg`, `addr`. Response: `signature`.

([source](../../raw/api/api-docs/api/lnd/wallet-kit/sign-message-with-addr.md))

### VerifyMessageWithAddr

Checks a base64 compact signature and that the recovered public key matches the given address; external addresses are allowed. Supported types: P2PKH, P2WKH, NP2WKH, P2TR ([source](../../raw/api/api-docs/api/lnd/wallet-kit/verify-message-with-addr.md)).

- gRPC: `rpc VerifyMessageWithAddr (VerifyMessageWithAddrRequest) returns (VerifyMessageWithAddrResponse);` REST: `POST /v2/wallet/address/verifymessage`
- Request: `msg`, `signature`, `addr`. Response: `valid`, `pubkey`.

([source](../../raw/api/api-docs/api/lnd/wallet-kit/verify-message-with-addr.md))

## Conflicts

- The XCreateAccount page says "NextAddr and NewAddress take lnrpc.AddressType, which has no HYBRID_NESTED_WITNESS_PUBKEY_HASH member" ([source](../../raw/api/api-docs/api/lnd/wallet-kit/x-create-account.md)). The NextAddr page shows `walletrpc.AddrRequest.type` as `walletrpc.AddressType`, whose enum includes `HYBRID_NESTED_WITNESS_PUBKEY_HASH` = `3` ([source](../../raw/api/api-docs/api/lnd/wallet-kit/next-addr.md)).

## Related

See also: [[lnd]], [[lnd-lightning]], [[lnd-signer]], [[lnd-watch-only]], [[lnd-wallet-unlocker]], [[lnd-wallet-and-psbt]], [[lnd-sweeper]], [[sweeping]], [[lnd-recovery]].
