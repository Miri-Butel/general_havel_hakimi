from typing import List, Tuple
from bins import Bins
from hh_strategy import HHStrategy
from strategies.max_degree_strategy import MaxDegreeStrategy

def havel_hakimi_general(degrees: List[int], strategy: HHStrategy) -> Tuple[bool, List[Tuple[int, int]]]:
    """
    Generalized Havel-Hakimi algorithm to check if a degree sequence is graphical.
    
    Args:
        degrees (list[int]): The degree sequence.
        strategy (HHStrategy): Strategy object for pivot/neighbor selection.
    
    Returns:
        bool, list[tuple]: True if the sequence is graphical, False otherwise. If True, also returns the edges.
    """
    if strategy is None:
        strategy = MaxDegreeStrategy()
    
    bins = Bins()
    for vertex_id, degree in enumerate(degrees):
        if degree > 0:
            bins.add_node(degree, vertex_id)
    
    edges = []

    while bins.size > 0:
        pivot_degree, pivot_vertex = strategy.choose_pivot(bins)
        
        if pivot_degree > bins.size:
            return False, []
        
        neighbors = strategy.choose_and_add_neighbors(bins, pivot_degree, pivot_vertex)
        
        for neighbor in neighbors:
            edges.append((pivot_vertex, neighbor))
    
    return True, edges