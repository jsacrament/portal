import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração
st.set_page_config(page_title="🎯 Quiz OKRs", page_icon="🎯", layout="centered")

# Cabeçalho
st.title("🎯 Quiz 1 – Fundamentos dos OKRs")
st.markdown("Objetivo: Avaliar a compreensão dos conceitos principais de OKRs e suas diferenças com KPIs.")
email = st.text_input("Digite seu e-mail para começar:", key="email")

if email and st.button("Iniciar Quiz"):
    st.session_state['quiz_iniciado'] = True

if st.session_state.get("quiz_iniciado"):
    perguntas = [
        # (PERGUNTA, RESPOSTA_CORRETA, [OPCOES])
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

    # Justificativas e dicas por questão (adicione suas próprias se quiser)
    justificativas = [
        "OKR significa Objectives and Key Results, ou seja, Objetivos e Resultados-Chave.",
        "OKRs são ambiciosos e buscam transformação real, não apenas manutenção.",
        "KPIs olham o presente; OKRs mostram para onde ir.",
        "Um bom objetivo deve inspirar e desafiar.",
        "O ideal é ter de 2 a 5 KRs por objetivo para manter o foco.",
        "Churn Rate é um indicador, não um objetivo ou resultado-chave.",
        "Moonshot é aquela meta ousada, quase inatingível.",
        "Metas tradicionais quase nunca focam em impacto transformador.",
        "OKRs geralmente são mensais ou trimestrais para garantir adaptação.",
        "OKRs focam em impacto, foco e adaptação, essenciais em ambientes ágeis."
    ]
    dicas = [
        "🔎 Dica: Objetivos claros e mensuráveis são fundamentais.",
        "💡 Ambição e transformação são palavras-chave dos OKRs.",
        "📊 KPI monitora o que já acontece, OKR direciona mudança.",
        "🚀 Inspire sua equipe com objetivos motivadores!",
        "🎯 Mais que 5 KRs por objetivo? Pode perder o foco!",
        "📉 KPI mede algo fixo, OKR impulsiona uma direção.",
        "🌕 Moonshot = pensar grande sem medo de errar.",
        "⚠️ Metas tradicionais: pouca mudança, pouca inovação.",
        "⏳ Frequência curta facilita ajustes rápidos.",
        "🌀 OKRs são mais dinâmicos e adaptáveis!"
    ]

    respostas_usuario = []
    score = 0
    for i, (pergunta, correta, opcoes) in enumerate(perguntas):
        escolha = st.radio(f"{i+1}. {pergunta}", opcoes, key=f"q{i}")
        respostas_usuario.append(escolha)
        if escolha == correta:
            score += 1

    if st.button("Enviar respostas"):
        st.markdown("---")
        st.markdown(f"**Pontuação final:** {score}/10")
        st.markdown("---")
        st.subheader("Feedback detalhado:")

        for i, (escolha, (_, correta, _)) in enumerate(zip(respostas_usuario, perguntas), 1):
            if escolha == correta:
                st.markdown(f"""✅  
{i}. Correta! {justificativas[i-1]}  
✔️ Muito bem!""")
            else:
                st.markdown(f"""❌  
{i}. Incorreta. Sua resposta: {escolha}  
Resposta correta: {correta}  
Justificativa: {justificativas[i-1]}  
{dicas[i-1]}""")

        st.markdown("---")
        if score == 10:
            st.balloons()
            st.success("🏆 Parabéns, você gabaritou! Mestre dos OKRs!")
        elif score >= 7:
            st.info("🎉 Muito bem! Você compreende bem os fundamentos dos OKRs.")
        elif score >= 4:
            st.warning("🧐 Você está no caminho certo, mas vale revisar alguns conceitos.")
        else:
            st.error("🚨 É recomendável revisar os conceitos fundamentais de OKRs.")
