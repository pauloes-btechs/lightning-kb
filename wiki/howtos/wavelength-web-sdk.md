---
title: Wavelength on the web
type: howto
sources:
  - raw/wavelength/web/get-started/installation.md
  - raw/wavelength/web/get-started/requirements.md
  - raw/wavelength/web/get-started/cross-origin-isolation.md
  - raw/wavelength/web/get-started/hosting-runtime-assets.md
  - raw/wavelength/web/get-started/quickstart.md
  - raw/wavelength/web/get-started/run-the-demo-app.md
  - raw/wavelength/web/runtime/data-and-persistence.md
  - raw/wavelength/web/support/browser-support.md
  - raw/wavelength/web/support/demo-app.md
  - raw/wavelength/web/support/troubleshooting.md
  - raw/wavelength/integrations/react.md
updated: 2026-11-14
---

# Wavelength on the web

This page covers putting the [[wavelength]] SDK into a browser app: packages, browser and backend requirements, the COOP/COEP headers, hosting the WebAssembly runtime, a React quickstart, storage, the demo app and troubleshooting. Exact signatures for every export are on [[wavelength-sdk-reference]].

## Packages and install

For web apps the SDK ships as three npm packages: `@lightninglabs/wavelength-core` (types, the `WavelengthClient` interface, errors and enums; pulled in transitively and rarely installed directly), `@lightninglabs/wavelength-web` (the browser WASM transport, framework-agnostic, re-exports everything from `core`) and `@lightninglabs/wavelength-react` (React provider and hooks; transport-agnostic, takes an injected engine and depends only on `core`). ([source](../../raw/wavelength/web/get-started/installation.md))

React apps install the web transport plus the React bindings; vanilla JS, Vue, Svelte and other non-React frameworks install only the web transport ([source](../../raw/wavelength/web/get-started/installation.md)):

```bash
npm install @lightninglabs/wavelength-web @lightninglabs/wavelength-react
# or, without React:
npm install @lightninglabs/wavelength-web
```

`@lightninglabs/wavelength-react` declares `react` as a peer dependency with the range `^18.0.0 || ^19.0.0`, and the app must also provide `react-dom` (or the equivalent for its renderer). ([source](../../raw/wavelength/web/get-started/installation.md))

## Requirements

| Browser | Minimum version |
|---|---|
| Chrome (and Chromium-based browsers) | 100+ |
| Firefox | 110+ |
| Safari (macOS and iOS) | 16+ |

Node.js 20 or later is recommended for local development (Vite, Next.js and similar). No special build plugins are needed beyond serving the WASM runtime assets and, for worker mode, setting cross-origin isolation headers. Passkeys (WebAuthn with PRF) are optional; password-based wallets work across the whole matrix. ([source](../../raw/wavelength/web/get-started/requirements.md))

The browser support page adds per-browser passkey and storage detail: Chrome / Edge supports WebAuthn PRF passkeys from `114+ (platform authenticator + PRF extension)`; Firefox has `Limited PRF support; prefer password fallback`; Safari on macOS and on iOS / iPadOS needs `17.4+ for PRF`. All four rows list SharedArrayBuffer and OPFS persistence as `Yes, with COOP/COEP`. ([source](../../raw/wavelength/web/support/browser-support.md))

The daemon in the browser still needs reachable **Ark**, **Esplora** and (for Lightning swaps) **swap server** endpoints. Signet works out of the box with `defaultConfig('signet')`, which connects to Lightning Labs hosted gateways; presets also exist for `testnet` and `mainnet`. Mainnet needs `defaultConfig('mainnet', { allowMainnet: true })`. ([source](../../raw/wavelength/web/get-started/requirements.md))

Regtest has no `defaultConfig` preset. You start arktest, note its ports, and build the `RuntimeConfig` by hand with the insecure-transport flags. For example ([source](../../raw/wavelength/web/get-started/requirements.md)):

