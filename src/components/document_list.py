import streamlit as st

def render_document_list(documents, pinecone_service):
    """Renderiza la lista de documentos en el sidebar"""
    st.sidebar.title("Documentos")
    
    # Subida de documentos
    uploaded_file = st.sidebar.file_uploader("Subir nuevo PDF", type="pdf", key="pdf_uploader")
    if uploaded_file and uploaded_file.name not in st.session_state.processed_files:
        if process_uploaded_file(uploaded_file, pinecone_service):
            st.session_state.active_doc = uploaded_file.name
            st.rerun()
    
    # Lista de documentos disponibles
    if documents:
        with st.sidebar.expander("📚 Documentos disponibles", expanded=True):
            render_document_items(documents, pinecone_service)
    else:
        st.sidebar.info("No hay documentos disponibles")

def render_document_items(documents, pinecone_service):
    """Renderiza cada item de documento en la lista"""
    for doc_id, doc_info in documents.items():
        with st.container():
            # Contenedor para fecha y botón de borrado
            col1, col2 = st.columns([6, 1])
            with col1:
                st.caption(f"📅 {doc_info['upload_date'].split()[0]}")
            with col2:
                # Botón de eliminar
                delete_clicked = st.button(
                    "🗑️", 
                    key=f"del_{doc_id}", 
                    help="Eliminar documento",
                    type="secondary",
                    use_container_width=True
                )
                if delete_clicked:
                    st.session_state.delete_confirm = doc_id

            # Confirmar borrado si se ha hecho clic en el botón
            if st.session_state.delete_confirm == doc_id:
                render_delete_confirmation(doc_id, doc_info, pinecone_service)
            
            # Botón del documento
            render_document_button(doc_id, doc_info)
            st.markdown("---")

def render_delete_confirmation(doc_id, doc_info, pinecone_service):
    """Renderiza los botones de confirmación de borrado"""
    confirm_col1, confirm_col2 = st.columns([1, 1])
    with confirm_col1:
        if st.button("✔️ Confirmar", key=f"confirm_{doc_id}", type="primary"):
            if pinecone_service.delete_document(doc_id, doc_info['namespace']):
                st.success(f"Documento eliminado")
                # Limpiar estados
                if st.session_state.active_doc == doc_id:
                    st.session_state.active_doc = None
                    st.session_state.messages = []
                if doc_id in st.session_state.processed_files:
                    st.session_state.processed_files.remove(doc_id)
                st.session_state.delete_confirm = None
                st.rerun()
    with confirm_col2:
        if st.button("❌ Cancelar", key=f"cancel_{doc_id}", type="secondary"):
            st.session_state.delete_confirm = None
            st.rerun()

def render_document_button(doc_id, doc_info):
    """Renderiza el botón principal del documento"""
    if doc_id == st.session_state.active_doc:
        st.button(f"📄 {doc_info['title']}", key=f"btn_{doc_id}", disabled=True)
    else:
        if st.button(f"📄 {doc_info['title']}", key=f"btn_{doc_id}"):
            st.session_state.active_doc = doc_id
            st.session_state.messages = []
            st.rerun()

def process_uploaded_file(uploaded_file, pinecone_service):
    """Procesa un archivo PDF recién subido"""
    try:
        with st.sidebar.status(f'Procesando {uploaded_file.name}...'):
            if uploaded_file.name in st.session_state.processed_files:
                st.sidebar.info(f"{uploaded_file.name} ya está procesado")
                return True

            # Extraer texto y generar embeddings
            from utils.pdf_processing import extract_text_from_pdf, split_text
            pdf_text = extract_text_from_pdf(uploaded_file)
            text_chunks = split_text(pdf_text)
            
            # Generar embeddings
            embeddings = []
            for chunk in text_chunks:
                embedding = st.session_state.openai_service.get_embedding(chunk)
                if embedding:
                    embeddings.append(embedding)
            
            # Almacenar en Pinecone
            if pinecone_service.store_document(uploaded_file.name, text_chunks, embeddings):
                st.session_state.processed_files.add(uploaded_file.name)
                st.sidebar.success(f"{uploaded_file.name} procesado correctamente")
                return True
            
            return False
            
    except Exception as e:
        st.sidebar.error(f"Error procesando {uploaded_file.name}: {e}")
        return False