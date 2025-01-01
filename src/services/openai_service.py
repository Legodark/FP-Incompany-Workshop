import streamlit as st
from openai import AzureOpenAI

class OpenAIService:
    def __init__(self, api_base, api_key, api_version="2023-05-15"):
        self.client = AzureOpenAI(
            azure_endpoint=api_base,
            api_key=api_key,
            api_version=api_version
        )

    def get_embedding(self, text, model=st.secrets["EMBED_MODEL"]):
        """Genera embeddings para un texto dado"""
        try:
            response = self.client.embeddings.create(
                input=[text],
                model=model
            )
            return response.data[0].embedding
        except Exception as e:
            st.error(f"Error generando embedding: {e}")
            return None

    def get_chat_completion(self, messages, model="gpt-4o", max_tokens=500):
        """Obtiene una respuesta del modelo de chat"""
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            st.error(f"Error generando respuesta: {e}")
            return None