import matplotlib.pyplot as plt
import networkx as nx

def visualize_graph(edges):
    """
    Visualizes a graph given its edges.

    Args:
        edges (list[tuple]): List of edges in the graph (e.g., [(u, v), ...]).
    """
    G = nx.Graph()
    G.add_edges_from(edges)
    
    # Draw the graph
    plt.figure(figsize=(8, 6))
    nx.draw(G, with_labels=True, node_color="lightblue", edge_color="gray", node_size=500, font_size=10)
    plt.show()
