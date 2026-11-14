---
title: Lightning Node Connect
type: howto
sources:
  - raw/docs/lightning-network-tools/lightning-terminal/lightning-node-connect.md
  - raw/docs/lightning-network-tools/lightning-terminal/lnc-npm.md
  - raw/docs/lightning-network-tools/lightning-terminal/privacy-and-security.md
updated: 2026-11-14
---

# Lightning Node Connect

Lightning Node Connect (LNC) is a mechanism to create an end-to-end encrypted connection between a Lightning Network node (initially just LND) and a web browser. It is the connection method used by [[lightning-terminal]]; creating a session is covered in [[running-litd]], and the session API in [[lit-sessions]]. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/lightning-node-connect.md))

LNC does not require the node to expose any ports. Instead, the application and the node are connected through a proxy server called the mailbox, and the connection between node and application is end-to-end encrypted. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/lnc-npm.md))

## The three parts

1. **Lightning Node Connect in `litd`.** It runs as part of the Lightning Terminal Daemon, is connected to the Lightning node and typically runs on the same machine or network as the node. This is where macaroons are baked, requests and data are forwarded between node and user, and where the connection to the proxy server is made.
2. **A proxy**, also called Traversal Using Relays around NAT (TURN), which establishes two semi-synchronous pipes through which the user and their node can communicate. It mainly improves the user experience for nodes set up behind a NAT or firewall.
3. **The application**, for instance Lightning Terminal, delivered by a web server and running in the user's browser. It could also run as a standalone application, for example on a laptop, smartphone or dedicated device.

([source](../../raw/docs/lightning-network-tools/lightning-terminal/lightning-node-connect.md))

## Connection establishment

The process starts with the user creating a new Lightning Node Connect session in `litd`. This creates a pairing phrase, typically 10 English words, from which a 64-byte stream ID can be derived. `litd` then listens for incoming connections through the proxy, on the stream with the derived ID. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/lightning-node-connect.md))

### Initial handshake

LNC uses the Noise Protocol Framework, which the Lightning Network already uses for encrypted connections between nodes (BOLT 8). Generating the pairing phrase in litd triggers the generation of a long-term public key for the handshakes in addition to the 64-byte stream ID. A password-authenticated key exchange (PAKE) is combined in a single step with the Noise handshake; through it, Lightning Node Connect and the application learn the other side's long-term Diffie-Hellman (DH) key and a shared secret, from which other keys can be derived. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/lightning-node-connect.md))

LNC only allows a single attempt to authenticate this key exchange, which is what allows the use of a low-entropy password that can be more easily typed or remembered. When the user enters the pairing phrase into their application, the initial handshake completes; Lightning Node Connect can then forget the pairing phrase and only communicates using the negotiated keys, preventing brute force attacks. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/lightning-node-connect.md))

At this stage, instead of transmitting a zero-value AEAD payload, Lightning Node Connect may also pass a newly baked macaroon to the client, restricting access to the node, for example by duration, types of actions taken or amount of value being transferred (see [[macaroons]]). While only a single pairing phrase may be generated at a time, multiple connections can be maintained, each with its own DH key and macaroon, for example for different types of applications or users. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/lightning-node-connect.md))

The handshake variant used for the initial connection is:

```
XXeke_secp256k1+SPAKE2_CHACHAPOLY1305_SHA256
```

([source](../../raw/docs/lightning-network-tools/lightning-terminal/lightning-node-connect.md))

### Secondary pairing handshake

For each subsequent connection LNC performs a secondary pairing handshake, in which the key authentication can be omitted as long as the long-term DH key is still known to the participants. This handshake takes the place of the usual TLS handshake in other gRPC calls to LND. The handshake used for each subsequent connection is:

```
IK_secp256k1+CHACHAPOLY1305_SHA256
```

([source](../../raw/docs/lightning-network-tools/lightning-terminal/lightning-node-connect.md))

## Terminal Proxy (mailbox)

When Lightning Node Connect is initialized using litd, a mailbox is created on the Terminal Proxy, identified with the hash of the pairing phrase. Once the pairing phrase is entered into the Terminal application on the web, the application can reach the mailbox and the initial handshake can start. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/lightning-node-connect.md))

The proxy server creates two pipes, one for the application to push data to the Lightning node and another in the opposite direction. Each pipe is identified with the 64-byte stream ID. Only this stream ID is needed to feed data into the pipe, and pipes can only be created through authentication. Messages in the pipes are delivered in order. According to the guide, these mechanisms make it possible to use Terminal on the web without having to trust the proxy. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/lightning-node-connect.md))

