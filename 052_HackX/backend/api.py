from fastapi import FastAPI, Request
import json
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SESSION_PATH = os.path.join(BASE_DIR, "latest_session.json")

@app.post("/session")
async def receive_session(request: Request):
    data = await request.json()

    with open(SESSION_PATH, "w") as f:
        json.dump(data, f)

    return {"status": "ok"}