from typing import Dict, List, Tuple
from bins import Bins
from hh_strategy import HHStrategy

class MatchingAwareStrategy(HHStrategy):
    def __init__(self):
        self.matching_nodes = set()
        self.matching_edges = list()
        self.current_top_nodes: Dict[int, int] = dict()

    def choose_neighbor(self, bins: Bins, neighbor_degree: int):
        pass

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
        # Commented out lines are for choosing the node with the minimum degree (seems to give worse results)
        # best_min_degree_node = None
        # best_min_degree_top_nodes = None
        for degree in bins.bins.keys():
            for node_id in bins.bins[degree]:
                if node_id in self.matching_nodes:
                    continue
                # Check if there is a potential neighbor not in matching among top degree nodes (excluding node_id)
                top_nodes = self._get_top_nodes_for_degree(bins, degree, node_id)
                if any(nid2 not in self.matching_nodes for nid2 in top_nodes.keys()):
                    # If there is a potential neighbor not in matching, return the node_id
                    self.current_top_nodes = top_nodes
                    bins.pop_node_by_id(node_id, degree)
                    return (degree, node_id)
                    # if best_min_degree_node is None or degree < best_min_degree_node[1]:
                    #     best_min_degree_node = (node_id, degree)
                    #     best_min_degree_top_nodes = top_nodes
        # if best_min_degree_node is None or best_min_degree_top_nodes is None:
        #     best_min_degree_node = (node_id, degree)
        #     best_min_degree_top_nodes = self._get_top_nodes_for_degree(bins, degree, node_id)
        # node_id, degree = best_min_degree_node
        # self.current_top_nodes = best_min_degree_top_nodes
        # print("No unmatched pivot found! returning", node_id, "with degree", degree)
        self.current_top_nodes = self._get_top_nodes_for_degree(bins, degree, node_id)
        bins.pop_node_by_id(node_id, degree)
        return (degree, node_id)

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
        neighbors = []
        is_pivot_unmatched = pivot_vertex not in self.matching_nodes
        
        # Prepare sorted nodes according to our priority rules
        sorted_nodes, min_unmatched_node = self._prepare_sorted_nodes()
        
        # Process nodes in sorted order and select neighbors
        self._select_neighbors(sorted_nodes, neighbors, bins, pivot_degree)
        
        # Add to matching if appropriate
        self._update_matching(min_unmatched_node, pivot_vertex, is_pivot_unmatched)
        
        assert len(neighbors) == pivot_degree, f"Not enough neighbors found for pivot {pivot_vertex} with degree {pivot_degree}."
        return neighbors
    
    def _prepare_sorted_nodes(self):
        """
        Prepares and sorts nodes based on degree and matching status.
        Returns:
            - a list of (node_id, degree, is_matched, is_min_unmatched) tuples.
            - the minimum degree unmatched node (node_is, degree, idx) if any.
        """        
        # Create list of all potential neighbors with their properties
        all_nodes = []
        min_unmatched_node = None
        i = 0
        for node_id, degree in self.current_top_nodes.items():
            is_matched = node_id in self.matching_nodes
            all_nodes.append((node_id, degree, is_matched, False))  # Initialize all as not special
            if not is_matched:
                if min_unmatched_node is None or degree < min_unmatched_node[1]:
                    min_unmatched_node = (node_id, degree, i)
            i += 1
        
        # Mark the smallest degree unmatched node as special
        min_unmatched_degree = min_unmatched_node[1] if min_unmatched_node else 0
        if min_unmatched_node:
            node_id, degree, idx = min_unmatched_node
            all_nodes[idx] = (node_id, degree, False, True)  # Mark as special unmatched node
        
        # Sort nodes according to priority rules
        all_nodes.sort(key=lambda n: (
            -n[1],  # Primary key: sort by degree (highest first)
            # Secondary key: within each degree group
            (0 if n[3] else      # Special unmatched node (smallest degree) goes first
             1 if n[2] else      # Then matched nodes
             2                   # Then remaining unmatched nodes
            ) if n[1] == min_unmatched_degree else 
            (0 if n[2] else 1)   # For non-min degree: matched before unmatched
        ))
        
        return all_nodes, min_unmatched_node
    
    def _select_neighbors(self, sorted_nodes: List[Tuple[int, int, bool, bool]], 
                          neighbors: List[int], bins: Bins, pivot_degree: int):
        """
        Selects neighbors from sorted nodes and tracks the minimum degree unmatched node.
        
        Args:
            sorted_nodes: List of (node_id, degree, is_matched, is_min_unmatched) tuples
            neighbors: List to append selected neighbor IDs to
            bins: The bins data structure
            pivot_degree: Required number of neighbors
            
        Returns:
            The minimum degree unmatched node added (degree, id), if any
        """
        for node_id, degree, _, _ in sorted_nodes:
            if len(neighbors) >= pivot_degree:
                break

            neighbors.append(node_id)
            bins.pop_node_by_id(node_id, degree)
            new_degree = degree - 1
            if new_degree > 0:
                bins.add_node(new_degree, node_id, index=0)
    
    def _update_matching(self, min_unmatched_node, pivot_vertex, is_pivot_unmatched):
        """
        Updates the matching with the pivot vertex and an unmatched node if appropriate.

        Args:
            min_unmatched_node: The minimum degree unmatched node (node_id, degree, idx)
            pivot_vertex: The id of the pivot vertex
            is_pivot_unmatched: Boolean indicating if the pivot vertex is unmatched
        """
        if min_unmatched_node and is_pivot_unmatched:
            matched_node_id = min_unmatched_node[0]
            self.matching_nodes.add(pivot_vertex)
            self.matching_nodes.add(matched_node_id)
            self.matching_edges.append((pivot_vertex, matched_node_id))

    def get_matching_edges(self):
        """
        Get the edges of the current matching.
        """
        return self.matching_edges
    
    def _get_top_nodes_for_degree(self, bins: Bins, degree: int, node_id: int) -> dict:
        """
        Get the top nodes for a given degree, excluding the specified node.

        Args:
            bins (Bins): The bins data structure containing nodes grouped by degree.
            degree (int): The degree for which to get top nodes.
            node_id (int): The node id to exclude from the top nodes.

        Returns:
            dict: Dictionary mapping node ids to their degrees.
        """
        top_nodes = dict()
        for top_degree in sorted(bins.bins.keys(), reverse=True):
            for nid2 in bins.bins[top_degree]:
                if nid2 != node_id:
                    top_nodes[nid2] = top_degree
            if len(top_nodes) >= degree:
                break
        assert len(top_nodes) >= degree, f"Not enough top nodes found for degree {degree}."
        return top_nodes

