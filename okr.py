import streamlit as st
import openai
import pandas as pd
import datetime
import requests

# --- Configurar chave da API ---
openai.api_key = st.secrets["OPENAI_API_KEY"]

# --- Função do Agente OpenAI para gerar OKRs ---
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

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é um especialista em OKRs para equipes de dados."},
            {"role": "user", "content": prompt}
        ]
    )
    return response["choices"][0]["message"]["content"]

# --- Gera recomendação com base no progresso ---
def gerar_recomendacao(kr, progresso):
    prompt = f"""
    O Resultado-Chave abaixo está com progresso em {progresso}%. Sugira melhorias, ações corretivas ou apoio:

    KR: {kr}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é um analista de desempenho de OKR para dados e BI."},
            {"role": "user", "content": prompt}
        ]
    )
    return response["choices"][0]["message"]["content"]

# --- Envio de e-mail via EmailJS ---
def enviar_email_via_emailjs(destinatario, nome, email, df):
    service_id = "masterclass"
    template_id = "masterclass"
    user_id = "FErZC3v5hYjeGxyax"
    url = "https://api.emailjs.com/api/v1.0/email/send"

    corpo = f"OKRs gerados para {nome} ({email}):\n\n"
    corpo += df.to_string(index=False)

    prompt = f"Gere uma análise executiva dos seguintes OKRs:\n\n{df.to_string(index=False)}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é um consultor sênior em gestão de desempenho e estratégias com OKR."},
            {"role": "user", "content": prompt}
        ]
    )
    analise = response["choices"][0]["message"]["content"]
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

# --- Inicializa session_state ---
if "novos_df" not in st.session_state:
    st.session_state.novos_df = pd.DataFrame()

# --- Interface ---
st.title("🌟 Simulador de OKR com IA para Dados e BI")
st.markdown("Crie, acompanhe e analise OKRs com apoio de Inteligência Artificial.")

area = st.selectbox("Área responsável:", ["Dados", "BI", "DataOps", "Governança", "Outro"])
desafio = st.text_area("Descreva seu desafio:")
nome = st.text_input("Seu nome completo:")
email = st.text_input("Seu e-mail:")
destinatario = st.text_input("E-mail para envio dos OKRs:")

if st.button("Gerar OKR com IA") and desafio and nome and email and destinatario:
    resultado = gerar_okr(desafio)
    st.success("OKR Gerado:")
    st.code(resultado, language='markdown')

    linhas = resultado.splitlines()
    objetivo = linhas[1].replace("- ", "") if len(linhas) > 1 else ""
    novos_okrs = []
    for linha in linhas:
        if linha.startswith("- ") and linha != linhas[1]:
            kr = linha.replace("- ", "")
            novos_okrs.append({
                "Área": area,
                "Objetivo": objetivo,
                "KR": kr,
                "Progresso (%)": 0,
                "Data de Início": str(datetime.date.today()),
                "Data Limite": str(datetime.date.today() + datetime.timedelta(days=90))
            })

    novos_df = pd.DataFrame(novos_okrs)
    st.session_state.novos_df = novos_df

    st.subheader("Resultados-Chave")
    st.dataframe(novos_df)

    status, resposta = enviar_email_via_emailjs(destinatario, nome, email, novos_df)
    if status == 200:
        st.success("E-mail com os OKRs enviado com sucesso!")
    else:
        st.error("Erro ao enviar e-mail: " + resposta)

# --- Atualização de progresso simples ---
st.subheader("📊 Simulação de Progresso")
if not st.session_state.novos_df.empty:
    with st.form("Atualizar KR"):
        index_map = st.session_state.novos_df.index.tolist()
        if index_map:
            index = st.selectbox("Selecione o KR:", index_map)
            novo_progresso = st.slider("Novo progresso (%)", 0, 100, int(st.session_state.novos_df.loc[index, "Progresso (%)"]))
            if st.form_submit_button("Atualizar"):
                st.session_state.novos_df.at[index, "Progresso (%)"] = novo_progresso
                st.success("Progresso atualizado!")
                recomendacao = gerar_recomendacao(st.session_state.novos_df.loc[index, "KR"], novo_progresso)
                st.info("Recomendação da IA:")
                st.write(recomendacao)
        else:
            st.warning("Nenhum KR disponível.")

    st.subheader("Progresso Atualizado")
    st.dataframe(st.session_state.novos_df)
    st.bar_chart(st.session_state.novos_df.set_index("KR")["Progresso (%)"])

# --- Exportar dados ---
if not st.session_state.novos_df.empty:
    st.download_button("📄 Exportar OKRs", st.session_state.novos_df.to_csv(index=False), file_name="okr_exportados.csv")



