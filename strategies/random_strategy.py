import random
from bins import Bins
from hh_strategy import HHStrategy
from pending_nodes import PendingNodes

class RandomStrategy(HHStrategy):
    def __init__(self, degrees=None):
        self.pending = PendingNodes()

    def choose_pivot(self, bins: Bins):
        degree = random.choice(list(bins.bins.keys()))
        node = bins.pop_node(degree)
        return degree, node

    def choose_neighbor(self, bins: Bins, neighbor_degree: int):
        idx = random.randrange(len(bins.bins[neighbor_degree]))
        return bins.pop_node(neighbor_degree, idx)
