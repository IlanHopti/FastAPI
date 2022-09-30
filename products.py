from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
import json


router = APIRouter(
    prefix="/products",
)
app = FastAPI()


# function for writing in json file

def write_db(data2):
    with open("antique_dealer.json", "w", encoding='utf-8') as f:
        json.dump(data2, f, ensure_ascii=False, indent=4)


# create new product

class Product(BaseModel):
    product_id: int | None = None
    product_name: str
    product_description: str
    product_year: int
    product_status: str
    product_price: float


def get_last_product_id():
    data = json.load(open("antique_dealer.json"))
    return data["products"][-1]["product_id"]


# function for get product

@router.get("/{product_id}")
async def read_products(product_id: int):
    data = json.load(open("antique_dealer.json"))
    for product in data["products"]:
        if product["product_id"] == product_id:
            return product
    if product_id not in data["products"]:
        return {"message": f"Product_id : {product_id} not found"}


# function for add new product
@router.post("/{product_id}")
async def create_product(product_id: int, product: Product):
    id_taken = False
    data = json.load(open("antique_dealer.json"))
    product.product_id = product_id
    for products in data["products"]:
        if product.product_id == products["product_id"]:
            product.product_id = get_last_product_id() + 1
            id_taken = True
    if id_taken:
        data["products"].append(product.dict())
        write_db(data)
        return {"created product": f"The id {product.product_id} was already taken,"
                                   f" your product id has been changed to {product.product_id}",
                "new product": product}
    else:
        data["products"].append(product.dict())
        write_db(data)
        return {"created product": product}


# function for delete product

@router.delete("/{product_id}")
async def delete_product(product_id: int):
    data = json.load(open("antique_dealer.json"))
    for product in data['products']:
        if product['product_id'] == product_id:
            data['products'].remove(product)
            write_db(data)
            return {"message": f"Product {product_id} deleted"}
    if product_id not in data['products']:
        return {"message": f"Product {product_id} not found"}

@router.get("/")
async def get_product():
    data = json.load(open("antique_dealer.json"))
    return data['products']
