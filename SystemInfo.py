# import psutil

# class sys_info:
# # Função para coletar as informações do sistema

#     def __init__(self):
#         self.cpu = psutil.cpu_percent(percpu=True, interval=1) # CPU em porcentagem e por nuclueo com intervalo de 1s
#         self.memory = psutil.virtual_memory() # Instância da memoria
#         self.disk = psutil.disk_usage('/') # Pasta/Instância do disco
    
#     def get_cpu_use(self):
#         return round(sum(self.cpu)/psutil.cpu_count(False), 1) # Uso de CPU em percentual (é feita a soma do uso em cada
#                                        # nucleo pois apenas o "percent" não representava corretamente)
    
#     def get_memory_use(self): 
#         return self.memory.percent # Uso de RAM em percentual

#     def get_disk_use(self): 
#         return self.disk.percent # Uso de Disco em percentual
    

#     def get_cpu_info(self):
#         return {
#             "physical_cores": psutil.cpu_count(logical=False), # Nucleos fisicos
#             "total_cores": psutil.cpu_count(logical=True), # Total de nucleos
#             "processor_speed": psutil.cpu_freq().current, # Velocidade do processador
#             "cpu_usage_per_core": dict(enumerate(self.cpu)) # Uso da CPU por nucleo
#         }
    
#     def get_memory_info(self):
#         return {
#             "total_memory": self.memory.total / (1024.0 ** 3), # Memoria total
#             "available_memory": self.memory.available / (1024.0 ** 3), # Memoria disponivel
#             "used_memory": self.memory.used / (1024.0 ** 3) # Memoria usada
#         }

#     def get_disk_info(self):
#         return {
#             "total_space": self.disk.total / (1024.0 ** 3), # Espaço total
#             "used_space": self.disk.used / (1024.0 ** 3), # Espaço usado
#             "free_space": self.disk.free / (1024.0 ** 3) # Espaço livre
#         }
    
# """
# DOCUMENTAÇÃO DE REFERÊNCIA: https://umeey.medium.com/system-monitoring-made-easy-with-pythons-psutil-library-4b9add95a443
# """

import psutil
import time


class sys_info:
    def __init__(self):
        self.previous_disk_io = psutil.disk_io_counters()
        self.previous_time = time.time()

    def update_cpu(self):
        return psutil.cpu_percent(interval=1)

    def update_memory(self):
        return psutil.virtual_memory()

    def update_disk(self):
        return psutil.disk_usage('/')

    def get_cpu_use(self):
        return psutil.cpu_percent(interval=1)
    
    def get_memory_use(self):
        memory = self.update_memory()
        return memory.percent
    
    def get_disk_use(self):
        partitions = psutil.disk_partitions()
        total_space = 0
        total_used = 0
        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                total_space += usage.total
                total_used += usage.used
            except PermissionError:
                # Ignorando partições não acessíveis
                continue
        return (total_used / total_space) * 100 if total_space > 0 else 0
    
    def get_cpu_info(self):
        return {
            "physical_cores": psutil.cpu_count(logical=False),
            "total_cores": psutil.cpu_count(logical=True),
            "processor_speed": psutil.cpu_freq().current / 1000,  # Convertendo MHz para GHz
            "base_speed": psutil.cpu_freq().max / 1000,  # Velocidade base em GHz
            "cpu_usage": self.get_cpu_use()
        }
    
    def get_memory_info(self):
        memory = self.update_memory()
        return {
            "total_memory": memory.total / (1024.0 ** 3),
            "available_memory": memory.available / (1024.0 ** 3),
            "used_memory": memory.used / (1024.0 ** 3)
        }
    
    def get_disk_info(self):
        disk = self.update_disk()
        return {
            "total_space": disk.total / (1024.0 ** 3),
            "used_space": disk.used / (1024.0 ** 3),
            "free_space": disk.free / (1024.0 ** 3)
        }

    def get_disk_io(self):
        current_disk_io = psutil.disk_io_counters()
        current_time = time.time()

        # Convertendo bytes para Kilobytes
        read_kb = current_disk_io.read_bytes / 1024
        write_kb = current_disk_io.write_bytes / 1024
        prev_read_kb = self.previous_disk_io.read_bytes / 1024
        prev_write_kb = self.previous_disk_io.write_bytes / 1024

        # Calculando a taxa de uso do disco em KB
        read_bytes = read_kb - prev_read_kb
        write_bytes = write_kb - prev_write_kb
        elapsed_time = current_time - self.previous_time

        read_rate_kb = read_bytes / elapsed_time  # Dividindo pelo tempo
        write_rate_kb = write_bytes / elapsed_time  # Dividindo pelo tempo

        # Calculando a porcentagem do tempo em que o disco está ocupado
        read_time = current_disk_io.read_time - self.previous_disk_io.read_time
        write_time = current_disk_io.write_time - self.previous_disk_io.write_time
        total_time = (current_time - self.previous_time) * 1000  # Convertendo segundos para milissegundos
        disk_busy_time = (read_time + write_time) / total_time * 100 if total_time > 0 else 0

        # Atualizando para a próxima chamada
        self.previous_disk_io = current_disk_io
        self.previous_time = current_time

        return {
            "disk_busy_time": disk_busy_time,
            "read_count": current_disk_io.read_count,
            "write_count": current_disk_io.write_count,
            "read_rate_kb": read_rate_kb,  # Taxa de leitura em KB/s
            "write_rate_kb": write_rate_kb  # Taxa de escrita em KB/s
        }

