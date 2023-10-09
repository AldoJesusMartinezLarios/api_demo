import os
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/images/")
async def upload_images(files: list[UploadFile]):
    for file in files:
        if file.content_type.startswith("image"):
            file_location = f"static/images/{file.filename}"
            with open(file_location, "wb") as file_object:
                file_object.write(file.file.read())
        else:
            return {"error": "Solo se permiten imágenes en este formulario."}
    
    return {"message": "Imágenes cargadas con éxito"}

@app.post("/pdfs/")
async def upload_pdfs(files: list[UploadFile]):
    for file in files:
        if file.content_type == "application/pdf":
            file_location = f"static/pdf/{file.filename}"
            with open(file_location, "wb") as file_object:
                file_object.write(file.file.read())
        else:
            return {"error": "Solo se permiten archivos PDF en este formulario."}
    
    return {"message": "Archivos PDF cargados con éxito"}

@app.get("/archivos/")
async def list_files():
    image_files = os.listdir("static/images")
    pdf_files = os.listdir("static/pdf")
    return {"message": "Archivos disponibles", "images": image_files, "pdfs": pdf_files}

    
@app.get("/")
async def main():
    content = """
<!DOCTYPE html>
<html>
<head>
    <title>Subir Archivos</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <h1 class="mb-4">Cargar Imágenes</h1>
        <form action="/subir-imagenes/" enctype="multipart/form-data" method="post">
            <div class="form-group">
                <input name="files" type="file" accept="image/*" multiple class="form-control-file">
            </div>
            <button type="submit" class="btn btn-primary">Cargar Imágenes</button>
        </form>
    </div>
    <div class="container mt-5">
        <h1 class="mb-4">Cargar Archivos PDF</h1>
        <form action="/subir-pdf/" enctype="multipart/form-data" method="post">
            <div class="form-group">
                <input name="files" type="file" accept=".pdf" multiple class="form-control-file">
            </div>
            <button type="submit" class="btn btn-primary">Cargar Archivos PDF</button>
        </form>
    </div>
</body>
</html>
    """
    return HTMLResponse(content=content)
