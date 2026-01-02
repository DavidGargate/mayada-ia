import json
import re

class IAPequena:
    def __init__(self, archivo_conocimiento):
        with open(archivo_conocimiento, "r", encoding="utf-8-sig") as f:
            self.conocimiento = json.load(f)

    def normalizar(self, texto):
        texto = texto.lower()

        reemplazos = {
            "2": "segunda",
            "ii": "segunda",
            "1": "primera",
            "i": "primera"
        }

        for k, v in reemplazos.items():
            texto = texto.replace(k, v)

        texto = re.sub(r"[^a-záéíóúñ\s]", "", texto)
        return texto

    def responder(self, pregunta):
        pregunta = self.normalizar(pregunta)

        for tema, datos in self.conocimiento.items():
            tema_normalizado = self.normalizar(tema)

            if all(palabra in pregunta for palabra in tema_normalizado.split()):

                if "cuando" in pregunta:
                    return f"La {tema} ocurrió entre {datos['inicio']} y {datos['fin']}."

                if "cuanto" in pregunta or "duro" in pregunta:
                    duracion = datos["fin"] - datos["inicio"]
                    return f"La {tema} duró aproximadamente {duracion} años."

                return datos["descripcion"]

        return "Todavía no tengo información sobre eso."
