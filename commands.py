from fastapi import FastAPI, APIRouter
import json
from pydantic import BaseModel

router = APIRouter(
    prefix="/commands",
)

app = FastAPI()


# function for writing in json file
def write_db(data2):
    with open("antique_dealer.json", "w", encoding='utf-8') as f:
        json.dump(data2, f, ensure_ascii=False, indent=4)


def write_db(data2):
    with open("antique_dealer.json", "w", encoding='utf-8') as f:
        json.dump(data2, f, ensure_ascii=False, indent=4)


# Commands #

@router.get("/{command_id}")
async def get_command_by_id(command_id: int):
    data = json.load(open("antique_dealer.json"))
    for command in data['commands']:
        if command['command_id'] == command_id:
            return command
    if command_id not in data['commands']:
        return {"message": f"Command_id : {command_id} not found"}


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
    data = json.load(open("antique_dealer.json"))
    data['commands'].append(command.dict())
    write_db(data)
    return data['commands']


# Update a command #

class CommandUpdate(BaseModel):
    command_status: str


@router.patch("/{command_id}")
async def update_command(command_id: int, updated_command: CommandUpdate):
    data = json.load(open("antique_dealer.json"))
    for command in data['commands']:
        if command['command_id'] == command_id:
            command['command_status'] = updated_command.command_status
            write_db(data)
            return command


# Delete a command #

@router.delete("/{command_id}")
async def delete_command(command_id: int):
    data = json.load(open("antique_dealer.json"))
    for command in data['commands']:
        if command['command_id'] == command_id:
            data['commands'].remove(command)
            write_db(data)
            return {"message": f"Command {command_id} deleted", "command": data['commands']}
