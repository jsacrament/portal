import streamlit as st

st.set_page_config(page_title="🚀 Quiz Prático de OKRs", page_icon="🚀", layout="centered")

st.title("🚀 Quiz 4 – OKRs na Prática: Casos Reais e Decisões")
st.subheader("Objetivo: Avaliar a aplicação de OKRs em contextos operacionais e tomada de decisão.")

perguntas = [
    ("Você é líder de BI e quer aumentar o uso de dashboards na operação. Qual KR seria mais adequado?", 
     "b) Aumentar o uso ativo dos dashboards de 40% para 80%", [
        "a) Publicar novos relatórios diariamente",
        "b) Aumentar o uso ativo dos dashboards de 40% para 80%",
        "c) Criar uma nova base de dados",
        "d) Treinar um estagiário de dados"
    ]),
    ("Sua equipe de dados demora 5 horas para atualizar os indicadores diários. Qual objetivo faria sentido?", 
     "a) Reduzir o tempo de processamento do pipeline para 15 minutos", [
        "a) Reduzir o tempo de processamento do pipeline para 15 minutos",
        "b) Aumentar a satisfação da equipe de RH",
        "c) Trocar de ferramenta de BI",
        "d) Implementar um novo CRM"
    ]),
    ("Você tem 12 métricas em um único OKR. Qual armadilha você caiu?", 
     "b) Excesso de indicadores", [
        "a) Boa governança",
        "b) Excesso de indicadores",
        "c) Foco técnico",
        "d) Estratégia top-down"
    ]),
    ("Um gestor quer que os analistas respondam chamados ad-hoc mesmo durante o ciclo de OKRs. O que você faz?", 
     "b) Define prioridades no ciclo e negocia entregas", [
        "a) Ignora os OKRs",
        "b) Define prioridades no ciclo e negocia entregas",
        "c) Cria mais dashboards para justificar",
        "d) Faz tudo ao mesmo tempo"
    ]),
    ("Qual dessas alternativas representa uma métrica técnica que pode ser usada como KR?", 
     "a) Tempo médio de atendimento (TMA)", [
        "a) Tempo médio de atendimento (TMA)",
        "b) Lucro líquido do trimestre",
        "c) Número de campanhas de marketing",
        "d) Salário médio da equipe"
    ]),
    ("Seu objetivo é 'Elevar a confiança nos dados para decisões operacionais'. Qual KR seria adequado?", 
     "a) Aumentar cobertura de testes automatizados de 40% para 90%", [
        "a) Aumentar cobertura de testes automatizados de 40% para 90%",
        "b) Criar mais dashboards",
        "c) Diminuir o backlog de chamados para metade",
        "d) Reduzir o headcount da equipe"
    ]),
    ("Você precisa acompanhar o progresso dos OKRs semanalmente. Qual ferramenta usaria?", 
     "a) Painel com status dos KRs", [
        "a) Painel com status dos KRs",
        "b) Relatório em papel",
        "c) Tabela dinâmica no Excel",
        "d) Apontamento em agenda pessoal"
    ]),
    ("Ao revisar os OKRs, a equipe percebe que atingiu 100% de todos os KRs facilmente. O que isso indica?", 
     "b) Faltou ambição nos objetivos", [
        "a) Excelente estratégia",
        "b) Faltou ambição nos objetivos",
        "c) Falha de comunicação",
        "d) Métricas mal definidas"
    ]),
    ("Seu call center teve queda no NPS. Qual KR pode ajudar?", 
     "a) Implementar 2 modelos preditivos para identificar causas do NPS", [
        "a) Implementar 2 modelos preditivos para identificar causas do NPS",
        "b) Reduzir o número de agentes",
        "c) Automatizar relatórios",
        "d) Trocar todos os líderes"
    ]),
    ("Qual papel é responsável por transformar dados brutos em insights estratégicos para os OKRs?", 
     "c) Profissional de dados", [
        "a) Analista de RH",
        "b) Gestor Financeiro",
        "c) Profissional de dados",
        "d) Assistente de suporte"
    ])
]

justificativas = [
    "O uso ativo mede se os dashboards realmente ajudam a operação e geram valor.",
    "O objetivo foca em eficiência operacional, reduzindo tempo e custo.",
    "Excesso de indicadores dispersa foco e dificulta a execução dos OKRs.",
    "Priorizar e negociar entregas mantém o alinhamento ao que importa e evita sobrecarga.",
    "TMA é uma métrica técnica útil para medir eficiência operacional.",
    "Cobertura de testes automatizados aumenta confiança e reduz riscos nos dados.",
    "Painéis de status facilitam acompanhamento e transparência dos resultados.",
    "Facilidade em atingir todos os KRs geralmente mostra falta de desafio e ambição.",
    "Modelos preditivos ajudam a identificar e atuar nas causas do NPS, gerando impacto real.",
    "O profissional de dados converte informação em ação estratégica para os OKRs."
]

dicas = [
    "📊 Priorize sempre o uso e engajamento, não só entrega de relatório.",
    "⚡ Eficiência e agilidade são ótimos objetivos para equipes de dados.",
    "🔢 Menos é mais: limite seus KRs para garantir foco.",
    "🤝 Negociar prioridades é essencial para evitar retrabalho.",
    "🎯 KRs técnicos devem ser claros e ligados à operação.",
    "🛡️ Qualidade dos dados começa nos testes.",
    "📈 Painéis visuais promovem acompanhamento coletivo.",
    "🚀 Busque sempre objetivos desafiadores, mas alcançáveis.",
    "🔎 Diagnóstico de causa traz ações concretas para o NPS.",
    "👩‍💻 Profissionais de dados são essenciais para gerar insights de valor."
]

respostas_usuario = []
score = 0
for i, (pergunta, correta, opcoes) in enumerate(perguntas):
    escolha = st.radio(f"{i+1}. {pergunta}", opcoes, key=f"q4_{i}")
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
        st.success("🏆 Parabéns, você gabaritou! Mestre dos OKRs na prática!")
    elif score >= 7:
        st.info("🎉 Muito bem! Você está aplicando os conceitos de OKRs em situações reais.")
    elif score >= 4:
        st.warning("🧐 Quase lá! Reforce os conceitos práticos de OKRs e tente novamente.")
    else:
        st.error("🚨 Hora de revisar como aplicar OKRs em contextos reais e decisões do dia a dia.")
