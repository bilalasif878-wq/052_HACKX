from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SESSION_PATH = os.path.join(BASE_DIR, "latest_session.json")

@app.post("/session")
async def receive_session(request: Request):
    data = await request.json()

    with open(SESSION_PATH, "w") as f:
        json.dump(data, f, indent=2)

    return {"status": "saved"}
