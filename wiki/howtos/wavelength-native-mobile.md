---
title: Wavelength on native iOS and Android
type: howto
sources:
  - raw/wavelength/native-ios-android/overview.md
  - raw/wavelength/native-ios-android/architecture.md
  - raw/wavelength/native-ios-android/quickstart.md
updated: 2026-11-14
---

# Wavelength on native iOS and Android

This page is for apps written directly in Kotlin or Swift, with no React Native layer. React Native apps should use [[wavelength-react-native-sdk]] instead. ([source](../../raw/wavelength/native-ios-android/overview.md))

## What the native SDK is

The native SDK lives in the `wavelength-mobile` repository (https://github.com/lightninglabs/wavelength-mobile). It wraps the same gomobile-compiled wallet daemon that powers the React Native package ([source](../../raw/wavelength/native-ios-android/overview.md)):

- **`android/walletkit`**: a Kotlin library exposing `suspend` functions, a `Flow` for wallet activity, and typed models.
- **`ios/WalletKit`**: a Swift library built as an `actor` with `async` functions, an `AsyncThrowingStream` for activity, and `Codable` models.

Both wrap the `Wavewalletdk` bindings: `Wavewalletdk.aar` on Android and `Wavewalletdk.xcframework` on iOS. The wavelength repo builds and publishes these with each release. The whole daemon runs inside the app's process, with no separate daemon and no open network port. The repo also has one sample app per platform: Jetpack Compose on Android and SwiftUI on iOS. ([source](../../raw/wavelength/native-ios-android/overview.md))

The overview recommends the native SDK if you have an existing Kotlin or Swift app and do not want a React Native dependency, or if you want platform-native concurrency idioms. It recommends React Native if you share a TypeScript codebase or want the `wavelength-react` hooks and the shared `WalletEngine` state layer. Both paths embed the same daemon and speak the same wallet API. ([source](../../raw/wavelength/native-ios-android/overview.md))

The docs site keeps the stable material: the overview, the architecture page and the quickstart. Anything that changes with upstream releases stays canonical in the wavelength-mobile repo: the API guide (`docs/api-guide.md`), the Android workflow (`docs/android.md`) and the signet setup (`docs/signet.md`). The full gomobile facade method list is `docs/wavewalletdk_mobile.md` in the wavelength repo. ([source](../../raw/wavelength/native-ios-android/overview.md))

## Architecture

A normal `waved` deployment is a daemon process that clients reach over a gRPC socket. Here the binding instead compiles the whole daemon into a native library and starts it inside the app's process. The Go SDK boots the daemon on a background goroutine and connects to it over an in-memory gRPC channel backed by a memory buffer, not a TCP socket. The React Native transport uses the same embedding. ([source](../../raw/wavelength/native-ios-android/architecture.md))

`gomobile bind` carries only a narrow set of types, so the facade is flat. RPC verbs take JSON bytes in and return JSON bytes out, and each wrapper decodes the results with `kotlinx.serialization` (Android) or `Codable` (iOS). Neither platform needs a protobuf runtime. A few hot paths return a plain scalar instead, such as a `Long` confirmed balance. ([source](../../raw/wavelength/native-ios-android/architecture.md))

The bindings use no callbacks. `start(config)` blocks until the daemon's gRPC channel is serving, and the wrappers run it off the main thread. Unary verbs are ordinary throwing calls. Streaming uses a pull handle that the wrappers turn into a Kotlin `Flow` or a Swift `AsyncThrowingStream`. ([source](../../raw/wavelength/native-ios-android/architecture.md))

One daemon runs per process. Calling `start` a second time before `stop` throws. `stop` tears the daemon down, unblocks in-flight stream reads and resets the guard, so the app can start again after the OS suspends and resumes it. Panics do not cross the language boundary. The facade recovers panics only at `start` and at the subscription's `next`, so a panic anywhere else takes the whole app down. ([source](../../raw/wavelength/native-ios-android/architecture.md))

## Quickstart

The wrappers are not published as artifacts yet, so you work from a checkout. The fetch scripts pull the bindings from the wavelength GitHub release with the `gh` CLI, so run `gh auth login` first ([source](../../raw/wavelength/native-ios-android/quickstart.md)):

```bash
git clone https://github.com/lightninglabs/wavelength-mobile.git
cd wavelength-mobile
./scripts/fetch-aar.sh
./scripts/fetch-xcframework.sh
```

Hold one `WalletClient` for the app's lifetime, for example as an Android `ViewModel` field or a Swift `@State` value or stored property. `WalletClient` is a Swift `actor` and does not conform to `ObservableObject`, so `@StateObject` does not apply. ([source](../../raw/wavelength/native-ios-android/quickstart.md))

`start` boots the daemon and returns once it is serving. `WalletConfig.signet(...)` fills in the public signet endpoints, and you override `dataDir` per install ([source](../../raw/wavelength/native-ios-android/quickstart.md)):

```kotlin
val client = WalletClient()
client.start(WalletConfig.signet(dataDir = "${context.filesDir}/wavewalletdk"))
val res = client.createWallet(walletPassword = "my-password".toByteArray())
saveMnemonic(res.mnemonic)
// later launches:
client.unlockWallet("my-password".toByteArray())
```

```swift
let client = WalletClient()
try await client.start(.signet(dataDir: dir))
let res = try await client.createWallet(walletPassword: Data("my-password".utf8))
_ = try await client.unlockWallet(walletPassword: Data("my-password".utf8))
```

`createWallet` with an empty mnemonic generates a fresh seed and returns the words to back up. Pass an existing mnemonic to restore instead. The password encrypts the seed on disk. `getInfo` returns a snapshot with the synced block height, operator connectivity and whether the wallet is ready for signing. Poll it to show sync progress, then read `balance()` once `walletReady` is true (for example `b.confirmedSat`). ([source](../../raw/wavelength/native-ios-android/quickstart.md))

To use the wrappers in your own app, add them as local modules, because there is no published Maven artifact or remote Swift package yet. On Android, include `android/walletkit` as a Gradle module with `implementation(project(":walletkit"))`. On iOS, add `ios/WalletKit` as a local Swift package. Its `Package.swift` declares a binary target at `Frameworks/Wavewalletdk.xcframework`, which is not committed, so the fetch script must stage it first. ([source](../../raw/wavelength/native-ios-android/quickstart.md))

See also: [[wavelength]], [[wavelength-react-native-sdk]], [[wavelength-api]], [[wavelength-concepts]].
