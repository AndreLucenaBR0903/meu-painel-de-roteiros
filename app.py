import streamlit as st
from notion_client import Client

# --- Configuração da Página ---
st.set_page_config(
    page_title="Painel de Roteiros",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Painel de Controle de Roteiros")

# --- Conexão Segura com o Notion ---
try:
    # Acessa os segredos guardados no Streamlit Cloud
    notion_token = st.secrets["NOTION_TOKEN"]
    page_id = st.secrets["PAGE_ID"]

    # Inicializa a conexão
    notion = Client(auth=notion_token)
    
    st.info("Conectando ao Notion para buscar suas bases de dados...")

    # --- Nossa nova função "Exploradora" ---
    def encontrar_tabelas(bloco_id):
        lista_de_tabelas = []
        try:
            # Pega os filhos do bloco atual (seja a página principal ou uma sub-página)
            resposta = notion.blocks.children.list(block_id=bloco_id)
            for bloco in resposta["results"]:
                # Se o bloco for uma tabela, adiciona à nossa lista
                if bloco["type"] == "child_database":
                    lista_de_tabelas.append(bloco["child_database"]["title"])
                # Se o bloco for uma sub-página, chama a função novamente para olhar dentro dela
                elif bloco["type"] == "child_page":
                    # Pega as tabelas encontradas na sub-página e adiciona à nossa lista principal
                    tabelas_na_subpagina = encontrar_tabelas(bloco["id"])
                    lista_de_tabelas.extend(tabelas_na_subpagina)
        except Exception as e:
            st.warning(f"Não foi possível ler o conteúdo de uma sub-página. Erro: {e}")
        
        return lista_de_tabelas

    # --- Execução Principal ---
    # Começa a busca a partir da página principal do projeto
    todas_as_tabelas = encontrar_tabelas(page_id)

    st.success("✅ Busca concluída!")

    st.subheader("Todas as Bases de Dados Encontradas no Projeto:")

    if todas_as_tabelas:
        for nome_tabela in todas_as_tabelas:
            st.write(f"- {nome_tabela}")
    else:
        st.warning("Nenhuma tabela foi encontrada no projeto, nem mesmo em sub-páginas.")

except Exception as e:
    st.error(f"❌ Ocorreu um erro geral ao conectar com o Notion.")
    st.error(f"Detalhes do erro: {e}")
    st.info("Dicas: Verifique se seus segredos (NOTION_TOKEN e PAGE_ID) estão corretos.")
