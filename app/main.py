#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field

#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

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

# Contendrá todos el código que comparte Person y PersonOut y éstas heredarán de PersonBase
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

class Person(PersonBase): #Es lo único que no hereda de PersonBase
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
class PersonOut(PersonBase): # Solo hereda de PersonBase
    pass


    ##Path Parameters are always required!##
    # Request and Response Body (FastAPI)

@app.get("/")
def home(): 
    return {"Hello": "World"}

"""
    # Ejemplo 2 - Output Model Person (This can be used as a quick shortcut if you have only one Pydantic model and want to remove some data from the output.)

@app.post("/person/new", response_model=Person, response_model_exclude={"password"})
def create_person(person: Person = Body(...)): 
    return person
"""

    # Ejemplo 1 - Output Model Person con el modelo de person pero en el path decorator se puede usar el modelo de personOut para el response.
@app.post("/person/new", response_model=PersonOut, status_code=201) #response_model is the model that will be returned in the response body
def create_person(person: Person = Body(...)): 
    return person

    # Validaciones: Query Parameters (FastAPI)  (Query Parameters are always optional)

@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1, 
        max_length=50,
        title="Person Name",
        description="This is the person name. It's between 1 and 50 characters",
        example="Rocio"
        ),
    age: str = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's required",
        example=25
        )
): 
    return {name: age}

    # Validaciones: Path Parameters (FastAPI)

@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ..., 
        gt=0,
        example=123
        )
): 
    return {person_id: "It exists!"}

    # Validaciones: Request Body (FastAPI)

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0,
        example=123
    ),
    person: Person = Body(...),
    #location: Location = Body(...)
): 
    #results = person.dict()
    #results.update(location.dict())
    #return results
    return person