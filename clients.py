from fastapi import FastAPI,APIRouter
from pydantic import BaseModel
from uuid import UUID
import json

router = APIRouter(
    prefix="/clients"
)

app = FastAPI()
data = json.load(open("antique_dealer.json"))


class Client(BaseModel):
    client_id: UUID
    client_first_name: str
    client_last_name: str
    client_mail: str


@router.post("/add")
async def create_client(client: Client):
    data['clients'].append(client.dict())
    return {"client" : client }


@router.get("/")
async def get_client():
    return data['clients']
