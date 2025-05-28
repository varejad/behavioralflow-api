import math
import threading
import time
from behavioralflow.core import Aprendente

PASSOS_POR_SEGUNDO = 20  # 1 segundo = 20 passos (com loop de 0.05s)

responses = {("frente",):[0,6],
             ("tras",):[5,6],
             ("esq",):[5,6],
             ("dir",):[0,6],
             ("parado",):[0,3]}

class Agents(Aprendente):
    def __init__(self, acoes, variar=False, prob_variacao=0.25, positionX = 0, positionY = 0, angle = 0):
        super().__init__(acoes, variar, prob_variacao)
        self.positionX = positionX
        self.positionY = positionY
        self.angle = angle
        self.passos_restantes = 0
    
    def to_respond(self):
        if self.passos_restantes == 0:
            self.proxima_acao(("sem contexto",))

        # Executa a ação atual
        if self._acao_atual == "frente":
            dx, dy = self._direction_vector()
            self.positionX += dx
            self.positionY += dy
        
        elif self._acao_atual == "tras":
            dx, dy = self._direction_vector()
            self.positionX -= dx
            self.positionY -= dy
        
        elif self._acao_atual == "esq":
            self.angle = (self.angle - 90) % 360
        
        elif self._acao_atual == "dir":
            self.angle = (self.angle + 90) % 360
        
        elif self._acao_atual == "parado":
            self.positionX += 0
            self.positionY += 0
        
        #diminui um passo
        self.passos_restantes -= 1
    
    def _direction_vector(self):
        # Retorna o vetor unitário da direção baseada no ângulo
        radians = math.radians(self.angle)
        dx = round(math.cos(radians))
        dy = round(-math.sin(radians))  # y invertido para "cima"
        return dx, dy
    
    # Facilita transformar as informações em dicionário para passar para get_statess()
    def to_dict(self):
        return {
            "positionX": self.positionX,
            "positionY": self.positionY,
            "angle": self.angle,
            "ação atual": self._acao_atual,
            "antecedente": self.antecedente_atual # ou outro atributo que você queira mostrar
        }


agents = [
    Agents(responses, prob_variacao=0.0, positionX=50, positionY=50),
    Agents(responses, prob_variacao=0.0, positionX=150, positionY=50),
]


# Loop de simulação
def simular_em_loop():
    while True:
        for agent in agents:
            agent.to_respond()
        time.sleep(1/PASSOS_POR_SEGUNDO)  # 50ms por passo

# Iniciar thread do loop
threading.Thread(target=simular_em_loop, daemon=True).start()

# Retorna o JSON com todos os dados a serem desenhados no canvaJS
def get_states():
    return [agent.to_dict() for agent in agents]
    #return[{"id": 1, "x": 50, "y": 50}, {"id": 2, "x": 150, "y": 50}]