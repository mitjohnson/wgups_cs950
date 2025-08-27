from classes import Hashtable, Package
from classes.graph import Graph, Node, Edge, Weight

import csv
from pathlib import Path
from datetime import datetime, time
from typing import List, Tuple


def load_package_data(
    path=Path(__file__).parent / "WGUPS_Package_File.csv",
) -> List[List]:
    """Loads the CSV file of packages to deliver."""

    with open(path, newline="", encoding="utf-8") as package_data:
        for row in csv.DictReader(package_data):
            yield row


def load_distance_data(
    path=Path(__file__).parent / "WGUPS_Distance_Table.csv",
) -> List[List]:
    """Loads the CSV file of delivery distances."""

    with open(path, newline="", encoding="utf-8") as distance_data:
        return list(csv.reader(distance_data))


def load_data() -> Tuple[Hashtable, Graph]:
    packages: Hashtable = Hashtable()
    for row in load_package_data():

        deadline = row.get("Delivery Deadline")

        if deadline.upper() == "EOD":
            deadline = time(hour=17, minute=00)
        elif deadline[-2:].upper() == "AM" or "PM":
            deadline = datetime.strptime(deadline, "%I:%M %p").time()

        packages.insert(
            Package(
                id=int(row.get("Package ID")),
                address=row.get("Address"),
                city=row.get("City"),
                state=row.get("State"),
                zip=int(row.get("Zip")),
                weight=int(row.get("Weight KILO")),
                delivery_deadline=deadline,
                special_notes=row.get("Special Notes"),
            )
        )

    distances: Graph = Graph()
    distance_matrix: List[List] = load_distance_data()
    headers: List = distance_matrix[0]
    nodes_length: int = len(headers) - 2

    edges: List[Tuple[Node, str, Weight]] = []
    for idx, row in enumerate(distance_matrix):
        name: str = row[0]
        address: str = row[1]

        if idx == 0:
            continue
        from_node: Node = Node(name.strip(), address.strip())
        distances.add_node(from_node)

        for j in range(nodes_length):
            distance_idx: int = j + 2
            to_node_name: str = headers[distance_idx]

            if distance_idx >= len(row):
                continue
            if row[distance_idx] and row[distance_idx].strip() is not None:
                distance_between: Weight = float(row[distance_idx])
                edges.append((from_node, to_node_name, distance_between))

    # We do not get enough info during parsing to initialize the Edge object.
    for node_one, node_two_name, weight in edges:
        node_two: Node = distances.get_node(name=node_two_name)
        if node_one is node_two:
            continue

        edge: Edge = Edge(node_two, weight)
        distances.add_edge(node_one, edge)

    print(distances._adjacenty_list)
    return (packages, distances)
