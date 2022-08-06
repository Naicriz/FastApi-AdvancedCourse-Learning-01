#Python
from typing import List, Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel, EmailStr
from pydantic import Field

#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path, Form, Header, Cookie, File, UploadFile

app = FastAPI()

    ## Models for the API endpoints (pydantic) ##

class HairColor(Enum): 
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Location(BaseModel): 
    city: str
    state: str
    country: str

    # Contiene todo el código que compartía previamente Person y PersonOut y éstas ahora heredarán de PersonBase.
class PersonBase(BaseModel):
    first_name: str = Field(
        ..., 
        min_length=1,
        max_length=50,
        example="Miguel" #example field for testing
        )
    last_name: str = Field(
        ..., 
        min_length=1,
        max_length=50,
        example="Torres"
        )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example=25
    )
    hair_color: Optional[HairColor] = Field(default=None, example=HairColor.black)
    is_married: Optional[bool] = Field(default=None, example=False)

class Person(PersonBase): # Password es lo único que no hereda de PersonBase.
    password: str = Field(..., min_length=8)

"""
class Config:  # example of config for pydantic to validate the model
    schema_extra = {
        "example": {
            "first_name": "Facundo",
            "last_name": "Garcia Martoni",
            "age": 21, 
            "hair_color": "blonde",
            "is_married": False
        }
    }
"""

    #Ejemplo 1 - Output Model Person
class PersonOut(PersonBase): # Solo hereda de PersonBase.
    pass

class LoginOut(BaseModel): # Solo retornará el username ###y el token?)
    username: str = Field(..., min_length=1, max_length=20, example="JhonDoe98")
    message: str = 'Succesfully Logged'

    ##Path Parameters are always required!##
    # Request and Response Body (FastAPI)

@app.get(
    path = "/",
    status_code = 200
    )
def home(): 
    return {"Hello": "World"}

"""
    # Ejemplo 2 - Output Model Person (This can be used as a quick shortcut if you have only one Pydantic model and want to remove some data from the output.)

@app.post("/person/new", response_model=Person, response_model_exclude={"password"})
def create_person(person: Person = Body(...)): 
    return person
"""

    # Ejemplo 1 - Output Model Person con el modelo de person pero en el path decorator se puede usar el modelo de personOut para el response.
        # response_model is the model that will be returned in the response body.
@app.post(
    path = "/person/new",
    response_model = PersonOut,
    status_code = 201 # status 201 significa que se creó un nuevo recurso
    )
def create_person(person: Person = Body(...)): 
    return person

    # Validaciones: Query Parameters (FastAPI)  [Query Parameters are always optional]

@app.get(
    path = "/person/detail",
    response_model = PersonOut,
    status_code = 200 # status code 200 significa que se obtuvo un recurso
    )
def show_person(
    name: Optional[str] = Query(
        None,
        min_length = 1, 
        max_length = 50,
        title = "Person Name",
        description = "This is the person name. It's between 1 and 50 characters.",
        example = "Marge"
        ),
    age: str = Query(
        ...,
        title = "Person Age",
        description = "This is the person age. It's required.",
        example = 25
        )
): 
    return {name: age}

    # Validaciones: Path Parameters (FastAPI)

@app.get(
    path = "/person/detail/{person_id}",
    response_model = PersonOut,
    status_code = 200
    )
def show_person(
    person_id: int = Path(
        ..., 
        gt = 0,
        example = 123
        )
): 
    return {person_id: "It exists!"}

    # Validaciones: Request Body (FastAPI)

@app.put(
    path = "/person/{person_id}",
    status_code = 202 # status code 202 significa que se actualizó un recurso
    )
def update_person(
    person_id: int = Path(
        ...,
        title = "Person ID",
        description = "This is the person ID. It's required.",
        gt = 0,
        example = 38472
    ),
    person: Person = Body(...),
    #location: Location = Body(...)
): 
    #results = person.dict()
    #results.update(location.dict())
    #return results
    return person

    # Forms

@app.post(
    path = "/login",
    response_model = LoginOut,
    status_code = 200
)
def login( #campos de formulario que vendrán del frontend.
    username: str = Form(...),
    password: str = Form(...)
    ):
    return LoginOut(username = username)

    # Parametros: Cookies and Headers (FastAPI)

@app.post(
    path = "/contact",
    status_code=200
)
def contact(
    first_name: str = Form(
        ...,
        max_length = 20,
        min_length = 3,
        example = "Miguel"
    ),
    last_name: str = Form(
        ...,
        max_length = 20,
        min_length = 3,
        example = "Torres"
    ),
    email: EmailStr = Form(
        ...,
        example = "example@example.cl"
    ),
    message: str = Form(
        ...,
        max_length=200,
        min_length=10
    ),
    # Header http que nos dice quien está intentando usar esta parte de la api (path operation)
    user_agent: Optional[str] = Header(default=None), # default=None significa que no se requiere el header
    ads: Optional[str] = Cookie(default=None)
):
    return user_agent

    # Parametros: Files (FastAPI)

@app.post(
    path = "/upload-image",
)
def post_image(
    image: UploadFile = File(...)
):
    return {
        "File Name": image.filename, # nombre del archivo
        "Content Type": image.content_type, # content_type es el tipo de archivo que se subió
        #"Size (kb)": round(len(image.file.read())/1024, ndigits = 2) # len(image.file.read()) es el tamaño en bytes y se divide por 1024 para obtener el tamaño en kilobytes.
        "Size (mb)": round(len(image.file.read())/(1024*1024), ndigits = 2) # len(image.file.read()) es el tamaño en bytes y se multiplica por 1024 para obtener el tamaño en megabytes.

    }

"""
@app.post(
    path = "/upload-images",
    status_code=200
)
def upload_images(
    images: List[UploadFile] = File(...)
):
    info_images = [{
        "File Name": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024, ndigits=2) # len(image.file.read()) es el tamaño en bytes y se divide por 1024 para obtener el tamaño en kilobytes.
    } for image in images]

    return info_images
"""