---
title: lit firewall service
type: service
sources:
  - raw/api/api-docs/api/lit.md
  - raw/api/api-docs/api/lit/rest-endpoints.md
  - raw/api/api-docs/api/lit/firewall/list-actions.md
  - raw/api/api-docs/api/lit/firewall/privacy-map-conversion.md
updated: 2026-11-14
---

# lit firewall service (Firewall)

The REST endpoints page of [[lightning-terminal]] lists two RPCs under `/v1/firewall`: ListActions and PrivacyMapConversion. ([source](../../raw/api/api-docs/api/lit/rest-endpoints.md))

Both RPC pages give `firewall.proto` as their source. ([source](../../raw/api/api-docs/api/lit/firewall/list-actions.md), [source](../../raw/api/api-docs/api/lit/firewall/privacy-map-conversion.md))

The reference was generated automatically against commit `068c1bfa3ec8ada4f2dcdb4deab7e4cb20522dce` of the `lightninglabs/lightning-terminal` repository. ([source](../../raw/api/api-docs/api/lit.md))

Both request messages have `session_id` and `group_id` fields; on PrivacyMapConversion `session_id` is deprecated in favour of `group_id`. ([source](../../raw/api/api-docs/api/lit/firewall/list-actions.md), [source](../../raw/api/api-docs/api/lit/firewall/privacy-map-conversion.md))

See also: [[lit-sessions]], [[lit-autopilot]], [[terminal-privacy-and-security]].

## ListActions

ListActions will return a list of actions that have been performed on the node. The actions that will be persisted depends on the value of the `--firewall.request-logger.level` config option. The default value is the "interceptor" mode, which persists only the actions (with all request parameters) made with macaroons with caveats that force them to be checked by an rpc middleware interceptor. In the "all" mode all actions are persisted, but full request parameters are only stored for interceptor actions; otherwise only the URI and timestamp of the actions are stored. The "full" mode persists all request data for all actions. ([source](../../raw/api/api-docs/api/lit/firewall/list-actions.md))

- gRPC: `rpc ListActions (ListActionsRequest) returns (ListActionsResponse);`
- REST: `POST /v1/firewall/actions`
- Request message: `litrpc.ListActionsRequest`
- Response message: `litrpc.ListActionsResponse`

Request filter fields: `feature_name`, `actor_name`, `method_name`, `state` (an `ActionState`; zero returns actions for any state), `session_id`, `group_id`, `start_timestamp` (only actions created after it) and `end_timestamp` (only actions created before it). Left empty, each name or ID filter matches everything. Paging fields: `index_offset`, `max_num_actions`, `reversed` (seek backwards from the index offset) and `count_total`, which the page warns will significantly decrease the performance of the query if there are many actions in the db. ([source](../../raw/api/api-docs/api/lit/firewall/list-actions.md))

Response fields: `actions` (`Action[]`), `last_index_offset` (the index of the last item returned, usable to seek further) and `total_count` (only set if `count_total` was set in the request). ([source](../../raw/api/api-docs/api/lit/firewall/list-actions.md))

Each `litrpc.Action` has `actor_name`, `feature_name`, `trigger` (a human readable reason that the action was performed), `intent`, `structured_json_data`, `rpc_method` (the URI of the method called), `rpc_params_json` (the parameters of the method call in compact json form), `timestamp` (unix seconds at which the action was attempted), `state`, `error_reason`, `session_id` and `macaroon_identifier` (the 4 byte identifier of the macaroon used, derived from the last 4 bytes of the macaroon's root key ID). ([source](../../raw/api/api-docs/api/lit/firewall/list-actions.md))

`litrpc.ActionState` values:

| Name | Number | Meaning |
| --- | --- | --- |
| `STATE_UNKNOWN` | `0` | No state was assigned to the action. This should never be the case. |
| `STATE_PENDING` | `1` | The request came through but no response came back from the appropriate backend; the Action is either still being processed or did not successfully complete. |
| `STATE_DONE` | `2` | The action successfully completed. |
| `STATE_ERROR` | `3` | The Action did not successfully complete. |

([source](../../raw/api/api-docs/api/lit/firewall/list-actions.md))

CLI: `litcli actions`, with options `--feature`, `--actor`, `--method`, `--session_id` (hex encoded), `--start_timestamp` (default: 0), `--end_timestamp` (default: 0), `--state` (options include 'pending', 'done' and 'error'), `--index_offset` (default: 0), `--max_num_actions` (default: 0), `--oldest_first`, `--count_total` and `--group_id`. The help text adds that the group ID is the same for all sessions that have been linked, that a session with no linked sessions has a group ID equal to its session ID, and that `--group_id` is ignored if `--session_id` is set. ([source](../../raw/api/api-docs/api/lit/firewall/list-actions.md))

## PrivacyMapConversion

PrivacyMapConversion can be used map real values to their pseudo counterpart and vice versa. ([source](../../raw/api/api-docs/api/lit/firewall/privacy-map-conversion.md))

- gRPC: `rpc PrivacyMapConversion (PrivacyMapConversionRequest) returns (PrivacyMapConversionResponse);`
- REST: `POST /v1/firewall/privacy_map/convert`
- Request message: `litrpc.PrivacyMapConversionRequest`
- Response message: `litrpc.PrivacyMapConversionResponse`

Request fields: `real_to_pseudo` (if true, the input is taken as the real value and the response is the pseudo value if it exists; otherwise the input is assumed to be the pseudo value), `input`, `group_id` (the group ID under which to search for the real-pseudo pair) and `session_id` (deprecated, use `group_id`). The response has `output`, the resulting real or pseudo output. ([source](../../raw/api/api-docs/api/lit/firewall/privacy-map-conversion.md))

CLI: `litcli privacy command [command options] [arguments...]`, with subcommands `str, s` (convert a string) and `uint64, u` (convert a uint64) and options `--realtopseudo` and `--group_id`. The help text says that, to improve privacy around data sharing, channel ids, channel points and node pubkeys are obfuscated by litd through a system called the Privacy Mapper. ([source](../../raw/api/api-docs/api/lit/firewall/privacy-map-conversion.md))
