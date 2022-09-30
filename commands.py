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


# Get command by id #

@router.get("/{command_id}")
async def get_command_by_id(command_id: int):
    data = json.load(open("antique_dealer.json"))
    for command in data['commands']:
        if command['command_id'] == command_id:
            return command
    if command_id not in data['commands']:
        return {"message": f"Command_id : {command_id} not found"}


# Get all commands #

@router.get("/")
async def get_antique_dealer():
    data = json.load(open("antique_dealer.json"))
    return data["commands"]


# Create a new command #

def get_last_command_id():
    data = json.load(open("antique_dealer.json"))
    return data["commands"][-1]["command_id"]


class Command(BaseModel):
    command_id: int | None = None
    client_id: int
    product_id: int
    product_name: str
    command_date: str
    command_status: str


@router.post("/{command_id}")
async def create_command(command_id: int, command: Command):
    id_taken = False
    data = json.load(open("antique_dealer.json"))
    command.command_id = command_id
    for commands in data['commands']:
        if command.command_id == commands['command_id']:
            command.command_id = get_last_command_id() + 1
            id_taken = True
    if id_taken:
        data['commands'].append(command.dict())
        write_db(data)
        return {"created command": f"The id {command_id} was already taken,"
                                   f" your command id has been changed to {command.command_id}",
                "new command": command,
                "all commands": data['commands']}
    else:
        data['commands'].append(command.dict())
        write_db(data)
        return {"created command": command, "all commands": data['commands']}


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
    if command_id not in data['commands']:
        return {"message": f"Command_id : {command_id} not found"}


# Delete a command #

@router.delete("/{command_id}")
async def delete_command(command_id: int):
    data = json.load(open("antique_dealer.json"))
    for command in data['commands']:
        if command['command_id'] == command_id:
            data['commands'].remove(command)
            write_db(data)
            return {"message": f"Command {command_id} deleted", "command": data['commands']}
    if command_id not in data['commands']:
        return {"message": f"Command_id : {command_id} not found"}
