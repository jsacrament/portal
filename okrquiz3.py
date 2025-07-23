import streamlit as st
import random

st.set_page_config(page_title="🧠 Quiz OKRs - Governança", page_icon="🧠", layout="centered")
st.title("🧠 Quiz 3 – Monitoramento e Governança dos OKRs")
st.subheader("Objetivo: Refletir sobre a importância do acompanhamento, governança e papel da área de dados.")

respostas_certas = [
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

perguntas = [
    "A chave para o sucesso dos OKRs está em:",
    "O papel da área de dados nos OKRs é:",
    "Uma boa prática de governança de OKRs inclui:",
    "O que é considerado uma armadilha na aplicação de OKRs?",
    "O monitoramento eficaz deve ser:",
    "OKRs funcionam melhor quando:",
    "Como os KPIs e OKRs se complementam?",
    "Qual destas ferramentas é fundamental para monitorar OKRs?",
    "Qual o risco de criar metas conservadoras demais nos OKRs?",
    "Qual é o papel dos KRs na avaliação dos OKRs?"
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

# Embaralhar opções, mas nunca deixar a resposta certa na posição A
def shift_correct_option(opcoes, correta):
    idx = opcoes.index(correta)
    if idx == 0:
        opcoes[0], opcoes[1] = opcoes[1], opcoes[0]
    return opcoes

random.seed(2024)
alternativas_embaralhadas = []
for i, opcoes in enumerate(alternativas):
    alt = opcoes[:]
    random.shuffle(alt)
    alt = shift_correct_option(alt, respostas_certas[i])
    alternativas_embaralhadas.append(alt)

respostas_usuario = []
for i, (pergunta, opcs) in enumerate(zip(perguntas, alternativas_embaralhadas)):
    resposta = st.radio(f"{i+1}. {pergunta}", opcs, key=f"q3_{i}")
    respostas_usuario.append(resposta)

todas_respondidas = all([r is not None for r in respostas_usuario])

if todas_respondidas:
    if st.button("Enviar respostas"):
        acertos = sum([resp == correta for resp, correta in zip(respostas_usuario, respostas_certas)])
        st.markdown("---")
        st.markdown(f"**Pontuação final:** {acertos}/10")
        st.markdown("---")
        if acertos >= 7:
            st.subheader("Feedback detalhado:")
            for i, (resp, correta, justificativa, dica) in enumerate(zip(respostas_usuario, respostas_certas, justificativas, dicas), 1):
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
                st.balloons()
                st.success("🏆 Parabéns, você gabaritou! Mestre dos OKRs!")
            elif acertos >= 7:
                st.info("🥇 Excelente! Você já domina o tema!")
        else:
            st.warning("Você acertou menos de 7. Tente novamente para ver o feedback detalhado!")
else:
    st.info("Responda todas as perguntas para enviar o quiz.")
