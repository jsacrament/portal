import streamlit as st
from openai import OpenAI
import re
import time

# Configuração da página
st.set_page_config(page_title="Detector e Reescritor de Texto IA", page_icon="🧠")
st.title("🕵️ Detector de Texto: Humano ou IA?")
st.markdown("Este app detecta se um texto foi escrito por IA e permite reescrevê-lo com estilo humano.")

# Inicializa cliente OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
ASSISTANT_ID = st.secrets["ASSISTANT_ID"]

# Abas da aplicação
tab1, tab2 = st.tabs(["🔍 Detectar IA ou Humano", "✍️ Reescrever como Humano"])

# ========== TAB 1: DETECTOR ==========
with tab1:
    with st.form("form_analise"):
        texto = st.text_area("Cole aqui o texto para análise de autoria:")
        enviar = st.form_submit_button("🔍 Analisar Texto")

    if enviar and texto:
        # PROMPT AJUSTADO para evitar falsos positivos em textos acadêmicos técnicos
        prompt_detector = f"""
Você é um especialista em detecção de autoria textual com foco em textos acadêmicos. Sua tarefa é analisar o texto a seguir e indicar se ele foi provavelmente escrito por um ser humano ou por um modelo de linguagem como o ChatGPT.

⚠️ Importante: Textos acadêmicos geralmente são formais, bem estruturados e objetivos. Isso **não deve ser considerado por si só como sinal de IA**.

🔍 Considere como indicativos de IA:
- Repetição de estruturas ou conectores de forma padronizada
- Falta de exemplos concretos ou contextualização crítica
- Linguagem genérica ou neutra em excesso
- Frases muito simétricas ou estilo explicativo repetitivo

✅ Textos humanos, mesmo técnicos, geralmente apresentam:
- Variedade estilística
- Progresso argumentativo natural
- Uso de analogias, exemplos reais ou opinião sutil

**Tarefa:**  
Analise o texto abaixo e forneça:
1. Uma justificativa detalhada
2. Uma **Pontuação de Autenticidade Humana (0 a 100)**:
   - 0–40 = Muito provavelmente IA
   - 41–70 = Influência de IA
   - 71–98 = Provavelmente humano, mas com traços automatizados
   - 99–100 = Altamente provável que seja humano

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

            # Buscar pontuação com segurança
            matches = re.findall(r"(\d{1,3})", resposta_assistente)
            score = None
            for m in matches:
                contexto = resposta_assistente.lower().split(m)[0][-60:]
                if "pontuação" in contexto or "autenticidade" in contexto:
                    score = int(m)
                    break

            if score is None:
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
Você é um revisor especialista em transformar textos escritos por inteligência artificial em versões com estilo humano autêntico.

Reescreva o texto abaixo com:
- Variedade sintática e vocabulário natural
- Frases com ritmo e pausas realistas
- Subjetividade leve, opiniões e analogias
- Estilo fluido e orgânico, sem repetições mecânicas

Evite manter a estrutura do original. Reformule com naturalidade e liberdade criativa.

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
