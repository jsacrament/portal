import streamlit as st
from openai import OpenAI
import re
import time

# Configuração da página
st.set_page_config(page_title="Detector de Texto IA ou Humano", page_icon="🕵️")
st.title("🕵️ Detector de Texto: IA ou Humano?")

# Inicialização do cliente OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
ASSISTANT_ID = st.secrets["ASSISTANT_ID"]

# Formulário de entrada
with st.form("form_analise"):
    texto = st.text_area("Cole aqui o texto para análise:")
    enviar = st.form_submit_button("Analisar Texto")

# Quando o usuário clica em "Analisar Texto"
if enviar and texto:
    # Prompt estruturado para garantir análise correta
    prompt_base = f"""
Você é um especialista em detecção de autoria textual. Sua função é analisar qualquer texto fornecido e indicar se ele foi provavelmente escrito por um ser humano ou por uma inteligência artificial.

Analise com base nos seguintes critérios:
- Estilo de escrita (variedade, naturalidade, subjetividade)
- Fluidez e coerência entre as ideias
- Estrutura textual (organização, progressão lógica)
- Grau de formalismo ou rigidez artificial
- Presença de repetições, padrões mecânicos ou falta de variação
- Elementos de autoria humana, como hesitação, analogia, crítica, exemplos ou opiniões

Texto para análise:
\"\"\"{texto}\"\"\"

Ao final, justifique sua resposta com base nos elementos observados.

Atribua uma **pontuação de autenticidade humana de 0 a 100**, sendo:
- 0 a 40: Muito provavelmente escrito por IA  
- 41 a 70: Pode ter sido gerado por IA com revisão humana  
- 71 a 100: Provavelmente escrito por um ser humano
"""

    with st.spinner("Analisando com o agente..."):
        # Criação e execução do thread do assistente
        resposta = client.beta.threads.create_and_run(
            assistant_id=ASSISTANT_ID,
            thread={"messages": [{"role": "user", "content": prompt_base}]}
        )

        thread_id = resposta.thread_id
        run_id = resposta.id
        status = resposta.status

        # Aguardar até a finalização
        while status in ["queued", "in_progress"]:
            time.sleep(2)
            status_resp = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            status = status_resp.status

        # Obter mensagens do assistente
        mensagens = client.beta.threads.messages.list(thread_id=thread_id)

        # Recuperar a última resposta do tipo "assistant"
        resposta_assistente = next(
            (msg.content[0].text.value for msg in mensagens.data if msg.role == "assistant"),
            "❌ Resposta não encontrada."
        )

        st.subheader("🔍 Resultado da Análise")
        st.markdown(resposta_assistente)

        # Corrigir extração da pontuação (pegar o maior número entre 0 e 100)
        matches = re.findall(r"(\d{1,3})", resposta_assistente)
        scores_validos = [int(m) for m in matches if 0 <= int(m) <= 100]

        if scores_validos:
            score = max(scores_validos)
            st.progress(score)

            if score < 50:
                st.warning("⚠️ Alta probabilidade de ter sido gerado por IA.")
            elif score < 80:
                st.info("ℹ️ Pode conter elementos gerados por IA.")
            else:
                st.success("✅ Provavelmente foi escrito por um humano.")
        else:
            st.text("Pontuação de autenticidade não identificada.")

