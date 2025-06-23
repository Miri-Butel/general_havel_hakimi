from collections import defaultdict
from bins import Bins

class PendingNodes:
    def __init__(self):
        self.pending = defaultdict(list)

    def add(self, degree, node):
        self.pending[degree].append(node)

    def clear(self):
        self.pending.clear()

    def items(self):
        return self.pending.items()

    def insert_into_bins(self, bins: Bins):
        """
        Insert all pending nodes back into bins, preserving the order they were popped.
        Each node is inserted at the beginning of its bin, so the first popped ends up first.
        *Important Note*: This does not necessarily preserve the original order of nodes within each degree bin!
        (e.g. when choosing the neighbors from random locations in the bin)
        """
        for degree, nodes in self.pending.items():
            for node in reversed(nodes):
                bins.add_node(degree, node, index=0)
