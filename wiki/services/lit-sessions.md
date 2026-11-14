---
title: lit sessions service
type: service
sources:
  - raw/api/api-docs/api/lit.md
  - raw/api/api-docs/api/lit/rest-endpoints.md
  - raw/api/api-docs/api/lit/sessions/add-session.md
  - raw/api/api-docs/api/lit/sessions/list-sessions.md
  - raw/api/api-docs/api/lit/sessions/revoke-session.md
updated: 2026-11-14
---

# lit sessions service (Sessions)

The REST endpoints page of [[lightning-terminal]] lists three RPCs under `/v1/sessions`: AddSession, ListSessions and RevokeSession. ([source](../../raw/api/api-docs/api/lit/rest-endpoints.md))

AddSession adds and starts a new LNC session, ListSessions returns all sessions known to the session store, and RevokeSession revokes a single session. Each of the three pages gives `lit-sessions.proto` as its source. ([source](../../raw/api/api-docs/api/lit/sessions/add-session.md), [source](../../raw/api/api-docs/api/lit/sessions/list-sessions.md), [source](../../raw/api/api-docs/api/lit/sessions/revoke-session.md))

The reference was generated automatically against commit `068c1bfa3ec8ada4f2dcdb4deab7e4cb20522dce` of the `lightninglabs/lightning-terminal` repository. ([source](../../raw/api/api-docs/api/lit.md))

See also: [[lightning-node-connect]], [[lit-autopilot]], [[lit-accounts]], [[lit-firewall]].

## AddSession

AddSession adds and starts a new LNC session. ([source](../../raw/api/api-docs/api/lit/sessions/add-session.md))

- gRPC: `rpc AddSession (AddSessionRequest) returns (AddSessionResponse);`
- REST: `POST /v1/sessions`
- Request message: `litrpc.AddSessionRequest`
- Response message: `litrpc.AddSessionResponse`

Request fields:

- `label`: a user assigned label for the session.
- `session_type`: a `SessionType`, used during macaroon construction to determine how restrictive to make the macaroon and thus the session access.
- `expiry_timestamp_seconds`: the time at which the session should automatically be revoked.
- `mailbox_server_addr`: the address of the mailbox server that the LNC connection should use.
- `dev_server`: if set to true, tls will be skipped when connecting to the mailbox.
- `macaroon_custom_permissions`: `MacaroonPermission[]`, any custom permissions to add the session's macaroon.
- `account_id`: the ID of the account to associate this session with; should only be set if the `session_type` is `TYPE_MACAROON_ACCOUNT`.

The response has one field, `session`, a `litrpc.Session`. ([source](../../raw/api/api-docs/api/lit/sessions/add-session.md))

`litrpc.SessionType` values: `TYPE_MACAROON_READONLY` (0), `TYPE_MACAROON_ADMIN` (1), `TYPE_MACAROON_CUSTOM` (2), `TYPE_UI_PASSWORD` (3), `TYPE_AUTOPILOT` (4), `TYPE_MACAROON_ACCOUNT` (5). `litrpc.SessionState` values: `STATE_CREATED` (0), `STATE_IN_USE` (1), `STATE_REVOKED` (2), `STATE_EXPIRED` (3), `STATE_RESERVED` (4). ([source](../../raw/api/api-docs/api/lit/sessions/add-session.md))

A `litrpc.MacaroonPermission` has `entity` and `action`. If `entity` is set to the "uri" keyword, `action` must be a particular URI to which access should be granted, a URI regex (access is granted to each URI that matches), or the "***readonly***" keyword, which grants access to all read-only endpoints. ([source](../../raw/api/api-docs/api/lit/sessions/add-session.md))

CLI: `litcli sessions add`, with options:

- `--label`: the session label.
- `--expiry`: the number of seconds that the session should remain active (default: 7776000).
- `--mailboxserveraddr`: the host:port of the mailbox server to be used (default: "mailbox.terminal.lightning.today:443").
- `--devserver`: set to true to skip verification of the server's tls cert.
- `--type`: options include readonly|admin|account|custom (default: "readonly").
- `--uri`: a URI to include in the macaroon of a custom session; only used if `--type` is 'custom'; can be given multiple times; a regex such as '/lnrpc\..*' includes all matching URIs.
- `--permission`: a permission in the format entity:action (e.g. info:read) for a custom session; only used if `--type` is 'custom'; can be repeated, comma-separated, or mixed.
- `--account_id`: the account id for an account session; only used if `--type` is 'account'.

([source](../../raw/api/api-docs/api/lit/sessions/add-session.md))

## The Session message

`litrpc.Session` is returned by AddSession and ListSessions. Fields:

- `id`: a unique ID assigned to the session, derived from the session macaroon.
- `label`, `session_state` (`SessionState`), `session_type` (`SessionType`), `expiry_timestamp_seconds`, `mailbox_server_addr`, `dev_server`.
- `pairing_secret` and `pairing_secret_mnemonic`: the LNC pairing phrase in byte form and in mnemonic form.
- `local_public_key`: the long term, local static public key used by this node for the LNC connection.
- `remote_public_key`: the long term, remote static public key used by the remote party for the LNC connection.
- `created_at`: the time at which the session was created.
- `macaroon_recipe`: a `MacaroonRecipe` (`permissions`, `caveats`), the recipe used for creating a macaroon to use with this session.
- `account_id`: if the session is for a specific account, the account ID it is associated with.
- `autopilot_feature_info`: if the session is for Autopilot use, the set of features the session can be used for along with the rules for each feature (a map to `RulesMap`).
- `revoked_at`: the unix timestamp at which the session was revoked. The field has not been around since the beginning, so a revoked session may not have it set; readers should not assume a zero value means not revoked and should first check `session_state`.
- `group_id`: the ID of the group of Sessions this Session is linked to; if it is not linked to any older Session, this is the same as the ID.
- `feature_configs`: a map from feature name to a JSON-serialized configuration.
- `privacy_flags`: privacy flags that determine how the privacy mapper operates.

([source](../../raw/api/api-docs/api/lit/sessions/add-session.md))

## ListSessions

ListSessions returns all sessions known to the session store. ([source](../../raw/api/api-docs/api/lit/sessions/list-sessions.md))

- gRPC: `rpc ListSessions (ListSessionsRequest) returns (ListSessionsResponse);`
- REST: `GET /v1/sessions`
- Request message: `litrpc.ListSessionsRequest`
- Response message: `litrpc.ListSessionsResponse`

The request has no parameters. The response has `sessions`, a list of `Session`. CLI: `litcli sessions list command [command options] [arguments...]`, with subcommands `all, a`, `revoked, r`, `inuse, u`, `expired, e` and `created, c`. ([source](../../raw/api/api-docs/api/lit/sessions/list-sessions.md))

## RevokeSession

RevokeSession revokes a single session and also stops it if it is currently active. ([source](../../raw/api/api-docs/api/lit/sessions/revoke-session.md))

- gRPC: `rpc RevokeSession (RevokeSessionRequest) returns (RevokeSessionResponse);`
- REST: `DELETE /v1/sessions/{local_public_key}`
- Request message: `litrpc.RevokeSessionRequest`
- Response message: `litrpc.RevokeSessionResponse`

The request has one field, `local_public_key`, the local static key of the session to be revoked; when using REST, this field must be encoded as base64url. The response has no parameters. CLI: `litcli sessions revoke`, with option `--localpubkey` (the local pubkey of the session to revoke). ([source](../../raw/api/api-docs/api/lit/sessions/revoke-session.md))
