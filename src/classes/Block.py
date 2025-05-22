import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, data, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.hash = self.calculate_hash()

    # Funcao que calcula o hash do bloco
    def calculate_hash(self):
        value = str(self.index) + self.previous_hash + str(self.timestamp) + self.data + str(self.nonce)
        return hashlib.sha256(value.encode()).hexdigest()
    
    # Funcao que executa a prova de trabalho (mineracao)
    def mine_block(self, difficulty, stop_event):
        prefix = '0' * difficulty
        while not self.hash.startswith(prefix):
            if stop_event.is_set():
                return
            self.nonce += 1
            self.hash = self.calculate_hash()
        # Avisar que um bloco foi minerado
        stop_event.set()
        print(f"Bloco minerado com nonce {self.nonce}: {self.hash}")