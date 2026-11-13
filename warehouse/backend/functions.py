from sqlalchemy import Integer, String, Column, create_engine, ForeignKey,func
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime,timedelta , timezone
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


ph = PasswordHasher()

DB_PATH = "warehouse.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()


ACCESS_TOKEN_EXPIRY = 15
REFRESH_TOKEN_EXPIRY = 7*24*60
SECRET_KEY ="SECRETCODE"
ALGORITHM = "HS256"


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

class User(Base):
    __tablename__ = "Users"
    user_id = Column[int](Integer,primary_key=True)
    user_name=Column[str](String)
    password=Column[str](String)
    role=Column[str](String)



Base.metadata.create_all(engine)


#E1
def add_package(name, destination, weight, arrival_date, status):
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
def update_package(id, destination=None, arrival_date=None, status=None, dispatch_id=None):
    session = Session(engine)
    package = session.query(Packages).filter(Packages.id == id).first()
    response = None
    if package:
        if destination:
            package.destination = destination
        if arrival_date:
            package.arrival_date = arrival_date
        if status:
            package.status = status
        if dispatch_id:
            package.dispatch_id = dispatch_id
            package.status = "dispatched"
        session.commit()
        response={
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



#E8
def add_dispatch(vehicle, destination, dispatch_date):
    session = Session(engine)
    dispatch = Dispatches(vehicle=vehicle, destination=destination, dispatch_date=dispatch_date, status="scheduled")
    session.add(dispatch)
    session.commit()
    response = {
        "id": dispatch.id,
        "vehicle": dispatch.vehicle,
        "destination": dispatch.destination,
        "dispatch_date": dispatch.dispatch_date,
        "status": dispatch.status
    }
    session.close()
    return response

def get_dispatch(id):
    session = Session(engine)
    dispatch = session.query(Dispatches).filter(Dispatches.id == id).first()
    response = None
    if dispatch:
        response = {
            "id": dispatch.id,
            "vehicle": dispatch.vehicle,
            "destination": dispatch.destination,
            "dispatch_date": dispatch.dispatch_date,
            "status": dispatch.status
        }
    session.close()
    return response


def verify_login(username,password):
    session = Session(engine)
    user = session.query(User).filter_by(user_name=username).first()
    if user is None:
        session.close()
        return False
    try :
        ph.verify(user.password,password)
       
    except VerifyMismatchError:
        session.close()
        return False 
    role=user.role 
    session.close()
    access_token = create_token(username=username,token_type="access",role=role)  
    refresh_token= create_token(username=username,token_type="refresh",role=role)
    return {"access_token":access_token,"refresh_token":refresh_token}

    

def create_token(username,token_type,role):
    time = ACCESS_TOKEN_EXPIRY
    if token_type == "refresh":
        time = REFRESH_TOKEN_EXPIRY
    payload={
        "username":username,
        "token_type":token_type,
        "role":role,
        "exp":datetime.now(timezone.utc)+timedelta(minutes=time)
    }
    token =jwt.encode(payload=payload,key=SECRET_KEY,algorithm=ALGORITHM)
    return token

def verify_token(token,token_type):
    try:
        payload = jwt.decode(jwt=token,key=SECRET_KEY,algorithms=[ALGORITHM])
    except:
        return False
    
    if payload ["token_type"] == token_type:
        return payload["username"]
    return False

def get_role(token):
    try:
        payload = jwt.decode(jwt=token,key=SECRET_KEY,algorithms=[ALGORITHM])
    except:
        return None
    return payload["role"]

#user
def register_user(user_name:str,password:str,role:str):
    session = Session(bind=engine)
    user_exists = session.query(User).filter_by(user_name=user_name).first()
    if user_exists is not None:
        session.close()
        return False
    session.add(User(user_name=user_name , password=ph.hash(password),role=role))
    session.commit()
    session.close()
    return True
    
        

    
   