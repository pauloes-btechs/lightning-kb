---
title: Wavelength for React Native
type: howto
sources:
  - raw/wavelength/react-native/get-started/installation.md
  - raw/wavelength/react-native/get-started/requirements.md
  - raw/wavelength/react-native/get-started/quickstart.md
  - raw/wavelength/react-native/get-started/passkey-setup.md
  - raw/wavelength/react-native/get-started/run-the-demo-app.md
  - raw/wavelength/react-native/troubleshooting.md
updated: 2026-11-14
---

# Wavelength for React Native

This page covers the React Native transport for the [[wavelength]] SDK: installing it, staging the native runtime binaries, wiring the provider, setting up passkeys, running the demo app and fixing common failures. Signatures for `createNativeWalletEngine`, `createNativePasskeyCeremony` and the hooks are on [[wavelength-sdk-reference]].

## Requirements

- React Native 0.76 or newer, with the New Architecture enabled. The package is New Architecture only and does not support the legacy architecture.
- iOS 15.1+.
- Android minSdk 24.
- Expo apps need a **development build**, not Expo Go, because the native wallet runtime is a compiled module that Expo Go cannot load.

([source](../../raw/wavelength/react-native/get-started/requirements.md))

Passkey wallets need the following. On Android: Android 9+ (API 28), Google Play services with a signed-in Google account, and a device screen lock. On iOS: iOS 18 or newer. iOS passkeys are experimental because the iOS ceremony has not been verified end to end. ([source](../../raw/wavelength/react-native/get-started/requirements.md))

Signet and testnet work out of the box over TLS with `defaultConfig('signet')` imported from `@lightninglabs/wavelength-react-native`, which presets gRPC `host:port` addresses. Mainnet uses `defaultConfig('mainnet', { allowMainnet: true })`. `walletEsploraUrl` remains an HTTP Esplora endpoint. Regtest needs a local stack on your development machine that the device or simulator can reach. ([source](../../raw/wavelength/react-native/get-started/requirements.md))

## Install

```bash
npm install @lightninglabs/wavelength-react-native @lightninglabs/wavelength-react
```

`@lightninglabs/wavelength-react-native` is the native transport: a Turbo Module wrapping the wallet runtime compiled into your app binary. It re-exports the entire `core` surface. `@lightninglabs/wavelength-react` is the transport-agnostic provider and hooks package; it takes an engine built with `createNativeWalletEngine`. `pod install` runs as part of `expo run:ios` or a standard React Native build. If it fails with a locale error, set `LANG=en_US.UTF-8`. ([source](../../raw/wavelength/react-native/get-started/installation.md))

## Stage the native runtime binaries

The npm package does not include the native binaries `Wavewalletdk.aar` and `Wavewalletdk.xcframework`. Download `Wavewalletdk.aar` and `Wavewalletdk.xcframework.tar.gz` from the wavelength release tagged with the `RUNTIME_MANIFEST_VERSION` that `@lightninglabs/wavelength-core` exports. Then stage them from `node_modules/@lightninglabs/wavelength-react-native` before running `pod install` or a Gradle build. ([source](../../raw/wavelength/react-native/get-started/installation.md))

The staging script on the installation page does four things. It extracts the xcframework into a scratch directory and rewrites the headers' `@import Foundation;` to `#import <Foundation/Foundation.h>`, because clang rejects the Objective-C modules syntax in the package's Objective-C++ glue. It copies the `.aar` into `android/libs/` and moves the framework into `ios/`. If extraction fails, it leaves the previously staged binaries in place. In an SDK repository checkout, the `bindings:fetch` script does all of this, and `bindings:local` builds the binaries from a `wavelength` source checkout. ([source](../../raw/wavelength/react-native/get-started/installation.md))

## Quickstart

Create a `WalletEngine` with `createNativeWalletEngine()` and wrap the app in `WavelengthProvider`. Pass `config` and `autoStart: true` to boot the daemon as soon as the runtime is ready. ([source](../../raw/wavelength/react-native/get-started/quickstart.md))

