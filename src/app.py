import streamlit as st

from services.pinecone_service import PineconeService
from services.openai_service import OpenAIService
from components.document_list import render_document_list
from components.chat_interface import render_chat_interface
from utils.session_state import init_session_state
from components.chat_interface import render_chat_interface

# Configuración inicial de la página
st.set_page_config(layout="wide", page_title="PDF Chatbot")

# Inicializar estado de la sesión
init_session_state()

# Inicializar servicios
if 'openai_service' not in st.session_state:
    st.session_state.openai_service = OpenAIService(
        api_base=st.secrets["AZURE_OPENAI_API_BASE"],
        api_key=st.secrets["AZURE_OPENAI_API_KEY"]
    )

if 'pinecone_service' not in st.session_state:
    st.session_state.pinecone_service = PineconeService(
        api_key=st.secrets["PINECONE_API_KEY"]
    )

# Obtener documentos disponibles
documents = st.session_state.pinecone_service.get_available_documents()

# Renderizar componentes principales
render_document_list(documents, st.session_state.pinecone_service)
render_chat_interface(
    documents, 
    st.session_state.pinecone_service, 
    st.session_state.openai_service
)