import streamlit as st
from openai import OpenAI
import requests
import time

# Configuração do envio de e-mail via EmailJS
def enviar_email_via_emailjs(destinatario, nome, email, respostas, feedbacks):
    service_id = "masterclass"
    template_id = "masterclass"
    user_id = "FErZC3v5hYjeGxyax"
    url = "https://api.emailjs.com/api/v1.0/email/send"

    corpo = f"Avaliação do usuário {nome} ({email}):\n\n"
    for i, (resp, feed) in enumerate(zip(respostas, feedbacks)):
        corpo += f"{i+1}. Resposta: {resp}\n   Análise da IA: {feed}\n\n"

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

# Formulário de Avaliação
st.title("✨ Avaliação da Master Class Data Galaxy")

st.write("Ajude-nos a melhorar! Responda às perguntas abaixo sobre sua experiência com a Master Class e os quizzes.")

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else st.text_input("Insira sua OpenAI API Key", type="password")
ASSISTANT_ID = st.secrets["ASSISTANT_ID"] if "ASSISTANT_ID" in st.secrets else st.text_input("Insira seu Assistant ID", type="password")

nome = st.text_input("Seu nome:")
email = st.text_input("Seu e-mail:")

perguntas = [
    {
        "pergunta": "Como você avalia a apresentação visual da Master Class?",
        "opcoes": [
            "Excelente, super envolvente!",
            "Muito boa, clara e agradável.",
            "Regular, poderia melhorar.",
            "Ruim, achei confusa ou cansativa."
        ]
    },
    {
        "pergunta": "O conteúdo apresentado foi:",
        "opcoes": [
            "Muito relevante e atualizado.",
            "Bom, atendeu às expectativas.",
            "Razoável, faltaram exemplos práticos.",
            "Pouco útil para minha realidade."
        ]
    },
    {
        "pergunta": "Como você avaliaria a interatividade dos quizzes?",
        "opcoes": [
            "Muito divertida e didática!",
            "Interessante, ajudou a fixar o conteúdo.",
            "Normal, esperava mais desafios.",
            "Desnecessária ou difícil de usar."
        ]
    },
    {
        "pergunta": "Você se sentiu motivado(a) a aprender mais sobre Engenharia de Dados após a Master Class?",
        "opcoes": [
            "Sim, me sinto muito motivado(a)!",
            "Sim, despertou meu interesse.",
            "Mais ou menos, foi neutro.",
            "Não, não me motivou."
        ]
    },
    {
        "pergunta": "Como avalia o equilíbrio entre teoria, prática e ludicidade (tema Star Wars) na experiência?",
        "opcoes": [
            "Ótimo equilíbrio, adorei a dinâmica!",
            "Bom, mas poderia ter mais prática.",
            "Teoria demais, faltou diversão.",
            "Muito lúdico, gostaria de mais conteúdo técnico."
        ]
    }
]

respostas = []
for idx, p in enumerate(perguntas):
    resp = st.radio(p["pergunta"], p["opcoes"], key=f"q{idx}")
    respostas.append(resp)

feedbacks = []
if st.button("Enviar Avaliação"):
    if not nome or not email:
        st.warning("Por favor, preencha seu nome e e-mail.")
    elif not OPENAI_API_KEY or not ASSISTANT_ID:
        st.warning("Preencha a chave da OpenAI e o Assistant ID.")
    else:
        st.info("Avaliando suas respostas com o agente Jedi...")
        client = OpenAI(api_key=OPENAI_API_KEY)

        for i, (perg, resp) in enumerate(zip(perguntas, respostas)):
            prompt = (
                f"Avalie a seguinte resposta do usuário a uma pergunta de feedback sobre um evento de Master Class sobre Engenharia de Dados e Star Wars. "
                f"Pergunta: {perg['pergunta']}\n"
                f"Resposta: {resp}\n"
                f"Comente em 1 a 2 frases o significado dessa resposta para o evento, de forma construtiva e acolhedora."
            )
            try:
                thread = client.beta.threads.create()
                client.beta.threads.messages.create(
                    thread_id=thread.id,
                    role="user",
                    content=prompt,
                )
                run = client.beta.threads.runs.create(
                    thread_id=thread.id,
                    assistant_id=ASSISTANT_ID,
                )
                status = "queued"
                with st.spinner(f"IA Jedi analisando a resposta {i+1}..."):
                    while status not in ["completed", "failed", "cancelled", "expired"]:
                        time.sleep(1.5)
                        run = client.beta.threads.runs.retrieve(
                            thread_id=thread.id,
                            run_id=run.id,
                        )
                        status = run.status
                if status == "completed":
                    messages = client.beta.threads.messages.list(thread_id=thread.id)
                    for msg in messages.data:
                        if msg.role == "assistant":
                            feedback = msg.content[0].text.value
                            break
                    else:
                        feedback = "Sem análise da IA."
                else:
                    feedback = f"IA falhou: {status}"
            except Exception as e:
                feedback = f"Erro na IA: {e}"
            feedbacks.append(feedback)
            st.success(f"Análise da IA para a pergunta {i+1}: {feedback}")

        # Envia o resultado por e-mail
        status, retorno = enviar_email_via_emailjs(
            destinatario="jsilvasacramento@gmail.com",
            nome=nome,
            email=email,
            respostas=respostas,
            feedbacks=feedbacks
        )
        if status == 200:
            st.success("Avaliação enviada por e-mail para jsilvasacramento@gmail.com!")
        else:
            st.error(f"Falha ao enviar o e-mail. Detalhes: {retorno}")

        st.markdown("---")
        st.markdown("### Seu feedback e análise do agente Jedi:")
        for idx, p in enumerate(perguntas):
            st.markdown(f"**{p['pergunta']}**")
            st.markdown(f"Resposta: {respostas[idx]}")
            st.markdown(f"Análise da IA: {feedbacks[idx]}")
            st.markdown("---")
