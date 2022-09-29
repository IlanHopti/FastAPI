from fastapi import FastAPI,APIRouter
from pydantic import BaseModel
from uuid import UUID
import json

router = APIRouter(
    prefix="/clients"
)

app = FastAPI()
data = json.load(open("antique_dealer.json"))


def write_db(data2):
    with open("antique_dealer.json", "w", encoding='utf-8') as f:
        json.dump(data2, f, ensure_ascii=False, indent=4)


class Client(BaseModel):
    client_id: UUID
    client_first_name: str
    client_last_name: str
    client_mail: str


@router.post("/add")
async def create_client(client: Client):
    data['clients'].append(client.dict())
    return {"client": client}


@router.delete("/{client_id}")
async def delete_client_by_id(client_id: int):
    return {"client": [f"Suppression du client n°{client_id}"]}


@router.delete("/{client_id}")
async def delete_client_by_id(client_id: str):
    data.json.load(open("antique_dealer.json"))
    for command in data['clients']:
        if command['client_id'] == client_id:
            data['clients'].remove(command)
            write_db(data)
            return {"client": [f"Client n°{client_id} deleted"]}


@router.get("/")
async def get_client():
    return data['clients']
