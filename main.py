import math
import random

# Função para calcular a distância Euclidiana entre duas cidades
def calcular_distancia(cidade1, cidade2):
    return math.sqrt((cidade2[0] - cidade1[0])**2 + (cidade2[1] - cidade1[1])**2)

# Função para ler os dados de X e Y do arquivo e criar a lista de cidades
def ler_dados_arquivo(nome_arquivo):
    cidades = []
    with open(nome_arquivo, 'r') as arquivo:
        linha = arquivo.readline()  # Ignorar as linhas iniciais
        while linha.startswith('NODE_COORD_SECTION') == False:
            linha = arquivo.readline()
        for linha in arquivo:
            if linha.strip() != '':
                _, x, y = linha.split()
                cidades.append((float(x), float(y)))
    return cidades

# Função para calcular o custo de uma solução (distância total percorrida)
def calcular_custo(solucao, cidades):
    custo = 0
    for i in range(len(solucao) - 1):
        cidade_atual = solucao[i]
        prox_cidade = solucao[i + 1]
        custo += calcular_distancia(cidades[cidade_atual], cidades[prox_cidade])
    custo += calcular_distancia(cidades[solucao[-1]], cidades[solucao[0]])
    return custo

# Função para gerar uma solução inicial aleatória
def gerar_solucao_inicial(num_cidades):
    solucao = list(range(num_cidades))
    random.shuffle(solucao)
    return solucao

def gerar_solucao_gulosa(num_cidades):
    
    visitados = [False] * num_cidades
    solucao = [0]  # Começar pela cidade 0 como ponto de partida
    visitados[0] = True

    for _ in range(num_cidades - 1):
        cidade_atual = solucao[-1]
        melhor_distancia = float('inf')
        melhor_vizinho = None

        for vizinho in range(num_cidades):
            if not visitados[vizinho]:
                distancia = calcular_distancia(cidades[cidade_atual], cidades[vizinho])
                if distancia < melhor_distancia:
                    melhor_distancia = distancia
                    melhor_vizinho = vizinho

        solucao.append(melhor_vizinho)
        visitados[melhor_vizinho] = True

    return solucao





# Função para realizar uma busca local usando a vizinhança 2-opt
def busca_local_2opt(solucao, cidades):
    melhoria = True
    while melhoria:
        melhor_custo = calcular_custo(solucao, cidades)
        melhoria = False
        for i in range(1, len(solucao) - 1):
            for j in range(i + 1, len(solucao)):
                nova_solucao = solucao[:i] + solucao[i:j+1][::-1] + solucao[j+1:]
                novo_custo = calcular_custo(nova_solucao, cidades)
                if novo_custo < melhor_custo:
                    solucao = nova_solucao
                    melhor_custo = novo_custo
                    melhoria = True

                    break
            if melhoria:
                break
    return solucao
# Função para realizar a perturbação usando a vizinhança 5-opt
# Função para realizar a perturbação usando a vizinhança 5-opt
# Função para realizar a perturbação usando a vizinhança 5-opt
def perturbacao_5opt(solucao, cidades):
    num_cidades = len(solucao)
    if num_cidades >= 5:
        indices = random.sample(range(num_cidades), 5)
        indices = sorted(indices)
        i1, i2, i3, i4, i5 = indices

        # Realizar a perturbação 5-opt
        nova_solucao = solucao[:i1] + solucao[i2:i3][::-1] + solucao[i4:i5][::-1] + solucao[i3:i4][::-1] + solucao[i5:]
        return nova_solucao
    return solucao
# Função para realizar a perturbação aleatória
def perturbacao_aleatoria(solucao, cidades):
    num_cidades = len(solucao)
    if num_cidades >= 2:
        indices = random.sample(range(num_cidades), 2)
        i, j = sorted(indices)

        # Realizar a perturbação aleatória
        nova_solucao = solucao[:i] + solucao[i:j+1][::-1] + solucao[j+1:]
        return nova_solucao
    return solucao





# Função para realizar a perturbação usando a vizinhança 3-opt
def perturbacao_3opt(solucao, cidades):
    num_cidades = len(solucao)
    if num_cidades >= 3:
        i, j, k = random.sample(range(num_cidades), 3)
        i, j, k = sorted([i, j, k])
        nova_solucao = solucao[:i] + solucao[i:j+1][::-1] + solucao[j+1:k+1][::-1] + solucao[k+1:]
        return nova_solucao
    return solucao
# Função para realizar a perturbação usando a vizinhança 4-opt
# Função para realizar a perturbação usando a vizinhança 4-opt
def perturbacao_4opt(solucao, cidades):
    num_cidades = len(solucao)
    if num_cidades >= 4:
        indices = random.sample(range(num_cidades), 4)
        indices = sorted(indices)
        i1, i2, i3, i4 = indices
        
        # Realizar a perturbação 4-opt
        nova_solucao = solucao[:i1] + solucao[i4:i3-1:-1] + solucao[i2:i3] + solucao[i1:i2] + solucao[i3:]
        return nova_solucao
    return solucao

    return solucao

# Função principal do ILS para resolver o TSP
def ils_tsp(cidades, num_iteracoes):
    num_cidades = len(cidades)
    s0 = gerar_solucao_inicial(num_cidades)
    c0=calcular_custo(s0,cidades)
    print("S0 = ",s0)
    melhor_solucao = busca_local_2opt(s0,cidades)
    print("S =",melhor_solucao)
    print("c0=",c0)
    melhor_custo = calcular_custo(melhor_solucao, cidades)
    print("m=",melhor_custo)
    
    for _ in range(10):
        solucao_inicial = perturbacao_3opt(melhor_solucao, cidades)
        print("pert = ",solucao_inicial)
        solucao_local = busca_local_2opt(solucao_inicial, cidades)
        print("local = ",solucao_local)
        custo_local = calcular_custo(solucao_local, cidades)
        
        if custo_local < melhor_custo:
            melhor_solucao = solucao_local
            melhor_custo = custo_local
        else:
            melhor_solucao = solucao_inicial
            melhor_custo = custo_local
    return melhor_solucao, melhor_custo

# Nome do arquivo contendo os dados de X e Y das cidades
arquivo_cidades = 'dj38.tsp'
# Número de iterações do ILS
num_iteracoes_ils = 100

# Ler os dados de X e Y das cidades do arquivo
cidades = ler_dados_arquivo(arquivo_cidades)

# Executar o algoritmo ILS para resolver o TSP
melhor_solucao, melhor_custo = ils_tsp(cidades, num_iteracoes_ils)

# Imprimir a melhor solução encontrada
print("Melhor solução encontrada:", melhor_solucao)
print("Custo da melhor solução:", melhor_custo)
