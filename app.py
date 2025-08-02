import streamlit as st

# --- Configuração da Página ---
# Usaremos o layout "centered" para uma aparência melhor na tela de boas-vindas
st.set_page_config(
    page_title="Painel de Roteiros",
    page_icon="🎬",
    layout="centered" 
)

# --- Gerenciamento de Estado ---
# Inicializa o 'modo' do aplicativo na primeira vez que o usuário abre
if 'app_mode' not in st.session_state:
    st.session_state['app_mode'] = 'Home'

# --- Lógica da Interface ---

# Se estamos na tela inicial, mostra as duas opções
if st.session_state['app_mode'] == 'Home':
    st.title("🎬 Bem-vindo ao seu Painel de Roteiros")
    st.write("---")
    st.subheader("O que você deseja fazer?")

    # Cria duas colunas para os botões ficarem lado a lado
    col1, col2 = st.columns(2)

    with col1:
        # Se o botão "Criar" for clicado...
        if st.button("🚀 Criar um novo projeto", use_container_width=True, type="primary"):
            # ...muda o estado do aplicativo para 'Criar'
            st.session_state['app_mode'] = 'Criar'
            # Força o aplicativo a recarregar imediatamente para mostrar a nova tela
            st.rerun()

    with col2:
        # Se o botão "Abrir" for clicado...
        if st.button("📂 Abrir um projeto existente", use_container_width=True):
            # ...muda o estado do aplicativo para 'Abrir'
            st.session_state['app_mode'] = 'Abrir'
            st.rerun()

# Se o usuário escolheu 'Criar', mostra esta tela
elif st.session_state['app_mode'] == 'Criar':
    st.success("Você escolheu: **Criar um novo projeto**")
    st.info("Nosso próximo passo será construir a lógica para mostrar os modelos aqui.")
    
    # Botão para voltar para a tela inicial
    if st.button("⬅️ Voltar ao início"):
        st.session_state['app_mode'] = 'Home'
        st.rerun()

# Se o usuário escolheu 'Abrir', mostra esta tela
elif st.session_state['app_mode'] == 'Abrir':
    st.success("Você escolheu: **Abrir um projeto existente**")
    st.info("Nosso próximo passo será construir a lógica para listar seus projetos existentes aqui.")

    # Botão para voltar para a tela inicial
    if st.button("⬅️ Voltar ao início"):
        st.session_state['app_mode'] = 'Home'
        st.rerun()
