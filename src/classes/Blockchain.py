import time
import threading
from classes import Block

# Classe de representação da Blockchain
class Blockchain():
    def __init__(self, difficulty=4):
        self.chain = [self.__create_genesis_block()] # Cadeia de Blocos (com o bloco inicial)
        self.difficulty = difficulty

    # Criação do Bloco inicial da cadeia
    def __create_genesis_block(self):
        return Block(0, "0", time.time(), "Genesis Block")
    
    # Retorna ultimo bloco na cadeia
    def get_latest_block(self):
        return self.chain[-1]
    
    def get_difficulty(self):
        return self.difficulty
    
    # Adiciona um bloco criado na cadeia com Hash
    def add_block(self, new_block: Block):
        new_block.previous_hash = self.get_latest_block().hash      # Adiciona o hash do bloco anterior ao novo bloco
        new_block.mine_block(self.difficulty, threading.Event())    # Minera o bloco com dificuldade escolhida, utilizando threading.Event() como placeholder
        self.chain.append(new_block)                                # Adiciona o Bloco à cadeia
    
    # Verifica se os blocos e encadeamento estão válidos com seus respectivos hashs
    def validating_blockchain(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False
            
            if current_block.previous_hash != previous_block.hash:
                return False
            
        return True
