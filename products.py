from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
import json


router = APIRouter(
    prefix="/products",
)
app = FastAPI()

data = json.load(open("antique_dealer.json"))

# function for writing in json file


def write_db(data2):
    with open("antique_dealer.json", "w", encoding='utf-8') as f:
        json.dump(data2, f, ensure_ascii=False, indent=4)


# create new product

class Product(BaseModel):
    product_id: int
    product_name: str
    product_description: str
    product_year: int
    product_status: str
    product_price: float


# function for get product

@router.get("/{product_id}")
async def read_products(product_id: int):
    for product in data["products"]:
        if product["product_id"] == product_id:
            return product


# function for add new product
@router.post("/")
async def create_product(product: Product):
    data = json.load(open("antique_dealer.json"))
    data['products'].append(product.dict())
    write_db(data)
    return data['products']


# function for delete product


@router.delete("/{product_id}")
async def delete_product(product_id: int):
    data = json.load(open("antique_dealer.json"))
    for product in data['products']:
        if product['product_id'] == product_id:
            data['products'].remove(product)
            write_db(data)
            return {"message": f"Product {product_id} deleted"}


