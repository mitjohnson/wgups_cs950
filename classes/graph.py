from dataclasses import dataclass, field
from typing import Dict, List, Optional, Iterable


@dataclass(frozen=True)
class Node:
    name: str
    address: str

    def __lt__(self, other: "Node") -> bool:
        return (self.name, self.address) < (other.name, other.address)


@dataclass
class Weight:
    value: float


@dataclass
class Edge:
    node: Node
    weight: Weight


@dataclass
class Graph:
    """Implementation of an undirected graph"""

    adjacenty_list: Dict[Node, Dict[Node, Weight]] = field(
        default_factory=dict
    )

    def add_node(self, node: Node) -> None:
        """
        Adds a node (vertex) to the graph

        Overall complexity O(V) - due to get_node method
        """

        if node is not None:
            if self.get_node(node.name, node.address) is None:
                self.adjacenty_list[node] = {}

    def add_edge(self, node: Node, edge: Edge) -> None:
        """Adds an edge to the graph"""

        self.add_node(node)
        self.add_node(edge.node)

        if node is not None and edge.node is not None:
            self.adjacenty_list[node][edge.node] = edge.weight
            self.adjacenty_list[edge.node][node] = edge.weight

    def nodes(self) -> Iterable[Node]:
        return list(self.adjacenty_list.keys())

    def get_weight(self, node_one: Node, node_two: Node) -> Optional[Weight]:
        """Return the weight between two nodes"""

        if node_two in self.adjacenty_list.get(node_one, {}):
            return self.adjacenty_list[node_one][node_two]
        if node_one in self.adjacenty_list.get(node_two, {}):
            return self.adjacenty_list[node_two][node_one]

        return None

    def get_node(
        self, name: Optional[str] = None, address: Optional[str] = None
    ) -> Optional[Node]:
        """
        Returns Node object

        # Overall complexity: O(V)
        """
        search_params: List[str] = []

        if name is not None:
            search_params.append(name)
        if address is not None:
            search_params.append(address)

        nodes = self.nodes()

        # O(V) - linear search
        for node in nodes:
            if node.name in search_params or node.address in search_params:
                return node
        return None

    def get_adjacency_list(self) -> Dict[Node, Dict[Node, Weight]]:
        """Get pre-computed adjacency list"""
        return self.adjacenty_list
