---
title: Wavelength
type: component
sources:
  - raw/wavelength/introduction/the-wavelength-system.md
  - raw/wavelength/introduction/what-is-wavelength-sdk.md
  - raw/wavelength/introduction/system-architecture.md
  - raw/wavelength/agents.md
updated: 2026-11-14
---

# Wavelength

Wavelength adds self-custodial Bitcoin and Lightning payments to an app through a handful of API calls. Users get a wallet that can send and receive over the Lightning Network, and the integrator does not run a Lightning node, open channels, or source liquidity. The docs state that stablecoin support is on the way through Taproot Assets, over the same wallet surface. ([source](../../raw/wavelength/introduction/the-wavelength-system.md))

The docs say this does not replace running your own node: the fully self-sovereign path of running your own node and channels remains, and Wavelength is for those who would rather not run infrastructure at all without giving up control of their funds. ([source](../../raw/wavelength/introduction/the-wavelength-system.md))

## What you run and what is managed

You run **Wavelength**, the self-custodial client compiled from the `lightninglabs/wavelength` repository. It holds the user's keys, tracks their balance, and builds and signs their payments; everything it talks to is managed. ([source](../../raw/wavelength/introduction/the-wavelength-system.md))

| Piece | Who runs it | What it does |
| --- | --- | --- |
| Wavelength (the client) | You | Holds keys, tracks balances, builds and signs payments. Runs as an embedded SDK in a web or mobile app, as a standalone server, or as an MCP server for agents. |
| Coordination + settlement | Wavelength Operator | An Ark-like layer that batches off-chain transfers. It settles between users but never takes unilateral control of anyone's funds. |
| Liquidity via Loop | Wavelength Operator | Lightning liquidity through [[loop]], so payments route without you sourcing, funding, or managing channels. |
| The Lightning Network | Open network | Everything speaks BOLT 11, so you can pay and be paid by any wallet, exchange, or app on Lightning. |

([source](../../raw/wavelength/introduction/the-wavelength-system.md))

Users hold their own keys, and a user can always move their balance back to the Bitcoin blockchain on their own, without anyone's cooperation; the wallet exposes this through an `exit` command. See [[wavelength-unilateral-exit]]. ([source](../../raw/wavelength/introduction/the-wavelength-system.md))

Every payment sent and received is a BOLT 11 invoice (see [[lightning-invoices]]). A normal Bitcoin address only appears at the edges, when funding a wallet or moving funds back to the chain. ([source](../../raw/wavelength/introduction/the-wavelength-system.md))

## Ways to integrate

- **Embedded SDK**: runs on web (compiled to WebAssembly, in a browser tab) and on mobile (compiled into the app binary), on React Native or on native Kotlin and Swift.
- **Standalone client**: a single self-contained process driven over a gRPC and REST API (see [[wavelength-api]]).
- **For agents**: an MCP server lets an AI agent drive the wallet as typed tool calls; wallet creation and unlock stay off the agent channel, so seeds and passwords are never exposed to a model.

The docs focus on the SDK (web, React Native, native iOS and Android); the other surfaces share the same wallet commands. ([source](../../raw/wavelength/introduction/the-wavelength-system.md))

Wavelength runs on signet and testnet by default, both open to everyone. Mainnet is also open to everyone but requires an explicit opt-in. ([source](../../raw/wavelength/introduction/the-wavelength-system.md))

## The SDK packages

The Wavelength SDK is a TypeScript library for embedding a self-custodial Bitcoin, Lightning, and Ark wallet in a web or mobile app. The wallet daemon is compiled to run inside the app: to WebAssembly in the browser, and into the app binary on mobile. There is no separate process, no local socket, and no backend to operate for the wallet logic. ([source](../../raw/wavelength/introduction/what-is-wavelength-sdk.md))

| Package | Role |
| --- | --- |
| `@lightninglabs/wavelength-core` | Shared types, the WavelengthClient interface, errors, and enums. No DOM, no transport. |
| `@lightninglabs/wavelength-web` | The browser WASM transport. Framework-agnostic. Re-exports core. |
| `@lightninglabs/wavelength-react-native` | The React Native transport. The daemon is compiled into the app binary. Re-exports core. |
| `@lightninglabs/wavelength-react` | React provider and hooks. Depends on core only and takes an injected engine. |

([source](../../raw/wavelength/introduction/what-is-wavelength-sdk.md))

React is described as the primary developer experience but is not required: on web without React, install `@lightninglabs/wavelength-web`, call `createWebClient()`, and use the `WavelengthClient` methods directly. Native iOS and Android apps use the `wavelength-mobile` wrappers, which embed the same daemon behind Kotlin and Swift APIs. ([source](../../raw/wavelength/introduction/what-is-wavelength-sdk.md))

A minimal web boot sequence from the docs:

