from fastapi import FastAPI, APIRouter,HTTPException
from pydantic import BaseModel
from uuid import UUID
import json

router = APIRouter(
    prefix="/clients"
)

app = FastAPI()
data = json.load(open("antique_dealer.json"))

# function for writing in json file
def write_db(data2):
    with open("antique_dealer.json", "w", encoding='utf-8') as f:
        json.dump(data2, f, ensure_ascii=False, indent=4)

# creating a model
class Client(BaseModel):
    client_id: UUID
    client_first_name: str
    client_last_name: str
    client_mail: str

# method for creating a client
@router.post("/add")
async def create_client(client: Client):
    data['clients'].append(client.dict())
    return {"client": client}


# method for deleting a client
@router.delete("/{client_id}")
async def delete_client(client_id: int):
    data = json.load(open("antique_dealer.json"))
    for client in data['clients']:
        if client["client_id"] == client_id:
            data['clients'].remove(client)
            write_db(data)
        return {f"the {client_id} as been deleted"}
    raise HTTPException(status_code=404, detail="user not found")


# method to get all the user
@router.get("/")
async def get_client():
    data = json.load(open("antique_dealer.json"))
    return data['clients']
