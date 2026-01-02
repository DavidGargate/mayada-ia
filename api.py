from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ia import IAPequena

app = FastAPI()

# Permitir acceso desde la web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ia = IAPequena("conocimiento.json")

class Pregunta(BaseModel):
    pregunta: str

@app.post("/preguntar")
def preguntar(data: Pregunta):
    respuesta = ia.responder(data.pregunta)
    return {"respuesta": respuesta}


@app.get("/")
def root():
    return {"status": "ok"}
