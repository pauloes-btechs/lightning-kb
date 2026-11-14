---
title: lit accounts service
type: service
sources:
  - raw/api/api-docs/api/lit.md
  - raw/api/api-docs/api/lit/rest-endpoints.md
  - raw/api/api-docs/api/lit/accounts/create-account.md
  - raw/api/api-docs/api/lit/accounts/update-account.md
  - raw/api/api-docs/api/lit/accounts/credit-account.md
  - raw/api/api-docs/api/lit/accounts/debit-account.md
  - raw/api/api-docs/api/lit/accounts/list-accounts.md
  - raw/api/api-docs/api/lit/accounts/account-info.md
  - raw/api/api-docs/api/lit/accounts/remove-account.md
  - raw/api/api-docs/api/lit/accounts/account-payments.md
  - raw/api/api-docs/api/lit/sessions/add-session.md
updated: 2026-11-14
---

# lit accounts service (Accounts)

The accounts service of [[lightning-terminal]] manages off-chain accounts: entries in litd's account database that cap how many satoshis the bearer of an account-locked macaroon can spend. ([source](../../raw/api/api-docs/api/lit/accounts/create-account.md))

The CreateAccount page gives `lit-accounts.proto` as its source. ([source](../../raw/api/api-docs/api/lit/accounts/create-account.md))

The reference was generated automatically against commit `068c1bfa3ec8ada4f2dcdb4deab7e4cb20522dce` of the `lightninglabs/lightning-terminal` repository. ([source](../../raw/api/api-docs/api/lit.md))

The REST endpoints page lists seven accounts RPCs, each with a path under `/v1/accounts`: ListAccounts, CreateAccount, CreditAccount, DebitAccount, AccountPayments, UpdateAccount and RemoveAccount. AccountInfo is not in that listing. ([source](../../raw/api/api-docs/api/lit/rest-endpoints.md))

An eighth RPC, AccountInfo, has its own reference page, which shows a gRPC signature and no REST path. ([source](../../raw/api/api-docs/api/lit/accounts/account-info.md))

The AddSession request has an `account_id` field, the ID of the account to associate the session with; it should only be set if the `session_type` is `TYPE_MACAROON_ACCOUNT`. ([source](../../raw/api/api-docs/api/lit/sessions/add-session.md))

See also: [[litd-accounts-guide]], [[lit-sessions]].

## The Account message

Several RPCs return `litrpc.Account`. Its fields are `id`, `initial_balance` (satoshis, set when the account was created), `current_balance` (satoshis), `last_update` (timestamp), `expiration_date` (timestamp; zero means it does not expire), `invoices` (`AccountInvoice[]`; an invoice created by an account will credit the account balance if it is settled), `payments` (`AccountPayment[]`; a payment made by an account will debit the account balance if it is settled) and `label` (optional; if not empty it is guaranteed to be unique). ([source](../../raw/api/api-docs/api/lit/accounts/account-info.md))

`litrpc.AccountInvoice` has one field, `hash`. `litrpc.AccountPayment` has `hash`, `state` (the state of the payment as reported by lnd) and `full_amount`: the full amount in satoshis reserved for the payment, including the routing fee estimated by the fee limit of the payment request; the actual debited amount will likely be lower if the fee is below the limit. ([source](../../raw/api/api-docs/api/lit/accounts/account-info.md))

## CreateAccount

CreateAccount adds an entry to the account database. The entry represents an amount of satoshis (account balance) that can be spent using off-chain transactions (e.g. paying invoices). Macaroons can be created to be locked to an account, so that the bearer of the macaroon can only spend at most that amount of satoshis through the daemon that has issued the macaroon. Accounts only assert a maximum amount spendable; having a certain account balance does not guarantee that the node has the channel liquidity to actually spend that amount. ([source](../../raw/api/api-docs/api/lit/accounts/create-account.md))

