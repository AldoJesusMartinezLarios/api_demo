"""
from fastapi import FastAPI, HTTPException, Request, status, Query
from pydantic import BaseModel
import csv

app = FastAPI()

@app.get("/", 
    status_code=status.HTTP_201_CREATED,
    description="Endpoint raiz de la Api Contactos",
    summary="Endpoint raiz")
async def root():
    """"""
    #Endpoint raiz
        ##Status code
        *201 created
    """"""
    return {"message": "Hello World"}

@app.get(
    "/v1/contactos", 
    status_code=status.HTTP_201_CREATED,
    description="Endpoint para listar contactos en la Api Contactos",
    summary="Endpoint para listar cotactos")
async def get_contactos():
    
    # Define la ruta de tu archivo CSV
    archivo_contactos = "contactos.csv"

    # Inicializa una lista para almacenar los datos de contacto
    contactos = []

    # Lee los datos del archivo CSV y los impríme
    with open(archivo_contactos, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            contactos.append(row)
            print(row)  # Imprime cada fila

    return {"contactos": contactos}

# Define el modelo Pydantic para los contactos
class Contacto(BaseModel):
    nombre: str
    email: str

# Nueva ruta y función para el método POST
@app.post(
    "/v1/contactos", 
    status_code=status.HTTP_201_CREATED,
    description="Endpoint para agregar un nuevo contacto",
    summary="Endpoint para agregar un nuevo contacto")

async def agregar_contacto(contacto: Contacto):
    nuevo_contacto = {
        "nombre": contacto.nombre,
        "email": contacto.email,
    }

    archivo_contactos = "contactos.csv"
    with open(archivo_contactos, mode='a', encoding='utf-8', newline='') as file:
        fieldnames = ["nombre", "email"]  # Agrega más campos si es necesario
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writerow(nuevo_contacto)

    return {"mensaje": "Contacto agregado correctamente"}

@app.get(
    "/v1/contactos/{search}",
    status_code=status.HTTP_200_OK,
    description="Endpoint para listar contactos por una palabra clave",
    summary="Endpoint para listar contactos por palabra clave"
)

async def get_contactos(search: str = Query(...)):
    archivo_contactos = "contactos.csv"
    contactos = []

    with open(archivo_contactos, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if search.lower() in row["nombre"].lower():
                contactos.append(row)

    return {"contactos": contactos}
"""
from fastapi import FastAPI, HTTPException, Request, status, Query
from pydantic import BaseModel
import csv

app = FastAPI()

@app.get("/", 
    status_code=status.HTTP_201_CREATED,
    description="Endpoint raiz de la Api Contactos",
    summary="Endpoint raiz")
async def root():
    """
    #Endpoint raiz
        ##Status code
        *201 created
    """
    return {"message": "Hello World"}

# Define el modelo Pydantic para los contactos
class Contacto(BaseModel):
    nombre: str
    email: str

# Nueva ruta y función para el método POST
@app.post(
    "/v1/contactos", 
    status_code=status.HTTP_201_CREATED,
    description="Endpoint para agregar un nuevo contacto",
    summary="Endpoint para agregar un nuevo contacto")

async def agregar_contacto(contacto: Contacto):
    nuevo_contacto = {
        "nombre": contacto.nombre,
        "email": contacto.email,
    }

    archivo_contactos = "contactos.csv"
    with open(archivo_contactos, mode='a', encoding='utf-8', newline='') as file:
        fieldnames = ["nombre", "email"]  # Agrega más campos si es necesario
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writerow(nuevo_contacto)

    return {"mensaje": "Contacto agregado correctamente"}

@app.get(
    "/v1/contactos",
    status_code=status.HTTP_200_OK,
    description="Endpoint para listar contactos por una palabra clave",
    summary="Endpoint para listar contactos por palabra clave"
)

async def get_contactos(search: str = Query(...)):
    archivo_contactos = "contactos.csv"
    contactos = []

    with open(archivo_contactos, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if search.lower() in row["nombre"].lower():
                contactos.append(row)

    return {"contactos": contactos}

