from typing import List, Tuple
from bins import Bins
from hh_strategy import HHStrategy

class MatchingAwareStrategy(HHStrategy):
    def __init__(self):
        self.matching_nodes = set()
        self.matching_edges = list()
        self.current_top_nodes = dict()

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
        print("No unmatched pivot found! returning", node_id, "with degree", degree)
        self.current_top_nodes = self._get_top_nodes_for_degree(bins, degree, node_id)
        bins.pop_node_by_id(node_id, degree)
        return (degree, node_id)

    def choose_and_add_neighbors(self, bins: Bins, pivot_degree: int, pivot_vertex: int):
        """
        Selects neighbors for the given pivot vertex by:
        1. Adding the first unmatched neighbor (if any), and if so adding also the
           pivot vertex to the matching,
        2. Then adding all matched neighbors,
        3. Then adding the rest of unmatched neighbors,
        until the required number of neighbors is reached.

        Args:
            bins (Bins): The bins data structure containing nodes grouped by degree.
            pivot_degree (int): The degree of the pivot vertex.
            pivot_vertex (int): The id of the pivot vertex.

        Returns:
            List[int]: List of neighbor node ids.
        """
        neighbors = []
        top_matched_nodes = [(d, id) for id, d in self.current_top_nodes.items() if id in self.matching_nodes]
        top_unmatched_nodes = [(d, id) for id, d in self.current_top_nodes.items() if id not in self.matching_nodes]
        top_matched_nodes.sort()
        # top_unmatched_nodes.sort(reverse=True)

        # Add first unmatched node if possible
        add_first_matched = pivot_vertex not in self.matching_nodes
        if len(top_unmatched_nodes) > 0:
            first_unmatched_list = top_unmatched_nodes[:1]
            matched_nid = self._add_neighbors_from_list(first_unmatched_list, neighbors, bins, pivot_degree, add_first_matched=add_first_matched)
            if matched_nid >= 0:
                self.matching_nodes.add(pivot_vertex)
                self.matching_edges.append((pivot_vertex, matched_nid))
        
        if len(neighbors) < pivot_degree:
            # Add matched nodes
            self._add_neighbors_from_list(top_matched_nodes, neighbors, bins, pivot_degree)

        if len(neighbors) < pivot_degree:
            # Add unmatched nodes
            self._add_neighbors_from_list(top_unmatched_nodes[1:], neighbors, bins, pivot_degree)

        assert len(neighbors) == pivot_degree, f"Not enough neighbors found for pivot {pivot_vertex} with degree {pivot_degree}."
        return neighbors
    
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

    def _add_neighbors_from_list(self, potential_neighbors: List[Tuple[int, int]],
                                    neighbors: List[int], bins: Bins, pivot_degree: int,
                                    add_first_matched: bool = False):
        """
        Add neighbors from a list of potential neighbors to the neighbors list, 
        updating bins and matching as needed.

        Args:
            potential_neighbors (List[Tuple[int, int]]): List of (degree, node id) tuples.
            neighbors (List[int]): List to append chosen neighbors to.
            bins (Bins): The bins data structure.
            pivot_degree (int): The degree of the pivot vertex.
            add_first_matched (bool, optional): Whether to add the first unmatched neighbor to the matching. Defaults to False.

        Returns:
            int: The id of the matched neighbor if one was added, otherwise -1.
        """
        matched_neighbor_id = -1
        for d, id in potential_neighbors:
            if len(neighbors) >= pivot_degree:
                break
            else:
                if add_first_matched and matched_neighbor_id < 0:
                    if id not in self.matching_nodes:
                        matched_neighbor_id = id
                        self.matching_nodes.add(id)
                neighbors.append(id)
                bins.pop_node_by_id(id, d)
                new_degree = d - 1
                if new_degree > 0:
                    bins.add_node(new_degree, id, index=0)

        return matched_neighbor_id
