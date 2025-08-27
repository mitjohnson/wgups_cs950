from dataclasses import dataclass, field
from typing import Tuple
from typing import Dict, List, Optional, Iterable


@dataclass(frozen=True)
class Node:
    name: str
    address: str


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

    _adjacenty_list: Dict[Tuple[str, str], List[Edge]] = field(
        default_factory=dict
    )

    def add_node(self, node: Node) -> None:
        """Adds a node (vertex) to the graph"""
        if node is not None:
            if self.get_node(node.name, node.address) is None:
                self._adjacenty_list[node] = []

    def add_edge(self, node: Node, edge: Edge) -> None:
        """Adds an edge to the graph"""

        self.add_node(node)
        self.add_node(edge.node)

        self._adjacenty_list[node].append(edge)

    def nodes(self) -> Iterable[Node]:
        return list(self._adjacenty_list.keys())

    def get_weight(self, node_one: Node, node_two: Node) -> Optional[Weight]:
        """Return the weight between two nodes"""

        for vertex, weight in self._adjacenty_list.get(node_one):
            if vertex == node_two:
                return weight
        return None

    def get_node(
        self, name: Optional[str] = None, address: Optional[str] = None
    ) -> Optional[Node]:
        """Returns Node object"""
        search_params: List[str] = []

        if name is not None:
            search_params.append(name)
        if address is not None:
            search_params.append(address)

        nodes = self.nodes()
        for node in nodes:
            if node.name in search_params or node.address in search_params:
                return node
        return None
