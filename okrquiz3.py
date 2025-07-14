
import streamlit as st

st.set_page_config(page_title="🧠 Quiz OKRs - Governança", page_icon="🧠", layout="centered")

st.title("🧠 Quiz 3 – Monitoramento e Governança dos OKRs")
st.subheader("Objetivo: Refletir sobre a importância do acompanhamento, governança e papel da área de dados.")

score = 0

q1 = st.radio("1. A chave para o sucesso dos OKRs está em:", [
    "a) Ter KRs muito fáceis",
    "b) Acompanhamento e ciclos de feedback contínuos",
    "c) Não precisar de reuniões",
    "d) Ser um documento fixo"
])
if q1 == "b) Acompanhamento e ciclos de feedback contínuos":
    score += 1

q2 = st.radio("2. O papel da área de dados nos OKRs é:", [
    "a) Criar gráficos bonitos",
    "b) Ajudar na redação dos objetivos",
    "c) Fornecer dados confiáveis e gerar insights estratégicos",
    "d) Validar metas operacionais"
])
if q2 == "c) Fornecer dados confiáveis e gerar insights estratégicos":
    score += 1

q3 = st.radio("3. Uma boa prática de governança de OKRs inclui:", [
    "a) Compartilhar publicamente os resultados",
    "b) Guardar os objetivos em planilhas secretas",
    "c) Atualizar os OKRs somente no fim do trimestre",
    "d) Fazer acompanhamento constante e comunicação"
])
if q3 == "d) Fazer acompanhamento constante e comunicação":
    score += 1

q4 = st.radio("4. O que é considerado uma armadilha na aplicação de OKRs?", [
    "a) Ajustar os KRs a cada ciclo",
    "b) Criar metas isoladas da estratégia",
    "c) Usar indicadores técnicos",
    "d) Medir performance com KPIs"
])
if q4 == "b) Criar metas isoladas da estratégia":
    score += 1

q5 = st.radio("5. O monitoramento eficaz deve ser:", [
    "a) Feito apenas pela liderança",
    "b) Rígido e punitivo",
    "c) Coletivo, transparente e frequente",
    "d) Mensal e sigiloso"
])
if q5 == "c) Coletivo, transparente e frequente":
    score += 1

q6 = st.radio("6. OKRs funcionam melhor quando:", [
    "a) Ficam apenas na liderança",
    "b) São adaptados e ajustados conforme o aprendizado",
    "c) Não envolvem métricas",
    "d) São longos e fixos"
])
if q6 == "b) São adaptados e ajustados conforme o aprendizado":
    score += 1

q7 = st.radio("7. Como os KPIs e OKRs se complementam?", [
    "a) KPIs validam os resultados dos OKRs",
    "b) São concorrentes",
    "c) Substituem-se entre si",
    "d) São usados apenas separadamente"
])
if q7 == "a) KPIs validam os resultados dos OKRs":
    score += 1

q8 = st.radio("8. Qual destas ferramentas é fundamental para monitorar OKRs?", [
    "a) Email",
    "b) Painéis de BI",
    "c) Post-its",
    "d) Excel impresso"
])
if q8 == "b) Painéis de BI":
    score += 1

q9 = st.radio("9. Qual o risco de criar metas conservadoras demais nos OKRs?", [
    "a) Motivação extra",
    "b) Menor alinhamento",
    "c) Falta de transformação real",
    "d) Facilidade no feedback"
])
if q9 == "c) Falta de transformação real":
    score += 1

q10 = st.radio("10. Qual é o papel dos KRs na avaliação dos OKRs?", [
    "a) Fazer revisões ortográficas",
    "b) Medir se o objetivo foi alcançado",
    "c) Substituir objetivos",
    "d) Justificar falhas"
])
if q10 == "b) Medir se o objetivo foi alcançado":
    score += 1

if st.button("Enviar respostas"):
    st.success(f"Você acertou {score} de 10 perguntas!")
    if score == 10:
        st.balloons()
    elif score >= 7:
        st.info("Ótimo! Você entende bem sobre monitoramento e governança de OKRs.")
    elif score >= 4:
        st.warning("Você tem uma boa base, mas pode reforçar alguns pontos.")
    else:
        st.error("Hora de revisar os conceitos de governança e acompanhamento de OKRs.")
