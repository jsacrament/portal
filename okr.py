import streamlit as st
from openai import OpenAI
import pandas as pd
import datetime
import requests
import time

st.set_page_config(page_title="Simulador de OKRs com IA", page_icon="🎯")
st.title("🎯 Simulador de OKRs com IA para Dados e BI")

# --- Inicialização da OpenAI ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
ASSISTANT_ID = st.secrets["ASSISTANT_ID"]

# --- EmailJS ---
EMAILJS_SERVICE_ID = "masterclass"
EMAILJS_TEMPLATE_ID = "masterclass"
EMAILJS_USER_ID = "FErZC3v5hYjeGxyax"
EMAILJS_URL = "https://api.emailjs.com/api/v1.0/email/send"

# --- Sessão ---
for key in ["etapa", "nome", "email", "desafio", "okr_df", "respostas"]:
    if key not in st.session_state:
        st.session_state[key] = None if key in ["nome", "email", "desafio"] else "inicio" if key == "etapa" else pd.DataFrame() if key == "okr_df" else []

# --- Funções ---
def gerar_okr_com_assistente(desafio):
    prompt = f"""
    Crie um OKR para a área de Business Intelligence com base no seguinte desafio:
    '{desafio}'.

    Formato da resposta:
    Objetivo:
    - [texto do objetivo]
    Resultados-Chave:
    - [KR1]
    - [KR2]
    - [KR3]
    """
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt,
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=ASSISTANT_ID,
    )

    with st.spinner("🔄 O assistente está gerando seu OKR..."):
        while True:
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            if run.status in ["completed", "failed", "cancelled"]:
                break
            time.sleep(1)

    if run.status != "completed":
        st.error("❌ O assistente falhou ao gerar o OKR.")
        return None

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    for msg in messages.data:
        if msg.role == "assistant":
            return msg.content[0].text.value
    return None

def gerar_recomendacao(kr, progresso):
    prompt = f"O KR '{kr}' está com {progresso}%. Sugira melhorias, ações ou apoio."
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é analista de desempenho de OKRs."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def enviar_email(destinatario, nome, email, df):
    corpo = f"OKRs gerados para {nome} ({email}):\n\n"
    corpo += df.to_string(index=False)

    analise = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é um consultor de estratégia com OKR."},
            {"role": "user", "content": f"Analise esses OKRs:\n\n{df.to_string(index=False)}"}
        ]
    ).choices[0].message.content

    corpo += f"\n\nAnálise da IA:\n{analise}"

    payload = {
        "service_id": EMAILJS_SERVICE_ID,
        "template_id": EMAILJS_TEMPLATE_ID,
        "user_id": EMAILJS_USER_ID,
        "template_params": {
            "to_email": destinatario,
            "from_name": nome,
            "from_email": email,
            "message": corpo
        }
    }
    return requests.post(EMAILJS_URL, json=payload)

# --- Etapa 1: Formulário ---
if st.session_state.etapa == "inicio":
    with st.form("form_identificacao"):
        nome = st.text_input("Seu nome completo:")
        email = st.text_input("Seu e-mail:")
        desafio = st.text_area("Descreva seu desafio de BI/Dados:")
        destinatario = st.text_input("E-mail para envio do resultado:")
        enviar = st.form_submit_button("Gerar OKR com IA")

    if enviar and nome and email and desafio and destinatario:
        st.session_state.nome = nome
        st.session_state.email = email
        st.session_state.desafio = desafio
        resultado = gerar_okr_com_assistente(desafio)
        if not resultado:
            st.stop()
        linhas = resultado.splitlines()
        objetivo = linhas[1].replace("- ", "")
        data_inicio = str(datetime.date.today())
        data_fim = str(datetime.date.today() + datetime.timedelta(days=90))
        registros = []
        for linha in linhas:
            if linha.startswith("- ") and linha != linhas[1]:
                registros.append({
                    "Objetivo": objetivo,
                    "KR": linha.replace("- ", ""),
                    "Progresso (%)": 0,
                    "Início": data_inicio,
                    "Limite": data_fim
                })
        df = pd.DataFrame(registros)
        st.session_state.okr_df = df
        st.session_state.etapa = "progresso"
        st.rerun()

# --- Etapa 2: Progresso ---
elif st.session_state.etapa == "progresso":
    st.subheader("📌 OKRs Gerados")
    st.dataframe(st.session_state.okr_df)
    st.subheader("📈 Atualize o progresso dos KRs")

    with st.form("form_progresso"):
        novos_valores = []
        for i, row in st.session_state.okr_df.iterrows():
            progresso = st.slider(
                f"{row['KR']}", 0, 100, int(row["Progresso (%)"]), key=f"prog_{i}"
            )
            novos_valores.append(progresso)
        if st.form_submit_button("Gerar Recomendações e Enviar por E-mail"):
            for i, p in enumerate(novos_valores):
                st.session_state.okr_df.at[i, "Progresso (%)"] = p
            st.session_state.etapa = "analise"
            st.rerun()

# --- Etapa 3: Análise e envio ---
elif st.session_state.etapa == "analise":
    st.subheader("📤 Enviando Análise e Recomendações")
    df = st.session_state.okr_df
    for i, row in df.iterrows():
        recomendacao = gerar_recomendacao(row["KR"], row["Progresso (%)"])
        st.markdown(f"**KR:** {row['KR']}")
        st.markdown(f"**Progresso:** {row['Progresso (%)']}%")
        st.info(f"💡 Recomendação da IA: {recomendacao}")
        st.divider()

    status = enviar_email(
        destinatario=st.session_state.email,
        nome=st.session_state.nome,
        email=st.session_state.email,
        df=st.session_state.okr_df
    )
    if status.status_code == 200:
        st.success("✅ E-mail enviado com sucesso!")
    else:
        st.error(f"❌ Falha ao enviar e-mail: {status.text}")

    st.button("🔁 Reiniciar", on_click=lambda: st.session_state.update({
        "etapa": "inicio",
        "okr_df": pd.DataFrame(),
        "nome": None,
        "email": None,
        "desafio": None
    }))
