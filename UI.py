import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from SystemInfo import sys_info


# Intervalo de atualização dos dados (em segundos)
intervalo = 1
# Número de pontos no histórico
historico = 100  

# Configurando os gráficos
plt.rcParams['toolbar'] = 'None'
plt.style.use('dark_background')
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)

# Configurações do primeiro gráfico (CPU)
ax1.set_ylim(0, 100)
ax1.set_xlim(0, historico)
ax1.set_xlabel('Tempo')
ax1.set_title('Uso da CPU (%)')

linha_cpu1, = ax1.plot([], [], label='CPU', color='blue')

# Configurações do segundo gráfico (Memória)
ax2.set_ylim(0, 100)
ax2.set_xlim(0, historico)
ax2.set_xlabel('Tempo')
ax2.set_title('Uso da Memória (%)')

linha_memoria1, = ax2.plot([], [], label='Memória', color='red')

# Configurações do terceiro gráfico (Disco)
ax3.set_ylim(0, 100)  # Ajuste os limites de acordo com sua necessidade
ax3.set_xlim(0, historico)
ax3.set_xlabel('Tempo')
ax3.set_title('Uso do Disco Escrita e Leitura (MB/s)')

linha_disco1, = ax3.plot([], [], label='Disco Gravação', color='green')
linha_disco2, = ax3.plot([], [], label='Disco Leitura', color='yellow')

# Adicionando legendas
cpu_legenda1 = ax1.text(0.77, 0.6, '', transform=ax1.transAxes)
memoria_legenda1 = ax2.text(0.77, 0.6, '', transform=ax2.transAxes)
disco_legenda1 = ax3.text(0.77, 0.6, '', transform=ax3.transAxes)

# Dados iniciais
dados_cpu = []
dados_memoria = []
dados_disco_write = []
dados_disco_read = []

def get_system_usage():
    sys = sys_info()
    return {
        'cpu_percent': sys.get_cpu_use(),
        'cpu_info': sys.get_cpu_info(),
        'memory_percent': sys.get_memory_use(),
        'disk_percent': sys.get_disk_use(),
        'disk_io': sys.get_disk_io()
    }

# Função de inicialização dos gráficos
def init_grafico():
    linha_cpu1.set_data([], [])
    linha_memoria1.set_data([], [])
    linha_disco1.set_data([], [])
    linha_disco2.set_data([], [])
    cpu_legenda1.set_text('')
    memoria_legenda1.set_text('')
    disco_legenda1.set_text('')

    return (linha_cpu1, linha_memoria1, linha_disco1, linha_disco2, cpu_legenda1, memoria_legenda1, disco_legenda1)

def upd_grafico(frame):
    global dados_cpu, dados_memoria, dados_disco_write, dados_disco_read  # Variáveis globais
    
    sys = sys_info()
    # Obter uso da CPU
    cpu = sys.get_cpu_use()
    # Obter uso da memória
    memoria = sys.get_memory_use()
    # Obter uso do disco
    disco = sys.get_disk_io()
    disco_write = disco.get('write_rate_kb') / 1024  # Converter de KB para MB
    disco_read = disco.get('read_rate_kb') / 1024  # Converter de KB para MB
    
    # Adicionar os dados ao histórico
    dados_cpu.append(cpu)
    dados_memoria.append(memoria)
    dados_disco_write.append(disco_write)
    dados_disco_read.append(disco_read)
    
    # Limitar o histórico ao número de pontos desejado
    dados_cpu = dados_cpu[-historico:]
    dados_memoria = dados_memoria[-historico:]
    dados_disco_write = dados_disco_write[-historico:]
    dados_disco_read = dados_disco_read[-historico:]

    # Atualizar os dados no gráfico de CPU
    linha_cpu1.set_data(list(range(len(dados_cpu))), dados_cpu)

    # Atualizar os dados no gráfico de Memória
    linha_memoria1.set_data(list(range(len(dados_memoria))), dados_memoria)

    # Atualizar os dados no gráfico de Disco
    linha_disco1.set_data(list(range(len(dados_disco_write))), dados_disco_write)  # Gravação
    linha_disco2.set_data(list(range(len(dados_disco_read))), dados_disco_read)  # Leitura

    # Atualizar as legendas
    cpu_legenda1.set_text(f'CPU: {cpu}%')
    memoria_legenda1.set_text(f'Memória: {memoria}%')
    disco_legenda1.set_text(f'W: {disco_write:.2f} MB/s\n R: {disco_read:.2f} MB/s')


    return (linha_cpu1, linha_memoria1, linha_disco1, linha_disco2, cpu_legenda1, memoria_legenda1, disco_legenda1)

# Animar os gráficos
animacao = FuncAnimation(fig, upd_grafico, init_func=init_grafico, frames=100, interval=intervalo, blit=True)

fig.subplots_adjust(hspace=0.7)
plt.show()
