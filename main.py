from fastapi import FastAPI

import json
import products, commands, clients

app = FastAPI()
app.include_router(products.router)
app.include_router(commands.router)
app.include_router(clients.router)


@app.get("/")
async def root():
    return {"message": "Bienvenue sur Antique Dealer!!"}


@app.get("/clients/{client_first_name}")
async def say_hello(client_first_name: str):
    return {"message": f"Hello {client_first_name}"}


@app.get("/antique_dealer")
async def get_antique_dealer():
    data = json.load(open("antique_dealer.json"))
    return data["commands"]
