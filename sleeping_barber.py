import multiprocessing
import time
import random
import os
from queue import Empty, Full

# quantidade de cadeiras de espera
VAGAS_ESPERA = 3

# total de clientes da simulação
TOTAL_CLIENTES = 10


def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


def mostrar_status(ocupadas):
    # mostra cadeiras ocupadas
    cadeiras = ["X" if i < ocupadas else " " for i in range(VAGAS_ESPERA)]
    print(f"Espera: [{cadeiras[0]}] [{cadeiras[1]}] [{cadeiras[2]}]")


def barbeiro(fila_espera, encerrado):
    # processo do barbeiro
    while True:
        try:
            print("\nBarbeiro dormindo...")

            # espera cliente entrar na fila
            cliente_id = fila_espera.get(timeout=3)

            print(f"\nAtendendo Cliente {cliente_id}...")
            time.sleep(random.uniform(2, 4))

            print(f"Cliente {cliente_id} finalizado.")
            print("PRÓXIMO!\n")

        except Empty:
            # encerra quando não houver mais clientes
            if encerrado.value == 1 and fila_espera.empty():
                print("\nBarbearia encerrando...")
                break


def cliente(id_cliente, fila_espera):
    # processo de cada cliente
    print(f"\nCliente {id_cliente} chegou.")

    try:
        # tenta sentar na espera
        fila_espera.put_nowait(id_cliente)

        ocupadas = fila_espera.qsize()
        print(f"Cliente {id_cliente} aguardando.")
        mostrar_status(ocupadas)

    except Full:
        print(f"Cliente {id_cliente} foi embora. Sem vagas.")


def main():
    limpar_tela()

    print("=" * 45)
    print("BARBEARIA SONECA")
    print("=" * 45)

    # fila representa as cadeiras de espera
    fila_espera = multiprocessing.Queue(maxsize=VAGAS_ESPERA)

    # controla encerramento do sistema
    encerrado = multiprocessing.Value('i', 0)

    # inicia barbeiro
    proc_barbeiro = multiprocessing.Process(
        target=barbeiro,
        args=(fila_espera, encerrado)
    )
    proc_barbeiro.start()

    processos_clientes = []

    # cria clientes em tempos aleatórios
    for i in range(1, TOTAL_CLIENTES + 1):
        time.sleep(random.uniform(0.5, 2.5))

        p = multiprocessing.Process(
            target=cliente,
            args=(i, fila_espera)
        )

        p.start()
        processos_clientes.append(p)

    # espera todos clientes terminarem
    for p in processos_clientes:
        p.join()

    # avisa que não chegarão mais clientes
    encerrado.value = 1

    # espera barbeiro finalizar
    proc_barbeiro.join()

    print("\nSistema finalizado.")


if __name__ == '__main__':
    main()