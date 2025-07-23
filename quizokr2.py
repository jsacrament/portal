import streamlit as st

st.set_page_config(page_title="🧩 Quiz OKRs no BI", page_icon="🧩", layout="centered")

st.title("🧩 Quiz 2 – Aplicação Prática de OKRs no BI")
st.subheader("Objetivo: Testar a capacidade de reconhecer boas práticas de construção e desdobramento de OKRs.")

perguntas = [
    ("Na prática, um bom Objetivo deve ser:", "c) Inspirador e qualitativo",
     ["a) Quantificável", "b) Detalhado tecnicamente", "c) Inspirador e qualitativo", "d) Curto e irrelevante"]),
    ("Qual destes seria um KR adequado para um time de Engenharia de Dados?", "b) Reduzir tempo de processamento de pipeline de 4h para 15 minutos",
     ["a) Aumentar o engajamento em redes sociais", "b) Reduzir tempo de processamento de pipeline de 4h para 15 minutos", "c) Publicar dashboards no mural da empresa", "d) Treinar 5 novos colaboradores"]),
    ("O que é o cascateamento de OKRs?", "b) O alinhamento dos OKRs da empresa até o nível individual",
     ["a) A ordenação de KRs por urgência", "b) O alinhamento dos OKRs da empresa até o nível individual", "c) A priorização de tarefas operacionais", "d) A divisão dos KPIs entre setores"]),
    ("Qual destas práticas deve ser evitada ao construir OKRs?", "b) Ter mais de 5 KRs por objetivo",
     ["a) Alinhar com os objetivos da empresa", "b) Ter mais de 5 KRs por objetivo", "c) Ser mensurável", "d) Estar conectada à estratégia do call center"]),
    ("Um bom resultado-chave (KR) deve ser:", "c) Mensurável e específico",
     ["a) Inspirador e qualitativo", "b) Vago, para dar margem", "c) Mensurável e específico", "d) Geral e de longo prazo"]),
    ("Na construção de OKRs, o primeiro passo é:", "c) Entender a estratégia do negócio",
     ["a) Definir KPIs", "b) Reunir o time", "c) Entender a estratégia do negócio", "d) Escolher as ferramentas"]),
    ("OKRs bem construídos ajudam equipes de dados a:", "c) Ter foco no que mais importa em cada ciclo",
     ["a) Reduzirem o número de reuniões", "b) Ignorar demandas ad-hoc", "c) Ter foco no que mais importa em cada ciclo", "d) Automatizar todo o trabalho"]),
    ("Qual métrica é típica de Call Centers e pode ser um KR?", "a) TMA – Tempo Médio de Atendimento",
     ["a) TMA – Tempo Médio de Atendimento", "b) ROI – Retorno sobre investimento", "c) RPA – Automação Robótica", "d) SQL – Linguagem de banco de dados"]),
    ("O que significa “Adoção de Insights” como métrica?", "c) Percentual de recomendações baseadas em dados implementadas",
     ["a) Quantos dashboards foram criados", "b) Quantas pessoas leram os relatórios", "c) Percentual de recomendações baseadas em dados implementadas", "d) Quantas visualizações teve um gráfico"]),
    ("Na Master Class, o exercício prático inclui:", "b) Definir OKRs com base em um cenário real",
     ["a) Criar um dashboard", "b) Definir OKRs com base em um cenário real", "c) Programar scripts", "d) Traduzir metas em inglês"])
]

justificativas = [
    "O objetivo precisa engajar, ser inspirador e mostrar direção clara. O mensurável é papel do KR.",
    "KR relevante para Engenharia de Dados foca em resultado concreto e melhoria do core do time.",
    "Cascatear OKRs é garantir alinhamento dos objetivos do estratégico ao operacional/individual.",
    "Evite ter mais de 5 KRs por objetivo para não dispersar o foco e dificultar a gestão.",
    "Resultados-chave (KRs) precisam ser mensuráveis e claros, nunca vagos ou subjetivos.",
    "Antes de definir OKRs, compreenda a estratégia do negócio para garantir relevância.",
    "OKRs focam esforços do time no que é prioridade real de cada ciclo, evitando dispersão.",
    "TMA é métrica clássica e útil de call center, ajudando a medir eficiência e atendimento.",
    "Adoção de Insights mede a ação efetiva baseada em recomendações de dados, não só relatório.",
    "O exercício coloca a teoria na prática, desafiando a construir OKRs de um caso real."
]

dicas = [
    "💡 Objetivos motivam, KRs comprovam resultado.",
    "⏱️ Sempre busque KRs mensuráveis e com impacto claro.",
    "🔄 Alinhamento estratégico traz resultado concreto.",
    "🔢 Mantenha foco: limite os KRs para execução eficaz.",
    "📏 KR sempre com número, prazo ou parâmetro.",
    "🗺️ Estratégia é o ponto de partida de bons OKRs.",
    "🎯 Foco do time é diferencial em ambientes de dados.",
    "☎️ TMA é KPI clássico em operações de atendimento.",
    "🟢 O que importa é recomendação implementada.",
    "🔎 OKRs práticos aceleram aprendizado real!"
]

respostas_usuario = []
score = 0
for i, (pergunta, correta, opcoes) in enumerate(perguntas):
    escolha = st.radio(f"{i+1}. {pergunta}", opcoes, key=f"q2_{i}")
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
        st.info("🎉 Muito bem! Você está aplicando bem os conceitos de OKRs no BI.")
    elif score >= 4:
        st.warning("🧐 Quase lá! Reforce os conceitos e tente novamente.")
    else:
        st.error("🚨 Hora de revisar os fundamentos e práticas de OKRs no BI.")
