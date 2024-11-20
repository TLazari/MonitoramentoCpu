import psutil 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from SystemInfo import sys_info
import time


# Intervalo de atualização dos dados (em segundos)
intervalo = 1
# Número de pontos no histórico
historico = 100  

# Configurando o gráfico
plt.rcParams['toolbar'] = 'None'
plt.style.use('dark_background')
fig, ax = plt.subplots()
ax.set_ylim(0, 100)
ax.set_xlim(0, historico)
ax.set_xlabel('Tempo')
ax.set_ylabel('Uso (%)')
ax.set_title('Uso da CPU e Memória')

linha_cpu, = ax.plot([], [], label='CPU', color='blue')
linha_memoria, = ax.plot([], [], label='Memória', color='red')

# Adicionando legenda
cpu_legenda = ax.text (0.77, 0.6, '', transform=ax.transAxes)
memoria_legenda = ax.text (0.77, 0.5, '', transform=ax.transAxes)

# Dados iniciais
dados_cpu = []
dados_memoria = []

# Função de inicialização do gráfico
def init_grafico():
    linha_cpu.set_data([], [])
    linha_memoria.set_data([], [])
    cpu_legenda.set_text('')
    memoria_legenda.set_text('')
    return linha_cpu, linha_memoria, cpu_legenda, memoria_legenda

# Função de atualização dos dados
def upd_grafico(frame):
    global dados_cpu, dados_memoria
    
    sys = sys_info()
    # Obter uso da CPU
    cpu = sys.get_cpu_use()
    # Obter uso da memória
    memoria = sys.get_memory_use()
    
    # Adicionar os dados ao histórico
    dados_cpu.append(cpu)
    dados_memoria.append(memoria)
    
    # Limitar o histórico ao número de pontos desejado
    dados_cpu = dados_cpu[-historico:]
    dados_memoria = dados_memoria[-historico:]
    
    # Atualizar os dados no gráfico
    linha_cpu.set_data(list(range(len(dados_cpu))), dados_cpu)
    linha_memoria.set_data(list(range(len(dados_memoria))), dados_memoria)

    # Atualizar a legenda
    cpu_legenda.set_text(f'CPU: {cpu:.1f}%')    
    memoria_legenda.set_text(f'Memória: {memoria:.1f}%')

    return linha_cpu, linha_memoria, cpu_legenda, memoria_legenda

# Animar o gráfico
animacao = FuncAnimation(fig, upd_grafico, init_func=init_grafico, frames=100, interval=100, blit=True) 

plt.show()