from havel_hakimi_algorithm import havel_hakimi_general
from graph_visualization import visualize_graph
from strategies.max_degree_strategy import MaxDegreeStrategy
from strategies.min_degree_strategy import MinDegreeStrategy
from strategies.random_strategy import RandomStrategy


def main():
    # degrees = [4, 3, 3, 3, 2, 2, 2, 1]
    k = 6
    degrees = [k]*(k+1) + [1]*(k*(k+1))
    is_graphical, edges = havel_hakimi_general(degrees, strategy=MaxDegreeStrategy())
    if is_graphical:
        print("The sequence is graphical. Edges:", edges)
        visualize_graph(edges)
    else:
        print("The sequence is not graphical.")

if __name__ == "__main__":
    main()
