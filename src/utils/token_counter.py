import tiktoken

def count_tokens(text: str, model: str = "gpt-4") -> int:
    """
    Cuenta los tokens en un texto dado.
    
    Args:
        text: El texto para contar tokens
        model: El modelo a usar para el conteo (por defecto gpt-4)
        
    Returns:
        int: Número de tokens
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except Exception:
        try:
            # Fallback a cl100k_base si el modelo no está disponible
            encoding = tiktoken.get_encoding("cl100k_base")
            return len(encoding.encode(text))
        except Exception as e:
            print(f"Error contando tokens: {e}")
            return 0

def count_messages_tokens(messages: list, model: str = "gpt-4") -> int:
    """
    Cuenta los tokens en una lista de mensajes.
    
    Args:
        messages: Lista de diccionarios con los mensajes
        model: El modelo a usar para el conteo
        
    Returns:
        int: Número total de tokens
    """
    total_tokens = 0
    for message in messages:
        # Contar tokens del contenido
        total_tokens += count_tokens(message.get("content", ""), model)
        # Añadir tokens por el rol y formato (aproximación)
        total_tokens += 4  # ~4 tokens por mensaje para rol y formato
    
    return total_tokens