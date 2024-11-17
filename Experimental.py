import psutil
import tkinter as tk
import pyqtgraph as pg
from tkinter import ttk
import numpy as np

# Listas para armazenar os dados históricos para plotagem
cpu_data = []
ram_data = []
disco_data = []
time_data = []

# Função para atualizar os dados de uso
def atualizar_dados():
    cpu = psutil.cpu_percent(interval=1)  # Uso da CPU em percentual
    ram = psutil.virtual_memory().percent  # Uso da RAM em percentual
    disco = psutil.disk_usage('/').percent  # Uso do disco em percentual

    # Adicionar os dados nas listas
    cpu_data.append(cpu)
    ram_data.append(ram)
    disco_data.append(disco)
    time_data.append(len(time_data))  # Usar o índice como tempo

    # Limitar o número de pontos exibidos
    max_data_points = 50
    if len(cpu_data) > max_data_points:
        cpu_data.pop(0)
        ram_data.pop(0)
        disco_data.pop(0)
        time_data.pop(0)

    # Atualizar os valores na interface
    label_cpu.config(text=f'CPU: {cpu}%')
    label_ram.config(text=f'RAM: {ram}%')
    label_disco.config(text=f'Disco: {disco}%')

    # Passar os dados corretamente para o gráfico
    plot_cpu.setData(np.array(time_data), np.array(cpu_data))
    plot_ram.setData(np.array(time_data), np.array(ram_data))
    plot_disco.setData(np.array(time_data), np.array(disco_data))

    # Chamar a função novamente após 1000ms (1 segundo)
    root.after(1000, atualizar_dados)

# Criando a interface gráfica
root = tk.Tk()
root.title("Monitor de Sistema")

# Labels para mostrar os valores de uso
label_cpu = ttk.Label(root, text="CPU: 0%", font=("Arial", 14))
label_cpu.pack(pady=10)

label_ram = ttk.Label(root, text="RAM: 0%", font=("Arial", 14))
label_ram.pack(pady=10)

label_disco = ttk.Label(root, text="Disco: 0%", font=("Arial", 14))
label_disco.pack(pady=10)

# Criando a área de gráficos com PyQtGraph
graphicsView = pg.GraphicsLayoutWidget()
graphicsView.show()
graphicsView.setWindowTitle('Gráficos de Uso')

# Gráficos
plot_cpu = graphicsView.addPlot(title="Uso da CPU")
plot_cpu.setLabel('left', 'Uso (%)')
plot_cpu.setLabel('bottom', 'Tempo')
plot_cpu.setYRange(0, 100)

plot_ram = graphicsView.addPlot(title="Uso da RAM")
plot_ram.setLabel('left', 'Uso (%)')
plot_ram.setLabel('bottom', 'Tempo')
plot_ram.setYRange(0, 100)

plot_disco = graphicsView.addPlot(title="Uso do Disco")
plot_disco.setLabel('left', 'Uso (%)')
plot_disco.setLabel('bottom', 'Tempo')
plot_disco.setYRange(0, 100)

# Função de atualização dos dados
atualizar_dados()

# Rodar a interface Tkinter
root.mainloop()
