import math
import os
import time
from utils.ssl.Navigation import Navigation, Point
from utils.ssl.base_agent import BaseAgent
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dificuldade", type=int, required=True)
args = parser.parse_args()
dificuldade = args.dificuldade

class ExampleAgent(BaseAgent):
    distancias_agentes = {}  # Dicionário: {id_alvo: (id_agente, distancia)}
    agentes_informacoes = {}  # Dicionário para informações exibidas
    ultimo_display = ""  # Para evitar exibições redundantes

    def __init__(self, id=0, yellow=False):
        super().__init__(id, yellow)
        self.modo_desviar = True

        ###### PARAMETROS ######

        self.distancia_de_evitar_range = (1, 0.2) # entre de 0.5 até 1.5, e de 0 até 0.5
        self.margem_safe = 0.2  # tem que ser 0.2, pois é o raio do objetivo e conta como margem
        self.distancia_perto_demais = 0.4 # desacelera chegando perto do objetivo, é bom de 0.3 até 0.6, dependendo da quantidade de desaceleração
        self.velocidade_do_agente = 1 # velocidade máxima no ínicio, depois vai mudar
        self.distancia_alerta = 0.5 #distancia que faz o display mostrar "desviando de obstaculos"

        ###### PARAMETROS ######

        self.targets = []
        self.target_designado = None

    def ray_casting(self, target, max_distance=3): ### Realiza o tal do ray casting em direção ao alvo.
        
        dx = target.x - self.robot.x
        dy = target.y - self.robot.y

        distance_to_target = (dx**2 + dy**2)**0.5


        return distance_to_target if distance_to_target < max_distance else float('inf')
    
    def painel_de_controle(self): ### Exibe informações detalhadas e organizadas sobre a simulação. Se ligar em abrir o terminal do ubuntu no tamanho certo
        
        
        ExampleAgent.agentes_informacoes[self.id] = {
            "posicao": f"({self.robot.x:.1f}, {self.robot.y:.1f})",
            "status": self.status_agente(),
        }

        # usa info_linha como uma lista e vai dando append, pra cada coisa que eu quero mostrar

        info_linha = [f"--- INFORMAÇÕES DA SIMULAÇÃO DE DIFICULDADE {dificuldade} ---"]
        info_linha.append("")

        for agent_id, info in sorted(ExampleAgent.agentes_informacoes.items()): #contrói o painel de controle com as informações
            posicao = info["posicao"]
            status = info["status"]
            info_linha.append(f"AGENTE {agent_id + 1} | Posição: {posicao} | Status: {status}")

        info_linha.append("")

        info_linha.append(f"Número total de agentes: {len(ExampleAgent.agentes_informacoes)}")
        info_linha.append("-------------------------------")
        info_linha.append("")
        info_linha.append('Matheus "Stepple" Stepple')
        
        # desenho artístico feito em 1892 por Leonardo Da Vinci
        info_linha.append("""
                                                                                
                .=%%%%%%%%%%%%%%%%%#-  .             
            .-%%%%%%%%%%%%%%%%%%%%%%%%%@+:           
         :-%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%=.         
       :=%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%=:       
     .=%%%%%%%%%%%%%%##*=-::-=*##%%%%%%%%%%%%%-.     
    --%%%%%%%%%##+-.  .:-#@@#-:.  .-+*#%%%%%%%%%-.   
   -@%%%%%%%%%-.:::@@@@@@@@@@@@@@@@:--.-#%%%%%%%%-   
   =%%%%%%%%%*-@@@@@@@@@@@@@@@@@@@@@@-@+*%%%%%%%%%=  
  -%%%%%%%%%#::@@@#:@@@@@@@@@@@@@@ +@@@::%%%%%%%%%%= 
 =%%%%%%%%%%*-@@@.  @@@@@@@@@@@@@=  :@@@.%%%%%%%%%%% 
:%%%%%%%%%%%*+@@@.  @@@@@@@@@@@@@*  +@@@.%%%%%%%%%%% 
 #%%%%%%%%%%*.@@@@@@@@@@@@@@@@@@@@@@@@@@.%%%%%%%%%%% 
 %%%%%%%%%%%* @ @@@@@@@@@@@@@@@@@@@@@# .:%%%%%%%%%%% 
 %%%%%%%%%%=.:@@@@*--:::::...::::-=#@@@@ -*%%%%%%%%% 
 %%%%%%%%*: @-@@@@@@@@@@@@@@@@@@@@@@@@@@@@ =%%%%%%%% 
 %%%%%%%=.+@@ @@@@@@@@--.    :-.@@@@@@@@-@@ :#%%%%%% 
 %%%%%#- @@@@:@@@@@@@.:@@@@@@@*. @@@@@@@@@@@+.*%%%%% 
.@%%%%+=@@@@@ @@@@@@@@ @@@@@@@@ @@@@@@@-:@@@@@:%%%%% 
 #%%%%=@@@@@. -@@@@@@@@@@@@@@@@@@@@@@@@  @@@@@:#%%%= 
  +@%%=@@@@--#- @@@@@@@@@@@@@@@@@@@@@#.++.%@@@-#%%-  
   +%%*:..:+#%%=.-@%@@@@@@@@@@@@@@@@.:*%%*-. .=%%-   
    %@%%%%%%%%%%#=: -@@@-   .*@@@:.-+%%%%%%%%%%%-    
     +-%%%%%%%%%%%%#+:.:+#%%*-..:+%%%%%%%%%%%%=.     
       .-%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%-       
         .-%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@+:        
            -#%%%%%%%%%%%%%%%%%%%%%%%%%%=:.          
               :+@%%%%%%%%%%%%%%%%%#-.               
        
    """)
        info_linha.extend([""] * 10)  
        
        # Verifica se a exibição mudou
        novo_display = "\n".join(info_linha)
        if novo_display != ExampleAgent.ultimo_display:
            
            print(novo_display)
            ExampleAgent.ultimo_display = novo_display


    def status_agente(self): ### Retorna o status do agente baseado em suas condições atuais
        
        if self.modo_desviar:
            # Verifica se o desvio ainda é necessário
            if self.target_designado and self.ray_casting(self.target_designado) < self.distancia_alerta:
                self.modo_desviar = True
                return "Evitando obstáculo"
            else:
                self.modo_desviar = False  # Sai do modo desviar
                return "Seguindo para o alvo"
            
        
        return "Sem alvo"


    def escolher_target(self): ### Escolhe o target mais próximo do agente
        
        if not self.targets:
            return None, float('inf')

        target_mais_perto = min(self.targets, key=self.calcular_distancia)
        distancia_mais_perto = self.calcular_distancia(target_mais_perto)
        return target_mais_perto, distancia_mais_perto

    def calcular_distancia(self, target): ### Calcula a distância do agente até o alvo
        
        dx = target.x - self.robot.x
        dy = target.y - self.robot.y
        return (dx**2 + dy**2)**0.5


    def designar_task(self): ### Atribui uma task ao agente, fazendo a lógica de escolher o mais perto tal

        target_mais_perto, distancia_mais_perto = self.escolher_target()
        if target_mais_perto is None:
            self.target_designado = None
            self.set_vel(Point(0, 0))
            self.set_angle_vel(0)
            return

        target_id = id(target_mais_perto)

        if target_id in ExampleAgent.distancias_agentes:
            agente_designado, distancia_designada = ExampleAgent.distancias_agentes[target_id]
            if agente_designado != self.id and distancia_mais_perto >= distancia_designada:
                self.target_designado = None
                self.set_vel(Point(0, 0))
                self.set_angle_vel(0)
                return

        if self.target_designado and self.calcular_distancia(self.target_designado) < self.margem_safe:
            target_id_to_remove = id(self.target_designado)
            if target_id_to_remove in ExampleAgent.distancias_agentes:
                del ExampleAgent.distancias_agentes[target_id_to_remove]

        ExampleAgent.distancias_agentes[target_id] = (self.id, distancia_mais_perto)
        self.target_designado = target_mais_perto

    def mover_direcao_target(self, target): ### Move o agente em direção ao alvo ou evita obstáculos se necessário
        
        obstacle_distance = self.ray_casting(target)

        if obstacle_distance:
            self.modo_desviar = True
            target_velocity, velocidade_angular_target = self.avoid_obstacle(target)
        else:
            self.modo_desviar = False
            self.velocidade_do_agente = 0.9
            target_velocity, velocidade_angular_target = Navigation.goToPoint(self.robot, target)

        velocidade_ajustada = Point(target_velocity.x * self.velocidade_do_agente, target_velocity.y * self.velocidade_do_agente)
        
        self.set_vel(velocidade_ajustada)
        self.set_angle_vel(velocidade_angular_target)

    def avoid_obstacle(self, target): ### Evita obstáculos ajustando o trajeto
       
        dx = target.x - self.robot.x
        dy = target.y - self.robot.y
       
        distance_to_target = (dx**2 + dy**2)**0.5

       
        min_distance, max_distance = self.distancia_de_evitar_range
        avoidance_distance = max(min_distance, min(max_distance, distance_to_target / 2))
       
        angulo_de_desvio = 0.70  # entre 0.6 e 0.9 está bom

        novo_target_x = self.robot.x + avoidance_distance * (angulo_de_desvio if dx >= 0 else -angulo_de_desvio)
        novo_target_y = self.robot.y + avoidance_distance * (angulo_de_desvio if dy >= 0 else -angulo_de_desvio)

        novo_target = Point(novo_target_x, novo_target_y)

        target_velocity, velocidade_angular_target = Navigation.goToPoint(self.robot, novo_target)

        if distance_to_target < self.distancia_perto_demais: # desacelerar ou velocidade normal para o agente, dependendo da distancia para o target
            self.velocidade_do_agente = 0.9
        else:
            self.velocidade_do_agente = 1.0

        velocidade_ajustada = Point( target_velocity.x * self.velocidade_do_agente, target_velocity.y * self.velocidade_do_agente,)

        return velocidade_ajustada, velocidade_angular_target

    def decision(self): ### Toma decisões...
        
        self.designar_task()
        if self.target_designado:
            self.mover_direcao_target(self.target_designado)
        self.painel_de_controle()

    def post_decision(self): ### Nao sei oque fazer aqui
        pass
