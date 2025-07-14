
import streamlit as st

st.set_page_config(page_title="Quiz OKRs", page_icon="🎯", layout="centered")
st.title("🎯 Quiz 1 – Fundamentos dos OKRs")
st.subheader("Objetivo: Avaliar a compreensão dos conceitos principais de OKRs e suas diferenças com KPIs.")

score = 0

q1 = st.radio("1. O que significa a sigla OKR?", [
    "a) Objectives and Knowledge Rate",
    "b) Organizational Key Reports",
    "c) Objectives and Key Results",
    "d) Operational Key Resources"
])
if q1 == "c) Objectives and Key Results":
    score += 1

q2 = st.radio("2. Qual das opções representa uma característica dos OKRs?", [
    "a) São metas conservadoras",
    "b) Têm ciclos longos e fixos",
    "c) São orientados ao passado",
    "d) São ambiciosos e focados em transformação"
])
if q2 == "d) São ambiciosos e focados em transformação":
    score += 1

q3 = st.radio("3. Qual a principal diferença entre KPIs e OKRs?", [
    "a) KPIs são qualitativos e OKRs são quantitativos",
    "b) KPIs monitoram o presente e OKRs direcionam o futuro",
    "c) Ambos são iguais",
    "d) OKRs são mais técnicos"
])
if q3 == "b) KPIs monitoram o presente e OKRs direcionam o futuro":
    score += 1

q4 = st.radio("4. Um bom objetivo em um OKR deve ser:", [
    "a) Técnico e detalhado",
    "b) Ambicioso e inspirador",
    "c) Baseado em backlog",
    "d) Específico e conservador"
])
if q4 == "b) Ambicioso e inspirador":
    score += 1

q5 = st.radio("5. Qual é a quantidade ideal de Resultados-Chave (KRs) por Objetivo?", [
    "a) 1",
    "b) 10",
    "c) 2 a 5",
    "d) Quantos forem possíveis"
])
if q5 == "c) 2 a 5":
    score += 1

q6 = st.radio("6. Qual exemplo abaixo é um KPI e não um OKR?", [
    "a) Aumentar NPS de 35 para 55",
    "b) Implementar 3 modelos preditivos",
    "c) Churn Rate",
    "d) Transformar o BI em parceiro estratégico"
])
if q6 == "c) Churn Rate":
    score += 1

q7 = st.radio("7. Qual tipo de objetivo representa uma meta ambiciosa que pode não ser totalmente alcançada?", [
    "a) Estratégico",
    "b) Tático",
    "c) Roofshot",
    "d) Moonshot"
])
if q7 == "d) Moonshot":
    score += 1

q8 = st.radio("8. Qual afirmativa está INCORRETA sobre metas tradicionais?", [
    "a) Geralmente são conservadoras",
    "b) São pouco adaptáveis",
    "c) Têm foco em impacto e transformação",
    "d) São isoladas por departamento"
])
if q8 == "c) Têm foco em impacto e transformação":
    score += 1

q9 = st.radio("9. Ciclos de OKRs geralmente ocorrem em qual frequência?", [
    "a) Anual",
    "b) Quinzenal",
    "c) Mensal ou Trimestral",
    "d) Semestral"
])
if q9 == "c) Mensal ou Trimestral":
    score += 1

q10 = st.radio("10. Por que os OKRs são mais eficazes do que metas tradicionais em ambientes ágeis?", [
    "a) Porque são mais simples",
    "b) Porque são fixos",
    "c) Porque promovem foco, adaptação e impacto",
    "d) Porque não precisam de acompanhamento"
])
if q10 == "c) Porque promovem foco, adaptação e impacto":
    score += 1

if st.button("Enviar respostas"):
    st.success(f"Você acertou {score} de 10 perguntas!")
    if score == 10:
        st.balloons()
    elif score >= 7:
        st.info("Muito bem! Você compreende bem os fundamentos dos OKRs.")
    elif score >= 4:
        st.warning("Você está no caminho certo, mas vale revisar alguns conceitos.")
    else:
        st.error("É recomendável revisar os conceitos fundamentais de OKRs.")
