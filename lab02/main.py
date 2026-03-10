from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Optional, List
import os
import shutil

app = FastAPI()

IMAGE_DIR = "images"
os.makedirs(IMAGE_DIR, exist_ok=True)

products = {}
cur_id = 1

class ProductCreate(BaseModel):
    name: str
    description: str

class ProductUpdate(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None

class Product(BaseModel):
    id: int
    name: str
    description: str
    icon: Optional[str] = None


@app.post("/product", response_model=Product)
def create_product(product: ProductCreate):
    global cur_id

    new_product = Product(
        id=cur_id,
        name=product.name,
        description=product.description,
        icon=None
    )

    products[cur_id] = new_product
    cur_id += 1

    return new_product


@app.get("/product/{product_id}", response_model=Product)
def get_product(product_id: int):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")

    return products[product_id]


@app.put("/product/{product_id}", response_model=Product)
def update_product(product_id: int, data: ProductUpdate):

    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")

    product = products[product_id]

    if data.name is not None:
        product.name = data.name
    if data.description is not None:
        product.description = data.description

    products[product_id] = product

    return product


@app.delete("/product/{product_id}", response_model=Product)
def delete_product(product_id: int):

    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")

    product = products.pop(product_id)

    return product


@app.get("/products", response_model=List[Product])
def get_products():
    return list(products.values())


@app.post("/product/{product_id}/image")
def upload_image(product_id: int, file: UploadFile = File(...)):

    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")

    name, ext = os.path.splitext(file.filename)
    filename = f"{name}_{product_id}{ext}"

    file_path = os.path.join(IMAGE_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    products[product_id].icon = file_path

    return {"message": "Image uploaded", "icon": file_path}


from fastapi.responses import FileResponse

@app.get("/product/{product_id}/image")
def get_image(product_id: int):

    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")

    icon_path = products[product_id].icon

    if icon_path is None or not os.path.exists(icon_path):
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(icon_path)