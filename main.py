from fastapi import FastAPI
import json

app = FastAPI()

data = json.load(open("antique_dealer.json"))

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/antique_dealer")
async def get_antique_dealer():
    return data