```ts
const config: RuntimeConfig = {
  network: 'regtest',
  arkServerAddress: 'http://127.0.0.1:7071',
  walletEsploraUrl: 'http://127.0.0.1:8501',
  swapServerAddress: 'http://127.0.0.1:10032',
  arkServerInsecure: true,
  swapServerInsecure: true,
};
```

On web, `arkServerAddress` and `swapServerAddress` must be REST URLs, and `walletEsploraUrl` is an HTTP Esplora endpoint. The web transport always rejects `arkServerTlsCertPath`. It accepts `swapServerTlsCertPath` only when `disableSwaps: true`, which suppresses every swap field. ([source](../../raw/wavelength/web/get-started/requirements.md))

## Cross-origin isolation (COOP/COEP)

The default transport runs the daemon in a Web Worker and stores encrypted wallet data in OPFS-backed SQLite. Both use `SharedArrayBuffer`, which browsers expose only on cross-origin isolated pages. Without isolation, OPFS persistence fails and the worker transport cannot start. The SDK cannot set these headers itself. Your own server has to send them on the HTML of every route that loads the wallet ([source](../../raw/wavelength/web/get-started/cross-origin-isolation.md)):

```http
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
```

`require-corp` requires every subresource to be same-origin or to opt in with `Cross-Origin-Resource-Policy: cross-origin`. You can scope the headers to wallet routes, for example with a `_headers` file on Netlify or Cloudflare Pages (`/wallet/*`). For Vite, set the headers on both `server` and `preview`. Self-host third-party fonts and scripts, because `require-corp` blocks cross-origin embeds. ([source](../../raw/wavelength/web/get-started/cross-origin-isolation.md))

```ts
const crossOriginIsolation = {
  'Cross-Origin-Opener-Policy': 'same-origin',
  'Cross-Origin-Embedder-Policy': 'require-corp',
  'Cross-Origin-Resource-Policy': 'same-origin',
};

export default defineConfig({
  server: { headers: crossOriginIsolation },
  preview: { headers: crossOriginIsolation },
});
```

`Cross-Origin-Embedder-Policy: credentialless` is an optional lighter alternative, but browsers do not support it uniformly (Safari in particular), so the SDK targets `require-corp`. To verify, run `curl -sI https://your-app.example/wallet/ | grep -i cross-origin` and check that `crossOriginIsolated` is `true` in DevTools. ([source](../../raw/wavelength/web/get-started/cross-origin-isolation.md))

If you cannot isolate the page, you can run the runtime on the main thread with `createWebClient({ runtimeThread: 'main' })`, but the requirements page says OPFS persistence will not be available and the UI thread blocks while the daemon is busy. ([source](../../raw/wavelength/web/get-started/requirements.md)) See Conflicts below.

## Hosting the runtime assets

You always host the WebAssembly runtime files yourself and point `runtimeBaseUrl` at them. The worker entry (`wavewalletdk-worker.js`) ships inside `@lightninglabs/wavelength-web` and your bundler emits it. If `runtimeBaseUrl` is unset, assets resolve relative to the page URL. `RUNTIME_ASSET_FILES` lists the files that must be served together: `wavewalletdk.wasm`, `wavewalletdk.wasm.gz`, `wasm_exec.js`, `sqlite-bridge.js`, `sqlite-worker.js`, `sqlite-node-vfs.js`, `sqlite3.js`, `sqlite3.wasm` and `sqlite3-opfs-async-proxy.js`. `RUNTIME_MANIFEST_VERSION` identifies the daemon build the SDK is paired with. ([source](../../raw/wavelength/web/get-started/hosting-runtime-assets.md))

There are two ways to get the asset set. One is to download `Wavewalletdk.wasm.tar.gz` from the paired wavelength GitHub release, which unpacks flat into your served directory. The other is to build it with `make -C /path/to/wavelength wasm-wallet` and copy the files out of `bin/wasm/`. ([source](../../raw/wavelength/web/get-started/hosting-runtime-assets.md))

```bash
BASE=https://github.com/lightninglabs/wavelength/releases/download
curl -fsSLO "$BASE/<version>/Wavewalletdk.wasm.tar.gz"
mkdir -p "./public/wavewalletdk/<version>"
tar -xzf Wavewalletdk.wasm.tar.gz -C "./public/wavewalletdk/<version>"
```

