import json
import re
import wikipedia

class IAPequena:
    def __init__(self, archivo_base, archivo_dinamico, idioma="es"):
        # todo tu código aquí

        self.archivo_base = archivo_base
        self.archivo_dinamico = archivo_dinamico
        wikipedia.set_lang(idioma)

        # Conocimiento base (solo lectura)
        try:
            with open(self.archivo_base, "r", encoding="utf-8-sig") as f:
                self.conocimiento_base = json.load(f)
        except:
            self.conocimiento_base = {}

        # Conocimiento dinámico (editable solo admin)
        try:
            with open(self.archivo_dinamico, "r", encoding="utf-8-sig") as f:
                self.conocimiento_dinamico = json.load(f)
        except:
            self.conocimiento_dinamico = {}

    # Guardar conocimiento dinámico
    def guardar_dinamico(self):
        with open(self.archivo_dinamico, "w", encoding="utf-8") as f:
            json.dump(self.conocimiento_dinamico, f, ensure_ascii=False, indent=2)

    # Normalizar texto
    def normalizar(self, texto):
        texto = texto.lower()
        reemplazos = {"2":"segunda","ii":"segunda","1":"primera","i":"primera"}
        for k,v in reemplazos.items():
            texto = texto.replace(k,v)
        texto = re.sub(r"[^a-záéíóúñ0-9\s\+\-\*/x]", "", texto)
        texto = re.sub(r"\s+", " ", texto)
        return texto.strip()

    # Extraer tema de la pregunta
    def extraer_tema(self, texto):
        texto = self.normalizar(texto)
        stopwords = ["que","qué","es","fue","cuando","cuanto","duró","la","el","los","las","un","una"]
        palabras = [p for p in texto.split() if p not in stopwords]
        return " ".join(palabras)

    # Aprender info segura (solo admin)
    def aprender_info_segura(self, tema, descripcion):
        clave = self.normalizar(tema)
        self.conocimiento_dinamico[clave] = {"descripcion": descripcion}
        self.guardar_dinamico()
        return f"✅ He aprendido sobre {tema}."

    # Responder
    def responder(self, pregunta):
        pregunta_norm = self.normalizar(pregunta)
        tema_pregunta = self.extraer_tema(pregunta)

        # 1️⃣ Buscar en base
        for tema, datos in self.conocimiento_base.items():
            if tema in tema_pregunta or tema_pregunta in tema:
                return datos.get("descripcion", "Tengo información, pero no una descripción clara.")

        # 2️⃣ Buscar en dinámico
        for tema, datos in self.conocimiento_dinamico.items():
            if tema in tema_pregunta or tema_pregunta in tema:
                return datos.get("descripcion", "Tengo información, pero no una descripción clara.")

        # 3️⃣ Saludos y cortesías
        if pregunta_norm in ["hola","buenas","buenos dias","buenas tardes","buenas noches"]:
            return "Hola 😊 ¿En qué puedo ayudarte?"
        if "gracias" in pregunta_norm:
            return "¡Con gusto! 😊"

        # 4️⃣ Mini fallback matemático
        if re.match(r"^\d+\s*(?:\+|\-|\*|x|/)\s*\d+$", pregunta_norm):
            try:
                expr = pregunta_norm.replace("x", "*")
                return str(eval(expr))
            except:
                pass

        # 5️⃣ Wikipedia fallback
        try:
            resumen = wikipedia.summary(pregunta, sentences=2, auto_suggest=True, redirect=True)
            return resumen
        except wikipedia.exceptions.DisambiguationError as e:
            return f"Hay varias opciones para '{pregunta}': {', '.join(e.options[:5])}..."
        except wikipedia.exceptions.PageError:
            return "No tengo información sobre esto. Solo un administrador puede enseñármelo."
        except Exception as e:
            return f"❌ Error consultando Wikipedia: {e}"
