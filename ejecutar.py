from ia import IAPequena

ia = IAPequena("conocimiento.json")

print("IA lista. Escribe una pregunta (salir para terminar)")

while True:
    pregunta = input("Tú: ")
    if pregunta.lower() == "salir":
        break

    respuesta = ia.responder(pregunta)
    print("IA:", respuesta)
