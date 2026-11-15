---
title: RFQ and price oracles in practice
type: howto
sources:
  - raw/docs/lightning-network-tools/taproot-assets/rfq.md
  - raw/docs/lightning-network-tools/taproot-assets/decimal-display.md
updated: 2026-11-14
---

# RFQ and price oracles in practice

What Request For Quote (RFQ) does for Taproot Assets on Lightning, how quotes are computed, the role of price oracles, and the configuration values for the mock oracle, the sample oracle and your own oracle.

See also: [[taproot-assets]], [[tapd-rfq]], [[tapd-price-oracle]], [[taproot-assets-channels-guide]], [[edge-node-operation]], [[minting-taproot-assets]], [[taproot-assets-on-lightning]].

## What RFQ is

Request For Quote (RFQ) is a mechanism that simplifies sending Taproot Assets over Lightning Network channels. When sending Taproot Assets over the Lightning Network, an Edge Node is needed: it receives the Taproot Asset in the channel with the direct user and swaps it for bitcoin. As the swap rate between Taproot Assets and bitcoin likely fluctuates, the user may make a Request for Quote to the Edge Node before generating a Lightning Network invoice or initiating a payment. ([source](../../raw/docs/lightning-network-tools/taproot-assets/rfq.md))

The Request for Quote contains a rate and an expiration time, which allows the sender to decide whether they want to complete the payment and craft a route to the intended recipient. Similarly, when receiving Taproot Assets over the Lightning Network, RFQ is used by the recipient to generate a satoshi-denominated Lightning invoice. ([source](../../raw/docs/lightning-network-tools/taproot-assets/rfq.md))

### Transport and message types

The request is made using BOLT 01 messages over an existing encrypted and authenticated BOLT 08 connection. Messages are encoded as TLV records and delivered over LND's custom message channel. The message type namespace starts at `MsgTypeOffset`, which is `CustomTypeStart + 20116`, where `20116` encodes "tap". The connection already exists because it is used for establishing and coordinating the Taproot Asset Channel. ([source](../../raw/docs/lightning-network-tools/taproot-assets/rfq.md))

There are three message types, each available in buy and sell variants:

- **Request** (`MsgTypeRequest`): initiates negotiation. The user tells the edge node what asset and amounts are involved, and optionally proposes a rate hint.
- **Accept** (`MsgTypeAccept`): the edge node agrees to the proposed terms at a specific rate. The accept is Schnorr-signed over the message fields so neither party can modify the agreed rate later.
- **Reject** (`MsgTypeReject`): the edge node declines, with a machine-readable error code and human-readable message.

([source](../../raw/docs/lightning-network-tools/taproot-assets/rfq.md))

## Directions and the two order types

The RFQ system is responsible for acquiring real-time price quotes for converting between asset units and satoshi (both directions) or between different asset types. The direction of "inbound/in/buy" and "outbound/out/sell" is always seen from the point of view of the wallet end user, so what is outbound for the end user is inbound for the RFQ peer (edge node) and vice versa. ([source](../../raw/docs/lightning-network-tools/taproot-assets/decimal-display.md))

All arithmetic conversions use fixed point arithmetic. A `scale` (equivalent to a decimal display, but just for computations) of either `11` or the `decimal_display` value is used, whichever is greater. ([source](../../raw/docs/lightning-network-tools/taproot-assets/decimal-display.md))

### Sell order (paying invoices)

The sell order covers the user who wants to pay a satoshi-denominated invoice with assets. The user uses the pre-image referenced by the payment hash in the invoice to atomically sell some of the asset units in their channel to the RFQ peer (edge node). From the point of view of the edge node, they are effectively paid a routing fee to buy asset units by also sending out BTC. ([source](../../raw/docs/lightning-network-tools/taproot-assets/decimal-display.md))

In the guide's formal definition (using an example asset `buxx`), `out_asset` is `buxx`, `in_asset` is `msat`, `max_amount` is expressed in the `in_asset` (the invoice amount plus the user-defined max routing fee limit), `price_out_asset` is `out_asset_units_per_btc` (`buxx per BTC`) and `price_in_asset` is `in_asset_units_per_btc` (`msat per BTC`). ([source](../../raw/docs/lightning-network-tools/taproot-assets/decimal-display.md))

The number of asset units to send is `U = (X / M) * Y`, where `X` is the invoice amount in mSAT, `M` is the number of mSAT in a BTC (100,000,000,000), specified by `price_in_asset`, and `Y` is the number of asset units per BTC, specified by `price_out_asset`. ([source](../../raw/docs/lightning-network-tools/taproot-assets/decimal-display.md))

