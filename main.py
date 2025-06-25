import streamlit as st
from auth import check_auth
from utils import render_page

st.set_page_config(page_title="Portal Corporativo", layout="wide")

# Autenticação
user_data = check_auth()
if not user_data:
    st.stop()

# Menu lateral baseado no perfil
menu_opcoes = ["Dashboard"]
if user_data["perfil"] == "admin":
    menu_opcoes += ["Relatórios", "Configurações"]

pagina = st.sidebar.selectbox("Menu", menu_opcoes)

# Renderização da página selecionada
render_page(pagina, user_data)
