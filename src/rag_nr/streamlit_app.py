"""Streamlit demo: ask a question about the ingested NRs, see the answer with
citations and the retrieved source chunks."""

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from rag_nr.generation import answer_question  # noqa: E402

st.set_page_config(page_title="RAG — Normas Regulamentadoras", page_icon="⚠️")
st.title("RAG — Normas Regulamentadoras")
st.caption("Respostas com citação de fonte, sobre NR-01, NR-05, NR-06, NR-17 e NR-35.")

question = st.text_input("Pergunta", value="Quais EPIs são obrigatórios para trabalho em altura?")

if st.button("Perguntar") and question:
    with st.spinner("Buscando e gerando resposta..."):
        answer, chunks = answer_question(question)
    st.markdown(answer.text)
    with st.expander("Trechos usados como contexto"):
        for c in chunks:
            st.markdown(f"**{c['norma']}, item {c['item']}** (p. {c['pagina']})")
            st.write(c["texto"])
            st.divider()
