from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import functions
from datetime import date



app = FastAPI()

# Lets the React app (Vite runs it on port 5173) call this API from the browser.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models: they check the request body before our code runs.
# Wrong type or a rule broken (like weight 0) -> FastAPI sends 422 by itself.

class PackageIn(BaseModel):
    package_name: str
    destination: str
    weight: float = Field(gt=0)
    arrival_date: date


class PackageUpdate(BaseModel):
    package_name: str = None
    destination: str = None
    weight: float = Field(default=None, gt=0)
    arrival_date: date = None
    status: str = None


class BatchIn(BaseModel):
    batch_name: str
    destination: str
    vehicle_number: str
    dispatch_date: str
    package_ids: str


class UserIn(BaseModel):
    username: str
    password: str


# Endpoint 1: POST /packages
# Purpose: Register a new package

@app.post("/packages")
def add_package(package_data: PackageIn, token = Header(None)):
    username = functions.verify_token(token=token, token_type="access")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    package = functions.add_package(
        package_data.package_name,
        package_data.destination,
        package_data.weight,
       str(package_data.arrival_date)
    )

    return package

# Endpoint 2: GET /packages/{package_id}
# Purpose: Get package details using package ID

@app.get("/packages/{package_id}")
def get_package(package_id: int, token = Header(None)):
    username = functions.verify_token(token=token, token_type="access")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    package = functions.get_package_by_id(package_id)

    if package is None:
        raise HTTPException(status_code=404, detail="Package not found")

    return package

# Endpoint 3: PATCH /packages/{package_id}
# Purpose: Update package details

@app.patch("/packages/{package_id}")
def update_package(package_id: int, package_data: PackageUpdate, token = Header(None)):
    username = functions.verify_token(token=token, token_type="access")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    package = functions.update_package(
        package_id,
        package_data.package_name,
        package_data.destination,
        package_data.weight,
        str(package_data.arrival_date),
        package_data.status
    )

    if package is None:
        raise HTTPException(status_code=404, detail="Package not found")

    if package == "invalid_status":
     raise HTTPException( status_code=400,detail="Invalid package status")
    return package

# Endpoint 4: DELETE /packages/{package_id}
# Purpose: Delete a package if it is not dispatched

@app.delete("/packages/{package_id}")
def delete_package(package_id: int, token = Header(None)):
    username = functions.verify_token(token=token, token_type="access")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    result = functions.delete_package(package_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Package not found")

    if result == "dispatched":
        raise HTTPException(status_code=409, detail="Dispatched package cannot be deleted")

    return result

# Endpoint 5: GET /packages
# Purpose: Get all packages with optional filters

@app.get("/packages")
def get_all_packages(
    destination: str = None,
    status: str = None,
    arrival_date: str = None,
    token = Header(None)
):
    username = functions.verify_token(token=token, token_type="access")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return functions.get_all_packages(destination=destination, status=status, arrival_date=arrival_date)

# Endpoint 6: GET /dispatch-batches
# Purpose: Get all dispatch batches with optional filters

@app.get("/dispatch-batches")
def get_all_dispatch_batches(
    destination: str = None,
    vehicle_number: str = None,
    status: str = None,
    token = Header(None)
):
    username = functions.verify_token(token=token, token_type="access")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return functions.get_all_dispatch_batches(destination=destination, vehicle_number=vehicle_number, status=status)

# Endpoint 7: GET /analytics
# Purpose: Get analytics data

@app.get("/analytics")
def get_analytics(token: str = Header(None)):

    username = function.verify_token(token=token,token_type="access")

    if not username:
        raise HTTPException(status_code=401,detail="Invalid or expired token")

    analytics = function.get_analytics()
    return analytics


# Endpoint 8: POST /dispatch-batches
# Purpose: Create a dispatch batch and assign packages

@app.post("/dispatch-batches")
def add_dispatch_batch(batch_data: BatchIn, token = Header(None)):
    username = functions.verify_token(token=token, token_type="access")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    result = functions.add_dispatch_batch(
        batch_data.batch_name,
        batch_data.destination,
        batch_data.vehicle_number,
        str(batch_data.dispatch_date),
        batch_data.package_ids
    )
    if result == "package_not_found":
        raise HTTPException(status_code=404,detail="Package not found or invalid package ID")
    if result == "destination_mismatch":
        raise HTTPException(status_code=400,detail="Package destination does not match batch destination" )
    if result == "package_not_pending":
        raise HTTPException(status_code=409,detail="Package is already assigned or dispatched")
    if result == "duplicate_package":
        raise HTTPException( status_code=400, detail="Duplicate package IDs are not allowed")
    return result


@app.post("/login")
def login(user: UserIn):
    token = functions.verify_login(username=user.username, password=user.password)

    if not token:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    return token

@app.post("/refresh")
def refresh(refresh_token = Header(None)):
    username = functions.verify_token(token=refresh_token, token_type="refresh")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or Expired refresh token")
    access_token = functions.create_token(username=username, token_type="access")
    return {"access_token": access_token}


@app.post("/register")
def register_user(user: UserIn):
    result = functions.register_user(username=user.username, password=user.password)
    if not result:
        raise HTTPException(status_code=400, detail="User already exists")
    return {"message": "User registered successfully"}
