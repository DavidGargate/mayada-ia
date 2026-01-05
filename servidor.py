from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ia import IAPequenaPro
from config import ADMIN_KEY  # solo ADMIN_KEY

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instancia IA usando Wikipedia
ia = IAPequenaPro(
    archivo_base="conocimiento.json",
    archivo_dinamico="conocimiento_dinamico.json",
    idioma="es"
)

class Pregunta(BaseModel):
    pregunta: str | None = None
    ensena: str | None = None

@app.post("/preguntar")
def preguntar(data: Pregunta):
    if not data.pregunta:
        return {"respuesta": "❌ No se recibió ninguna pregunta."}
    respuesta = ia.responder(data.pregunta)
    return {"respuesta": respuesta}

@app.post("/aprender")
def aprender(data: Pregunta, api_key: str = Query(...)):
    if api_key != ADMIN_KEY:
        return {"error": "No autorizado"}
    if not data.pregunta or not data.ensena:
        return {"error": "Faltan datos"}
    respuesta = ia.aprender_info_segura(data.pregunta, data.ensena)
    return {"respuesta": respuesta}
