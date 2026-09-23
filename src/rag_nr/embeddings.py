"""Local embedding model (same family used in hybrid-search-ptbr elsewhere in
this portfolio) — the only free, zero-marginal-cost step in this pipeline."""

from functools import lru_cache

EMBEDDING_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"


@lru_cache(maxsize=1)
def load_embedding_model():
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(EMBEDDING_MODEL_NAME)


def embed(texts: list[str], model=None) -> list[list[float]]:
    model = model or load_embedding_model()
    return model.encode(texts).tolist()
