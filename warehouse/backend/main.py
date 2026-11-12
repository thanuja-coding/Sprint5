from fastapi import FastAPI , HTTPException
from fastapi.middleware.cors import CORSMiddleware

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


#E1
@app.post("/packages")
def add_package(name , destination , weight , arrival_date , status="pending"):
    return functions.add_package(name=name , destination=destination , weight=weight , arrival_date=arrival_date , status=status)

#E2
@app.get("/packages/{package_id}")
def package(package_id):
    if functions.get_package(id=package_id) is None:
        raise HTTPException(status_code=404,detail="Package not found")
    return functions.get_package(id=package_id)

#E3
@app.patch("/packages/{package_id}")
def update_package(package_id , name=None , destination=None , weight=None , arrival_date=None , status=None):
    if functions.get_package(id=package_id) is None:
        raise HTTPException(status_code=404,detail="Package not found")
    response = functions.update_package(id=package_id , name=name , destination=destination , weight=weight , arrival_date=arrival_date , status=status)
    return response

#E4
@app.delete("/packages/{package_id}")
def delete_package(package_id):
    if functions.get_package(id=package_id) is None:
        raise HTTPException(status_code=404,detail="Package not found")
    if functions.get_package(id=package_id)["status"] == "dispatched":
        raise HTTPException(status_code=400,detail="Cannot delete a dispatched package")
    response = functions.delete_package(id=package_id)
    return {"message":"deleted"}

#E5
@app.get("/packages")
def packages(destination=None , status=None , arrival_date=None):
    return functions.get_all_packages(destination=destination , status=status , arrival_date=arrival_date)

#E6
@app.get("/dispatches")
def dispatches(destination=None , vehicle=None , status=None):
    return functions.get_all_dispatches(destination=destination , vehicle=vehicle , status=status)

#E7
@app.get("/stats")
def stats():
    return functions.get_summary()

#E8
@app.post("/dispatches")
def add_dispatch(vehicle , destination , dispatch_date):
    if functions.get_all_packages(destination=destination , status="pending") == []:
        raise HTTPException(status_code=404,detail="No pending packages for this destination")
    return functions.add_dispatch(vehicle=vehicle , destination=destination , dispatch_date=dispatch_date)