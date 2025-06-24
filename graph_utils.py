from typing import List, Tuple
import random
import re
from collections import defaultdict

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
    