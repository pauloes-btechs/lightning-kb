---
title: lit autopilot service
type: service
sources:
  - raw/api/api-docs/api/lit.md
  - raw/api/api-docs/api/lit/rest-endpoints.md
  - raw/api/api-docs/api/lit/autopilot/list-autopilot-features.md
  - raw/api/api-docs/api/lit/autopilot/add-autopilot-session.md
  - raw/api/api-docs/api/lit/autopilot/list-autopilot-sessions.md
  - raw/api/api-docs/api/lit/autopilot/revoke-autopilot-session.md
updated: 2026-11-14
---

# lit autopilot service (Autopilot)

The REST endpoints page of [[lightning-terminal]] lists four RPCs under `/v1/autopilot`: ListAutopilotFeatures, ListAutopilotSessions, AddAutopilotSession and RevokeAutopilotSession. ([source](../../raw/api/api-docs/api/lit/rest-endpoints.md))

The ListAutopilotFeatures page gives `lit-autopilot.proto` as its source. ([source](../../raw/api/api-docs/api/lit/autopilot/list-autopilot-features.md))

The reference was generated automatically against commit `068c1bfa3ec8ada4f2dcdb4deab7e4cb20522dce` of the `lightninglabs/lightning-terminal` repository. ([source](../../raw/api/api-docs/api/lit.md))

AddAutopilotSession creates a new LNC session and attempts to register it with the Autopilot server; its response carries a `Session`. ([source](../../raw/api/api-docs/api/lit/autopilot/add-autopilot-session.md))

See also: [[lit-sessions]], [[lit-firewall]], [[terminal-liquidity-tools]].

## ListAutopilotFeatures

ListAutopilotFeatures fetches all the features supported by the Autopilot server along with the rules that we need to support in order to subscribe to those features. ([source](../../raw/api/api-docs/api/lit/autopilot/list-autopilot-features.md))

- gRPC: `rpc ListAutopilotFeatures (ListAutopilotFeaturesRequest) returns (ListAutopilotFeaturesResponse);`
- REST: `GET /v1/autopilot/features`
- Request message: `litrpc.ListAutopilotFeaturesRequest`
- Response message: `litrpc.ListAutopilotFeaturesResponse`

The request has no parameters. The response has `features`, a map of feature names to `Feature` objects. CLI: `litcli autopilot features`. ([source](../../raw/api/api-docs/api/lit/autopilot/list-autopilot-features.md))

Each `litrpc.Feature` has:

