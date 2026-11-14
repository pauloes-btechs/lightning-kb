---
name: example
description: Produce a working example for a Lightning Labs RPC or task and, where possible, run it against the Sovereign Wallet regtest harness before presenting it. Regtest only. Use for "show me how to call X", "give me a tested example", or "try this against regtest".
---
# Tested examples (regtest only)

Turn knowledge into something that runs, and say honestly whether it ran.

## 1. Build the example from the knowledge base

- `./kb graph <rpc> --json` for the service, request and response messages.
- `./kb show <path> --full` on the RPC's page for the reference code samples
  and the CLI form.
- Use only fields and flags that appear in those pages. Cite the page.

## 2. Test it, if the harness can

The only place commands may run is the regtest harness in the wallet repo:
`../sovereign-wallet/harness/regtest/docker-compose.yml` (or
`$SOVEREIGN_WALLET_DIR/harness/regtest/docker-compose.yml`). It runs
bitcoind, `lnd-alice`, `lnd-bob` and `litd`, all on regtest with throwaway
credentials.

1. Check it is up: `docker compose -f <compose file> ps`. If it is not
   running, **ask before starting it**.
2. Run lnd calls inside a container, never from the host:
   `docker compose -f <compose file> exec -T lnd-alice lncli --network=regtest <command>`
3. Read-only calls (getinfo, list*, describe*, decode*) can run without
   asking. Anything that moves funds, opens or closes channels, or changes
   node state: show the exact command and wait for a yes, even on regtest.

## 3. Report

Label the result one of:

- **TESTED**: the command, the trimmed output, the image tag from the
  compose file, and the date.
- **UNTESTED**: the reason. Loop, Pool, Faraday and standalone tapd are not
  in the harness, so their examples are UNTESTED unless the user has added
  them.

Never present an example as working when it was not run.

## Hard limits

- Never run against mainnet, testnet or signet, and never pass a
  `--network` other than `regtest`.
- Never run `lncli`, `litcli`, `tapcli`, `loop`, `pool` or `frcli` directly
  on the host; a host binary may point at a real node.
- Never read or print macaroons, seeds or wallet passwords from anywhere
  outside the harness's own `data/` folder.

## Turning a result into work (ask first, every time)

- **A task:** draft the issue text and show it. Create it with
  `gh issue create` only after a yes.
- **A code change in the wallet:** make it on a new branch in the wallet
  repo, run that repo's tests, open a pull request. Never commit to `main`
  and never merge it yourself.
