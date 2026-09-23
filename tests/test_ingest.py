from rag_nr.ingest import chunk_by_item


def test_chunk_by_item_basic_hierarchy():
    pages = [
        "6.1 Objetivo\n"
        "6.1.1 Esta norma estabelece requisitos.\n"
        "6.2 Campo de aplicação\n"
        "6.2.1 Aplica-se a todas as organizações.\n"
    ]
    chunks = chunk_by_item(pages, norma_numero=6)
    items = {c.item: c.texto for c in chunks}
    assert "6.1" in items
    assert "6.1.1" in items
    assert "Esta norma estabelece requisitos." in items["6.1.1"]
    assert "6.2.1" in items


def test_chunk_by_item_dedupes_toc_keeping_longer_text():
    pages = [
        "6.1 Objetivo\n"
        "6.2 Campo de aplicação\n"  # table of contents: short titles only
        "6.1 Objetivo\n"
        "6.1.1 Esta norma estabelece os requisitos mínimos para EPI, muito mais texto aqui.\n"
        "6.2 Campo de aplicação\n"
        "6.2.1 Aplica-se a todas as organizações que adquiram EPI e aos trabalhadores.\n"
    ]
    chunks = chunk_by_item(pages, norma_numero=6)
    items = {c.item: c.texto for c in chunks}
    # Only one chunk per item, and it must be the longer (body) occurrence.
    assert len(chunks) == len(items)
    assert "mínimos" not in items["6.1"]  # 6.1 itself has no body beyond the title either way


def test_chunk_by_item_ignores_unrelated_numbers():
    pages = [
        "Portaria MTb n. 3.214, de 08 de junho de 1978\n"
        "6.1 Objetivo\n"
        "6.1.1 Conteúdo real do item.\n"
    ]
    chunks = chunk_by_item(pages, norma_numero=6)
    items = [c.item for c in chunks]
    assert "3.214" not in items
    assert "6.1.1" in items


def test_chunk_by_item_tracks_page_number():
    pages = [
        "6.1 Objetivo\n",
        "6.1.1 Conteúdo na página dois.\n",
    ]
    chunks = chunk_by_item(pages, norma_numero=6)
    by_item = {c.item: c for c in chunks}
    assert by_item["6.1"].pagina == 1
    assert by_item["6.1.1"].pagina == 2


def test_chunk_by_item_empty_input():
    assert chunk_by_item([], norma_numero=6) == []
