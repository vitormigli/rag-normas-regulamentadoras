"""Evaluates retrieval (vector-only vs hybrid, recall@5) for free, then
generation (refusal correctness + citation accuracy) against the real OpenAI
API for the gold question set. Writes results.json and results.md."""

import json
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from dotenv import load_dotenv
from questions import QUESTIONS

load_dotenv()

from rag_nr.embeddings import load_embedding_model  # noqa: E402
from rag_nr.generation import answer_question  # noqa: E402
from rag_nr.retrieval import search_dense, search_hybrid  # noqa: E402

EVALS_DIR = Path(__file__).parent
REFUSAL_PHRASE = "não encontrado"


def recall_at_5(results: list[dict], expected_items: list[str]) -> float:
    if not expected_items:
        return 1.0
    retrieved = {r["item"] for r in results}
    hit = any(item in retrieved for item in expected_items)
    return 1.0 if hit else 0.0


def evaluate_retrieval() -> dict:
    model = load_embedding_model()
    vector_recalls, hybrid_recalls = [], []
    for q in QUESTIONS:
        if not q["answerable"]:
            continue
        dense = search_dense(q["question"], top_k=5, model=model)
        hybrid = search_hybrid(q["question"], top_k=5, model=model)
        vector_recalls.append(recall_at_5(dense, q["expected_items"]))
        hybrid_recalls.append(recall_at_5(hybrid, q["expected_items"]))
    return {
        "vector_only_recall@5": statistics.mean(vector_recalls),
        "hybrid_recall@5": statistics.mean(hybrid_recalls),
        "n_answerable_questions": len(vector_recalls),
    }


def evaluate_generation() -> dict:
    rows = []
    for q in QUESTIONS:
        answer, chunks = answer_question(q["question"], top_k=5)
        said_not_found = REFUSAL_PHRASE in answer.text.lower()

        if q["answerable"]:
            refusal_correct = not said_not_found
            cited_correct_norma = (
                q["expected_norma"] is not None and q["expected_norma"] in answer.text
            )
        else:
            refusal_correct = said_not_found
            cited_correct_norma = None  # not applicable

        rows.append(
            {
                "id": q["id"],
                "question": q["question"],
                "answerable": q["answerable"],
                "answer": answer.text,
                "refusal_correct": refusal_correct,
                "cited_correct_norma": cited_correct_norma,
            }
        )
        print(f"[{q['id']}] refusal_correct={refusal_correct} answerable={q['answerable']}")

    refusal_accuracy = statistics.mean(r["refusal_correct"] for r in rows)
    citation_rows = [r for r in rows if r["cited_correct_norma"] is not None]
    citation_accuracy = (
        statistics.mean(r["cited_correct_norma"] for r in citation_rows) if citation_rows else 0.0
    )
    return {
        "refusal_accuracy": refusal_accuracy,
        "citation_accuracy": citation_accuracy,
        "rows": rows,
    }


def main() -> None:
    print("=== Retrieval (free) ===")
    retrieval_results = evaluate_retrieval()
    print(json.dumps(retrieval_results, indent=2))

    print("\n=== Generation (real API calls) ===")
    generation_results = evaluate_generation()

    summary = {**retrieval_results, **{k: v for k, v in generation_results.items() if k != "rows"}}
    (EVALS_DIR / "results.json").write_text(
        json.dumps(
            {"summary": summary, "rows": generation_results["rows"]}, indent=2, ensure_ascii=False
        ),
        encoding="utf-8",
    )

    lines = ["# RAG Evaluation Results", ""]
    lines.append(
        f"{len(QUESTIONS)} gold questions ({retrieval_results['n_answerable_questions']} "
        f"answerable, {len(QUESTIONS) - retrieval_results['n_answerable_questions']} deliberately "
        "unanswerable / out of scope).\n"
    )
    lines.append("| Stage | Value |")
    lines.append("|---|---|")
    lines.append(f"| Recall@5 — vector only | {retrieval_results['vector_only_recall@5']:.1%} |")
    lines.append(f"| Recall@5 — hybrid (RRF) | {retrieval_results['hybrid_recall@5']:.1%} |")
    lines.append(
        f'| Refusal accuracy (correctly says "não encontrado" or doesn\'t) | '
        f"{generation_results['refusal_accuracy']:.1%} |"
    )
    lines.append(
        f"| Citation accuracy (cites the expected norm) | "
        f"{generation_results['citation_accuracy']:.1%} |"
    )
    (EVALS_DIR / "results.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("\n=== Summary ===")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
