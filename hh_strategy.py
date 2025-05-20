from abc import ABC, abstractmethod

from bins import Bins
from pending_nodes import PendingNodes

class HHStrategy(ABC):
    def __init__(self):
        self.pending = PendingNodes()

    @abstractmethod
    def choose_pivot(self, bins):
        """Return (pivot_degree, pivot_node)"""
        pass

    @abstractmethod
    def choose_neighbor(self, bins, neighbor_degree):
        """Return neighbor_node given degree"""
        pass

    def choose_and_add_neighbors(self, bins, pivot_degree, pivot_node):
        """Return a list of neighbors to add"""
        neighbors = []
        self.pending.clear()
        for _ in range(pivot_degree):
            if bins.size == 0:
                break
            neighbor_degree = bins.get_max_degree()
            neighbor_node = self.choose_neighbor(bins, neighbor_degree)
            neighbors.append(neighbor_node)
            new_degree = neighbor_degree - 1
            if new_degree > 0:
                self.pending.add(new_degree, neighbor_node)
        
        self.pending.insert_into_bins(bins)
        return neighbors
