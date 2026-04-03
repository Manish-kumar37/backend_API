from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException
from database import SessionLocal, engine
import database_models
from models import ProductCreate, Product
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
database_models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE
@app.post("/products", response_model=Product)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    db_product = database_models.ProductDB(
        name=product.name,
        description=product.description,
        price=product.price,
        quantity=product.quantity
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# READ ALL
@app.get("/products", response_model=list[Product])
def get_all_products(db: Session = Depends(get_db)):
    return db.query(database_models.ProductDB).all()

# READ ONE
@app.get("/products/{id}", response_model=Product)
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    return db.query(database_models.ProductDB).filter(
        database_models.ProductDB.id == id
    ).first()


@app.post("/products")
def add_product(product: Product):
    Product.append(product)
    return product

# @app.put("/products/{id}")
# def update_product(id: int, product: Product):
#     for i in range(len(Product)):
#         if Product[i].id == id:
#             Product[i] = product
#             return "product added successfully"
#     return "Product not found"



@app.put("/products/{id}", response_model=Product)
def update_product(
    id: int,
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    db_product = db.query(database_models.ProductDB).filter(
        database_models.ProductDB.id == id
    ).first()

    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.quantity = product.quantity

    db.commit()
    db.refresh(db_product)

    return db_product

# @app.delete("/products/{id}")
# def delete_product(id: int):
#     for i in range(len(Product)):
#         if Product[i].id == id:
#             Product.pop(i)
#             return "product deleted successfully"
#     return "Product not found"
@app.delete("/products/{id}")
def delete_product(
    id: int,
    db: Session = Depends(get_db)
):
    db_product = db.query(database_models.ProductDB).filter(
        database_models.ProductDB.id == id
    ).first()

    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(db_product)
    db.commit()

    return {"message": "Product deleted successfully"}
