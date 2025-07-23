import streamlit as st

st.set_page_config(page_title="🧠 Quiz OKRs - Governança", page_icon="🧠", layout="centered")
st.title("🧠 Quiz 3 – Monitoramento e Governança dos OKRs")
st.subheader("Objetivo: Refletir sobre a importância do acompanhamento, governança e papel da área de dados.")

# Gabarito, justificativa e dicas
respostas = [
    "b) Acompanhamento e ciclos de feedback contínuos",
    "c) Fornecer dados confiáveis e gerar insights estratégicos",
    "d) Fazer acompanhamento constante e comunicação",
    "b) Criar metas isoladas da estratégia",
    "c) Coletivo, transparente e frequente",
    "b) São adaptados e ajustados conforme o aprendizado",
    "a) KPIs validam os resultados dos OKRs",
    "b) Painéis de BI",
    "c) Falta de transformação real",
    "b) Medir se o objetivo foi alcançado"
]
justificativas = [
    "O acompanhamento constante e ciclos de feedback permitem ajustes e engajamento ao longo do ciclo dos OKRs.",
    "O papel da área de dados é fornecer informações confiáveis e gerar insights estratégicos para orientar decisões.",
    "Governança eficiente requer acompanhamento contínuo e comunicação aberta com todos os envolvidos.",
    "Metas isoladas da estratégia dificultam o alinhamento organizacional e reduzem o impacto dos OKRs.",
    "Monitoramento coletivo, transparente e frequente garante engajamento e resultados efetivos.",
    "OKRs devem ser flexíveis, permitindo ajustes e aprendizados ao longo do tempo.",
    "KPIs ajudam a validar os resultados dos OKRs, servindo como métricas objetivas.",
    "Painéis de BI facilitam o acompanhamento visual, frequente e compartilhado dos OKRs.",
    "Metas muito conservadoras dificultam transformação e inovação real na organização.",
    "Os KRs existem para medir de forma objetiva se o objetivo foi alcançado."
]
dicas = [
    "🔎 Dica: Sempre mantenha ciclos de feedback ativos para evoluir os OKRs.",
    "💡 Curiosidade: Dados confiáveis = decisões mais inteligentes!",
    "👥 Comunicação e acompanhamento são o coração da governança.",
    "⚠️ Armadilha: Alinhe OKRs à estratégia para gerar impacto real.",
    "🙌 Monitoramento coletivo cria mais engajamento.",
    "♻️ Adaptar OKRs ao aprendizado traz resultados mais reais.",
    "📊 Use KPIs para validar, não para competir com seus OKRs.",
    "🖥️ Ferramentas visuais tornam o acompanhamento mais simples.",
    "🚀 Metas ousadas promovem a verdadeira transformação.",
    "🎯 KRs são o termômetro do alcance dos objetivos."
]

# Perguntas
perguntas = [
    "1. A chave para o sucesso dos OKRs está em:",
    "2. O papel da área de dados nos OKRs é:",
    "3. Uma boa prática de governança de OKRs inclui:",
    "4. O que é considerado uma armadilha na aplicação de OKRs?",
    "5. O monitoramento eficaz deve ser:",
    "6. OKRs funcionam melhor quando:",
    "7. Como os KPIs e OKRs se complementam?",
    "8. Qual destas ferramentas é fundamental para monitorar OKRs?",
    "9. Qual o risco de criar metas conservadoras demais nos OKRs?",
    "10. Qual é o papel dos KRs na avaliação dos OKRs?"
]

alternativas = [
    ["a) Ter KRs muito fáceis","b) Acompanhamento e ciclos de feedback contínuos","c) Não precisar de reuniões","d) Ser um documento fixo"],
    ["a) Criar gráficos bonitos","b) Ajudar na redação dos objetivos","c) Fornecer dados confiáveis e gerar insights estratégicos","d) Validar metas operacionais"],
    ["a) Compartilhar publicamente os resultados","b) Guardar os objetivos em planilhas secretas","c) Atualizar os OKRs somente no fim do trimestre","d) Fazer acompanhamento constante e comunicação"],
    ["a) Ajustar os KRs a cada ciclo","b) Criar metas isoladas da estratégia","c) Usar indicadores técnicos","d) Medir performance com KPIs"],
    ["a) Feito apenas pela liderança","b) Rígido e punitivo","c) Coletivo, transparente e frequente","d) Mensal e sigiloso"],
    ["a) Ficam apenas na liderança","b) São adaptados e ajustados conforme o aprendizado","c) Não envolvem métricas","d) São longos e fixos"],
    ["a) KPIs validam os resultados dos OKRs","b) São concorrentes","c) Substituem-se entre si","d) São usados apenas separadamente"],
    ["a) Email","b) Painéis de BI","c) Post-its","d) Excel impresso"],
    ["a) Motivação extra","b) Menor alinhamento","c) Falta de transformação real","d) Facilidade no feedback"],
    ["a) Fazer revisões ortográficas","b) Medir se o objetivo foi alcançado","c) Substituir objetivos","d) Justificar falhas"]
]

respostas_usuario = []
for i, (pergunta, opcoes) in enumerate(zip(perguntas, alternativas)):
    respostas_usuario.append(
        st.radio(f"{pergunta}", opcoes, key=f"q{i}")
    )

if st.button("Enviar respostas"):
    acertos = sum([ru == r for ru, r in zip(respostas_usuario, respostas)])
    st.markdown("---")
    st.markdown(f"**Pontuação final:** {acertos}/10")
    st.markdown("---")
    st.subheader("Feedback detalhado:")

    for i, (resp, correta, justificativa, dica) in enumerate(zip(respostas_usuario, respostas, justificativas, dicas), 1):
        if resp == correta:
            st.markdown(f"""✅  
{i}. Correta! {justificativa}  
✔️ Muito bem!""")
        else:
            st.markdown(f"""❌  
{i}. Incorreta. Sua resposta: {resp}  
Resposta correta: {correta}  
Justificativa: {justificativa}  
{dica}""")

    st.markdown("---")
    if acertos == 10:
        st.success("🏆 Parabéns, você gabaritou! Mestre dos OKRs!")
    elif acertos >= 7:
        st.info("🥇 Excelente! Você já domina o tema!")
    elif acertos >= 4:
        st.warning("🥉 Bom! Você está no caminho, mas pode revisar alguns pontos.")
    else:
        st.error("💡 Que tal revisar e tentar de novo?")
