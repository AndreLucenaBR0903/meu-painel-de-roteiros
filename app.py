import streamlit as st
from notion_client import Client
import google.generativeai as genai

# --- Configuração da Página ---
st.set_page_config(page_title="Painel de Roteiros", page_icon="🎬", layout="wide")
st.title("🤖 Assistente de World-Building")

# --- Funções do Backend ---

# Função para inicializar as conexões com as APIs de forma segura
def inicializar_conexoes():
    try:
        notion = Client(auth=st.secrets["NOTION_TOKEN"])
        genai.configure(api_key=st.secrets["GOOGLE_AI_KEY"])
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        return notion, model
    except Exception as e:
        st.error(f"Erro ao inicializar as conexões. Verifique seus segredos. Detalhes: {e}")
        return None, None

# Função para encontrar todas as tabelas (já a tínhamos)
def encontrar_tabelas(notion_client, bloco_id):
    tabelas = {}
    try:
        resposta = notion_client.blocks.children.list(block_id=bloco_id)
        for bloco in resposta["results"]:
            if bloco["type"] == "child_database":
                tabelas[bloco["child_database"]["title"]] = bloco["id"]
            elif bloco["type"] == "child_page":
                tabelas.update(encontrar_tabelas(notion_client, bloco["id"]))
    except Exception as e:
        st.warning(f"Não foi possível ler uma sub-página. Erro: {e}")
    return tabelas

# --- Início da Interface do App ---

# Inicializa as conexões
notion, model = inicializar_conexoes()

if notion and model:
    # Pega o ID da página principal dos segredos
    page_id = st.secrets["PAGE_ID"]

    # Encontra todas as tabelas e as coloca em um menu
    lista_de_tabelas = encontrar_tabelas(notion, page_id)

    if lista_de_tabelas:
        st.sidebar.header("Módulos de Geração")
        tabela_selecionada = st.sidebar.selectbox(
            "Escolha a tabela que deseja preencher:",
            options=list(lista_de_tabelas.keys())
        )

        # --- Módulo: Gerador de Opções para "Sistemas de Magia" ---
        if tabela_selecionada == "Sistemas de Magia":
            st.header("🔮 Gerador de Opções para 'Sistemas de Magia'")
            st.info("Esta ferramenta usa a IA para sugerir opções para o campo 'Fonte de Poder'.")

            tema = st.text_input("Dê um tema ou conceito para guiar a IA (opcional):", placeholder="Ex: Magia baseada em emoções, tecnologia antiga...")

            if st.button("Gerar Sugestões de 'Fonte de Poder'"):
                with st.spinner("🧠 A IA está pensando..."):
                    prompt = f"""
                    Liste 7 fontes de poder criativas e concisas para um sistema de magia de fantasia.
                    Se um tema for fornecido, baseie as sugestões nesse tema. Tema: '{tema}'.
                    Retorne apenas a lista, com um item por linha. Não adicione números, marcadores ou texto extra.
                    """
                    ai_response = model.generate_content(prompt)
                    sugestoes = [linha.strip() for linha in ai_response.text.strip().split('\n') if linha.strip()]
                    # Guarda as sugestões na memória da sessão para não perdê-las
                    st.session_state['sugestoes_magia'] = sugestoes

            # Se houver sugestões na memória, exibe-as com caixas de seleção
            if 'sugestoes_magia' in st.session_state:
                st.write("---")
                st.subheader("Sugestões Geradas:")
                selecionadas = []
                for sugestao in st.session_state['sugestoes_magia']:
                    if st.checkbox(sugestao, key=sugestao):
                        selecionadas.append(sugestao)

                st.write("---")
                if st.button("Salvar Opções Selecionadas no Notion"):
                    if not selecionadas:
                        st.warning("Nenhuma opção foi selecionada!")
                    else:
                        with st.spinner("🔄 Atualizando sua base de dados no Notion..."):
                            try:
                                database_id = lista_de_tabelas[tabela_selecionada]
                                opcoes_formatadas = [{"name": nome_opcao} for nome_opcao in selecionadas]
                                notion.databases.update(
                                    database_id=database_id,
                                    properties={"Fonte de Poder": {"select": {"options": opcoes_formatadas}}}
                                )
                                st.success("✅ Opções salvas com sucesso no Notion!")
                                # Limpa a memória para a próxima geração
                                del st.session_state['sugestoes_magia']
                            except Exception as e:
                                st.error(f"Erro ao salvar no Notion: {e}")
        else:
            st.info(f"O módulo para preencher a tabela '{tabela_selecionada}' ainda não foi construído.")
    else:
        st.error("Nenhuma base de dados foi encontrada no seu projeto do Notion.")
