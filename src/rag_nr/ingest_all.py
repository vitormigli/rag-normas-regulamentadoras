"""Ingests every PDF in data/pdfs/ into the nr_chunks table: extract, chunk by
item number, embed locally, upsert. Run once (or after changing the PDFs)."""

from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from rag_nr.db import get_client  # noqa: E402
from rag_nr.embeddings import embed, load_embedding_model  # noqa: E402
from rag_nr.ingest import ingest_pdf  # noqa: E402
from rag_nr.normas import NORMAS  # noqa: E402

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "pdfs"


def main() -> None:
    client = get_client()
    model = load_embedding_model()

    client.table("nr_chunks").delete().neq("id", 0).execute()

    total = 0
    for norma_id, meta in NORMAS.items():
        pdf_path = DATA_DIR / meta["arquivo"]
        chunks = ingest_pdf(pdf_path, meta["numero"])
        print(f"{norma_id}: {len(chunks)} chunks from {pdf_path.name}")

        embeddings = embed([c.texto for c in chunks], model=model)
        rows = [
            {
                "norma": norma_id,
                "titulo_norma": meta["titulo"],
                "item": chunk.item,
                "texto": chunk.texto,
                "pagina": chunk.pagina,
                "embedding": embedding,
            }
            for chunk, embedding in zip(chunks, embeddings, strict=True)
        ]
        client.table("nr_chunks").insert(rows).execute()
        total += len(rows)

    print(f"Ingested {total} chunks total.")


if __name__ == "__main__":
    main()