Hosting rules from the guide ([source](../../raw/wavelength/web/get-started/hosting-runtime-assets.md)):

- Host every file under one path, preferably one that includes `RUNTIME_MANIFEST_VERSION` (for example `/wavewalletdk/<version>/`). Trailing slashes are optional.
- Assets are version-locked to the daemon embedded in `@lightninglabs/wavelength-web`. When you upgrade the SDK, redeploy the matching bundle.
- The client fetches `wavewalletdk.wasm.gz` first and falls back to `wavewalletdk.wasm`, so host both. No particular compression headers are required, because the client branches on the file's magic number.
- A cross-origin `runtimeBaseUrl` needs `Cross-Origin-Resource-Policy: cross-origin` and CORS headers on the asset host.
- If you set a Content-Security-Policy, `script-src` must include `blob:` alongside `'self'`.

**Integrity verification.** Before it executes the wasm binary, `wasm_exec.js` or `sqlite-bridge.js`, the transport checks their bytes against SHA-256 digests pinned in the npm package. A mismatch fails with `asset_integrity_failed`. The sqlite worker chain is not verified at runtime. You can check it at deploy time against `RUNTIME_ASSET_DIGESTS` (SRI format `sha256-<base64>`). For a runtime built from source, set `runtimeIntegrity: false` on `createWebClient()` or `createWebWalletEngine()`. This logs a one-time console warning, and a mainnet start rejects with `invalid_config` while verification is off. ([source](../../raw/wavelength/web/get-started/hosting-runtime-assets.md))

## Quickstart (React)

The quickstart requires Node 20 or later and says no special build config is needed for Vite or Next.js. Build the engine once with `createWebWalletEngine()` and wrap the app in `WavelengthProvider`. Pass `config` and `autoStart: true` to boot the daemon as soon as the runtime is ready. ([source](../../raw/wavelength/web/get-started/quickstart.md))

```tsx
import { createWebWalletEngine, defaultConfig } from '@lightninglabs/wavelength-web';
import { WavelengthProvider, useWallet } from '@lightninglabs/wavelength-react';

const engine = createWebWalletEngine({
  runtimeBaseUrl: '/wavewalletdk/',
  config: defaultConfig('signet'),
  autoStart: true,
});
```

`defaultConfig(network, overrides?)` returns a `RuntimeConfig` preloaded with public REST gateway endpoints. Overrides are a shallow merge, so pass only top-level fields such as `dataDir`. To create a wallet, call `create({ password })` from `useWalletCreate`, which returns `{ mnemonic }`. Afterwards `phase` from `useWallet` advances (through `'syncing'` if needed) to `'ready'`. To pay, call `send({ invoice })` or `send({ onchainAddress })` from `useWalletSend`. Lightning payments go through the swap server, and on-chain sends settle through a cooperative leave with the Ark operator. ([source](../../raw/wavelength/web/get-started/quickstart.md))

Without React, create the client directly ([source](../../raw/wavelength/web/get-started/installation.md)):

```ts
const client = createWebClient({ runtimeBaseUrl: 'https://your-host/wavewalletdk/' });
await client.ready();
await client.start(defaultConfig('signet'));
```

`error` from `useWallet` holds the last fatal runtime-level error. It is set when the initial runtime load fails or when `start`/`stop` fails. ([source](../../raw/wavelength/web/get-started/installation.md))

## React integration details

`WavelengthProvider` takes a prebuilt `WalletEngine` and does not dispose it on unmount. The engine itself handles sync polling while `phase === 'syncing'`, activity-driven balance refresh, the restore readiness poll and the `'stopped'` transition on a runtime crash. Without `autoStart`, call `start()` from `useWallet()` once `phase === 'runtimeReady'`. `phase` is one of `'loading'`, `'runtimeReady'`, `'starting'`, `'needsWallet'`, `'locked'`, `'syncing'`, `'restoring'`, `'ready'`, `'stopping'`, `'stopped'` or `'error'`. ([source](../../raw/wavelength/integrations/react.md))

