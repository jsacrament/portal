import streamlit as st
from utils import render_page

st.set_page_config(page_title="Portal Corporativo", layout="wide")

# 🔓 Simula login automático (sem autenticação)
user_data = {
    "username": "admin",
    "name": "Admin (Acesso Livre)",
    "perfil": "admin"
}

# Menu lateral baseado no perfil
menu_opcoes = ["Dashboard"]
if user_data["perfil"] == "admin":
    menu_opcoes += ["Relatórios", "Configurações"]

pagina = st.sidebar.selectbox("Menu", menu_opcoes)

# Renderização da página selecionada
render_page(pagina, user_data)
