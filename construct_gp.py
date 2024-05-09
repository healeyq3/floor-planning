import networkx as nx
import cvxpy as cp
from typing import List

def generate_sources(G: nx.DiGraph) -> List:
    return [node for node, indegree in G.in_degree() if indegree == 0]

def generate_sinks(G: nx.DiGraph) -> List:
    return [node for node, outdegree in G.out_degree() if outdegree == 0]

def generate_source_sink_paths(G: nx.DiGraph, sources, sinks):
    all_paths = [] # what is proper empty array declaration in Python? <- related to Heaps in C
    
    for (source, sink) in [(source, sink) for source in sources for sink in sinks]:
        for path in nx.all_simple_paths(G, source=source, target=sink):
            all_paths.append(path)

    return(all_paths)

def construct_ggp_expressions(H, V, x, y, w, h):
    
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

    # objective = cp.Minimize( cp.multiply(Height, Width) )

    ### ###

    ### work on boundary constraints - have to do GGP parsing ###

    # harder case: GGP #

    t_right = cp.Variable(pos=True)
    right_boundary = [lhs <= t_right for lhs in width_arguments]
    right_boundary += [x[val - 1] + w[val - 1] <= t_right for val in right_boundary_nodes]

    # right_boundary = [x[val - 1] + w[val - 1] <= Width for val in right_boundary_nodes]

    # t_right = cp.Variable(len(right_boundary_nodes), pos=True)
    # for i, val in enumerate(right_boundary_nodes):
    #     right_boundary += [x[val - 1] + w[val - 1] <= t_right[i]]
    #     right_boundary += [lhs <= t_right[i] for lhs in width_arguments]
    
    t_top = cp.Variable(pos=True)
    top_boundary = [lhs <= t_top for lhs in height_arguments]
    top_boundary += [y[val - 1] + h[val - 1] <= t_top for val in top_boundary_nodes]

    # top_boundary = [y[val - 1] + h[val - 1] <= Height for val in top_boundary_nodes]
    
    # t_top = cp.Variable(len(top_boundary_nodes), pos=True)
    # for i, val in enumerate(top_boundary_nodes):
    #     top_boundary += [y[val - 1] + h[val - 1] <= t_top[i]]
    #     top_boundary += [lhs <= t_top[i] for lhs in height_arguments]

    ### ###

    constraints = right_boundary + top_boundary

    objective = cp.Minimize( cp.multiply(t_right, t_top) )

    return (objective, constraints, Height, Width)


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
                                  x: cp.Variable, y: cp.Variable, w: cp.Variable, h: cp.Variable,) -> List[cp.Expression]:
    left_boundary_nodes = generate_sources(H)
    right_boundary_nodes = generate_sinks(H)
    bottom_boundary_nodes = generate_sources(V)
    top_boundary_nodes = generate_sinks(V)

    # left_boundary = [x[i - 1] >= 0 for i in left_boundary_nodes]
    right_boundary = [x[i - 1] + w[i - 1] <= Width for i in right_boundary_nodes]
    # bottom_boundary = [y[i - 1] >= 0 for i in bottom_boundary_nodes]
    top_boundary = [y[i - 1] + h[i - 1] <= Height for i in top_boundary_nodes]

    # return left_boundary + right_boundary + bottom_boundary + top_boundary
    return right_boundary + top_boundary


def find_floor_placement(H: nx.DiGraph, V: nx.DiGraph, areas: List[float]):
    '''
    Assume that the nodes/cells are 1-based, thus need to make adjustment
    '''
    if (H.number_of_nodes() != V.number_of_nodes()):
        print(H.number_of_nodes())
        print(V.number_of_nodes())
        raise ValueError
    
    n = H.number_of_nodes()

    if (len(areas) != n):
        raise ValueError

    x = cp.Variable(n, pos=True)
    y = cp.Variable(n, pos=True)
    w = cp.Variable(n, pos=True)
    h = cp.Variable(n, pos=True)

    # question: are width and height optimization variables in GP formulation
    # question: need to declare as variable if just constructed as expression of others?

    (objective, constraints, Height, Width) = construct_ggp_expressions(H, V, x, y, w, h)
    # (Width, Height) = generate_objective(H, V, w, h)

    # objective = cp.Minimize( cp.multiply(Height, Width) )

    # print(objective.is_dgp())

    # constraints = generate_boundary_constraints(H, V, Height, Width, x, y, w, h)
    
    # relative positioning constraints
    # constraints = []
    constraints += [x[i - 1] + w[i - 1] <= x[j - 1] for (i, j) in H.edges()]
    constraints += [y[i - 1] + h[i - 1] <= y[j - 1] for (i, j) in V.edges()]

    # area constraints
    # constraints = []
    constraints += [cp.multiply(w[i], h[i]) == areas[i] for i in range(len(areas))]

    problem = cp.Problem(objective, constraints)
    print(problem)
    # print(objective.is_dgp(dpp=True))
    # print(problem.is_dgp())

    problem.solve(gp=True)

    print(problem.status)
    print(Height.value)
    print(Width.value)

    return (x, y, w, h)

