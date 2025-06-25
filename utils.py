import streamlit as st
import importlib

def render_page(pagina, user_data):
    paginas = {
        "Dashboard": "pages.dashboard",
        "Relatórios": "pages.relatorios",
        "Configurações": "pages.configuracoes"
    }
    modulo = paginas.get(pagina)
    if modulo:
        pagina_modulo = importlib.import_module(modulo)
        pagina_modulo.app(user_data)
    else:
        st.error("Página não encontrada.")
