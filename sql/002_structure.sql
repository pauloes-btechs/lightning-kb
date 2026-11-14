-- Structured knowledge on top of the page link graph, plus version stamps.
alter table documents add column if not exists version text;   -- e.g. lnd@895118a for API pages
-- Hash of the exact text that was embedded, so an identical chunk is embedded once.
alter table chunks add column if not exists ekey text;
create index if not exists chunks_ekey_idx on chunks(ekey);

-- Typed API graph, parsed (never inferred) from the API reference:
--   product -has_service-> service -has_rpc-> rpc -request/response/uses-> message -contains-> message
create table if not exists entities (
  id      bigserial primary key,
  kind    text not null,                    -- product | service | rpc | message
  name    text not null,
  product text not null,
  doc_id  bigint references documents(id) on delete set null,
  unique (kind, product, name)
);
create table if not exists relations (
  src  bigint not null references entities(id) on delete cascade,
  dst  bigint not null references entities(id) on delete cascade,
  kind text not null,
  primary key (src, dst, kind)
);
create index if not exists relations_dst_idx on relations(dst);
