---
title: Machine Payments Protocol
type: howto
sources:
  - raw/docs/lightning-network-tools/aperture/machine-payments-protocol.md
  - raw/docs/lightning-network-tools/aperture.md
updated: 2026-11-14
---

# Machine Payments Protocol

The Machine Payments Protocol (MPP) is a proposed protocol for machine-to-machine payments over Lightning and other payment rails. The abbreviation is not to be confused with Multi-path Payments (for those see [[multipath-payments]]). ([source](../../raw/docs/lightning-network-tools/aperture/machine-payments-protocol.md))

[[aperture]] implements both the L402 and the MPP specifications. ([source](../../raw/docs/lightning-network-tools/aperture.md))

## How it differs from L402

The guide contrasts MPP with L402 (see [[l402]] and [[macaroons]]) on three points:

| | L402 | MPP |
| --- | --- | --- |
| Payment rails | Lightning Network payments | multiple payment rails, not limited to Lightning Network payments |
| Token | macaroons | credentials, which can be for a single use or multiple uses |
| Proof of payment | payment hashes | payment receipts, issued by the service upon successful payment and passed together with the credential when requesting the resource |

([source](../../raw/docs/lightning-network-tools/aperture/machine-payments-protocol.md))

The guide refers to <https://mpp.dev/> for more on the protocol; the specification itself is not in the sources. ([source](../../raw/docs/lightning-network-tools/aperture/machine-payments-protocol.md))

## Enable MPP in Aperture

Aperture implements MPP alongside L402. To enable it, amend the `aperture.yaml` file in the authenticator and services sections. L402 and MPP may be served and authenticated in parallel. ([source](../../raw/docs/lightning-network-tools/aperture/machine-payments-protocol.md))

```yaml
authenticator:
  # Enable the Payment HTTP Authentication Scheme (MPP) alongside L402.
  # When enabled, 402 responses include both L402 and Payment challenges.
  # enablempp: true

  # Realm string used in MPP challenge headers. Defaults to the server's
  # listen address.
  # mpprealm: "api.example.com"

  # Enable MPP session intent for prepaid sessions with deposit, bearer,
  # top-up, and close operations. Requires enablempp to be true.
  # enablesessions: true

services:
   # Payment auth scheme for this service. Valid values: "l402" (default),
   # "mpp" (Payment HTTP Auth only), or "l402+mpp" (both schemes).
   # authscheme: "l402"
```

([source](../../raw/docs/lightning-network-tools/aperture/machine-payments-protocol.md))

| Key | Section | Meaning (from the sample's comments) |
| --- | --- | --- |
| `enablempp` | `authenticator` | Enables the Payment HTTP Authentication Scheme (MPP) alongside L402. When enabled, 402 responses include both L402 and Payment challenges. |
| `mpprealm` | `authenticator` | Realm string used in MPP challenge headers. Defaults to the server's listen address. |
| `enablesessions` | `authenticator` | Enables MPP session intent for prepaid sessions with deposit, bearer, top-up, and close operations. Requires `enablempp` to be true. |
| `authscheme` | per service | Payment auth scheme for the service. Valid values: `"l402"` (default), `"mpp"` (Payment HTTP Auth only), or `"l402+mpp"` (both schemes). |

([source](../../raw/docs/lightning-network-tools/aperture/machine-payments-protocol.md))

All four keys are shown commented out in the sample. ([source](../../raw/docs/lightning-network-tools/aperture/machine-payments-protocol.md))

## Related

- [[running-aperture]] for the rest of `aperture.yaml`.
- [[aperture-pricing-and-services]] for the `services:` entries that `authscheme` is added to.
