import math
import threading
import time
from behavioralflow.core import Aprendente

PASSOS_POR_SEGUNDO = 20  # 1 segundo = 20 passos (com loop de 0.05s)

WIDTH = 600
HEIGHT = 400

responses = {("cima",):[3,6],
             ("baixo",):[6,6],  # valor alterado para testar direção
             ("esq",):[5,6],
             ("dir",):[5,6],
             ("parado",):[0,3]}

class Agents(Aprendente):
    def __init__(self, acoes, variar=False, prob_variacao=0.25, positionX = 0, positionY = 0, angle = 0, color="#000000"):
        super().__init__(acoes, variar, prob_variacao)
        self.positionX = positionX
        self.positionY = positionY
        self.angle = angle
        self.passos_restantes = 0
        self.color = color
        self.triangle_color = "#ffffff"
    
    # Executa as ações
    def to_respond(self):
        if self.passos_restantes == 0:
            self.proxima_acao(("sem contexto",))
            self.passos_restantes = PASSOS_POR_SEGUNDO

        # Executa a ação atual
        if self._acao_atual[0] == "cima":
            #dx, dy = self._direction_vector()
            #self.positionX = (self.positionX + dx) % WIDTH
            #self.positionY = (self.positionY + dy) % HEIGHT
            self.positionY -= 1 % HEIGHT
        
        elif self._acao_atual[0] == "baixo":
            #dx, dy = self._direction_vector()
            #self.positionX = (self.positionX - dx) % WIDTH
            #self.positionY = (self.positionY - dy) % HEIGHT
            self.positionY = (self.positionY + 1) % HEIGHT
        
        elif self._acao_atual[0] == "esq":
            self.angle = (self.angle - (math.pi / 2)/PASSOS_POR_SEGUNDO) % (2 * math.pi) # 90/PASSOS_POR_SEGUNDO para que ao final tenha feito o movimento apenas 1x
        
        elif self._acao_atual[0] == "dir":
            self.angle = (self.angle + (math.pi / 2)/PASSOS_POR_SEGUNDO) % (2 * math.pi) # 90/PASSOS_POR_SEGUNDO para que ao final tenha feito o movimento apenas 1x
        
        elif self._acao_atual[0] == "parado":
            self.positionX += 0
            self.positionY += 0
        
        #diminue um passo
        self.passos_restantes -= 1
    
    # Calcula a direção (.angle)
    def _direction_vector(self):
        # Retorna o vetor unitário da direção baseada no ângulo (em radianos)
        dx = round(math.cos(self.angle))
        dy = round(-math.sin(self.angle))  # y invertido para "cima"
        return dx, dy

    # Facilita transformar as informações em dicionário para passar para get_statess()
    def to_dict(self):
        return {
            "positionX": self.positionX,
            "positionY": self.positionY,
            "angle": self.angle,
            "ação atual": self._acao_atual,
            "antecedente": self.antecedente_atual,
            "color": self.color,
            "triangle_color": self.triangle_color #ACABEI DE ADICIONAR ESSE
        }

# Criando dois agentes
agents = [
    Agents(responses, prob_variacao=0.0, positionX=50, positionY=50, color="#5690E6"),
    Agents(responses, prob_variacao=0.0, positionX=150, positionY=50, color="#B91CBE"),
]


# Loop de simulação
def simular_em_loop():
    while True:
        for agent in agents:
            agent.to_respond()
        time.sleep(1/PASSOS_POR_SEGUNDO)  # PASSOS_POR_SEGUNDO = 20, logo 50ms por passo

# Iniciar thread do loop
threading.Thread(target=simular_em_loop, daemon=True).start()

# Retorna o JSON com todos os dados a serem desenhados no canvaJS
def get_states():
    return [agent.to_dict() for agent in agents]
    #return[{"id": 1, "x": 50, "y": 50}, {"id": 2, "x": 150, "y": 50}]