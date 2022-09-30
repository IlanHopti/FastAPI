from fastapi import FastAPI, APIRouter, HTTPException
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


@router.post("/")
async def create_client(client: Client):
    data = json.load(open("antique_dealer.json"))
    data['clients'].append(client.dict())
    return {"client": client}


# update a client

class ClientUpdate(BaseModel):
    client_id: int | None = None
    client_first_name: str
    client_last_name: str
    client_email: str


@router.put("/{client_id}")
async def update_client(client_id: int, updated_client: ClientUpdate):
    data = json.load(open("antique_dealer.json"))
    for client in data['clients']:
        if client['client_id'] == client_id:
            if updated_client.client_id is None:
                updated_client.client_id = client_id
            else:
                client['client_id'] = updated_client.client_id
            client['client_first_name'] = updated_client.client_first_name
            client['client_last_name'] = updated_client.client_last_name
            client['client_email'] = updated_client.client_email
            write_db(data)
            return client
    raise HTTPException(status_code=404, detail="Client not found")


# delete a client #

@router.delete("/{client_id}")
async def delete_client(client_id: int):
    data = json.load(open("antique_dealer.json"))
    for client in data['clients']:
        if client["client_id"] == client_id:
            data['clients'].remove(client)
            write_db(data)
        return {f"the {client_id} as been deleted"}
    raise HTTPException(status_code=404, detail="user not found")

# get a client by id #


@router.get("/")
async def get_client():
    data = json.load(open("antique_dealer.json"))
    return data['clients']
