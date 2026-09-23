# Project instructions for Claude

This project follows the rules of the portfolio master plan, with one documented
exception (OpenAI for generation instead of Claude — see
`docs/decisions/0003-openai-for-generation.md`):

1. No client code or data — the corpus is public regulatory text (NRs from
   gov.br), fetched and cited under `data/pdfs/`.
2. No committed secrets — use `.env` (gitignored) and keep `.env.example` up
   to date. `gitleaks` runs on pre-commit and in CI.
3. Every project reports numeric evaluation metrics — see `evals/results.md`.
4. Everything runs with a single command: `docker compose up` or `make run`
   (after a one-time `make ingest`, which needs Supabase credentials).
5. README in English, with a short "Resumo em português" section at the end.
   Header banner + badges matching the other portfolio repos.
6. Small, descriptive commits using Conventional Commits.
7. Prefer simplicity — RRF fusion for hybrid search (same method as
   `hybrid-search-ptbr`), no LangChain/LlamaIndex.

## Layout

- `src/rag_nr/ingest.py` — chunks a PDF by its own item numbering (6.2, 6.2.1, ...).
- `src/rag_nr/ingest_all.py` — full pipeline: extract, chunk, embed, load into
  Supabase. Run once (`make ingest`), free (local embeddings only).
- `src/rag_nr/retrieval.py` — full-text search + vector search (pgvector) + RRF.
- `src/rag_nr/generation.py` — cited answer generation; costs real API money.
- `evals/run_eval.py` — retrieval recall@5 (free) + generation refusal/citation
  accuracy (real API calls) — do not run without the user's awareness of cost.
