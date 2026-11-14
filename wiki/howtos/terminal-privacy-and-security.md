---
title: Terminal privacy and security
type: howto
sources:
  - raw/docs/lightning-network-tools/lightning-terminal/privacy-and-security.md
  - raw/docs/lightning-network-tools/lightning-terminal/privacy.md
  - raw/docs/lightning-network-tools/lightning-terminal/tos.md
  - raw/docs/lightning-network-tools/lightning-terminal/lnc-npm.md
  - raw/docs/lightning-network-tools/lightning-terminal/command-line-interface.md
updated: 2026-11-14
---

# Terminal privacy and security

What using [[lightning-terminal]] on the web exposes and what it does not, how to operate `litd` and the pairing phrase safely, and a summary of the Lightning Labs Privacy Policy and Terms of Use that apply to the hosted services. The summaries of the two legal documents below are abridged; read the cited sources for the full text.

## Security model

Lightning Terminal connects your browser to your node with an end-to-end encrypted connection made via a web-based proxy. The guide states that Terminal is operated in a way that Lightning Labs never has access or insight to your node. The mechanism is described in [[lightning-node-connect]]. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/privacy-and-security.md))

**Your network.** Terminal does not require modifications to the node's local network. You do not need to open additional ports or change your Tor configuration (see [[lnd-tor-and-networking]]). ([source](../../raw/docs/lightning-network-tools/lightning-terminal/privacy-and-security.md))

**litd.** The Lightning Terminal Daemon runs either on the same machine as your node or remotely on a separate machine. Access to it needs to be carefully restricted, for example by making Lightning Terminal inaccessible from the internet, choosing a secure password and running it on a device you control and trust: anybody with access to your litd instance could gain access to your Lightning node. An application's access, such as the web version of Terminal, can be revoked at any time from the litd user interface. Setup is covered in [[running-litd]]; sessions in [[lit-sessions]]. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/privacy-and-security.md))

**The pairing phrase.** litd creates a pairing phrase to connect to the web version of Terminal. It does not need to be stored anywhere. Only one concurrent connection is possible with each pairing phrase. It is communicated out of band between the machine running `litd` and your browser. Be careful where you enter it: verify you are on the correct trusted site, e.g. https://terminal.lightning.engineering/, and do not enter it into applications and sites you do not trust. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/privacy-and-security.md))

**Your browser.** Use a reputable browser that ideally updates itself regularly, and be careful with extensions that might intercept and alter content. The browser stores sensitive information, encrypted with a password of your choice. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/privacy-and-security.md))

**Phishing.** Be vigilant of phishing attacks directing you to sites attempting to steal your pairing phrase before you have connected yourself. Ideally, bookmark the page and only navigate to it using the bookmark bar. Choose a strong and unique password for Terminal, for example one created with a password manager. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/privacy-and-security.md))

**Other applications.** Lightning Node Connect is open source, so developers can build their own applications that connect to your node. All software authorized to connect to your node needs to be sufficiently trusted. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/privacy-and-security.md))

## What Lightning Labs and the proxy can see

- All connections between the node and Terminal are encrypted end-to-end; Lightning Labs can only see encrypted traffic along the route. The node's private information, such as private channel and on-chain balances, remains private.
- Lightning Labs maintains usage statistics about how many nodes are connected through Lightning Terminal, and when they last connected.
- Unless your node and browser are behind a VPN or other relay, the Terminal Proxy is able to see your IP addresses. Even if the node runs behind the Tor Socks proxy, `litd` makes an outwards connection in the clear.
- Theoretically, the proxy server could infer usage patterns from packets forwarded between node and browser, although the guide states no such information is stored or analyzed.
- Lightning Terminal uses the mempool.space API services for timestamp and fee information for the node's on-chain transactions. All calls are made from your browser and are not directly associated with your node, but, as with visiting mempool.space directly, this reveals your IP address.

([source](../../raw/docs/lightning-network-tools/lightning-terminal/privacy-and-security.md))

When enabling Autofees, channel ids, channel points and node pubkeys are obfuscated by `litd` through a system called the "Privacy Mapper". Autofees and AutoOpen, and the data each shares, are covered in [[terminal-liquidity-tools]]; the related APIs are [[lit-firewall]] and [[lit-autopilot]]. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/privacy-and-security.md))

## Privacy Policy (summary)

The policy shown in the sources is marked "Last modified: July 28, 2026". It is issued by Lightning Labs, Inc. and covers information collected through the website https://lightning.engineering, including the Terminal, Loop, Pool, and Node Assistant network access services, through electronic messages with the website, and through mobile and desktop applications downloaded from it. The website is not intended for anyone under 18 years of age. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/privacy.md))

**What is collected.** The policy lists information by which you may be personally identified, such as your IP address, an L402, public key address, and any other identifier; information that does not individually identify you, such as usage statistics regarding encrypted web traffic between users and their Lightning Network nodes; and information about your internet connection, equipment and usage details. Collection is direct (forms, correspondence, survey responses, Node Assistant chat messages), automatic (site visits, session duration, IP addresses, cookies, web beacons), and from third parties such as site analytics providers. The policy says L402s or macaroons may also be used as authentication tokens, including for purposes such as A/B testing new features. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/privacy.md))

**Third parties.** Some content or applications on the website are served by third parties, such as Google Analytics or Tag Manager, which may use cookies and other tracking technologies. The policy states "We do not sell your personal information." Personal information may be disclosed to subsidiaries and affiliates, contractors and service providers bound by confidentiality, a successor in a merger or sale, to Anthropic in connection with Node Assistant, and to comply with a court order, law or legal process. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/privacy.md))

