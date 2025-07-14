import streamlit as st
import streamlit_authenticator as stauth


names, users, hashed_passwords = LoginController.get_users()

authenticator = stauth.Authenticate(
  names,
  users,
  hashed_passwords,
  'bus_optimizer_app',
  'abcdef',
  cookie_expiry_days=1
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status is False:
  st.error('Usuário ou senha incorretos')
elif authentication_status is None:
  st.warning('Por favor, insira seu usuário e senha')
elif authentication_status:
  st.success(f'Bem-vindo, {name}!')
  st.write('Você está logado.')
  if st.button('Logout'):
    authenticator.logout('Logout', 'main')