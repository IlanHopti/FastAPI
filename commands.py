from fastapi import FastAPI, APIRouter
import json
from pydantic import BaseModel

router = APIRouter(
    prefix="/commands",
)

app = FastAPI()
data = json.load(open("antique_dealer.json"))


# Commands #

@router.get("/{command_id}")
async def get_antique_dealer_by_id(command_id: int):
    for command in data['commands']:
        if command['command_id'] == command_id:
            return command


# Create a new command #

class Command(BaseModel):
    command_id: int
    client_id: int
    product_id: int
    product_name: str
    command_date: str
    command_status: str


@router.post("/")
async def create_command(command: Command):
    data['commands'].append(command.dict())
    return command
