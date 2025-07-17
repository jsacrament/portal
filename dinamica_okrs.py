# app_dinamica_okrs.py

import streamlit as st

st.title("Dinâmica Prática: Criando OKRs Reais no Call Center")

st.header("1. Apresentação do Cenário")
st.info("""
Você faz parte da equipe de dados de um grande call center nacional. Nos últimos meses, a diretoria percebeu que:
- O tempo médio de atendimento aumentou.
- A rotatividade dos operadores está alta.
- Clientes reclamam de demora na resolução dos problemas.

Seu desafio: propor OKRs que ajudem a equipe de dados a contribuir para a melhoria dos resultados do call center.
""")

st.header("2. Exercício 1: Identificação dos Problemas")
problemas = st.text_area("Liste os principais problemas identificados:", height=80)

st.header("3. Exercício 2: Definição dos Objetivos (O)")
objetivo1 = st.text_input("Objetivo 1:")
objetivo2 = st.text_input("Objetivo 2 (opcional):")

st.header("4. Exercício 3: Resultados-Chave (Key Results)")
st.markdown("**Para cada objetivo, crie de 2 a 3 Resultados-Chave mensuráveis.**")

st.subheader("Para Objetivo 1")
kr1_1 = st.text_input("KR1 para Objetivo 1:")
kr1_2 = st.text_input("KR2 para Objetivo 1:")
kr1_3 = st.text_input("KR3 para Objetivo 1 (opcional):")

if objetivo2:
    st.subheader("Para Objetivo 2")
    kr2_1 = st.text_input("KR1 para Objetivo 2:")
    kr2_2 = st.text_input("KR2 para Objetivo 2:")
    kr2_3 = st.text_input("KR3 para Objetivo 2 (opcional):")

st.header("5. Apresentação e Feedback")
apresentacao = st.text_area("Como você apresentaria seus OKRs ao grupo? Faça um breve resumo:", height=70)
feedback = st.text_area("Anote feedbacks ou sugestões recebidas:", height=70)

st.header("6. Refinamento dos OKRs")
refino = st.text_area("Com base nos feedbacks, faça ajustes ou melhorias em seus OKRs:", height=80)

st.header("7. Visualização Final dos OKRs")

if st.button("Mostrar OKRs Finais"):
    st.markdown("### OKRs Finais")
    st.markdown(f"**Problemas Identificados:** {problemas}")
    st.markdown(f"**Objetivo 1:** {objetivo1}")
    st.markdown(f"- KR1: {kr1_1}")
    st.markdown(f"- KR2: {kr1_2}")
    if kr1_3:
        st.markdown(f"- KR3: {kr1_3}")
    if objetivo2:
        st.markdown(f"**Objetivo 2:** {objetivo2}")
        st.markdown(f"- KR1: {kr2_1}")
        st.markdown(f"- KR2: {kr2_2}")
        if kr2_3:
            st.markdown(f"- KR3: {kr2_3}")
    st.markdown(f"**Refinamentos Finais:** {refino}")

st.header("8. Debriefing")
st.markdown("""
- O que foi mais difícil: definir objetivos estratégicos ou mensurar resultados?
- Como a clareza nos OKRs pode impactar os resultados do time de dados?
- Você vê aplicação imediata dessa metodologia na sua rotina de trabalho?
""")
