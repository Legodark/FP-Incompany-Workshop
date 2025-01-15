import streamlit as st

def render_chat_interface(documents, pinecone_service, openai_service):
    """Renderiza la interfaz principal del chat"""
    if st.session_state.active_doc and documents:
        # Añadir toggle para modo debug en la parte superior
        col1, col2, col3 = st.columns([2, 2, 1])
        with col3:
            st.toggle("🐛 Modo Debug", key="debug_mode")
        
        render_active_chat(documents, pinecone_service, openai_service)
    else:
        st.title("PDF Chatbot")
        st.info("👈 Selecciona o sube un documento en el panel lateral para comenzar a chatear")

def render_active_chat(documents, pinecone_service, openai_service):
    """Renderiza el chat cuando hay un documento activo"""
    doc_info = documents.get(st.session_state.active_doc, {})
    
    # Título y metadata
    st.title(f"Chat sobre: {doc_info.get('title', st.session_state.active_doc)}")
    
    col1, col2, col3 = st.columns([2, 2, 3])
    with col1:
        st.caption(f"📅 Subido: {doc_info.get('upload_date', 'Desconocido')}")
    with col2:
        st.caption(f"📄 Páginas: {doc_info.get('num_pages', 'Desconocido')}")
    with col3:
        st.caption(f"🔄 Modo: {'RAG (Búsqueda semántica)' if st.session_state.chat_mode == 'RAG' else 'NO_RAG (Documento completo)'}")
    
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
        
        if st.session_state.chat_mode == "RAG":
            handle_rag_mode(user_input, doc_info, pinecone_service, openai_service)
        else:
            handle_no_rag_mode(user_input, doc_info, openai_service, pinecone_service)

def handle_rag_mode(user_input, doc_info, pinecone_service, openai_service):
    """Procesa la entrada del usuario en modo RAG"""
    # Debug info - Inicio del proceso
    if st.session_state.debug_mode:
        st.info("🔍 Debug Info (RAG Mode):")
        st.write("1. Generando embedding para la pregunta...")

    question_embedding = openai_service.get_embedding(user_input)
    if question_embedding:
        # Debug info - Embedding generado
        if st.session_state.debug_mode:
            st.write(f"✓ Embedding generado (dimensión: {len(question_embedding)})")
            st.write("2. Buscando chunks relevantes en Pinecone...")

        query_response = pinecone_service.query_document(
            query_embedding=question_embedding,
            namespace=doc_info.get('namespace'),
            top_k=3
        )
        
        if query_response:
            context_chunks = []
            scores = []
            
            for match in query_response.matches:
                if hasattr(match, 'metadata') and 'chunk_text' in match.metadata:
                    context_chunks.append(match.metadata['chunk_text'])
                    scores.append(match.score if hasattr(match, 'score') else 0)
            
            # Debug info - Chunks encontrados
            if st.session_state.debug_mode:
                st.write(f"✓ Encontrados {len(context_chunks)} chunks relevantes")
                st.write("3. Chunks seleccionados con sus scores:")
                for i, (chunk, score) in enumerate(zip(context_chunks, scores)):
                    with st.expander(f"Chunk {i+1} (Score: {score:.4f})"):
                        st.text(chunk)

            context = "\n".join(context_chunks)
            
            messages = prepare_chat_messages(context)

            # Debug info - Preparación del prompt
            if st.session_state.debug_mode:
                st.write("4. Preparando prompt para GPT:")
                with st.expander("Ver prompt completo"):
                    st.write("Mensajes del sistema:")
                    for msg in messages[:2]:  # Los primeros dos mensajes son del sistema
                        st.text(msg['content'])
            
            generate_response(messages, openai_service)
    elif st.session_state.debug_mode:
        st.error("❌ Error: No se pudo generar el embedding para la pregunta")

def handle_no_rag_mode(user_input, doc_info, openai_service, pinecone_service):
    """Procesa la entrada del usuario en modo NO_RAG"""
    # Intentar obtener el contenido del documento
    doc_content = st.session_state.document_contents.get(st.session_state.active_doc)
    
    # Si no está en session_state, intentar recuperarlo de Pinecone
    if not doc_content:
        doc_content = pinecone_service.get_full_document_text(st.session_state.active_doc)
        if doc_content:
            # Guardar en session_state para futuros usos
            st.session_state.document_contents[st.session_state.active_doc] = doc_content
    
    # Debug info
    if st.session_state.debug_mode:
        st.info("🔍 Debug Info:")
        st.write(f"- Documento activo: {st.session_state.active_doc}")
        st.write(f"- Longitud del contenido: {len(doc_content)} caracteres")
        if len(doc_content) == 0:
            st.error("⚠️ Error: No se encontró contenido para el documento activo")
            return
    
    # Si no hay contenido, mostrar error y salir
    if not doc_content:
        st.error("No se pudo recuperar el contenido del documento.")
        return
    
    # Crear un prompt más específico que fuerce al modelo a usar el contenido
    system_message = (
        "Eres un asistente experto que analiza y responde preguntas sobre documentos. "
        "A continuación se te proporcionará el contenido completo de un documento. "
        "Debes basar todas tus respuestas únicamente en la información de este documento. "
        "Si la información no está en el documento, indícalo claramente."
    )
    
    content_message = f"""
A continuación está el contenido completo del documento:

---INICIO DEL DOCUMENTO---
{doc_content}
---FIN DEL DOCUMENTO---

La pregunta del usuario es: {user_input}

Responde usando ÚNICAMENTE la información proporcionada en el documento anterior.
"""
    
    messages = [
        {
            "role": "system",
            "content": system_message
        },
        {
            "role": "user",
            "content": content_message
        }
    ]
    
    # Debug info
    if st.session_state.debug_mode:
        st.write(f"- Número de mensajes: {len(messages)}")
        st.write(f"- Longitud del content_message: {len(content_message)} caracteres")
        st.write("- Primeros 500 caracteres del documento:")
        st.code(doc_content[:500] + "...")
    
    generate_response(messages, openai_service)

def prepare_chat_messages(context):
    """Prepara los mensajes para el modelo de chat en modo RAG"""
    messages = [
        {
            "role": "system", 
            "content": "Eres un asistente experto que mantiene conversaciones sobre documentos PDF. "
                      "Usa el contexto proporcionado para responder de forma precisa y natural."
        },
        {
            "role": "system", 
            "content": f"Contexto relevante del documento: {context}"
        }
    ]
    
    # Agregar historial de conversación
    for msg in st.session_state.messages:
        messages.append({"role": msg["role"], "content": msg["content"]})
    
    return messages

def generate_response(messages, openai_service):
    """Genera y muestra la respuesta del asistente"""
    with st.chat_message("assistant"):
        with st.spinner('Pensando...'):
            assistant_response = openai_service.get_chat_completion(messages)
            if assistant_response:
                st.write(assistant_response)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": assistant_response
                })