The guide's sequence diagram for a sell order runs: `SendPayment` from the user, `AddAssetSellOrder` on Node A, a price rate hint from Node A's oracle (`QueryAssetRate[type=SALE,intent=PAY_INVOICE_HINT,peer=NodeB]`), the sell request with the hint sent to Node B over p2p, Node B's oracle determining the actual rate (`QueryAssetRate[type=PURCHASE,intent=PAY_INVOICE,peer=NodeA]`), the actual rate returned to Node A, Node A's oracle validating it (`QueryAssetRate[type=SALE,intent=PAY_INVOICE_QUALIFY,peer=NodeB]`), and the payment sent over LN using the approved rate. ([source](../../raw/docs/lightning-network-tools/taproot-assets/decimal-display.md))

### Buy order (receiving via an invoice)

The buy order covers the user who wants to get paid: they create an invoice specifying the number of asset units they want to receive, which is mapped to a normal, satoshi-denominated invoice. The user uses the satoshis sent by the sender through the normal LN network to buy enough asset units to satisfy their invoice, using the edge node and the atomic exchange of the pre-image. ([source](../../raw/docs/lightning-network-tools/taproot-assets/decimal-display.md))

In the formal definition, `out_asset` is `msat`, `in_asset` is `buxx`, `max_amount` is expressed in the `in_asset` (the amount in the user query), `price_out_asset` is `out_asset_units_per_btc` (`msat per BTC`) and `price_in_asset` is `in_asset_units_per_btc` (`buxx per BTC`). ([source](../../raw/docs/lightning-network-tools/taproot-assets/decimal-display.md))

The amount to be paid into the edge node is `X = (U / Y) * M`, where `X` is the number of mSAT to receive, `U` is the desired number of asset units, `Y` is the number of asset units per BTC and `M` is the number of mSAT in a BTC (100,000,000,000). ([source](../../raw/docs/lightning-network-tools/taproot-assets/decimal-display.md))

The sequence diagram for a buy order runs: `AddInvoice` from the user, `AddAssetBuyOrder` on Node A, a hint from Node A's oracle (`QueryAssetRate[type=PURCHASE,intent=RECV_PAYMENT_HINT,peer=NodeB]`), the buy request sent to Node B over p2p, Node B's oracle determining the actual rate (`QueryAssetRate[type=SALE,intent=RECV_PAYMENT,peer=NodeA]`), Node A's oracle validating it (`QueryAssetRate[type=PURCHASE,intent=RECV_PAYMENT_QUALIFY,peer=NodeB]`), and the invoice created using the actual rate. ([source](../../raw/docs/lightning-network-tools/taproot-assets/decimal-display.md))

### Worked figures

For a USD asset with decimal display 6 (1_000_000 asset units = 1 USD) against satoshi, at 1 BTC = 20,000.00 USD the guide lists: Satoshi per USD 5000, Asset Units per Satoshi 200, Price In Asset 20000000000, Price Out Asset 100000000000, Min payable invoice amount 5 mSAT, Max MPP rounding error 80 mSAT (@16 shards). At 1 BTC = 1,000,000.00 USD it lists Asset Units per Satoshi 10000, Min payable invoice amount 1 mSAT and Max MPP rounding error 1 mSAT (@16 shards). The guide says these examples are constructed in `TestFindDecimalDisplayBoundaries` and `TestUsdToJpy` in `rfqmath/convert_test.go`. ([source](../../raw/docs/lightning-network-tools/taproot-assets/decimal-display.md))

## Price oracles

The price oracle provides the values for the exchange rates used by the RFQ system. Both parties of an asset channel (the wallet end user and the edge node) might use a price oracle, but its role is different for each, and the implementations are expected to differ. ([source](../../raw/docs/lightning-network-tools/taproot-assets/decimal-display.md))

The price oracle for the edge node puts a price tag on the service offered by the edge node, which is an atomic swap between two types of assets (often one of them being BTC). Its inputs are variables such as the official exchange rate between the asset and BTC, the size/volume of the swap and the requested validity duration (expiry). Its output is an exchange rate adjusted to include a spread, which is what compensates the edge node for offering the swap service, including exchange rate fluctuation risks. ([source](../../raw/docs/lightning-network-tools/taproot-assets/decimal-display.md))

The price oracle for the wallet end user is simply tasked with validating exchange rates offered by the edge node, to make sure they aren't proposing absurd rates. ([source](../../raw/docs/lightning-network-tools/taproot-assets/decimal-display.md))

