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
    motor_repair_cost: float
    amount_of_downtime: float
    per_hour_downtime_cost: float

class Item(BaseModel):
    threadName: str