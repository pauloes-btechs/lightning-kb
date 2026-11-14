---
title: "Using Loop: Loop In and Loop Out"
type: howto
sources:
  - raw/docs/lightning-network-tools/loop/get-started.md
  - raw/docs/lightning-network-tools/loop/the-loop-cli.md
  - raw/docs/lightning-network-tools/loop/peer-with-loop.md
  - raw/docs/lightning-network-tools/loop/autoloop.md
updated: 2026-11-14
---

# Using Loop: Loop In and Loop Out

How to install [[loop]], run swaps with the `loop` CLI, and peer with the Loop node. The RPCs behind the commands are on [[loop-swap-client]]; the swap mechanism is described on [[submarine-swaps]].

## Get started

Loop comes bundled with Lightning Terminal (`litd`). If you are already running `litd`, you can access Loop through the command line or the Lightning Terminal UI and may skip the installation steps (see [[lightning-terminal]]). ([source](../../raw/docs/lightning-network-tools/loop/get-started.md))

To run Loop you need to be running LND from the binary releases, or compile it from source with `make install tags="signrpc walletrpc chainrpc invoicesrpc"` (see [[lnd]]). ([source](../../raw/docs/lightning-network-tools/loop/get-started.md))

Loop itself can be run from the binary releases (`https://github.com/lightninglabs/loop/releases`) or compiled from source, which requires Golang:

```
git clone https://github.com/lightninglabs/loop.git
cd loop
make && make install
```

([source](../../raw/docs/lightning-network-tools/loop/get-started.md))

By default, the `loopd.conf` is placed in `~/.loop/mainnet/`. If you start `loopd` on another network (e.g. `loopd --network=signet`), the configuration file is expected in the relevant directory (e.g. `~/.loop/signet`). You may also pass a custom directory with the `--configfile=` flag. ([source](../../raw/docs/lightning-network-tools/loop/get-started.md))

### loopd on a different machine than LND

You may run `loopd` on a separate machine and network as LND. You may have to first configure LND to listen on external IPs with `lnd.rpclisten=0.0.0.0:10009`, add the LND machine's IP address(es) to the TLS certificate with `tlsextraip=`, delete the existing `tls.key` and `tls.cert` and restart LND to regenerate the certificates. ([source](../../raw/docs/lightning-network-tools/loop/get-started.md))

In `loopd.conf`, define the LND host (`lnd.host=<ip>:10009`), copy the LND admin macaroon and TLS certificate over and specify their paths with `lnd.macaroonpath=/path/to/admin.macaroon` and `lnd.tlspath=/path/to/tls.cert`. ([source](../../raw/docs/lightning-network-tools/loop/get-started.md))

## Terms and quotes

As soon as Loop is running you can use the CLI, by typing `loop` or by executing `./loop` where the binaries are stored. ([source](../../raw/docs/lightning-network-tools/loop/the-loop-cli.md))

`loop terms` gives the minimum and maximum amounts of satoshis that can be looped in or out, and the CLTV Delta, the number of blocks the bitcoin would be locked up in the event a Loop In is unsuccessful (i.e. due to lack of inbound liquidity). `loop getparams` shows current fees, prepaid amounts and [[autoloop]] settings. ([source](../../raw/docs/lightning-network-tools/loop/the-loop-cli.md))

`loop quote in 500000` gives a more precise quote for a Loop In. A Loop In makes an on-chain transaction, for which on-chain transaction fees are paid; if there are enough satoshis in the on-chain LND wallet, Loop can estimate these fees as well. The swap fee is quoted in satoshi as `swap_fee_sat`. ([source](../../raw/docs/lightning-network-tools/loop/the-loop-cli.md))

`loop quote out <amount in satoshi>` gives a quote for a Loop Out. The cost of sweeping the HTLC smart contract is quoted in satoshi as `htlc_sweep_fee_sat`, an estimate based on the amount of data required to sweep the funds and the current level of on-chain fees necessary to have the transaction confirmed within the CLTV window. ([source](../../raw/docs/lightning-network-tools/loop/the-loop-cli.md))

## Loop In

The command is `loop in <amount in satoshis>`. The `--last_hop` parameter specifies the channel the Lightning payment should arrive in; the last hop is identified by the public key of a node, with which you should have an active channel and plenty of incoming capacity. `--label` sets a label. A higher `--conf_target` gives lower fees and longer processing times. ([source](../../raw/docs/lightning-network-tools/loop/the-loop-cli.md))

Example from the guide:

```
loop in --last_hop 02e7a7d3c1e6055b7b7457d95e04d9bbd24f200fd4a58daca7beee7bc776e17440 --amt 295916
```

Once the command is run, the upper bound of the fees for the transaction is quoted. Loop will then obtain a LSAT for 1 satoshi and initiate the swap. ([source](../../raw/docs/lightning-network-tools/loop/the-loop-cli.md))

