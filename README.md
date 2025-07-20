# General Havel-Hakimi Graph Generator and Visualizer

This project provides a Python tool for generating, analyzing, and visualizing graphs based on the Havel-Hakimi algorithm and various construction strategies. It supports random graph generation, perfect matchings, and several strategies for realizing degree sequences.

## Features
- Generate graphs from user-specified or random degree sequences
- Visualize both the original and constructed graphs
- Multiple construction strategies (max degree, min degree, random, matching-aware, naive matching-aware)
- Highlight perfect matchings in visualizations
- Command-line interface for flexible usage

## Requirements
- Python 3.8+
- [rustworkx](https://github.com/Qiskit/rustworkx)
- matplotlib

Install dependencies with:
```bash
pip install -r requirements.txt
```

## Usage
Run the main script with various options:

```bash
python main.py [--n N] [--degrees DEGSEQ] [--strategy STRATEGY] [--p PROB]
```

- `--n N`: Number of vertices (for random graph with perfect matching)
- `--degrees DEGSEQ`: Degree sequence as comma-separated list (e.g. `3,3,2,2,2,1`) or Python-style (e.g. `[3]*2 + [2]*3 + [1]`)
- `--strategy STRATEGY`: Construction strategy (`max`, `min`, `random`, `matching`, `naive_matching`). (default: `matching`)
- `--p PROB`: Edge probability for random graph (default: 0.1)

If neither `--n` nor `--degrees` is provided, you will be prompted to enter a degree sequence or use the default.

## Example
Generate and visualize a graph with a specific degree sequence using the matching-aware strategy:

```bash
python main.py --degrees 3,3,2,2,2,2 --strategy matching
```
```bash
python main.py --degrees "[3]*2 + [2]*6" --strategy max
```

<!-- ## Project Structure
- `main.py`: Entry point and CLI
- `havel_hakimi_algorithm.py`: Havel-Hakimi algorithm implementation
- `graph_utils.py`: Utilities for degree sequences and graph operations
- `graph_visualization.py`: Visualization functions
- `strategies/`: Different construction strategies
- `requirements.txt`: Python dependencies
- `test_degree_sequences.py`: Unit tests

## License
MIT License -->
