from sqlalchemy import Integer, String, Column, create_engine, ForeignKey
from sqlalchemy.orm import Session, declarative_base

DB_PATH = "warehouse.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

class Packages(Base):
    __tablename__ = "packages"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    destination = Column(String)
    weight = Column(String)
    arrival_date = Column(String)
    status = Column(String)
    dispatch_id = Column(Integer, ForeignKey("dispatches.id"))


class Dispatches(Base):
    __tablename__ = "dispatches"
    id = Column(Integer, primary_key=True)
    vehicle = Column(String)
    destination = Column(String)
    dispatch_date = Column(String)
    status = Column(String)

Base.metadata.create_all(engine)


#E1
def add_package(name, destination, weight, arrival_date, status="pending"):
    session = Session(engine)
    package = Packages(name=name, destination=destination, weight=weight, arrival_date=arrival_date, status=status)
    session.add(package)
    session.commit()
    response = {
        "id": package.id,
        "name": package.name,
        "destination": package.destination,
        "weight": package.weight,
        "arrival_date": package.arrival_date,
        "status": package.status
    }
    session.close()
    return response


#E2
def get_package(id):
    session = Session(engine)
    package = session.query(Packages).filter(Packages.id == id).first()
    response = None
    if package:
        response = {
            "id": package.id,
            "name": package.name,
            "destination": package.destination,
            "weight": package.weight,
            "arrival_date": package.arrival_date,
            "status": package.status,
            "dispatch_id": package.dispatch_id
        }
    session.close()
    return response

#E3
def update_package(id, name=None, destination=None, weight=None, arrival_date=None, status=None):
    session = Session(engine)
    package = session.query(Packages).filter(Packages.id == id).first()
    response = None
    if package:
        if name:
            package.name = name
        if destination:
            package.destination = destination
        if weight:
            package.weight = weight
        if arrival_date:
            package.arrival_date = arrival_date
        if status:
            package.status = status
        session.commit()
        response = {
            "id": package.id,
            "name": package.name,
            "destination": package.destination,
            "weight": package.weight,
            "arrival_date": package.arrival_date,
            "status": package.status
        }
    session.close()
    return response

#E4
def delete_package(id):
    session = Session(engine)
    package = session.query(Packages).filter(Packages.id == id).first()
    session.delete(package)
    session.commit()
    session.close()
    return {"message": "Package deleted"}


