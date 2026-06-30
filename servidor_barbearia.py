import socket
import threading
import time
import random
import queue

VAGAS_ESPERA = 3
fila_espera = queue.Queue(maxsize=VAGAS_ESPERA)
barbeiro_dormindo = True

def logica_barbeiro():
    global barbeiro_dormindo
    while True:
        if fila_espera.empty():
            if not barbeiro_dormindo:
                print("\n[Barbeiro]: Não há clientes. Sentou na cadeira e começou a tirar um cochilo... Zzz...")
                barbeiro_dormindo = True
            time.sleep(1)
            continue
        
        # Puxa o cliente da fila (PRÓXIMO)
        conn_cliente, cliente_id = fila_espera.get()
        barbeiro_dormindo = False
        
        print(f"\n[Barbeiro]: Atendendo Cliente {cliente_id}...")
        
        # Simula o tempo do corte
        time.sleep(random.uniform(3, 5))
        
        print(f"[Barbeiro]: Cliente {cliente_id} finalizado.")
        try:
            conn_cliente.sendall("Corte finalizado! Obrigado.".encode())
            conn_cliente.close()
        except:
            pass
        
        print('[Barbeiro]: "PRÓXIMO!"')

def iniciar_servidor():
    global barbeiro_dormindo
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Permite rodar no mesmo PC usando localhost ou IP da rede local
    server.bind(('localhost', 12345))
    server.listen()
    
    print("=" * 45)
    print("BARBEARIA SONECA BARBER - SERVIDOR ATIVO")
    print("=" * 45)
    print("[Sistema]: Aguardando conexões de clientes na porta 12345...")
    print("[Barbeiro]: Sentou na cadeira e começou a tirar um cochilo... Zzz...")

    # Dispara a thread que simula o barbeiro trabalhando em paralelo
    threading.Thread(target=logica_barbeiro, daemon=True).start()

    while True:
        conn, addr = server.accept()
        # Recebe a mensagem inicial do cliente contendo o seu ID
        dados = conn.recv(1024).decode()
        
        if dados.startswith("CHEGOU:"):
            cliente_id = dados.split(":")[1]
            print(f"\n[Rede]: Mensagem recebida de um Cliente (ID: {cliente_id}).")
            
            if fila_espera.full():
                print(f"[Servidor]: Fila cheia! Rejeitando Cliente {cliente_id}.")
                conn.sendall("LOTADO".encode())
                conn.close()
            else:
                if barbeiro_dormindo:
                    # Envia o comando para o terminal avisando que o cliente acordou o barbeiro
                    conn.sendall("ACORDA".encode())
                else:
                    conn.sendall("AGUARDE".encode())
                
                fila_espera.put((conn, cliente_id))
                ocupadas = fila_espera.qsize()
                cadeiras = ["X" if i < ocupadas else " " for i in range(VAGAS_ESPERA)]
                print(f"[Servidor]: Cliente {cliente_id} colocado na espera: [{cadeiras[0]}] [{cadeiras[1]}] [{cadeiras[2]}]")

if __name__ == "__main__":
    iniciar_servidor()