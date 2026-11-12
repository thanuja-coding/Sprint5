from sqlalchemy import Integer, String, Column, create_engine, ForeignKey, func
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


#E5
def get_all_packages(destination=None, status=None, arrival_date=None):
    session = Session(engine)
    packages = session.query(Packages)
    if destination:
        packages = packages.filter(Packages.destination == destination)
    if status:
        packages = packages.filter(Packages.status == status)
    if arrival_date:
        packages = packages.filter(Packages.arrival_date == arrival_date)
    response = []
    for package in packages.all():
        temp_package = {
            "id": package.id,
            "name": package.name,
            "destination": package.destination,
            "weight": package.weight,
            "arrival_date": package.arrival_date,
            "status": package.status,
            "dispatch_id": package.dispatch_id
        }
        response.append(temp_package)
    session.close()
    return response


#E6
def get_all_dispatches(destination=None, vehicle=None, status=None):
    session = Session(engine)
    dispatches = session.query(Dispatches)
    if destination:
        dispatches = dispatches.filter(Dispatches.destination == destination)
    if vehicle:
        dispatches = dispatches.filter(Dispatches.vehicle == vehicle)
    if status:
        dispatches = dispatches.filter(Dispatches.status == status)
    response = []
    for dispatch in dispatches.all():
        temp_dispatch = {
            "id": dispatch.id,
            "vehicle": dispatch.vehicle,
            "destination": dispatch.destination,
            "dispatch_date": dispatch.dispatch_date,
            "status": dispatch.status
        }
        response.append(temp_dispatch)
    session.close()
    return response


#E7
def get_summary():
    session = Session(engine)
    total = session.query(Packages).count()
    pending = session.query(Packages).filter(Packages.status == "pending").count()
    dispatched = session.query(Packages).filter(Packages.status == "dispatched").count()
    summary = session.query(Packages.destination, func.count(Packages.id)).group_by(Packages.destination).all()
    destinations = []
    for item in summary:
        temp_destination = {
            "destination": item[0],
            "count": item[1]
        }
        destinations.append(temp_destination)
    response = {
        "total_received": total,
        "total_pending": pending,
        "total_dispatched": dispatched,
        "destination_wise_count": destinations
    }
    session.close()
    return response


##E8
def add_dispatch(vehicle, destination, dispatch_date):
    session = Session(engine)
    dispatch = Dispatches(vehicle=vehicle, destination=destination, dispatch_date=dispatch_date, status="scheduled")
    session.add(dispatch)
    session.commit()
    packages = session.query(Packages).filter(Packages.destination == destination, Packages.status == "pending").all()
    for package in packages:
        package.status = "dispatched"
        package.dispatch_id = dispatch.id
    session.commit()
    response = {
        "id": dispatch.id,
        "vehicle": dispatch.vehicle,
        "destination": dispatch.destination,
        "dispatch_date": dispatch.dispatch_date,
        "status": dispatch.status,
        "packages_dispatched": len(packages)
    }
    session.close()
    return response