import os
from typing import Dict, Any
from fastapi import FastAPI

from handler import EndpointHandler

app = FastAPI()
endpoint_handler = EndpointHandler(os.environ.get("MODEL_PATH", "."))


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/rewrite")
async def query_rewrite(data: Dict[str, Any]):
    return endpoint_handler(data)
