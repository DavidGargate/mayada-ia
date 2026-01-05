import json
import re

class IAPequena:
    def __init__(self, archivo_conocimiento):
        self.archivo = archivo_conocimiento
        try:
            with open(self.archivo, "r", encoding="utf-8-sig") as f:
                self.conocimiento = json.load(f)
        except:
            self.conocimiento = {}

        self.ultimo_tema = None
        self.esperando_aprendizaje = None

    # -------------------------
    # Normalizar texto
    # -------------------------
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
        texto = re.sub(r"\s+", " ", texto)
        return texto.strip()

    # -------------------------
    # Guardar conocimiento
    # -------------------------
    def guardar(self):
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(self.conocimiento, f, ensure_ascii=False, indent=2)

    # -------------------------
    # Extraer tema de una frase
    # -------------------------
    def extraer_tema(self, texto):
        texto = self.normalizar(texto)
        stopwords = [
            "que", "qué", "es", "fue", "cuando", "cuanto",
            "duró", "la", "el", "los", "las", "un", "una"
        ]
        palabras = [p for p in texto.split() if p not in stopwords]
        return " ".join(palabras)

    # -------------------------
    # Aprender información libre
    # -------------------------
    def aprender_info(self, tema, descripcion):
        clave = self.normalizar(tema)
        self.conocimiento[clave] = {
            "descripcion": descripcion
        }
        self.guardar()
        return f"✅ He aprendido sobre {tema}."

    # -------------------------
    # Aprender desde frase con fechas
    # -------------------------
    def aprender_desde_frase(self, texto):
        patron = r"(.+) empezó en (\d{4}) y terminó en (\d{4})"
        m = re.search(patron, texto)
        if m:
            tema = self.normalizar(m.group(1))
            self.conocimiento[tema] = {
                "inicio": int(m.group(2)),
                "fin": int(m.group(3)),
                "descripcion": f"{tema.capitalize()} fue un evento importante."
            }
            self.guardar()
            return f"Perfecto. He aprendido sobre {tema}."
        return None

    # -------------------------
    # Responder preguntas
    # -------------------------
    def responder(self, pregunta):
        original = pregunta
        pregunta = self.normalizar(pregunta)

        # Saludos
        if pregunta in ["hola", "buenas", "buenos dias", "buenas tardes", "buenas noches"]:
            return "Hola 😊 ¿En qué puedo ayudarte?"
        if "gracias" in pregunta:
            return "¡Con gusto! 😊"

        # Aprendizaje automático
        aprendido = self.aprender_desde_frase(original)
        if aprendido:
            return aprendido

        # Buscar tema
        tema_pregunta = self.extraer_tema(pregunta)

        for tema, datos in self.conocimiento.items():
            if tema in tema_pregunta or tema_pregunta in tema:
                self.ultimo_tema = tema

                if "cuando" in pregunta and "inicio" in datos:
                    return f"{tema.capitalize()} ocurrió entre {datos['inicio']} y {datos['fin']}."

                if ("cuanto" in pregunta or "duró" in pregunta) and "inicio" in datos:
                    return f"{tema.capitalize()} duró {datos['fin'] - datos['inicio']} años."

                return datos.get("descripcion", "Tengo información, pero no una descripción clara.")

        # Contexto
        if self.ultimo_tema:
            datos = self.conocimiento.get(self.ultimo_tema, {})
            if "cuando" in pregunta and "inicio" in datos:
                return f"Ocurrió entre {datos['inicio']} y {datos['fin']}."

        # No sabe
        self.esperando_aprendizaje = tema_pregunta
        return "No tengo esa información. ¿Quieres enseñármela?"
