# Utilidades

Este directorio contiene utilidades y funciones auxiliares que se utilizan en toda la aplicación. Estas utilidades proporcionan funcionalidad común y reutilizable.

## Estructura

```
utils/
├── pdf_processing.py     # Utilidades para procesamiento de PDFs
├── session_state.py      # Gestión del estado de la sesión
└── README.md            # Este archivo
```

## Utilidades Disponibles

### PDF Processing

Este módulo proporciona funciones para el procesamiento de archivos PDF:

- Extracción de texto de PDFs
- División de texto en chunks manejables
- Limpieza y normalización de texto
- Manejo de diferentes formatos de PDF

### Session State

Este módulo maneja la inicialización y gestión del estado de la sesión:

- Inicialización de variables de estado
- Gestión de persistencia de datos
- Control de estados de la aplicación
- Manejo de estados temporales

## Uso

Para utilizar estas utilidades en tu código:

```python
from utils.pdf_processing import extract_text_from_pdf, split_text
from utils.session_state import init_session_state

# Inicializar estado
init_session_state()

# Procesar PDF
text = extract_text_from_pdf(pdf_file)
chunks = split_text(text)
```

## Funciones Auxiliares

Las utilidades están diseñadas para:

1. **Reutilización**: Funciones comunes que se utilizan en múltiples lugares
2. **Eficiencia**: Optimizadas para rendimiento
3. **Robustez**: Manejo de errores y casos extremos
4. **Mantenibilidad**: Código limpio y bien documentado

## Agregar Nuevas Utilidades

Para agregar una nueva utilidad:

1. Crea un nuevo archivo `nombre_util.py`
2. Implementa las funciones necesarias
3. Incluye documentación y tipos
4. Agrega tests si es apropiado
5. Actualiza este README con la nueva información

## Mejores Prácticas

- Todas las funciones deben tener docstrings
- Incluir manejo de errores apropiado
- Usar type hints para mejor comprensión
- Mantener las funciones pequeñas y enfocadas
- Evitar efectos secundarios no documentados
