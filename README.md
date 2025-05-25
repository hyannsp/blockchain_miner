# Atividade: Análise e Extensão de um Código de Mineração Blockchain
**Professor:** Wanderson Muniz de Santana  
**Turma:** CC7N  
**Alunos:** Hyann Silva Piffer & Ingridy Rodrigues Fagundes
#
Uma vez que concluímos a parte introdutória sobre blockchain, expomos códigos em Python que simulam e mineram os blocos (com prova de trabalho simples usando hashlib e um nonce), vamos agora analisar, modificar e estender os código para criar uma aplicação distribuída e concorrente básica!

## Os objetivos desta atividade são os seguintes:
- Compreender os mecanismos de mineração por prova de trabalho (PoW).
- Explorar concorrência no processo de mineração (uso de threads ou multiprocessing).
- Simular uma rede blockchain distribuída com múltiplos nós minerando blocos.
- Identificar desafios reais de consenso, propagação e sincronização.
Vocês deverão cumprir as seguintes etapas:

## 1. Análise e Explicação (individual ou em dupla)
- Estudar o código fornecido no material introdutório de aula.
- Apresentar comentários explicativos nas seguintes partes:
    - Estrutura do bloco (campos, encadeamento via hash).
    - Algoritmo de prova de trabalho.
    - Verificação da validade do bloco.
- Responda brevemente:
    - O que impede dois blocos de serem minerados simultaneamente?
    - Como o hash e o nonce garantem a dificuldade da mineração?

## 2. Modificação e Concorrência
- Altere o código para executar mineração com múltiplas threads (ou processos) competindo para encontrar um nonce válido.
- Quando uma thread encontrar o nonce, as outras devem parar imediatamente.
- Meça o tempo de mineração com 1, 2, 4, 8 threads e registre os resultados em um gráfico.
Exemplo de Resultado Esperado:
```bash
Minerando com 1 thread... Tempo: 12.3s
Minerando com 2 threads... Tempo: 6.8s
Minerando com 4 threads... Tempo: 3.5s
```
A partir do padrão de saída acima, fornecer gráfico: **threads vs. tempo de mineração**.

## Entrega
1. Código com comentários.
2. Gráfico de desempenho.
3. Respostas conceituais.

## Avaliação
- **Análise conceitual do código:** 0.5 ponto
- **Implementação concorrente correta:** 1 ponto
- **Medições e gráfico de desempenho:** 0.25 ponto
- **Clareza do código e documentação:** 0.25 ponto


# Análise e Explicação do Código
## Arquivo `Block.py`
Essa classe representa um bloco que será alocado na blockchain.
### Importações:
- `hashlib`: Biblioteca de geração de hash.

### Construtor: `__init__`
```python
def __init__(self, index, previous_hash, timestamp, data, nonce=0):
    self.index = index                  
    self.previous_hash = previous_hash
    self.timestamp = timestamp
    self.data = data
    self.nonce = nonce
    self.hash = self.calculate_hash()   
```
Método construtor da classe, define atributos e instância o bloco. Seus atributos são:
- `index`: Indice na blockchain
- `previous_hash`: Hash do bloco anterior na blockchain
- `timestamp`: Data e hora da criação do bloco
- `data`: Dados que serão armazenados no bloco
- `nonce`: Número auxiliar para encontrar o hash desejado
- `hash`: Hash identificador do bloco (recalculado sempre que o nonce muda)

### Método: `calculate_hash`
```python
def calculate_hash(self):
    value = str(self.index) + self.previous_hash + str(self.timestamp) + self.data + str(self.nonce)
    return hashlib.sha256(value.encode()).hexdigest()
```
Concatena **todos** os atributos relevantes do bloco em uma string chamada `value`, em seguida utilizando o algoritimo **SHA256** retornando o hash como uma string hexadecimal.
>[!IMPORTANT]
>
>Isso garante que caso haja uma alteração no bloco, o novo hash gerado será diferente do original, invalidando a cadeia.
### Método: `mine_block`
```python
def mine_block(self, difficulty, stop_event):
        prefix = '0' * difficulty
        while not self.hash.startswith(prefix):
            if stop_event.is_set():
                return
            self.nonce += 1
            self.hash = self.calculate_hash()

        stop_event.set()
        print(f"Bloco minerado com nonce {self.nonce}: {self.hash}")
```
Essa função garante a mineração por prova de trabalho:
1. Define um prefixo de 0's, de acordo com a dificuldade da blockchain.
2. Incrementa o `nonce` do bloco e recalcula o hash até que ele comece com o prefixo definido.
3. Encontrado o hash, sinaliza as outras *Threads* que o hash foi encontrado pelo `stop_event.set()`, interrompendo a mineração concorrente.

## Arquivo `Blockchain.py`
Define a estrutura principal da cadeia de blocos e garante a integridade e segurança da blockchain.
### Importações
- `Block`: Importa a classe Bloco, definida anteriormente contendo a estrutura de um Bloco que ficará na cadeia.
- `time`: Biblioteca para trabalharmos com o tempo.
- `threading`: Biblioteca que permite a manipulação das *threads* do computador.

