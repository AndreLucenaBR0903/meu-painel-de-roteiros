import streamlit as st
from notion_client import Client

# --- Configuração da Página ---
st.set_page_config(
    page_title="Painel de Roteiros",
    page_icon="🎬",
    layout="centered"
)

# --- Funções do Backend ---

# Função para buscar as sub-páginas (nossos modelos ou projetos) dentro de uma página-mãe
@st.cache_data(ttl=600) # Cache para não sobrecarregar o Notion
def buscar_paginas_filhas(_notion_client, page_id):
    try:
        resposta = _notion_client.blocks.children.list(block_id=page_id)
        paginas = {}
        for bloco in resposta["results"]:
            if bloco["type"] == "child_page":
                # Guarda o nome da página e seu ID
                paginas[bloco["child_page"]["title"]] = bloco["id"]
        return paginas
    except Exception as e:
        st.error(f"Erro ao buscar páginas: {e}")
        return {}

# --- Gerenciamento de Estado ---
if 'app_mode' not in st.session_state:
    st.session_state['app_mode'] = 'Home'

# --- Interface Principal ---

# Tenta conectar ao Notion
try:
    notion = Client(auth=st.secrets["NOTION_TOKEN"])
except Exception as e:
    st.error("Falha ao conectar com o Notion. Verifique seu NOTION_TOKEN nos segredos.")
    st.stop() # Para a execução se não conseguir conectar

# --- Tela de Boas-Vindas ---
if st.session_state['app_mode'] == 'Home':
    st.title("🎬 Bem-vindo ao seu Painel de Roteiros")
    st.write("---")
    st.subheader("O que você deseja fazer?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Criar um novo projeto", use_container_width=True, type="primary"):
            st.session_state['app_mode'] = 'Criar'
            st.rerun()
    with col2:
        if st.button("📂 Abrir um projeto existente", use_container_width=True):
            st.session_state['app_mode'] = 'Abrir'
            st.rerun()

# --- Tela de "Criar Novo Projeto" ---
elif st.session_state['app_mode'] == 'Criar':
    st.header("🚀 Criar um Novo Projeto")
    
    # Busca os modelos na página de MOLDES
    moldes_page_id = st.secrets.get("MOLDES_PAGE_ID")
    if not moldes_page_id:
        st.error("O ID da página de modelos (MOLDES_PAGE_ID) não foi encontrado nos seus segredos.")
    else:
        lista_de_moldes = buscar_paginas_filhas(notion, moldes_page_id)
        if lista_de_moldes:
            modelo_escolhido = st.selectbox("1. Escolha um modelo:", options=list(lista_de_moldes.keys()))
            nome_novo_projeto = st.text_input("2. Dê um nome para o seu novo projeto:")
            
            if st.button("Criar Projeto"):
                st.info(f"Nosso próximo passo será construir a lógica para duplicar o modelo '{modelo_escolhido}' com o nome '{nome_novo_projeto}'.")
        else:
            st.warning("Nenhum modelo foi encontrado na sua página de 'MOLDES'.")

    if st.button("⬅️ Voltar ao início"):
        st.session_state['app_mode'] = 'Home'
        st.rerun()

# --- Tela de "Abrir Projeto Existente" ---
elif st.session_state['app_mode'] == 'Abrir':
    st.header("📂 Abrir um Projeto Existente")

    # Busca os projetos na página de PROJETOS EM ANDAMENTO
    projetos_page_id = st.secrets.get("PROJETOS_PAGE_ID")
    if not projetos_page_id:
        st.error("O ID da página de projetos (PROJETOS_PAGE_ID) não foi encontrado nos seus segredos.")
    else:
        lista_de_projetos = buscar_paginas_filhas(notion, projetos_page_id)
        if lista_de_projetos:
            projeto_escolhido = st.selectbox("Escolha um projeto para abrir:", options=list(lista_de_projetos.keys()))
            
            if st.button("Abrir Projeto"):
                st.success(f"Você abriu o projeto: **{projeto_escolhido}**")
                st.info("Nosso próximo passo será carregar o painel de controle deste projeto.")
        else:
            st.warning("Nenhum projeto foi encontrado na sua página de 'PROJETOS EM ANDAMENTO'.")

    if st.button("⬅️ Voltar ao início"):
        st.session_state['app_mode'] = 'Home'
        st.rerun()
