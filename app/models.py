from pydantic import BaseModel
from typing import List

class AccelerometerReading(BaseModel):
    x: float
    y: float
    z: float

class RepCountRequest(BaseModel):
    data: List[AccelerometerReading]
