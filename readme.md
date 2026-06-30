# 💈 Sleeping Barber

Este repositório contém a implementação concorrente e distribuída do clássico problema de sincronização do **Barbeiro Dorminhoco (Sleeping Barber)**, desenvolvido como trabalho prático para a disciplina de **Sistemas Distribuídos**.

A arquitetura foi modelada seguindo o paradigma de **Cliente/Servidor**, realizando a **Troca de Mensagens (Inter-Process Communication - IPC)** através de **Sockets TCP/IP** nativos do Python. Cada cliente disparado roda em um processo independente no Sistema Operacional, comunicando-se com o servidor por meio da rede local.

---

# 🎯 Cenário da Simulação e Regras de Negócio

A barbearia possui regras estritas de funcionamento e capacidade limitada:

- **Capacidade:** 1 Barbeiro, 1 Cadeira de Atendimento e 3 Cadeiras de Espera (`VAGAS_ESPERA = 3`).
- **O Barbeiro (Servidor):** Fica em estado de bloqueio (dormindo) se não houver conexões na fila. Quando um cliente se conecta, ele sai do bloqueio, assume o atendimento e, ao finalizar, chama o **"PRÓXIMO!"**.
- **Os Clientes (Processos Externos):** Conectam-se de forma assíncrona. Se houver cadeira vazia, entram na fila de espera. Se as 3 cadeiras estiverem cheias, recebem o comando `LOTADO` via rede e vão embora imediatamente. O primeiro cliente a chegar acorda o barbeiro com o grito:

> **"ACORDA! Hora de trabalhar seu dorminhoco!"**

---

# 🛠️ Tecnologias e Conceitos Aplicados

- **Sockets TCP/IP (`socket`)**
  - Canal de comunicação orientado à conexão utilizando `AF_INET` e `SOCK_STREAM` para tráfego seguro de mensagens em bytes entre processos.

- **Multi-Threading (`threading`)**
  - Utilizado no servidor para isolar a função `logica_barbeiro()` da thread principal que escuta a rede (`server.accept()`), permitindo concorrência real.

- **Fila Sincronizada (`queue.Queue`)**
  - Buffer *thread-safe* que gerencia as 3 cadeiras de espera e armazena os descritores de arquivos de conexão (`conn`) dos clientes.

---

# 📂 Estrutura dos Arquivos

| Arquivo | Descrição |
|----------|-----------|
| **`servidor_barbearia.py`** | Nó centralizado (Servidor). Abre a porta TCP `12345` em `localhost`, gerencia o estado do barbeiro em uma thread paralela e controla as vagas de espera. |
| **`cliente_processo.py`** | Script cliente. Cada execução cria um processo independente (com PID próprio) que se conecta ao servidor para solicitar atendimento. |

---

# 🚀 Como Executar a Simulação

Para simular o sistema distribuído, abra **múltiplos terminais** no computador.

## 1️⃣ Iniciar o Servidor (A Barbearia)

No **Terminal 1**, navegue até a pasta do projeto e execute:

```bash
python servidor_barbearia.py
```

O console indicará que o servidor está ativo e o barbeiro começará dormindo.

---

## 2️⃣ Disparar os Clientes (Processos Independentes)

Abra novos terminais e execute o cliente passando um identificador como argumento.

### Terminal 2 (Cliente 1 — Acorda o barbeiro)

```bash
python cliente_processo.py 1
```

### Terminal 3 (Cliente 2 — Entra na fila)

```bash
python cliente_processo.py 2
```

### Terminal 4 (Cliente 3 — Entra na fila)

```bash
python cliente_processo.py 3
```

Você pode continuar abrindo novos terminais para simular mais clientes simultaneamente.

---

# 📊 Demonstração das Situações Exigidas

O sistema demonstra em tempo real as três situações obrigatórias do problema.

## 💤 1. Abertura da Barbearia

O servidor inicia exibindo que:

- as cadeiras estão vazias;
- o barbeiro está dormindo (`Zzz...`).

Exemplo:

```text
💈 Barbearia aberta!
😴 Barbeiro dormindo... Zzz...
```

---

## ✂️ 2. Atendimento com Fila Ocupada

Quando o primeiro cliente chega:

- acorda o barbeiro;
- inicia o corte;
- os próximos clientes ocupam as cadeiras de espera.

Exemplo:

```text
Cliente 1: "ACORDA! Hora de trabalhar seu dorminhoco!"

[Servidor]
Fila:
[X] [ ] [ ]

Barbeiro cortando o cabelo do Cliente 1...

Novo cliente chegou.

Fila:
[X] [X] [ ]
```

---

## 🚫 3. Cliente Vai Embora por Lotação

Quando todas as cadeiras de espera estão ocupadas:

```text
Fila:
[X] [X] [X]
```

o próximo cliente recebe via socket o status:

```text
LOTADO
```

e encerra sua execução.

Exemplo:

```text
Cliente 7:
❌ Barbearia lotada.
Indo embora...
```

---

# ✅ Resumo da Arquitetura

```text
                 +----------------------+
                 | Servidor Barbearia   |
                 |  (Barbeiro)          |
                 |----------------------|
                 | Thread Principal     |
                 | aceita conexões TCP  |
                 |                      |
                 | Thread Barbeiro      |
                 | atende clientes      |
                 +----------+-----------+
                            │
                     Socket TCP/IP
                            │
        ┌──────────────┬──────────────┬──────────────┐
        │              │              │
   Cliente 1      Cliente 2      Cliente 3
  (Processo)      (Processo)      (Processo)
```