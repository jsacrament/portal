import streamlit as st
from openai import OpenAI
import re
import time

# Configuração da página
st.set_page_config(page_title="Detector e Reescritor de Texto IA", page_icon="🧠")
st.title("🕵️ Detector de Texto: Humano ou IA?")
st.markdown("Este app permite detectar se um texto foi escrito por IA e reescrevê-lo de forma mais humana e autêntica.")

# Inicializa cliente OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
ASSISTANT_ID = st.secrets["ASSISTANT_ID"]

# Abas para DETECTOR e REESCRITOR
tab1, tab2 = st.tabs(["🔍 Detectar IA ou Humano", "✍️ Reescrever como Humano"])

# ========== TAB 1: DETECTOR ==========
with tab1:
    with st.form("form_analise"):
        texto = st.text_area("Cole aqui o texto para análise de autoria:")
        enviar = st.form_submit_button("🔍 Analisar Texto")

    if enviar and texto:
        prompt_detector = f"""
Você é um especialista em detecção de autoria textual. Analise o texto abaixo e determine, com base em estilo, fluidez, estrutura, subjetividade e outros sinais, se ele foi escrito por um ser humano ou por um modelo da família ChatGPT.

Considere:
- Linguagem excessivamente formal e explicativa
- Estrutura muito organizada (introdução, desenvolvimento, conclusão)
- Pouca subjetividade ou ausência de digressões humanas
- Conectores previsíveis e tom enciclopédico

Forneça:
1. Uma justificativa clara.
2. Uma **Pontuação de Autenticidade Humana de 0 a 100**, sendo:
   - 0–40 = Muito provavelmente IA
   - 41–70 = Pode ter influência de IA
   - 71–98 = Provavelmente humano com traços automatizados
   - 99–100 = Altamente provável que seja humano autêntico

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
                status = client.beta.threads.runs.retrieve(
                    thread_id=thread_id, run_id=run_id
                ).status

            mensagens = client.beta.threads.messages.list(thread_id=thread_id)
            resposta_assistente = next(
                (msg.content[0].text.value for msg in mensagens.data if msg.role == "assistant"),
                "❌ Resposta não encontrada."
            )

            st.subheader("🔍 Resultado da Análise")
            st.markdown(resposta_assistente)

            # Buscar pontuação com contexto
            matches = re.findall(r"(\d{1,3})", resposta_assistente)
            score = None
            for m in matches:
                contexto = resposta_assistente.lower().split(m)[0][-60:]
                if "pontuação" in contexto or "autenticidade" in contexto:
                    score = int(m)
                    break

            if score is None:
                # fallback: usar maior número entre 0-100
                valid_scores = [int(m) for m in matches if 0 <= int(m) <= 100]
                if valid_scores:
                    score = max(valid_scores)

            if score is not None:
                st.progress(score)

                if score >= 99:
                    st.success("✅ Muito provavelmente escrito por um humano autêntico (≥ 99%).")
                elif score >= 71:
                    st.info("🧠 Provavelmente humano, mas com traços de IA.")
                elif score >= 41:
                    st.warning("⚠️ Pode ter sido influenciado ou revisado por IA.")
                else:
                    st.error("❌ Muito provavelmente gerado por IA.")
            else:
                st.text("Pontuação de autenticidade não identificada.")

# ========== TAB 2: REESCRITOR ==========
with tab2:
    with st.form("form_humanizar"):
        texto_ia = st.text_area("Cole aqui o texto gerado por IA para reescrita humanizada:")
        enviar_humanizar = st.form_submit_button("✍️ Reescrever como Humano")

    if enviar_humanizar and texto_ia:
        prompt_humanizar = f"""
Você é um revisor especializado em transformar textos escritos por inteligência artificial em conteúdos com estilo humano.

Reescreva o texto abaixo com:
- Variedade de vocabulário e estruturas
- Frases com hesitações naturais, pausas e ritmo humano
- Inserção sutil de subjetividade, opiniões ou analogias
- Estilo fluido, não mecânico, sem repetições previsíveis

Evite copiar a estrutura do original. Reformule com liberdade criativa, mantendo o sentido geral.

Texto original:
\"\"\"{texto_ia}\"\"\"
"""

        with st.spinner("Reescrevendo de forma humanizada..."):
            resposta = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt_humanizar}],
                temperature=0.95
            )
            texto_reescrito = resposta.choices[0].message.content

            st.subheader("✍️ Texto Reescrito (Humanizado)")
            st.markdown(texto_reescrito)
