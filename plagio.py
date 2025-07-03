import streamlit as st
from openai import OpenAI
import re

st.set_page_config(page_title="Detector de Texto IA ou Humano", page_icon="🕵️")
st.title("🕵️ Detector de Texto: IA ou Humano?")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
ASSISTANT_ID = st.secrets["ASSISTANT_ID"]

with st.form("form_analise"):
    texto = st.text_area("Cole aqui o texto para análise:")
    enviar = st.form_submit_button("Analisar Texto")

if enviar and texto:
    with st.spinner("Analisando com o agente..."):
        resposta = client.beta.threads.create_and_run(
            assistant_id=ASSISTANT_ID,
            thread={"messages": [{"role": "user", "content": f"Texto: {texto}"}]}
        )

        # Esperar finalização do processamento
        import time
        status = resposta.status
        thread_id = resposta.thread_id
        run_id = resposta.id

        while status in ["queued", "in_progress"]:
            time.sleep(2)
            status_resp = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            status = status_resp.status

        mensagens = client.beta.threads.messages.list(thread_id=thread_id)
        conteudo = mensagens.data[0].content[0].text.value

        st.subheader("🔍 Resultado da Análise")
        st.markdown(conteudo)

        match = re.search(r"(\d{1,3})", conteudo)
        if match:
            score = int(match.group(1))
            st.progress(score if score <= 100 else 100)
            if score < 50:
                st.warning("⚠️ Alta probabilidade de ter sido gerado por IA.")
            elif score < 80:
                st.info("ℹ️ Pode conter elementos gerados por IA.")
            else:
                st.success("✅ Provavelmente foi escrito por um humano.")
        else:
            st.text("Pontuação de autenticidade não identificada.")
