import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from . import schemas, database
from sqlalchemy.orm import Session, sessionmaker
from typing import List

app = FastAPI()

origins = [
    "http://localhost:5173/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials = True,
    allow_methods=['*'],
    allow_headers=['*']
)

def get_db():
    db = database.Session()
    try:
        yield db
    finally:
        db.close()

@app.get("/fruits", response_model=List[schemas.Fruit])
def get_fruits(db: Session = Depends(get_db)):
    fruits = db.query(database.Fruit).all()
    return fruits

@app.post("/fruits", response_model=schemas.Fruit)
def add_fruit(fruit: schemas.Fruit, db: Session = Depends(get_db)):
   
    fruit_db = database.Fruit(name=fruit.name)
    
    db.add(fruit_db)
    db.commit()
    db.refresh(fruit_db)  

    return fruit_db

@app.get("/fruits/{id}", response_model=schemas.Fruit)
def get_fruit(id: int, db:Session = Depends(get_db)):
    
    fruit = db.query(database.Fruit).filter(database.Fruit.id == id).first()
    return fruit

@app.put("/fruits/{id}", response_model=schemas.Fruit)
def update_fruit(id: int, fruit: schemas.FruitUpdate, db: Session = Depends(get_db)):
    db_fruit = db.query(database.Fruit).filter(database.Fruit.id == id).first()
   

    update_data = fruit.dict(exclude_unset=True)  # fruit here is Pydantic
    for key, value in update_data.items():
        setattr(db_fruit, key, value)  # db_fruit is SQLAlchemy

    db.commit()
    db.refresh(db_fruit) 
    return db_fruit

@app.delete("/fruits/{id}")
def delete_fruit(id: int, db: Session = Depends(get_db)):
    fruit_db =  db.query(database.Fruit).filter(database.Fruit.id == id).first()
    db.delete(fruit_db)
    db.commit()
    
    return "deleted"

if __name__ == "main" :
    uvicorn.run(app, host="0.0.0.0", port=8000)