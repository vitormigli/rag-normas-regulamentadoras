# 1. Chunk by the document's own item numbering, not fixed-size windows

## Status

Accepted

## Context

NRs are written as a strict hierarchy: `6.2` → `6.2.1` → `6.2.1.1`. A citation
that says "NR-06, item 6.5.1" is directly checkable against the real PDF — a
citation that says "chunk 14 of 48" is not.

## Decision

`src/rag_nr/ingest.py` finds every line starting with `<norma_numero>.<n>...`
and treats the span between one match and the next as that item's chunk. No
fixed token/character window anywhere.

## Consequences

- Citations map onto the document a person would actually go read.
- Real complication found via testing, not assumed: each NR's PDF also
  contains a table of contents that repeats every item number with just its
  short title before the real body appears — same item number, twice. Fixed by
  keeping whichever occurrence has more text (the body, not the TOC line).
- Another real complication: NR-01 has an annex whose *own* numbering restarts
  at `1.1` and collides with the main body's `1.1`–`1.9`. The
  keep-the-longer-text heuristic isn't guaranteed to pick the main body over
  the annex in every case — documented as a known limitation rather than
  silently ignored (see README → Limitations).
