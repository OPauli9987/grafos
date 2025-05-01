import heapq
from typing import TypeVar, Generic, Dict, List, Optional, Tuple

T = TypeVar('T')

class Nodo(Generic[T]):
    def __init__(self, dato: T):
        self.dato: T = dato
        self.vecinos: Dict['Nodo[T]', float] = {}
        
    def agregar_nodob(self, nodo: 'Nodo[T]', peso: float, bidireccional: bool = True):
        self.vecinos[nodo] = peso
        if bidireccional:
            nodo.vecinos[self] = peso
            
    def __repr__(self):
        return f"Nodo({self.dato})"
    
    def __hash__(self):
        return hash(id(self))
    
    def __eq__(self, other):
        if not isinstance(other, Nodo):
            return False
        return id(self) == id(other)
    
    def __lt__(self, other):
        return id(self) < id(other)

class GrafoNoDirigido(Generic[T]):
    def __init__(self):
        self.nodos: List[Nodo[T]] = []
        
    def agregar_nodo(self, dato: T) -> Nodo[T]:
        nuevo_nodo = Nodo(dato)
        self.nodos.append(nuevo_nodo)
        return nuevo_nodo
    
    def agregar_arista(self, nodo1: Nodo[T], nodo2: Nodo[T], peso: float):
        if nodo1 not in self.nodos or nodo2 not in self.nodos:
            raise ValueError("Ambos nodos deben estar en un grafo")
        nodo1.agregar_nodob(nodo2, peso)
    
    def encontrar_ruta(self, inicio: Nodo[T], destino: Nodo[T]) -> Tuple[float, List[Nodo[T]]]:
        if inicio not in self.nodos or destino not in self.nodos:
            raise ValueError("Los nodos deben estar en un grafo")
            
        distancias, predecesor = self.dijkstra(inicio)
        
        if distancias[destino] == float('infinity'):
            raise ValueError(f"No hay camino desde {inicio.dato} hasta {destino.dato}")
            
        camino = self.obtener_ruta(predecesor, destino)
        return distancias[destino], camino
    
    def mostrar_datos_nodo(self, nodo: Nodo[T]):
        if nodo not in self.nodos:
            print("El nodo no existe en un grafo")
        else:
            print(f"Datos almacenados en el nodo: {nodo.dato}")
    
    def dijkstra(self, inicio: Nodo[T]) -> Tuple[Dict[Nodo[T], float], Dict[Nodo[T], Optional[Nodo[T]]]]:
        distancias: Dict[Nodo[T], float] = {nodo: float('infinity') for nodo in self.nodos}
        distancias[inicio] = 0
        predecesor: Dict[Nodo[T], Optional[Nodo[T]]] = {nodo: None for nodo in self.nodos}
        
        cola: List[Tuple[float, Nodo[T]]] = []
        heapq.heappush(cola, (0, inicio))
        
        while cola:
            distancia_actual, nodo_actual = heapq.heappop(cola)
            
            if distancia_actual > distancias[nodo_actual]:
                continue
                
            for vecino, peso in nodo_actual.vecinos.items():
                distancia = distancia_actual + peso
                
                if distancia < distancias[vecino]:
                    distancias[vecino] = distancia
                    predecesor[vecino] = nodo_actual
                    heapq.heappush(cola, (distancia, vecino))
                    
        return distancias, predecesor
    
    def obtener_ruta(self, predecesores: Dict[Nodo[T], Optional[Nodo[T]]], destino: Nodo[T]) -> List[Nodo[T]]:
        camino = []
        actual = destino
        
        while actual is not None:
            camino.append(actual)
            actual = predecesores[actual]
            
        camino.reverse()
        return camino

if __name__ == "__main__":
    grafo = GrafoNoDirigido[str]()
    
    saltillo = grafo.agregar_nodo("Saltillo")
    monterrey = grafo.agregar_nodo("Monterrey")
    ciudadmx = grafo.agregar_nodo("Ciudadmx")
    torreon = grafo.agregar_nodo("Torreon")
    guadalajara = grafo.agregar_nodo("Guadalajara")
    
    grafo.agregar_arista(saltillo, monterrey, 100)
    grafo.agregar_arista(saltillo, ciudadmx, 1500)
    grafo.agregar_arista(saltillo, torreon, 200)
    grafo.agregar_arista(monterrey, ciudadmx, 1600)
    grafo.agregar_arista(ciudadmx, torreon, 300)
    grafo.agregar_arista(saltillo, guadalajara, 450)
    grafo.agregar_arista(monterrey, guadalajara, 550)
    
    try:
        distancia, camino = grafo.encontrar_ruta(saltillo, torreon)
        print(f"\nRuta más corta desde saltillo a torreon:")
        print(" -> ".join(str(nodo.dato) for nodo in camino))
        print(f"Distancia total: {distancia} km")
        
        print("\nDatos del nodo destino:")
        grafo.mostrar_datos_nodo(torreon)

        distancia, camino = grafo.encontrar_ruta(ciudadmx, guadalajara)
        print(f"\nRuta más corta desde ciudadmx a guadalajara:")
        print(" -> ".join(str(nodo.dato) for nodo in camino))
        print(f"Distancia total: {distancia} km")
        
        print("\nDatos del nodo destino:")
        grafo.mostrar_datos_nodo(guadalajara)

    except ValueError as e:
        print(e)
    