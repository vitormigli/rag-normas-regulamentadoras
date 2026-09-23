.PHONY: ingest run demo eval test lint

ingest:
	uv run python -m rag_nr.ingest_all

run:
	uv run uvicorn rag_nr.api:app --host 0.0.0.0 --port 8000 --reload

demo:
	uv run streamlit run src/rag_nr/streamlit_app.py

eval:
	uv run python evals/run_eval.py

test:
	uv run pytest

lint:
	uv run ruff check .
