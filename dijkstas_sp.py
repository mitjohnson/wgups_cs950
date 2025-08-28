from classes import Node, Edge, Graph
from typing import Dict, List
import heapq


def shortest_path(starting_vertex: Node, graph: Graph) -> Dict:
    adjacency_list: Dict[Node, List[Edge]] = graph.get_adjacency_list()

    shortest = {}

    min_heap = [[0, starting_vertex]]
    while min_heap:
        node, weight = heapq.heappop(min_heap)

        if node in shortest:
            continue

        shortest[node] = weight

        for adjacent_node, adjacent_weight in adjacency_list[
            (node.name, node.address)
        ]:
            if adjacent_node not in shortest:
                heapq.heappush(
                    min_heap, [weight + adjacent_weight, adjacent_node]
                )
    for node in adjacency_list.keys():
        if node not in shortest:
            shortest[node] = -1

    return shortest
