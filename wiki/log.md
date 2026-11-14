# Log

Append-only. One line per operation: date, operation, what changed.
- 2026-11-14 ingest loop: 7 pages (component, 2 services, 4 how-tos) from 43 raw files; checker PASS after 3 rounds.
- 2026-11-14 conflict (loop): `--failurebackoff` default is 24 hours in autoloop.md and 0 in the-loop-cli.md; recorded on [[autoloop]] and [[using-loop]].
- 2026-11-14 conflict (loop): peer-with-loop.md gives the Loop node at 50.112.125.89:9735 in the example and 44.228.158.82:9735 under Mainnet; recorded on [[using-loop]].
- 2026-11-14 conflict (loop): static-loop-in-addresses.md disagrees with itself and the API on timeout, one versus many addresses, channel opens (StaticOpenChannel exists) and command names; recorded on [[static-loop-in-addresses]].
- 2026-11-14 conflict (loop): autoloop.md allows `--type=<in|out>` while the SuggestSwaps page says only loop out suggestions are supported; recorded on [[autoloop]].
