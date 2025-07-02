import streamlit as st
from openai import OpenAI
import pandas as pd
import datetime
import requests
import time

st.set_page_config(page_title="Simulador Manual de OKRs", page_icon="🎯")
st.title("📝 Simulador Manual de OKRs com IA")

# --- Inicialização da OpenAI ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
ASSISTANT_ID = st.secrets["ASSISTANT_ID"]

# --- EmailJS ---
EMAILJS_SERVICE_ID = "masterclass"
EMAILJS_TEMPLATE_ID = "masterclass"
EMAILJS_USER_ID = "FErZC3v5hYjeGxyax"
EMAILJS_URL = "https://api.emailjs.com/api/v1.0/email/send"

# --- Sessão ---
if "etapa" not in st.session_state:
    st.session_state.etapa = "formulario"

# --- Funções ---
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
    corpo = f"OKRs inseridos por {nome} ({email}):\n\n"
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

# --- Etapa 1: Formulário manual ---
if st.session_state.etapa == "formulario":
    with st.form("form_manual"):
        nome = st.text_input("Seu nome completo:")
        email = st.text_input("Seu e-mail:")
        destinatario = st.text_input("E-mail para envio do resultado:")
        objetivo = st.text_area("Objetivo:")

        kr_inputs = []
        for i in range(1, 6):
            kr = st.text_input(f"KR {i}:", key=f"kr_{i}")
            if kr:
                kr_inputs.append(kr)

        enviar = st.form_submit_button("Avançar para Progresso")

    if enviar and nome and email and objetivo and kr_inputs:
        data_inicio = str(datetime.date.today())
        data_fim = str(datetime.date.today() + datetime.timedelta(days=90))
        registros = []
        for kr in kr_inputs:
            registros.append({
                "Objetivo": objetivo,
                "KR": kr,
                "Progresso (%)": 0,
                "Início": data_inicio,
                "Limite": data_fim
            })
        st.session_state.okr_df = pd.DataFrame(registros)
        st.session_state.nome = nome
        st.session_state.email = email
        st.session_state.destinatario = destinatario
        st.session_state.etapa = "progresso"
        st.rerun()

# --- Etapa 2: Acompanhamento de progresso ---
elif st.session_state.etapa == "progresso":
    st.subheader("📌 OKRs Inseridos")
    st.dataframe(st.session_state.okr_df)

    st.subheader("📈 Atualize o progresso de cada KR")
    with st.form("form_progresso_manual"):
        novos_valores = []
        for i, row in st.session_state.okr_df.iterrows():
            progresso = st.slider(
                f"{row['KR']}", 0, 100, int(row["Progresso (%)"]), key=f"prog_manual_{i}"
            )
            novos_valores.append(progresso)
        if st.form_submit_button("Gerar Recomendações e Enviar por E-mail"):
            for i, p in enumerate(novos_valores):
                st.session_state.okr_df.at[i, "Progresso (%)"] = p
            st.session_state.etapa = "analise"
            st.rerun()

# --- Etapa 3: Recomendação e envio ---
elif st.session_state.etapa == "analise":
    st.subheader("📤 Recomendação da IA por KR")
    df = st.session_state.okr_df
    for i, row in df.iterrows():
        recomendacao = gerar_recomendacao(row["KR"], row["Progresso (%)"])
        st.markdown(f"**KR:** {row['KR']}")
        st.markdown(f"**Progresso:** {row['Progresso (%)']}%")
        st.info(f"💡 Recomendação da IA: {recomendacao}")
        st.divider()

    status = enviar_email(
        destinatario=st.session_state.destinatario,
        nome=st.session_state.nome,
        email=st.session_state.email,
        df=df
    )
    if status.status_code == 200:
        st.success("✅ E-mail enviado com sucesso!")
    else:
        st.error(f"❌ Falha ao enviar e-mail: {status.text}")

    st.button("🔁 Reiniciar", on_click=lambda: st.session_state.clear())
