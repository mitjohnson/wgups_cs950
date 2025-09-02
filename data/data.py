from classes import Hashtable, Package

import re
from classes.graph import Graph, Node, Edge, Weight

import csv
from pathlib import Path
from datetime import datetime, time
from typing import List, Tuple


def address_normalizer(address: str) -> str:
    """helper method to Normalize cardinal directions."""
    if not address:
        return address
    address = re.sub(r'\bN\b', 'North', address, flags=re.IGNORECASE)
    address = re.sub(r'\bS\b', 'South', address, flags=re.IGNORECASE)
    address = re.sub(r'\bE\b', 'East', address, flags=re.IGNORECASE)
    address = re.sub(r'\bW\b', 'West', address, flags=re.IGNORECASE)
    return address


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

    # O(n) for each row in the CSV
    with open(path, newline="", encoding="utf-8") as distance_data:
        return list(csv.reader(distance_data))


def parse_package_data(hashtable: Hashtable) -> None:
    """parses raw csv data and inserts it into a hash table."""

    # O(n) for each row in the CSV
    for row in load_package_data():
        normalized_address = address_normalizer(row.get("Address"))

        deadline = row.get("Delivery Deadline")
        if deadline.upper() == "EOD":
            deadline = time(hour=17, minute=00)
        elif deadline[-2:].upper() == "AM" or "PM":
            deadline = datetime.strptime(deadline, "%I:%M %p").time()

        hashtable.insert(
            Package(
                id=int(row.get("Package ID")),
                address=normalized_address,
                city=row.get("City"),
                state=row.get("State"),
                zip=int(row.get("Zip")),
                weight=int(row.get("Weight KILO")),
                delivery_deadline=deadline,
                special_notes=row.get("Special Notes"),
            )
        )


def parse_distance_data(graph: Graph) -> None:
    """
    Parses raw csv data and adds to a undirected graph

    Overall complexity: O(n^2), due to nested loops
    """

    distance_matrix: List[List] = load_distance_data()
    headers: List = distance_matrix[0]

    # O(n) create all nodes first
    node_map = {}
    for row in distance_matrix[1:]:
        name: str = row[0]
        address: str = address_normalizer(row[1])
        node = Node(name.strip(), address.strip())
        graph.add_node(node)
        node_map[name.strip()] = node

    # O(n^2) add edges
    for row in distance_matrix[1:]:
        from_node = node_map[row[0].strip()]
        for i, distance in enumerate(row[2:], start=2):
            if distance.strip():
                to_node_name = headers[i].strip()
                to_node = node_map[to_node_name]
                weight = float(distance)
                edge = Edge(to_node, weight)
                graph.add_edge(from_node, edge)


def load_data() -> Tuple[Hashtable, Graph]:
    """
    Loads and parses package and delivery data

    Overall complexity: O(n^2)
    """

    packages: Hashtable = Hashtable()
    # O(n)
    parse_package_data(packages)

    distances: Graph = Graph()
    # O(n^2)
    parse_distance_data(distances)

    return (packages, distances)
