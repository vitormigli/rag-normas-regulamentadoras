"""Generates an answer grounded in retrieved NR chunks, with citations, using
OpenAI (see docs/decisions/0003-openai-for-generation.md for why — budget,
not a stack choice). Explicitly instructed to say "não encontrado" rather
than guess when the retrieved context doesn't actually answer the question."""

from dataclasses import dataclass

from openai import OpenAI

DEFAULT_MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = """Você responde perguntas sobre Normas Regulamentadoras (NRs) \
brasileiras de segurança do trabalho, usando SOMENTE os trechos fornecidos como \
contexto. Regras obrigatórias:

- Cite a norma e o item de cada afirmação, no formato (NR-XX, item Y.Y.Y).
- Se o contexto fornecido não contém a resposta, responda exatamente: \
"Não encontrado nas normas consultadas." Não tente adivinhar ou usar \
conhecimento geral sobre NRs que não esteja no contexto.
- Seja direto e objetivo, em português.
"""


@dataclass
class Answer:
    text: str
    input_tokens: int
    output_tokens: int


def _format_context(chunks: list[dict]) -> str:
    parts = []
    for c in chunks:
        parts.append(f"[{c['norma']}, item {c['item']}]\n{c['texto']}")
    return "\n\n".join(parts)


def generate_answer(
    question: str,
    chunks: list[dict],
    *,
    client: OpenAI | None = None,
    model: str = DEFAULT_MODEL,
) -> Answer:
    client = client or OpenAI()
    context = _format_context(chunks)
    prompt = (
        f"Contexto:\n{context}\n\n"
        f"Pergunta: {question}\n\n"
        "Responda usando apenas o contexto acima, com citações (NR-XX, item Y.Y.Y)."
    )
    response = client.chat.completions.create(
        model=model,
        max_tokens=500,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )
    text = response.choices[0].message.content or ""
    return Answer(
        text=text,
        input_tokens=response.usage.prompt_tokens,
        output_tokens=response.usage.completion_tokens,
    )


def answer_question(
    question: str, *, top_k: int = 5, model: str = DEFAULT_MODEL
) -> tuple[Answer, list[dict]]:
    from rag_nr.retrieval import search_hybrid

    chunks = search_hybrid(question, top_k=top_k)
    answer = generate_answer(question, chunks, model=model)
    return answer, chunks


if __name__ == "__main__":
    import sys

    q = sys.argv[1] if len(sys.argv) > 1 else "Quais EPIs são obrigatórios para trabalho em altura?"
    ans, chunks = answer_question(q)
    print(ans.text)
    print("\nFontes:", [f"{c['norma']} {c['item']}" for c in chunks])