### Node Assistant

The Terminal web application includes an AI-powered chat feature called Node Assistant, powered by Anthropic's Claude API. According to the policy:

- It is opt-in: you must affirmatively choose to enable it before any data is sent to Anthropic.
- Chat message text is transmitted through the Lightning Labs server to Anthropic's API.
- Node data needed to answer a question is first processed through a privacy obfuscation pipeline that runs entirely in the browser. It replaces node public keys, channel IDs, transaction hashes and other identifiers with randomized pseudonyms, approximates numeric amounts such as balances and fees by applying a variance of approximately five percent, and strips human-readable identifiers such as node aliases. The obfuscation is always active and cannot be disabled.
- Anthropic does not receive real node public keys, real channel IDs, exact balances or fee amounts, exact timestamps, node aliases, or any credentials or authentication material.
- The pipeline protects data retrieved from the node, not the text you type: sensitive information you include in a chat message is sent unmodified.
- Lightning Labs maintains a zero-data-retention agreement with Anthropic for Node Assistant, with two stated exceptions: retention where required by law, and, if a session is flagged for a usage policy violation, retention of inputs and outputs for up to two years.
- Conversation history and obfuscation mappings are stored only in the browser (IndexedDB) and are not accessible to Lightning Labs.
- The server acts as a stateless proxy that does not write, log, or retain chat messages, tool results, or conversation state; server-side logging captures errors and operational metrics only.

([source](../../raw/docs/lightning-network-tools/lightning-terminal/privacy.md))

**Data security and your responsibility.** The policy says security measures include ensuring that Lightning Labs does not see information such as encrypted pairing phrases and cached node aliases, and encrypting all traffic to the website in transit. A password you choose, for example where you generate an Encrypted Pairing Phrase, is stored locally on your machine, and you are principally responsible for the security of authentication credentials stored on your machine. Requests to access, correct or delete personal information go to support@lightning.engineering. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/privacy.md))

## Terms of Use (summary)

The terms shown in the sources are marked "Last Modified: December 4, 2021". They govern access to and use of the Lightning Labs website and associated network access or software services offered through https://lightning.engineering, including Lightning Terminal, Lightning Loop and Lightning Pool, and incorporate the Privacy Policy and, with respect to the Loop and Pool software, the MIT license and any other applicable open-source licenses. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/tos.md))

Points an operator is likely to care about:

- **Eligibility.** The website is offered to users who are 18 years of age or older and permitted to use it in their country of residence.
- **Network Access Fees.** Lightning Labs charges fees when you use Loop or Pool ("Network Access Fee"); the amount depends on wait time and chain fee conditions, you are notified of it at or before the time you authorize a transaction, and the fees are non-refundable.
- **Personal, non-commercial use.** The terms permit use of the website "for your personal, non-commercial use only" and say you must not access or use any part of the website or its services for commercial purposes.
- **Automated access.** You agree not to use any robot, spider, or other automatic device, process, or means to access the website for any purpose, including monitoring or copying material.
- **Trademarks.** "Lightning Labs," "LND," "Loop," and "Pool" are named as trademarks of the company.
- **Geographic restrictions.** The website is provided for use only by persons located in the United States; those accessing it from elsewhere do so on their own initiative and are responsible for compliance with local laws.
- **Warranties and liability.** The website and services are provided on an "as is" and "as available" basis, with warranties disclaimed and liability limited to the fullest extent provided by law.
- **Disputes.** New York law governs; suits are to be brought in federal or state courts located in New York County; the company may at its sole discretion require arbitration under the Rules of Arbitration of the American Arbitration Association; claims must be commenced within six (6) months after the cause of action accrues.
- **Changes.** The terms may be revised at any time and are effective immediately when posted.

([source](../../raw/docs/lightning-network-tools/lightning-terminal/tos.md))

## Conflicts

- **Restricting an application's level of access.** The privacy and security guide says: "While it will be possible in the future to restrict the level of access to your node directly in Lightning Terminal, this is not implemented as of yet" ([source](../../raw/docs/lightning-network-tools/lightning-terminal/privacy-and-security.md)). The LNC package guide says a user generating a pairing phrase "may specify limited conditions, such as 'read-only' or 'administrator'" ([source](../../raw/docs/lightning-network-tools/lightning-terminal/lnc-npm.md)), and the CLI guide says a pairing phrase created with litcli is "readonly" by default and can be changed with `--type` ([source](../../raw/docs/lightning-network-tools/lightning-terminal/command-line-interface.md)).
- **Reusing a pairing phrase.** The privacy and security guide says the pairing phrase "can be reused for another connection attempt" ([source](../../raw/docs/lightning-network-tools/lightning-terminal/privacy-and-security.md)); the under-the-hood guide's description of a single authentication attempt is recorded on [[lightning-node-connect]].
- **What Lightning Labs holds.** The security guide says Lightning Labs "only maintains usage statistics about how many nodes are connected through Lightning Terminal, and when they last connected" ([source](../../raw/docs/lightning-network-tools/lightning-terminal/privacy-and-security.md)). The Privacy Policy lists a wider set of collected information for the website as a whole, including IP addresses, L402s, public key addresses, cookies and third-party analytics ([source](../../raw/docs/lightning-network-tools/lightning-terminal/privacy.md)).
- **Contact address.** In the Privacy Policy the contact address is displayed as support@lightning.engineering while several of the underlying mail links point to hello@lightning.engineering ([source](../../raw/docs/lightning-network-tools/lightning-terminal/privacy.md)).
