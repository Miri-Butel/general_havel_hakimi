import argparse
from graph_utils import degree_sequence, degree_sequence_repr, generate_graph_with_perfect_matching, parse_degree_sequence
from havel_hakimi_algorithm import havel_hakimi_general
from graph_visualization import visualize_graph
from strategies.max_degree_strategy import MaxDegreeStrategy
from strategies.min_degree_strategy import MinDegreeStrategy
from strategies.random_strategy import RandomStrategy
from strategies.matching_aware_strategy import MatchingAwareStrategy
import matplotlib.pyplot as plt

# Edit this line to change the default degree sequence
# k = 5
# DEFAULT_DEGREE_SEQUENCE = [k]*(k+1) + [1]*(k*(k+1))
DEFAULT_DEGREE_SEQUENCE = "[3]*4 + [2]*6 + [1]*4"

STRATEGY_MAP = {
    "max": MaxDegreeStrategy,
    "min": MinDegreeStrategy,
    "random": RandomStrategy,
    "matching": MatchingAwareStrategy,
}

def parse_args():
    parser = argparse.ArgumentParser(description="Havel-Hakimi Graph Generator and Visualizer")
    parser.add_argument('--n', type=int, default=None, help="Number of vertices (for random graph with perfect matching)")
    parser.add_argument('--degrees', type=str, default=None, help="Degree sequence as comma-separated list (e.g. 3,3,2,2,2,1)")
    parser.add_argument('--strategy', type=str, default="matching", choices=STRATEGY_MAP.keys(),
                        help="Strategy to use: max, min, random, matching (default: matching)")
    parser.add_argument('--p', type=float, default=0.1, help="Edge probability for random graph with perfect matching (default: 0.1)")
    return parser.parse_args()

def get_degree_sequence(args):
    """
    Get degree sequence based on input arguments or user input
    """
    if args.degrees:
        degrees = parse_degree_sequence(args.degrees)
        return degrees, None, None
    elif args.n:
        n = args.n
        original_edges, matching = generate_graph_with_perfect_matching(n, args.p)
        degrees = degree_sequence(original_edges)
        return degrees, original_edges, matching
    else:
        # Prompt user for degree sequence
        print("Enter degree sequence as:")
        print("  - Comma-separated list (e.g., 3,3,2,2,2,1)")
        print("  - Python-style expression (e.g., [3]*2 + [2]*3 + [1])")
        print("  - Or press Enter to use the default sequence: " + DEFAULT_DEGREE_SEQUENCE)
        deg_str = input("> ")
        if not deg_str.strip():
            # Use the default sequence
            deg_str = DEFAULT_DEGREE_SEQUENCE
            print(f"Using default sequence: {DEFAULT_DEGREE_SEQUENCE}")
        
        degrees = parse_degree_sequence(deg_str)
        return degrees, None, None

def setup_visualization(degrees):
    """
    Set up figure and axes for visualization
    """
    n = len(degrees)
    deg_seq_str = degree_sequence_repr(degrees)
    print("Degree sequence:", deg_seq_str)

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle(f"Degree sequence: ({deg_seq_str}), n={n}", fontsize=16)
    return fig, axes, n, deg_seq_str

def visualize_original_graph(original_edges, matching, axes, n):
    """
    Visualize the original graph if available
    """
    if original_edges is not None:
        visualize_graph(
            original_edges,
            highlight_edges=matching,
            ax=axes[0],
            title=f"Random Graph with Perfect Matching, matching size: {len(matching) if matching is not None else 0}/{n // 2}"
        )
    else:
        axes[0].set_visible(False)

def run_and_visualize_havel_hakimi(degrees, strategy, axes, n):
    """
    Run Havel-Hakimi algorithm and visualize the resulting graph
    """
    is_graphical, edges = havel_hakimi_general(degrees, strategy=strategy)
    if is_graphical:
        # print("The sequence is graphical. Edges:", edges)
        matching_edges = None
        if hasattr(strategy, "get_matching_edges"):
            matching_edges = strategy.get_matching_edges()
        matching_size = len(matching_edges) if matching_edges else 0
        visualize_graph(
            edges, 
            highlight_edges=matching_edges, 
            ax=axes[1],
            title=f"Graph from HH Algorithm ({strategy.__class__.__name__}), matching size: {matching_size}/{n // 2}"
        )
        return True
    else:
        print("The sequence is not graphical.")
        axes[1].set_visible(False)
        return False

def main():
    args = parse_args()
    strategy = STRATEGY_MAP[args.strategy]()
    
    # Get degree sequence and original graph if applicable
    degrees, original_edges, matching = get_degree_sequence(args)
    
    # Setup visualization
    fig, axes, n, _ = setup_visualization(degrees)
    
    # Visualize original graph if available
    visualize_original_graph(original_edges, matching, axes, n)
    
    # Run Havel-Hakimi algorithm and visualize result
    run_and_visualize_havel_hakimi(degrees, strategy, axes, n)
    
    plt.show()

if __name__ == "__main__":
    main()
