"""Gold question set for the RAG eval. `expected_items` lists item codes a
good retrieval should surface (used for retrieval recall@5); `answerable`
marks whether the ingested corpus should let the model answer at all
(used for the refusal-correctness metric)."""

QUESTIONS: list[dict] = [
    {
        "id": "q01",
        "question": "O que é considerado trabalho em altura segundo a NR-35?",
        "answerable": True,
        "expected_norma": "NR-35",
        "expected_items": ["35.1.1"],
    },
    {
        "id": "q02",
        "question": "Qual a carga horária mínima do treinamento inicial para trabalho em altura?",
        "answerable": True,
        "expected_norma": "NR-35",
        "expected_items": ["35.4.2.1"],
    },
    {
        "id": "q03",
        "question": "O que é a Análise de Risco (AR) no contexto de trabalho em altura?",
        "answerable": True,
        "expected_norma": "NR-35",
        "expected_items": ["35.5.5", "35.5.5.1"],
    },
    {
        "id": "q04",
        "question": "Quem é considerado fabricante de EPI para efeitos da NR-06?",
        "answerable": True,
        "expected_norma": "NR-06",
        "expected_items": ["6.2.1.1"],
    },
    {
        "id": "q05",
        "question": "Quais são as responsabilidades do trabalhador em relação ao uso de EPI?",
        "answerable": True,
        "expected_norma": "NR-06",
        "expected_items": ["6.6"],
    },
    {
        "id": "q06",
        "question": "O que é a CIPA segundo a NR-05?",
        "answerable": True,
        "expected_norma": "NR-05",
        "expected_items": ["5.1", "5.1.1"],
    },
    {
        "id": "q07",
        "question": (
            "Como deve ser implementado o gerenciamento de riscos ocupacionais "
            "nos estabelecimentos, segundo a NR-01?"
        ),
        "answerable": True,
        "expected_norma": "NR-01",
        "expected_items": ["1.5.3.1"],
    },
    {
        "id": "q08",
        "question": "O que a NR-17 diz sobre organização do trabalho?",
        "answerable": True,
        "expected_norma": "NR-17",
        "expected_items": ["17.4.1"],
    },
    {
        "id": "q09",
        "question": "É permitido trabalho em altura sob condições meteorológicas adversas?",
        "answerable": True,
        "expected_norma": "NR-35",
        "expected_items": ["35.5.4"],
    },
    {
        "id": "q10",
        "question": (
            "O gerenciamento de riscos ocupacionais deve constituir qual "
            "programa, segundo a NR-01?"
        ),
        "answerable": True,
        "expected_norma": "NR-01",
        "expected_items": ["1.5.3.1.1"],
    },
    {
        "id": "q11",
        "question": "Quem considera-se importador de EPI segundo a NR-06?",
        "answerable": True,
        "expected_norma": "NR-06",
        "expected_items": ["6.2.1.2"],
    },
    {
        "id": "q12",
        "question": (
            "O procedimento operacional para trabalho em altura rotineiro "
            "deve conter o quê?"
        ),
        "answerable": True,
        "expected_norma": "NR-35",
        "expected_items": ["35.5.6.1"],
    },
    {
        "id": "q13",
        "question": "Qual o valor do adicional de insalubridade para grau médio?",
        "answerable": False,
        "expected_norma": None,
        "expected_items": [],
    },
    {
        "id": "q14",
        "question": "Quais são as regras de exame demissional previstas no PCMSO?",
        "answerable": False,
        "expected_norma": None,
        "expected_items": [],
    },
    {
        "id": "q15",
        "question": "Qual o prazo de validade da CNH para motoristas profissionais?",
        "answerable": False,
        "expected_norma": None,
        "expected_items": [],
    },
    {
        "id": "q16",
        "question": (
            "Quais EPIs são obrigatórios especificamente para trabalho em "
            "altura segundo a NR-35?"
        ),
        "answerable": False,
        "expected_norma": None,
        "expected_items": [],
    },
]
