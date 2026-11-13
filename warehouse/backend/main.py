from fastapi import FastAPI , HTTPException , Header , Body
from fastapi.middleware.cors import CORSMiddleware 
from pydantic import BaseModel , Field
from datetime import date
import functions


app = FastAPI(
    title = "Warehouse Dispatch API",
    description="Manage warehouse packages,dispatch batches and view warehouse statistics",
)
ROLES = ["admin", "staff"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173" , "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def authorize(token, allowed_roles):
    payload = functions.verify_token(token=token, token_type="access")
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")
    if payload["role"] not in allowed_roles:
        raise HTTPException(status_code=403, detail="You do not have permission to do this")
    return payload


class PackageCreate(BaseModel):
    name: str = Field(min_length=2)
    destination: str
    weight: float = Field(gt=0)
    arrival_date: date
    status: str = "pending"


class PackageUpdate(BaseModel):
    destination: str = None
    arrival_date: date = None
    status: str = None
    dispatch_id: int = None

class DispatchCreate(BaseModel):
    vehicle: str
    destination: str

#E1
@app.post("/packages")
def add_package(package: PackageCreate , token = Header(None)):
    authorize(token, ["admin", "staff"])
    return functions.add_package(name=package.name , destination=package.destination , weight=package.weight , arrival_date=str(package.arrival_date) , status=package.status)

#E2
@app.get("/packages/{package_id}")
def package(package_id:int,token = Header(None)):
    authorize(token, ["admin", "staff"])
    if functions.get_package(id=package_id) is None:
        raise HTTPException(status_code=404,detail="Package not found")
    return functions.get_package(id=package_id)

#E3
@app.patch("/packages/{package_id}")
def update_package(package_id , package: PackageUpdate , token = Header(None)):
    authorize(token, ["admin", "staff"])
    if functions.get_package(id=package_id) is None:
        raise HTTPException(status_code=404,detail="Package not found")
    response = functions.update_package(id=package_id , destination=package.destination , arrival_date=package.arrival_date , status=package.status , dispatch_id=package.dispatch_id)
    return response

#E4
@app.delete("/packages/{package_id}")
def delete_package(package_id,token = Header(None)):
    authorize(token, ["admin"])
    if functions.get_package(id=package_id) is None:
        raise HTTPException(status_code=404,detail="Package not found")
    if functions.get_package(id=package_id).status == "dispatched":
        raise HTTPException(status_code=400,detail="Cannot delete a dispatched package")
    response = functions.delete_package(id=package_id)
    return {"message":"deleted"}

#E5
@app.get("/packages")
def search_packages(destination: str = None, status: str = None, arrival_date: str = None, token = Header(None)):
    authorize(token, ["admin", "staff"])
    result = functions.get_all_packages(destination, status, arrival_date)
    return result

#E6
@app.get("/dispatches")
def dispatches(destination=None , vehicle=None , status=None,token = Header(None)):
    authorize(token, ["admin", "staff"])
    return functions.get_all_dispatches(destination=destination , vehicle=vehicle , status=status)

#E7
@app.get("/stats")
def stats(token = Header(None)):
    authorize(token, ["admin", "staff"])
    return functions.get_summary()

#E8
@app.post("/dispatches")
def add_dispatch(dispatch: DispatchCreate , token = Header(None)):
    authorize(token, ["admin"])
    return functions.add_dispatch(vehicle=dispatch.vehicle , destination=dispatch.destination)

@app.post("/login")
def login(username=Body(),password=Body()):
    token=functions.verify_login(username=username,password=password)
    if not token :
        raise HTTPException(status_code=401,detail="Invalid username")
    return token

@app.post("/refresh")
def refresh(refresh_token=Header(None)):
    payload = functions.verify_token(token=refresh_token,token_type="refresh")
    if not payload:
        raise HTTPException(status_code=401,detail="Invalid or Expired refresh token")

    access_token = functions.create_token(username=payload["username"],token_type="access",role=payload["role"])
    return {"access_token":access_token}

@app.post("/register")
def register_user(user_name=Body(),password=Body(),role=Body("staff")):
    if role not in ROLES:
        raise HTTPException(status_code=400,detail="Role must be admin or staff")
    if functions.register_user(user_name=user_name,password=password,role=role):
        return {"message":"user registered successfully"}
    raise HTTPException(status_code=400,detail="USer already exists")
