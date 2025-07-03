import streamlit as st
from openai import OpenAI
import re
import time

# Configuração da página
st.set_page_config(page_title="Detector de Texto IA ou Humano", page_icon="🕵️")
st.title("🕵️ Detector de Texto: Humano ou ChatGPT?")

# Inicialização da API
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
ASSISTANT_ID = st.secrets["ASSISTANT_ID"]

# Formulário de entrada
with st.form("form_analise"):
    texto = st.text_area("Cole aqui o texto para análise:")
    enviar = st.form_submit_button("Analisar Texto")

if enviar and texto:
    prompt_chatgpt = f"""
Você é um detector treinado para identificar textos gerados por modelos da família ChatGPT (como GPT-3.5 e GPT-4). Sua tarefa é analisar o seguinte texto e indicar com base em estilo, estrutura e padrões linguísticos se ele foi provavelmente escrito por um ser humano ou por um modelo ChatGPT.

Considere os seguintes sinais comuns de texto gerado por ChatGPT:
- Estrutura excessivamente organizada e limpa
- Uso sistemático de conectores como "além disso", "em síntese", "por outro lado"
- Falta de subjetividade ou posicionamento pessoal explícito
- Frases muito completas e explicativas, com tom enciclopédico
- Pouca digressão, erros ou hesitações naturais
- Uso recorrente de expressões genéricas e neutras

Texto a ser analisado:
\"\"\"{texto}\"\"\"

Justifique sua análise com base nos critérios linguísticos e estruturais observados.

Ao final, atribua uma **pontuação de probabilidade de ter sido gerado por ChatGPT**, entre 0 e 100:
- 0 a 40: Muito improvável que seja ChatGPT
- 41 a 70: Pode ter influência ou revisão de ChatGPT
- 71 a 100: Muito provavelmente foi escrito com ChatGPT
"""

    with st.spinner("Analisando com o detector especializado em ChatGPT..."):
        resposta = client.beta.threads.create_and_run(
            assistant_id=ASSISTANT_ID,
            thread={"messages": [{"role": "user", "content": prompt_chatgpt}]}
        )

        thread_id = resposta.thread_id
        run_id = resposta.id
        status = resposta.status

        while status in ["queued", "in_progress"]:
            time.sleep(2)
            status_resp = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            status = status_resp.status

        mensagens = client.beta.threads.messages.list(thread_id=thread_id)
        resposta_assistente = next(
            (msg.content[0].text.value for msg in mensagens.data if msg.role == "assistant"),
            "❌ Resposta não encontrada."
        )

        st.subheader("🔍 Resultado da Análise")
        st.markdown(resposta_assistente)

        matches = re.findall(r"(\d{1,3})", resposta_assistente)
        scores_validos = [int(m) for m in matches if 0 <= int(m) <= 100]

        if scores_validos:
            score = max(scores_validos)
            st.progress(score)

            if score < 41:
                st.success("✅ Muito improvável que tenha sido gerado por ChatGPT.")
            elif score < 71:
                st.info("ℹ️ Pode ter sido influenciado ou revisado por ChatGPT.")
            else:
                st.warning("⚠️ Alta probabilidade de ter sido gerado por ChatGPT.")
        else:
            st.text("Pontuação de autenticidade não identificada.")

