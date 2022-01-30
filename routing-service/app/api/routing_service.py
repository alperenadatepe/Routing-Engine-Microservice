from typing import List
from fastapi import APIRouter, HTTPException

from app.api.models import RoutingInput, RoutingOutput
from app.api.routing_engine import RoutingEngine

routing_service = APIRouter()

@routing_service.post('/optimize', response_model=RoutingOutput, status_code=201)
async def route_with_all(routing_input_payload: RoutingInput):
    routing_engine = RoutingEngine(routing_input_payload)

    result = routing_engine.optimize()
    routing_output = RoutingOutput(**result)

    return routing_output