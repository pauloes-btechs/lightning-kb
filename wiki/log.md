# Log

Append-only. One line per operation: date, operation, what changed.
- 2026-11-14 ingest loop: 7 pages (component, 2 services, 4 how-tos) from 43 raw files; checker PASS after 3 rounds.
- 2026-11-14 conflict (loop): `--failurebackoff` default is 24 hours in autoloop.md and 0 in the-loop-cli.md; recorded on [[autoloop]] and [[using-loop]].
- 2026-11-14 conflict (loop): peer-with-loop.md gives the Loop node at 50.112.125.89:9735 in the example and 44.228.158.82:9735 under Mainnet; recorded on [[using-loop]].
- 2026-11-14 conflict (loop): static-loop-in-addresses.md disagrees with itself and the API on timeout, one versus many addresses, channel opens (StaticOpenChannel exists) and command names; recorded on [[static-loop-in-addresses]].
- 2026-11-14 conflict (loop): autoloop.md allows `--type=<in|out>` while the SuggestSwaps page says only loop out suggestions are supported; recorded on [[autoloop]].
- 2026-11-14 ingest faraday, aperture: 8 pages (2 components, 1 service, 5 how-tos) from 20 raw files; checker PASS after 2 rounds.
- 2026-11-14 conflict (faraday): REST port is 8082 in the API overview and 8466 in RPC example requests; recorded on [[faraday]] and [[faraday-server]].
- 2026-11-14 conflict (faraday): ThresholdRecommendations `metric` description names two values while the enum lists five; recorded on [[faraday-server]].
- 2026-11-14 conflict (faraday): `frcli insights` example output and the ChannelInsight message list different fields; recorded on [[using-faraday]].
- 2026-11-14 conflict (faraday): guide's `--enable_fiat` flag versus the NodeAudit `disable_fiat` field; recorded on [[using-faraday]].
- 2026-11-14 conflict (faraday): guide says `frcli outliers` shares flags with `frcli threshold`, but their --help samples show `--incoming_volume`/`--outgoing_volume` against `--incoming`/`--outgoing`; recorded on [[using-faraday]].
- 2026-11-14 conflict (aperture): step-by-step.md says each L402 costs 21 satoshis while its config sets `price: 2`; recorded on [[aperture-pricing-and-services]].
- 2026-11-14 conflict (aperture): expiry via `timeout: 3600` (step-by-step.md) versus `constraints: "valid_until"` (pricing.md); recorded on [[aperture-pricing-and-services]].
- 2026-11-14 conflict (aperture): connection phrase is eight words in lnc-backend.md and 10 words in mailbox.md; recorded on [[aperture-mailbox-and-lnc]].
- 2026-11-14 conflict (aperture): mailbox.md spells its placeholder domain three ways and its autocert cache directory two ways; recorded on [[aperture-mailbox-and-lnc]].
- 2026-11-14 conflict (aperture): `tlspath` and `macdir` home paths differ between get-aperture.md and step-by-step.md; recorded on [[running-aperture]].
