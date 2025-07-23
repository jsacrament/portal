import streamlit as st
import random

st.set_page_config(page_title="🎯 Quiz OKRs", page_icon="🎯", layout="centered")
st.title("🎯 Quiz 1 – Fundamentos dos OKRs")
st.markdown("Objetivo: Avaliar a compreensão dos conceitos principais de OKRs e suas diferenças com KPIs.")

email = st.text_input("Digite seu e-mail para começar:", key="email")

if email and st.button("Iniciar Quiz"):
    st.session_state['quiz1_iniciado'] = True

if st.session_state.get("quiz1_iniciado"):
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
        ("Qual é a quantidade ideal de Resultados-Chave (KRs) por Objetivo?", "c) 3 a 5", [
            "a) 1",
            "b) 10",
            "c) 3 a 5",
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

    justificativas = [
        "OKR significa Objectives and Key Results, ou seja, Objetivos e Resultados-Chave.",
        "OKRs são ambiciosos e buscam transformação real, não apenas manutenção.",
        "KPIs olham para o presente; OKRs mostram para onde a empresa quer ir.",
        "Um bom objetivo de OKR deve ser inspirador e desafiar o time.",
        "O ideal é ter de 3 a 5 KRs por objetivo para manter o foco e a clareza.",
        "Churn Rate é um indicador de negócio (KPI), não um objetivo nem um resultado-chave.",
        "Moonshot é aquela meta ousada, quase inatingível, que incentiva a inovação.",
        "Metas tradicionais raramente focam em impacto e transformação, são conservadoras.",
        "Ciclos mais curtos, como mensal ou trimestral, favorecem adaptação contínua.",
        "OKRs promovem foco, adaptação rápida e resultados de impacto em ambientes ágeis."
    ]
    dicas = [
        "🔎 Dica: O segredo do OKR está em mensurar o que realmente importa.",
        "💡 Ambição e transformação andam junto com OKR.",
        "📊 KPI monitora desempenho, OKR direciona a mudança.",
        "🚀 Objetivos inspiradores movem pessoas!",
        "🎯 Muitos KRs diluem o foco. Mantenha entre 2 e 5.",
        "📉 KPI = métrica; OKR = direção e transformação.",
        "🌕 Moonshot: pense grande, erre rápido, aprenda rápido.",
        "⚠️ Metas tradicionais quase sempre buscam manter o status quo.",
        "⏳ Frequência curta facilita ajustes e evolução.",
        "🌀 OKRs favorecem times adaptáveis e protagonistas!"
    ]

    def shift_correct_option(opcoes, correta):
        idx = opcoes.index(correta)
        if idx == 0:
            opcoes[0], opcoes[1] = opcoes[1], opcoes[0]
        return opcoes

    random.seed(42)
    alternativas_embaralhadas = []
    respostas_certas = []
    for i, (pergunta, correta, opcoes) in enumerate(perguntas):
        alt = opcoes[:]
        random.shuffle(alt)
        alt = shift_correct_option(alt, correta)
        alternativas_embaralhadas.append(alt)
        respostas_certas.append(correta)

    respostas_usuario = []
    for i, (pergunta, opcs) in enumerate(zip([p[0] for p in perguntas], alternativas_embaralhadas)):
        resposta = st.radio(f"{i+1}. {pergunta}", opcs, key=f"q1_{i}")
        respostas_usuario.append(resposta)

    todas_respondidas = all([r is not None for r in respostas_usuario])

    if todas_respondidas:
        if st.button("Enviar respostas"):
            score = sum([resp == correta for resp, correta in zip(respostas_usuario, respostas_certas)])
            st.markdown("---")
            st.markdown(f"**Pontuação final:** {score}/10")
            st.markdown("---")
            if score >= 7:
                st.subheader("Feedback detalhado:")
                for i, (escolha, correta) in enumerate(zip(respostas_usuario, respostas_certas)):
                    if escolha == correta:
                        st.markdown(f"""✅  
{i+1}. Correta! {justificativas[i]}  
✔️ Muito bem!""")
                    else:
                        st.markdown(f"""❌  
{i+1}. Incorreta. Sua resposta: {escolha}  
Resposta correta: {correta}  
Justificativa: {justificativas[i]}  
{dicas[i]}""")
                st.markdown("---")
                if score == 10:
                    st.balloons()
                    st.success("🏆 Parabéns, você gabaritou! Mestre dos OKRs!")
                elif score >= 7:
                    st.info("🎉 Muito bem! Você compreende bem os fundamentos dos OKRs.")
            else:
                st.warning("Você acertou menos de 7. Tente novamente para ver o feedback detalhado!")
    else:
        st.info("Responda todas as perguntas para enviar o quiz.")
