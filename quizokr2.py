import streamlit as st
import pandas as pd
import smtplib
import qrcode
import io

st.set_page_config(page_title="🧩 Quiz OKRs no BI", page_icon="🧩", layout="centered")

st.title("🧩 Quiz 2 – Aplicação Prática de OKRs no BI")
st.subheader("Objetivo: Testar a capacidade de reconhecer boas práticas de construção e desdobramento de OKRs.")

score = 0

q1 = st.radio("1. Na prática, um bom Objetivo deve ser:", [
    "a) Quantificável",
    "b) Detalhado tecnicamente",
    "c) Inspirador e qualitativo",
    "d) Curto e irrelevante"
])
if q1 == "c) Inspirador e qualitativo":
    score += 1

q2 = st.radio("2. Qual destes seria um KR adequado para um time de Engenharia de Dados?", [
    "a) Aumentar o engajamento em redes sociais",
    "b) Reduzir tempo de processamento de pipeline de 4h para 15 minutos",
    "c) Publicar dashboards no mural da empresa",
    "d) Treinar 5 novos colaboradores"
])
if q2 == "b) Reduzir tempo de processamento de pipeline de 4h para 15 minutos":
    score += 1

q3 = st.radio("3. O que é o cascateamento de OKRs?", [
    "a) A ordenação de KRs por urgência",
    "b) O alinhamento dos OKRs da empresa até o nível individual",
    "c) A priorização de tarefas operacionais",
    "d) A divisão dos KPIs entre setores"
])
if q3 == "b) O alinhamento dos OKRs da empresa até o nível individual":
    score += 1

q4 = st.radio("4. Qual destas práticas deve ser evitada ao construir OKRs?", [
    "a) Alinhar com os objetivos da empresa",
    "b) Ter mais de 5 KRs por objetivo",
    "c) Ser mensurável",
    "d) Estar conectada à estratégia do call center"
])
if q4 == "b) Ter mais de 5 KRs por objetivo":
    score += 1

q5 = st.radio("5. Um bom resultado-chave (KR) deve ser:", [
    "a) Inspirador e qualitativo",
    "b) Vago, para dar margem",
    "c) Mensurável e específico",
    "d) Geral e de longo prazo"
])
if q5 == "c) Mensurável e específico":
    score += 1

q6 = st.radio("6. Na construção de OKRs, o primeiro passo é:", [
    "a) Definir KPIs",
    "b) Reunir o time",
    "c) Entender a estratégia do negócio",
    "d) Escolher as ferramentas"
])
if q6 == "c) Entender a estratégia do negócio":
    score += 1

q7 = st.radio("7. OKRs bem construídos ajudam equipes de dados a:", [
    "a) Reduzirem o número de reuniões",
    "b) Ignorar demandas ad-hoc",
    "c) Ter foco no que mais importa em cada ciclo",
    "d) Automatizar todo o trabalho"
])
if q7 == "c) Ter foco no que mais importa em cada ciclo":
    score += 1

q8 = st.radio("8. Qual métrica é típica de Call Centers e pode ser um KR?", [
    "a) TMA – Tempo Médio de Atendimento",
    "b) ROI – Retorno sobre investimento",
    "c) RPA – Automação Robótica",
    "d) SQL – Linguagem de banco de dados"
])
if q8 == "a) TMA – Tempo Médio de Atendimento":
    score += 1

q9 = st.radio("9. O que significa “Adoção de Insights” como métrica?", [
    "a) Quantos dashboards foram criados",
    "b) Quantas pessoas leram os relatórios",
    "c) Percentual de recomendações baseadas em dados implementadas",
    "d) Quantas visualizações teve um gráfico"
])
if q9 == "c) Percentual de recomendações baseadas em dados implementadas":
    score += 1

q10 = st.radio("10. Na Master Class, o exercício prático inclui:", [
    "a) Criar um dashboard",
    "b) Definir OKRs com base em um cenário real",
    "c) Programar scripts",
    "d) Traduzir metas em inglês"
])
if q10 == "b) Definir OKRs com base em um cenário real":
    score += 1

if st.button("Enviar respostas"):
    st.success(f"Você acertou {score} de 10 perguntas!")
    if score == 10:
        st.balloons()
    elif score >= 7:
        st.info("Parabéns! Você está aplicando bem os conceitos de OKRs no BI.")
    elif score >= 4:
        st.warning("Quase lá! Reforce os conceitos e tente novamente.")
    else:
        st.error("Hora de revisar os fundamentos e práticas de OKRs no BI.")
