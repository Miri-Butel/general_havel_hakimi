from abc import ABC, abstractmethod

class HHStrategy(ABC):
    @abstractmethod
    def choose_pivot(self, bins):
        """Return (pivot_degree, pivot_node)"""
        pass

    @abstractmethod
    def choose_neighbor(self, bins, neighbor_degree):
        """Return neighbor_node given degree"""
        pass
