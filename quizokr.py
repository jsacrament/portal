
import streamlit as st
import pandas as pd
import smtplib
import qrcode
import io
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configurações
st.set_page_config(page_title="🎯 Quiz OKRs", page_icon="🎯", layout="centered")

# Função para enviar e-mail
def enviar_email(destinatario, assunto, corpo):
    import os
    remetente = os.getenv("EMAIL_REMETENTE")
    senha = os.getenv("EMAIL_SENHA")
    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = assunto
    msg.attach(MIMEText(corpo, 'plain'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(remetente, senha)
            server.send_message(msg)
        return True
    except Exception as e:
        st.error(f"Erro ao enviar e-mail: {e}")
        return False

# Função para gerar QR Code
def gerar_qrcode(link):
    img = qrcode.make(link)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    st.image(buf.getvalue(), caption="📲 Escaneie para fazer novamente")

# Cabeçalho
st.title("🎯 Quiz 1 – Fundamentos dos OKRs")
st.markdown("Objetivo: Avaliar a compreensão dos conceitos principais de OKRs e suas diferenças com KPIs.")
email = st.text_input("Digite seu e-mail para começar:", key="email")

if email and st.button("Iniciar Quiz"):
    st.session_state['quiz_iniciado'] = True

if st.session_state.get("quiz_iniciado"):
    score = 0

    perguntas = [
        ("O que significa a sigla OKR?", "c) Objectives and Key Results", [
            "a) Objectives and Knowledge Rate",
            "b) Organizational Key Reports",
            "c) Objectives and Key Results",
            "d) Operational Key Resources"
        ]),
        ("Qual das opções representa uma característica dos OKRs?", "d) São ambiciosos e focados em transformação", [
            "a) São metas conservadoras",
            "b) Têm ciclos longos e fixos",
            "c) São orientados ao passado",
            "d) São ambiciosos e focados em transformação"
        ]),
        ("Qual a principal diferença entre KPIs e OKRs?", "b) KPIs monitoram o presente e OKRs direcionam o futuro", [
            "a) KPIs são qualitativos e OKRs são quantitativos",
            "b) KPIs monitoram o presente e OKRs direcionam o futuro",
            "c) Ambos são iguais",
            "d) OKRs são mais técnicos"
        ]),
        ("Um bom objetivo em um OKR deve ser:", "b) Ambicioso e inspirador", [
            "a) Técnico e detalhado",
            "b) Ambicioso e inspirador",
            "c) Baseado em backlog",
            "d) Específico e conservador"
        ]),
        ("Qual é a quantidade ideal de Resultados-Chave (KRs) por Objetivo?", "c) 2 a 5", [
            "a) 1",
            "b) 10",
            "c) 2 a 5",
            "d) Quantos forem possíveis"
        ]),
        ("Qual exemplo abaixo é um KPI e não um OKR?", "c) Churn Rate", [
            "a) Aumentar NPS de 35 para 55",
            "b) Implementar 3 modelos preditivos",
            "c) Churn Rate",
            "d) Transformar o BI em parceiro estratégico"
        ]),
        ("Qual tipo de objetivo representa uma meta ambiciosa que pode não ser totalmente alcançada?", "d) Moonshot", [
            "a) Estratégico",
            "b) Tático",
            "c) Roofshot",
            "d) Moonshot"
        ]),
        ("Qual afirmativa está INCORRETA sobre metas tradicionais?", "c) Têm foco em impacto e transformação", [
            "a) Geralmente são conservadoras",
            "b) São pouco adaptáveis",
            "c) Têm foco em impacto e transformação",
            "d) São isoladas por departamento"
        ]),
        ("Ciclos de OKRs geralmente ocorrem em qual frequência?", "c) Mensal ou Trimestral", [
            "a) Anual",
            "b) Quinzenal",
            "c) Mensal ou Trimestral",
            "d) Semestral"
        ]),
        ("Por que os OKRs são mais eficazes do que metas tradicionais em ambientes ágeis?", "c) Porque promovem foco, adaptação e impacto", [
            "a) Porque são mais simples",
            "b) Porque são fixos",
            "c) Porque promovem foco, adaptação e impacto",
            "d) Porque não precisam de acompanhamento"
        ])
    ]

    respostas = []
    for i, (pergunta, correta, opcoes) in enumerate(perguntas):
        escolha = st.radio(f"{i+1}. {pergunta}", opcoes, key=f"q{i}")
        respostas.append((escolha, correta))
        if escolha == correta:
            score += 1

    if st.button("Enviar respostas"):
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df = pd.DataFrame([[email, score, data]], columns=["email", "pontuacao", "data"])
        try:
            df.to_csv("ranking.csv", mode="a", header=not Path("ranking.csv").exists(), index=False)
        except:
            st.warning("⚠️ Não foi possível gravar a pontuação localmente.")

        st.success(f"✅ Você acertou {score} de 10 perguntas!")
        if score == 10:
            st.balloons()
        elif score >= 7:
            st.info("🎉 Muito bem! Você compreende bem os fundamentos dos OKRs.")
        elif score >= 4:
            st.warning("🧐 Você está no caminho certo, mas vale revisar alguns conceitos.")
        else:
            st.error("🚨 É recomendável revisar os conceitos fundamentais de OKRs.")

        corpo = f"Olá!

Você concluiu o Quiz OKR com {score}/10 acertos.

Obrigado por participar!"
        enviar_email(email, "Resultado do seu Quiz OKR", corpo)

        gerar_qrcode("https://quiz-okr.streamlit.app")  # ou link local
        st.info("🔁 Escaneie o QR Code para refazer o quiz.")

        # Mostrar top 5 ranking
        try:
            df_total = pd.read_csv("ranking.csv")
            top5 = df_total.sort_values(by="pontuacao", ascending=False).head(5)
            st.subheader("🏆 Top 5 Pontuações")
            st.table(top5)
        except:
            st.warning("⚠️ Ranking ainda não disponível.")
