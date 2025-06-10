import math
import threading
import time
from behavioralflow.core import Aprendente

PASSOS_POR_SEGUNDO = 20  # 1 segundo = 20 passos (com loop de 0.05s)

WIDTH = 600
HEIGHT = 400

responses = {("cima",):[3,6],
             ("baixo",):[3,6],
             ("esq",):[3,6],
             ("dir",):[3,6],
             ("parado",):[0,3]}

class Agents(Aprendente):
    def __init__(self, acoes, variar=False, prob_variacao=0.25, positionX = 0, positionY = 0, angle = 0, color="#000000", previousPositionX=0, previousPositionY=0):
        super().__init__(acoes, variar, prob_variacao)
        self.positionX = positionX
        self.positionY = positionY
        #self.angle = angle # servia para definir para onde o agente está 'virado'
        self.passos_restantes = 0
        self.color = color
        self.circle_color = "#ffffff"
        self.previousPositionX = previousPositionX
        self.previousPositionY = previousPositionY
    
    def set_context(self):
        context = (self.positionX, self.positionY)
        return context

    # Executa as ações
    def to_respond(self, context):
        if self.passos_restantes == 0:
            self.circle_color = "#FFFFFF"
            self.proxima_acao(context)
            self.passos_restantes = PASSOS_POR_SEGUNDO

        # Executa a ação atual
        if self._acao_atual[0] == "cima":
            self.positionY = (self.positionY - 1) % HEIGHT
        
        elif self._acao_atual[0] == "baixo":
            self.positionY = (self.positionY + 1) % HEIGHT
        
        elif self._acao_atual[0] == "esq":
            self.positionX = (self.positionX + 1) % WIDTH
        
        elif self._acao_atual[0] == "dir":
            self.positionX = (self.positionX - 1) % WIDTH
        
        elif self._acao_atual[0] == "parado":
            self.positionX += 0
            self.positionY += 0
        
        #diminue um passo
        self.passos_restantes -= 1
    
    def set_consequence(self):
        in_area_now = 150 <= self.positionY <= 250 and 250 <= self.positionX <= 350
        in_area_before = 150 <= self.previousPositionY <= 250 and 250 <= self.previousPositionX <= 350

        # Reforço: entrou na área
        if not in_area_before and in_area_now:
            self.reforcar()
            self.circle_color = "#4af51f"

        # Punição: saiu da área
        if in_area_before and not in_area_now:
            self.reforcar(-1)
            self.circle_color = "#000000"
        """
        # teste para reforçar quando entrar em um quadrado no meio da tela
        if 250 > self.previousPositionX > 350 and 150 > self.previousPositionY > 250 : # posição inicial fora
            if 150 <= self.positionY <= 250 and 250 <= self.positionX <= 350:
                self.reforcar()
                self.circle_color = "#4af51f"
        # pune quando sair do quadrado
        if 250 <= self.previousPositionX <= 350 and 150 <= self.previousPositionY <= 250 : # posição inicial dentro
            if 150 > self.positionY > 250 and 250 > self.positionX > 350:
                self.reforcar(-1)
                self.circle_color = "#000000"
                """

    
    # Calcula a direção (.angle)
    """def _direction_vector(self):
        # Retorna o vetor unitário da direção baseada no ângulo (em radianos)
        dx = round(math.cos(self.angle))
        dy = round(-math.sin(self.angle))  # y invertido para "cima"
        return dx, dy"""

    # Facilita transformar as informações em dicionário para passar para get_statess()
    def to_dict(self):
        return {
            "positionX": self.positionX,
            "positionY": self.positionY,
            "ação atual": self._acao_atual,
            "antecedente": self.antecedente_atual,
            "color": self.color,
            "circle_color": self.circle_color #ACABEI DE ADICIONAR ESSE
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
            agent.previousPositionY = agent.positionY
            agent.previousPositionX = agent.positionX
            context = agent.set_context()
            agent.to_respond(context)
            agent.set_consequence()
        time.sleep(1/PASSOS_POR_SEGUNDO)  # PASSOS_POR_SEGUNDO = 20, logo 50ms por passo

# Iniciar thread do loop
threading.Thread(target=simular_em_loop, daemon=True).start()

# Retorna o JSON com todos os dados a serem desenhados no canvaJS
def get_states():
    return [agent.to_dict() for agent in agents]
    #return[{"id": 1, "x": 50, "y": 50}, {"id": 2, "x": 150, "y": 50}]