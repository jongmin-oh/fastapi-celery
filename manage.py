from fastapi import Body, FastAPI
from fastapi.responses import JSONResponse
from celery_worker import create_task

app = FastAPI()


@app.post("/ex1")
def run_task(data=Body(...)):
    amount = int(data["amount"])
    x = data["x"]
    y = data["y"]
    task = create_task.delay(amount, x, y)
    return JSONResponse({"Result": task.get()})