The hooks fall into four groups ([source](../../raw/wavelength/integrations/react.md)):

- **Shell:** `useWallet()` returns `phase`, `error`, `start` and `stop`.
- **State readers:** `useWalletInfo`, `useWalletBalance`, `useWalletActivity`, `useWalletRecovery` and `useWalletLogs`.
- **Mutations:** `useWalletCreate`, `useWalletRestore`, `useWalletUnlock`, `useWalletDeposit`, `useWalletReceive`, `useWalletPrepareSend`, `useWalletSend` and `useWalletRefresh`. Each returns verb-prefixed `<verb>Pending` / `<verb>Error` / `<verb>Data` / `reset<Verb>` fields and follows a "throw-and-capture" convention.
- **Exits:** `useWalletExit`, `useWalletExitPlan`, `useWalletSweep`, `useWalletExitBatch`, `useWalletExitStatus(outpoint, opts?)`, `useWalletExits` and `useWalletList`.

Passkeys use `useWalletPasskey(ceremony)`; on web, pass `webPasskeyCeremony` from `@lightninglabs/wavelength-web`. Both `create(appName)` and `open(credentialId?)` resolve to `{ result, credentialId }`. Persist `credentialId` so you can do scoped unlocks later. A dismissed prompt rejects with `PasskeyCancelledError`, which is not recorded into `createError`/`openError`. ([source](../../raw/wavelength/integrations/react.md))

## Data and persistence

The daemon persists encrypted seed and wallet metadata plus SQLite state for swap tracking. `swapDatabaseFileName` names the SQLite file, `disableSwaps` turns the swap subsystem off, and `dataDir` chooses an OPFS subdirectory (for example `'/my-wallet'`). `localStorage` is not available in Web Workers, so daemon state stays in OPFS. An app may still use localStorage for its own markers, such as a passkey credential id. `navigator.storage.persist()` is best-effort and does not replace backing up the recovery phrase. ([source](../../raw/wavelength/web/runtime/data-and-persistence.md))

The SDK caches the WASM binary in Cache Storage, in a bucket named `wavelength-runtime-v1-<version>` and keyed on `RUNTIME_MANIFEST_VERSION`. The cache holds one runtime at a time. The binary is around 20 MB compressed, and you should budget roughly 130 MB of origin storage for the cache. The guide puts the load time at roughly 3.2 s uncached versus around 165 ms cached on a 50 Mbps connection. Pass `runtimeCache: false` to `createWebClient` to always fetch from the network, which helps when iterating on a local daemon build. ([source](../../raw/wavelength/web/runtime/data-and-persistence.md))

`createWebClient()` accepts `runtimeThread`. The default, `'worker'`, runs the daemon in a dedicated Web Worker with OPFS storage. `'main'` runs it on the page main thread and is an escape hatch that the page describes as having "No OPFS SQLite path". Use `workerURL` to override the bundled worker. Persistence in worker mode needs four things: COOP/COEP headers, the asset set at `runtimeBaseUrl`, a secure context (HTTPS or localhost) for passkeys, and a stable `dataDir` per wallet profile. ([source](../../raw/wavelength/web/runtime/data-and-persistence.md))

## Demo app

A hosted signet demo runs at https://wavelength.lightning.engineering/demo/. The reference integration is `apps/web-wallet-demo` in the `wavelength-sdk` monorepo ([source](../../raw/wavelength/web/get-started/run-the-demo-app.md)):

```bash
git clone https://github.com/lightninglabs/wavelength-sdk.git
cd wavelength-sdk
pnpm install
pnpm build
pnpm --filter web-wallet-demo run wasm:local
pnpm --filter web-wallet-demo run dev:local
```

