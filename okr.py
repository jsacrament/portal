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

def avaliar_kr_com_base_no_objetivo(objetivo, kr, nivel):
    prompt = f"Avalie se o seguinte Resultado-Chave (KR) está bem alinhado ao Objetivo apresentado, considerando o nível de OKR: {nivel}.\n\nObjetivo: {objetivo}\nKR: {kr}"
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é especialista em gestão com foco em OKRs."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def sugerir_cronograma_padrao(kr, nivel):
    prompt = f"Sugira um cronograma padrão com dias úteis para o seguinte Resultado-Chave (KR), levando em conta que é um KR de nível '{nivel}':\n\nKR: {kr}"
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é especialista em planejamento de projetos com foco em OKRs e cronogramas."},
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
        gerar_cascata = st.radio("Deseja criar OKRs para todos os níveis da cascata?", ["Sim", "Não"])

        registros = []

        niveis = ["Empresa", "Departamento", "Equipe", "Individual"] if gerar_cascata == "Sim" else [st.selectbox("Nível do OKR:", ["Empresa", "Departamento", "Equipe", "Individual"])]

        for nivel in niveis:
            st.markdown(f"### Nível: {nivel}")
            objetivo = st.text_area(f"Objetivo ({nivel}):", key=f"obj_{nivel}")

            st.markdown("#### Key Results (até 5)")
            kr1 = st.text_input(f"KR 1 ({nivel}):", key=f"kr1_{nivel}")
            kr2 = st.text_input(f"KR 2 ({nivel}):", key=f"kr2_{nivel}")
            kr3 = st.text_input(f"KR 3 ({nivel}):", key=f"kr3_{nivel}")
            kr4 = st.text_input(f"KR 4 ({nivel}):", key=f"kr4_{nivel}")
            kr5 = st.text_input(f"KR 5 ({nivel}):", key=f"kr5_{nivel}")

            kr_inputs = [kr for kr in [kr1, kr2, kr3, kr4, kr5] if kr.strip()]
            data_inicio = str(datetime.date.today())
            data_fim = str(datetime.date.today() + datetime.timedelta(days=90))
            for kr in kr_inputs:
                registros.append({
                    "Nível": nivel,
                    "Objetivo": objetivo,
                    "KR": kr,
                    "Progresso (%)": 0,
                    "Início": data_inicio,
                    "Limite": data_fim
                })

        enviar = st.form_submit_button("Avançar para Progresso")

    if enviar and nome and email and registros:
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
    st.subheader("📤 Avaliação e Recomendação da IA por KR")
    df = st.session_state.okr_df
    for i, row in df.iterrows():
        recomendacao = gerar_recomendacao(row["KR"], row["Progresso (%)"])
        avaliacao_kr = avaliar_kr_com_base_no_objetivo(row["Objetivo"], row["KR"], row["Nível"])
        cronograma = sugerir_cronograma_padrao(row["KR"], row["Nível"])
        st.markdown(f"**Nível:** {row['Nível']}")
        st.markdown(f"**KR:** {row['KR']}")
        st.markdown(f"**Progresso:** {row['Progresso (%)']}%")
        st.info(f"💡 Recomendação da IA: {recomendacao}")
        st.warning(f"🧠 Avaliação do KR em relação ao Objetivo ({row['Nível']}): {avaliacao_kr}")
        st.success(f"📅 Cronograma Sugerido: {cronograma}")
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


