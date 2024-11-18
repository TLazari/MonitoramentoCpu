
# Monitoramento em Tempo Real de CPU e Memória  

Este projeto é uma aplicação Python que utiliza as bibliotecas **Matplotlib** e **Psutil** para monitorar e exibir o uso da CPU e memória do sistema em tempo real. O gráfico é atualizado periodicamente e mantém um histórico dos últimos valores monitorados.

## 🚀 Funcionalidades  

- Monitoramento contínuo do uso de **CPU** e **memória**.  
- Atualização do gráfico em tempo real em intervalos configuráveis.  
- Histórico configurável para exibir os últimos valores medidos.

## 🖥️ Pré-requisitos  

Certifique-se de ter o Python 3.x instalado e as seguintes bibliotecas:  

- **Matplotlib**  
- **Psutil**  

### Instalação das Dependências  

Use o **pip** para instalar as dependências:  

```bash
pip install matplotlib psutil
```

## 📄 Como Usar  

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/TLazari/MonitoramentoCpu
   cd monitoramento-monitoramentocpu
   ```

2. **Execute o script principal**:
   ```bash
   python Usage.py
   ```

3. **Configurações Personalizadas**:
   - Ajuste o intervalo de atualização e o número de pontos do histórico alterando as variáveis `intervalo` e `historico` no script:
     ```python
     intervalo = 1000  # Intervalo de atualização em ms
     historico = 50    # Quantidade de pontos no gráfico
     ```

## 🛠️ Estrutura do Código  

### Funções Principais  

- **`upd_grafico(i)`**  
  Atualiza os dados no gráfico com os valores atuais de uso de CPU e memória.  
   
- **`init_grafico()`**  
  Configura os eixos e os elementos iniciais do gráfico.

### Animação  

A função `FuncAnimation` do Matplotlib é usada para animar o gráfico, atualizando-o em intervalos definidos.  

```python
from matplotlib.animation import FuncAnimation
animacao = FuncAnimation(fig, upd_grafico, init_func=init_grafico, frames=100, interval=1000, blit=True)
```

## 🌟 Demonstração  

A aplicação exibe algo assim durante a execução:

![Demonstração do Gráfico](https://via.placeholder.com/800x400?text=CPU+%26+Memory+Monitor)  

## 📂 Estrutura do Projeto  

```plaintext
├── Usage.py     # Script principal
├── README.md            # Instruções do projeto
```


👨‍💻 **Contribuições são bem-vindas!** Sinta-se à vontade para abrir issues ou enviar pull requests.

👨‍💻 **Projeto Desenvolvido para Faculdade UFBRA matéria Sistema Operacionais** 



