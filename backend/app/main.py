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

if __name__ == "main" :
    uvicorn.run(app, host="0.0.0.0", port=8000)