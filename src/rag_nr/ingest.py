"""Extracts text from an NR PDF and chunks it by its own item/subitem numbering
(e.g. 6.2, 6.2.1, 6.2.1.1) — the structure the norms are written in, so a
citation like "NR-06, item 6.3.2" maps directly onto how a person would look
it up in the real document."""

import re
from dataclasses import dataclass
from pathlib import Path

import pdfplumber


@dataclass
class Chunk:
    item: str
    texto: str
    pagina: int


def extract_pages(pdf_path: Path) -> list[str]:
    with pdfplumber.open(pdf_path) as pdf:
        return [page.extract_text() or "" for page in pdf.pages]


def chunk_by_item(pages: list[str], norma_numero: int) -> list[Chunk]:
    """Splits the document into one chunk per top-level item match
    (e.g. `6.2`, `6.2.1`, `6.2.1.1`), using only items that start with this
    norm's own number — which also skips the preamble/publication-history
    page, since it has no lines starting with e.g. "6.<n>"."""
    full_text = ""
    page_starts: list[tuple[int, int]] = []
    for i, page_text in enumerate(pages):
        page_starts.append((len(full_text), i + 1))
        full_text += page_text + "\n"

    pattern = re.compile(rf"(?m)^({norma_numero}\.\d+(?:\.\d+){{0,4}})[ \t]+")
    matches = list(pattern.finditer(full_text))

    def page_for_offset(offset: int) -> int:
        page = 1
        for start, page_num in page_starts:
            if start <= offset:
                page = page_num
            else:
                break
        return page

    raw_chunks: list[Chunk] = []
    for idx, match in enumerate(matches):
        item = match.group(1)
        text_start = match.end()
        text_end = matches[idx + 1].start() if idx + 1 < len(matches) else len(full_text)
        texto = full_text[text_start:text_end].strip()
        texto = re.sub(r"\s+", " ", texto)
        if not texto:
            continue
        raw_chunks.append(Chunk(item=item, texto=texto, pagina=page_for_offset(match.start())))

    # The document's own table of contents repeats every item number with just
    # its short title before the real body text appears — same item, appears
    # twice. Keep whichever occurrence has the most text (the body, not the
    # one-line TOC entry).
    best_by_item: dict[str, Chunk] = {}
    for chunk in raw_chunks:
        current = best_by_item.get(chunk.item)
        if current is None or len(chunk.texto) > len(current.texto):
            best_by_item[chunk.item] = chunk

    def item_sort_key(item: str) -> tuple[int, ...]:
        return tuple(int(p) for p in item.split("."))

    return sorted(best_by_item.values(), key=lambda c: item_sort_key(c.item))


def ingest_pdf(pdf_path: Path, norma_numero: int) -> list[Chunk]:
    pages = extract_pages(pdf_path)
    return chunk_by_item(pages, norma_numero)
