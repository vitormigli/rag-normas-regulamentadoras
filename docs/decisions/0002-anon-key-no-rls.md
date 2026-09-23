# 2. Anon key, RLS left off

## Status

Accepted — scoped to this project's data, not a general recommendation.

## Context

Supabase's service_role key (which bypasses Row Level Security) isn't exposed
by the Supabase MCP tooling used to provision this project, and wasn't needed:
the entire `nr_chunks` table is public regulatory text with no user data, no
multi-tenancy, and no write path exposed to anyone but the one-time ingestion
script.

## Decision

Use the anon key for both ingestion and querying. Do not enable Row Level
Security on `nr_chunks`.

## Consequences

- Anyone with the anon key (which lives in `.env`, gitignored) could technically
  write to this table over PostgREST. Acceptable here because there is nothing
  sensitive to protect and no cost to a bad write beyond re-running ingestion.
- This is *not* the pattern to copy for a project with real user data — that
  needs RLS policies and a service_role key kept server-side, never shipped to
  a client.
