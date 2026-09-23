# 3. OpenAI instead of Claude for answer generation

## Status

Accepted

## Context

Same situation as `sales-agent-evals` elsewhere in this portfolio: this
project was built after the Anthropic API budget for the portfolio work was
nearly exhausted, with an OpenAI key available instead. Retrieval (chunking,
embeddings, full-text and vector search) has no model dependency either way —
only `src/rag_nr/generation.py` calls an LLM.

## Decision

Use the OpenAI SDK and `gpt-4o-mini` for the cited-answer generation step.

## Consequences

- Two repos in this portfolio use OpenAI instead of Claude for generation
  (this one and `sales-agent-evals`) — worth being upfront about, not glossed
  over, in interviews.
- `generate_answer()` only touches the OpenAI client in one place
  (`client.chat.completions.create` and how it reads the response) — porting
  back to `anthropic`'s Messages API is a contained, mechanical change.