```ts
import { createWebClient, defaultConfig } from '@lightninglabs/wavelength-web';

const client = createWebClient({ runtimeBaseUrl: '/wavewalletdk/' });

await client.ready();                        // load WASM runtime
await client.start(defaultConfig('signet')); // boot daemon, connect gateways
// Show the mnemonic to the user for backup.
const { mnemonic } = await client.createWallet({ password: '…' });
```

On React Native the same sequence uses `createNativeClient()` from `@lightninglabs/wavelength-react-native`. ([source](../../raw/wavelength/introduction/what-is-wavelength-sdk.md))

## Architecture

`WavelengthClient` is the app-facing API. It is defined in `@lightninglabs/wavelength-core` and implemented by each transport. App code calls typed methods (`deposit`, `receive`, `send`, `balance`, and so on) and receives plain JavaScript objects. The React Native transport uses the daemon's native gRPC; the web transport uses REST against the embedded daemon's HTTP facade, because browsers cannot open arbitrary gRPC connections. The daemon owns local persistence (wallet database, swap state) and signing. ([source](../../raw/wavelength/introduction/system-architecture.md))

On web, the client forwards calls to the embedded daemon in a Web Worker by default, or the main thread if configured. Seed generation, signing, and wallet state live on the device (OPFS in the browser; the app data directory on React Native); user keys never leave the device. ([source](../../raw/wavelength/introduction/what-is-wavelength-sdk.md))

The daemon reaches three backend gateways configured in `RuntimeConfig`, or pre-filled by the transport's `defaultConfig(network)` presets for signet, testnet, and mainnet:

| Field | Service | Used for |
| --- | --- | --- |
| `arkServerAddress` | Ark operator and mailbox edge | Ark rounds, VTXO lifecycle, and mailbox relay for out-of-round transfers. A REST URL on web; a `host:port` gRPC address on React Native. |
| `swapServerAddress` | Swap server | Lightning-Ark atomic swaps (Lightning receive and send). A REST URL on web; a `host:port` gRPC address on React Native. |
| `walletEsploraUrl` | Esplora-compatible indexer | Chain and UTXO queries; an HTTP endpoint implementing the Esplora `/address/:addr/utxo` API. |

([source](../../raw/wavelength/introduction/system-architecture.md))

There is no separate mailbox field: mailbox traffic rides the Ark server edge. Lightning is not a fourth gateway; Lightning send and receive are swap operations through `swapServerAddress`. Setting `disableSwaps: true` suppresses the preset and any override swap fields, for apps that only need Ark and on-chain flows. ([source](../../raw/wavelength/introduction/system-architecture.md))

The architecture page describes the payment rails behind one balance and one activity stream: on-chain in through boarding (`deposit()`), Lightning receive and send as atomic swaps (`receive()`, `send({ invoice })`, or `prepareSend()`/`sendPrepared()`), on-chain out through a cooperative leave (`send({ onchainAddress })`), and unilateral exit as the emergency fallback (`getExitPlan()`, `exit()`, `exitStatus()`). Wavelength does not open Lightning channels in the browser. ([source](../../raw/wavelength/introduction/system-architecture.md))

## Building with agents

`npx skills add lightninglabs/wavelength-sdk` installs four skills: `wavelength-web`, `wavelength-react-native`, `wavelength-api`, and `wavelength-cli`. Claude Code users can use `/plugin marketplace add lightninglabs/wavelength-sdk`, and `npx skills add wavelength.lightning.engineering` also works. The GitHub install commands go live when the repository is public at launch; until then the docs-domain install is used. ([source](../../raw/wavelength/agents.md))

The docs publish `llms.txt` and `llms-full.txt`, and every page has a markdown twin at the same URL with `.md` appended. Lightning Labs does not run a hosted docs MCP server; integrators running the daemon can run `wavecli mcp serve` to start a local MCP server exposing each daemon RPC as a typed tool call (see [[wavelength-cli]]). ([source](../../raw/wavelength/agents.md))

The suggested `AGENTS.md` rules say to create the web engine with `createWebWalletEngine()` (or `createNativeWalletEngine()` on React Native) and inject it via `<WavelengthProvider engine={...}>`, to self-host the wasm runtime assets and set `runtimeBaseUrl`, and to check npm for current package versions. ([source](../../raw/wavelength/agents.md))

## Pages in this section

- [[wavelength-concepts]]: Wavelength concepts: Ark, VTXOs, balances, lifecycle
- [[wavelength-wallet-guides]]: Wavelength wallet guides: create, send, receive, restore
- [[wavelength-unilateral-exit]]: Leaving Ark: unilateral exit
- [[wavelength-web-sdk]]: Wavelength on the web
- [[wavelength-react-native-sdk]]: Wavelength for React Native
- [[wavelength-native-mobile]]: Wavelength on native iOS and Android
- [[wavelength-sdk-reference]]: Wavelength SDK packages
- [[wavelength-api]]: Wavelength remote API (gRPC and REST)
- [[wavelength-cli]]: wavecli command reference

See also: [[submarine-swaps]], [[lightning-network-overview]].
