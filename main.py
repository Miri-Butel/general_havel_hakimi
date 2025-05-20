from graph_utils import degree_sequence, degree_sequence_repr, generate_graph_with_perfect_matching
from havel_hakimi_algorithm import havel_hakimi_general
from graph_visualization import visualize_graph
from strategies.max_degree_strategy import MaxDegreeStrategy
from strategies.min_degree_strategy import MinDegreeStrategy
from strategies.random_strategy import RandomStrategy
from strategies.matching_aware_strategy import MatchingAwareStrategy
import matplotlib.pyplot as plt


def main():
    # degrees = [4, 3, 3, 3, 2, 2, 2, 1]
    # k = 5
    # degrees = [k]*(k+1) + [1]*(k*(k+1))
    n = 20
    strategy = MatchingAwareStrategy()
    original_edges, matching = generate_graph_with_perfect_matching(n, 0.1)
    degrees = degree_sequence(original_edges)
    deg_seq_str = degree_sequence_repr(degrees)
    print("Degree sequence:", deg_seq_str)

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle(f"Degree sequence: ({deg_seq_str}), n={n}", fontsize=16)
    visualize_graph(original_edges, highlight_edges=matching, ax=axes[0],
                    title=f"Random Graph with Perfect Matching, matching size: {len(matching)}/{n // 2}")
    is_graphical, edges = havel_hakimi_general(degrees, strategy=strategy)
    if is_graphical:
        print("The sequence is graphical. Edges:", edges)
        matching_edges = None
        if hasattr(strategy, "get_matching_edges"):
            matching_edges = strategy.get_matching_edges()
        maching_size = len(matching_edges) if matching_edges else 0
        visualize_graph(edges, highlight_edges=matching_edges, ax=axes[1],
                        title=f"Graph from HH Algorithm ({strategy.__class__.__name__}), matching size: {maching_size}/{n // 2}")
    else:
        print("The sequence is not graphical.")
        axes[1].set_visible(False)
    plt.show()


if __name__ == "__main__":
    main()
