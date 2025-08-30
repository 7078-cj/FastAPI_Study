from sqlalchemy import create_engine, Integer, String, Float, Column, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine('sqlite:///mydb.db', echo=True)

Base = declarative_base()

class Fruit(Base):
    __tablename__ = 'fruits'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
   
Base.metadata.create_all(engine)
Session  = sessionmaker(bind=engine)
