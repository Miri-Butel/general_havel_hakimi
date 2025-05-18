import matplotlib.pyplot as plt
import networkx as nx

def visualize_graph(edges, highlight_edges=None, title=None, ax=None):
    """
    Visualizes a graph given its edges. Optionally highlights specific edges.

    Args:
        edges (list[tuple]): List of edges in the graph (e.g., [(u, v), ...]).
        highlight_edges (list[tuple], optional): Edges to highlight in a different color.
        title (str, optional): Title for the figure.
        ax (matplotlib.axes.Axes, optional): Axes to plot on.
    """
    G = nx.Graph()
    G.add_edges_from(edges)
    pos = nx.spring_layout(G)
    if ax is None:
        plt.figure(figsize=(8, 6))
        ax = plt.gca()
    # Draw all edges in gray
    nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color="gray", ax=ax)
    # Draw highlighted edges if provided
    if highlight_edges:
        nx.draw_networkx_edges(
            G, pos, edgelist=highlight_edges, edge_color="red", width=2, ax=ax
        )
    nx.draw_networkx_nodes(G, pos, node_color="lightblue", node_size=500, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=10, ax=ax)
    if title:
        ax.set_title(title)
    ax.axis("off")