The mailbox is unable to see the contents of the packages transmitted between node and application. It is also possible to select a custom mailbox, which then also has to be specified in the application. Running your own mailbox is covered in [[aperture-mailbox-and-lnc]]. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/lnc-npm.md))

## WebAssembly client

Instead of implementing the client in Javascript, Lightning Terminal uses WebAssembly (WASM) and readily available libraries, such as the noise implementation in lnd. For gRPC connections, existing clients are used with modifications for the custom transport mechanisms. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/lightning-node-connect.md))

The user feeds the pairing phrase to the application, which triggers the generation of a public key for the DH handshake and a stream ID, and allows the application to verify the connection and discard the pairing phrase. The user additionally selects a password, ideally using their password manager, to encrypt the generated secrets locally and prevent unauthorized use. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/lightning-node-connect.md))

## The user's view

1. The user generates a pairing phrase in their node. They may be behind a NAT or firewall and do not need to expose ports. They may specify limited conditions, such as 'read-only' or 'administrator.'
2. The user enters the pairing phrase into the application and chooses a password. The phrase can be copied, written or scanned via a QR code. The password is used to encrypt the connection details in the browser's storage or the device.
3. A persistent connection is established directly between the node and the application.
4. Subsequent connections require only the user's password: the long-term Diffie-Hellman key is decrypted using the password, and a second handshake is used to reestablish and verify the connection.

([source](../../raw/docs/lightning-network-tools/lightning-terminal/lnc-npm.md))

Through Lightning Node Connect a user may access their node in addition to liquidity services like [[loop]] and [[pool]]. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/lnc-npm.md))

## Using LNC in your own application: lnc-web

LNC works natively with WebAssembly applications (Wasm). To use LNC on the web, set up the open source NPM module `lnc-web` (repository `lightninglabs/lnc-web`) by configuring it with a pairing phrase (supplied by the user), a mailbox and your application's Wasm binary. The package is intended for web applications, where users navigate to a website and the lnc package and wasm are loaded into their browser; the guide points to Lightning Terminal as a reference. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/lnc-npm.md))

Install the package:

```
npm install @lightninglabs/lnc-web
```

Import it (the guide prints this line with typographic quotes):

```
import LNC from ‘@lightninglabs/lnc-web’
```

([source](../../raw/docs/lightning-network-tools/lightning-terminal/lnc-npm.md))

Best practice: credentials such as the long-term Diffie-Hellman keys should be encrypted at rest with a solid password of the user's choosing. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/lnc-npm.md))

### Demo application

The LNC-web demo React application connects to your own node via LNC by providing only the pairing phrase from litd. It shows basic information obtained through the "getinfo" RPC call: alias, pubkey, active and inactive channels, and synchronization status. Install and run it with:

```
git clone https://github.com/lightninglabs/lnc-web.git
cd lnc-web/demos/connect-demo
npm install
npm start
```

([source](../../raw/docs/lightning-network-tools/lightning-terminal/lnc-npm.md))

To connect, the node needs to run LND and litd (see [[running-litd]]). Obtain a pairing phrase through litd, either through the GUI or on the command line:

```
litcli --lndtlscertpath ~/.lit/tls.cert sessions add --label="LNC Demo" --type admin
```

Then open the app in the browser at localhost:3000, click the 'Connect' button at the top right, enter the pairing phrase and specify a password. The page can be closed and reopened at any time: credentials are stored locally in encrypted form, and on reconnection the password is used to decrypt the connection details and re-authenticate the session with litd on the node. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/lnc-npm.md))

## Future work

The guide states that extending Terminal on the web beyond sending and receiving payments, opening and closing channels or inspecting payments in flight requires extensions to the LND API, and that the API endpoints of Pool and Loop will have to be further abstracted as well. ([source](../../raw/docs/lightning-network-tools/lightning-terminal/lightning-node-connect.md))

## Related

- [[litd-accounts-guide]]: Using litd accounts
- [[terminal-liquidity-tools]]: Terminal liquidity tools: autofees, autoopen, reports
- [[terminal-privacy-and-security]]: Terminal privacy and security
- [[litd-integration]]: Integrating litd and its CLI
- [[lit-proxy]], [[lit-status]]

## Conflicts

- **Reusing a pairing phrase.** The under-the-hood guide says LNC "will only allow a single attempt to authenticate this key exchange" and that after the initial handshake Lightning Node Connect "can now forget the pairing phrase" ([source](../../raw/docs/lightning-network-tools/lightning-terminal/lightning-node-connect.md)). The privacy and security guide says the pairing phrase "does not need to be stored anywhere, but can be reused for another connection attempt", with only one concurrent connection possible per pairing phrase ([source](../../raw/docs/lightning-network-tools/lightning-terminal/privacy-and-security.md)).