### Construtor: `__init__`
```python
def __init__(self, difficulty=4):
    self.chain = [self.__create_genesis_block()]
    self.difficulty = difficulty
```
Método construtor para instânciação da cadeia, inicia atributos:
- `chain`: Lista de blocos, iniciado com um bloco inicial 'gênese'.
- `difficulty`: Dificuldade da cadeia, impacta na hora de mineração dos blocos, sendo a quantidade de 0's que será atribuida como prefixo.

### Método: `__create_genesis_block`
```python
def __create_genesis_block(self):
    return Block(0, "0", time.time(), "Genesis Block")
```
Uma simples função apenas utilizada para criar o primeiro bloco da cadeia, ela é chamada apenas pelo construtor.

### Método: `get_latest_block`
```python
def get_latest_block(self):
    return self.chain[-1]
```
Outra função simples, retornando apenas o último bloco que foi adicionado à cadeia.

### Método: `get_difficulty`
```python
def get_difficulty(self):
    return self.difficulty
```
A última função simples da classe, retornando a difficuldade direta da blockchain.

### Método: `add_block`
```python
def add_block(self, new_block: Block):
    new_block.previous_hash = self.get_latest_block().hash
    new_block.mine_block(self.difficulty, threading.Event())
    self.chain.append(new_block)
```
Esse método visa adicionar um novo bloco à cadeia, adicionando o hash do bloco anterior como o `previous_hash` e chamando a função de mineração do bloco, quando finalizada a mineração, adiciona o bloco novo à cadeia.
>[!]NOTE
>
> O `threading.Event()` é utilizado como placeholder para chamar a função `mine_block`, não influenciando no código sequencial!

### Método: `validating_blockchain`
```python
def validating_blockchain(self):
    for i in range(1, len(self.chain)):
        current_block = self.chain[i]
        previous_block = self.chain[i-1]

        if current_block.hash != current_block.calculate_hash():
            return False
        
        if current_block.previous_hash != previous_block.hash:
            return False
        
    return True
```
Percorre a blockchain, verificando se ela está integra e sem alterações.  
Ao percorrer a cadeia, vai verificando o hash atual com o hash recalculado de cada bloco e compara o `previous_hash` com o hash do bloco anterior, retornando `True` ou  `False` de acordo com a validação...

## Arquivo `main.py`
Script principal, simulando o processo de mineração de forma sequencial e concorrente, comparando o tempo de execução e retornando uma visualização gráfica!
### Importações
- ``time``: Medição de tempo de execução.
- `threading`: Execução concorrente usando múltiplas threads.
- `matplotlib.pyplot`: Geração de gráficos.
- `Block`, `Blockchain`: Classes principais da estrutura de blockchain.

### Função: `create_blockchain`
```python
def create_blockchain(difficulty):
    return Blockchain(difficulty=difficulty)
```
Instância uma nova blockchain com dificuldade especificada.

### Função: `sequential_mining`
```python
def sequential_mining(fakechain: Blockchain, new_block: Block):
    start_time = time.time()
    fakechain.add_block(new_block)
    elapsed_time = time.time() - start_time
    print(f"\nMineracao sequencial concluida em {elapsed_time:.2f} segundos.")
    return elapsed_time
```
Função que minera um bloco de maneira sequêncial, o atribui à blockchain, retornando o tempo de mineração.

### Função: `concurrent_mining`
```python
def concurrent_mining(fakechain: Blockchain, new_block: Block, num_threads):
    stop_event = threading.Event()
    minered_blocks = [None]
    def mine():
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
    
    if minered_blocks[0]:
        fakechain.chain.append(minered_blocks[0])


    elapsed_time = time.time() - start_time
    print(f"Mineracao com {num_threads} threads concluida em {elapsed_time:.2f} segundos.\n")
    return elapsed_time
```
Essa função realiza a mineração de maneira Concorrente, onde uma certa quantidade de Threads são selecionadas e passadas para realizar a função `mine()`, realizando os seguintes passos a seguir:
1. Cada Thread cria uma cópia local do bloco passado para mineração;
2. A primeira Thread que encontrar o hash válido, salva o resultado.
3. Todas as outras Thread param por meipo da `stop_event.set()`

### Função: `blockchain_miner`
```python
def blockchain_miner():
    concurrent_times = [] 
    sequential_times = []

    print("===== Mineração com Multiplas Threads =====\n")
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
    return concurrent_times, sequential_times
```


### Função: `graph_view`
```python
def graph_view(concurrent_times, sequential_times, n_threads):
    n_blocks = list(range(1, len(n_threads) + 1))

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
```

### Função Principal
```python
# Ponto de entrada principal
if __name__ == "__main__":
    difficulty = 5
    n_threads = [1, 2, 4, 8]

    concurret_chain: Blockchain = create_blockchain(difficulty)
    sequential_chain: Blockchain = create_blockchain(difficulty)

    concurrent_times, sequential_times = blockchain_miner()

    print("\nValidação das blockchains:")
    print(f"Concorrente válida? {concurret_chain.validating_blockchain()}")
    print(f"Sequencial válida? {sequential_chain.validating_blockchain()}")

    print("\nComparativo entre as minerações:")
    print(f"Concorrente: {concurrent_times} - Total : {sum(concurrent_times):.2f}")
    print(f"Sequencial: {sequential_times} - Total : {sum(sequential_times):.2f}")

    print("\nVisualização dos Gráficos disponíveis em ./output/")
    graph_view(concurrent_times, sequential_times, n_threads)
```