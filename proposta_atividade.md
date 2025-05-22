# Atividade: Análise e Extensão de um Código de Mineração Blockchain
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
- Código com comentários.
- Gráfico de desempenho.
- Respostas conceituais.

## Avaliação
- **Análise conceitual do código:** 0.5 ponto
- **Implementação concorrente correta:** 1 ponto
- **Medições e gráfico de desempenho:** 0.25 ponto
- **Clareza do código e documentação:** 0.25 ponto