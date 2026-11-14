---
title: Using litd accounts
type: howto
sources:
  - raw/docs/lightning-network-tools/lightning-terminal/accounts.md
updated: 2026-11-14
---

# Using litd accounts

LND Accounts let you create custodial accounts on top of your LND node, enforced with custom macaroons. Using litd (see [[lightning-terminal]]), users can create virtual off-chain accounts on top of their LND node, each with its own macaroon (see [[macaroons]]) and spending rules, such as spending limits or an expiration date. The gRPC service behind the feature is described in [[lit-accounts]]. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/accounts.md))

## Trust model and limits

The accounts feature does not validate whether the sum of all account balances is smaller than or equal to the channel balance held in the underlying LND node. A user issued such an account enters a trust relationship with the node operator regarding availability of the funds and the node. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/accounts.md))

To expose accounts via the gRPC interface, the RPC Middleware Interceptor (see [[lnd-interceptors]]) is used together with individually baked macaroons for each account, which allows the feature to be integrated into existing gRPC-based applications. Enabling the interceptor for a remote LND is covered in [[running-litd]]. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/accounts.md))

At this point, it is not possible to pay invoices between two accounts using the same LND node. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/accounts.md))

## Rules enforced on an account macaroon

When an account-restricted macaroon is used, the RPC middleware interceptor enforces the following rules on the RPC interface:

- Any payment made by the account is deducted from the account's virtual balance (the full amount, including off-chain routing fees).
- If a payment (or the sum of multiple in-flight payments) exceeds the account's virtual balance, it is denied.
- The on-chain balance of any RPC responses such as the `WalletBalance` RPC is always shown as `0`, since an account can only spend off-chain balances.
- The off-chain balance (e.g. the response returned by the `ChannelBalance` RPC) always reflects the account's virtual balance and not the node's overall channel balance, and any remote balances are always shown as `0`.
- The list of active/pending/closed channels is always returned empty.
- The list of payments and invoices is filtered to only return payments/invoices created or paid by the account.
- Invoices created by an account are mapped to that account. If/when such a mapped invoice is paid, the amount is credited to that account's virtual balance.

([source](../../raw/docs/lightning-network-tools/lightning-terminal/accounts.md))

## Use cases

- **The community model:** a tech-savvy community member operates the node, manages its liquidity and provides the capital for channels, and onboards others by creating an account, locking a macaroon to it and scanning a QR code with an app like Zeus on the member's smartphone.
- **"Spend up to a certain amount automatically":** a browser extension like Alby is allowed to pay paywall invoices up to a certain amount per month, enforced by the account. An account can be shared between extensions installed in different browsers.
- **The "allowance" model:** a parent creates an account over the allowance amount and tops it up each week/month.
- **The "enhanced security" model:** a service running multiple applications on a single LND node limits the damage from a single faulty application.

([source](../../raw/docs/lightning-network-tools/lightning-terminal/accounts.md))

## Create an account

The node operator (with access to `litd` using `litcli`, or gRPC via the lit.macaroon) creates an account, here with 50,000 satoshis:

```
litcli accounts create 50000 --save_to /tmp/user.macaroon
```

The `user.macaroon` can then be passed to the user. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/accounts.md))

An account can also be created from the litd user interface: create a new session under "Lightning Node Connect," give it a name, select "Custom" under permissions, then choose "Custodial Account" in the next window. This creates a custom pairing phrase that can be passed to wallets like Alby or Zeus. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/accounts.md))

## Use the macaroon

The user or application can use the macaroon to make calls to LND's gRPC interface as they otherwise would, for example via LNDconnect (as used by Zeus Wallet), lncli, Alby or an LNbits installation:

```
lncli --macaroonpath=/tmp/user.macaroon channelbalance
```

The permissions of the macaroon can be inspected with lncli:

```
lncli printmacaroon --macaroon_file /tmp/user.macaroon
```

In the guide's example output the macaroon has the permissions `info:read`, `invoices:read`, `invoices:write`, `offchain:read`, `offchain:write` and `onchain:read`, and the caveat `lnd-custom account d64dbc31b28edf66`. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/accounts.md))

## Create an LNC session for an account

Because litd creates and manages accounts, access to an account can be granted using a [[lightning-node-connect]] pairing phrase, removing the need for the LND node to be directly accessible from the web. LNC sessions can be created for specific accounts, which is useful when connecting external wallets to that account, and multiple LNC sessions can be created for the same account. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/accounts.md))

First obtain the account ID, either from a macaroon as above or with `litcli accounts list`. Then:

```
litcli sessions add --label pointofsale --type account --account_id d64dbc31b28edf66
```

This returns all relevant information, most importantly the mnemonic required to connect. The session API is described in [[lit-sessions]]. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/accounts.md))

## Recreate an account macaroon

If you have lost access to an account macaroon, or need to issue a new one:

1. Get the account ID with `litcli accounts list`; IDs look like `07a4a3d12462b52e`.
2. Bake a generic macaroon with the minimal permissions required and save it:

   ```
   lncli bakemacaroon info:read invoices:read invoices:write offchain:read offchain:write onchain:read peers:read --save_to tmp.macaroon
   ```
3. Add a custom caveat that makes the macaroon useful only for that account:

   ```
   lncli constrainmacaroon --custom_caveat_name account --custom_caveat_condition 07a4a3d12462b52e tmp.macaroon accounts.macaroon
   ```
4. Delete the temporary macaroon: `rm tmp.macaroon`
5. Inspect the permissions with `lncli printmacaroon`, then test with a call to LND using the restricted macaroon. The `getinfo` command should return zero channels, while the `channelbalance` command should only return the balance associated with that account:

   ```
   lncli --macaroonpath accounts.macaroon getinfo
   ```

([source](../../raw/docs/lightning-network-tools/lightning-terminal/accounts.md))

Baking and constraining macaroons in lnd generally is covered in [[lnd-macaroons]].

## Conflicts

- **Who enforces balances.** The guide says "The account balances are tracked and enforced by LND", and also that litd is used to create and manage accounts and that the RPC middleware interceptor enforces the account rules on the RPC interface ([source](../../raw/docs/lightning-network-tools/lightning-terminal/accounts.md)).
- **Macaroon file name in the recreate steps.** The steps write the constrained macaroon to `accounts.macaroon`, but the inspection command shown is `lncli printmacaroon --macaroon_file zeus.macaroon` ([source](../../raw/docs/lightning-network-tools/lightning-terminal/accounts.md)).
- **Permission sets.** The example macaroon produced by `litcli accounts create` lists six permissions, while the recreate steps bake those six plus `peers:read` and call them "the minimal permissions required" ([source](../../raw/docs/lightning-network-tools/lightning-terminal/accounts.md)).