- `name` and `description`.
- `rules`: a map of rules that make sense for this feature, each a `RuleValues` with `known` (whether the user's version of Litd is aware of this rule), `defaults` (the default values the Autopilot server recommends), `min_value` and `max_value` (the minimum and maximum sane value for the rule).
- `permissions_list`: a list of URI permissions required by the feature (`Permissions`: `method`, `operations`).
- `requires_upgrade`: true if the user would need to upgrade their Litd version in order to subscribe to the feature, which is the case if the feature rules set contains a rule that Litd is unaware of.
- `default_config`: the JSON-marshaled representation of the feature's default configuration.
- `privacy_flags`: the feature may require relaxed privacy obfuscation that can be enabled with these flags.

([source](../../raw/api/api-docs/api/lit/autopilot/list-autopilot-features.md))

## Rule messages

`litrpc.RuleValue` has nine fields, listed in the table below. In a `RulesMap`, `rules` is a map of rule name to `RuleValue`, and the `RuleValue` should be parsed based on the name of the rule. ([source](../../raw/api/api-docs/api/lit/autopilot/add-autopilot-session.md))

In feature listings, the `defaults`, `min_value` and `max_value` fields of `RuleValues` are each a `RuleValue`. ([source](../../raw/api/api-docs/api/lit/autopilot/list-autopilot-features.md))

| `RuleValue` field | Message | Fields |
| --- | --- | --- |
| `rate_limit` | `RateLimit` | `read_limit`, `write_limit`, each a `Rate` with `iterations` and `num_hours` |
| `chan_policy_bounds` | `ChannelPolicyBounds` | `min_base_msat`, `max_base_msat`, `min_rate_ppm`, `max_rate_ppm`, `min_cltv_delta`, `max_cltv_delta`, `min_htlc_msat`, `max_htlc_msat` |
| `history_limit` | `HistoryLimit` | `start_time`, `duration` (set only one of the two) |
| `off_chain_budget` | `OffChainBudget` | `max_amt_msat` (excluding fees), `max_fees_msat` |
| `on_chain_budget` | `OnChainBudget` | `absolute_amt_sats` (including fees), `max_sat_per_v_byte` |
| `send_to_self` | `SendToSelf` | no parameters |
| `channel_restrict` | `ChannelRestrict` | `channel_ids`: channel IDs the Autopilot should *not* perform any actions on |
| `peer_restrict` | `PeerRestrict` | `peer_ids`: peer IDs the Autopilot should *not* perform any actions on |
| `channel_constraint` | `ChannelConstraint` | `min_capacity_sat`, `max_capacity_sat`, `max_push_sat`, `private_allowed`, `public_allowed` |

([source](../../raw/api/api-docs/api/lit/autopilot/add-autopilot-session.md))

## AddAutopilotSession

AddAutopilotSession creates a new LNC session and attempts to register it with the Autopilot server. ([source](../../raw/api/api-docs/api/lit/autopilot/add-autopilot-session.md))

- gRPC: `rpc AddAutopilotSession (AddAutopilotSessionRequest) returns (AddAutopilotSessionResponse);`
- REST: `POST /v1/autopilot/sessions`
- Request message: `litrpc.AddAutopilotSessionRequest`
- Response message: `litrpc.AddAutopilotSessionResponse`

Request fields:

- `label`: a human readable label to assign to the session.
- `expiry_timestamp_seconds`: the unix timestamp at which this session should be revoked.
- `mailbox_server_addr`: the address of the mailbox server to connect to for this session.
- `dev_server`: set to true if tls should be skipped when connecting to the mailbox.
- `features`: the features the session should subscribe to; each feature maps to a `FeatureConfig` with `rules` (a `RulesMap` that overrides the rule values recommended by the Auto Pilot server, which are used by default) and `config` (serialised configuration for the feature).
- `session_rules`: a `RulesMap` of rules that apply to the entire session; by default, no rules apply to the entire session.
- `no_privacy_mapper`: set to true if the session should not make use of the privacy mapper.
- `linked_group_id`: the ID of the group to link this session to, if any.
- `privacy_flags`: the privacy flags used by this session; if set, `privacy_flags_set` must be set.
- `privacy_flags_set`: indicates whether privacy flags are set.

The response has `session`, the `Session` that was just created. ([source](../../raw/api/api-docs/api/lit/autopilot/add-autopilot-session.md))

CLI: `litcli autopilot add`, with options:

- `--label`: the session label.
- `--expiry`: the number of seconds that the session should remain active (default: 7776000).
- `--mailboxserveraddr`: the host:port of the mailbox server to be used (default: "mailbox.terminal.lightning.today:443").
- `--devserver`: set to true to skip verification of the server's tls cert.
- `--feature`: no help text is given.
- `--group_id`: the hex encoded group ID of the session group to link this one to.
- `--feature-config`: JSON-serialized configuration with the expected format `{"version":0,"option1":"parameter1","option2":"parameter2",...}`; `{}` uses the default configuration.
- `--feature-rules`: JSON-serialized rule map; `{}` uses the default rules.
- `--privacy-flags`: string representation of privacy flags, for example "ClearPubkeys|ClearAmounts".

([source](../../raw/api/api-docs/api/lit/autopilot/add-autopilot-session.md))

The command's help text adds these rules. If one of the 'feature-' flags is set for any 'feature', that flag must be provided for each 'feature'. For a rule, all fields must be set, since unset ones are interpreted as zero values; rule values must adhere to the limits found in 'autopilot features'; if a rule is not set, default values are used. Each privacy flag removes privacy from certain aspects of messages transmitted to autopilot; the strongest privacy is on by default and an empty string means full privacy. The minimally required privacy flags of a feature are set automatically if nothing is specified. Combining several features requires the union of all the individual features' privacy flags, which is why registering each feature separately is recommended for best privacy. Linking to a previous session must preserve the privacy flags of the previous session. ([source](../../raw/api/api-docs/api/lit/autopilot/add-autopilot-session.md))

The help text's example call for AutoFees:

```
./litcli autopilot add --label=customRules \
--feature=AutoFees \
--feature-rules='{
  "rules": {
    "channel-policy-bounds":  {
      "chan_policy_bounds":  {
        "min_base_msat":  "0",
        "max_base_msat":  "10000",
        "min_rate_ppm":   10,
        "max_rate_ppm":   5000,
        "min_cltv_delta": 60,
        "max_cltv_delta": 120,
        "min_htlc_msat":  "1",
        "max_htlc_msat":  "100000000000"
      }
    },
    "peer-restriction":  {
      "peer_restrict":  {
        "peer_ids":  [
          "abcabc",
          "defdef"
        ]
      }
    }
  }
}' \
--feature-config='{}'
```

([source](../../raw/api/api-docs/api/lit/autopilot/add-autopilot-session.md))

## ListAutopilotSessions

ListAutopilotSessions lists all the sessions that are of type TypeAutopilot. ([source](../../raw/api/api-docs/api/lit/autopilot/list-autopilot-sessions.md))

- gRPC: `rpc ListAutopilotSessions (ListAutopilotSessionsRequest) returns (ListAutopilotSessionsResponse);`
- REST: `GET /v1/autopilot/sessions`
- Request message: `litrpc.ListAutopilotSessionsRequest`
- Response message: `litrpc.ListAutopilotSessionsResponse`

The request has no parameters. The response has `sessions`, a list of the Autopilot sessions (`Session[]`); the `SessionType` enum on the page includes `TYPE_AUTOPILOT` (4). CLI: `litcli autopilot list`. ([source](../../raw/api/api-docs/api/lit/autopilot/list-autopilot-sessions.md))

## RevokeAutopilotSession

RevokeAutopilotSession revokes an Autopilot session. ([source](../../raw/api/api-docs/api/lit/autopilot/revoke-autopilot-session.md))

- gRPC: `rpc RevokeAutopilotSession (RevokeAutopilotSessionRequest) returns (RevokeAutopilotSessionResponse);`
- REST: `DELETE /v1/autopilot/sessions/{local_public_key}`
- Request message: `litrpc.RevokeAutopilotSessionRequest`
- Response message: `litrpc.RevokeAutopilotSessionResponse`

The request has one field, `local_public_key`, the local static public key of the Autopilot session to be revoked; when using REST, this field must be encoded as base64url. The response has no parameters. CLI: `litcli autopilot revoke`, with option `--localpubkey` (local pubkey of the session to revoke). ([source](../../raw/api/api-docs/api/lit/autopilot/revoke-autopilot-session.md))

## Notes

Synthesis, not from the sources: this is litd's Autopilot service in the `litrpc` package; [[lnd-autopilot]] is a different service that belongs to lnd.
