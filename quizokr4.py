import streamlit as st
import random

st.set_page_config(page_title="🚀 Quiz Prático de OKRs", page_icon="🚀", layout="centered")

st.title("🚀 Quiz 4 – OKRs na Prática: Casos Reais e Decisões")
st.subheader("Objetivo: Avaliar a aplicação de OKRs em contextos operacionais e tomada de decisão.")

# Perguntas com resposta certa SEMPRE fora da posição A (embaralhamento controlado)
perguntas = [
    {
        "pergunta": "Você é líder de BI e quer aumentar o uso de dashboards na operação. Qual KR seria mais adequado?",
        "correta": "Aumentar o uso ativo dos dashboards de 40% para 80%",
        "opcoes": [
            "Publicar novos relatórios diariamente",
            "Aumentar o uso ativo dos dashboards de 40% para 80%",
            "Criar uma nova base de dados",
            "Treinar um estagiário de dados"
        ],
        "justificativa": "O uso ativo mede se os dashboards realmente ajudam a operação e geram valor.",
        "dica": "📊 Priorize sempre o uso e engajamento, não só entrega de relatório."
    },
    {
        "pergunta": "Sua equipe de dados demora 5 horas para atualizar os indicadores diários. Qual objetivo faria sentido?",
        "correta": "Reduzir o tempo de processamento do pipeline para 15 minutos",
        "opcoes": [
            "Aumentar a satisfação da equipe de RH",
            "Reduzir o tempo de processamento do pipeline para 15 minutos",
            "Trocar de ferramenta de BI",
            "Implementar um novo CRM"
        ],
        "justificativa": "O objetivo foca em eficiência operacional, reduzindo tempo e custo.",
        "dica": "⚡ Eficiência e agilidade são ótimos objetivos para equipes de dados."
    },
    {
        "pergunta": "Você tem 12 métricas em um único OKR. Qual armadilha você caiu?",
        "correta": "Excesso de indicadores",
        "opcoes": [
            "Foco técnico",
            "Excesso de indicadores",
            "Boa governança",
            "Estratégia top-down"
        ],
        "justificativa": "Excesso de indicadores dispersa foco e dificulta a execução dos OKRs.",
        "dica": "🔢 Menos é mais: limite seus KRs para garantir foco."
    },
    {
        "pergunta": "Um gestor quer que os analistas respondam chamados ad-hoc mesmo durante o ciclo de OKRs. O que você faz?",
        "correta": "Define prioridades no ciclo e negocia entregas",
        "opcoes": [
            "Ignora os OKRs",
            "Cria mais dashboards para justificar",
            "Define prioridades no ciclo e negocia entregas",
            "Faz tudo ao mesmo tempo"
        ],
        "justificativa": "Priorizar e negociar entregas mantém o alinhamento ao que importa e evita sobrecarga.",
        "dica": "🤝 Negociar prioridades é essencial para evitar retrabalho."
    },
    {
        "pergunta": "Qual dessas alternativas representa uma métrica técnica que pode ser usada como KR?",
        "correta": "Tempo médio de atendimento (TMA)",
        "opcoes": [
            "Número de campanhas de marketing",
            "Salário médio da equipe",
            "Lucro líquido do trimestre",
            "Tempo médio de atendimento (TMA)"
        ],
        "justificativa": "TMA é uma métrica técnica útil para medir eficiência operacional.",
        "dica": "🎯 KRs técnicos devem ser claros e ligados à operação."
    },
    {
        "pergunta": "Seu objetivo é 'Elevar a confiança nos dados para decisões operacionais'. Qual KR seria adequado?",
        "correta": "Aumentar cobertura de testes automatizados de 40% para 90%",
        "opcoes": [
            "Criar mais dashboards",
            "Aumentar cobertura de testes automatizados de 40% para 90%",
            "Diminuir o backlog de chamados para metade",
            "Reduzir o headcount da equipe"
        ],
        "justificativa": "Cobertura de testes automatizados aumenta confiança e reduz riscos nos dados.",
        "dica": "🛡️ Qualidade dos dados começa nos testes."
    },
    {
        "pergunta": "Você precisa acompanhar o progresso dos OKRs semanalmente. Qual ferramenta usaria?",
        "correta": "Painel com status dos KRs",
        "opcoes": [
            "Relatório em papel",
            "Painel com status dos KRs",
            "Tabela dinâmica no Excel",
            "Apontamento em agenda pessoal"
        ],
        "justificativa": "Painéis de status facilitam acompanhamento e transparência dos resultados.",
        "dica": "📈 Painéis visuais promovem acompanhamento coletivo."
    },
    {
        "pergunta": "Ao revisar os OKRs, a equipe percebe que atingiu 100% de todos os KRs facilmente. O que isso indica?",
        "correta": "Faltou ambição nos objetivos",
        "opcoes": [
            "Excelente estratégia",
            "Falha de comunicação",
            "Faltou ambição nos objetivos",
            "Métricas mal definidas"
        ],
        "justificativa": "Facilidade em atingir todos os KRs geralmente mostra falta de desafio e ambição.",
        "dica": "🚀 Busque sempre objetivos desafiadores, mas alcançáveis."
    },
    {
        "pergunta": "Seu call center teve queda no NPS. Qual KR pode ajudar?",
        "correta": "Implementar 2 modelos preditivos para identificar causas do NPS",
        "opcoes": [
            "Reduzir o número de agentes",
            "Trocar todos os líderes",
            "Automatizar relatórios",
            "Implementar 2 modelos preditivos para identificar causas do NPS"
        ],
        "justificativa": "Modelos preditivos ajudam a identificar e atuar nas causas do NPS, gerando impacto real.",
        "dica": "🔎 Diagnóstico de causa traz ações concretas para o NPS."
    },
    {
        "pergunta": "Qual papel é responsável por transformar dados brutos em insights estratégicos para os OKRs?",
        "correta": "Profissional de dados",
        "opcoes": [
            "Assistente de suporte",
            "Profissional de dados",
            "Gestor Financeiro",
            "Analista de RH"
        ],
        "justificativa": "O profissional de dados converte informação em ação estratégica para os OKRs.",
        "dica": "👩‍💻 Profissionais de dados são essenciais para gerar insights de valor."
    }
]

