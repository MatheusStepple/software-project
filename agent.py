##  CÓDIGO DA ENTREGA PRÉVIA  17/01 ##

import math
import time
from utils.ssl.Navigation import Navigation, Point
from utils.ssl.base_agent import BaseAgent

class ExampleAgent(BaseAgent):
    assigned_targets = {}  # Dicionário compartilhado entre agentes: {target: (agent_id, distancia)}

    def __init__(self, id=0, yellow=False):
        self.id = id
        self.yellow = yellow
        self.last_avoidance_time = time.time()

        ### PARÂMETROS DE NAVEGAÇÃO E EVITAÇÃO DE OBSTÁCULOS ###
        self.avoidance_mode = False  # Modo de evitação de obstáculos ativo ou inativo
        self.avoidance_distancia_range = (1, 0)  # Faixa de distâncias para aplicar a evitação de obstáculos
        self.safe_margin = 0.2  # Margem de segurança para evitar colisões
        self.close_obstacle_distancia = 0.4  # Distância crítica para identificar obstáculos próximos
        self.slow_down_factor = 1.0  # Fator de desaceleração quando o agente se aproxima de obstáculos

        self.targets = []  # Lista de objetivos a serem atingidos pelo agente
        self.assigned_target = None  # Objetivo atribuído ao agente atual
        self.visited_targets = set()  # Conjunto de objetivos já visitados ou cumpridos

    ### FUNÇÕES DE DETECÇÃO E EVITAÇÃO DE OBSTÁCULOS ###

    def cast_ray(self, target, max_distancia=3):
        """Simula a detecção de obstáculos ao longo de uma linha reta até o objetivo."""

        ## calcular a distancia real no plano cartesiano
        dx = target.x - self.robot.x
        dy = target.y - self.robot.y
        distancia_to_target = math.sqrt(dx**2 + dy**2)

        # Simula a detecção de obstáculos com base na distância máxima permitida
        if distancia_to_target < max_distancia:
            return distancia_to_target  # Obstáculo detectado dentro do limite
        return float('inf')  # Sem obstáculos detectados dentro do alcance

    def avoid_obstacle(self, target):
        """Lógica de desvio de obstaculos quando o agente está se aproximando de um objetivo."""
        dx = target.x - self.robot.x
        dy = target.y - self.robot.y
        distancia_to_target = math.sqrt(dx**2 + dy**2)

        # Calcula a distância dinâmica de desvio baseada no alcance do obstáculo
        min_distancia, max_distancia = self.avoidance_distancia_range
        avoidance_distancia = max(
            min_distancia,
            min(max_distancia, distancia_to_target / 2)
        )

        # Calcula um novo ponto para desviar do obstáculo
        avoidance_angle = math.pi / 4  # Ângulo de desvio em relação ao alvo (de 30 até 55 é bom)
        novo_target_x = self.robot.x + (avoidance_distancia * math.cos(avoidance_angle) if dx >= 0 else -avoidance_distancia * math.cos(avoidance_angle))
        novo_target_y = self.robot.y + (avoidance_distancia * math.sin(avoidance_angle) if dy >= 0 else -avoidance_distancia * math.sin(avoidance_angle)) 
        # acima desse comentário é o cálculo de desvio em relação tanto ao eixo x tanto ou eixo y, usando da avoidance_distancia e avoidance_angle como parametro)

        novo_target = Point(novo_target_x, novo_target_y)

        # Calcula a velocidade necessária para atingir o ponto de desvio
        target_velocity, target_angle_velocity = Navigation.goToPoint(self.robot, novo_target)

        # Ajuste de desaceleração quando o obstáculo está muito próximo, bom para ficar mais lento e partir para o próximo objetivo com mais calma, close_obstacle_distancia é parametro mutável
        if distancia_to_target < self.close_obstacle_distancia: 
            self.slow_down_factor = 0.8  # Reduz a velocidade se o obstáculo estiver muito próximo
        else:
            self.slow_down_factor = 1.0  # continua ou restaura a velocidade normal

        # Aplica o fator de desaceleração ou aceleração ao movimento
        adjusted_velocity = Point(
            target_velocity.x * self.slow_down_factor,
            target_velocity.y * self.slow_down_factor
        )

        return adjusted_velocity, target_angle_velocity

    ### FUNÇÕES DE SELEÇÃO E PRIORIZAÇÃO DE TARGETS ###

    def choose_target(self):
        """Escolhe o alvo mais próximo entre os objetivos disponíveis, e marca eles, aplicando a regra da exclusividade"""
        if len(self.targets) == 0: #se nao existir targets 
            return None #retorna nenhum target no momento para esse agent

        sorted_targets = sorted(self.targets, key=lambda target: self.calculate_distancia(target)) #lista de distancias de cada agente para cada target sortada, sendo o primeiro a menor distancia
        closest_target = sorted_targets[0] #seleciona o primeiro, the choosen one
        dx = closest_target.x - self.robot.x
        dy = closest_target.y - self.robot.y
        distancia_to_target = math.sqrt(dx**2 + dy**2) #recalcula a distancia para o target

        return closest_target, distancia_to_target #retorna qual o target mais perto, e sua distancia

    def calculate_distancia(self, target):
        """Calcula a distância real entre o agente e um alvo, dinamicamente."""
        dx = target.x - self.robot.x
        dy = target.y - self.robot.y
        return math.sqrt(dx**2 + dy**2)

    ### FUNÇÕES DE ALOCAÇÃO DE TAREFAS E EXCLUSIVIDADE ###

    def assign_task(self):
        """Atribui um alvo ao agente de forma exclusiva, levando em consideração a proximidade e a exclusividade de alvos."""
        closest_target, closest_distancia = self.choose_target()

        if closest_target is None: #se nao existir target para ele
            print("Nenhum objetivo válido encontrado!")
            self.assigned_target = None
            self.set_vel(Point(0, 0))
            self.set_angle_vel(0)
            return

        # Verifica se o objetivo já foi atribuído a outro agente, para garantir a exclusividade
        if closest_target in ExampleAgent.assigned_targets:
            assigned_agent, assigned_distancia = ExampleAgent.assigned_targets[closest_target]

            if assigned_agent != self.id and closest_distancia >= assigned_distancia:
                print(f"Agente {self.id}: O objetivo já está sendo perseguido pelo agente {assigned_agent}.") #debugar
                self.assigned_target = None
                self.set_vel(Point(0, 0))
                self.set_angle_vel(0)
                return

        # Atualiza a atribuição do objetivo no dicionário compartilhado
        ExampleAgent.assigned_targets[closest_target] = (self.id, closest_distancia)
        self.assigned_target = closest_target

    ### FUNÇÕES DE MOVIMENTAÇÃO E DECISÃO ###

    def move_towards_target(self, target, distancia):
        """Movimenta o agente em direção ao alvo, levando em consideração a evitação de obstáculos."""
        dx = target.x - self.robot.x
        dy = target.y - self.robot.y

        # Verifica obstáculos no caminho
        obstacle_distancia = self.cast_ray(target)

        if obstacle_distancia < float('inf'):
            self.avoidance_mode = True
            target_velocity, target_angle_velocity = self.avoid_obstacle(target)
        else:
            self.avoidance_mode = False
            self.slow_down_factor = 1

            target_velocity, target_angle_velocity = Navigation.goToPoint(self.robot, target)

        # Ajuste da velocidade do agente após desvio ou movimento normal
        adjusted_velocity = Point(
            target_velocity.x * self.slow_down_factor,
            target_velocity.y * self.slow_down_factor
        )

        self.set_vel(adjusted_velocity)
        self.set_angle_vel(target_angle_velocity)

    def decision(self):
        """Função de decisão principal do agente, que determina o que fazer a cada ciclo de execução."""
        self.assign_task()

        if self.assigned_target:
            print(f"Agente {self.id} se movendo em direção ao objetivo: ({self.assigned_target.x:.2f}, {self.assigned_target.y:.2f})")
            self.move_towards_target(self.assigned_target, self.calculate_distancia(self.assigned_target))
        else:
            print(f"Agente {self.id} está parado, sem objetivo atribuído.")
            self.set_vel(Point(0, 0))
            self.set_angle_vel(0)

    def post_decision(self):
        """Função executada após a tomada de decisão, nao sei mt oque fazer aqui"""
        pass
