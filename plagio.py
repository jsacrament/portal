import streamlit as st
from openai import OpenAI
import re
import time

# Configuração da página
st.set_page_config(page_title="Detector de Texto IA ou Humano", page_icon="🕵️")
st.title("🕵️ Detector de Texto: Humano ou ChatGPT?")

# Inicialização do cliente da OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
ASSISTANT_ID = st.secrets["ASSISTANT_ID"]

# Formulário de entrada do texto
with st.form("form_analise"):
    texto = st.text_area("Cole aqui o texto para análise:")
    enviar = st.form_submit_button("Analisar Texto")

# Executar se texto for submetido
if enviar and texto:
    # Prompt especializado para detecção de textos do ChatGPT
    prompt = f"""
Você é um avaliador altamente treinado para detectar textos gerados por modelos da família ChatGPT (como GPT-3.5 e GPT-4). Seu objetivo é analisar cuidadosamente o seguinte texto e indicar, com base em estrutura, estilo e padrões linguísticos, se ele foi escrito por um humano ou por IA.

Leve em consideração os seguintes critérios:
- Uso excessivo de conectores estruturados e linguagem formal demais
- Ausência de hesitações, pausas reflexivas ou digressões naturais
- Organização rígida (introdução, desenvolvimento, conclusão) sem variação estilística
- Frases muito explicativas, com tom neutro ou enciclopédico
- Pouca subjetividade, opiniões ou experiências pessoais

Analise o texto abaixo e forneça:
1. Uma justificativa detalhada sobre os sinais que indicam autoria humana ou por IA.
2. Uma **pontuação de probabilidade de autoria humana de 0 a 100**, sendo:
   - 0 a 40 → Muito provavelmente IA
   - 41 a 70 → Pode ter sido revisado ou iniciado por IA
   - 71 a 98 → Provavelmente humano, mas com traços artificiais
   - 99 a 100 → Muito provavelmente escrito por um humano com estilo autêntico e não-automatizado

Texto para análise:
\"\"\"{texto}\"\"\"
"""

    with st.spinner("Analisando com o agente..."):
        resposta = client.beta.threads.create_and_run(
            assistant_id=ASSISTANT_ID,
            thread={"messages": [{"role": "user", "content": prompt}]}
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

        # Captura de pontuação com validação segura
        matches = re.findall(r"(\d{1,3})", resposta_assistente)
        scores_validos = [int(m) for m in matches if 0 <= int(m) <= 100]

        if scores_validos:
            score = max(scores_validos)
            st.progress(score)

            # Lógica de avaliação refinada
            if score >= 99:
                st.success("✅ Muito provavelmente escrito por um humano autêntico (≥ 99%).")
            elif score >= 71:
                st.info("🧠 Provavelmente escrito por um humano, mas com traços que lembram IA.")
            elif score >= 41:
                st.warning("⚠️ Pode ter sido iniciado ou revisado por IA.")
            else:
                st.error("❌ Muito provavelmente gerado por IA (≤ 40%).")
        else:
            st.text("Pontuação de autenticidade não identificada.")


