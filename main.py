from fastapi import FastAPI
import csv

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/v1/contactos")
async def get_contactos():
    # Leer el archivo CSV
    contactos = []
    with open("contactos.csv", mode="r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            contactos.append(row)

    return contactos
