import streamlit as st
from openai import OpenAI
import re
import time

# Configurações iniciais da página
st.set_page_config(page_title="🧠 Detector & Reescritor de Texto IA", page_icon="🕵️")
st.title("🕵️ Detector de Texto: Humano ou ChatGPT?")
st.markdown("🚀 Este app detecta se um texto foi gerado por IA e oferece uma opção para reescrevê-lo de forma humanizada.")

# OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
ASSISTANT_ID = st.secrets["ASSISTANT_ID"]

tab1, tab2 = st.tabs(["🔍 Detectar IA ou Humano", "✍️ Reescrever como Humano"])

# ---------- TAB 1: DETECTOR ----------
with tab1:
    with st.form("form_analise"):
        texto = st.text_area("Cole aqui o texto para análise de autoria:")
        enviar = st.form_submit_button("🔍 Analisar Texto")

    if enviar and texto:
        prompt_detector = f"""
Você é um avaliador treinado para detectar textos gerados por modelos ChatGPT (GPT-3.5, GPT-4). Analise o texto abaixo e informe se ele foi provavelmente escrito por um humano ou por IA.

Considere:
- Estrutura excessivamente organizada
- Linguagem excessivamente formal ou didática
- Pouca subjetividade ou digressão
- Ausência de falhas naturais e hesitações

Atribua uma **pontuação de autoria humana (0 a 100)**:
- 0 a 40 = Muito provavelmente IA
- 41 a 70 = Pode ter influência de IA
- 71 a 98 = Provavelmente humano, mas ainda com traços automatizados
- 99 a 100 = Autenticidade humana muito alta

Texto:
\"\"\"{texto}\"\"\"
"""

        with st.spinner("Analisando com o agente..."):
            resposta = client.beta.threads.create_and_run(
                assistant_id=ASSISTANT_ID,
                thread={"messages": [{"role": "user", "content": prompt_detector}]}
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

                if score >= 99:
                    st.success("✅ Muito provavelmente escrito por um humano autêntico (≥ 99%).")
                elif score >= 71:
                    st.info("🧠 Provavelmente humano, mas com traços que lembram IA.")
                elif score >= 41:
                    st.warning("⚠️ Pode ter sido influenciado ou revisado por IA.")
                else:
                    st.error("❌ Muito provavelmente gerado por IA.")
            else:
                st.text("Pontuação de autenticidade não identificada.")

# ---------- TAB 2: REESCRITOR ----------
with tab2:
    with st.form("form_humanizar"):
        texto_ia = st.text_area("Cole aqui o texto gerado por IA para reescrita humanizada:")
        enviar_humanizar = st.form_submit_button("✍️ Reescrever como Humano")

    if enviar_humanizar and texto_ia:
        prompt_humanizar = f"""
Você é um especialista em reescrita humanizada. Seu papel é transformar o texto abaixo — que pode ter sido escrito por IA — em uma versão com estilo humano, natural e autêntico.

Instruções:
- Use frases com variações, hesitações naturais e fluidez realista
- Evite estrutura simétrica ou polida demais
- Inclua metáforas, perguntas retóricas, pausas ou elementos subjetivos
- Reformule frases inteiras; não apenas substitua palavras
- A nova versão deve parecer escrita por um ser humano experiente

Texto original:
\"\"\"{texto_ia}\"\"\"
"""

        with st.spinner("Reescrevendo com estilo humano..."):
            resposta = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt_humanizar}],
                temperature=0.95
            )
            texto_reescrito = resposta.choices[0].message.content

            st.subheader("✍️ Texto Reescrito (Humanizado)")
            st.markdown(texto_reescrito)
