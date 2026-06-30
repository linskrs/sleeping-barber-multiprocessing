import socket
import sys
import random
import time

def rodar_cliente(cliente_id):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 12345))
        
        # Envia mensagem inicial via rede para o servidor
        client.sendall(f"CHEGOU:{cliente_id}".encode())
        
        # Aguarda a resposta do servidor para saber o status da barbearia
        resposta = client.recv(1024).decode()
        
        if resposta == "LOTADO":
            print(f"\n[Cliente {cliente_id}]: Viu que as cadeiras estavam cheias e FOI EMBORA.")
            client.close()
            return
            
        elif resposta == "ACORDA":
            print(f'\n[Cliente {cliente_id}]: Grita "ACORDA! Hora de trabalhar seu dorminhoco!"')
            print(f"[Cliente {cliente_id}]: Sentou na cadeira de atendimento principal.")
            
        elif resposta == "AGUARDE":
            print(f"\n[Cliente {cliente_id}]: Conseguiu uma cadeira de espera. Aguardando...")

        # Aguarda o barbeiro terminar o atendimento (mensagem de finalização)
        status_final = client.recv(1024).decode()
        print(f"[Cliente {cliente_id} | Resposta do Servidor]: {status_final}")
        
    except ConnectionRefusedError:
        print("[Erro]: O servidor da barbearia não está rodando!")

if __name__ == "__main__":
    # Sorteia um ID se não for passado por argumento
    meu_id = sys.argv[1] if len(sys.argv) > 1 else str(random.randint(1, 99))
    rodar_cliente(meu_id)