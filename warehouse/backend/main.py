from fastapi import FastAPI , HTTPException , Header , Body
from fastapi.middleware.cors import CORSMiddleware 
from pydantic import BaseModel , Field
from datetime import date
import functions


app = FastAPI(
    title = "Warehouse Dispatch API",
    description="Manage warehouse packages,dispatch batches and view warehouse statistics",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173" , "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    dispatch_date: date

#E1
@app.post("/packages")
def add_package(package: PackageCreate , token = Header(None)):
    username=functions.verify_token(token=token,token_type="access")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    return functions.add_package(name=package.name , destination=package.destination , weight=package.weight , arrival_date=str(package.arrival_date) , status=package.status)

@app.get("/packages/{package_id}")
def package(package_id:int,token = Header(None)):
    username=functions.verify_token(token=token,token_type="access")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    if functions.get_package(id=package_id) is None:
        raise HTTPException(status_code=404,detail="Package not found")
    return functions.get_package(id=package_id)
#E3
@app.patch("/packages/{package_id}")
def update_package(package_id , package: PackageUpdate , token = Header(None)):
    username = functions.verify_token(token=token,token_type="access")
    if not username:
        raise HTTPException(status_code=401,detail="Invalid token")
    if functions.get_package(id=package_id) is None:
        raise HTTPException(status_code=404,detail="Package not found")
    response = functions.update_package(id=package_id , destination=package.destination , arrival_date=package.arrival_date , status=package.status , dispatch_id=package.dispatch_id)
    return response

#E4
@app.delete("/packages/{package_id}")
def delete_package(package_id,token = Header(None)):
    username=functions.verify_token(token=token,token_type="access")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    if functions.get_role(token=token) != "admin":
        raise HTTPException(status_code=403, detail="Only admin can delete packages")
    if functions.get_package(id=package_id) is None:
        raise HTTPException(status_code=404,detail="Package not found")
    if functions.get_package(id=package_id)["status"] == "dispatched":
        raise HTTPException(status_code=400,detail="Cannot delete a dispatched package")
    response = functions.delete_package(id=package_id)
    return {"message":"deleted"}

#E5
@app.get("/packages")
def search_packages(destination: str = None, status: str = None, arrival_date: str = None, token = Header(None)):
    username=functions.verify_token(token=token,token_type="access")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    result = functions.get_all_packages(destination, status, arrival_date)
    return result
#E6
@app.get("/dispatches")
def dispatches(destination=None , vehicle=None , status=None,token = Header(None)):
    username=functions.verify_token(token=token,token_type="access")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    return functions.get_all_dispatches(destination=destination , vehicle=vehicle , status=status)

#E7
@app.get("/stats")
def stats(token = Header(None)):
    username=functions.verify_token(token=token,token_type="access")
    if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
    return functions.get_summary()

#E8
@app.post("/dispatches")
def add_dispatch(dispatch: DispatchCreate , token = Header(None)):
    username = functions.verify_token(token=token,token_type="access")
    if not username:
        raise HTTPException(status_code=401,detail="Invalid token")
    if functions.get_role(token=token) != "admin":
        raise HTTPException(status_code=403, detail="Only admin can create dispatches")
    return functions.add_dispatch(vehicle=dispatch.vehicle , destination=dispatch.destination , dispatch_date=str(dispatch.dispatch_date))

@app.post("/login")
def login(username=Body(),password=Body()):
    token=functions.verify_login(username=username,password=password)
    if not token :
        raise HTTPException(status_code=401,detail="Invalid username")
    return token

@app.post("/refresh")
def refresh(refresh_token=Header(None)):
    username = functions.verify_token(token=refresh_token,token_type="refresh")
    if not username:
        raise HTTPException(status_code=401,detail="Invalid or Expired refresh token")

    role = functions.get_role(token=refresh_token)
    access_token = functions.create_token(username=username,token_type="access",role=role)
    return {"access_token":access_token}

@app.post("/register")
def register_user(user_name=Body(),password=Body(),role=Body("staff")):
    if functions.register_user(user_name=user_name,password=password,role=role):
        return {"message":"user registered successfully"}
    raise HTTPException(status_code=400,detail="USer already exists")


