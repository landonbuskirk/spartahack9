from pydantic import BaseModel

class MotorData(BaseModel):
    volt : float
    rotate : float
    pressure : float
    vibration : float


class MotorResponse(BaseModel):
    volt : float
    rotate: float
    pressure: float
    vibration: float
    timestamp: str


class PredictionBody(BaseModel):
    repair_cost: int
    downtime: int
    downtime_per_hour_cost: int

class Item(BaseModel):
    threadName: str