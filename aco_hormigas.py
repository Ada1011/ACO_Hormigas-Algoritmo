import random

# Grafo representado como diccionario de adyacencias con pesos (distancias)
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1}
}

# Parámetros del algoritmo
pheromone = {}  # feromonas en cada arista
for node in graph:
    for neighbor in graph[node]:
        pheromone[(node, neighbor)] = 1.0  # inicializamos con feromona 1

alpha = 1.0  # importancia de la feromona
beta = 2.0   # importancia de la heurística (inversa de la distancia)
evaporation_rate = 0.5
Q = 100  # cantidad de feromona depositada

def heuristic(u, v):
    return 1.0 / graph[u][v]

def choose_next_node(current, visited):
    neighbors = graph[current]
    probabilities = []
    total = 0
    for node in neighbors:
        if node not in visited:
            tau = pheromone[(current, node)] ** alpha
            eta = heuristic(current, node) ** beta
            prob = tau * eta
            probabilities.append((node, prob))
            total += prob
    if total == 0:
        return None
    # Selección probabilística del siguiente nodo
    r = random.uniform(0, total)
    cumulative = 0
    for node, prob in probabilities:
        cumulative += prob
        if cumulative >= r:
            return node
    return probabilities[-1][0]

def aco(start, end, iterations=10, ants=5):
    best_path = None
    best_length = float('inf')

    for iteracion in range(iterations):
        print(f"\nIteración {iteracion + 1}:")
        all_paths = []
        for ant in range(ants):
            path = [start]
            visited = set(path)
            while path[-1] != end:
                next_node = choose_next_node(path[-1], visited)
                if next_node is None:
                    break  # no hay camino válido
                path.append(next_node)
                visited.add(next_node)
            if path[-1] == end:
                length = sum(graph[path[i]][path[i+1]] for i in range(len(path)-1))
                all_paths.append((path, length))
                print(f"Hormiga {ant + 1}: camino {path}, longitud {length}")

        # Actualizar feromonas
        # Evaporación
        for edge in pheromone:
            pheromone[edge] *= (1 - evaporation_rate)
            if pheromone[edge] < 0.1:
                pheromone[edge] = 0.1  # feromona mínima para evitar bloqueo

        # Depositar feromonas según calidad de la solución
        for path, length in all_paths:
            if length < best_length:
                best_length = length
                best_path = path
            deposit = Q / length
            for i in range(len(path)-1):
                pheromone[(path[i], path[i+1])] += deposit
                pheromone[(path[i+1], path[i])] += deposit  # grafo no dirigido

        print(f"Mejor camino actual: {best_path if best_path else 'Ninguno'}, longitud {best_length if best_path else 'Infinito'}")

    return best_path, best_length

# Ejecución del algoritmo
start_node = 'A'
end_node = 'D'
path, length = aco(start_node, end_node, iterations=5, ants=3)
print("\n--- Resultado final ---")
print(f"Mejor camino encontrado: {path} con longitud {length}")
