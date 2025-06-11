from fastapi import FastAPI
from simulation import get_states, get_learning
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/estate")
def get_estado():
    return get_states()

@app.get("/")
def read_root():
    return {"message": "BehavioralFlow backend is running!"}

@app.get("/learning")
def get_learning():
    return get_learning()