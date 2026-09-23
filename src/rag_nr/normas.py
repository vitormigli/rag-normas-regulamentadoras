"""Registry of the ingested NRs (Normas Regulamentadoras) — public documents
from gov.br, Ministério do Trabalho e Emprego. No client/company data."""

NORMAS: dict[str, dict] = {
    "NR-01": {
        "numero": 1,
        "titulo": "Disposições Gerais e Gerenciamento de Riscos Ocupacionais",
        "arquivo": "nr-01.pdf",
    },
    "NR-05": {
        "numero": 5,
        "titulo": "Comissão Interna de Prevenção de Acidentes e de Assédio",
        "arquivo": "nr-05.pdf",
    },
    "NR-06": {
        "numero": 6,
        "titulo": "Equipamento de Proteção Individual",
        "arquivo": "nr-06.pdf",
    },
    "NR-17": {
        "numero": 17,
        "titulo": "Ergonomia",
        "arquivo": "nr-17.pdf",
    },
    "NR-35": {
        "numero": 35,
        "titulo": "Trabalho em Altura",
        "arquivo": "nr-35.pdf",
    },
}
