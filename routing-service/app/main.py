import uvicorn
from fastapi import FastAPI
from app.api.routing_service import routing_service

description = "Alperen's Routing Engine 🚀 :)"
title = "Routing Engine"
version = "0.0.1"
contact = { 
  "name": "Alperen Adatepe",
  "email": "alperennadatepe@gmail.com"
}

app = FastAPI(title=title, description=description, contact=contact, openapi_url="/api/v1/routing_service/openapi.json", docs_url="/api/v1/routing_service/docs")

app.include_router(routing_service, prefix='/api/v1/routing_service', tags=['routing_service'])

if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000)