- gRPC: `rpc CreateAccount (CreateAccountRequest) returns (CreateAccountResponse);`
- REST: `POST /v1/accounts`
- Request message: `litrpc.CreateAccountRequest`
- Response message: `litrpc.CreateAccountResponse`

Request fields: `account_balance` (the initial account balance in satoshis representing the maximum amount that can be spent), `expiration_date` (timestamp; set to 0 to never expire) and `label` (optional; if not empty it must be unique). The response has `account` (the new `Account`) and `macaroon` (the macaroon with all permissions required to access the account). ([source](../../raw/api/api-docs/api/lit/accounts/create-account.md))

CLI: `litcli accounts create [command options] balance [expiration_date] [--label=LABEL] [--save_to=FILE]`, with options `--balance` (default: 0), `--expiration_date` (seconds since the unix epoch; 0 means it does not expire; default: 0), `--save_to` (store the account macaroon to the given file) and `--label`. ([source](../../raw/api/api-docs/api/lit/accounts/create-account.md))

## UpdateAccount

UpdateAccount updates an existing account in the account database. ([source](../../raw/api/api-docs/api/lit/accounts/update-account.md))

- gRPC: `rpc UpdateAccount (UpdateAccountRequest) returns (Account);`
- REST: `POST /v1/accounts/{id}`
- Request message: `litrpc.UpdateAccountRequest`
- Response message: `litrpc.Account`

Request fields: `id` (either the ID or the label must be set), `account_balance` (deprecated; the new account balance to set, -1 to not update the balance), `expiration_date` (the new expiry; -1 to not update the expiry, 0 to never expire), `label` (only used to identify the account) and `new_label` (the new label to set). ([source](../../raw/api/api-docs/api/lit/accounts/update-account.md))

CLI: `litcli accounts update command [command options] [id | label] [new_expiration_date]`, with options `--id`, `--label`, `--new_label` and `--new_expiration_date` (default: -1), and subcommands `credit, c` and `debit, d`. ([source](../../raw/api/api-docs/api/lit/accounts/update-account.md))

## CreditAccount

CreditAccount increases the balance of an existing account in the account database. ([source](../../raw/api/api-docs/api/lit/accounts/credit-account.md))

- gRPC: `rpc CreditAccount (CreditAccountRequest) returns (CreditAccountResponse);`
- REST: `POST /v1/accounts/credit/{account.id}`
- Request message: `litrpc.CreditAccountRequest`
- Response message: `litrpc.CreditAccountResponse`

