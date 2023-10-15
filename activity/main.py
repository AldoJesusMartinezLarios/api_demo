from fastapi import FastAPI, HTTPException, Request, status, Query, Path, Body, File, UploadFile
from pydantic import BaseModel, Field
import csv
import os
from starlette.staticfiles import StaticFiles
from PIL import Image
from io import BytesIO
import openai

app = FastAPI()

# Define el modelo Pydantic para los contactos
class Contacto(BaseModel):
    id_contacto: int 
    nombre: str
    primer_apellido: str
    segundo_apellido: str
    email: str
    telefono: str

# Define el modelo Pydantic para el texto para la API de OpenAI
class Model(BaseModel):
    text: str = Field(min_lenght=10,max_length=200)

# Endpoint GET que devuelve en formato JSON la lista de todos los contactos almacenados en contactos.csv
@app.get(
    "/v1/contactos",
    summary="Obtener todos los contactos"
)
async def get_contactos():
    """
    # Obtener todos los contactos
    ### Devuelve una lista de todos los contactos almacenados en contactos.csv
    - **Status code 200**: OK si tiene éxito
    - **Status code 404**: Not Found si no se encuentran contactos
    """
    with open('contactos.csv', mode='r',newline='') as file:
        reader = csv.DictReader(file)
        contactos = list(reader)
    if not contactos:
        raise HTTPException(status_code=404, detail="No se encontraron contactos.")
    return contactos


# Endpoint POST que permite insertar un nuevo registro en contactos.csv
@app.post(
    "/v1/contactos",
    summary = "Agregar un nuevo contacto"
)
async def add_contacto(contacto:Contacto):
    """
    # Agregar un nuevo contacto
    ### Permite insertar un nuevo registro en contactos.csv
    - **Status code 201 Created**: si tiene éxito
    - **Status code 400 Bad Request**: si los datos proporcionados son incorrectos
    - **Status code 500 Internal Server Error**: Si ocurre un error inesperado en el servidor
    """

    try:
        # Validar los datos del contacto
        if not contacto.nombre or not contacto.email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Existen datos obligatorios que no han sido agregados")

        with open('contactos.csv', mode='a', newline='') as file:
            fieldnames = ['id_contacto', 'nombre', 'primer_apellido', 'segundo_apellido', 'email', 'telefono']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow(contacto.dict())
        return contacto

    except Exception as e:
        # Manejo de errores
        raise HTTPException(status_code=500, detail="Error interno del servidor")


