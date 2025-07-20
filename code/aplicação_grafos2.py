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
    
class AplicacaoLabirinto:
    def init(self, janela_principal):
        self.janela = janela_principal
        self.janela.title("Aplicação de Labirinto com Grafos e Pesos")
        # Define cor de fundo bege claro
        self.janela.configure(bg="#F5F5DC")
        self.grafo_atual = None
        self.nome_no_meta = "Fim"
        self._configurar_interface()
        self._executar_atualizacao_labirinto()

    def _configurar_interface(self):
        """Configura todos os widgets da interface gráfica."""
        # Frame principal com cor de fundo bege claro
        painel_principal = ttk.Frame(self.janela, padding="10")
        painel_principal.pack(fill=tk.BOTH, expand=True)
        painel_principal.configure(style="Bege.TFrame")

        # --- Painel de Controles Superiores ---
        painel_controles = ttk.Frame(painel_principal)
        painel_controles.pack(fill=tk.X, pady=5)
        painel_controles.configure(style="Bege.TFrame")

        ttk.Label(painel_controles, text="Quantidade de Vértices:").pack(side=tk.LEFT, padx=(0, 5))
        self.entrada_num_vertices = ttk.Entry(painel_controles, width=5)
        self.entrada_num_vertices.insert(0, "8")
        self.entrada_num_vertices.pack(side=tk.LEFT, padx=5)

        # Botão com cor contrastante
        self.botao_labirinto = tk.Button(painel_controles, text=" Novo Labirinto ", command=self._executar_atualizacao_labirinto, bg="#8B4513", fg="white", activebackground="#A0522D", activeforeground="white")
        self.botao_labirinto.pack(side=tk.LEFT, padx=5)

        # --- Tela para o Labirinto Principal ---
        self.figura_labirinto = Figure(figsize=(8, 5))
        self.eixo_labirinto = self.figura_labirinto.add_subplot(111)
        self.tela_labirinto = FigureCanvasTkAgg(self.figura_labirinto, master=painel_principal)
        self.tela_labirinto.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # --- Painel de Controles Inferiores ---
        painel_caminho = ttk.Frame(painel_principal)
        painel_caminho.pack(fill=tk.X, pady=10)
        painel_caminho.configure(style="Bege.TFrame")

        ttk.Label(painel_caminho, text="Nó de Partida:").pack(side=tk.LEFT, padx=(0, 5))
        self.entrada_no_inicial = ttk.Entry(painel_caminho, width=10)
        self.entrada_no_inicial.pack(side=tk.LEFT, padx=5)

        # Botão com cor contrastante
        self.botao_caminho = tk.Button(painel_caminho, text="Calcular Menor Caminho ", command=self._executar_calculo_caminho, bg="#8B4513", fg="white", activebackground="#A0522D", activeforeground="white")
        self.botao_caminho.pack(side=tk.LEFT, padx=5)

        self.rotulo_resultado = ttk.Label(painel_caminho, text="")
        self.rotulo_resultado.pack(side=tk.LEFT, padx=10)

        # --- Tela para o Menor Caminho ---
        self.figura_caminho = Figure(figsize=(8, 2.5))
        self.eixo_caminho = self.figura_caminho.add_subplot(111)
        self.figura_caminho.tight_layout()
        self.tela_caminho = FigureCanvasTkAgg(self.figura_caminho, master=painel_principal)
        self.tela_caminho.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        # Estilo ttk para frames bege
        estilo = ttk.Style()
        estilo.configure("Bege.TFrame", background="#F5F5DC")

    def _gerar_labirinto(self, numero_de_vertices):
        """Cria um novo grafo que representa o labirinto."""
        numero_de_arestas = random.randint(numero_de_vertices, numero_de_vertices * 2)
        
        grafo_temporario = nx.gnm_random_graph(numero_de_vertices, numero_de_arestas)
        grafo_temporario.add_node(self.nome_no_meta)
        
        mapeamento_nomes = {i: chr(65 + i) for i in range(numero_de_vertices - 1)}
        mapeamento_nomes[numero_de_vertices - 1] = self.nome_no_meta
        self.grafo_atual = nx.relabel_nodes(grafo_temporario, mapeamento_nomes)
        
        for no1, no2 in self.grafo_atual.edges():
            self.grafo_atual.edges[no1, no2]['weight'] = random.randint(1, 10)

    def _desenhar_labirinto(self):
        """Desenha o grafo completo na tela superior."""
        self.eixo_labirinto.clear()
        if self.grafo_atual:
            posicoes = nx.spring_layout(self.grafo_atual, k=0.8, seed=42)
            # Bolinhas laranja, exceto o nó Fim que permanece vermelho
            cores_dos_nos = ['orange' if no != self.nome_no_meta else 'red' for no in self.grafo_atual.nodes()]
            nx.draw(self.grafo_atual, posicoes, ax=self.eixo_labirinto, with_labels=True, node_size=700,
                    node_color=cores_dos_nos, font_size=10, font_weight='bold',
                    width=1.5, edge_color='gray')
            rotulos_arestas = nx.get_edge_attributes(self.grafo_atual, 'weight')
            nx.draw_networkx_edge_labels(self.grafo_atual, posicoes, edge_labels=rotulos_arestas, ax=self.eixo_labirinto)
        self.eixo_labirinto.set_title("Labirinto Completo")
        self.tela_labirinto.draw()

    def _executar_atualizacao_labirinto(self):
        """Lê a entrada, gera um novo labirinto e o desenha."""
        try:
            numero_de_vertices = int(self.entrada_num_vertices.get())
            if not (2 <= numero_de_vertices <= 25):
                messagebox.showerror("Erro de Entrada", "Por favor, insira um número de vértices entre 2 e 25.")
                return
        except ValueError:
            messagebox.showerror("Erro de Entrada", "Entrada inválida. Por favor, insira um número inteiro.")
            return
            
        self._gerar_labirinto(numero_de_vertices)
        self._desenhar_labirinto()
        
        self.eixo_caminho.clear()
        self.eixo_caminho.set_title("Menor Caminho")
        self.tela_caminho.draw()
        self.rotulo_resultado.config(text="")
        self.entrada_no_inicial.delete(0, tk.END)

    def _executar_calculo_caminho(self):
        """Calcula e desenha o Menor Caminho na tela inferior."""
        no_inicial_str = self.entrada_no_inicial.get().strip().upper()

        if not self.grafo_atual:
            self.rotulo_resultado.config(text="Gere um labirinto primeiro.")
            return

        if not no_inicial_str:
            self.rotulo_resultado.config(text="Erro: Digite um nó de partida.")
            return
            
        if no_inicial_str not in self.grafo_atual.nodes:
            self.rotulo_resultado.config(text=f"Erro: Nó '{no_inicial_str}' não existe no labirinto.")
            return

        caminho_encontrado = dijkstra(self.grafo_atual, no_origem=no_inicial_str, no_destino=self.nome_no_meta)
        
        self.eixo_caminho.clear()

        if not caminho_encontrado:
            self.rotulo_resultado.config(text=f"Não há caminho de '{no_inicial_str}' até o Fim.")
        else:
            custo_total = nx.path_weight(self.grafo_atual, caminho_encontrado, weight='weight')
            self.rotulo_resultado.config(text=f"Caminho: {' → '.join(caminho_encontrado)} (Custo: {custo_total})")
            subgrafo_caminho = self.grafo_atual.subgraph(caminho_encontrado)
            posicoes_caminho = nx.spring_layout(subgrafo_caminho, k=0.8, seed=42)
            # Bolinhas laranja, exceto o nó Fim que permanece vermelho
            cores_dos_nos_caminho = ['orange' if no != self.nome_no_meta else 'red' for no in subgrafo_caminho.nodes()]
            nx.draw(subgrafo_caminho, posicoes_caminho, ax=self.eixo_caminho, with_labels=True, node_size=700,
                    node_color=cores_dos_nos_caminho, font_size=10, font_weight='bold',
                    width=2.0, edge_color='blue')
            rotulos_arestas_caminho = nx.get_edge_attributes(subgrafo_caminho, 'weight')
            nx.draw_networkx_edge_labels(subgrafo_caminho, posicoes_caminho, edge_labels=rotulos_arestas_caminho, ax=self.eixo_caminho)

        self.eixo_caminho.set_title("Menor Caminho")
        self.tela_caminho.draw()

if name == "main":
    janela = tk.Tk()
    # Para usar as partes separadamente, você precisaria instanciar a classe
    # app = AplicacaoLabirinto(janela) 
    janela.mainloop()
