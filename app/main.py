#Python
from typing import List, Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel, EmailStr
from pydantic import Field

#FastAPI
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Body, Query, Path, Form, Header, Cookie, File, UploadFile

app = FastAPI()


    # ------------------------- #
    ## Models for the API endpoints (pydantic) ##
    # ------------------------- #

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
    # --------------------------------- #
    # Request and Response Body (FastAPI)
    # --------------------------------- #

@app.get(
    path = "/",
    status_code = 200,
    tags = ["Home"],
    summary = "Home Page"
    )
def home():
    """
    ## Home page ##

    Index page of the API.

    Returns:
        Returns a dictionary with the key "Hello" and the value "World"
    """
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
    status_code = 201, # status 201 significa que se creó un nuevo recurso
    tags = ["Persons"], # tags are used to group endpoints in the documentation.
    summary = "Creates a new person in the system"
    )
def create_person(
    person: Person = Body(...)
    ):
    """
        ## Create new Person ##
        
        This endpoint*(path operation)* will create a new person based on the data in the body of the request
        and so, it creates a new person in the application and saves the information in the database.
        
        Parameters:
        - Request body parameters:
            - **person: Person** => A *person model* that contains *first_name*, *last_name*, *age*, *hair_color* *is_married* and *password*

        Returns:
        - A newly created person withouth the password.
        - **person: PersonOut** => A *person model* that contains *first_name*, *last_name*, *age*, *hair_color* and *is_married*
    """
    return person


    # --------------------------------- #
    # Validaciones: Query Parameters (FastAPI)  [Query Parameters are always optional]
    # --------------------------------- #

@app.get(
    path = "/person/detail",
    response_model = PersonOut,
    status_code = 200, # status code 200 significa que se obtuvo un recurso
    tags = ["Persons"]
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


    # --------------------------------- #
    # Validaciones: Path Parameters (FastAPI)
    # --------------------------------- #

persons = [1, 2, 3, 4, 5] # Lista de personas

@app.get(
    path = "/person/detail/{person_id}",
    response_model = PersonOut,
    status_code = 200,
    tags = ["Persons"],
    summary = "Shows a person detail"
    )
def show_person(
    person_id: int = Path(
        ..., 
        gt = 0,
        example = 123
        )
):  # Si se ingresa un id que no existe, retornará una http exception con status code 404 (Not Found) y el mensaje de error.
    if person_id not in persons:
        raise HTTPException(status_code=404, detail="Person not found... :[") # raise es una función que lanza una excepción.
    return {person_id: "It exists!"}


    # --------------------------------- #
    # Validaciones: Request Body (FastAPI)
    # --------------------------------- #

@app.put(
    path = "/person/{person_id}",
    response_model=PersonOut,
    status_code = 202, # status code 202 significa que se actualizó un recurso
    tags = ["Persons"],
    summary="Updates a person in the system"
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


    # --------------------------------- #
    #     --------- Forms ---------     #
    # --------------------------------- #

@app.post(
    path = "/login",
    response_model = LoginOut,
    status_code = 200,
    tags = ["Login"],
    summary = "Log in to the system"
)
def login( #campos de formulario que vendrán del frontend.
    username: str = Form(...),
    password: str = Form(...)
    ):
    """
        ## Login ##
        
        It will login the user and return the username and the token.

        Parameters:
        - Request body parameters:
            - **username: str** => The username of the user.
            - **password: str** => The password of the user.
        
        Returns:
        - LoginOut(username = username) => A *login model* that contains *username*, message and *(soon)* a *token*.
        It has the variables on it to return the data as a dictionary.
    """
    return LoginOut(username = username) # la clase a retornar es LoginOut y esta al crear el objeto lo convierte a JSON.


    # --------------------------------- #
    # Parametros: Cookies and Headers (FastAPI)
    # --------------------------------- #

@app.post(
    path = "/contact",
    status_code=200,
    tags = ["Forms"],
    summary = "Creates a new contact"
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


    # --------------------------------- #
    # Parametros: Files (FastAPI)
    # --------------------------------- #

@app.post(
    path = "/upload-image",
    status_code = 200,
    tags = ["Files"],
    summary = "Uploads an image"
)
def post_image(
    image: UploadFile = File(...)
):
    """
        ## Post Image

        This endpoint will receive an image and save it in the server.
        
        Parameters:
        - Request body parameters:
            - **image: UploadFile** => A *File* that contains the image

        Returns:
        - dict: A dictionary with the image's information. The image's name, content type and the image's size

    """
    return {
        "File name": image.filename, # nombre del archivo
        "Content type": image.content_type, # content_type es el tipo de archivo que se subió
        "Size (mb)": round(len(image.file.read())/(1024*1024), ndigits = 2) # len(image.file.read()) es el tamaño en bytes y se divide en 1024*1024 para obtener el tamaño en megabytes
        #"Size (kb)": round(len(image.file.read())/1024, ndigits = 2) # len(image.file.read()) es el tamaño en bytes y se divide por 1024 para obtener el tamaño en kilobytes
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