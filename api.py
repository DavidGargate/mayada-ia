from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ia import IAPequena




app = FastAPI()

# CORS (permitir web / frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instancia única de la IA
ia = IAPequena("conocimiento.json", "conocimiento_dinamico.json")

# Modelo de entrada
class Pregunta(BaseModel):
    pregunta: str | None = None
    ensena: str | None = None

@app.post("/preguntar")
def preguntar(data: Pregunta):

    # 🔹 CASO 1: El usuario está enseñando algo
    if data.ensena:
        if not ia.esperando_aprendizaje:
            return {
                "respuesta": "⚠️ No te pedí aprender nada todavía."
            }

        tema = ia.esperando_aprendizaje
        ia.aprender_info(tema, data.ensena)
        ia.esperando_aprendizaje = None

        return {
            "respuesta": f"✅ He aprendido sobre: {tema}"
        }

    # 🔹 CASO 2: Pregunta normal
    if data.pregunta:
        respuesta = ia.responder(data.pregunta)
        return {"respuesta": respuesta}

    # 🔹 CASO 3: Entrada inválida
    return {
        "respuesta": "❌ No se recibió ninguna pregunta."
    }
