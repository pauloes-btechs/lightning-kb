---
title: Debugging, fuzzing and contributing to lnd
type: howto
sources:
  - raw/docs/lightning-network-tools/lnd/debugging_lnd.md
  - raw/docs/lightning-network-tools/lnd/fuzz.md
  - raw/docs/lightning-network-tools/lnd/contribute-to-lnd.md
updated: 2026-11-14
---

# Debugging, fuzzing and contributing to lnd

[[lnd]] ships with a built-in profiler and tunable logging levels. Capturing debug logs and performance data ahead of time helps when submitting a bug report ([source](../../raw/docs/lightning-network-tools/lnd/debugging_lnd.md)).

## Debug logging

Logs are typically at `~/.lnd/logs/bitcoin/mainnet/lnd.log` on Linux, `~/Library/Application Support/Lnd/logs/bitcoin/mainnet` on macOS, or wherever `--logdir` points. By default LND logs 10MB of history and keeps three more blocks of logs, gzip-compressed as `lnd.log.<i>.gz` in the same directory ([source](../../raw/docs/lightning-network-tools/lnd/debugging_lnd.md)).

Adjust in `lnd.conf` ([source](../../raw/docs/lightning-network-tools/lnd/debugging_lnd.md)):

```
logdir=~/.lnd/logs
maxlogfiles=3
maxlogfilesize=10
debuglevel=debug,PEER=info
```

Change the level without a restart with `lncli debuglevel --level=`. Levels, in descending detail: `trace`, `debug`, `info`, `warn`, `error`, `critical`, `off`. List subsystems with `lncli debuglevel --show`, and chain per-subsystem levels, e.g. `debuglevel --level=BTCN=trace,LNWL=debug` ([source](../../raw/docs/lightning-network-tools/lnd/debugging_lnd.md)).

Subsystem codes listed in the guide include `LNWL` (lnwallet), `DISC` (discovery), `NTFN` (chainntnfs), `CHDB` (channeldb), `HSWC` (htlcswitch), `CMGR` (connmgr), `BTCN` (neutrino), `CNCT`/`UTXN`/`BRAR` (contractcourt), `SPHX` (sphinx), `SWPR` (sweep), `SGNR` (signrpc), `WLKT` (walletrpc), `ARPC` (autopilotrpc), `INVC` (invoices), `NANN` (netann), `WTWR` (watchtower), `NTFR` (chainrpc), `IRPC` (invoicesrpc), `CHNF` (channelnotifier), `CHBU` (chanbackup), `PROM` (monitoring), `WTCL` (wtclient), `PRNF` (peernotifier), `CHFD` (chanfunding), `PEER` (peer) and `CHCL` (chancloser) ([source](../../raw/docs/lightning-network-tools/lnd/debugging_lnd.md)).

## Profiling with pprof

Start `lnd` with `--profile` on a free port, or add `profile=9736` to `lnd.conf`. The profiler has negligible overhead unless CPU profiling is explicitly enabled ([source](../../raw/docs/lightning-network-tools/lnd/debugging_lnd.md)):

```
lnd --profile=9736
curl http://localhost:9736/debug/pprof/goroutine?debug=1
curl http://localhost:9736/debug/pprof/profile?seconds=10 > cpu.prof      # CPU
curl http://localhost:9736/debug/pprof/goroutine?debug=2 > goroutine.prof # deadlocks, lock contention
curl http://localhost:9736/debug/pprof/heap > heap.prof                   # memory allocations
go tool pprof -svg cpu.prof > cpu.svg                                     # visualize
```

## Fuzzing

The `fuzz` package has subpackages named after the `lnd` packages they test, each with its own fuzz targets. Build all harnesses with `make fuzz-build` (this creates zip files per target and may take a while); run all harnesses for 30 seconds with `make fuzz-run` ([source](../../raw/docs/lightning-network-tools/lnd/fuzz.md)).

`go-fuzz` prints periodic log lines. `corpus` is the number of corpus items, `crashers` the number of crashing inputs (logged by default in `fuzz/<package>/<harness>/crashers`), and `cover` the edge coverage. A `suppressions` directory holds stack traces to ignore so duplicates are not created ([source](../../raw/docs/lightning-network-tools/lnd/fuzz.md)).

Parameters appended to the make commands ([source](../../raw/docs/lightning-network-tools/lnd/fuzz.md)):

| Parameter | Meaning | Default |
|---|---|---|
| `run_time` | how long each harness runs | 30 seconds |
| `timeout` | max time per testcase before an error | 20 seconds |
| `processes` | number of parallel processes | not stated |
| `pkg` | `lnd` packages to build or fuzz | all: `brontide lnwire wtwire zpay32` |
| `base_workdir` | fuzzer workspace (corpus, crashers, suppressions) | not stated |

`go-fuzz` minimizes the corpus in memory before fuzzing, so a large corpus should not matter. Crashers that affect LND security should be disclosed per the security section of the lnd repository README ([source](../../raw/docs/lightning-network-tools/lnd/fuzz.md)).

## Contributing

LND is open source, published and maintained by Lightning Labs, and follows a development process that values safety, security, reliability and quality above features or speed ([source](../../raw/docs/lightning-network-tools/lnd/contribute-to-lnd.md)).

**As a user:** be ready to provide extensive logs (e.g. debug mode) and profiling data, test in environments like signet, apply patches, and run release candidates early (recommended on signet nodes only) and report bugs ([source](../../raw/docs/lightning-network-tools/lnd/contribute-to-lnd.md)).

**As a developer:** it helps to understand Bitcoin and Lightning at a high level, c-like languages, Go, the domain you contribute to, and to have an appetite for code review. Read the code contribution guidelines, and filter the issue log by labels like 'good first issue', 'up for grabs' or 'beginner'. Code review is an important contribution: start with a small or medium pull request, run it locally, and go through its unit and integration tests. The LND PR Review Club is run by LND core developers ([source](../../raw/docs/lightning-network-tools/lnd/contribute-to-lnd.md)).

**Documentation:** document your setup and tools, report or fix documentation errors with a pull request, and share guides and sample configurations ([source](../../raw/docs/lightning-network-tools/lnd/contribute-to-lnd.md)).

See also: [[running-lnd]], [[lnd-configuration]], [[lnd-sweeper]], [[lnd-recovery]].
