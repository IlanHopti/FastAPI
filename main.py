from fastapi import FastAPI
from pydantic import BaseModel
from uuid import UUID
import json

import clients

app = FastAPI()
data = json.load(open("antique_dealer.json"))
app.include_router(clients.router)

