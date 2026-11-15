---
title: Setting up watchtowers
type: howto
sources:
  - raw/docs/lightning-network-tools/lnd/watchtower.md
  - raw/docs/lightning-network-tools/lnd/quick-tor-setup.md
updated: 2026-11-14
---

# Setting up watchtowers

A watchtower watches a node for potential channel breaches. The functionality is bundled in [[lnd]] but must be specifically enabled, and two nodes can act as each other's watchtowers, running server and client mode at the same time. The watchtowers in this guide are altruistic: there is no compensation or incentive for them to serve your node. Ideally you run your own tower on a separate machine, network and location ([source](../../raw/docs/lightning-network-tools/lnd/watchtower.md)).

## Run a watchtower (server)

Add to `lnd.conf` and restart ([source](../../raw/docs/lightning-network-tools/lnd/watchtower.md)):

```
watchtower.active=1
```

Then view the tower's information with `lncli tower info`. The tower has its own public key, and if Tor is configured the output includes the tower's onion. If the command is not found (`No help topic for 'tower'`), make sure LND is compiled with the `watchtowerrpc` flag. Example output ([source](../../raw/docs/lightning-network-tools/lnd/watchtower.md)):

```
{
"pubkey": "02f1158dd65fb7dad3d8274e39edcb8c03ff639365884ced2f143372b5fb050bc1",
"listeners": [
     "[::]:9911"
],
"uris": [   "02f1158dd65fb7dad3d8274e39edcb8c03ff639365884ced2f143372b5fb050bc1@ddoi7crm7rhj2eyztcsv6iprclrxhmsquhaswef3xphhu2fin726w7ad.onion:9911"
]
}
```

The quick Tor guide lists `tor.watchtowerkeypath=/other/path/` among the optional Tor settings for key paths ([source](../../raw/docs/lightning-network-tools/lnd/quick-tor-setup.md)).

## Connect to a watchtower (client)

Add to `lnd.conf` and restart ([source](../../raw/docs/lightning-network-tools/lnd/watchtower.md)):

```
wtclient.active=1
```

Then add a tower by its URI ([source](../../raw/docs/lightning-network-tools/lnd/watchtower.md)):

```
lncli wtclient add 02f1158dd65fb7dad3d8274e39edcb8c03ff639365884ced2f143372b5fb050bc1@ddoi7crm7rhj2eyztcsv6iprclrxhmsquhaswef3xphhu2fin726w7ad.onion:9911
```

The `wtclient` commands also list towers, remove them, and display stats or the tower policy ([source](../../raw/docs/lightning-network-tools/lnd/watchtower.md)):

```
lncli wtclient add
lncli wtclient remove
lncli wtclient towers
lncli wtclient tower
lncli wtclient stats
lncli wtclient policy
```

The sweep fee is expressed in satoshi per vByte and set in the configuration file ([source](../../raw/docs/lightning-network-tools/lnd/watchtower.md)):

```
wtclient.sweep-fee-rate=10
```

See also: [[watchtowers]], [[lnd-watchtower]], [[lnd-watchtower-client]], [[lnd-tor-and-networking]], [[lnd-recovery]].
