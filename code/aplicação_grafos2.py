import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import random
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def dijkstra(grafo, no_origem, no_destino):
    """
    Executa o algoritmo de Dijkstra para encontrar o menor caminho entre dois nós em um grafo.
    """
    # Inicializa as distâncias: todos os nós começam com infinito, exceto a origem que recebe zero
    distancias = {no: float('inf') for no in grafo.nodes()}
    distancias[no_origem] = 0

    # Guarda os nós que já foram processados
    nos_visitados = set()

    # Armazena o nó anterior para reconstrução do caminho mínimo
    predecessores = {no: None for no in grafo.nodes()}

    # Enquanto houver nós não visitados, busca o nó com menor distância conhecida
    while len(nos_visitados) < len(grafo.nodes()):
        # Seleciona o nó não visitado com a menor distância até o momento
        no_distancia_minima = None
        for no_atual in grafo.nodes():
            if no_atual not in nos_visitados:
                if no_distancia_minima is None or distancias[no_atual] < distancias[no_distancia_minima]:
                    no_distancia_minima = no_atual

        # Interrompe se não houver mais nós acessíveis ou se o destino foi alcançado
        if no_distancia_minima is None or distancias[no_distancia_minima] == float('inf'):
            break

        # Marca o nó atual como visitado
        nos_visitados.add(no_distancia_minima)

        # Se chegou ao destino, encerra o loop
        if no_distancia_minima == no_destino:
            break

        # Atualiza as distâncias dos vizinhos do nó atual
        distancia_acumulada = distancias[no_distancia_minima]
        for vizinho in grafo.neighbors(no_distancia_minima):
            peso_aresta = grafo[no_distancia_minima][vizinho]['weight']
            nova_distancia = distancia_acumulada + peso_aresta

            # Se encontrou um caminho mais curto para o vizinho, atualiza
            if nova_distancia < distancias[vizinho]:
                distancias[vizinho] = nova_distancia
                predecessores[vizinho] = no_distancia_minima

    # Reconstrói o menor caminho do destino até a origem
    caminho_final = []
    no_atual_no_caminho = no_destino

    # Se não existe caminho entre origem e destino, retorna lista vazia
    if predecessores[no_atual_no_caminho] is None and no_origem != no_destino:
        return []

    # Monta o caminho percorrendo os predecessores
    while no_atual_no_caminho is not None:
        caminho_final.insert(0, no_atual_no_caminho)
        no_atual_no_caminho = predecessores[no_atual_no_caminho]

    # Confirma se o caminho começa na origem
    if caminho_final and caminho_final[0] == no_origem:
        return caminho_final
    else:
        return []