from sqlalchemy import create_engine, Integer, String, Float, Column, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine('sqlite:///mydb.db', echo=True)

Base = declarative_base()

class Fruit(Base):
    __tablename__ = 'fruits'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    hashed_password = Column(String , nullable=False)
   
Base.metadata.create_all(engine)
Session_Local  = sessionmaker(bind=engine)
