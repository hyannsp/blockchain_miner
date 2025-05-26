import time
import threading
import matplotlib.pyplot as plt
from classes import Block, Blockchain

# Cria uma Blockchain com o nível de dificuldade para o hashing
def create_blockchain(difficulty):
    return Blockchain(difficulty=difficulty)

def sequential_mining(fakechain: Blockchain, new_block: Block):
    start_time = time.time()
    fakechain.add_block(new_block)
    elapsed_time = time.time() - start_time
    print(f"Mineracao sequencial concluida em {elapsed_time:.2f} segundos.\n")
    return elapsed_time

def concurrent_mining(fakechain: Blockchain, new_block: Block, num_threads):
    stop_event = threading.Event()
    minered_blocks = [None]
    def mine():
        # Cada thread trabalha em uma cópia para evitar condição de corrida no nonce
        local_block = Block(
            new_block.index,
            new_block.previous_hash,
            new_block.timestamp,
            new_block.data
        )
        # fakechain.add_block(local_block) duplicaria os resultados por quantidade de threads
        local_block.mine_block(fakechain.get_difficulty(), stop_event)
        if not stop_event.is_set():
            minered_blocks[0] = local_block
            stop_event.set()

    threads = []
    start_time = time.time()

    for _ in range(num_threads):
        t = threading.Thread(target=mine)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
    
    # Adicionando o bloco minerado à chain
    if minered_blocks[0]:
        fakechain.chain.append(minered_blocks[0])


    elapsed_time = time.time() - start_time
    print(f"Mineracao com {num_threads} threads concluida em {elapsed_time:.2f} segundos.\n")
    return elapsed_time

def blockchain_miner(n_threads):
    concurrent_times = [] 
    sequential_times = []

    print("===== Mineração com Multiplas Threads =====\n")
    for i, count in enumerate(n_threads):
        latest_block: Block = concurret_chain.get_latest_block() # Captura o ultimo bloco da blockchain para inserir os dados do novo bloco

        # Define novo Bloco
        new_block = Block(
            index=i+1, 
            previous_hash = latest_block.hash, 
            timestamp = time.time(),
            data = str(i*1000)
        ) 

        # Minera o novo bloco de maneira concorrente e retorna o tempo, adicionando-o na blockchain e o tempo na lista de tempos
        elapsed_time = concurrent_mining(fakechain=concurret_chain,new_block=new_block ,num_threads=count) 
        concurrent_times.append(elapsed_time)

    print("===== Mineração Sequencial =====\n")
    for i, _ in enumerate(n_threads):
        latest_block: Block = sequential_chain.get_latest_block()
        new_block = Block(
            index=i+1, 
            previous_hash = latest_block.hash, 
            timestamp = time.time(),
            data = str(i*1000)
        )
        elapsed_time = sequential_mining(fakechain=sequential_chain, new_block=new_block )
        sequential_times.append(elapsed_time)
    return concurrent_times, sequential_times

def graph_view(concurrent_times, sequential_times, n_threads):
    n_blocks = list(range(1, len(n_threads) + 1))

    # Tempo acumulado por bloco (concorrente e sequencial)
    concurrent_agg = [sum(concurrent_times[:i+1]) for i in range(len(concurrent_times))]
    sequential_agg = [sum(sequential_times[:i+1]) for i in range(len(sequential_times))]

    # ======== GRÁFICO 1 ========
    plt.figure(figsize=(10, 6))
    plt.plot(n_threads, concurrent_times, marker='o', color='blue', label='Concorrente')

    for x, y in zip(n_threads, concurrent_times):
        plt.text(x, y, f'{y:.2f}s', ha='right', va='bottom', fontsize=9)

    plt.xlabel('Número de Threads')
    plt.ylabel('Tempo de Mineração (s)')
    plt.title('Mineração Concorrente: Threads vs Tempo')
    plt.grid(True)
    plt.legend()
    plt.savefig('./output/concorrente_por_thread.png')

    # ======== GRÁFICO 2 ========
    plt.figure(figsize=(10, 6))
    plt.plot(n_blocks, concurrent_agg, marker='o', label='Concorrente', color='blue')
    plt.plot(n_blocks, sequential_agg, marker='o', label='Sequencial', color='red')

    for x, y in zip(n_blocks, concurrent_agg):
        plt.text(x, y, f'{y:.2f}s', ha='right', va='bottom', fontsize=9, color='blue')

    for x, y in zip(n_blocks, sequential_agg):
        plt.text(x, y, f'{y:.2f}s', ha='left', va='top', fontsize=9, color='red')

    plt.xlabel('Número de Blocos Adicionados')
    plt.ylabel('Tempo Acumulado (s)')
    plt.title('Tempo Acumulado por Bloco')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.savefig('./output/comparativo_mineração.png')
    return

# Ponto de entrada principal
if __name__ == "__main__":
    # Escolhendo nivel de dificuldade (0's) e numero de Threads que irão trabalhar
    difficulty = 5
    n_threads = [1, 2, 4, 8]

    # Criando Blockchain e o bloco inicial (Optamos por inserir o tipo sempre que for a classe para ajudar no autocomplete dos métodos)
    concurret_chain: Blockchain = create_blockchain(difficulty)
    sequential_chain: Blockchain = create_blockchain(difficulty)

    concurrent_times, sequential_times = blockchain_miner(n_threads)

    print("\nValidação das blockchains:")
    print(f"Concorrente válida? {concurret_chain.validating_blockchain()}")
    print(f"Sequencial válida? {sequential_chain.validating_blockchain()}")

    print("\nComparativo entre as minerações:")
    print(f"Concorrente: {concurrent_times} - Total : {sum(concurrent_times):.2f}")
    print(f"Sequencial: {sequential_times} - Total : {sum(sequential_times):.2f}")

    print("\nVisualização dos Gráficos disponíveis em ./output/")
    graph_view(concurrent_times, sequential_times, n_threads)