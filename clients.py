from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
import json

router = APIRouter(
    prefix="/clients"
)

app = FastAPI()


def write_db(data2):
    with open("antique_dealer.json", "w", encoding='utf-8') as f:
        json.dump(data2, f, ensure_ascii=False, indent=4)


# create a new client #
def get_last_client_id():
    data = json.load(open("antique_dealer.json"))
    return data["clients"][-1]["client_id"]


class Client(BaseModel):
    client_id: int | None = None
    client_first_name: str
    client_last_name: str
    client_email: str


@router.post("/{client_id}")
async def create_client(client_id: int, client: Client):
    id_taken = False
    data = json.load(open("antique_dealer.json"))
    client.client_id = client_id
    for clients in data['clients']:
        if client.client_id == clients['client_id']:
            client.client_id = get_last_client_id() + 1
            id_taken = True
    if id_taken:
        data['clients'].append(client.dict())
        write_db(data)
        return {"created client": f"The id {client_id} was already taken,"
                                  f" your client id has been changed to {client.client_id}",
                "new client": client,
                "all clients": data['clients']}
    else:
        data['clients'].append(client.dict())
        write_db(data)
        return {"created client": client, "all clients": data['clients']}


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
            return {"detail": "Client updated", "client": client}
    raise HTTPException(status_code=404, detail=f"client with id {client_id} not found")


# delete a client #

@router.delete("/{client_id}")
async def delete_client(client_id: int):
    data = json.load(open("antique_dealer.json"))
    for client in data['clients']:
        if client["client_id"] == client_id:
            data['clients'].remove(client)
            write_db(data)
            return {"detail": f"the {client_id} as been deleted", "client": data['clients']}
    raise HTTPException(status_code=404, detail=f"client not found with id {client_id}")


# get a client by id #
@router.get("/{client_id}")
async def get_client_by_id(client_id: int):
    data = json.load(open("antique_dealer.json"))
    for client in data['clients']:
        if client['client_id'] == client_id:
            return client
    if client_id not in data['clients']:
        return {"message": f"client_id : {client_id} not found"}


@router.get("/")
async def get_client():
    data = json.load(open("antique_dealer.json"))
    return data['clients']
