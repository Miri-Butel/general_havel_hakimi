from collections import defaultdict

class Bins:
    def __init__(self, pop_pos=0):
        """
        Initialize the bins data structure.
        """
        self.bins = defaultdict(list)
        self.size = 0  # Total number of nodes across all bins
        self.pop_pos = pop_pos

    def add_node(self, degree, node_id, index=None):
        """
        Add a node to the bin corresponding to its degree.

        Args:
            degree (int): The degree of the node.
            node_id (int): The ID of the node.
        """
        if index is None:
            index = len(self.bins[degree])
        self.bins[degree].insert(index, node_id)
        self.size += 1

    def pop_node(self, degree, pop_pos=None):
        """
        Pop a node from the bin corresponding to the given degree, and in a specific position.

        Args:
            degree (int): The degree of the bin to pop from.
            pop_pos (int, optional): The position to pop from. Defaults to default of the class.

        Returns:
            int: The ID of the popped node.
        """
        if pop_pos is None:
            pop_pos = self.pop_pos
        node_id = self.bins[degree].pop(pop_pos)
        if not self.bins[degree]:
            del self.bins[degree]
        self.size -= 1
        return node_id
    
    def pop_node_by_id(self, node_id, degree):
        """
        Pop a node by its ID from the bin corresponding to its degree.

        Args:
            node_id (int): The ID of the node.
            degree (int): The degree of the bin to pop from.

        Returns:
            int: The ID of the popped node.
        """
        self.bins[degree].remove(node_id)
        if not self.bins[degree]:
            del self.bins[degree]
        self.size -= 1
        return node_id

    def get_max_degree(self):
        """
        Get the maximum degree present in the bins.
        """
        return max(self.bins)

    def __iter__(self):
        """
        Create an iterator to iterate over nodes in the bins without mutating.

        Yields:
            tuple: A tuple (degree, node_id) for each node in the bins.
        """
        for degree in sorted(self.bins.keys(), reverse=True):
            for node_id in self.bins[degree]:
                yield degree, node_id

    def iter_degrees_descending(self):
        """
        Returns an iterator that yields degrees in descending order.
        
        Returns:
            iterator: An iterator over degrees in descending order
        """
        return iter(sorted(self.bins.keys(), reverse=True))


    def __str__(self) -> str:
        return f"Bins(size={self.size}, bins={dict(sorted(self.bins.items(), reverse=True))})"