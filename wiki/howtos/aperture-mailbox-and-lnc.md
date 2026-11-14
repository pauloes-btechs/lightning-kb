---
title: Aperture as LNC mailbox and backend
type: howto
sources:
  - raw/docs/lightning-network-tools/aperture/mailbox.md
  - raw/docs/lightning-network-tools/aperture/lnc-backend.md
updated: 2026-11-14
---

# Aperture as LNC mailbox and backend

[[aperture]] relates to Lightning Node Connect (LNC, see [[lightning-node-connect]]) in two separate ways. The Lightning Node Connect relay proxy server, the mailbox, comes bundled in Aperture, and you can install your own. ([source](../../raw/docs/lightning-network-tools/aperture/mailbox.md))

Aperture can also connect to its LND backend over LNC. This configuration is different from configuring the LNC Mailbox, though both may be configured at the same time. ([source](../../raw/docs/lightning-network-tools/aperture/lnc-backend.md))

## Part 1: running your own LNC mailbox

### Background

LNC is a protocol that establishes a connection between your Lightning Network node (LND) and a remote application, such as Lightning Terminal or Zeus. To traverse firewalls and Network Address Translation (NAT), LNC makes use of a mailbox proxy, which is part of the open-source aperture and can be installed freely by anybody. ([source](../../raw/docs/lightning-network-tools/aperture/mailbox.md))

LNC is most useful when both the client and the Lightning node are behind a firewall or NAT, but it can also be useful when only the Lightning node is unreachable. In that case aperture may be installed on the same machine as the client application. ([source](../../raw/docs/lightning-network-tools/aperture/mailbox.md))

### Configure aperture

Edit the configuration file with `nano ~/.aperture/aperture.yaml`. The guide's template follows; swap the domain name for your own, and make sure that domain points to the server on which aperture is being set up.

```yaml
listenaddr: "lnc.yourlightning.app:443"
debuglevel: "trace"
autocert: true
servername: lnc.yourlightning.app
authenticator:
  disable: true
hashmail:
  enabled: true
  messagerate: 1ms
  messageburstallowance: 99999999
prometheus:
  enabled: false
```

([source](../../raw/docs/lightning-network-tools/aperture/mailbox.md))

### Run aperture

Run `aperture`. The logs may show that it is listening for connections:

```
[INF] APER: Configuring autocert for server lnc.yourlightning.app with cache dir /root/.aperture/autocert
[INF] APER: Starting the server, listening on lnc.yourlightning.app:443.
```

([source](../../raw/docs/lightning-network-tools/aperture/mailbox.md))

### Connect to Terminal

The LND node can now be connected to Lightning Terminal using the self-hosted mailbox. litd must be running alongside LND (see [[running-litd]] and [[lightning-terminal]]). Create a session that names the mailbox:

```
litcli sessions add --label="My own mailbox" --type admin --mailboxserveraddr lnc.yourlightningapp:443
```

Then type the generated connection string into Lightning Terminal, together with the url and port number of the mailbox, connect, and select and confirm a password. The sessions API is on [[lit-sessions]]. ([source](../../raw/docs/lightning-network-tools/aperture/mailbox.md))

### Troubleshooting

On some VPS providers, aperture fails to correctly bind to the address and port it listens on. The guide shows the resulting log:

```
[ERR] APER: Error while running aperture: listen tcp 172.81.180.188:443: bind: cannot assign requested address
[INF] APER: Shutdown complete
```

A fix for this error is not found in sources. ([source](../../raw/docs/lightning-network-tools/aperture/mailbox.md))

### Optional: systemd

Navigate to the systemd directory and create a new service:

```
cd /etc/systemd/system
sudo nano aperture.service
```

Template:

```
[Unit]
Description=LNC mailbox service

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu
ExecStart=/usr/local/bin/aperture
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Reload the list of services with `sudo systemctl daemon-reload`, start the service with `sudo systemctl start aperture.service`, and check its status with `sudo systemctl status aperture.service`. ([source](../../raw/docs/lightning-network-tools/aperture/mailbox.md))

## Part 2: connecting Aperture to its LND backend over LNC

From version 0.2 aperture supports connecting to its LND backend over LNC, which lets it connect to your personal node without opening ports or configuring Tor or NAT. ([source](../../raw/docs/lightning-network-tools/aperture/lnc-backend.md))

### Create an LNC pairing phrase

A pairing phrase can be created using the Lightning Terminal UI or the command line. See [[lightning-node-connect]]. ([source](../../raw/docs/lightning-network-tools/aperture/lnc-backend.md))

### Configure Aperture

Edit or create the configuration file in `~/.aperture/aperture.yaml`. The relevant section should look like this:

```yaml
# The address which the proxy can be reached at.
listenaddr: "localhost:8080"

# Settings for the lnd node used to generate payment requests. All of these
# options are required.
authenticator:
  passphrase: "your pairing phrase"
  mailboxaddress: "mailbox.terminal.lightning.today:443"
  network: "mainnet"
  devserver: false

# The selected database backend. The current default backend is "sqlite".
# Aperture also has support for postgres and etcd.
dbbackend: "sqlite"
```

([source](../../raw/docs/lightning-network-tools/aperture/lnc-backend.md))

At the time of writing of the guide, Aperture over LNC only works with the default database backend sqlite. ([source](../../raw/docs/lightning-network-tools/aperture/lnc-backend.md))

### Run

Run aperture with `aperture`. The rest of the configuration (services, pricing, TLS) is on [[running-aperture]] and [[aperture-pricing-and-services]]. ([source](../../raw/docs/lightning-network-tools/aperture/lnc-backend.md))

## Conflicts

- Length of the connection phrase. The LNC backend page describes passing on "an eight word connection phrase" ([source](../../raw/docs/lightning-network-tools/aperture/lnc-backend.md)); the mailbox page says to type "the generated 10-word connection string" into Lightning Terminal ([source](../../raw/docs/lightning-network-tools/aperture/mailbox.md)).
- Mailbox domain spelling. Within the mailbox page the configuration template and first log use `lnc.yourlightning.app`, the `litcli sessions add` command uses `--mailboxserveraddr lnc.yourlightningapp:443`, and the troubleshooting log uses `lnc.yourlightningapp.com` ([source](../../raw/docs/lightning-network-tools/aperture/mailbox.md)). These are placeholder domains, copied here as printed.
- autocert cache dir. In the same page the first log shows the cache dir `/root/.aperture/autocert`, while the troubleshooting log, run as `root@mailbox`, shows `/home/ubuntu/.aperture/autocert` ([source](../../raw/docs/lightning-network-tools/aperture/mailbox.md)).
