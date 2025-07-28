from typing import List
from hh_strategy import HHStrategy
from bins import Bins
from pending_nodes import PendingNodes


class NaiveMatchingAwareStrategy(HHStrategy):
    def __init__(self, degrees=None):
        self.matching_nodes = set()
        self.matching_edges = list()
        self.pending = PendingNodes()

    def choose_pivot(self, bins: Bins):
        """
        Choose a pivot node from the bins that is not already in the matching, 
        preferring nodes with potential unmatched neighbors among the top degree nodes.
        If no such node is found, returns the last node considered (with smallest degree) 
        even if it is already in the matching.

        Args:
            bins (Bins): The bins data structure containing nodes grouped by degree.

        Returns:
            Tuple[int, int]: The degree and node id of the chosen pivot.
        """
        # Finds a pivot node that is not in the matching and has at least one unmatched neighbor
        for degree, node_id in bins:
            if node_id not in self.matching_nodes:
                top_neighbors = self.get_top_neighbors(bins, node_id, degree)
                if any(not neighbor[-1] for neighbor in top_neighbors):
                    # If there is at least one unmatched neighbor, we can use this node as a pivot
                    # Remove the node from bins and return it
                    bins.pop_node_by_id(node_id, degree)
                    return degree, node_id
        # Finds a pivot node that is in the matching, and has at least "degree" unmatched neighbors
        for degree, node_id in bins:
            if node_id in self.matching_nodes:
                top_neighbors = self.get_top_neighbors(bins, node_id, degree)
                min_neighbor_degree = min(neighbor[1] for neighbor in top_neighbors)
                high_deg_neighbor = [neighbor for neighbor in top_neighbors if neighbor[1] > min_neighbor_degree]
                min_deg_matched_neighbors = [neighbor for neighbor in top_neighbors if neighbor[1] == min_neighbor_degree and neighbor[-1]]
                necessary_min_deg_count = degree - len(high_deg_neighbor)
                if len(min_deg_matched_neighbors) >= necessary_min_deg_count and all(neighbor[-1] for neighbor in high_deg_neighbor):
                    # If there are enough matched neighbors, we can use this node as a pivot
                    # Remove the node from bins and return it
                    bins.pop_node_by_id(node_id, degree)
                    return degree, node_id
        bins.pop_node_by_id(node_id, degree)
        return degree, node_id

    def choose_neighbor(self, bins: Bins, neighbor_degree: int):
        pass

    def choose_and_add_neighbors(self, bins: Bins, pivot_degree: int, pivot_vertex: int):
        """
        Selects neighbors for the given pivot vertex by sorting nodes based on:
        1. Degree (highest to lowest)
        2. For minimum degree nodes: one unmatched first, then matched nodes, then remaining unmatched
        3. For other degrees: matched nodes before unmatched

        Args:
            bins (Bins): The bins data structure containing nodes grouped by degree.
            pivot_degree (int): The degree of the pivot vertex.
            pivot_vertex (int): The id of the pivot vertex.

        Returns:
            List[int]: List of neighbor node ids.
        """
        self.pending.clear()
        neighbors = []
        top_neighbors = self.get_top_neighbors(bins, pivot_vertex, pivot_degree)
        neighbor_to_match, neighbor_degree_to_match = self.get_neighbor_and_degree_to_match(top_neighbors)
        
        if neighbor_to_match is not None and pivot_vertex not in self.matching_nodes:
            # Add the selected neighbor to the matching nodes, and add the edge to the matching edges
            bins.pop_node_by_id(neighbor_to_match, neighbor_degree_to_match)
            self.matching_nodes.add(neighbor_to_match)
            self.matching_nodes.add(pivot_vertex)
            self.matching_edges.append((pivot_vertex, neighbor_to_match))
            assert type(neighbor_degree_to_match) is int, "neighbor_degree_to_match should be an integer"
            self.add_node_to_neighbors(neighbors, neighbor_to_match, neighbor_degree_to_match)

        min_neighbor_degree = min(neighbor[1] for neighbor in top_neighbors)
        # Add all top_neighbors with degree > min_neighbor_degree
        for node_id, degree, _ in top_neighbors:
            if degree > min_neighbor_degree and node_id != neighbor_to_match:
                bins.pop_node_by_id(node_id, degree)
                self.add_node_to_neighbors(neighbors, node_id, degree)
        
        # Now we need to add nodes with min_neighbor_degree, first matched nodes, then unmatched nodes
        top_neighbors_min_degree = [node for node in top_neighbors if node[1] == min_neighbor_degree]
        # sort top_neighbors_min_degree by matching status
        top_neighbors_min_degree.sort(key=lambda x: x[-1], reverse=True)
        for node_id, degree, _ in top_neighbors_min_degree:
            if len(neighbors) >= pivot_degree:
                break
            if node_id != neighbor_to_match:
                bins.pop_node_by_id(node_id, degree)
                self.add_node_to_neighbors(neighbors, node_id, degree)

        self.pending.insert_into_bins(bins)
        return neighbors

    
    def get_top_neighbors(self, bins: Bins, pivot_vertex: int, pivot_degree: int):
        """
        Get the top neighbors for a given pivot vertex and degree.
        
        Args:
            bins (Bins): The bins data structure containing nodes grouped by degree.
            pivot_vertex (int): The id of the pivot vertex.
            pivot_degree (int): The degree of the pivot vertex.
        
        Returns:
            List[Tuple[int, int, bool]]: List of tuples containing neighbor node ids, their degrees, and matching status.
        """
        neighbors = []
        for degree in bins.iter_degrees_descending():
            if len(neighbors) >= pivot_degree:
                break
            
            # add all nodes with the current degree, excluding the pivot vertex
            for node_id in bins.bins[degree]:
                if node_id != pivot_vertex:
                    neighbors.append((node_id, degree, node_id in self.matching_nodes))
        
        return neighbors
    
    def get_neighbor_and_degree_to_match(self, neighbors):
        """
        Get the node with the minimum degree that is unmatched from the list of neighbors.
        
        Args:
            neighbors (List[Tuple[int, int, bool]]): List of tuples containing neighbor node ids, their degrees, and matching status.
        
        Returns:
            Tuple[int, int]: The id and degree of the selected neighbor to match, or (None, flot('inf')) if no unmatched neighbor is found.
        """
        selected_node = None
        selected_node_degree = float('inf')
        for node_id, degree, is_matched in neighbors:
            if not is_matched and degree < selected_node_degree:
                selected_node = node_id
                selected_node_degree = degree
                
        return selected_node, selected_node_degree
    
    def add_node_to_neighbors(self, neighbors: List[int], node_id: int, degree: int):
        """
        Add a node to the neighbors list and update the bins.
        
        Args:
            neighbors (List[int]): The list of neighbor node ids to add to.
            node_id (int): The id of the node to add.
            degree (int): The degree of the node.
        """
        neighbors.append(node_id)
        new_degree = degree - 1
        if new_degree > 0:
            self.pending.add(new_degree, node_id)

    def get_matching_edges(self):
        """
        Get the edges of the current matching.
        """
        return self.matching_edges
