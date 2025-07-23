import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ---- Autenticação Google Sheets ----
scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]
# Substitua pelo nome do seu arquivo de credenciais
credentials = ServiceAccountCredentials.from_json_keyfile_name('credenciais.json', scope)
gc = gspread.authorize(credentials)

# Substitua pelo nome da sua planilha e aba
planilha_nome = 'OKR_KRs'
aba_nome = 'Sheet1'
sheet = gc.open(planilha_nome).worksheet(aba_nome)

st.set_page_config(page_title="Simulador Colaborativo OKR", page_icon="✨", layout="centered")
st.title("✨ Simulador Colaborativo de KRs para OKR")
st.markdown("Cada participante pode sugerir um KR para o OKR abaixo e votar nos seus favoritos.")

okr = st.text_area("OKR Proposto (Objetivo):", "Aumentar o engajamento dos clientes na plataforma digital.")

# --- Submissão de KR ---
with st.form("kr_form", clear_on_submit=True):
    email = st.text_input("Seu e-mail ou apelido (único):", max_chars=60)
    kr = st.text_input("Sua sugestão de KR:", max_chars=120)
    enviar = st.form_submit_button("Enviar meu KR")
    if enviar:
        if not email or not kr:
            st.warning("Preencha seu e-mail e seu KR.")
        else:
            # Checa se já existe KR para esse e-mail
            todos = sheet.get_all_records()
            ja_tem = any(str(email).strip().lower() == str(x["email"]).strip().lower() for x in todos)
            if ja_tem:
                st.warning("Você já enviou um KR.")
            elif len(todos) >= 110:
                st.warning("Limite de 110 participações atingido.")
            else:
                # Adiciona linha: [email, kr, votos=0]
                sheet.append_row([email, kr, 0])
                st.success("KR enviado com sucesso!")

# --- Lê todos os KRs (atualizado para todos) ---
todos = sheet.get_all_records()
df = pd.DataFrame(todos)

st.markdown(f"### 👥 KRs sugeridos ({len(df)}/110)")
if not df.empty:
    df_show = df[["email", "kr", "votos"]]
    df_show.columns = ["E-mail", "KR sugerido", "Votos"]
    st.dataframe(df_show, use_container_width=True)

    # --- Nuvem de palavras ---
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

    # --- Votação ---
    st.markdown("#### 🗳️ Vote no KR que você mais gostou (1 voto por pessoa)")
    email_votante = st.text_input("Seu e-mail/apelido para votar:", key="voto_email")
    if email_votante:
        if email_votante.strip().lower() not in [str(e).strip().lower() for e in df["E-mail"]]:
            st.info("Só pode votar quem já sugeriu KR.")
        else:
            opcoes = [f"{i+1} - {kr}" for i, kr in enumerate(df["KR sugerido"])]
            escolha = st.selectbox("Escolha 1 KR:", opcoes)
            if st.button("Registrar meu voto"):
                idx = int(escolha.split(" - ")[0]) - 1
                # Só permite 1 voto por pessoa (pelo e-mail)
                votos_feitos = [str(e).strip().lower() for e in df["E-mail"] if df["votos"][df["E-mail"] == e].sum() > 0]
                if email_votante.strip().lower() in votos_feitos:
                    st.warning("Você já votou!")
                else:
                    # Incrementa o voto na célula correta
                    cell = f"C{idx+2}"  # C: votos, +2 por conta do cabeçalho e index
                    votos_atuais = int(sheet.acell(cell).value)
                    sheet.update_acell(cell, votos_atuais + 1)
                    st.success("Voto registrado!")

    # --- Ranking dos mais votados ---
    st.markdown("#### 🏆 Ranking dos KRs mais votados")
    df_sorted = df_show.sort_values(by="Votos", ascending=False)
    for i, row in df_sorted.head(10).iterrows():
        st.markdown(f"**{row['KR sugerido']}** — {row['Votos']} voto(s)")

    # --- Download dos dados
    st.download_button("⬇️ Baixar todos os KRs com votos (Excel)", df_show.to_csv(index=False), file_name="KRs_com_votos.csv")
else:
    st.info("Nenhum KR enviado ainda. Participe!")

if len(df) == 110:
    st.success("Limite de 110 participações atingido! Analise os KRs com sua equipe.")
