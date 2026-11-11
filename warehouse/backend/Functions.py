from sqlalchemy import Column, Integer, Float, String, create_engine, DateTime, func, ForeignKey
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime

DB_PATH = "warehouse.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()


class Package(Base):
    __tablename__ = "packages"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    destination = Column(String)
    weight = Column(String)
    arrival_date = Column(DateTime, default=datetime.now())
    status = Column(Integer)