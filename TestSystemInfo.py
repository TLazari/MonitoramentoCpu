import time
import threading
import os
from SystemInfo import sys_info


# # Função para coletar as informações do sistema
# def get_system_usage():
#     sys = sys_info() # Usando a classe de systemInformation
#     return {
#         'cpu_percent': sys.get_cpu_use(),
#         'memory_percent': sys.get_memory_use(),
#         'disk_percent': sys.get_disk_use()

#     }

# # Função para imprimir os dados no terminal a cada 2 segundos
# def print_usage_terminal():
#     while True:
#         usage = get_system_usage()
#         os.system('cls')
#         print(f"CPU: {usage['cpu_percent']}% | RAM: {usage['memory_percent']}% | Disco: {usage['disk_percent']}%")
#         #time.sleep(1) #Intervalo entre atulizações em segundos

# if __name__ == '__main__':
#     # Iniciando a thread que vai imprimir as informações no terminal
#     terminal_thread = threading.Thread(target=print_usage_terminal)
#     terminal_thread.daemon = True  # Para garantir que a thread seja encerrada ao fechar o programa
#     terminal_thread.start()
#     terminal_thread.join()


def get_system_usage():
    sys = sys_info()
    return {
        'cpu_percent': sys.get_cpu_use(),
        'cpu_info': sys.get_cpu_info(),
        'memory_percent': sys.get_memory_use(),
        'disk_percent': sys.get_disk_use(),
        'disk_io': sys.get_disk_io()
    }

def print_usage_terminal():
    while not exit_flag:
        usage = get_system_usage()
        os.system('cls' if os.name == 'nt' else 'clear')
        cpu_info = usage.get('cpu_info', {})
        disk_io = usage.get('disk_io', {})
        print(f"CPU: {usage['cpu_percent']}% | Velocidade atual: {cpu_info.get('processor_speed', 0):.2f} GHz | Velocidade base: {cpu_info.get('base_speed', 0):.2f} GHz")
        print(f"RAM: {usage['memory_percent']}% | Disco: {usage['disk_percent']:.2f}%")
        print(f"Taxa de leitura: {disk_io.get('read_rate_kb', 0):.2f} KB/s | Taxa de gravação: {disk_io.get('write_rate_kb', 0):.2f} KB/s")
        print(f"Tempo de atividade do Disco: {disk_io.get('disk_busy_time', 0):.2f}%") #Kb/s
        print(f"Total de leituras: {disk_io.get('read_count', 0)} | Total de escritas: {disk_io.get('write_count', 0)}")
        time.sleep(1)
    print("Programa encerrado pelo usuário.")

# Função para monitorar a entrada do usuário
def check_for_exit():
    global exit_flag
    input("Pressione 'q' e Enter para encerrar o programa.\n")
    exit_flag = True

if __name__ == '__main__':
    exit_flag = False

    # Iniciando a thread que vai imprimir as informações no terminal
    terminal_thread = threading.Thread(target=print_usage_terminal)
    terminal_thread.daemon = True
    terminal_thread.start()

    # Iniciando a thread para verificar a entrada do usuário
    exit_thread = threading.Thread(target=check_for_exit)
    exit_thread.daemon = True
    exit_thread.start()

    terminal_thread.join()