from bins import Bins
from pending_nodes import PendingNodes
from strategies.max_degree_strategy import MaxDegreeStrategy

def havel_hakimi_general(degrees, strategy=None):
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
    pending = PendingNodes()

    while bins.size > 0:
        pivot_degree, pivot_vertex = strategy.choose_pivot(bins)
        
        if pivot_degree > bins.size:
            return False, []
        
        pending.clear()
        
        for _ in range(pivot_degree):
            if bins.size == 0:
                return False, []
            
            neighbor_degree = bins.get_max_degree()
            neighbor_vertex = strategy.choose_neighbor(bins, neighbor_degree)
            
            edges.append((pivot_vertex, neighbor_vertex))
            
            new_degree = neighbor_degree - 1
            if new_degree > 0:
                pending.add(new_degree, neighbor_vertex)
        
        pending.insert_into_bins(bins)
    
    return True, edges