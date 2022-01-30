# Routing Engine
 
## How to run?
 - Create a virtual environment `virtualenv env` and activate `source ./env/bin/activate`
 - Install fastapi and uvicorn with `pip install fastapi` and `pip install uvicorn`
 - Make sure you have installed `docker` and `docker-compose`
 - Run `docker-compose up -d`
 - Head over to http://localhost:8080/api/v1/routing_service/docs for routing service endpoints.

## Couple of notes
 - This repo is designed for microservice architecture, yet only routing-service app is here. But you can extend however you prefer.
 - You can view nginx configs and docker compose file at the root folder.
 - You can find the `input.json` and corresponding `output.json` in the root folder. 
 - Routing-service folder is the main folder for the source
  - You can access the `Dockerfile`. 
  - Also requirements.txt represents the necessary libraries for the app.
  - App folder has a `main.py` file which initialize the app. Also contains a folder called api which includes;
    - `Routing_service.py` - Endpoints for the api.
    - `Routing_engine.py` - Optimizer for the problem.
    - `Models.py` - Necessary data object definitions.
    - `Helpers.py` - Util functions for data manipulations and so on.