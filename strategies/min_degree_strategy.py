from hh_strategy import HHStrategy
from bins import Bins

class MinDegreeStrategy(HHStrategy):
    def choose_pivot(self, bins: Bins):
        degree = min(bins.bins)
        node = bins.pop_node(degree, pop_pos=-1)
        return degree, node

    def choose_neighbor(self, bins: Bins, neighbor_degree: int):
        return bins.pop_node(neighbor_degree)