`loop monitor` gives updates about the swap. As soon as the on-chain transaction has one confirmation, the off-chain transaction should arrive in the specified channel. ([source](../../raw/docs/lightning-network-tools/loop/the-loop-cli.md))

### External Loop In

A Loop In can be funded from any external wallet with the `--external` flag. After executing `loop in`, two HTLC smart contract addresses are presented in addition to the swap ID; the on-chain transaction may go to either, though P2WSH (starting with bc1) is recommended for maximum efficiency. The payment needs to be the exact amount and carry an appropriate transaction fee. There is no time limit for when the on-chain payment has to confirm, but if a channel was specified, the state of that channel might change over the next day or two. ([source](../../raw/docs/lightning-network-tools/loop/the-loop-cli.md))

## Loop Out

Loop Out requires a minimum amount, typically around 250,000 satoshis; the value may increase in times of high on-chain fees and can be obtained with `loop terms`. The `--channel` flag with a short channel ID selects the channel to loop out of. ([source](../../raw/docs/lightning-network-tools/loop/the-loop-cli.md))

Flags that influence speed and fees:

- `--fast`: the Loop server publishes its on-chain transaction quickly, but at a higher fee.
- `--conf_target`: the number of blocks within which the HTLC is swept to your own wallet once the server's transaction is confirmed; this is usually done within 9 blocks.
- `--max_swap_routing_fee`: an upper bound in satoshi for the off-chain fees.
- `--addr`: the Bitcoin address of an external wallet; by default the on-chain transaction arrives in your LND's wallet.

([source](../../raw/docs/lightning-network-tools/loop/the-loop-cli.md))

Example from the guide:

```
loop out --channel 735057608151793668 --conf_target 250 --label ‘Guide to Loop’ --max_swap_routing_fee 2500 --addr bc1qvnfuf2zvg6mrfyjhc8h4c7ge9a7ywfrav52qru --amt 1000000
```

Before the swap begins, a fee overview is shown:

```
Estimated on-chain sweep fee:        7372 sat
Max on-chain sweep fee:            737200 sat
Max off-chain swap routing fee:       2500 sat
Max no show penalty (prepay):       30000 sat
Max off-chain prepay routing fee:      610 sat
Max swap fee:                        3260 sat
```

([source](../../raw/docs/lightning-network-tools/loop/the-loop-cli.md))

How a Loop Out proceeds, according to the guide:

1. The Loop server makes its on-chain transaction to the HTLC smart contract first, before the client makes its Lightning payment; the smart contract acts as a trustless arbiter (see [[htlc]]).
2. The client makes the Lightning payment to Loop. If the client fails to make it, the server can claim the on-chain funds back for itself and charge a penalty fee.
3. Once the Lightning payment was made successfully, the client can sweep the funds from the smart contract using the secret obtained in the payment. As soon as the on-chain transaction to the HTLC is confirmed, the Loop instance sweeps the funds into the internal wallet or the specified external address, and the client pays the miner fee for this.

([source](../../raw/docs/lightning-network-tools/loop/the-loop-cli.md))

`loop monitor` follows the status of the swap. Transactions are batched. While waiting for the on-chain transaction to the smart contract to confirm, the overall capacity of the node, and of the channel being looped out of, appears decreased by the Loop Out amount; once the transaction confirms, the channel capacity goes back to its full amount and the local and remote balances change by the Loop Out amount. ([source](../../raw/docs/lightning-network-tools/loop/the-loop-cli.md))

### Worked fee example

For the 1 million satoshi Loop Out above, the guide reports `cost: server 3260, onchain 6802, offchain 2524` on completion: 12,586 satoshi in fees in total, of which 6802 went to Bitcoin miners, 3260 to Loop and 2524 to the Lightning nodes routing the off-chain payment. ([source](../../raw/docs/lightning-network-tools/loop/the-loop-cli.md))

`lncli listpayments` shows two outgoing payments: first the 30,000 satoshi prepayment, which covers the sweep fee for Loop in case the full off-chain payment is not made, then 973,260 satoshi, which is the remaining 970,000 satoshi of the swap plus the 3,260 satoshi swap fee. 993,198 satoshi were received in the on-chain address. ([source](../../raw/docs/lightning-network-tools/loop/the-loop-cli.md))

## Parameters for frequent users

`loop setparams <options>` sets parameters for swaps. The guide lists these options, each shown with `(default: 0)`:

| Option | Meaning |
| --- | --- |
| `--sweeplimit value` | the limit placed on our estimated sweep fee in sat/vByte |
| `--maxswapfee value` | the maximum percentage of swap volume we are willing to pay in server fees |
| `--maxroutingfee value` | the maximum percentage of off-chain payment volume that we are willing to pay in routing fees |
| `--maxprepayfee value` | the maximum percentage of off-chain prepay volume that we are willing to pay in routing fees |
| `--maxprepay value` | the maximum no-show (prepay) in satoshis that swap suggestions should be limited to |
| `--maxminer value` | the maximum miner fee in satoshis that swap suggestions should be limited to |
| `--sweepconf value` | the number of blocks from htlc height that swap suggestion sweeps should target, used to estimate max miner fee |
| `--failurebackoff value` | the amount of time, in seconds, that should pass before a channel that previously had a failed swap will be included in suggestions |

