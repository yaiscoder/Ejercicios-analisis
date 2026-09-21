from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
products = []

class Product(BaseModel):
    id: int
    name : str
    price : float
    quantity : int
    category: str

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    category: Optional[str] = None


# crear, leer, actualizar, eliminar

# @app.get("/products")
# def get_products():
#     return products

@app.post("/products")
def create_product(product: Product):
    products.append(product.model_dump())
    return {"message" : "Product successfully saved"}

@app.put("/products/{id}")
def update_product(id: int, product_selectd: ProductUpdate):
    for product in products:
        if product["id"] == id:
            product.update(product_selectd.model_dump())
            return{
                "message" : "Product updated",
                "product" : product
            }
    raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/products/{id}")
def delete_product(id: int):
    for product in products:
        if product["id"] == id:
            products.remove(product)
            return{
                "message" : "Product removed",
                "product" : product
            }
    raise HTTPException(status_code=404, detail="Item not found")


@app.get("/products")
def get_products(
    skip: int = 0, 
    limit: int = 10, 
    category: Optional[str] = None, 
    search: Optional[str] = None
):
    result = products

    # Filtrar por categoría 
    if category:
        result = [p for p in result if p["category"].lower() == category.lower()]  # comprension de lista

    # Filtrar por nombre 
    if search:
        result = [p for p in result if search.lower() in p["name"].lower()] # comprension de lista

    return result[skip : skip + limit]
