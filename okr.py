import streamlit as st
import openai
import pandas as pd
import datetime
import json
import os
import requests

# --- API Key via Streamlit Secrets ---
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else ""
openai.api_key = OPENAI_API_KEY

# --- Caminho do arquivo de persistência ---
DATA_PATH = "okr_data.json"

# --- Função do Agente OpenAI com tratamento de erro ---
def gerar_okr(desafio):
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
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um especialista em OKRs para equipes de dados."},
                {"role": "user", "content": prompt}
            ]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        st.error(f"Erro ao gerar OKR com a IA: {e}")
        return ""

# --- Recomendações com tratamento de erro ---
def gerar_recomendacao(kr, progresso):
    prompt = f"""
    O Resultado-Chave abaixo está com progresso em {progresso}%. Sugira melhorias, ações corretivas ou apoio:

    KR: {kr}
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um analista de desempenho de OKR para dados e BI."},
                {"role": "user", "content": prompt}
            ]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        st.error(f"Erro ao gerar recomendação: {e}")
        return "Erro ao gerar recomendação."

# --- Função para envio de e-mail via EmailJS ---
def enviar_email_via_emailjs(destinatario, nome, email, df):
    service_id = "masterclass"
    template_id = "masterclass"
    user_id = "FErZC3v5hYjeGxyax"
    url = "https://api.emailjs.com/api/v1.0/email/send"

    corpo = f"OKRs gerados para {nome} ({email}):\n\n"
    corpo += df.to_string(index=False)

    prompt = f"Gere uma análise executiva dos seguintes OKRs:\n\n{df.to_string(index=False)}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um consultor sênior em gestão de desempenho e estratégias com OKR."},
                {"role": "user", "content": prompt}
            ]
        )
        analise = response["choices"][0]["message"]["content"]
    except Exception as e:
        analise = f"Erro ao gerar análise da IA: {e}"

    corpo += f"\n\nAnálise da IA:\n{analise}"

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

# --- Funções auxiliares ---
def carregar_dados():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            return pd.DataFrame(json.load(f))
    return pd.DataFrame(columns=["Área", "Objetivo", "KR", "Progresso (%)", "Data de Início", "Data Limite"])

def salvar_dados(df):
    with open(DATA_PATH, "w") as f:
        json.dump(df.to_dict(orient="records"), f)

# --- Layout da Aplicação ---
st.title("🎯 Simulador de OKR para Dados e BI")
st.markdown("Crie, acompanhe e compartilhe OKRs com apoio de Inteligência Artificial.")

if not OPENAI_API_KEY:
    st.warning("⚠️ A chave da OpenAI não foi configurada. Adicione-a em secrets.toml ou via campo acima.")
    st.stop()

# Carrega dados salvos
df = carregar_dados()

# Inputs do usuário
area = st.selectbox("Área responsável:", ["Dados", "BI", "DataOps", "Governança", "Outro"])
desafio = st.text_area("Descreva seu desafio na área selecionada:")
nome = st.text_input("Seu nome completo:")
email = st.text_input("Seu e-mail:")
destinatario = st.text_input("E-mail para envio do OKR:")

if st.button("Gerar OKR com IA") and desafio and nome and email and destinatario:
    resultado = gerar_okr(desafio)
    if not resultado.strip():
        st.warning("A geração do OKR falhou ou retornou vazio.")
        st.stop()

    st.success("OKR Gerado:")
    st.code(resultado, language='markdown')

    linhas = resultado.splitlines()
    objetivo = ""
    novos_okrs = []
    captura_krs = False

    for linha in linhas:
        if linha.strip().lower().startswith("objetivo") and "- " in linha:
            objetivo = linha.split("- ", 1)[1].strip()
        elif linha.strip().startswith("- ") and captura_krs:
            kr = linha.replace("- ", "").strip()
            novos_okrs.append({
                "Área": area,
                "Objetivo": objetivo,
                "KR": kr,
                "Progresso (%)": 0,
                "Data de Início": str(datetime.date.today()),
                "Data Limite": str(datetime.date.today() + datetime.timedelta(days=90))
            })
        elif linha.lower().strip().startswith("resultados-chave") or linha.lower().strip().startswith("resultados chave"):
            captura_krs = True

    novos_df = pd.DataFrame(novos_okrs)
    df = pd.concat([df, novos_df], ignore_index=True)
    salvar_dados(df)

    status, resposta = enviar_email_via_emailjs(destinatario, nome, email, novos_df)
    if status == 200:
        st.success("E-mail com os OKRs enviado com sucesso!")
    else:
        st.error("Erro ao enviar e-mail: " + resposta)

# Mostrar OKRs
st.subheader("📊 Acompanhamento dos Resultados-Chave")
area_filtro = st.selectbox("Filtrar por área:", sorted(df["Área"].unique()) if not df.empty else ["-"])
okr_filtrados = df[df["Área"] == area_filtro]
st.dataframe(okr_filtrados)

# Atualização de progresso
st.subheader("✏️ Atualizar Progresso de KRs")
with st.form("Atualizar KR"):
    index_map = okr_filtrados.index.tolist()
    if index_map:
        index = st.selectbox("Selecione o KR para atualizar:", index_map)
        novo_progresso = st.slider("Novo progresso (%)", 0, 100, int(df.loc[index, "Progresso (%)"]))
        submit = st.form_submit_button("Atualizar")
        if submit:
            df.at[index, "Progresso (%)"] = novo_progresso
            salvar_dados(df)
            st.success("Progresso atualizado com sucesso!")
            recomendacao = gerar_recomendacao(df.loc[index, "KR"], novo_progresso)
            st.info("Recomendação da IA:")
            st.write(recomendacao)
    else:
        st.warning("Nenhum KR disponível para essa área.")
        st.form_submit_button("Atualizar", disabled=True)

# Gráfico
st.subheader("📈 Evolução Visual")
if not okr_filtrados.empty:
    st.bar_chart(okr_filtrados.set_index("KR")["Progresso (%)"])



