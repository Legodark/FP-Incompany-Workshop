"""
Utilidad de Extracción y Procesamiento de PDF

Este módulo proporciona funciones para:
1. Extraer texto de archivos PDF
2. Guardar archivos subidos
3. Procesar archivos PDF
4. Dividir textos largos en fragmentos manejables

Dependencias:
- PyMuPDF (fitz): Para extracción de texto de PDF
- tiktoken: Para dividir texto basado en tokens
- os: Para operaciones de rutas y directorios
"""

import os
import fitz  # Biblioteca PyMuPDF para procesamiento de PDFs
import tiktoken  # Biblioteca de tokenización de OpenAI

def extract_text_from_pdf(archivo_subido):
    """
    Extrae el contenido de texto de un archivo PDF.

    Args:
        archivo_subido (objeto similar a archivo): El archivo PDF del que se extraerá texto.
    
    Returns:
        str: Texto concatenado de todas las páginas del PDF.

    Notas:
    - Utiliza PyMuPDF (fitz) para leer archivos PDF
    - Soporta lectura directa desde objetos de archivo
    - Extrae texto de cada página y lo concatena
    """
    # Inicializar una cadena vacía para almacenar el texto extraído
    texto_pdf = ""
    
    # Abrir el archivo PDF desde el flujo del archivo subido
    # filetype="pdf" ayuda a fitz a identificar el tipo de archivo
    with fitz.open(stream=archivo_subido.read(), filetype="pdf") as doc:
        # Iterar por cada página del PDF
        for pagina in doc:
            # Extraer texto de la página actual y agregarlo a texto_pdf
            texto_pdf += pagina.get_text()
    
    return texto_pdf

def save_uploaded_file(archivo_subido):
    """
    Guarda el archivo subido en un directorio especificado.

    Args:
        archivo_subido (objeto similar a archivo): El archivo a guardar.
    
    Returns:
        str: Ruta completa del archivo guardado.

    Notas:
    - Crea un directorio 'uploads' si no existe
    - Guarda el archivo con su nombre original
    """
    # Asegurar que el directorio de uploads exista
    os.makedirs("uploads", exist_ok=True)
    
    # Construir la ruta completa del archivo
    ruta_archivo = os.path.join("uploads", archivo_subido.name)
    
    # Escribir el contenido del archivo en la ruta especificada
    with open(ruta_archivo, "wb") as archivo:
        archivo.write(archivo_subido.getbuffer())
    
    return ruta_archivo

def process_pdf(archivo_subido):
    """
    Función integral de procesamiento de PDF que:
    1. Guarda el archivo PDF subido
    2. Extrae texto del PDF guardado

    Args:
        archivo_subido (objeto similar a archivo): El archivo PDF a procesar.
    
    Returns:
        str: Contenido de texto extraído del PDF.
    """
    # Guardar el archivo subido y obtener su ruta
    ruta_archivo = save_uploaded_file(archivo_subido)
    
    # Extraer texto del PDF guardado
    texto = extract_text_from_pdf(archivo_subido)
    
    return texto

def split_text(texto, max_tokens=8191):
    """
    Divide un texto largo en fragmentos más pequeños basándose en el conteo de tokens.

    Args:
        texto (str): El texto de entrada a dividir.
        max_tokens (int, opcional): Número máximo de tokens por fragmento. 
                                    Por defecto 8191 (adecuado para muchas API de LLM).
    
    Returns:
        list: Una lista de fragmentos de texto, cada uno dentro del límite de tokens.

    Notas:
    - Utiliza tiktoken de OpenAI para contar tokens con precisión
    - Límite de tokens por defecto establecido en 8191, compatible con muchas API de LLM
    - Útil para procesar textos largos que exceden las limitaciones de ventana de contexto
    """
    # Obtener el tokenizador base usado por muchos modelos de OpenAI
    codificacion = tiktoken.get_encoding("cl100k_base")
    
    # Codificar todo el texto en tokens
    tokens = codificacion.encode(texto)
    
    # Dividir tokens en fragmentos del tamaño máximo de tokens
    fragmentos = [tokens[i:i + max_tokens] for i in range(0, len(tokens), max_tokens)]
    
    # Decodificar cada fragmento de vuelta a texto
    return [codificacion.decode(fragmento) for fragmento in fragmentos]

# Ejemplo de uso
if __name__ == "__main__":
    # Esta sección demuestra cómo usar las funciones
    # Nota: En una aplicación real, normalmente obtendría el archivo_subido de un formulario web o entrada de archivo
    
    # Uso simulado (comentado)
    # archivo_subido = ...  # Su mecanismo de carga de archivos
    # texto_procesado = process_pdf(archivo_subido)
    # fragmentos_texto = split_text(texto_procesado)
    pass