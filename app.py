import streamlit as st

st.set_page_config(layout="wide")

st.title("Meu Painel de Controle de Roteiros")
st.header("Bem-vindo!")

st.write("Este é o início do nosso aplicativo web, rodando online!")

if st.button("Clique em mim para testar"):
    st.success("Parabéns! Seu primeiro aplicativo está funcionando!")
