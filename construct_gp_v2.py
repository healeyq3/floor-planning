import networkx as nx
import cvxpy as cp

#### STILL WORKING ON -> was using this to experiment with my previous incorrect GGP formulation.

def generate_sources(G: nx.DiGraph) -> list:
    return [node for node, indegree in G.in_degree() if indegree == 0]

def generate_sinks(G: nx.DiGraph) -> list:
    return [node for node, outdegree in G.out_degree() if outdegree == 0]

def generate_source_sink_paths(G: nx.DiGraph, sources, sinks):
    all_paths = [] # what is proper empty array declaration in Python? <- related to Heaps in C
    
    for (source, sink) in [(source, sink) for source in sources for sink in sinks]:
        for path in nx.all_simple_paths(G, source=source, target=sink):
            all_paths.append(path)

    return(all_paths)

def generate_objective(H, V, w, h):
    left_boundary_nodes = generate_sources(H)
    right_boundary_nodes = generate_sinks(H)
    bottom_boundary_nodes = generate_sources(V)
    top_boundary_nodes = generate_sinks(V)

    ### Create boundary expressions ###

    possible_widths = generate_source_sink_paths(H, left_boundary_nodes, right_boundary_nodes)
    possible_heights = generate_source_sink_paths(V, bottom_boundary_nodes, top_boundary_nodes)

    width_arguments = [sum( [w[i - 1] for i in width] ) for width in possible_widths]
    height_arguments = [ sum( [h[i - 1] for i in height] ) for height in possible_heights ]

    Width = cp.maximum(*width_arguments)
    Height = cp.maximum(*height_arguments)

    return (Width, Height)

def generate_boundary_constraints(H: nx.DiGraph, V: nx.DiGraph, Height: cp.Expression, Width: cp.Expression,
                                  x: cp.Variable, y: cp.Variable, w: cp.Variable, h: cp.Variable,) -> list[cp.Expression]:
    right_boundary_nodes = generate_sinks(H)
    top_boundary_nodes = generate_sinks(V)

    right_boundary = [x[i - 1] + w[i - 1] <= Width for i in right_boundary_nodes]
    top_boundary = [y[i - 1] + h[i - 1] <= Height for i in top_boundary_nodes]

    return right_boundary + top_boundary

def find_floor_placement(H: nx.DiGraph, V: nx.DiGraph, areas = list[float]):

    n = len(areas)

    x = cp.Variable(n, pos=True)
    y = cp.Variable(n, pos=True)
    w = cp.Variable(n, pos=True)
    h = cp.Variable(n, pos = True)

    Height = cp.Variable(pos=True)
    Width = cp.Variable(pos=True)

    Width, Height = generate_objective(H, V, w, h)

    constraints = generate_boundary_constraints(H, V, Height, Width, x, y, w, h)

    constraints += [x[i - 1] + w[i - 1] <= x[j - 1] for (i, j) in H.edges()]
    constraints += [y[i - 1] + h[i - 1] <= y[j - 1] for (i, j) in V.edges()]

    constraints += [cp.multiply(w[i], h[i]) == areas[i] for i in range(len(areas))]

    objective = cp.Minimize(Height * Width)

    print(f"OBJ IS DGP? {objective.is_dgp()}")

    problem = cp.Problem(objective, constraints)

    problem.solve(gp=True)

    print(problem.status)
    print(Height.value)
    print(Width.value)

    return (x, y, w, h)



    


