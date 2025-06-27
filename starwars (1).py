import streamlit as st
from openai import OpenAI
import time
import pandas as pd
import requests
import re

# Função para envio de e-mail via EmailJS
def enviar_email_via_emailjs(destinatario, nome, email, df, total_pontos):
    service_id = "masterclass"
    template_id = "masterclass"
    user_id = "FErZC3v5hYjeGxyax"
    url = "https://api.emailjs.com/api/v1.0/email/send"

    corpo = f"Respostas do usuário {nome} ({email}):\n\n"
    corpo += df.to_string(index=False)
    corpo += f"\n\nPontuação total atribuída pelo assistente: {total_pontos} / {len(df)*10}\n"
    
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

# Quiz e lógica igual ao anterior
st.set_page_config(page_title="Quiz Star Wars: Engenharia de Dados", page_icon="🪐")
st.title("🌟 Quiz Star Wars — Suporte e Engenharia de Dados")

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else st.text_input("Insira sua OpenAI API Key", type="password")
ASSISTANT_ID = st.secrets["ASSISTANT_ID"] if "ASSISTANT_ID" in st.secrets else st.text_input("Insira seu Assistant ID", type="password")

quiz = [
    {
        "pergunta": "O que representa o 'Data Lake' na rebelião da Aliança, em comparação ao universo Star Wars?",
        "alternativas": [
            "Um depósito centralizado de dados crus, como a base secreta de Yavin 4",
            "Um robô que armazena informações de protocolos",
            "O sabre de luz azul de Luke Skywalker",
            "Um satélite de comunicação imperial"
        ],
        "resposta_certa": "Um depósito centralizado de dados crus, como a base secreta de Yavin 4"
    },
    {
        "pergunta": "Na saga, R2-D2 é famoso por carregar e entregar mensagens críticas. Em Engenharia de Dados, que ferramenta cumpre função similar?",
        "alternativas": [
            "ETL (Extract, Transform, Load)",
            "Dashboard BI",
            "Data Lakehouse",
            "Chatbot Jedi"
        ],
        "resposta_certa": "ETL (Extract, Transform, Load)"
    },
    {
        "pergunta": "Se Darth Vader fosse um pipeline de dados, qual seria o maior risco para o Império?",
        "alternativas": [
            "Falta de monitoramento de falhas",
            "Documentação excessiva",
            "Governança eficiente",
            "Backups automáticos"
        ],
        "resposta_certa": "Falta de monitoramento de falhas"
    },
    {
        "pergunta": "Explique, em poucas palavras, o que seria uma 'Replicação de Dados' usando o exemplo dos clones do planeta Kamino.",
        "alternativas": [],
        "resposta_certa": None
    },
    {
        "pergunta": "Qual componente de uma arquitetura moderna de dados seria equivalente aos holocrons Jedi (dispositivos que armazenam sabedoria milenar)?",
        "alternativas": [
            "Data Warehouse",
            "API REST",
            "Servidor de backup",
            "Processador Spark"
        ],
        "resposta_certa": "Data Warehouse"
    },
    {
        "pergunta": "Quando Luke precisa analisar sinais na Base Echo em Hoth, qual processo técnico da engenharia de dados está sendo realizado?",
        "alternativas": [
            "Ingestão de dados em tempo real",
            "Limpeza de dados históricos",
            "Criação de dashboard em Power BI",
            "Treinamento de modelo de IA"
        ],
        "resposta_certa": "Ingestão de dados em tempo real"
    },
    {
        "pergunta": "No Império, como seria chamada a política que garante que apenas determinados oficiais possam acessar certos dados secretos?",
        "alternativas": [
            "Controle de acesso (RBAC)",
            "Data Mart",
            "Carga incremental",
            "Serviço de fila"
        ],
        "resposta_certa": "Controle de acesso (RBAC)"
    },
    {
        "pergunta": "Dê um exemplo de incidente em suporte técnico usando a metáfora da pane do hiperdrive da Millennium Falcon.",
        "alternativas": [],
        "resposta_certa": None
    },
    {
        "pergunta": "Qual dos seguintes Jedi seria o mais adequado para atuar como engenheiro de dados (pela habilidade de organizar e interpretar informações)?",
        "alternativas": [
            "Yoda",
            "Chewbacca",
            "Han Solo",
            "C-3PO"
        ],
        "resposta_certa": "C-3PO"
    },
    {
        "pergunta": "No contexto de suporte, o que representa um 'backup' para a Aliança Rebelde após a destruição de Alderaan?",
        "alternativas": [
            "Uma cópia dos planos da Estrela da Morte armazenada em outro planeta",
            "O sabre de luz de Obi-Wan",
            "O treinamento Jedi de Luke",
            "A frota imperial remanescente"
        ],
        "resposta_certa": "Uma cópia dos planos da Estrela da Morte armazenada em outro planeta"
    }
]

if "identificado" not in st.session_state:
    st.session_state.identificado = False
if "nome" not in st.session_state:
    st.session_state.nome = ""
if "email" not in st.session_state:
    st.session_state.email = ""
if "indice" not in st.session_state:
    st.session_state.indice = 0
if "historico" not in st.session_state:
    st.session_state.historico = []

if not st.session_state.identificado:
    st.header("Identificação do Padawan")
    nome = st.text_input("Nome")
    email = st.text_input("E-mail")
    if st.button("Iniciar Quiz"):
        if not nome or not email:
            st.warning("Por favor, preencha nome e e-mail para começar.")
        else:
            st.session_state.nome = nome
            st.session_state.email = email
            st.session_state.identificado = True
            st.rerun()
    st.stop()

