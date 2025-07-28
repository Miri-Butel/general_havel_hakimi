from hh_strategy import HHStrategy
from bins import Bins
from pending_nodes import PendingNodes


class MaxDegreeStrategy(HHStrategy):
    def __init__(self, degrees=None):
        self.pending = PendingNodes()

    def choose_pivot(self, bins: Bins):
        degree = bins.get_max_degree()
        node = bins.pop_node(degree)
        return degree, node

    def choose_neighbor(self, bins: Bins, neighbor_degree: int):
        return bins.pop_node(neighbor_degree)
