from fastapi import FastAPI
from simulation import Simulation, get_statess
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
simulation = Simulation()
simulation.start()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/estate")
def get_estado():
    return get_statess()

"""@app.get("/estate")
def get_estado():
    return simulation.get_states()"""

@app.get("/")
def read_root():
    return {"message": "BehavioralFlow backend is running!"}
