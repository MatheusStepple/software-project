### 💚🚀 Seletiva RoboCIn 2025 - Software 🚀💚

# Meu projeto de Agente Robô com Desvio de Obstáculos e Atribuição de Tarefas 🚀💚



## 📋 Descrição Geral
Este projeto implementa um sistema dinâmico e em tempo real para controle do "cérebro" de agentes robóticos em um ambiente simulado. Utilizando técnicas personalizadas de navegação, como **Ray Casting**, o sistema permite que os agentes detectem e evitem obstáculos enquanto realizam tarefas específicas, como alcançar destinos de maneira eficiente e coordenada.

---

## ⚙️ Funcionalidades
- **Navegação com Evitação de Obstáculos**:
  - Utiliza **Ray Casting** para detectar obstáculos e calcular desvios baseados em ângulos e distâncias.
- **Atribuição de Tarefas**:
  - Os agentes são designados ao destino mais próximo, garantindo exclusividade de tarefas.
- **Adaptação em Tempo Real**:
  - Sistema ajusta rotas dinamicamente conforme mudanças no ambiente, incluindo posicionamento de obstáculos e destinos.
- **Integração Simulada**:
  - Baseado em bibliotecas como `gymnasium`, `rsoccer_gym` e `pygame`.

---

## 🧠 Algoritmo Principal: Ray Casting
- **Conceito**:
  - Inspiração no conceito de "ver" antes de "agir".
  - Simula raios emitidos pelo agente em direção ao alvo para identificar obstáculos no caminho.
- **Características**:
  - Calcula distância até os obstáculos e ajusta o ângulo para evitar colisões.
  - Baseado em trigonometria para movimentos precisos.

---

## 🏗️ Estrutura do Projeto
- **`agent.py`**:
  - Código principal do agente, incluindo lógica de desvio e designação de tarefas.
- **`utils/`**:
  - Utilitário para armazenar dados históricos, como trajetórias e estados.
- **Simuladores**:
  - Integração com simulações baseadas em `rsoccer_gym` e `gymnasium`.

---

## 🛠️ Tecnologias Utilizadas
- **Python**:
  - Linguagem principal para desenvolvimento.
- **Bibliotecas**:
  - `gymnasium` para simulações dinâmicas.
  - `rsoccer_gym` para controle robótico.
  - `pygame` para manipulação de eventos.
- **Algoritmos**:
  - "Ray Casting" e lógica personalizada para desvio de obstáculos.
  - Atribuição de tarefas com base na distância.

---

## 🚀 Melhorias e Implementações Futuras
- **Aprimoramento da Navegação**:
  - Implementar técnicas mais robustas para desvio de obstáculos
- **Algoritmos**:
  - **Otimização do Ray Casting**:
    - Reduzir consumo de recursos ajustando número de raios e intervalos angulares.
    - Implementar verificação em níveis hierárquicos para detectar obstáculos em diferentes escalas.
  - **Atribuição de Tarefas Avançada**:
    - Usar algoritmos como **Hungarian Algorithm** para designação ótima em ambientes multiagentes.
    - Implementar lógica de reassigmento para reagir rapidamente a mudanças no ambiente.
- **Integração Multiagentes**:
  - Criar coordenação colaborativa entre agentes para evitar conflitos de rota e melhorar eficiência.
  - Melhorar a capacidade de troca de informações entre agentes.
- **Visualização e Feedback**:
  - Melhorar interface visual com indicadores de estado do agente (ex. trajetórias planejadas e ângulos de Ray Casting).
  - Melhorar o feedback em tempo real no ambiente para depuração e análise de desempenho.
- **Suporte a Hardware Real**:
  - Preparar o código para integração com robôs físicos, incluindo bibliotecas de controle como `ROS` e sensores reais como LIDAR.


---

## 🚀 Como Usar
1. **Instale as Dependências**:
   ```bash
   pip install -r requirements.txt
2. **Inicie o arquivo do start.py com a dificuldade 1-4**:
   ```bash
   python3 start.py -d 1
