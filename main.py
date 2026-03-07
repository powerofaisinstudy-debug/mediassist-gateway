import time
import threading
import requests
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

RENDER_URL = "https://mediassist-gateway.onrender.com"


# -------------------------------
# Root endpoint
# -------------------------------
@app.get("/")
def home():
    return {"status": "gateway running"}


# -------------------------------
# Send task from frontend
# -------------------------------
@app.post("/send-task")
def send_task(data: dict):

    task_store["task"] = data

    return {"status": "task stored"}


# -------------------------------
# Client backend fetch task
# -------------------------------
@app.get("/get-task")
def get_task():

    return task_store.get("task", {})


# -------------------------------
# Client backend submit result
# -------------------------------
@app.post("/submit-result")
def submit_result(data: dict):

    result_store["result"] = data

    return {"status": "result stored"}


# -------------------------------
# Frontend get result
# -------------------------------
@app.get("/get-result")
def get_result():

    result = result_store.get("result", {})

    # Reset after sending
    result_store["result"] = {}
    task_store["task"] = {}

    return result


# -------------------------------
# Self ping function
# -------------------------------
def keep_alive():

    while True:

        try:

            requests.get(RENDER_URL)

            print("Self ping sent")

        except Exception as e:

            print("Ping error:", e)

        # 10 minutes
        time.sleep(600)


# -------------------------------
# Start background thread
# -------------------------------
@app.on_event("startup")
def startup_event():

    thread = threading.Thread(target=keep_alive)

    thread.daemon = True

    thread.start()

    print("Render keep-alive started")
