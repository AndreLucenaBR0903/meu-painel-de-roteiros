import streamlit as st
from notion_client import Client
import time

# --- Configuração da Página ---
st.set_page_config(page_title="Painel de Roteiros", page_icon="🎬", layout="centered")

# --- Funções do Backend ---

@st.cache_data(ttl=600)
def buscar_paginas_filhas(_notion_client, page_id):
    try:
        resposta = _notion_client.blocks.children.list(block_id=page_id)
        paginas = {}
        for bloco in resposta["results"]:
            if bloco["type"] == "child_page":
                paginas[bloco["child_page"]["title"]] = bloco["id"]
        return paginas
    except Exception as e:
        st.error(f"Erro ao buscar páginas: {e}")
        return {}

def duplicar_projeto(notion_client, modelo_id, destino_id, novo_nome):
    try:
        st.write("1/4 - Criando a nova página do projeto...")
        nova_pagina_projeto = notion_client.pages.create(
            parent={"page_id": destino_id},
            properties={"title": [{"type": "text", "text": {"content": novo_nome}}]},
            children=[{"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "Bases de Dados do Projeto"}}]}}]
        )
        novo_projeto_id = nova_pagina_projeto["id"]

        st.write("2/4 - Lendo a estrutura do modelo...")
        blocos_modelo = notion_client.blocks.children.list(block_id=modelo_id)["results"]
        tabelas_modelo = [b for b in blocos_modelo if b["type"] == "child_database"]
        
        id_map = {}
        schemas_originais = {}

        st.write("3/4 - Construindo as novas bases de dados...")
        for tabela_modelo in tabelas_modelo:
            id_antigo = tabela_modelo["id"]
            schema_original = notion_client.databases.retrieve(database_id=id_antigo)
            schemas_originais[id_antigo] = schema_original["properties"]
            
            propriedades_sem_relacao = {
                nome: prop for nome, prop in schema_original["properties"].items() if prop["type"] != "relation"
            }

            nova_tabela = notion_client.databases.create(
                parent={"page_id": novo_projeto_id},
                title=[{"type": "text", "text": {"content": tabela_modelo["child_database"]["title"]}}],
                properties=propriedades_sem_relacao
            )
            id_map[id_antigo] = nova_tabela["id"]
            time.sleep(0.5)

        st.write("4/4 - Conectando os relacionamentos entre as tabelas...")
        for id_antigo, id_novo in id_map.items():
            propriedades_originais = schemas_originais[id_antigo]
            propriedades_para_atualizar = {}

            for nome, prop in propriedades_originais.items():
                if prop["type"] == "relation":
                    id_relacao_antiga = prop["relation"]["database_id"]
                    if id_relacao_antiga in id_map:
                        id_relacao_nova = id_map[id_relacao_antiga]
                        
                        # --- A CORREÇÃO ESTÁ AQUI ---
                        # Agora especificamos que é uma "relação de mão única"
                        propriedades_para_atualizar[nome] = {
                            "relation": {
                                "database_id": id_relacao_nova,
                                "type": "single_property",
                                "single_property": {}
                            }
                        }
            
            if propriedades_para_atualizar:
                notion_client.databases.update(database_id=id_novo, properties=propriedades_para_atualizar)
                time.sleep(0.5)

        return nova_pagina_projeto["url"]

    except Exception as e:
        st.error(f"Ocorreu um erro durante a duplicação: {e}")
        return None

# --- Gerenciamento de Estado e Interface ---
if 'app_mode' not in st.session_state:
    st.session_state['app_mode'] = 'Home'

try:
    notion = Client(auth=st.secrets["NOTION_TOKEN"])
except Exception as e:
    st.error("Falha ao conectar com o Notion. Verifique seu NOTION_TOKEN.")
    st.stop()

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

elif st.session_state['app_mode'] == 'Criar':
    st.header("🚀 Criar um Novo Projeto")
    moldes_page_id = st.secrets.get("MOLDES_PAGE_ID")
    projetos_page_id = st.secrets.get("PROJETOS_PAGE_ID")

    if not moldes_page_id or not projetos_page_id:
        st.error("IDs das páginas de MOLDES ou PROJETOS não encontrados nos segredos.")
    else:
        lista_de_moldes = buscar_paginas_filhas(notion, moldes_page_id)
        if lista_de_moldes:
            modelo_escolhido_nome = st.selectbox("1. Escolha um modelo:", options=list(lista_de_moldes.keys()))
            nome_novo_projeto = st.text_input("2. Dê um nome para o seu novo projeto:")
            
            if st.button("Criar Projeto Agora"):
                if not nome_novo_projeto.strip():
                    st.warning("Por favor, insira um nome para o projeto.")
                else:
                    with st.spinner("Clonando seu projeto... Este processo pode levar um minuto."):
                        modelo_id = lista_de_moldes[modelo_escolhido_nome]
                        url_novo_projeto = duplicar_projeto(notion, modelo_id, projetos_page_id, nome_novo_projeto)
                    
                    if url_novo_projeto:
                        st.success(f"🎉 Projeto '{nome_novo_projeto}' criado com sucesso!")
                        st.markdown(f"**[Clique aqui para ver seu novo projeto no Notion]({url_novo_projeto})**")
        else:
            st.warning("Nenhum modelo foi encontrado na sua página de 'MOLDES'.")

    if st.button("⬅️ Voltar ao início"):
        st.session_state['app_mode'] = 'Home'
        st.rerun()

elif st.session_state['app_mode'] == 'Abrir':
    st.header("📂 Abrir um Projeto Existente")
    projetos_page_id = st.secrets.get("PROJETOS_PAGE_ID")
    if not projetos_page_id:
        st.error("O ID da página de projetos não foi encontrado nos segredos.")
    else:
        lista_de_projetos = buscar_paginas_filhas(notion, projetos_page_id)
        if lista_de_projetos:
            projeto_escolhido = st.selectbox("Escolha um projeto para abrir:", options=list(lista_de_projetos.keys()))
            if st.button("Abrir Projeto"):
                st.success(f"Você abriu o projeto: **{projeto_escolhido}**")
        else:
            st.warning("Nenhum projeto foi encontrado na sua página de 'PROJETOS EM ANDAMENTO'.")

    if st.button("⬅️ Voltar ao início"):
        st.session_state['app_mode'] = 'Home'
        st.rerun()
