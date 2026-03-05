from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

task_store = {}
result_store = {}

@app.post("/send-task")
def send_task(data: dict):
    task_store["task"] = data
    return {"status": "task stored"}

@app.get("/get-task")
def get_task():
    return task_store.get("task", {})

@app.post("/submit-result")
def submit_result(data: dict):
    result_store["result"] = data
    return {"status": "result stored"}

@app.get("/get-result")
def get_result():
    return result_store.get("result", {})
