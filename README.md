# Design Document : API REST CONTACTOS

## 1. Descripcion
Ejemplo de una API REST para gestionar contactos en una DB utilizando FastAPI.

## 2. Objetivo
Realizar un ejemplo de diseño de una API REST de tipo CRUD y su posterior codificacion utilizando el framework  [FastAPI](https://fastapi.tiangolo.com/).

## 3. Diseño de l BD
Para este ejemplo se utilizara el gestor de base de datos [SQLite3](https://www.sqlite.org) con las siguientes tablas:

## 3.1 Tabla: contactos
| contactos |
| --- |
| +id_contactos |
| nombres |
| primer_apellido |
| segundo_apellido |
| correo |
| telefono |

## 3.2 Tablas de la API
### GET http://localhost:8000/
| No | Propiedad | Detalle |
| --- | --- | --- |
| 1 | Description | Endpoint raíz de la API |
| 2 | Summary | Endpoint raíz |
| 3 | Method | GET |
| 4 | Endpoint | http://localhost/8000/ |
| 5 | Query Param | NA |
| 6 | Path Param | NA |
| 7 | Data | NA |
| 8 | Version | v1 |
| 9 | Status Code | 200 Ok |
| 10 | Response Type | application/json |
| 11 | Response | {"version":"v1","message":"Endpoint raíz","datetime":"21/9/23 10:16"} |
| 12 | curl | curl -X 'GET' 'http://localhost:8000/' -H 'accept:application/json' |
| 13 | Status Code (error) | NA |
| 14 | Response Type (error) | NA |
| 15 | Response (error) | NA |

### GET http://localhost:8000/contactos
| No | Propiedad           | Detalle                            |
|--- | ------------------- | ---------------------------------- |
| 1  | Description         | Obtener la lista de contactos      |
| 2  | Summary             | Obtener contactos                  |
| 3  | Method              | GET                                |
| 4  | Endpoint            | http://localhost/8000/contactos    |
| 5  | Query Param         | NA                                 |
| 6  | Path Param          | NA                                 |
| 7  | Data                | NA                                 |
| 8  | Version             | v1                                 |
| 9  | Status Code         | 200 Ok                             |
| 10 | Response Type       | application/json                   |
| 11 | Response            | {"version": "v1","message": "Lista de contactos","datetime": "27/9/23 14:30","data": [{"id_contacto": 1,"primer_apellido": "Ejemplo","segundo_apellido": "Apellido","correo": "dañlf@gasf.com","telefono": "123-456-7890"}]} |
| 12 | curl | curl -X 'GET' 'http://localhost:8000/contactos' -H 'accept: application/json' |
| 13 | Status Code (error) | NA |
| 14 | Response Type (error) | NA |
| 15 | Response (error) | NA |

### POST http://localhost:8000/contactos
| No | Propiedad           | Detalle                                     |
|--- | ------------------- | ------------------------------------------- |
| 1  | Description         | Crear un nuevo contacto                     |
| 2  | Summary             | Crear contacto                              |
| 3  | Method              | POST                                        |
| 4  | Endpoint            | http://localhost/8000/contactos             |
| 5  | Query Param         | NA                                          |
| 6  | Path Param          | NA                                          |
| 7  | Data                | Datos del nuevo contacto (application/json) |
| 8  | Version             | v1                                          |
| 9  | Status Code         | 201 Created                                |
| 10 | Response Type       | application/json                           |
| 11 | Response            | {"version": "v1","message": "Contacto creado exitosamente","datetime": "27/9/23 15:00","data": {"id_contacto": 3,"primer_apellido": "Nuevo","segundo_apellido": "Apellido","edad": 35,"telefono": "555-555-5555"}} |
| 12 | curl | curl -X 'POST' 'http://localhost:8000/contactos' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"primer_apellido": "Nuevo","segundo_apellido": "Apellido","correo": "nuevo@gmail.com","telefono": "555-555-5555"}' |
| 13 | Status Code (error) | NA |
| 14 | Response Type (error) | NA |
| 15 | Response (error) | NA |

### DELETE http://localhost:8000/contactos/?id_contactos
| No | Propiedad           | Detalle                                |
|--- | ------------------- | -------------------------------------- |
| 1  | Description         | Eliminar un contacto por ID           |
| 2  | Summary             | Eliminar contacto                      |
| 3  | Method              | DELETE                                 |
| 4  | Endpoint            | http://localhost/8000/contactos/?id_contactos |
| 5  | Query Param         | NA                                     |
| 6  | Path Param          | id_contactos (integer)                |
| 7  | Data                | NA                                     |
| 8  | Version             | v1                                     |
| 9  | Status Code         | 204 No Content                         |
| 10 | Response Type       | NA                                     |
| 11 | Response            | NA                                     |
| 12 | curl                | curl -X 'DELETE' 'http://localhost:8000/contactos/?id_contactos' -H 'accept: application/json' |
| 13 | Status Code (error) | 404 Not Found (Si el contacto no existe) |
| 14 | Response Type (error) | application/json |
| 15 | Response (error) | {"version": "v1","message": "El contacto con ID {id_contactos} no se encontró"} |

### PUT http://localhost:8000/contactos/?id_contactos
| No | Propiedad           | Detalle                                      |
|--- | ------------------- | -------------------------------------------- |
| 1  | Description         | Actualizar un contacto por ID               |
| 2  | Summary             | Actualizar contacto                          |
| 3  | Method              | PUT                                          |
| 4  | Endpoint            | http://localhost/8000/contactos/?id_contactos |
| 5  | Query Param         | NA                                           |
| 6  | Path Param          | id_contactos (integer)                      |
| 7  | Data                | Datos actualizados del contacto (application/json) |
| 8  | Version             | v1                                           |
| 9  | Status Code         | 200 OK                                       |
| 10 | Response Type       | application/json                             |
| 11 | Response            | {"version": "v1","message": "Contacto actualizado exitosamente","datetime": "27/9/23 16:00","data": {"id_contacto": {id_contactos},"primer_apellido": "Actualizado","segundo_apellido": "Apellido","edad": 40,"telefono": "555-555-5555"}} |
| 12 | curl | curl -X 'PUT' 'http://localhost:8000/contactos/?id_contactos' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"primer_apellido": "Actualizado","segundo_apellido": "Apellido","correo": "put@gmail.com","telefono": "555-555-5555"}' |
| 13 | Status Code (error) | 404 Not Found (Si el contacto no existe) |
| 14 | Response Type (error) | application/json |
| 15 | Response (error) |{"version": "v1","message": "El contacto con ID ?id_contactos no se encontró"} |