Request fields: `account` (an `AccountIdentifier` with `id` and `label`) and `amount` (the amount by which the account's balance should be credited). The response has `account`, the credited account. CLI: `litcli accounts update credit [command options] [id | label] amount`, with options `--id`, `--label` and `--amount` (default: 0). ([source](../../raw/api/api-docs/api/lit/accounts/credit-account.md))

## DebitAccount

DebitAccount decreases the balance of an existing account in the account database. ([source](../../raw/api/api-docs/api/lit/accounts/debit-account.md))

- gRPC: `rpc DebitAccount (DebitAccountRequest) returns (DebitAccountResponse);`
- REST: `POST /v1/accounts/debit/{account.id}`
- Request message: `litrpc.DebitAccountRequest`
- Response message: `litrpc.DebitAccountResponse`

Request fields: `account` (an `AccountIdentifier`) and `amount` (the amount by which the account's balance should be debited). The response has `account`, the debited account. CLI: `litcli accounts update debit [command options] [id | label] amount`, with options `--id`, `--label` and `--amount` (default: 0). ([source](../../raw/api/api-docs/api/lit/accounts/debit-account.md))

## ListAccounts

ListAccounts returns all accounts that are currently stored in the account database. ([source](../../raw/api/api-docs/api/lit/accounts/list-accounts.md))

- gRPC: `rpc ListAccounts (ListAccountsRequest) returns (ListAccountsResponse);`
- REST: `GET /v1/accounts`
- Request message: `litrpc.ListAccountsRequest`
- Response message: `litrpc.ListAccountsResponse`

The request has no parameters. The response has `accounts`, all accounts in the account database. CLI: `litcli accounts list`. ([source](../../raw/api/api-docs/api/lit/accounts/list-accounts.md))

## AccountInfo

AccountInfo returns the account with the given ID or label. ([source](../../raw/api/api-docs/api/lit/accounts/account-info.md))

- gRPC: `rpc AccountInfo (AccountInfoRequest) returns (Account);`
- REST: none listed on the page
- Request message: `litrpc.AccountInfoRequest`
- Response message: `litrpc.Account`

Request fields: `id` and `label`; either the ID or the label must be set, and if an account has no label the ID must be used. CLI: `litcli accounts info [command options] [id | label]`, with options `--id` and `--label`. ([source](../../raw/api/api-docs/api/lit/accounts/account-info.md))

## RemoveAccount

RemoveAccount removes the given account from the account database. ([source](../../raw/api/api-docs/api/lit/accounts/remove-account.md))

- gRPC: `rpc RemoveAccount (RemoveAccountRequest) returns (RemoveAccountResponse);`
- REST: `DELETE /v1/accounts/{id}`
- Request message: `litrpc.RemoveAccountRequest`
- Response message: `litrpc.RemoveAccountResponse`

Request fields: `id` (the hexadecimal ID of the account to remove; in the REST path) and `label` (a REST query parameter); either the ID or the label must be set. The response has no parameters. CLI: `litcli accounts remove [command options] [id | label]`, with options `--id` and `--label`. ([source](../../raw/api/api-docs/api/lit/accounts/remove-account.md))

## AccountPayments

AccountPayments returns the detailed payment history for the given account. ([source](../../raw/api/api-docs/api/lit/accounts/account-payments.md))

- gRPC: `rpc AccountPayments (AccountPaymentsRequest) returns (AccountPaymentsResponse);`
- REST: `GET /v1/accounts/payments`
- Request message: `litrpc.AccountPaymentsRequest`
- Response message: `litrpc.AccountPaymentsResponse`

Request fields: `account` (an `AccountIdentifier`; in REST, `account.id` and `account.label` are query parameters), `max_payments` (if set to 0 it defaults to 20; capped at 50), `index_offset` (the row offset used as the start of the query) and `count_total_payments`. Payments are returned in ascending lexicographical order of their payment hash. ([source](../../raw/api/api-docs/api/lit/accounts/account-payments.md))

Response fields: `payments` (`Payment[]`, linked on the page as `lnrpc.Payment`), `first_index_offset`, `last_index_offset` (can be used as the `index_offset` in a subsequent query to paginate forwards) and `total_num_payments` (only set if `count_total_payments` was true in the request). ([source](../../raw/api/api-docs/api/lit/accounts/account-payments.md))

CLI: `litcli accounts payments [command options] [id | label]`, with options `--id`, `--label`, `--max_payments` (default: 20), `--index_offset` (default: 0) and `--count_total_payments`. Its description says the history is built by fetching the account's stored hashes and querying LND. ([source](../../raw/api/api-docs/api/lit/accounts/account-payments.md))

## Conflicts

- CLI command path for crediting and debiting. The `account_balance` field description on the UpdateAccount page says: "Deprecated, use the `litcli update credit` or `litcli update debit` commands instead." ([source](../../raw/api/api-docs/api/lit/accounts/update-account.md)) The CreditAccount and DebitAccount pages give the commands as `litcli accounts update credit` and `litcli accounts update debit`. ([source](../../raw/api/api-docs/api/lit/accounts/credit-account.md), [source](../../raw/api/api-docs/api/lit/accounts/debit-account.md))

## Notes

Synthesis, not from the sources: on the AccountInfo page the `id` and `label` field descriptions read "of the account to remove", the same text as on RemoveAccount, although AccountInfo only reads an account. This looks like a copied proto comment rather than a behavioural claim.
