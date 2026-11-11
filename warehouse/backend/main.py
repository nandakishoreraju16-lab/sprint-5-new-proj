from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine

app = FastAPI(
    title="Warehouse Dispatch Management System",
    description="REST API for managing warehouse packages and dispatch batches.",
    version="0.1.0",
)

# Allow the React frontend (Vite dev server) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Warehouse Dispatch API is running. Open /docs for Swagger UI."}


@app.get("/health")
def health():
    """Checks that the API can reach PostgreSQL."""
    try:
        with engine.connect():
            return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "ok", "database": "not connected", "error": str(e)}


# TODO: seed data endpoint (row 8 in the README API table)
# TODO: endpoint 1
# TODO: endpoint 2
