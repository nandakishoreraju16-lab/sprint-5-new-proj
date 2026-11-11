from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import functions

app = FastAPI()

# Lets the React app (Vite runs it on port 5173) call this API from the browser.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# E1 - Register a package
@app.post("/packages", status_code=201)
def add_package(name, destination, weight: int):
    if name.strip() == "":
        raise HTTPException(status_code=422, detail="Name is required.")
    if destination.strip() == "":
        raise HTTPException(status_code=422, detail="Destination is required.")
    if weight <= 0:
        raise HTTPException(status_code=422, detail="Weight must be more than 0.")
    return functions.add_package(name=name, destination=destination, weight=weight)


# E2 - Get one package
@app.get("/packages/{package_id}")
def get_package(package_id: int):
    package = functions.get_package(package_id=package_id)
    if package is None:
        raise HTTPException(status_code=404, detail="Package not found.")
    return package


# E3 - Partially update a package
@app.patch("/packages/{package_id}")
def update_package(package_id: int, name=None, destination=None, weight: int = None, status=None):
    if name is None and destination is None and weight is None and status is None:
        raise HTTPException(status_code=422, detail="Send at least one field to update.")
    if name is not None and name.strip() == "":
        raise HTTPException(status_code=422, detail="Name is required.")
    if destination is not None and destination.strip() == "":
        raise HTTPException(status_code=422, detail="Destination is required.")
    if weight is not None and weight <= 0:
        raise HTTPException(status_code=422, detail="Weight must be more than 0.")
    if status is not None and status not in ["pending", "dispatched"]:
        raise HTTPException(status_code=422, detail="Status must be pending or dispatched.")
    package = functions.update_package(package_id=package_id, name=name, destination=destination, weight=weight, status=status)
    if package is None:
        raise HTTPException(status_code=404, detail="Package not found.")
    return package


# E8 - Add data manually (create a dispatch batch and assign packages)
@app.post("/dispatch-batches", status_code=201)
def add_data(name, destination, weight: int, vehicle=None, batch_id: int = None):
    if name.strip() == "":
        raise HTTPException(status_code=422, detail="Name is required.")
    if destination.strip() == "":
        raise HTTPException(status_code=422, detail="Destination is required.")
    if weight <= 0:
        raise HTTPException(status_code=422, detail="Weight must be more than 0.")
    if batch_id is None and vehicle is None:
        raise HTTPException(status_code=422, detail="Vehicle is required to make a new batch.")
    response = functions.add_data(name=name, destination=destination, weight=weight, vehicle=vehicle, batch_id=batch_id)
    if response is None:
        raise HTTPException(status_code=404, detail="Dispatch batch not found.")
    return response
