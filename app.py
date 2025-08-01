import streamlit as st
from notion_client import Client

# --- Configuração da Página ---
st.set_page_config(
    page_title="Painel de Roteiros",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Painel de Controle de Roteiros")
st.write("Conectando ao Notion para buscar suas bases de dados...")

# --- Conexão Segura com o Notion ---
try:
    # Acessa os segredos guardados no Streamlit Cloud
    notion_token = st.secrets["NOTION_TOKEN"]
    page_id = st.secrets["PAGE_ID"]

    # Inicializa a conexão
    notion = Client(auth=notion_token)

    # Busca o conteúdo da página do projeto
    response = notion.blocks.children.list(block_id=page_id)

    st.success("✅ Conexão com o Notion bem-sucedida!")

    st.subheader("Bases de Dados Encontradas neste Projeto:")

    # Procura por tabelas (databases) e as exibe na tela
    tabelas_encontradas = False
    for block in response["results"]:
        if block["type"] == "child_database":
            tabelas_encontradas = True
            st.write(f"- {block['child_database']['title']}")

    if not tabelas_encontradas:
        st.warning("Nenhuma tabela foi encontrada diretamente nesta página.")

except Exception as e:
    st.error(f"❌ Ocorreu um erro ao conectar com o Notion.")
    st.error(f"Detalhes do erro: {e}")
    st.info("Dicas: Verifique se seus segredos (NOTION_TOKEN e PAGE_ID) estão corretos nas configurações do app no Streamlit Cloud e se você conectou a integração a esta página no Notion.")
