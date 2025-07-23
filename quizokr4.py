import streamlit as st

st.set_page_config(page_title="🚀 Quiz Prático de OKRs", page_icon="🚀", layout="centered")

st.title("🚀 Quiz 4 – OKRs na Prática: Casos Reais e Decisões")
st.subheader("Objetivo: Avaliar a aplicação de OKRs em contextos operacionais e tomada de decisão.")

score = 0

q1 = st.radio("1. Você é líder de BI e quer aumentar o uso de dashboards na operação. Qual KR seria mais adequado?", [
    "a) Publicar novos relatórios diariamente",
    "b) Aumentar o uso ativo dos dashboards de 40% para 80%",
    "c) Criar uma nova base de dados",
    "d) Treinar um estagiário de dados"
])
if q1 == "b) Aumentar o uso ativo dos dashboards de 40% para 80%":
    score += 1

q2 = st.radio("2. Sua equipe de dados demora 5 horas para atualizar os indicadores diários. Qual objetivo faria sentido?", [
    "a) Reduzir o tempo de processamento do pipeline para 15 minutos",
    "b) Aumentar a satisfação da equipe de RH",
    "c) Trocar de ferramenta de BI",
    "d) Implementar um novo CRM"
])
if q2 == "a) Reduzir o tempo de processamento do pipeline para 15 minutos":
    score += 1

q3 = st.radio("3. Você tem 12 métricas em um único OKR. Qual armadilha você caiu?", [
    "a) Boa governança",
    "b) Excesso de indicadores",
    "c) Foco técnico",
    "d) Estratégia top-down"
])
if q3 == "b) Excesso de indicadores":
    score += 1

q4 = st.radio("4. Um gestor quer que os analistas respondam chamados ad-hoc mesmo durante o ciclo de OKRs. O que você faz?", [
    "a) Ignora os OKRs",
    "b) Define prioridades no ciclo e negocia entregas",
    "c) Cria mais dashboards para justificar",
    "d) Faz tudo ao mesmo tempo"
])
if q4 == "b) Define prioridades no ciclo e negocia entregas":
    score += 1

q5 = st.radio("5. Qual dessas alternativas representa uma métrica técnica que pode ser usada como KR?", [
    "a) Tempo médio de atendimento (TMA)",
    "b) Lucro líquido do trimestre",
    "c) Número de campanhas de marketing",
    "d) Salário médio da equipe"
])
if q5 == "a) Tempo médio de atendimento (TMA)":
    score += 1

q6 = st.radio("6. Seu objetivo é 'Elevar a confiança nos dados para decisões operacionais'. Qual KR seria adequado?", [
    "a) Aumentar cobertura de testes automatizados de 40% para 90%",
    "b) Criar mais dashboards",
    "c) Diminuir o backlog de chamados para metade",
    "d) Reduzir o headcount da equipe"
])
if q6 == "a) Aumentar cobertura de testes automatizados de 40% para 90%":
    score += 1

q7 = st.radio("7. Você precisa acompanhar o progresso dos OKRs semanalmente. Qual ferramenta usaria?", [
    "a) Painel com status dos KRs",
    "b) Relatório em papel",
    "c) Tabela dinâmica no Excel",
    "d) Apontamento em agenda pessoal"
])
if q7 == "a) Painel com status dos KRs":
    score += 1

q8 = st.radio("8. Ao revisar os OKRs, a equipe percebe que atingiu 100% de todos os KRs facilmente. O que isso indica?", [
    "a) Excelente estratégia",
    "b) Faltou ambição nos objetivos",
    "c) Falha de comunicação",
    "d) Métricas mal definidas"
])
if q8 == "b) Faltou ambição nos objetivos":
    score += 1

q9 = st.radio("9. Seu call center teve queda no NPS. Qual KR pode ajudar?", [
    "a) Implementar 2 modelos preditivos para identificar causas do NPS",
    "b) Reduzir o número de agentes",
    "c) Automatizar relatórios",
    "d) Trocar todos os líderes"
])
if q9 == "a) Implementar 2 modelos preditivos para identificar causas do NPS":
    score += 1

q10 = st.radio("10. Qual papel é responsável por transformar dados brutos em insights estratégicos para os OKRs?", [
    "a) Analista de RH",
    "b) Gestor Financeiro",
    "c) Profissional de dados",
    "d) Assistente de suporte"
])
if q10 == "c) Profissional de dados":
    score += 1

if st.button("Enviar respostas"):
    st.success(f"Você acertou {score} de 10 perguntas!")
    if score == 10:
        st.balloons()
    elif score >= 7:
        st.info("Parabéns! Você está aplicando bem os conceitos de OKRs no contexto prático.")
    elif score >= 4:
        st.warning("Quase lá! Reforce os conceitos e tente novamente.")
    else:
        st.error("Hora de revisar os fundamentos e práticas de OKRs.")

