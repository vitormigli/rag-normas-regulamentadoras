"""Hybrid retrieval over nr_chunks: Postgres full-text search (tsvector) +
pgvector cosine similarity, fused with Reciprocal Rank Fusion — the same
fusion method used in this portfolio's hybrid-search-ptbr, applied here
against a real Postgres/pgvector backend instead of an in-memory index."""

from rag_nr.db import get_client
from rag_nr.embeddings import embed, load_embedding_model


def search_fts(query: str, top_k: int = 10) -> list[dict]:
    client = get_client()
    response = (
        client.table("nr_chunks")
        .select("id,norma,titulo_norma,item,texto,pagina")
        .limit(top_k)
        .text_search("fts", query, options={"type": "web_search", "config": "portuguese"})
        .execute()
    )
    return response.data


def search_dense(query: str, top_k: int = 10, model=None) -> list[dict]:
    client = get_client()
    query_embedding = embed([query], model=model or load_embedding_model())[0]
    response = client.rpc(
        "match_nr_chunks", {"query_embedding": query_embedding, "match_count": top_k}
    ).execute()
    return response.data


def reciprocal_rank_fusion(result_lists: list[list[dict]], k: int = 60) -> list[dict]:
    scores: dict[int, float] = {}
    rows_by_id: dict[int, dict] = {}
    for results in result_lists:
        for rank, row in enumerate(results, start=1):
            scores[row["id"]] = scores.get(row["id"], 0.0) + 1.0 / (k + rank)
            rows_by_id[row["id"]] = row
    ranked_ids = sorted(scores, key=lambda i: -scores[i])
    return [rows_by_id[i] for i in ranked_ids]


def search_hybrid(query: str, top_k: int = 10, model=None) -> list[dict]:
    fts_results = search_fts(query, top_k=max(top_k, 20))
    dense_results = search_dense(query, top_k=max(top_k, 20), model=model)
    fused = reciprocal_rank_fusion([fts_results, dense_results])
    return fused[:top_k]
