from hh_strategy import HHStrategy
from bins import Bins
import random

class RandomStrategy(HHStrategy):
    def choose_pivot(self, bins: Bins):
        degree = random.choice(list(bins.bins.keys()))
        node = bins.pop_node(degree)
        return degree, node

    def choose_neighbor(self, bins: Bins, neighbor_degree: int):
        idx = random.randrange(len(bins.bins[neighbor_degree]))
        return bins.pop_node(neighbor_degree, idx)
