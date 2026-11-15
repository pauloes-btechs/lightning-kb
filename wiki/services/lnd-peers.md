---
title: lnd peers service
type: service
sources:
  - raw/api/api-docs/api/lnd.md
  - raw/api/api-docs/api/lnd/rest-endpoints.md
  - raw/api/api-docs/api/lnd/peers/update-node-announcement.md
updated: 2026-11-14
---

# lnd peers service (Peers)

The REST endpoints page lists one `peersrpc` RPC, UpdateNodeAnnouncement. ([source](../../raw/api/api-docs/api/lnd/rest-endpoints.md)) Its page gives `peersrpc/peers.proto` as its source. ([source](../../raw/api/api-docs/api/lnd/peers/update-node-announcement.md))

The REST endpoints page lists one `peersrpc` RPC, `peersrpc.UpdateNodeAnnouncement` at `/v2/peers/nodeannouncement`. ([source](../../raw/api/api-docs/api/lnd/rest-endpoints.md))

The lnd API overview lists Service *Peers* (file: `peersrpc/peers.proto`) among the experimental services, which are subject to change and need a compile-time flag to be active (they are active in the official release binaries). The reference was generated against commit `895118ac4ec59e78b2c14f5b0d31ac6f862434bb`. ([source](../../raw/api/api-docs/api/lnd.md))

See also: [[lnd-lightning]], [[lnd-tor-and-networking]].

## UpdateNodeAnnouncement

UpdateNodeAnnouncement allows the caller to update the node parameters and broadcasts a new version of the node announcement to its peers. The lncli command is `peers updatenodeannouncement`. ([source](../../raw/api/api-docs/api/lnd/peers/update-node-announcement.md))

- gRPC: `rpc UpdateNodeAnnouncement (NodeAnnouncementUpdateRequest) returns (NodeAnnouncementUpdateResponse);`
- REST: `POST /v2/peers/nodeannouncement`
- Request: `peersrpc.NodeAnnouncementUpdateRequest`, fields `feature_updates` (`UpdateFeatureAction[]`: `action`, `feature_bit`), `color` (hex code format), `alias` and `address_updates` (`UpdateAddressAction[]`: `action`, `address`)
- Response: `peersrpc.NodeAnnouncementUpdateResponse`, field `ops` (`lnrpc.Op[]`: `entity`, `actions`)

The `peersrpc.UpdateAction` enum has `ADD` (`0`, an insertion) and `REMOVE` (`1`, a deletion). `feature_bit` takes a value of the `lnrpc.FeatureBit` enum, for example `MPP_OPT` (`17`), `ANCHORS_OPT` (`21`), `ROUTE_BLINDING_OPTIONAL` (`25`) or `AMP_OPT` (`31`). ([source](../../raw/api/api-docs/api/lnd/peers/update-node-announcement.md))
