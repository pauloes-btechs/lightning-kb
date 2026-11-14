-- Plain Postgres + pgvector. Nothing here is Docker-specific, so the same
-- file runs unchanged on Supabase or Neon (./kb push <DATABASE_URL>).
-- {{DIM}} and {{VEC_INDEX}} are filled in at migrate time from EMBED_DIM:
-- up to 2000 dims gets an HNSW index, wider vectors are searched exactly.
create extension if not exists vector;

create table if not exists documents (
  id         bigserial primary key,
  path       text not null unique,          -- e.g. raw/api/api-docs/api/lnd/lightning/get-info.md
  layer      text not null,                 -- raw | wiki
  source     text,                          -- docs | wavelength | api | wiki
  product    text,                          -- lnd, loop, pool, faraday, taproot-assets, lit, ...
  title      text,
  url        text,                          -- canonical source URL (raw layer)
  sha256     text not null,
  updated_at timestamptz not null default now()
);

create table if not exists chunks (
  id        bigserial primary key,
  doc_id    bigint not null references documents(id) on delete cascade,
  ord       int not null,
  heading   text,
  content   text not null,
  tsv       tsvector generated always as
            (to_tsvector('english', coalesce(heading, '') || ' ' || content)) stored,
  embedding vector({{DIM}})
);
create index if not exists chunks_doc_idx on chunks(doc_id);
create index if not exists chunks_tsv_idx on chunks using gin(tsv);
{{VEC_INDEX}}

-- The link graph: wikilinks, markdown links and wiki -> raw citations.
create table if not exists edges (
  src  bigint not null references documents(id) on delete cascade,
  dst  bigint not null references documents(id) on delete cascade,
  kind text not null,                       -- wikilink | mdlink | cites
  primary key (src, dst, kind)
);
create index if not exists edges_dst_idx on edges(dst);

create table if not exists eval_runs (
  id         bigserial primary key,
  created_at timestamptz not null default now(),
  mode       text not null,
  embed_model text not null,
  questions  int not null,
  hit_at_1   real not null,
  hit_at_5   real not null,
  mrr        real not null,
  detail     jsonb not null
);
