import streamlit as st

# --- Configuração da Página ---
# Usaremos o layout "wide" para dar mais espaço ao editor de texto
st.set_page_config(
    page_title="Editor de Roteiro",
    page_icon="✍️",
    layout="wide"
)

# --- Simulação de Dados do Roteiro (no futuro, virá do Notion) ---
# Usamos o st.session_state para que os dados não se percam a cada interação
if 'roteiro' not in st.session_state:
    st.session_state['roteiro'] = {
        "Ato 1": {
            "Cena 1": "Roteiro inicial da Cena 1, Ato 1...",
            "Cena 2": "Roteiro inicial da Cena 2, Ato 1...",
        },
        "Ato 2": {
            "Cena 1": "Roteiro inicial da Cena 1, Ato 2...",
        }
    }

# --- Barra Lateral de Navegação (Sidebar) ---
st.sidebar.title("Navegação do Roteiro")
ato_selecionado = st.sidebar.radio(
    "Selecione o Ato:",
    options=list(st.session_state['roteiro'].keys()),
    key="ato_selecionado"
)

# O seletor de cenas muda dinamicamente com base no ato escolhido
cena_selecionada = st.sidebar.radio(
    "Selecione a Cena:",
    options=list(st.session_state['roteiro'][ato_selecionado].keys()),
    key="cena_selecionada"
)

# --- Área Principal de Edição ---
st.title("✍️ Editor de Roteiro")
st.header(f"{ato_selecionado} - {cena_selecionada}")

# Área de texto para exibir e editar o roteiro da cena selecionada
roteiro_atual = st.text_area(
    "Roteiro da Cena:",
    value=st.session_state['roteiro'][ato_selecionado][cena_selecionada],
    height=400,
    key="editor_texto"
)

# Salva qualquer alteração feita pelo usuário no texto
st.session_state['roteiro'][ato_selecionado][cena_selecionada] = roteiro_atual

# Botões de Ação na parte inferior
st.write("---")
col1, col2, _ = st.columns([1, 1, 5]) # Colunas para alinhar os botões

with col1:
    if st.button("✅ Aprovar Cena", use_container_width=True):
        st.success(f"Cena '{cena_selecionada}' do '{ato_selecionado}' marcada como APROVADA!")
        # Aqui, no futuro, salvaríamos o status no Notion

with col2:
    if st.button("🔄 Refazer com IA", use_container_width=True, type="primary"):
        with st.spinner("🤖 A IA está reescrevendo a cena..."):
            # Lógica de placeholder para a chamada da IA
            # No futuro, chamaríamos a API do Gemini aqui para gerar um novo texto
            novo_roteiro_ia = f"Este é um novo roteiro gerado pela IA para a {cena_selecionada} do {ato_selecionado}, com mais detalhes e diálogos."
            st.session_state['roteiro'][ato_selecionado][cena_selecionada] = novo_roteiro_ia
            st.rerun() # Força o recarregamento da página para mostrar o novo texto

