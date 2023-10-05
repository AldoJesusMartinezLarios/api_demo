import requests
import json

while True:
    # Obtén la lista de clases
    URI = "https://www.dnd5eapi.co/api/classes"
    response = requests.get(URI)
    response_json = json.loads(response.text)

    # Muestra la lista de clases y permite al usuario elegir una
    print("Lista de clases disponibles:")
    for index, resultado in enumerate(response_json['results']):
        print(f"{index + 1}. {resultado['name']}")

    while True:
        try:
            seleccion = int(input("Elige un personaje por su número (0 para salir): ")) - 1
            if seleccion == -1:
                exit()
            elif 0 <= seleccion < len(response_json['results']):
                break
            else:
                print("Selección inválida. Introduce un número válido.")
        except ValueError:
            print("Por favor, introduce un número válido.")

    # Obtiene la URL relativa de la clase seleccionada
    clase_seleccionada = response_json['results'][seleccion]
    clase_url = clase_seleccionada['url']

    # Construye la URL completa usando la URL base
    base_url = "https://www.dnd5eapi.co"
    full_url = base_url + clase_url

    # Realiza una solicitud para obtener información sobre la clase seleccionada
    response = requests.get(full_url)
    clase_data = json.loads(response.text)

    # Muestra las proficiencies de la clase seleccionada
    print(f"\nProficiencies de {clase_data['name']}:")
    for proficiency in clase_data['proficiencies']:
        print(proficiency['name'])