# Função para garantir que a opção correta nunca é a primeira
def shift_correct_option(opcoes, correta):
    idx = opcoes.index(correta)
    if idx == 0:
        # Troca para posição 1 (B)
        opcoes[0], opcoes[1] = opcoes[1], opcoes[0]
    return opcoes

# Montar perguntas embaralhando as alternativas (exceto nunca na posição 0/A)
random.seed(42)  # Para reprodutibilidade, remova em produção se quiser total aleatoriedade

for p in perguntas:
    opcoes = p['opcoes'][:]
    # Embaralha e reposiciona se correta caiu na posição 0
    random.shuffle(opcoes)
    opcoes = shift_correct_option(opcoes, p['correta'])
    p['opcoes_embaralhadas'] = opcoes

respostas_usuario = []
score = 0
for i, p in enumerate(perguntas):
    escolha = st.radio(f"{i+1}. {p['pergunta']}", p['opcoes_embaralhadas'], key=f"q4_{i}")
    respostas_usuario.append(escolha)
    if escolha == p['correta']:
        score += 1

if st.button("Enviar respostas"):
    st.markdown("---")
    st.markdown(f"**Pontuação final:** {score}/10")
    st.markdown("---")
    st.subheader("Feedback detalhado:")

    for i, (escolha, p) in enumerate(zip(respostas_usuario, perguntas), 1):
        if escolha == p['correta']:
            st.markdown(f"""✅  
{i}. Correta! {p['justificativa']}  
✔️ Muito bem!""")
        else:
            st.markdown(f"""❌  
{i}. Incorreta. Sua resposta: {escolha}  
Resposta correta: {p['correta']}  
Justificativa: {p['justificativa']}  
{p['dica']}""")

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
