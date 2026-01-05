from ia import IAPequena

ia = IAPequena("conocimiento.json")

print("🤖 IA lista. Escribe una pregunta (salir para terminar)\n")

while True:
    pregunta = input("Tú: ").strip()
    if pregunta.lower() == "salir":
        print("Adiós 👋")
        break

    respuesta = ia.responder(pregunta)
    print("IA:", respuesta)

    # Si la IA pide aprendizaje, preguntar si quiere enseñar
    if ia.esperando_aprendizaje:
        opcion = input("¿Quieres enseñarle algo? (s/n): ").lower()

        if opcion == "s":
            info = input("Enseñanza: ")
            tema = ia.esperando_aprendizaje
            ia.aprender_info(tema, info)
            ia.esperando_aprendizaje = None
            print(f"IA: ✅ He aprendido sobre {tema}")
        else:
            ia.esperando_aprendizaje = None
            print("IA: Está bien, no aprenderé eso.")
