import psutil 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

intervalo = 1

# Configurando o gráfico
fig, ax = plt.subplots()
ax.set_ylim(0, 100)
ax.set_xlim(0, 100)
ax.set_xlabel('Tempo')
ax.set_ylabel('Uso (%)')
ax.set_title('Uso da CPU e Memória')

linha_cpu, = ax.plot([], [], label='CPU', color='blue')
linha_memoria, = ax.plot([], [], label='Memória', color='red')

# Adicionando legenda
cpu_legenda = ax.text (0.77, 0.6, '', transform=ax.transAxes)
memoria_legenda = ax.text (0.77, 0.5, '', transform=ax.transAxes)

# Função de atualização dos dados
def upd_grafico (frame):
    #Obter uso da CPU
    cpu = psutil.cpu_percent(interval=intervalo)
    #Obter uso da memória
    memoria = psutil.virtual_memory().percent
    
    #Adicionar os dados ao gráfico
    linha_cpu.set_data(list(range(frame)), [cpu]*frame)
    linha_memoria.set_data(list(range(frame)), [memoria]*frame)

    #Atualizar a legenda
    cpu_legenda.set_text(f'CPU: {cpu:.1f}%')    
    memoria_legenda.set_text(f'Memória: {memoria:.1f}%')

    return linha_cpu, linha_memoria, cpu_legenda, memoria_legenda

#Animar o gráfico
animacao = FuncAnimation(fig, upd_grafico, frames=100, interval= 10000, blit=True) 

print(f'Uso da CPU em percentual: {linha_cpu} % e Uso da RAM em percentual: {linha_memoria} %')

plt.show()

