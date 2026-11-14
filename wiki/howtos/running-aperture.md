---
title: Installing and running Aperture
type: howto
sources:
  - raw/docs/lightning-network-tools/aperture/get-aperture.md
  - raw/docs/lightning-network-tools/aperture/step-by-step.md
updated: 2026-11-14
---

# Installing and running Aperture

How to download, build, configure and deploy [[aperture]] in front of an HTTP service. For what an L402 is, see [[l402]] and [[macaroons]]. For the service and pricing options in the configuration file see [[aperture-pricing-and-services]].

## Short version

The "Get Aperture" page gives the minimal procedure. The requirement is go 1.19 or later.

```
git clone https://github.com/lightninglabs/aperture.git
cd aperture
make install
```

```
mkdir ~/.aperture
cp sample-conf.yaml ~/.aperture/aperture.yaml
```

Then run `aperture`. ([source](../../raw/docs/lightning-network-tools/aperture/get-aperture.md))

By default Aperture uses port 8081, and this port needs to be reachable from the outside. Aperture will create a TLS key and self-signed certificate; to run in production it needs a valid TLS certificate for the domain it is running on. ([source](../../raw/docs/lightning-network-tools/aperture/get-aperture.md))

The same page links an L402 demo at <https://lsat-playground-bucko.vercel.app/> (with a testnet version) where you can go through minting a Macaroon, turning it into an L402, restricting and validating it. ([source](../../raw/docs/lightning-network-tools/aperture/get-aperture.md))

## Step by step

### Prerequisites

- A server, ideally Linux with root privileges
- A domain name or its subdomain
- An LND node (port 10009 must be reachable); see [[lnd]]

([source](../../raw/docs/lightning-network-tools/aperture/step-by-step.md))

### Install

Aperture requires root access to bind to privileged ports. The guide sets everything up in the root shell, entered with `sudo -i`. ([source](../../raw/docs/lightning-network-tools/aperture/step-by-step.md))

Download the latest Go release for the correct chip architecture (typically amd64) and unpack it:

```
wget https://go.dev/dl/go[version].linux-amd64.tar.gz
tar -C /usr/local -xzf go[version].linux-amd64.tar.gz
```

Add the following lines to `.bashrc`, then reload `bash`:

```bash
export PATH=$PATH:/usr/local/go/bin
export GOPATH=~/go
export PATH=$PATH:$GOPATH/bin
```

Clone and build Aperture:

```
git clone https://github.com/lightninglabs/aperture.git
cd aperture
make install
```

([source](../../raw/docs/lightning-network-tools/aperture/step-by-step.md))

### Configure

A sample configuration file is provided in the aperture folder under the name `sample-conf.yaml`. The guide's example sets up a simple proxy to a service called "l402proxy" running on port 8080 on the same machine, so https is not configured between the proxy and the service. The service is meant to be reached through its domain `l402proxy.domain.com`. Only requests to /service are proxied, everything else is dropped, and all calls to the endpoint /service/free are exempt from the fee. ([source](../../raw/docs/lightning-network-tools/aperture/step-by-step.md))

The top-level and authenticator settings of the example are:

```yaml
# Your proxy will listen to all incoming connections on port 443.
listenaddr: "0.0.0.0:443"
debuglevel: "debug"
configfile: "/root/.aperture/aperture.yaml"
basedir: "/root/.aperture"

# Settings for the lnd node used to generate payment requests.
authenticator:
  network: "mainnet"
  disable: false
  # The IP or domain and port where your LND node can be reached.
  lndhost: "127.0.0.1:10009"
  # The path to lnd's TLS certificate.
  tlspath: "/home/ubuntu/.lnd/tls.cert"
  # The path to lnd's macaroon directory. If your node is on another machine, you may copy the invoice.macaroon file from there and place it in "/root/.aperture", then specify that directory instead.
  macdir: "/home/.lnd/data/chain/bitcoin/mainnet"

# The selected database backend.
dbbackend: "sqlite"
```

([source](../../raw/docs/lightning-network-tools/aperture/step-by-step.md))

The `services:` list of the same example is reproduced and explained on [[aperture-pricing-and-services]]. ([source](../../raw/docs/lightning-network-tools/aperture/step-by-step.md))

The example also serves a static page to requests not matched by the services, with:

```yaml
servestatic: true
staticroot: "/root/.aperture/static"
```

An `index.html` must be created in the folder `/root/.aperture/static`. ([source](../../raw/docs/lightning-network-tools/aperture/step-by-step.md))

### Obtain a TLS certificate

The guide uses Certbot to obtain a Let's Encrypt certificate for the domain before starting Aperture. Port 80 and 443 must be reachable from the outside with no other service, such as an existing web server, binding to them; if Aperture is already running, shut it down. ([source](../../raw/docs/lightning-network-tools/aperture/step-by-step.md))

```
certbot certonly --standalone
```

Certbot installs the certificates in its own directory, typically `/etc/letsencrypt/live/l402proxy.domain.com/`. Copy and rename them for aperture:

```
cp /etc/letsencrypt/live/l402proxy.domain.com/fullchain.pem /root/.aperture/tls.cert
cp /etc/letsencrypt/live/l402proxy.domain.com/privkey.pem /root/.aperture/tls.key
```

([source](../../raw/docs/lightning-network-tools/aperture/step-by-step.md))

### Start and verify

Start Aperture with `aperture`. You should then be able to go to your domain in a web browser and see the static page, and get the HTTP response "402 Payment Required" when navigating to `/service`. ([source](../../raw/docs/lightning-network-tools/aperture/step-by-step.md))

## Related

- [[aperture-mailbox-and-lnc]] includes an optional systemd unit for running `aperture` as a service.
- [[machine-payments-protocol]] for enabling MPP in the same configuration file.

## Conflicts

- macdir path. In the step-by-step example `tlspath` is `"/home/ubuntu/.lnd/tls.cert"` while `macdir` is `"/home/.lnd/data/chain/bitcoin/mainnet"` (no `ubuntu` path element) ([source](../../raw/docs/lightning-network-tools/aperture/step-by-step.md)).

## Notes

Synthesis, not from a single source: "Get Aperture" says "By default Aperture uses port 8081" ([source](../../raw/docs/lightning-network-tools/aperture/get-aperture.md)), while the step-by-step example sets `listenaddr: "0.0.0.0:443"` ([source](../../raw/docs/lightning-network-tools/aperture/step-by-step.md)). One is stated as a default and the other is an explicit setting in an example, so this is not recorded as a conflict. Neither page shows a default `listenaddr` line.
