# Componentes

Este directorio contiene los componentes de la interfaz de usuario de la aplicación. Cada componente es una unidad independiente que maneja una parte específica de la interfaz.

## Estructura

```
components/
├── document_list.py     # Componente de lista de documentos
├── chat_interface.py    # Componente de interfaz de chat
└── README.md           # Este archivo
```

## Componentes Disponibles

### DocumentList

Este componente maneja la visualización y gestión de documentos en el panel lateral. Sus características incluyen:

- Carga de nuevos documentos PDF
- Listado de documentos disponibles
- Gestión de selección de documentos
- Funcionalidad de eliminación de documentos
- Visualización de metadata de documentos

### ChatInterface

Este componente maneja la interfaz principal del chat. Sus características incluyen:

- Visualización del historial de mensajes
- Entrada de mensajes del usuario
- Visualización de respuestas del asistente
- Indicadores de estado (typing, loading, etc.)
- Gestión del contexto de la conversación

## Uso

Para utilizar estos componentes en tu código:

```python
from components.document_list import render_document_list
from components.chat_interface import render_chat_interface

# Renderizar lista de documentos
render_document_list(documents, pinecone_service)

# Renderizar interfaz de chat
render_chat_interface(
    documents,
    pinecone_service,
    openai_service
)
```

## Diseño de Componentes

Los componentes siguen estos principios de diseño:

1. **Independencia**: Cada componente funciona de manera independiente
2. **Reutilización**: Los componentes son reutilizables en diferentes contextos
3. **Responsabilidad única**: Cada componente tiene una única responsabilidad bien definida
4. **Estado gestionado**: Utilizan st.session_state para gestión de estado
5. **Diseño consistente**: Mantienen una apariencia y comportamiento coherentes

## Creación de Nuevos Componentes

Para crear un nuevo componente:

1. Crea un nuevo archivo `nombre_componente.py`
2. Define las funciones de renderizado necesarias
3. Implementa la lógica del componente
4. Asegúrate de manejar correctamente el estado
5. Documenta el uso y las propiedades del componente
6. Actualiza este README con la nueva información

## Consideraciones de UI/UX

- Los componentes utilizan el sistema de grid de Streamlit
- Implementan feedback visual para todas las acciones
- Manejan estados de carga y error apropiadamente
- Son responsivos y se adaptan a diferentes tamaños de pantalla
- Siguen las mejores prácticas de accesibilidad