```tsx
import { createNativeWalletEngine, defaultConfig } from '@lightninglabs/wavelength-react-native';
import { WavelengthProvider, useWallet } from '@lightninglabs/wavelength-react';

const engine = createNativeWalletEngine({
  config: defaultConfig('signet'),
  autoStart: true,
});
```

`defaultConfig(network, overrides?)` returns a `RuntimeConfig` with public gRPC `host:port` gateway addresses. Overrides are a shallow merge of top-level fields such as `dataDir`. To create a wallet, call `create({ password })` from `useWalletCreate`, which returns `{ mnemonic }` for backup. `phase` from `useWallet` then advances to `'ready'`. To pay, call `send({ invoice })` (or `onchainAddress`) from `useWalletSend`. The native side is built by `npx expo run:android` / `npx expo run:ios`, so there is no separate pod step. ([source](../../raw/wavelength/react-native/get-started/quickstart.md))

## Passkey setup

Passkeys bind to a relying-party domain (`rpId`) that must vouch for your app. Without that association, `createNativePasskeyCeremony({ rpId })` fails with "RP ID cannot be validated". If the web app and the mobile app use the same `rpId`, the same passkey, and therefore the same wallet, works on both. ([source](../../raw/wavelength/react-native/get-started/passkey-setup.md))

- **Android:** serve `https://<rpId>/.well-known/assetlinks.json` with your package name, your signing-certificate SHA-256 fingerprint, and the relations `delegate_permission/common.handle_all_urls` and `delegate_permission/common.get_login_creds`. On the app side, declare an `asset_statements` string resource wired up through a manifest `meta-data` entry. For an Expo app, `apps/rn-wallet-demo/plugins/withAssetStatements.js` is a working example.
- **iOS (experimental):** add the Associated Domains capability (`webcredentials:<rpId>`) and serve `https://<rpId>/.well-known/apple-app-site-association` with your Team ID and bundle id. This requires iOS 18+.

`supportsPasskeyPrf()` surfaces as the `supported` flag from `useWalletPasskey`. A supported device can still decline the ceremony, and that shows up as a normal error. ([source](../../raw/wavelength/react-native/get-started/passkey-setup.md))

## Run the demo app

The reference app is `apps/rn-wallet-demo` in the `wavelength-sdk` monorepo ([source](../../raw/wavelength/react-native/get-started/run-the-demo-app.md)):

```bash
git clone https://github.com/lightninglabs/wavelength-sdk.git
cd wavelength-sdk
pnpm install
pnpm build
pnpm --filter @lightninglabs/wavelength-react-native run bindings:fetch
cd apps/rn-wallet-demo
npx expo start --dev-client --clear   # Metro, in its own terminal
pnpm run android                      # or: pnpm run ios
```

`pnpm run ios` sets `LANG=en_US.UTF-8` for `pod install` and needs no code signing. The exception is demo iOS passkey support, which is opt-in behind `WAVELENGTH_IOS_PASSKEYS=1`. The first run generates the gitignored `android/` and `ios/` projects. The start screen offers regtest, testnet and signet. For regtest, the Android emulator reaches your machine as `10.0.2.2` and the iOS simulator as `127.0.0.1`. All endpoints can be edited under "Advanced endpoints". The page says the app mirrors the web demo screen for screen. ([source](../../raw/wavelength/react-native/get-started/run-the-demo-app.md))

## Troubleshooting

| Problem | Fix |
|---|---|
| App runs old code after a native change | Restart Metro with `npx expo start --dev-client --clear` and relaunch. |
| Module fails to load in Expo Go | Use a development build (`npx expo run:android` or `npx expo run:ios`). |
| Where are runtime logs? | In the platform log (Android logcat, iOS `os_log`), not in JS-visible events or the Metro console. |
| `pod install` locale error | `LANG=en_US.UTF-8 npx expo run:ios` |
| "RP ID cannot be validated" | The relying-party domain association is missing or incomplete; see Passkey setup above. |

([source](../../raw/wavelength/react-native/troubleshooting.md))

See also: [[wavelength]], [[wavelength-web-sdk]], [[wavelength-native-mobile]], [[wavelength-sdk-reference]], [[wavelength-wallet-guides]].
