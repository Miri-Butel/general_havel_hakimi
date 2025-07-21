from typing import List, Tuple
import random
import re
from collections import defaultdict
from math import floor
import numpy as np
from rustworkx import PyGraph

def generate_graph_with_perfect_matching(n, p=0.1):
    """
    Generate a random undirected graph with n vertices (even), 
    containing a perfect matching and additional edges with probability p.
    Returns a tuple: (edges, matching).
    """
    if n % 2 != 0:
        raise ValueError("n must be even for a perfect matching.")
    vertices = list(range(n))
    random.shuffle(vertices)
    matching = [(vertices[i], vertices[i+1]) for i in range(0, n, 2)]
    edge_set = set(tuple(sorted(edge)) for edge in matching)
    # Add other possible edges with probability p
    for i in range(n):
        for j in range(i+1, n):
            edge = (i, j)
            if edge not in edge_set and random.random() < p:
                edge_set.add(edge)
    edges = list(edge_set)
    return edges, matching

def degree_sequence(graph):
    """
    Given a list of edges, return the degree sequence (sorted).
    """
    degree_count = defaultdict(int)
    for u, v in graph:
        degree_count[u] += 1
        degree_count[v] += 1
    degrees = list(degree_count.values())
    return sorted(degrees, reverse=True)

def degree_sequence_repr(degrees):
    """
    Given a sorted degree sequence, returns a string like "[d] * r" for each group of repeated degrees.
    Example: [4, 4, 3, 3, 3, 2] -> "[4] *2, [3] *3, [2] *1"
    """
    if not degrees:
        return ""
    result = []
    prev = degrees[0]
    count = 1
    for d in degrees[1:]:
        if d == prev:
            count += 1
        else:
            result.append(f"[{prev}] *{count}")
            prev = d
            count = 1
    result.append(f"[{prev}] *{count}")
    return ", ".join(result)

def parse_degree_sequence(input_str):
    """
    Parse a degree sequence from a string that can be either:
    - Comma-separated list of integers (e.g., "3,3,2,2,2,1")
    - Python-style list expression (e.g., "[3]*2 + [2]*3 + [1]")
    """
    # Check if the input is in Python-style list expression format
    if '[' in input_str and '*' in input_str:
        # Create a safe evaluation of the expression
        # The pattern captures: [number], followed by * and another number, or + operator
        result = []
        pattern = r'\[(\d+)\]\s*\*\s*(\d+)'
        
        # Split by + sign
        parts = input_str.split('+')
        for part in parts:
            part = part.strip()
            match = re.match(pattern, part)
            if match:
                value = int(match.group(1))
                count = int(match.group(2))
                result.extend([value] * count)
        
        return result
    else:
        # Handle standard comma-separated format
        return [int(x) for x in input_str.split(",")]


def check_legal_matching(matching: List[Tuple[int, int]]):
    """
    Check if the given matching is legal, meaning each vertex appears only once.
    Args:
        matching (List[Tuple[int, int]]): List of edges representing the matching.
    Returns:
        bool: True if the matching is legal, False otherwise.
    """
    seen = set()
    for u, v in matching:
        if u in seen or v in seen:
            return False
        seen.add(u)
        seen.add(v)
    return True

def edges_to_rustworkx_graph(edges: List[Tuple[int, int]]) -> PyGraph:
    rw_graph = PyGraph()
    node_map = {}
    for u, v in edges:
        if u not in node_map:
            node_map[u] = rw_graph.add_node(u)
        if v not in node_map:
            node_map[v] = rw_graph.add_node(v)
        rw_graph.add_edge(node_map[u], node_map[v], None)
    return rw_graph


# ***************************************************************************
#  Implementation of Theorem 2.13 and Theorem 2.14 from the paper
# "New results on graph matching from degree preserving growth" (4/12/24) 
# ***************************************************************************

def maximal_matching_lower_bound(d):
    n = len(d)
    min_val = float('inf')

    for k in range(1, n + 1):
        dk = d[k - 1]  # d_k
        count = sum(1 for di in d if k <= di <= dk)
        value = k - 1 + 0.5 * count
        min_val = min(min_val, floor(value))

    return min_val

def td(delta: int, deg_seq: List[int]) -> Tuple[int, int]:
    assert delta < len(deg_seq), "Delta must be a valid index of the degree sequence."
    d_delta = deg_seq[delta]
    larger_indices_count, smaller_indices_count = 0, 0
    for i, d in enumerate(deg_seq):
        if d == d_delta:
            if i > delta:
                larger_indices_count += 1
            elif i < delta:
                smaller_indices_count += 1
    return larger_indices_count - smaller_indices_count, larger_indices_count

def maximum_matching_size_numpy(deg_seq: List[int]) -> int:
    """
    Efficient numpy implementation of maximum_matching_size.
    Calculate the potentially maximum matching size based on the degree sequence.
    """
    n = len(deg_seq)

    if n == 0:
        return 0
    
    deg_array = np.array(deg_seq)
    start_n = n if n % 2 == 0 else n - 1
    
    for delta in range(start_n, 1, -2):
        h_delta = delta // 2
        d_delta = deg_seq[delta - 1]
        
        # First condition check
        first_flag = True
        s1 = 0
        for k in range(1, h_delta):
            s1 += deg_seq[k - 1]
            
            # Vectorized computation of s2
            indices = np.arange(k, n)
            indicator = (indices <= (delta - 1)).astype(int)
            s2 = np.sum(np.minimum(deg_array[k:] - indicator, k))
            
            first_flag = first_flag and (s1 <= k**2 + s2)
            if not first_flag:
                break
        
        if not first_flag:
            continue
        
        # Second condition
        t_delta, s2 = td(delta-1, deg_seq)
        k = delta + t_delta
        
        # Vectorized computation of s1 and s3
        s1 = np.sum(deg_array[:k])
        if k < n:
            indicator = (deg_array[k:] == d_delta).astype(int)
            s3 = np.sum(np.minimum(deg_array[k:] - indicator, k))
        else:
            s3 = 0
        
        second_flag = (s1 + s2) <= (k**2 + s3)
        
        if second_flag:
            return h_delta
        
    return 0