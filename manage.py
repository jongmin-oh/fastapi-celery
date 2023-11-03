from fastapi import FastAPI
from fastapi.responses import JSONResponse
from celery_worker import respond

from pydantic import BaseModel

app = FastAPI()


class chatRequest(BaseModel):
    text: str


@app.post("/chat")
def chatbot(request: chatRequest):
    text = request.text
    task = respond.delay(text)
    result = task.get()
    if result == "Too many requests":
        return JSONResponse({"Result": "Too many reqeusts"}, status_code=429)
    return JSONResponse({"Result": task.get()})
