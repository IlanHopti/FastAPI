from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel
from enum import Enum

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


# Python Types - Intro #

# Motivation #

def get_full_name(first_name: str, last_name: str):
    full_name = first_name.title() + " " + last_name.title()
    return full_name


print(get_full_name("john", "doe"))


# More Motivation #

def get_name_with_age(name: str, age: int):
    name_with_age = name + " is this old: " + str(age)
    return name_with_age


print(get_name_with_age("john", 20))


# Declaring types #

# Simple types #
def get_items(item_a: str, item_b: int, item_c: float, item_d: bool, item_e: bytes):
    return item_a, item_b, item_c, item_d, item_d, item_e


print(get_items("Hello", 1, 2.0, True, b"World"))


# List types #

def process_items(items: list[str]):
    for item in items:
        print(item)


process_items(["a", "b", "c"])


# Tuple and Set types #

def process_items_tuple_set(items_t: tuple[int, int, str], items_s: set[bytes]):
    return items_t, items_s


print(process_items_tuple_set((1, 2, "a"), {b"1", b"2", b"3"}))


# Dict types #

def process_items_dict(prices: dict[str, float]):
    for item_name, item_price in prices.items():
        print(item_name)
        print(item_price)


process_items_dict({"a": 1.0, "b": 2.0, "c": 3.0})


# Union types #

def process_item_union(item: int | str):
    print(item)


process_item_union(1)


# Possible types #

def say_hi(name: str | None = None):
    if name is not None:
        print(f"Hey {name}!")
    else:
        print("Hello World")


say_hi("john")
say_hi()


# Classes as types #

class Person:
    def __init__(self, name: str):
        self.name = name


def get_person_name(one_person: Person):
    return one_person.name


# Pydantic models #

class User(BaseModel):
    id: int
    name = "John Doe"
    signup_ts: datetime | None = None
    friends: list[int] = []


external_data = {
    "id": "123",
    "signup_ts": "2017-06-01 12:22",
    "friends": [1, "2", b"3"],
}
user = User(**external_data)
print(user)
# > User id=123 name='John Doe' signup_ts=datetime.datetime(2017, 6, 1, 12, 22) friends=[1, 2, 3]
print(user.id)
# > 123


# Tutorial - User Guide - Path Parameters #


@app.get("/item/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}


# Tutorial - User Guide - Order matters #
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


@app.get("/users")
async def read_users():
    return ["Rick", "Morty"]


@app.get("/users")
async def read_users2():
    return ["Bean", "Elfo"]


# Tutorial - User Guide - Predefined values #
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


# Tutorial - User Guide - Path parameters containing paths #

@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


# Tutorial - User Guide - Query parameters #


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]
