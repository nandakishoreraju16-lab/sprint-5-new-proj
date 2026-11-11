from sqlalchemy import Integer, String, Column, DateTime, create_engine
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime

DB_PATH = "warehouse.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()


class Package(Base):
    __tablename__ = "packages"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    destination = Column(String)
    weight = Column(Integer)
    arrival_date = Column(DateTime, default=datetime.now)
    status = Column(String, default="pending")
    batch_id = Column(Integer, nullable=True)


class DispatchBatch(Base):
    __tablename__ = "dispatch_batches"
    id = Column(Integer, primary_key=True)
    destination = Column(String)
    vehicle = Column(String)
    status = Column(String, default="planned")
    dispatched_at = Column(DateTime, nullable=True)


Base.metadata.create_all(engine)


# ---------- Turning rows into dicts ----------

def package_to_dict(package):
    return {
        "id": package.id,
        "name": package.name,
        "destination": package.destination,
        "weight": package.weight,
        "arrival_date": package.arrival_date,
        "status": package.status,
        "batch_id": package.batch_id,
    }


def batch_to_dict(batch):
    return {
        "id": batch.id,
        "destination": batch.destination,
        "vehicle": batch.vehicle,
        "status": batch.status,
        "dispatched_at": batch.dispatched_at,
    }


# ---------- E1: Register a package ----------

def add_package(name, destination, weight):
    session = Session(engine)
    package = Package(name=name, destination=destination, weight=weight)
    session.add(package)
    session.commit()
    response = package_to_dict(package)
    session.close()
    return response


# ---------- E2: Get one package ----------

def get_package(package_id):
    session = Session(engine)
    package = session.get(Package, package_id)
    if package is None:
        session.close()
        return None
    response = package_to_dict(package)
    session.close()
    return response


# ---------- E3: Partially update a package ----------

def update_package(package_id, name=None, destination=None, weight=None, status=None):
    session = Session(engine)
    package = session.get(Package, package_id)
    if package is None:
        session.close()
        return None

    # change only the fields that were sent
    if name is not None:
        package.name = name
    if destination is not None:
        package.destination = destination
    if weight is not None:
        package.weight = weight
    if status is not None:
        package.status = status
    session.commit()
    response = package_to_dict(package)
    session.close()
    return response


# ---------- E8: Add data manually ----------

def add_data(name, destination, weight, vehicle=None, batch_id=None):
    session = Session(engine)

    # no batch_id given, so make a new batch
    if batch_id is None:
        batch = DispatchBatch(destination=destination, vehicle=vehicle)
        session.add(batch)
        session.commit()
    else:
        batch = session.get(DispatchBatch, batch_id)
        if batch is None:
            session.close()
            return None

    package = Package(name=name, destination=destination, weight=weight, batch_id=batch.id)
    session.add(package)
    session.commit()
    response = {"batch": batch_to_dict(batch), "package": package_to_dict(package)}
    session.close()
    return response
