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
    created_at = Column(String)

class User(Base):
    __tablename__ = "Users"
    user_id = Column[int](Integer,primary_key=True)
    user_name=Column[str](String)
    password=Column[str](String)
    role=Column[str](String, default="staff")


Base.metadata.create_all(engine)


#E1
def add_package(name, destination, weight, arrival_date, status):
    session = Session(engine)
    new_package = Packages(name=name, destination=destination, weight=weight, arrival_date=arrival_date, status=status)
    session.add(new_package)
    session.commit()
    response = {
        "id": new_package.id,
        "name": new_package.name,
        "destination": new_package.destination,
        "weight": new_package.weight,
        "arrival_date": new_package.arrival_date,
        "status": new_package.status
    }
    session.close()
    return response

#E2
def get_package(id):
    session = Session(engine)
    package = session.get(Packages, id)
    session.close()
    return package

#E3
def update_package(id, destination=None, arrival_date=None, status=None, dispatch_id=None):
    session = Session(engine)
    package = session.get(Packages, id)
    if destination is not None:
        package.destination = destination
    if arrival_date is not None:
        package.arrival_date = str(arrival_date)
    if status is not None:
        package.status = status
    if dispatch_id is not None:
        package.dispatch_id = dispatch_id
        package.status = "dispatched"
    session.commit()
    session.close()
    return {"message": "Package updated successfully"}

#E4
def delete_package(id):
    session = Session(engine)
    package = session.get(Packages, id)
    session.delete(package)
    session.commit()
    session.close()
    return {"message": "Package deleted successfully"}

#E5
def get_all_packages(destination=None, status=None, arrival_date=None):
    session = Session(engine)
    query = session.query(Packages)
    if destination is not None:
        query = query.filter(Packages.destination == destination)
    if status is not None:
        query = query.filter(Packages.status == status)
    if arrival_date is not None:
        query = query.filter(Packages.arrival_date == arrival_date)
    response = []
    for package in query.all():
        response.append(package)
    session.close()
    return response

#E6
def get_all_dispatches(destination=None, vehicle=None, status=None):
    session = Session(engine)
    query = session.query(Dispatches)
    if destination is not None:
        query = query.filter(Dispatches.destination == destination)
    if vehicle is not None:
        query = query.filter(Dispatches.vehicle == vehicle)
    if status is not None:
        query = query.filter(Dispatches.status == status)
    response = []
    for dispatch in query.all():
        response.append(dispatch)
    session.close()
    return response

# E7
def get_summary():
    session = Session(engine)
    package_list = session.query(Packages).all()

    pending = 0
    dispatched = 0
    destination_count = {}

    for package in package_list:
        if package.status == "pending":
            pending = pending + 1
        if package.status == "dispatched":
            dispatched = dispatched + 1

        if package.destination in destination_count:
            destination_count[package.destination] = destination_count[package.destination] + 1
        else:
            destination_count[package.destination] = 1

    session.close()
    return {
        "total_received": len(package_list),
        "total_pending": pending,
        "total_dispatched": dispatched,
        "destination_wise_count": destination_count,
    }

# E8
def add_dispatch(vehicle, destination):
    session = Session(engine)
    new_dispatch = Dispatches(
        vehicle=vehicle,
        destination=destination,
        status="scheduled",
        dispatch_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        created_at=datetime.now().strftime("%Y-%m-%d"),
    )

    session.add(new_dispatch)
    session.commit()
    session.close()
    return {"message": "Dispatch created successfully"}


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
    
    access_token = create_token(username=username,token_type="access",role=user.role)
    refresh_token= create_token(username=username,token_type="refresh",role=user.role)

    session.close()
    return {"access_token":access_token,"refresh_token":refresh_token}


def create_token(username,token_type,role):
    time = ACCESS_TOKEN_EXPIRY
    if token_type == "refresh":
        time = REFRESH_TOKEN_EXPIRY
    payload={
        "role":role,
        "username":username,
        "token_type":token_type,
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
        return payload
    return False


#user
def register_user(user_name :str, password: str, role: str):
    session = Session(engine)
    user_exists = session.query(User).filter_by(user_name = user_name).first()
    if user_exists is not None:
        session.close()
        return False

    try:
        hashed_password = ph.hash(password)
    except Exception:
        session.close()
        return False

    session.add(User(user_name=user_name, password=hashed_password, role=role))
    session.commit()
    session.close()
    return True