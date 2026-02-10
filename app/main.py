from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
# CORS is important for allowing cross-origin requests, especially if your frontend is hosted on a different domain than your backend API.
from fastapi.middleware.cors import CORSMiddleware
from . import models, database, schemas, crud

app = FastAPI(title="Kumo FinOps Engine")

# CORS Middleware Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

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

# --- The Ingestion Endpoint ---


@app.post("/ingest/", response_model=schemas.CloudCostResponse)
def ingest_data(cost: schemas.CloudCostCreate, db: Session = Depends(get_db)):
    # This calls the Logic file to save data
    return crud.create_cost(db=db, cost=cost)

# --- The View Endpoint ---


@app.get("/costs/", response_model=List[schemas.CloudCostResponse])
def read_costs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_costs(db, skip=skip, limit=limit)
