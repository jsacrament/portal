import streamlit as st

st.set_page_config(page_title="🧠 Quiz OKRs - Governança", page_icon="🧠", layout="centered")
st.markdown("""
    <style>
        .st-success {background-color: #e6ffe6;}
        .st-error {background-color: #fff0f0;}
        .badge {
            display: inline-block;
            padding: 0.3em 0.7em;
            border-radius: 12px;
            font-size: 0.8em;
            background: #FFDE59;
            color: #333;
            margin-left: 6px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 Quiz 3 – Monitoramento e Governança dos OKRs")
st.subheader("Objetivo: Refletir sobre a importância do acompanhamento, governança e papel da área de dados.")

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
    "✅ O acompanhamento constante e ciclos de feedback permitem ajustes e engajamento ao longo do ciclo dos OKRs.",
    "✅ O papel da área de dados é fornecer informações confiáveis e gerar insights estratégicos para orientar decisões.",
    "✅ Governança eficiente requer acompanhamento contínuo e comunicação aberta com todos os envolvidos.",
    "❌ Metas isoladas da estratégia dificultam o alinhamento organizacional e reduzem o impacto dos OKRs.",
    "✅ Monitoramento coletivo, transparente e frequente garante engajamento e resultados efetivos.",
    "✅ OKRs devem ser flexíveis, permitindo ajustes e aprendizados ao longo do tempo.",
    "✅ KPIs ajudam a validar os resultados dos OKRs, servindo como métricas objetivas.",
    "✅ Painéis de BI facilitam o acompanhamento visual, frequente e compartilhado dos OKRs.",
    "❌ Metas muito conservadoras dificultam transformação e inovação real na organização.",
    "✅ Os KRs existem para medir de forma objetiva se o objetivo foi alcançado."
]

dicas = [
    "Dica: Busque sempre ciclos de feedback rápidos nos seus OKRs!",
    "Fun fact: Dados bem utilizados aumentam o impacto dos OKRs.",
    "Governança é mais forte quando é coletiva e transparente.",
    "Lembre-se: Alinhar OKRs com a estratégia é essencial.",
    "Engajamento coletivo = melhores resultados!",
    "OKRs engessados não acompanham o ritmo das empresas inovadoras.",
    "KPIs e OKRs juntos são imparáveis.",
    "Ferramentas visuais tornam o progresso mais tangível.",
    "Desafie sua equipe: metas ousadas promovem inovação.",
    "Sempre meça o que importa. 😉"
]

score = 0
respostas_usuario = []

# Perguntas e barra de progresso
progress = st.progress(0)
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

for i, (pergunta, opcoes) in enumerate(zip(perguntas, alternativas)):
    respostas_usuario.append(
        st.radio(f"{pergunta}", opcoes, key=f"q{i}")
    )
    progress.progress((i+1)/len(perguntas))

if st.button("Enviar respostas"):
    st.balloons()
    st.success(f"🎯 Sua pontuação: {sum([ru==r for ru,r in zip(respostas_usuario,respostas)])} de 10 perguntas.")
    badges = ""
    acertos = sum([ru==r for ru,r in zip(respostas_usuario,respostas)])
    # Badges personalizados
    if acertos == 10:
        badges += "🏆 <span class='badge'>Gabaritou!</span>"
    elif acertos >= 7:
        badges += "🥇 <span class='badge'>Especialista</span>"
    elif acertos >= 4:
        badges += "🥉 <span class='badge'>Aprendiz</span>"
    else:
        badges += "💡 <span class='badge'>Recomeçar</span>"
    st.markdown(f"**Seu status:** {badges}", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("Feedback por questão:")

    for i, (resp, correta, justificativa, dica) in enumerate(zip(respostas_usuario, respostas, justificativas, dicas), 1):
        if resp == correta:
            st.success(
                f"**{i}. Correta!** {justificativa} <br>"
                f"<span style='color:green'>✔️ Parabéns! Você acertou.</span>", 
                icon="✅", 
                unsafe_allow_html=True
            )
        else:
            st.error(
                f"**{i}. Incorreta.** <br>"
                f"Sua resposta: <b>{resp}</b><br>Resposta correta: <b>{correta}</b><br>"
                f"{justificativa} <br>"
                f"<span style='color:orange'>{dica}</span>", 
                icon="❌",
                unsafe_allow_html=True
            )
    st.info(f"Total de acertos: {acertos}/10", icon="📊")
    if acertos == 10:
        st.success("Uau! Você merece o título de Mestre dos OKRs! 🚀")
    elif acertos >= 7:
        st.info("Mandou bem! Seu domínio de OKRs está acima da média. Continue assim! 👏")
    elif acertos >= 4:
        st.warning("Você já tem uma boa base, mas vale revisar os pontos das respostas erradas. Siga praticando!")
    else:
        st.error("Que tal estudar um pouco mais sobre governança e OKRs e tentar novamente? 💪")

