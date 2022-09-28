from fastapi import FastAPI, APIRouter
import json
from pydantic import BaseModel

router = APIRouter(
    prefix="/commands",
)

app = FastAPI()
data = json.load(open("antique_dealer.json"))


def write_db(data2):
    with open("antique_dealer.json", "w", encoding='utf-8') as f:
        json.dump(data2, f, ensure_ascii=False, indent=4)


# Commands #

@router.get("/{command_id}")
async def get_command_by_id(command_id: int):
    for command in data['commands']:
        if command['command_id'] == command_id:
            return command


@router.delete("/{command_id}")
async def delete_command_by_id(command_id: str):
    data.json.load(open("antique_dealer.json"))
    for command in data['commands']:
        if command['command_id'] == command_id:
            data['commands'].remove(command)
            write_db(data)
            return {"command": [f"Command n°{command_id} deleted"]}


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
