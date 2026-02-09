from pydantic import BaseModel
from datetime import datetime

# This is what the user MUST send us
class CloudCostCreate(BaseModel):
    service: str  # e.g. "AWS EC2"
    amount: float # e.g. 50.5
    
# This is what we give back (including the ID created by the DB)
class CloudCostResponse(CloudCostCreate):
    id: int
    timestamp: datetime
    is_anomaly: bool

    class Config:
        from_attributes = True