([source](../../raw/docs/lightning-network-tools/loop/the-loop-cli.md))

These parameters are not persistent and need to be specified again upon restart. More on them is on [[autoloop]]. ([source](../../raw/docs/lightning-network-tools/loop/the-loop-cli.md))

## Past swaps

`loop listswaps` gives detailed information about past Loops, including their amounts, on-chain addresses, associated fees and eventual failure messages. `loop swapinfo <swap id>` queries the status of an individual swap. ([source](../../raw/docs/lightning-network-tools/loop/the-loop-cli.md))

## Peer with Loop

The Loop Lightning Network node is publicly reachable and accepts incoming channels. Lightning Loop helps merchants and other Lightning services swap their off-chain funds for on-chain funds, and Lightning Labs looks for well-connected routing node operators interested in earning routing fees to help route these funds to the Loop node (see [[routing-nodes]]). ([source](../../raw/docs/lightning-network-tools/loop/peer-with-loop.md))

What to expect: as merchants and services Loop Out, the unidirectional movement of funds drains the peer's channels, which can happen rapidly for routing nodes with competitive fee rates and good connectivity. Once the channel capacity is exhausted, the channel is likely to be cooperatively closed so that the on-chain funds, which have moved to Loop's side, can be used to fund swaps on-chain. Peering with Loop requires adequate inbound capacity from the wider network, which is likely to deplete over time (see [[inbound-capacity]] and [[liquidity]]). ([source](../../raw/docs/lightning-network-tools/loop/peer-with-loop.md))

Loop peers are compensated for their blockchain fees and liquidity costs mainly by earning fees on the forwarded payments, so the fees for the channel with Loop should be set appropriately before the channel is active, ideally by configuring defaults (see [[channel-fees]]). The guide states that in practice most of the fees of a Loop Out are paid to routing node operators rather than to the Loop service itself. ([source](../../raw/docs/lightning-network-tools/loop/peer-with-loop.md))

Steps given by the guide:

1. Loop requires a minimum channel size of 30,000,000 satoshis.
2. Amend `lnd.conf` with `bitcoin.feerate=1000` and restart LND to put the change into effect.
3. Open the channel to Loop: `lncli openchannel –node_key 021c97a90a411ff2b10dc2a8e32de2f29d2fa49d41bfbb52bd416e460db0747d0d –connect 50.112.125.89:9735 –local_amt 210000000 –conf_target 6`
4. The channel becomes active after 6 confirmations.

([source](../../raw/docs/lightning-network-tools/loop/peer-with-loop.md))

Loop node addresses given by the guide:

| Network | Node |
| --- | --- |
| Mainnet | `021c97a90a411ff2b10dc2a8e32de2f29d2fa49d41bfbb52bd416e460db0747d0d@44.228.158.82:9735` |
| Testnet3 | `0200a7f20e51049363cb7f2a0865fe072464d469dca0ac34c954bb3d4b552b6e95@80.253.94.252:9736` |
| Signet | `022b9e44b3a8093d9512b61f5f83a72d5634201efc49718efd34f2ee851b3afa8e@50.112.25.211:9735` |

([source](../../raw/docs/lightning-network-tools/loop/peer-with-loop.md))

Performing Loop Ins, meaning refilling your channels through an onchain swap, is described as a cost effective way to extend the lifetime of a channel with Loop and keep it from closing. These swaps use Taproot by default, which allows Loop In to be priced as low as 1 ppm. At a fee rate of 50 sat/vB, a one-input-one-output transaction costs about 7200 satoshis, compared to about 8000 satoshis to close a channel plus a minimum of 7200 to reopen it. ([source](../../raw/docs/lightning-network-tools/loop/peer-with-loop.md))

## Conflicts

- Loop node IP on mainnet: the example `lncli openchannel` command connects to `50.112.125.89:9735`, while the "Mainnet" section of the same page gives the node (same public key) at `44.228.158.82:9735`. The source does not say which is current. ([source](../../raw/docs/lightning-network-tools/loop/peer-with-loop.md))
- `--failurebackoff` default: the CLI guide lists it with `(default: 0)` ([source](../../raw/docs/lightning-network-tools/loop/the-loop-cli.md)), while the Autoloop guide says the default value of the failure backoff is 24 hours ([source](../../raw/docs/lightning-network-tools/loop/autoloop.md)). Both are recorded on [[autoloop]].

## Notes

Synthesis, not from a single source statement: the `lncli openchannel` example in the guide is printed with en dashes (`–node_key`) rather than double hyphens; it is copied here exactly as the source has it. The guide also says the client obtains "a LSAT" where other pages say L402 (see [[l402]]).
