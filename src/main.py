import time
import threading
from classes import Block, Blockchain

# Cria uma Blockchain com o nível de dificuldade para o hashing
def create_blockchain(difficulty):
    return Blockchain(difficulty=difficulty)

def sequential_mining(fakechain: Blockchain, new_block: Block):
    start_time = time.time()
    fakechain.add_block(new_block)
    elapsed_time = time.time() - start_time
    print(f"\nMineracao sequencial concluida em {elapsed_time:.2f} segundos.")
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
    print(f"\nMineracao com {num_threads} threads concluida em {elapsed_time:.2f} segundos.")
    return elapsed_time

# Ponto de entrada principal
if __name__ == "__main__":
    # Escolhendo nivel de dificuldade (0's) e numero de Threads que irão trabalhar
    difficulty = 5
    n_threads = [2, 4, 8, 16]
    concurrent_times = [] 
    sequential_times = []

    # Criando Blockchain e o bloco inicial (Optamos por inserir o tipo sempre que for a classe para ajudar no autocomplete dos métodos)
    concurret_chain: Blockchain = create_blockchain(difficulty)
    sequential_chain: Blockchain = create_blockchain(difficulty)

    print("===== Mineração Concorrente =====\n")
    for i, count in enumerate(n_threads):
        latest_block: Block = concurret_chain.get_latest_block()
        new_block = Block(
            index=i+1, 
            previous_hash = latest_block.hash, 
            timestamp = time.time(),
            data = str(i*1000)
        )
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

    print("\nValidação das blockchains:")
    print(f"Concorrente válida? {concurret_chain.validating_blockchain()}")
    print(f"Sequencial válida? {sequential_chain.validating_blockchain()}")
    print("\nComparativo entre as minerações:")
    print(f"Concorrente: {concurrent_times} - Total : {sum(concurrent_times):.2f}")
    print(f"Sequencial: {sequential_times} - Total : {sum(sequential_times):.2f}")