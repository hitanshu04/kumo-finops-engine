"""Kumo FinOps Platform - FastAPI application entrypoint."""

'''from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.db.session import init_db
from app.api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: init DB (optional). Shutdown: cleanup."""
    # Create tables on startup (use Alembic migrations in production)
    await init_db()
    yield
    # Shutdown cleanup if needed
    pass


app = FastAPI(
    title=settings.app_name,
    description="High-performance FinOps platform backend",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/health", tags=["Health"])
async def health_check() -> dict:
    """Health check endpoint for load balancers and orchestration."""
    return {
        "status": "healthy",
        "service": settings.app_name,
        "environment": settings.environment,
    }


@app.get("/", tags=["Root"])
async def root() -> dict:
    """Root endpoint."""
    return {"message": f"Welcome to {settings.app_name} API", "docs": "/docs"}'''



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