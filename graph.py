import networkx as nx
import random

def calculate_heuristic(graph, node1, node2):
    edge_data = graph.get_edge_data(node1, node2)
    if edge_data is not None:
        return edge_data['length'] / edge_data['effective_speed1']
    else:
        return float('inf')

def a_star(graph, start, goal):
    open_list = {start}
    came_from = {}
    g_score = {node: float('inf') for node in graph.nodes}
    g_score[start] = 0
    f_score = {node: float('inf') for node in graph.nodes}
    f_score[start] = calculate_heuristic(graph, start, goal)

    while open_list:
        current = min(open_list, key=lambda node: f_score[node])

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(current)
            path.reverse()
            return path, round(g_score[goal] * 60, 1)  # Return the total time in minutes

        open_list.remove(current)

        for neighbor in graph.neighbors(current):
            tentative_g_score = g_score[current] + calculate_heuristic(graph, current, neighbor)

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + calculate_heuristic(graph, neighbor, goal)
                if neighbor not in open_list:
                    open_list.add(neighbor)

    return None, None

def create_graph():
    # Create an undirected graph
    G = nx.Graph()

    # Create a list of nodes
    nodes = list(range(100))

    # Randomly shuffle the nodes
    random.shuffle(nodes)

    # Add nodes to the graph
    for node in nodes:
        G.add_node(node)

    # Add edges with weights (lengths), speed limits, and congestion
    for node in nodes:
        # Choose a random number of connections for this node
        num_connections = random.randint(1, 10)

        for _ in range(num_connections):
            # Choose a random node to connect to
            other_node = random.choice(nodes)

            # Don't connect a node to itself
            if other_node == node:
                continue

            length = round(random.uniform(0.1, 10), 1)  # Length in kilometers
            speed_limit = random.randint(20, 110)  # Speed limit
            congestion1 = random.randint(1, 10)  # Congestion in one direction
            congestion2 = random.randint(1, 10)  # Congestion in the other direction

            # Effective speed is speed limit divided by congestion
            effective_speed1 = speed_limit / congestion1
            effective_speed2 = speed_limit / congestion2

            # Add edge to graph
            G.add_edge(node, other_node, length=length, speed_limit=speed_limit, 
                       congestion1=congestion1, effective_speed1=effective_speed1,
                       congestion2=congestion2, effective_speed2=effective_speed2)

    return G
