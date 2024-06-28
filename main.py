import random
import matplotlib.pyplot as plt
import networkx as nx

from relative_position_graph import create_dags
from construct_gp import find_floor_placement

def draw_graph(G: nx.Graph):
    plt.figure()
    nx.draw_circular(
        G,
        with_labels=True,
        node_size=1000,
        node_color='white',  # Set node color to white
        edge_color='black',  # Set edge color to black
        edgecolors='black',
        linewidths=1, 
        width=0.8,
        font_size=14,
    )

def draw_graph_labels(G: nx.Graph, labels):
    plt.figure()
    pos = nx.spring_layout(G)  # Position nodes using Fruchterman-Reingold force-directed algorithm
    
    nx.draw(
        G, 
        pos=pos, 
        with_labels=False,  # We'll use node labels instead of default labels
        node_size=1000, 
        node_color='white',  
        edge_color='black',  
        linewidths=1,        
        edgecolors='black',  
        font_size=14
    )
    
    # Draw node labels
    nx.draw_networkx_labels(G, pos=pos, labels=labels, font_size=12, font_color='black', font_weight='bold')
    
    plt.show()

def draw_solution(boxes, sizes, labels):
    if len(labels) == 0:
        labels = [i+ 1 for i in range(len(boxes))]

    fig, ax = plt.subplots()

    colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightsalmon', 'lightseagreen']  # Define colors

    for (x, y), (width, height), label, color in zip(boxes, sizes, labels, colors):
        # Plot the rectangle with a different color
        ax.add_patch(plt.Rectangle((x, y), width, height, color=color))
        
        # Add label on top of the rectangle
        ax.text(x + width / 2, y + height / 2, label, ha='center', va='center', fontsize=10)

    ax.set_aspect('equal')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Optimal Floor Placement')
    # plt.grid(True)

    # Adjust the plot limits to include the boxes
    ax.autoscale()

if __name__ == '__main__':
    # EXAMPLE 1
    nodes = [1, 2, 3, 4, 5]
    areas = [random.randint(1, 5) for _ in range(5)]
    h_edges = [(1, 3), (2, 3), (3, 5), (4, 5)]
    v_edges = [(2, 1), (1, 4), (3, 4)]
    labels = []

    # EXAMPLE 2
    # nodes = [1, 2, 3, 4]
    # areas = [0.2, 0.5, 1.5, 0.5]
    # h_edges = [(1, 2), (3, 4)]
    # v_edges = [(3, 1), (3, 2), (4, 1), (4, 2)]
    # labels = ['A', 'B', 'C', 'D']
    # labels_dict = {
    #     1: 'A',
    #     2: 'B',
    #     3: 'C',
    #     4: 'D'
    # }
    
    H, V = create_dags(nodes, h_edges=h_edges, v_edges=v_edges)

    x, y, w, h = find_floor_placement(H, V, areas)

    boxes = list(zip(x.value, y.value))
    sizes = list(zip(w.value, h.value))

    draw_solution(boxes, sizes, labels)
    draw_graph(H)
    draw_graph(V)
    
    plt.show()
    plt.close('all')