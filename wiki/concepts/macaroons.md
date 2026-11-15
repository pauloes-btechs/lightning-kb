---
title: Macaroons
type: concept
sources:
  - raw/docs/the-lightning-network/l402/macaroons.md
  - raw/docs/the-lightning-network/l402.md
  - raw/docs/the-lightning-network/l402/l402.md
  - raw/docs/community-resources/glossary.md
updated: 2026-11-14
---

# Macaroons

Macaroons are an authentication mechanism for distributed systems, designed to combine the advantages of bearer and identity-based authentication systems in a single token that can quickly be issued and verified without requiring access to a central database. The glossary calls them bearer credentials that allow for detailed attenuation as well as delegation. ([source](../../raw/docs/the-lightning-network/l402/macaroons.md)) ([source](../../raw/docs/community-resources/glossary.md))

## Macaroons compared with cookies

Cookies are data, typically containing a unique identifier, and as a bearer asset the pure presence of the cookie authenticates the user. A Macaroon is at first glance also a bearer asset. Unlike a cookie, it can be validated cryptographically by the issuer, or the issuer can delegate verification to someone else. An API endpoint no longer needs to look up a cookie in a central user database before it grants access; it only requires the root keys to verify the Macaroon. ([source](../../raw/docs/the-lightning-network/l402/macaroons.md))

Macaroons can include their own permissions. The API endpoint can read these permissions, verify the Macaroon and execute the request without looking up externally whether the Macaroon is valid or what permissions it has. Macaroons can also be attenuated by the user with their own restrictions, which allows permissions and functions to be delegated safely. ([source](../../raw/docs/the-lightning-network/l402/macaroons.md))

The L402 overview adds that this makes it possible to separate the logic of issuing and verifying Macaroons, which matters for distributed systems that want to avoid, or are unable to, look up the validity and permissions of each token. ([source](../../raw/docs/the-lightning-network/l402.md))

## Use in Lightning Labs products

Macaroons are used extensively in Lightning Labs products. Together with preimages obtained through Lightning Network payments, they form the basis of L402, which is used by Lightning Pool and Lightning Loop to authenticate users. See [[l402]], [[pool]] and [[loop]]. ([source](../../raw/docs/the-lightning-network/l402/macaroons.md))

## Revocation

The main disadvantage of Macaroons over cookie or user-based authentication is that they are harder to revoke, especially in distributed systems. To revoke a Macaroon, the corresponding root key must be deleted, which also invalidates all other Macaroons signed with that key. ([source](../../raw/docs/the-lightning-network/l402/macaroons.md))

To make revocation easier, the guide recommends embedding 32-byte user identifiers in the Macaroon, as these identifiers can safely be communicated across a distributed architecture. When a Macaroon is revoked, the user identifier is marked as invalid and a new user identifier is issued. ([source](../../raw/docs/the-lightning-network/l402/macaroons.md))

## How a Macaroon is minted

At the most basic level, a cookie (`id12345678id`) becomes a Macaroon by signing it with an HMAC using a secret key known only to the issuer. The Macaroon can then be validated just by checking that the HMAC is correctly signed with the secret key. ([source](../../raw/docs/the-lightning-network/l402/macaroons.md))

More commonly, a location (for instance `api.domain.com`) and a publicly visible identifier (such as `your macaroon`) are set in addition to the cookie, and the HMAC is computed over all of them. ([source](../../raw/docs/the-lightning-network/l402/macaroons.md))

To further amend or restrict a Macaroon, a "caveat" is added, which is a further restriction or attribute. It is appended in a line below, and the output of the existing HMAC is used as the key to another HMAC function. This can be done by anyone in possession of the Macaroon. The guide's example caveat is `expires:2023-12-31`. ([source](../../raw/docs/the-lightning-network/l402/macaroons.md))

Only each line with caveats and the final HMAC need to be included in the Macaroon. The verifying service calculates the HMACs line by line and checks that the final value matches the one provided by the user, which tells it the Macaroon is valid and which caveats to apply. Whether the request conforms with the Macaroon has to be checked separately. Such a chain of caveats can be almost endlessly extended. ([source](../../raw/docs/the-lightning-network/l402/macaroons.md))

The guide's example of a Lightning Loop Macaroon ([source](../../raw/docs/the-lightning-network/l402/macaroons.md)):

```
identifier:
version = 0
user_id = fed74b3ef24820f440601eff5bfb42bef4d615c4948cec8aca3cb15bd23f1013
payment_hash = 163102a9c88fa4ec9ac9937b6f070bc3e27249a81ad7a05f398ac5d7d16f7bea
caveats:
services = lightning_loop:0
lightning_loop_capabilities = loop_out,loop_in
loop_out_monthly_volume_sats = 200000000
```

The meaning of each identifier field and caveat is given on [[l402]]. ([source](../../raw/docs/the-lightning-network/l402/macaroons.md))

## Delegation

Macaroons can be used to delegate permissions. For example, Loop could issue a Macaroon to an exchange, which could apply further restrictions before handing it to the end users, who can present it to Loop. ([source](../../raw/docs/the-lightning-network/l402/macaroons.md))

## Third-party caveats

Macaroons can also include third-party caveats, which require some interaction with a third party to obtain an additional secret that completes the Macaroon. The guide describes L402s as a form of such caveats: Macaroons that are only complete upon paying an attached Lightning Network invoice. ([source](../../raw/docs/the-lightning-network/l402/macaroons.md))

## Conflicts

- The example Loop Macaroon on the Macaroons page has `loop_out_monthly_volume_sats = 200000000`. ([source](../../raw/docs/the-lightning-network/l402/macaroons.md)) The L402 page uses the same `user_id` and `payment_hash` values in its examples but gives the constraint as `loop_out_monthly_volume_sats = 2000000`, described as "two million satoshis per month". ([source](../../raw/docs/the-lightning-network/l402/l402.md)) Both are illustrative values; the sources do not say which is intended.

See also: [[l402]], [[aperture]], [[lnd-macaroons]], [[glossary]].
