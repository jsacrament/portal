import streamlit as st
from openai import OpenAI
import pandas as pd
import datetime
import requests

st.set_page_config(page_title="Formulário OKR com IA", page_icon="🛰️")
st.title("🛰️ Missão OKR: Construindo o Futuro da Equipe de Dados e BI")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
ASSISTANT_ID = st.secrets["ASSISTANT_ID"]

EMAILJS_SERVICE_ID = "masterclass"
EMAILJS_TEMPLATE_ID = "masterclass"
EMAILJS_USER_ID = "FErZC3v5hYjeGxyax"
EMAILJS_URL = "https://api.emailjs.com/api/v1.0/email/send"

if "etapa" not in st.session_state:
    st.session_state.etapa = "formulario"

def verificar_autenticidade_respostas(df):
    prompt = f"Analise as respostas a seguir e indique se parecem ter sido geradas por um ser humano ou por uma IA. Dê uma pontuação de 0 a 100 para o grau de autenticidade humana (quanto maior, mais humano).\n\n{df.to_string(index=False)}"
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é um detector de respostas geradas por inteligência artificial."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def enviar_email(destinatario, nome, email, df, autenticidade):
    corpo = f"Formulário preenchido por {nome} ({email}):\n\n"
    corpo += df.to_string(index=False)

    analise = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é um consultor de OKR."},
            {"role": "user", "content": f"Analise este formulário de OKR:\n\n{df.to_string(index=False)}"}
        ]
    ).choices[0].message.content

    corpo += f"\n\nAnálise da IA:\n{analise}"
    corpo += f"\n\nValidação de autenticidade das respostas:\n{autenticidade}"

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

if st.session_state.etapa == "formulario":
    with st.form("form_missao_okr"):
        nome = st.text_input("Seu nome completo:")
        email = st.text_input("Seu e-mail:")
        destinatario = st.text_input("E-mail para envio do resultado:")

        area = st.multiselect("Qual área do time você representa?", [
            "BI (Business Intelligence)", "Engenharia de Dados", "Análise de Dados", "Governança/Qualidade", "Outra (especificar)"
        ])

        objetivo = st.text_area("Na sua visão, qual deveria ser um objetivo principal do time no próximo mês?")

        st.markdown("#### Quais Resultados-Chave você sugere para esse objetivo? (até 3)")
        kr1 = st.text_input("KR1:")
        kr2 = st.text_input("KR2:")
        kr3 = st.text_input("KR3:")

        atividades_kr1 = [st.text_input(f"Atividade {i+1} para KR1:", key=f"a1_{i}") for i in range(5)]
        atividades_kr2 = [st.text_input(f"Atividade {i+1} para KR2:", key=f"a2_{i}") for i in range(5)]
        atividades_kr3 = [st.text_input(f"Atividade {i+1} para KR3:", key=f"a3_{i}") for i in range(5)]

        mensuravel = st.radio("Você considera que sua proposta pode ser mensurada?", [
            "Sim, com números claros", "Parcialmente, precisa de ajustes", "Não, ainda está genérica"
        ])

        medicao = st.text_input("Como você imagina que podemos medir o sucesso dessa meta?")

        ideias = st.text_area("Outras ideias de objetivos ou melhorias para o time (opcional):")

        oficina = st.radio("Você gostaria de participar da construção colaborativa dos OKRs em uma oficina curta (30min)?", ["Sim", "Não"])

        enviar = st.form_submit_button("Enviar")

    if enviar and nome and email and objetivo:
        df = pd.DataFrame([{
            "Nome": nome,
            "Email": email,
            "Area": ", ".join(area),
            "Objetivo": objetivo,
            "KR1": kr1,
            "Atividades KR1": ", ".join([a for a in atividades_kr1 if a]),
            "KR2": kr2,
            "Atividades KR2": ", ".join([a for a in atividades_kr2 if a]),
            "KR3": kr3,
            "Atividades KR3": ", ".join([a for a in atividades_kr3 if a]),
            "Mensurável": mensuravel,
            "Medição": medicao,
            "Ideias Extras": ideias,
            "Quer Oficina?": oficina
        }])

        autenticidade = verificar_autenticidade_respostas(df)

        st.markdown("---")
        st.subheader("🔎 Validação de Autenticidade das Respostas")
        st.info(autenticidade)

        if "grau de autenticidade" in autenticidade.lower():
            try:
                import re
                match = re.search(r"(\d{1,3})", autenticidade)
                if match:
                    score = int(match.group(1))
                    st.progress(score if score <= 100 else 100)
                    if score < 50:
                        st.warning("⚠️ As respostas podem ter sido geradas por IA. Avalie com cuidado.")
                    elif score < 80:
                        st.info("ℹ️ As respostas parecem parcialmente humanas.")
                    else:
                        st.success("✅ As respostas parecem ter sido escritas por um humano.")
            except:
                st.text("Erro ao extrair a pontuação de autenticidade.")

        status = enviar_email(destinatario, nome, email, df, autenticidade)

        if status.status_code == 200:
            st.success("✅ Formulário enviado com sucesso! Análise da IA e verificação de autenticidade enviadas por e-mail.")
        else:
            st.error(f"❌ Erro ao enviar o e-mail: {status.text}")

        st.session_state.clear()

