# thread_miner.py
import hashlib
import time
import threading
from classes.Block import Block

# Funcao para mineracao concorrente com multiplas threads
def concurrent_mining(num_threads, difficulty):
    latest_block = Block(1, "0", time.time(), "Bloco concorrente")
    stop_event = threading.Event()

    def mine():
        block_copy = Block(latest_block.index, latest_block.previous_hash, latest_block.timestamp, latest_block.data)
        block_copy.mine_block(difficulty, stop_event)

    threads = []
    start_time = time.time()

    for _ in range(num_threads):
        t = threading.Thread(target=mine)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    elapsed_time = time.time() - start_time
    print(f"\nMineracao com {num_threads} threads concluida em {elapsed_time:.2f} segundos.")

# Ponto de entrada principal
if __name__ == "__main__":
    # Altere os parametros para testar diferentes numeros de threads
    num_threads = [2, 4, 8, 16]
    concurrent_mining(num_threads=4, difficulty=4)