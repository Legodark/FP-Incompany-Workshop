import streamlit as st
from pinecone import Pinecone, ServerlessSpec
from datetime import datetime

class PineconeService:
    def __init__(self, api_key, index_name="pdf-index"):
        self.index_name = index_name
        try:
            self.client = Pinecone(api_key=api_key)
            self.index = self._create_or_get_index()
        except Exception as e:
            st.error(f"Error inicializando Pinecone: {e}")
            self.client = None
            self.index = None

    def _create_or_get_index(self):
        """Crea o obtiene el índice de Pinecone"""
        try:
            existing_indexes = self.client.list_indexes()
            existing_index_names = [idx.name for idx in existing_indexes]
            
            if self.index_name not in existing_index_names:
                self.client.create_index(
                    name=self.index_name,
                    dimension=1536,
                    metric='dotproduct',
                    spec=ServerlessSpec(
                        cloud='aws',
                        region=st.secrets["PINECONE_ENVIRONMENT"]
                    )
                )
                
            return self.client.Index(self.index_name)
        except Exception as e:
            st.error(f"Error creando/obteniendo índice Pinecone: {e}")
            return None
            
    def _split_text_for_metadata(self, text, max_chunk_size=30000):
        """Divide el texto en chunks más pequeños para los metadatos"""
        return [text[i:i + max_chunk_size] for i in range(0, len(text), max_chunk_size)]

    def store_document(self, doc_name, chunks, embeddings, full_text=None):
        """Almacena un documento en Pinecone"""
        try:
            # Namespace para chunks (modo RAG)
            rag_namespace = f"{doc_name}_namespace"
            
            # Metadata común
            doc_metadata = {
                'document_id': doc_name,
                'title': doc_name,
                'upload_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'num_pages': len(chunks),
                'type': 'pdf'
            }
            
            # Almacenar chunks para RAG
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                chunk_metadata = {
                    **doc_metadata,
                    'chunk_text': chunk,
                    'chunk_index': i
                }
                
                self.index.upsert(
                    vectors=[(
                        f"{doc_name}_chunk_{i}",
                        embedding,
                        chunk_metadata
                    )],
                    namespace=rag_namespace
                )
            
            # Si se proporciona el texto completo, almacenarlo en chunks para NO-RAG
            if full_text is not None:
                norag_namespace = f"{doc_name}_full_namespace"
                text_chunks = self._split_text_for_metadata(full_text)
                
                # Almacenar cada chunk del texto completo
                for i, text_chunk in enumerate(text_chunks):
                    chunk_metadata = {
                        **doc_metadata,
                        'full_text_chunk': text_chunk,
                        'chunk_index': i,
                        'total_chunks': len(text_chunks)
                    }
                    
                    # Usar el primer embedding como representativo
                    self.index.upsert(
                        vectors=[(
                            f"{doc_name}_full_{i}",
                            embeddings[0],  # Usamos el primer embedding
                            chunk_metadata
                        )],
                        namespace=norag_namespace
                    )
            
            return True
        except Exception as e:
            st.error(f"Error almacenando documento: {e}")
            return False

    def get_full_document_text(self, doc_id):
        """Recupera el texto completo de un documento"""
        try:
            norag_namespace = f"{doc_id}_full_namespace"
            
            # Usar un vector dummy para la consulta
            vector_dummy = [0.0] * 1536
            
            # Obtener todos los chunks
            response = self.index.query(
                vector=vector_dummy,
                top_k=1000,  # Un número suficientemente grande para obtener todos los chunks
                namespace=norag_namespace,
                include_metadata=True
            )
            
            if not response.matches:
                return ''
            
            # Ordenar chunks por índice
            chunks = []
            total_chunks = None
            
            for match in response.matches:
                if hasattr(match, 'metadata'):
                    metadata = match.metadata
                    chunk_index = metadata.get('chunk_index')
                    chunk_text = metadata.get('full_text_chunk', '')
                    total_chunks = metadata.get('total_chunks')
                    
                    if chunk_index is not None and chunk_text:
                        chunks.append((chunk_index, chunk_text))
            
            # Verificar que tenemos todos los chunks
            if total_chunks is None or len(chunks) != total_chunks:
                st.warning(f"Algunos chunks del documento están faltantes ({len(chunks)}/{total_chunks})")
                return ''
            
            # Ordenar y unir los chunks
            chunks.sort(key=lambda x: x[0])
            return ''.join(chunk[1] for chunk in chunks)
            
        except Exception as e:
            st.error(f"Error recuperando documento completo: {e}")
            return ''

    def query_document(self, query_embedding, namespace, top_k=3):
        """Realiza una consulta en Pinecone"""
        try:
            return self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True,
                namespace=namespace
            )
        except Exception as e:
            st.error(f"Error consultando documento: {e}")
            return None

    def delete_document(self, doc_id, namespace):
        """Elimina todas las versiones de un documento de Pinecone"""
        try:
            # Eliminar namespace RAG
            self.index.delete(namespace=namespace, deleteAll=True)
            
            # Eliminar namespace NO-RAG
            norag_namespace = f"{doc_id}_full_namespace"
            self.index.delete(namespace=norag_namespace, deleteAll=True)
            
            return True
        except Exception as e:
            st.error(f"Error eliminando documento: {e}")
            return False

    def get_available_documents(self):
        """Obtiene la lista de documentos disponibles"""
        try:
            # Obtener lista de namespaces
            stats = self.index.describe_index_stats()
            namespaces = stats.namespaces

            documents = {}
            for namespace in namespaces:
                # Solo procesar namespaces de RAG (ignorar los _full_namespace)
                if not namespace.endswith('_full_namespace'):
                    doc_name = namespace.replace('_namespace', '')
                    vector_dummy = [0.0] * 1536
                    response = self.index.query(
                        vector=vector_dummy,
                        top_k=1,
                        namespace=namespace,
                        include_metadata=True
                    )
                    
                    if response.matches:
                        metadata = response.matches[0].metadata if hasattr(response.matches[0], 'metadata') else {}
                        documents[doc_name] = {
                            'title': metadata.get('title', doc_name),
                            'upload_date': metadata.get('upload_date', 'Desconocido'),
                            'num_pages': metadata.get('num_pages', 'Desconocido'),
                            'namespace': namespace
                        }
            
            return documents
        except Exception as e:
            st.sidebar.error(f"Error obteniendo documentos: {e}")
            return {}