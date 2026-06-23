# 💈 O Problema da Barbearia Soneca (Sleeping Barber Problem)

Este repositório contém uma implementação robusta e concorrente do clássico problema de sincronização de processos proposto por Edsger Dijkstra, desenvolvido como trabalho prático para a disciplina de **Sistemas Distribuídos**.

A aplicação utiliza o paradigma de **Troca de Mensagens (Inter-Process Communication - IPC)** por meio da biblioteca nativa `multiprocessing` do Python, simulando o comportamento de sistemas concorrentes reais de forma isolada e segura.

---

## 🎯 Cenário da Simulação

A barbearia possui regras estritas de funcionamento e capacidade limitada:
* **Capacidade**: 1 Barbeiro, 1 Cadeira de Atendimento e 3 Cadeiras de Espera (`VAGAS_ESPERA = 3`).
* **O Barbeiro (Consumidor)**: Se não há clientes na fila, ele entra em estado de bloqueio (dorme). Quando um cliente chega, ele consome a requisição e inicia o corte.
* **Os Clientes (Produtores)**: Chegam em intervalos assíncronos e aleatórios. Se houver cadeira vazia, eles sentam e aguardam. Se as 3 cadeiras estiverem ocupadas, eles vão embora imediatamente por falta de vagas.

---

## 🛠️ Tecnologias e Conceitos Aplicados

* **Python 3**: Linguagem base do projeto.
* **`multiprocessing.Process`**: Garante o paralelismo real utilizando múltiplos núcleos da CPU, isolando o espaço de memória de cada cliente e do barbeiro.
* **`multiprocessing.Queue`**: Funciona como o canal seguro de comunicação e armazenamento das mensagens (as cadeiras de espera), impedindo condições de corrida (*Race Conditions*) de forma atômica.
* **`multiprocessing.Value`**: Memória compartilhada segura controlada pelo Sistema Operacional para sinalizar de forma coordenada o encerramento gracioso das atividades.

---

## 📂 Estrutura do Código

O programa divide-se em funções limpas e de responsabilidades isoladas:
* `barbeiro(fila_espera, encerrado)`: Loop infinito que realiza a leitura da fila usando `get(timeout=3)`. Se estourar o tempo limite e a flag de encerramento estiver ativa, finaliza o processo.
* `cliente(id_cliente, fila_espera)`: Tenta inserir o identificador do cliente na fila por meio do método não-bloqueante `put_nowait()`. Trata a exceção `Full` caso o buffer atinja o limite máximo.
* `mostrar_status(ocupadas)`: Atualiza graficamente o terminal mostrando quais cadeiras de espera estão em uso (ex: `[X] [ ] [ ]`).
* `main()`: Gerencia o ciclo de vida e a sincronização do término dos processos filhos através do método `join()`.

---

## 🚀 Como Executar

### Pré-requisitos
* Python 3.x instalado.
* Sistema Operacional Windows, Linux ou macOS (o código implementa a diretiva `if __name__ == '__main__':` necessária para a portabilidade via método *spawn* no Windows).

### Execução no Terminal
1. Clone o repositório ou baixe o arquivo fonte.
2. Abra o terminal na pasta do arquivo e digite:
   ```bash
   python sleeping_barber.py