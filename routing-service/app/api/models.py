from pydantic import BaseModel
from typing import Dict, List

class Vehicle(BaseModel):
    id: int
    start_index: int
    capacity: int

class Job(BaseModel):
    id: int
    location_index: int
    load: int

class RoutingInput(BaseModel):
    vehicles: List[Vehicle]
    jobs: List[Job]
    matrix: List[List[int]]

class RoutingOutput(BaseModel):
    total_duration: int
    routes: Dict[str, Dict]
    