# Importar la clase FastAPI del módulo fastapi
from fastapi import FastAPI, status

# Importar el módulo csv para trabajar con archivos CSV
import csv

# Crear una instancia de FastAPI
app = FastAPI()

# Definir un manejador de ruta para la raíz ("/"). Esto responderá a las solicitudes HTTP GET en la ruta raíz.
@app.get(
    "/", 
    status_code=status.HTTP_200_OK,
    summary="Endpoint raìz"
    )
    
async def root():
    """
    # Endpoint raiz
    ## 1 - Status code
    * 289 -
    * 301 -
    """
    # Devolver un diccionario JSON como respuesta con un mensaje
    return {"message": "Hello World"}

# Definir un manejador de ruta para la ruta "/v1/contactos". Esto responderá a las solicitudes HTTP GET en esa ruta.
@app.get("/v1/contactos")
async def get_contactos():
    # Crear una lista llamada "contactos" para almacenar los datos del archivo CSV
    contactos = []

    # Abrir el archivo CSV llamado "contactos.csv" en modo lectura (mode="r") y UTF-8 (encoding="utf-8")
    with open("contactos.csv", mode="r", encoding="utf-8") as file:
        # Crear un lector CSV que trate el archivo como un diccionario (cada fila es un diccionario)
        csv_reader = csv.DictReader(file)

        # Iterar sobre las filas del archivo CSV
        for row in csv_reader:
            # Agregar cada fila (diccionario) a la lista de "contactos"
            contactos.append(row)

    # Devolver la lista de "contactos" como respuesta. FastAPI automáticamente convertirá esto a JSON.
    return contactos
