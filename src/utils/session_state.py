import streamlit as st

def init_session_state():
    """Inicializa todos los estados necesarios para la aplicación"""
    if 'active_doc' not in st.session_state:
        st.session_state.active_doc = None
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'processed_files' not in st.session_state:
        st.session_state.processed_files = set()
    if 'delete_confirm' not in st.session_state:
        st.session_state.delete_confirm = None
    if 'chat_mode' not in st.session_state:
        st.session_state.chat_mode = "RAG"  # Puede ser "RAG" o "NO_RAG"
    if 'document_contents' not in st.session_state:
        st.session_state.document_contents = {}  # Para modo NO_RAG
    if 'debug_mode' not in st.session_state:
        st.session_state.debug_mode = False  # Control del modo debug