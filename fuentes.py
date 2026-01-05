import wikipedia

# Configurar idioma español
wikipedia.set_lang("es")

def buscar_wikipedia(consulta: str) -> str:
    """
    Busca información en Wikipedia.
    Devuelve un resumen de 1-2 frases o un mensaje de error si no encuentra nada.
    """
    try:
        resumen = wikipedia.summary(consulta, sentences=2)
        return resumen
    except wikipedia.exceptions.DisambiguationError as e:
        opciones = ", ".join(e.options[:5])
        return f"Hay varias opciones sobre eso: {opciones}"
    except wikipedia.exceptions.PageError:
        return "No encontré información sobre eso en Wikipedia."
    except Exception as e:
        return f"Error al buscar en Wikipedia: {str(e)}"
