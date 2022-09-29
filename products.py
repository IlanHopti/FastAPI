from fastapi import FastAPI, APIRouter

import json

router = APIRouter(
    prefix="/products",
)
app = FastAPI()

data = json.load(open("antique_dealer.json"))


@router.get("/{product_id}")
async def read_products(product_id: int):
    for product in data["products"]:
        if product["product_id"] == product_id:
            return product


