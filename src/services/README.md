# Servicios

Este directorio contiene los servicios que manejan la integración con APIs externas y proporcionan funcionalidad core para la aplicación.

## Estructura

```
services/
├── pinecone_service.py    # Servicio de integración con Pinecone
├── openai_service.py      # Servicio de integración con Azure OpenAI
└── README.md             # Este archivo
```

## Servicios Disponibles

### PineconeService

El servicio de Pinecone maneja todas las operaciones relacionadas con el almacenamiento y recuperación de embeddings de documentos. Sus principales responsabilidades incluyen:

- Creación y gestión de índices de Pinecone
- Almacenamiento de vectores de documentos
- Búsqueda semántica en documentos almacenados
- Gestión de namespaces para diferentes documentos
- Operaciones CRUD para documentos

### OpenAIService

El servicio de OpenAI maneja todas las interacciones con la API de Azure OpenAI. Sus principales responsabilidades incluyen:

- Generación de embeddings para texto
- Procesamiento de conversaciones con el modelo de chat
- Gestión de tokens y límites de la API
- Manejo de errores y reintentos

## Uso

Para utilizar estos servicios en tu código:

```python
from services.pinecone_service import PineconeService
from services.openai_service import OpenAIService

# Inicializar servicios
pinecone_service = PineconeService(api_key="tu-api-key")
openai_service = OpenAIService(
    api_base="tu-endpoint",
    api_key="tu-api-key"
)

# Ejemplo de uso
embedding = openai_service.get_embedding("texto de ejemplo")
pinecone_service.store_document("documento.pdf", chunks, embeddings)
```

## Consideraciones

- Los servicios están diseñados para ser thread-safe y manejar errores de forma robusta
- Incluyen reintentos automáticos para operaciones que pueden fallar
- Implementan logging para facilitar el debugging
- Manejan la gestión de recursos de forma eficiente

## Extensión

Para agregar un nuevo servicio:

1. Crea un nuevo archivo `nombre_service.py`
2. Implementa la clase del servicio siguiendo el patrón existente
3. Incluye manejo de errores y logging apropiado
4. Documenta las funcionalidades del servicio
5. Actualiza este README con la nueva información
