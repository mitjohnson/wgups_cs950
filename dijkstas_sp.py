from classes import Node, Graph
from typing import Dict
import heapq


def shortest_path(starting_vertex: Node, graph: Graph) -> Dict:
    """
    Implementation of Dijkstra's algorithm to find the shortest path
    from a starting vertex to all other vertices in the graph.

    Overall complexity: O((V + E) log V)
    """

    # O(1) - Retrieving the pre-computed adjacency list
    adjacency_list: Dict[Node, Dict[Node, float]] = graph.get_adjacency_list()

    shortest = {}

    min_heap = [[0, starting_vertex]]
    while min_heap:

        # O(log V) - heap operations
        weight, node = heapq.heappop(min_heap)

        if node in shortest:
            continue

        shortest[node] = weight
        if node in adjacency_list:
            # O(E)
            for adjacent_node, adjacent_weight in adjacency_list[node].items():
                if adjacent_node not in shortest:
                    # O(log v)
                    heapq.heappush(
                        min_heap,
                        [weight + adjacent_weight, adjacent_node],
                    )

    # O(V)
    for node in adjacency_list.keys():
        if node not in shortest:
            shortest[node] = -1

    return shortest