indice = st.session_state.indice
historico = st.session_state.historico
nome = st.session_state.nome
email = st.session_state.email

def extrair_nota(texto):
    """Extrai o valor da nota de 0 a 10 do texto do feedback."""
    match = re.search(r'(Nota|Pontuação):?\s*(\d{1,2})', texto, re.IGNORECASE)
    if match:
        nota = int(match.group(2))
        if 0 <= nota <= 10:
            return nota
    # Tentativa de pegar um número solto se formato mudar
    match2 = re.search(r'\b([0-9]|10)\b', texto)
    if match2:
        nota = int(match2.group(1))
        if 0 <= nota <= 10:
            return nota
    return None

if indice < len(quiz):
    q = quiz[indice]
    st.subheader(f"Pergunta {indice+1}:")
    st.write(q["pergunta"])

    resposta_usuario = ""
    resposta_valida = False

    if q["alternativas"]:
        alternativas = ["Selecione uma opção"] + q["alternativas"]
        resposta_usuario = st.radio(
            "Escolha uma opção:",
            alternativas,
            index=0,
            key=f"radio_{indice}"
        )
        resposta_valida = resposta_usuario != "Selecione uma opção"
    else:
        resposta_usuario = st.text_input(
            "Digite sua resposta:", key=f"text_{indice}"
        )
        resposta_valida = bool(resposta_usuario.strip())

    if st.button("Enviar resposta", key=f"botao_{indice}"):
        if not OPENAI_API_KEY or not ASSISTANT_ID:
            st.warning("Informe sua chave da OpenAI e seu Assistant ID para continuar.")
        elif not resposta_valida:
            st.warning("Digite ou selecione uma resposta!")
        else:
            st.info("Avaliando resposta com o assistente, aguarde...")

            instrucao = (
                "Avalie a resposta do usuário para a pergunta abaixo. "
                "Diga se está correta ou não, explique o motivo e mostre a resposta certa de forma clara, sempre mantendo o tema Star Wars e Engenharia de Dados. "
                "Se for resposta aberta, seja construtivo, use metáforas da saga e explique o conceito. "
                "Ao final, atribua uma nota de 0 a 10 para a resposta, escrevendo claramente assim: Nota: X."
            )
            if q["resposta_certa"]:
                instrucao += f"\nA resposta correta esperada é: '{q['resposta_certa']}'."

            prompt = (
                f"{instrucao}\nPergunta: {q['pergunta']}\nResposta do usuário: {resposta_usuario}"
            )

            try:
                client = OpenAI(api_key=OPENAI_API_KEY)
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
                with st.spinner("O assistente Jedi está avaliando sua resposta..."):
                    while status not in ["completed", "failed", "cancelled", "expired"]:
                        time.sleep(2)
                        run = client.beta.threads.runs.retrieve(
                            thread_id=thread.id,
                            run_id=run.id,
                        )
                        status = run.status

                if status == "completed":
                    messages = client.beta.threads.messages.list(thread_id=thread.id)
                    feedback = "Nenhum feedback do assistente."
                    nota = None
                    for msg in messages.data:
                        if msg.role == "assistant":
                            feedback = msg.content[0].text.value
                            nota = extrair_nota(feedback)
                            break
                    historico.append({
                        "nome": nome,
                        "email": email,
                        "pergunta": q["pergunta"],
                        "resposta_usuario": resposta_usuario,
                        "feedback": feedback,
                        "nota": nota if nota is not None else ""
                    })
                    st.session_state.indice += 1
                    st.rerun()
                else:
                    st.error(f"O assistente falhou: {status}")
            except Exception as e:
                st.error(f"Erro ao avaliar resposta: {e}")
else:
    st.success(f"Quiz finalizado, {nome}! Veja seu desempenho na galáxia dos dados:")
    df = pd.DataFrame(st.session_state.historico)
    total_pontos = df["nota"].replace("", 0).fillna(0).astype(int).sum()
    for i, h in enumerate(st.session_state.historico):
        st.markdown(f"**Pergunta {i+1}:** {h['pergunta']}")
        st.markdown(f"**Sua resposta:** {h['resposta_usuario']}")
        st.markdown(f"**Feedback Jedi:** {h['feedback']}")
        st.markdown(f"**Nota atribuída:** {h['nota'] if h['nota'] != '' else 'N/A'}")
        st.markdown("---")
    st.markdown(f"### 🌟 Pontuação Final: **{total_pontos} / {len(df)*10}**")
    if st.button("Enviar respostas por e-mail"):
        status, retorno = enviar_email_via_emailjs(
            destinatario="jsilvasacramento@gmail.com",
            nome=nome,
            email=email,
            df=df,
            total_pontos=total_pontos
        )
        if status == 200:
            st.success("Respostas enviadas com sucesso para jsilvasacramento@gmail.com!")
        else:
            st.error(f"Falha ao enviar o e-mail. Detalhes: {retorno}")
    st.button(
        "Reiniciar Quiz",
        on_click=lambda: [
            st.session_state.update({
                'indice': 0,
                'historico': [],
                'identificado': False,
                'nome': '',
                'email': ''
            })
        ]
    )

st.markdown("---")
st.markdown(
    "Este é um Quiz Star Wars para Engenheiros de Dados, com feedback automático de IA Jedi e pontuação personalizada! "
    "Adapte as perguntas, crie sua liga de Padawans e divirta-se treinando na galáxia dos dados 🚀"
)



