from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import models, database, schemas, crud

app = FastAPI(title="Kumo FinOps Engine")

# Create Tables
models.Base.metadata.create_all(bind=database.engine)

# Dependency to get DB


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"System": "Kumo", "Status": "Ready for Money"}

# --- NEW: The Ingestion Endpoint ---


@app.post("/ingest/", response_model=schemas.CloudCostResponse)
def ingest_data(cost: schemas.CloudCostCreate, db: Session = Depends(get_db)):
    # This calls the Logic file to save data
    return crud.create_cost(db=db, cost=cost)

# --- NEW: The View Endpoint (To see what we saved) ---


@app.get("/costs/", response_model=List[schemas.CloudCostResponse])
def read_costs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_costs(db, skip=skip, limit=limit)
