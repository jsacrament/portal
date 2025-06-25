import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

def check_auth():
    with open('users.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )

    name, auth_status, username = authenticator.login('Login', 'main')

    if auth_status:
        authenticator.logout('Logout', 'sidebar')
        st.sidebar.success(f"Bem-vindo, {name}!")
        perfil = config['credentials']['usernames'][username]['perfil']
        return {"username": username, "name": name, "perfil": perfil}
    elif auth_status is False:
        st.error('Usuário ou senha inválidos.')
    elif auth_status is None:
        st.warning('Por favor, insira suas credenciais.')

    return None
