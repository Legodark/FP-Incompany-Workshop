# Chatbot PDF con GPT-4o

Esta aplicación permite subir archivos PDF y hacer preguntas sobre su contenido utilizando el modelo GPT-4o de Azure OpenAI y Pinecone para la base de datos de vectores. El sistema procesa los documentos, almacena sus embeddings en Pinecone y proporciona respuestas contextuales basadas en el contenido del documento.

## Estructura del Proyecto

```
chatbot-streamlit
├── src
│   ├── app.py                  # Punto de entrada principal de la aplicación
│   ├── services/              # Servicios de integración con APIs externas
│   │   ├── pinecone_service.py # Servicio de Pinecone
│   │   └── openai_service.py   # Servicio de Azure OpenAI
│   ├── components/            # Componentes de la interfaz de usuario
│   │   ├── document_list.py    # Lista de documentos
│   │   └── chat_interface.py   # Interfaz del chat
│   ├── utils/                # Utilidades y funciones auxiliares
│   │   ├── pdf_processing.py   # Procesamiento de PDFs
│   │   └── session_state.py    # Gestión del estado
│   ├── .streamlit
│   │   └── secrets.toml        # Variables de entorno para la aplicación
├── requirements.txt           # Dependencias de Python necesarias
└── README.md                 # Documentación del proyecto
```

## Requisitos

- Python 3.11 o superior
- Azure OpenAI API Key y acceso al modelo GPT-4o
- Pinecone API Key y una cuenta activa
- Las dependencias especificadas en requirements.txt:
  - streamlit==1.41.1
  - openai==1.58.1
  - pinecone-client==5.0.1
  - PyPDF2==3.0.1
  - PyMuPDF==1.25.1
  - requests==2.32.3
  - tiktoken==0.8.0

## Instalación

1. Clona el repositorio:

   ```sh
   git clone <repository_url>
   cd chatbot-streamlit
   ```

2. Crea un entorno virtual e instala las dependencias:

   ```sh
   python -m venv venv
   source venv/bin/activate  # En Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Configura las variables de entorno en `src/.streamlit/secrets.toml`:

   ```toml
   AZURE_OPENAI_API_KEY = "your_azure_openai_api_key"
   AZURE_OPENAI_API_BASE = "your_azure_openai_api_base"
   PINECONE_API_KEY = "your_pinecone_api_key"
   PINECONE_ENVIRONMENT = "your_pinecone_environment"
   PINECONE_HOST = "your_pinecone_host"
   EMBED_MODEL = "your_vectorizer_model_name"
   ```

## Uso

Para ejecutar la aplicación localmente:

```sh
cd src
streamlit run app.py
```

La aplicación estará disponible en `http://localhost:8501` y ofrece las siguientes funcionalidades:

1. **Gestión de Documentos**:

   - Sube archivos PDF desde el panel lateral
   - Visualiza la lista de documentos disponibles
   - Elimina documentos cuando ya no son necesarios

2. **Interacción con el Chat**:

   - Selecciona un documento para iniciar una conversación
   - Realiza preguntas sobre el contenido del documento
   - Recibe respuestas contextuales basadas en el contenido

3. **Características Avanzadas**:
   - Procesamiento automático de PDFs
   - Búsqueda semántica en el contenido
   - Historial de conversación persistente
   - Interfaz intuitiva y responsive

## Desarrollo

El proyecto está estructurado en módulos independientes para facilitar el mantenimiento y la extensión:

- `services/`: Contiene la lógica de integración con APIs externas
- `components/`: Implementa los elementos de la interfaz de usuario
- `utils/`: Proporciona funciones auxiliares y utilidades comunes

Cada directorio contiene su propio README con documentación detallada sobre su funcionamiento y uso.

## Contribuciones

Las contribuciones son bienvenidas. Si deseas mejorar este proyecto:

1. Haz un fork del repositorio
2. Crea una rama para tu característica (`git checkout -b feature/nueva-caracteristica`)
3. Realiza tus cambios y haz commit (`git commit -am 'Añade nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

Por favor, asegúrate de que tu código sigue las convenciones de estilo del proyecto y está bien documentado.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
