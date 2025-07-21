import streamlit as st
import plotly.graph_objects as go
import networkx as nx
from rustworkx import max_weight_matching
from graph_utils import degree_sequence_repr, edges_to_rustworkx_graph, parse_degree_sequence, maximum_matching_size_numpy
from havel_hakimi_algorithm import havel_hakimi_general
from strategies.max_degree_strategy import MaxDegreeStrategy
from strategies.min_degree_strategy import MinDegreeStrategy
from strategies.naive_matching_aware_strategy import NaiveMatchingAwareStrategy
from strategies.random_strategy import RandomStrategy
from strategies.matching_aware_strategy import MatchingAwareStrategy

STRATEGY_MAP = {
    "max": MaxDegreeStrategy,
    "min": MinDegreeStrategy,
    "random": RandomStrategy,
    "matching": MatchingAwareStrategy,
    "naive_matching": NaiveMatchingAwareStrategy
}

def plot_graph_plotly(edges, matching_edges=None, title=""):
    G = nx.Graph()
    G.add_edges_from(edges)
    pos = nx.spring_layout(G, seed=42)
    edge_x = []
    edge_y = []
    for e in G.edges():
        x0, y0 = pos[e[0]]
        x1, y1 = pos[e[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='#888'),
        hoverinfo='none',
        mode='lines')

    match_x = []
    match_y = []
    if matching_edges:
        for e in matching_edges:
            x0, y0 = pos[e[0]]
            x1, y1 = pos[e[1]]
            match_x += [x0, x1, None]
            match_y += [y0, y1, None]
    match_trace = go.Scatter(
        x=match_x, y=match_y,
        line=dict(width=3, color='red'),
        hoverinfo='none',
        mode='lines',
        name='Matching')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=[str(n) for n in G.nodes()],
        textposition="top center",
        marker=dict(size=12, color='lightblue', line=dict(width=2)),
        hoverinfo='text')

    fig = go.Figure(data=[edge_trace, match_trace, node_trace] if matching_edges else [edge_trace, node_trace],
                    layout=go.Layout(
                        title=title,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40),
                        xaxis=dict(showgrid=False, zeroline=False, visible=False),
                        yaxis=dict(showgrid=False, zeroline=False, visible=False)
                    ))
    return fig

st.title("Havel-Hakimi Graph Generator and Visualizer (Interactive)")

st.markdown("""
Enter a degree sequence (comma-separated or Python-style, e.g. `[3]*4 + [2]*6 + [1]*4`), or use the default.
""")

default_seq = "[3]*4 + [2]*6 + [1]*4"
deg_str = st.text_input("Degree sequence:", value=default_seq)
strategy_name = st.selectbox("Strategy", list(STRATEGY_MAP.keys()), index=3)

if st.button("Generate Interactive Graph"):
    try:
        degrees = parse_degree_sequence(deg_str)
        degrees = sorted(degrees, reverse=True)
        n = len(degrees)
        deg_seq_str = degree_sequence_repr(degrees)
        st.write(f"Degree sequence: {deg_seq_str} (n={n})")
        strategy = STRATEGY_MAP[strategy_name]()
        is_graphical, edges = havel_hakimi_general(degrees, strategy=strategy)
        if is_graphical:
            matching_edges = None
            if hasattr(strategy, "get_matching_edges"):
                matching_edges = strategy.get_matching_edges()
            matching_size = len(matching_edges) if matching_edges else 0
            rw_graph = edges_to_rustworkx_graph(edges)
            rw_matching = max_weight_matching(rw_graph, max_cardinality=True)
            max_matching_size_graph = len(rw_matching)
            max_matching_size_degseq = maximum_matching_size_numpy(degrees)

            # Display matching sizes above the graph
            st.write(f"*Matching size by algorithm:* {matching_size}")
            st.write(f"*Maximum matching size (resulting graph):* {max_matching_size_graph}")
            st.write(f"*Maximum matching size (degree sequence):* {max_matching_size_degseq}")
            fig = plot_graph_plotly(
                edges,
                matching_edges=matching_edges,
                title=f"Graph from HH Algorithm ({strategy.__class__.__name__})"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("The sequence is not graphical.")
    except Exception as e:
        st.error(f"Error: {e}")
