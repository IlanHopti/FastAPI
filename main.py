from fastapi import FastAPI

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


# More Motivation #
def get_name_with_age(name: str, age: int):
    name_with_age = name + " is this old: " + str(age)
    return name_with_age


# Declaring types #

# Simple types #
def get_items(item_a: str, item_b: int, item_c: float, item_d: bool, item_e: bytes):
    return item_a, item_b, item_c, item_d, item_d, item_e


# List types #
def process_items(items: list[str]):
    for item in items:
        print(item)


# Tuple and Set types #
def process_items_tuple_set(items_t: tuple[int, int, str], items_s: set[bytes]):
    return items_t, items_s


print(get_full_name("john", "doe"))
print(get_name_with_age("john", 20))
print(get_items("Hello", 1, 2.0, True, b"World"))
print(process_items(["a", "b", "c"]))
print(process_items_tuple_set((1, 2, "a"), {b"1", b"2", b"3"}))
