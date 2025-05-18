from graph_utils import degree_sequence, degree_sequence_repr, generate_graph_with_perfect_matching
from havel_hakimi_algorithm import havel_hakimi_general
from graph_visualization import visualize_graph
from strategies.max_degree_strategy import MaxDegreeStrategy
from strategies.min_degree_strategy import MinDegreeStrategy
from strategies.random_strategy import RandomStrategy
import matplotlib.pyplot as plt


def main():
    # degrees = [4, 3, 3, 3, 2, 2, 2, 1]
    # k = 6
    # degrees = [k]*(k+1) + [1]*(k*(k+1))
    n = 20
    strategy = RandomStrategy()
    original_edges, matching = generate_graph_with_perfect_matching(n, 0.1)
    degrees = degree_sequence(original_edges)
    deg_seq_str = degree_sequence_repr(degrees)
    print("Degree sequence:", deg_seq_str)

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle(f"Degree sequence: ({deg_seq_str}), n={n}", fontsize=16)
    visualize_graph(original_edges, highlight_edges=matching, title="Random Graph with Perfect Matching", ax=axes[0])
    is_graphical, edges = havel_hakimi_general(degrees, strategy=strategy)
    if is_graphical:
        # print("The sequence is graphical. Edges:", edges)
        visualize_graph(edges, title=f"Graph from HH Algorithm ({strategy.__class__.__name__})", ax=axes[1])
    else:
        print("The sequence is not graphical.")
        axes[1].set_visible(False)
    plt.show()


if __name__ == "__main__":
    main()
