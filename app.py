import streamlit as st

# --- Configuração da Página ---
st.set_page_config(
    page_title="Editor de Roteiro",
    page_icon="✍️",
    layout="wide"
)

# --- Simulação de Dados do Roteiro ---
if 'roteiro' not in st.session_state:
    st.session_state['roteiro'] = {
        "Ato 1": {
            "Cena 1": "Roteiro inicial da Cena 1, Ato 1...",
            "Cena 2": "Roteiro inicial da Cena 2, Ato 1...",
        },
        "Ato 2": {
            "Cena 1": "Roteiro inicial da Cena 1, Ato 2...",
        },
        "Ato 3": {
            "Cena 1": "Roteiro inicial da Cena 1, Ato 3...",
            "Cena 2": "Roteiro inicial da Cena 2, Ato 3...",
            "Cena 3": "Roteiro inicial da Cena 3, Ato 3...",
        }
    }

st.title("✍️ Editor de Roteiro")

# --- Criação do Layout com Duas Colunas ---
# A primeira coluna (editor) terá o dobro da largura da segunda (controles)
col_editor, col_controles = st.columns([2, 1])


# --- Coluna da Direita: Controles de Navegação ---
with col_controles:
    st.header("Navegação")
    
    # Adiciona um container com borda para organizar os controles
    with st.container(border=True):
        st.subheader("Atos")
        ato_selecionado = st.radio(
            "Selecione o Ato:",
            options=list(st.session_state['roteiro'].keys()),
            key="ato_selecionado",
            label_visibility="collapsed" # Esconde o rótulo "Selecione o Ato:"
        )

    with st.container(border=True):
        st.subheader("Cenas")
        # O seletor de cenas muda dinamicamente com base no ato escolhido
        cena_selecionada = st.radio(
            "Selecione a Cena:",
            options=list(st.session_state['roteiro'][ato_selecionado].keys()),
            key="cena_selecionada",
            label_visibility="collapsed"
        )


# --- Coluna da Esquerda: Área Principal de Edição ---
with col_editor:
    st.header(f"{ato_selecionado} - {cena_selecionada}")

    # Área de texto para exibir e editar o roteiro da cena selecionada
    roteiro_atual = st.text_area(
        "Roteiro da Cena:",
        value=st.session_state['roteiro'][ato_selecionado][cena_selecionada],
        height=450,
        key="editor_texto",
        label_visibility="collapsed"
    )

    # Salva qualquer alteração feita pelo usuário no texto
    st.session_state['roteiro'][ato_selecionado][cena_selecionada] = roteiro_atual

    # Botões de Ação na parte inferior
    st.write("---")
    botoes_col1, botoes_col2 = st.columns(2)

    with botoes_col1:
        if st.button("✅ Aprovar Cena", use_container_width=True):
            st.success(f"Cena '{cena_selecionada}' do '{ato_selecionado}' marcada como APROVADA!")
            # Aqui, no futuro, salvaríamos o status no Notion

    with botoes_col2:
        if st.button("🔄 Refazer com IA", use_container_width=True, type="primary"):
            with st.spinner("🤖 A IA está reescrevendo a cena..."):
                # Lógica de placeholder para a chamada da IA
                novo_roteiro_ia = f"Este é um novo roteiro gerado pela IA para a {cena_selecionada} do {ato_selecionado}, com mais detalhes e diálogos."
                st.session_state['roteiro'][ato_selecionado][cena_selecionada] = novo_roteiro_ia
                st.rerun()

