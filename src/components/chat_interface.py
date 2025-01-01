import streamlit as st

def render_chat_interface(documents, pinecone_service, openai_service):
    """Renderiza la interfaz principal del chat"""
    if st.session_state.active_doc and documents:
        render_active_chat(documents, pinecone_service, openai_service)
    else:
        st.title("PDF Chatbot")
        st.info("👈 Selecciona o sube un documento en el panel lateral para comenzar a chatear")

def render_active_chat(documents, pinecone_service, openai_service):
    """Renderiza el chat cuando hay un documento activo"""
    doc_info = documents.get(st.session_state.active_doc, {})
    
    # Título y metadata
    st.title(f"Chat sobre: {doc_info.get('title', st.session_state.active_doc)}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.caption(f"📅 Subido: {doc_info.get('upload_date', 'Desconocido')}")
    with col2:
        st.caption(f"📄 Páginas: {doc_info.get('num_pages', 'Desconocido')}")
    
    # Mostrar historial de mensajes
    render_chat_history()
    
    # Input del chat
    handle_user_input(doc_info, pinecone_service, openai_service)

def render_chat_history():
    """Renderiza el historial de mensajes del chat"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

def handle_user_input(doc_info, pinecone_service, openai_service):
    """Maneja la entrada del usuario y genera respuestas"""
    user_input = st.chat_input("Escribe tu mensaje...")
    
    if user_input:
        # Mostrar y guardar mensaje del usuario
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
        
        # Generar embedding para la pregunta
        question_embedding = openai_service.get_embedding(user_input)
        if question_embedding:
            # Buscar en Pinecone
            query_response = pinecone_service.query_document(
                query_embedding=question_embedding,
                namespace=doc_info.get('namespace'),
                top_k=3
            )
            
            if query_response:
                # Extraer contexto relevante
                context_chunks = []
                for match in query_response.matches:
                    if hasattr(match, 'metadata') and 'chunk_text' in match.metadata:
                        context_chunks.append(match.metadata['chunk_text'])
                
                context = "\n".join(context_chunks)
                
                # Preparar mensajes para el chat
                messages = prepare_chat_messages(context)
                
                # Generar y mostrar respuesta
                with st.chat_message("assistant"):
                    with st.spinner('Pensando...'):
                        assistant_response = openai_service.get_chat_completion(messages)
                        if assistant_response:
                            st.write(assistant_response)
                            st.session_state.messages.append({
                                "role": "assistant", 
                                "content": assistant_response
                            })

def prepare_chat_messages(context):
    """Prepara los mensajes para el modelo de chat"""
    messages = [
        {
            "role": "system", 
            "content": "Eres un asistente experto que mantiene conversaciones sobre documentos PDF. "
                      "Usa el contexto proporcionado para responder de forma precisa y natural."
        },
        {
            "role": "system", 
            "content": f"Contexto del documento: {context}"
        }
    ]
    
    # Agregar historial de conversación
    for msg in st.session_state.messages:
        messages.append({"role": msg["role"], "content": msg["content"]})
    
    return messages