By default, the minimum quote expiry a tapd node will accept is 10 seconds. ([source](../../raw/docs/lightning-network-tools/taproot-assets/decimal-display.md))

### Edge node oracle

No default implementation of a price oracle for edge nodes is provided. Edge node operators need to implement the RPC interface defined in `taprpc/priceoraclerpc` and point their `tapd` to it with the `experimental.rfq.priceoracleaddress=rfqrpc://<hostname>:<port>` configuration value. The guide points to an example Golang implementation in `docs/examples/basic-price-oracle`. The RPC reference is on [[tapd-price-oracle]]. ([source](../../raw/docs/lightning-network-tools/taproot-assets/decimal-display.md))

### Wallet end user oracle

The wallet end user's oracle can be quite simple: all it needs to do is query an exchange provider's API for the current exchange rate of an asset. The maximum deviation from that market rate that is accepted from edge nodes is configured with `experimental.rfq.acceptpricedeviationppm=`, which is in parts per million; the default value is `50000`, equal to `5%`. There is no default implementation of an end user price oracle either; the guide expects third party developers to offer a gRPC (`rfqrpc`) compatible price oracle endpoint that can be plugged into `experimental.rfq.priceoracleaddress=rfqrpc://<hostname>:<port>`. ([source](../../raw/docs/lightning-network-tools/taproot-assets/decimal-display.md))

## Configuration for testing

When added to `lit.conf`, all Taproot Assets configuration options have to be prefixed with `taproot-assets.`. ([source](../../raw/docs/lightning-network-tools/taproot-assets/rfq.md))

### The mock oracle

For testing purposes, tapd includes a mock oracle, which lets the tester set up a static exchange rate between Taproot Assets and bitcoin:

```
taproot-assets.experimental.rfq.priceoracleaddress=use_mock_price_oracle_service_promise_to_not_use_on_mainnet
```

([source](../../raw/docs/lightning-network-tools/taproot-assets/rfq.md))

A fixed swap rate can be set to avoid building a custom price oracle. The guide's example for trading one unit per satoshi is:

```
taproot-assets.experimental.rfq.mockoraclesatsperasset=1
```

Alternatively a price of asset per Bitcoin can be set. If the asset has decimal places, enter the full precision (for two decimal places, add two zeroes). The guide's example defines one asset per satoshi, without decimal places:

```
taproot-assets.experimental.rfq.mockoracleassetsperbtc=100000000
```

([source](../../raw/docs/lightning-network-tools/taproot-assets/rfq.md))

Both peers of a Taproot Assets channel may set up an RFQ oracle. Alternatively, one of the nodes may choose to operate without an oracle, simply accepting all quotes from the Edge Node:

```
taproot-assets.experimental.rfq.skipacceptquotepricecheck=true
```

([source](../../raw/docs/lightning-network-tools/taproot-assets/rfq.md))

### The sample oracle

For signet, a sample oracle is deployed at `tassandra.laisee.org` for asset group key `02db9c81b87830b73331e0f1f69271791f13a24848ceec9bd38e32383e384cc468`. It is configured by adding only the following to `lit.conf` (the sample oracle is not compatible with the mock oracle):

```
taproot-assets.experimental.rfq.priceoracleaddress=rfqrpc://tassandra.laisee.org:20590
```

For regtest, signet and testnet you may also deploy your own instance of Tassandra (`https://github.com/liongrass/tassandra`). ([source](../../raw/docs/lightning-network-tools/taproot-assets/rfq.md))

## Conflicts

- **Buy-order price fields.** In the buy order's formal definition, `price_out_asset` is `msat per BTC` and `price_in_asset` is `buxx per BTC`; the calculation directly beneath it says `Y` (asset units per BTC) is "specified by `price_out_asset`" and `M` (mSAT in a BTC) is "specified by `price_in_asset`". ([source](../../raw/docs/lightning-network-tools/taproot-assets/decimal-display.md))
- **`mockoraclesatsperasset` description.** The RFQ guide introduces `mockoraclesatsperasset` with the words "in Taproot Assets units per bitcoin" and then says "To trade one unit per satoshi for example, set the value to 1"; the option name and the example describe satoshis per asset unit, the sentence describes units per bitcoin. ([source](../../raw/docs/lightning-network-tools/taproot-assets/rfq.md))
- **Which file.** The same sentence says the fixed swap rate is set "in the `tapd.conf` file", while the option is printed with the `taproot-assets.` prefix that the guide says is for `lit.conf`. ([source](../../raw/docs/lightning-network-tools/taproot-assets/rfq.md))
