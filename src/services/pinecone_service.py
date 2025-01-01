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
            if self.index_name not in [idx.name for idx in existing_indexes]:
                self.client.create_index(
                    name=self.index_name,
                    dimension=1536,
                    metric='dotproduct',
                    spec=ServerlessSpec(cloud='aws', region=st.secrets["PINECONE_ENVIRONMENT"])
                )
            return self.client.Index(self.index_name)
        except Exception as e:
            st.sidebar.error(f"Error con Pinecone: {e}")
            return None

    def get_available_documents(self):
        """Obtiene la lista de documentos disponibles"""
        try:
            stats = self.index.describe_index_stats()
            namespaces = stats.namespaces

            documents = {}
            for namespace in namespaces:
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

    def store_document(self, doc_name, chunks, embeddings):
        """Almacena un documento en Pinecone"""
        try:
            namespace = f"{doc_name}_namespace"
            
            doc_metadata = {
                'document_id': doc_name,
                'title': doc_name,
                'upload_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'num_pages': len(chunks),
                'type': 'pdf'
            }
            
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
                    namespace=namespace
                )
            
            return True
        except Exception as e:
            st.error(f"Error almacenando documento: {e}")
            return False

    def delete_document(self, doc_id, namespace):
        """Elimina un documento de Pinecone"""
        try:
            self.index.delete(namespace=namespace, deleteAll=True)
            return True
        except Exception as e:
            st.error(f"Error eliminando documento: {e}")
            return False

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