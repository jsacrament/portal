import streamlit as st
import pandas as pd
import requests

# Função de envio de e-mail via EmailJS
def enviar_email_via_emailjs(destinatario, nome, email, df, total_pontos):
    service_id = "masterclass"
    template_id = "masterclass"
    user_id = "FErZC3v5hYjeGxyax"
    url = "https://api.emailjs.com/api/v1.0/email/send"

    corpo = f"Respostas do usuário {nome} ({email}):\n\n"
    corpo += df.to_string(index=False)
    corpo += f"\n\nPontuação total atribuída pelo assistente: {total_pontos} / {len(df)*10}\n"
    
    payload = {
        "service_id": service_id,
        "template_id": template_id,
        "user_id": user_id,
        "template_params": {
            "to_email": destinatario,
            "from_name": nome,
            "from_email": email,
            "message": corpo
        }
    }
    response = requests.post(url, json=payload)
    return response.status_code, response.text

# Início do app
st.title("Dinâmica Prática: Criando OKRs Reais no Call Center")

# Campos para identificação
st.sidebar.header("Identificação")
nome = st.sidebar.text_input("Seu nome:")
email = st.sidebar.text_input("Seu e-mail:")

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
else:
    kr2_1 = kr2_2 = kr2_3 = ""

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
dificuldade = st.radio(
    "O que foi mais difícil?",
    ["Definir objetivos estratégicos", "Mensurar resultados", "Ambos", "Nenhum"]
)
impacto = st.text_area("Como a clareza nos OKRs pode impactar os resultados do time de dados?")
aplicacao = st.text_area("Você vê aplicação imediata dessa metodologia na sua rotina de trabalho? Justifique.")

# Botão para envio de e-mail
st.header("9. Enviar Respostas por E-mail")

destinatario = st.text_input("E-mail de destino (facilitador ou seu próprio e-mail):", value=email)

if st.button("Enviar por E-mail"):
    # Montar DataFrame com as respostas
    data = {
        "Pergunta": [
            "Problemas Identificados", "Objetivo 1", "KR1 Objetivo 1", "KR2 Objetivo 1", "KR3 Objetivo 1",
            "Objetivo 2", "KR1 Objetivo 2", "KR2 Objetivo 2", "KR3 Objetivo 2",
            "Apresentação", "Feedback", "Refino",
            "Dificuldade", "Impacto", "Aplicação"
        ],
        "Resposta": [
            problemas, objetivo1, kr1_1, kr1_2, kr1_3,
            objetivo2, kr2_1, kr2_2, kr2_3,
            apresentacao, feedback, refino,
            dificuldade, impacto, aplicacao
        ]
    }
    df = pd.DataFrame(data)
    # Atribuir pontuação total fictícia (ajuste a regra se quiser)
    total_pontos = 10 * sum([bool(str(v).strip()) for v in data["Resposta"]])
    status, retorno = enviar_email_via_emailjs(destinatario, nome, email, df, total_pontos)
    if status == 200:
        st.success(f"E-mail enviado com sucesso para {destinatario}!")
    else:
        st.error(f"Falha ao enviar o e-mail: {retorno}")


