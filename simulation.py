import threading
import time

class Agent:
    def __init__(self, name):
        self.name = name
        self.state = "idle"

    def act(self):
        # Simulação simples (você pode usar sua lógica BehavioralFlow aqui)
        self.state = "thinking"

class Simulation:
    def __init__(self):
        self.agents = [Agent(f"Agent{i}") for i in range(3)]
        self.running = True
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True  # Encerra com o processo principal

    def start(self):
        self.thread.start()

    def run(self):
        while self.running:
            for agent in self.agents:
                agent.act()
            time.sleep(1)  # Espera 1 segundo entre ciclos
    
    # Retorna o JSON com todos os dados a serem desenhados no canvaJS
    def get_states(self):
        return [{ "name": a.name, "state": a.state } for a in self.agents]