# Endpoint PUT que permite actualizar los datos de un contacto buscandolo por el id_contacto
@app.put(
    "/v1/contactos/{id_contacto}", 
    summary="Actualizar un contacto"
)
async def update_contacto(
    id_contacto: int = Path(..., description="ID del contacto a actualizar"),
    contacto: Contacto = Body(..., description="Nuevos datos del contacto")
):
    """
    # Actualizar un contacto por ID.

    ### Permite actualizar los datos de un contacto buscándolo por el id_contacto.

    - **Status Code 200 OK**: Si la operación tiene éxito.
    - **Status Code 400 Bad Request**: Si los datos proporcionados son incorrectos.
    - **Status Code 404 Not Found**: Si no se encuentra el contacto.
    """

    try:
        # Validar los datos del contacto
        if not contacto.nombre or not contacto.email:
            raise HTTPException(status_code=400, detail="Los datos proporcionados son incorrectos.")

        contactos = []
        with open('contactos.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            found = False
            for row in reader:
                if int(row['id_contacto']) == id_contacto:
                    contactos.append(contacto.dict())
                    found = True
                else:
                    contactos.append(row)

        if not found:
            raise HTTPException(status_code=404, detail="El contacto no se encontró.")

        with open('contactos.csv', mode='w', newline='') as file:
            fieldnames = ['id_contacto', 'nombre', 'primer_apellido', 'segundo_apellido', 'email', 'telefono']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(contactos)

        # Devuelve el contacto actualizado.
        return contacto
    except Exception as e:
        # Manejo de errores
        raise HTTPException(status_code=500, detail="Error interno del servidor")


# Endpoint DELETE que permite borrar un contacto por el id_contacto
@app.delete(
    "/v1/contactos/{id_contacto}", 
    summary="Eliminar un contacto"
    )
async def delete_contacto(id_contacto: int = Path(..., description="ID del contacto a eliminar")):
    """
    # Eliminar un contacto por ID.

    ### Permite borrar un contacto de contactos.csv por el id_contacto.

    - **Status Code 204 No Content**: Si la operación tiene éxito y no se devuelve contenido.
    - **Status Code 404 Not Found**: Si no se encuentra el contacto.
    """

    try:
        contactos = []
        found = False

        with open('contactos.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if int(row['id_contacto']) != id_contacto:
                    contactos.append(row)
                else:
                    found = True

        if not found:
            raise HTTPException(status_code=404, detail="El contacto no se encontró.")

        with open('contactos.csv', mode='w', newline='') as file:
            fieldnames = ['id_contacto', 'nombre', 'primer_apellido', 'segundo_apellido', 'email', 'telefono']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(contactos)

        # Devuelve una respuesta con un mensaje de éxito.
        return {"message": "Contacto eliminado con éxito"}

    except Exception as e:
        # Manejo de errores
        raise HTTPException(status_code=500, detail="Error interno del servidor")


# Endpoint GET que permite buscar contactos que contengan el nombre buscado.
@app.get(
    "/v1/contactos/search", 
    summary="Buscar contactos por nombre"
    )
async def search_contactos(nombre: str = Query(..., description="Nombre a buscar")):
    """
    # Buscar contactos por nombre
    ### Permite buscar contactos que contengan el nombre buscado.
    - **Status code 200 OK**: si tiene éxito.
    - **Status code 404 Not Found**: si no se encuentran contactos.
    """
    contactos = []
    with open('contactos.csv', mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if nombre.lower() in row['nombre'].lower():
                contactos.append(row)

    if not contactos:
        raise HTTPException(status_code=404, detail="No se encontraron contactos con el nombre especificado.")

    return contactos



app.mount("/static", StaticFiles(directory="static"), name="static")

# Ruta para cargar una imagen y aplicar recorte (crop)
@app.post(
    "/v1/imagenes/crop", 
    summary="Aplicar recorte a una imagen"
    )
async def crop_image(
    file: UploadFile,
    crop: str = Query(..., description="Coordenadas de recorte (x1, y1, x2, y2) en formato 'x1,y1,x2,y2'"),
):
    """
    # Cargar y aplicar recorte a una imagen
    ### Permite cargar una imagen, aplicar un recorte y guardarla en el sistema.
    - **Status code 200 OK**: si la imagen se carga y el recorte se aplica con éxito.
    - **Status code 400 Bad Request**: si el archivo no es una imagen o las coordenadas de recorte son incorrectas.
    """
    if not file.content_type.startswith("image"):
        raise HTTPException(status_code=400, detail="Solo se permiten imágenes en este formulario.")

    # Leer y procesar la imagen
    img = Image.open(BytesIO(file.file.read()))

    # Parsear las coordenadas de recorte
    try:
        x1, y1, x2, y2 = map(int, crop.split(","))
        img = img.crop((x1, y1, x2, y2))
    except (ValueError, IndexError):
        raise HTTPException(status_code=400, detail="Coordenadas de recorte incorrectas. Deben estar en formato 'x1,y1,x2,y2'.")

    # Define la ruta y el nombre de archivo para guardar la imagen con recorte
    save_path = f"static/images/{file.filename}"

    # Guardar la imagen con recorte en el sistema
    img.save(save_path)

    return {"message": "Imagen cargada y recorte aplicado con éxito", "file_path": save_path}

# Ruta para cargar una imagen y aplicar un efecto flip horizontal (fliph)
@app.post(
    "/v1/imagenes/fliph", 
    summary="Aplicar flip horizontal a una imagen"
    )
async def flip_horizontal_image(file: UploadFile):
    """
    # Cargar y aplicar flip horizontal a una imagen
    ### Permite cargar una imagen y aplicar un efecto flip horizontal (espejo) para invertir la imagen horizontalmente.
    - **Status code 200 OK**: si la imagen se carga y el flip horizontal se aplica con éxito.
    - **Status code 400 Bad Request**: si el archivo no es una imagen.
    """
    if not file.content_type.startswith("image"):
        raise HTTPException(status_code=400, detail="Solo se permiten imágenes en este formulario.")

    # Leer y procesar la imagen
    img = Image.open(BytesIO(file.file.read()))

    # Aplicar el flip horizontal
    img = img.transpose(Image.FLIP_LEFT_RIGHT)

    # Define la ruta y el nombre de archivo para guardar la imagen con flip horizontal
    save_path = f"static/images/{file.filename}"

    # Guardar la imagen con flip horizontal en el sistema
    img.save(save_path)

    return {"message": "Imagen cargada y flip horizontal aplicado con éxito", "file_path": save_path}

# Ruta para cargar una imagen y aplicar efecto de colorización (colorize)
@app.post(
    "/v1/imagenes/colorize",
    summary="Aplicar colorización a una imagen"
    )
async def colorize_image(file: UploadFile):
    """
    # Cargar y aplicar colorización a una imagen
    ### Permite cargar una imagen y aplicar un efecto de colorización a la imagen.
    - **Status code 200 OK**: si la imagen se carga y la colorización se aplica con éxito.
    - **Status code 400 Bad Request**: si el archivo no es una imagen.
    """
    if not file.content_type.startswith("image"):
        raise HTTPException(status_code=400, detail="Solo se permiten imágenes en este formulario.")

    # Leer y procesar la imagen
    img = Image.open(BytesIO(file.file.read()))

    # Aplicar la colorización (puedes personalizar esta función)
    # Por ejemplo, convertir la imagen a escala de grises
    img = img.convert("L")

    # Define la ruta y el nombre de archivo para guardar la imagen con colorización
    save_path = f"static/images/{file.filename}"

    # Guardar la imagen con colorización en el sistema
    img.save(save_path)

    return {"message": "Imagen cargada y colorización aplicada con éxito", "file_path": save_path}



openai.api_key = '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'

@app.post(
    '/v1/chat_gpt', 
    summary="Generar respuesta"
    )
def generate_response(prompt: Model):
    """
    # Generar una respuesta de chat.

    ### Permite generar una respuesta de chat en función de un prompt proporcionado.

    - **Status Code 200 OK**: Si la respuesta se genera con éxito.
    - **Status Code 400 Bad Request**: Si la solicitud es incorrecta o el texto del prompt es demasiado largo.
    """

    try:
        engine_model_gpt3 = "text-davinci-003"

        if len(prompt.text) > 1024:
            raise HTTPException(status_code=400, detail="El texto del prompt es demasiado largo.")

        response = openai.Completion.create(
            engine=engine_model_gpt3,
            prompt=prompt.text,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.3
        )

        return response.choices[0].text
    except Exception as e:
        # Manejo de errores
        raise HTTPException(status_code=500, detail="Error interno del servidor")