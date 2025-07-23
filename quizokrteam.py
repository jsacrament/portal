import streamlit as st
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulador de KRs com Nuvem e Votação", page_icon="✨", layout="centered")
st.title("✨ Simulador de KRs para OKR - Nuvem de Palavras & Votação")
st.markdown("Cada participante pode sugerir um KR para o OKR abaixo e votar nos seus favoritos.")

# OKR do exercício
okr = st.text_area("OKR Proposto (Objetivo):", "Aumentar o engajamento dos clientes na plataforma digital.")

if 'krs_list' not in st.session_state:
    st.session_state['krs_list'] = []
if 'votes' not in st.session_state:
    st.session_state['votes'] = {}  # email: [idx1, idx2, ...]

st.markdown("## 💡 Sugira seu KR")
with st.form("kr_form", clear_on_submit=True):
    email = st.text_input("Seu e-mail ou apelido (único):", max_chars=60)
    kr = st.text_input("Sua sugestão de KR:", max_chars=120)
    enviar = st.form_submit_button("Enviar meu KR")
    if enviar:
        if not email or not kr:
            st.warning("Preencha seu e-mail e seu KR.")
        elif any(email.lower() == k['email'].lower() for k in st.session_state['krs_list']):
            st.warning("Você já enviou um KR.")
        elif len(st.session_state['krs_list']) >= 110:
            st.warning("Limite de 110 participações atingido.")
        else:
            st.session_state['krs_list'].append({"email": email, "kr": kr})

st.markdown("---")

df = pd.DataFrame(st.session_state['krs_list'])

if not df.empty:
    st.markdown(f"### 👥 KRs sugeridos ({len(df)}/110)")
    # Mostra lista resumida e IDs
    df_exibe = df.copy()
    df_exibe.index.name = "ID"
    st.dataframe(df_exibe[["kr"]], use_container_width=True)

    # Nuvem de palavras (WordCloud)
    st.markdown("#### ☁️ Nuvem de Palavras dos KRs")
    texto = " ".join(df["kr"].tolist())
    if texto.strip():
        wc = WordCloud(width=600, height=300, background_color="white").generate(texto)
        plt.figure(figsize=(10,4))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis("off")
        st.pyplot(plt)
    else:
        st.info("Aguardando sugestões para montar a nuvem de palavras.")

    # Votação nos melhores KRs
    st.markdown("#### 🗳️ Vote nos KRs que você mais gostou (até 3 votos)")
    voto_email = st.text_input("Seu e-mail/apelido para votar:", key="voto_email")
    if voto_email:
        if voto_email.lower() not in [k['email'].lower() for k in st.session_state['krs_list']]:
            st.info("Só pode votar quem já sugeriu KR.")
        else:
            votados = st.session_state['votes'].get(voto_email.lower(), [])
            options = [f"ID {i} - {kr}" for i, kr in enumerate(df["kr"])]
            votos = st.multiselect("Escolha até 3 KRs (pelo número/descrição):", options, default=[options[i] for i in votados] if votados else [], max_selections=3)
            submit_vote = st.button("Registrar meus votos")
            if submit_vote:
                idxs = [int(v.split()[1]) for v in votos]
                st.session_state['votes'][voto_email.lower()] = idxs
                st.success("Voto(s) registrado(s)!")

    # Mostrar contagem de votos em tempo real
    st.markdown("#### 🏆 Ranking dos KRs mais votados")
    all_votes = []
    for voted in st.session_state['votes'].values():
        all_votes.extend(voted)
    contagem = Counter(all_votes)
    if contagem:
        top = contagem.most_common(10)
        for i, (idx, qtd) in enumerate(top, 1):
            st.markdown(f"**{i}º** - `{df.iloc[idx]['kr']}`<br>({qtd} voto(s))", unsafe_allow_html=True)
    else:
        st.info("Nenhum voto registrado ainda.")

    # Download
    df_votes = df.copy()
    df_votes["votos"] = [contagem.get(idx, 0) for idx in range(len(df))]
    st.download_button("⬇️ Baixar todos os KRs com votos (Excel)", df_votes.to_csv(index=False), file_name="KRs_com_votos.csv")
else:
    st.info("Nenhum KR enviado ainda. Participe!")

if len(st.session_state['krs_list']) == 110:
    st.success("Limite de 110 participações atingido! Analise os KRs com sua equipe.")
    if st.button("Reiniciar tudo para nova rodada"):
        st.session_state['krs_list'] = []
        st.session_state['votes'] = {}