`dev:local` disables integrity verification (`VITE_RUNTIME_INTEGRITY=off`) because locally built assets cannot match the pinned digests. The dev server is typically at `http://localhost:5173`. For a production build, use `pnpm --filter web-wallet-demo run build:local && pnpm --filter web-wallet-demo preview`. `wasm:local` runs `make wasm-wallet` in a sibling wavelength checkout (override the location with `WAVELENGTH_DIR`) and stages the files into `public/runtime/<RUNTIME_MANIFEST_VERSION>/`. ([source](../../raw/wavelength/web/get-started/run-the-demo-app.md))

The demo exercises `WavelengthProvider` with `createWebWalletEngine()` and multiple named wallets per origin (`src/lib/walletRegistry.ts`). It also covers phase-based routing, password and passkey onboarding, and network presets for signet, testnet and regtest. Regtest is hidden unless you open the demo with `?regtest=1`. The page treats the demo as the source of truth for wiring details. Its key entry points are `src/main.tsx`, `src/App.tsx`, `src/lib/walletRegistry.ts` and `src/lib/runtime-config.ts`. ([source](../../raw/wavelength/web/support/demo-app.md))

## Troubleshooting

| Symptom / code | Fix from the guide |
|---|---|
| `asset_load_failed` | Host every file in `RUNTIME_ASSET_FILES` at one base URL and set `runtimeBaseUrl`. A 404 usually means the path or version folder is wrong. |
| `asset_integrity_failed` | Redeploy the asset set matching the SDK's `RUNTIME_MANIFEST_VERSION`, then reload. Use `runtimeIntegrity: false` only for source-built runtimes. |
| Runtime blocked by CSP | Add `blob:` to `script-src`. This surfaces as `asset_load_failed` on the main thread and as `wavelength_error` in worker mode. |
| `wallet_locked` | Another tab of the same origin is running the wallet. Ask the user to close it and offer a retry. `runtime_lock_unavailable` means the browser refused or dropped the lock request itself. |
| Not cross-origin isolated | Send COOP `same-origin`, COEP `require-corp` (plus CORP `same-origin` for your own assets) and check that `crossOriginIsolated` is `true`. |
| Passkey unsupported / PRF missing | Requires a secure context, a user-verifying platform authenticator and PRF support (Safari 17.4+, Chrome 114+). Offer a password or recovery-phrase path. |
| Connection refused | Check that the gateways are reachable from the browser and that URLs include the scheme. The demo's local regtest defaults are Ark `7071`, Esplora `8501` and swap `10032`. |
| Persistent 401 from a gateway | Restart the backend. Make sure you are hitting the REST gateway hostname (`*-rest` on public networks). It surfaces as `wavelength_error`. |
| Stale SDK code | For Vite, run `vite --force` or remove `node_modules/.vite`. For Expo/Metro, run `npx expo start --clear`. |

([source](../../raw/wavelength/web/support/troubleshooting.md))

Lightning sends are atomic swaps and can stay `pending` while the swap server waits for liquidity. Typical outbound `progress.phase` values are `waiting_for_payment`, `settling` and `confirmed`. A timeout moves the entry to `refunding` and then `refunded`, and the funds return automatically. For a stuck send, call `refresh()` or `client.list({ pendingOnly: true })`, inspect `log` events, check `swapServerAddress` and `disableSwaps`, and retry only after the previous attempt reaches `failed`/`refunded`. ([source](../../raw/wavelength/web/support/troubleshooting.md))

## Conflicts

- **Does `runtimeThread: 'main'` change storage?** The requirements page says that on the main thread "OPFS persistence will not be available" ([source](../../raw/wavelength/web/get-started/requirements.md)), and the data and persistence page lists `'main'` storage as "No OPFS SQLite path" ([source](../../raw/wavelength/web/runtime/data-and-persistence.md)). The browser support page says `runtimeThread: 'main'` "does not change the storage backend, so it is not a fallback for missing OPFS" ([source](../../raw/wavelength/web/support/browser-support.md)).

See also: [[wavelength]], [[wavelength-sdk-reference]], [[wavelength-react-native-sdk]], [[wavelength-concepts]], [[wavelength-wallet-guides]], [[wavelength-unilateral-exit]].
