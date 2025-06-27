import streamlit as st

st.set_page_config(page_title="Escolha do Sabre Jedi", page_icon="🌟")

st.title("🌟 Escolha do Sabre — Jornada do Jedi de Dados")
st.write("**Feche os olhos, ouça a Força e escolha seu sabre. Sua missão como Jedi de Dados começa agora.**")

sabres = {
    "Sabre Vermelho 🟥": {
        "titulo": "Guardião das Estruturas",
        "area": "Armazenamento e Modelagem",
        "descricao": "Você domina os cofres da informação. Cria modelos robustos e protege os dados como um verdadeiro arquiteto da galáxia.",
        "historia": """
        Ao empunhar o Sabre Vermelho, os antigos arquivos secretos se revelam diante de você. 
        Nas ruínas de Coruscant, você encontra mapas de bases perdidas e descobre como proteger a informação contra o próprio Império.
        Seus aliados o chamam quando precisam estruturar a resistência, e seu conhecimento constrói pontes entre sistemas de planetas distantes.
        """
    },
    "Sabre Azul 🟦": {
        "titulo": "Mestre dos Fluxos",
        "area": "Pipelines e Orquestração",
        "descricao": "Você guia os dados pelo hiperespaço. Coordena tarefas, conecta sistemas e garante que a Força flua sem interrupções.",
        "historia": """
        O Sabre Azul cintila como um rio de dados cruzando a galáxia. 
        Nos túneis secretos de Bespin, você desvia fluxos de informação antes que sejam capturados por caçadores de recompensas.
        Sua habilidade em conectar fontes e destinos faz de você o verdadeiro Maestro da Orquestra dos Dados!
        """
    },
    "Sabre Verde 🟩": {
        "titulo": "Visionário da Verdade",
        "area": "Visualização e Business Intelligence",
        "descricao": "Você revela o invisível. Transforma números em narrativas e dashboards em sabedoria estratégica para toda a Aliança.",
        "historia": """
        Com o Sabre Verde em mãos, você enxerga padrões onde outros só veem caos. 
        Nos salões da Aliança Rebelde, seus painéis interativos inspiram estratégias que decidem batalhas. 
        Você transforma dados brutos em visões que guiam Jedi e Generais para a vitória.
        """
    },
    "Sabre Amarelo 🟨": {
        "titulo": "Guardião da Ordem Galáctica",
        "area": "Governança e Qualidade de Dados",
        "descricao": "Você garante integridade e ética na galáxia. Defende normas, combate a corrupção dos dados e protege a privacidade interplanetária.",
        "historia": """
        O Sabre Amarelo brilha quando há desordem. 
        Nas assembleias de Naboo, você estabelece regras justas e pune quem corrompe os registros da República.
        Sob seu olhar vigilante, nem mesmo um bit foge à lei galáctica!
        """
    }
}

sabres_list = list(sabres.keys())
escolha = st.radio("Escolha seu sabre:", sabres_list, index=0)

sabre = sabres[escolha]
st.markdown(f"### {escolha} — {sabre['titulo']}")
st.markdown(f"**{sabre['area']}**")
st.markdown(sabre['descricao'])

if st.button("Confirmar Escolha"):
    st.success(f"Parabéns! Você escolheu o {escolha}.")
    st.markdown("---")
    st.markdown(f"#### 🌌 Sua Jornada Jedi:")
    st.markdown(sabre['historia'])
    st.balloons()
    
    # Adiciona imagem temática de estrelas com parâmetro atualizado
    st.image("https://www.adrenaline.com.br/wp-content/uploads/2025/05/darth-cader-fromtine-chamada-ai-912x569.webp", caption="A Força está com você!", use_container_width=True)



