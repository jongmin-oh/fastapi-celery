from fastapi import FastAPI
from fastapi.responses import JSONResponse
from celery_worker import create_task, respond

from pydantic import BaseModel

app = FastAPI()


class testRequset(BaseModel):
    amount: str
    x: int
    y: int


class chatRequest(BaseModel):
    text: str


@app.post("/ex1")
def run_task(request: testRequset):
    amount = int(request.amount)
    x = request.x
    y = request.y
    task = create_task.delay(amount, x, y)
    return JSONResponse({"Result": task.get()})


@app.post("/chat")
def chatbot(request: chatRequest):
    text = request.text
    task = respond.delay(text)
    result = task.get()
    if result == "Too many requests":
        return JSONResponse({"Result": "Too many reqeusts"}, status_code=429)
    return JSONResponse({"Result": task.get()})
