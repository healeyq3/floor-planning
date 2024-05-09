import networkx as nx
from typing import List, Tuple

def check_valid_positioning(nodes: List, h_edges: List, v_edges: List):
    # need to check if all nodes have relevant position
    # we require that for every pair of cells,
    # there is a directed path from one to the other in one of the graphs.
    # TO IMPLEMENT
    return

def create_dags(nodes: List, h_edges: List, v_edges: List) -> Tuple[nx.DiGraph, nx.DiGraph]:

    # if (node_labels != None and len(nodes) != len(node_labels)):
    #     raise ValueError

    # check_valid_positioning()

    # can call is DAG

    H = nx.DiGraph()
    H.add_nodes_from(nodes)
    H.add_edges_from(h_edges)
    
    V = nx.DiGraph()
    V.add_nodes_from(nodes)
    V.add_edges_from(v_edges)

    return (H, V)