import os
import numpy as np
from datetime import datetime
import random

from rustworkx import max_weight_matching, undirected_gnp_random_graph, barabasi_albert_graph

from utils import ensure_dir
from graph_utils import check_legal_matching, degree_sequence, degree_sequence_repr, maximum_matching_size_numpy
from havel_hakimi_algorithm import havel_hakimi_general
from strategies.matching_aware_strategy import MatchingAwareStrategy
from strategies.naive_matching_aware_strategy import NaiveMatchingAwareStrategy


def run_rounds_for_np_general(StrategyClass, n, p, rounds, degseq_log, seed=None):
    degseq_log.write("n,p,round,degree_sequence,matching_size\n")
    for round_idx in range(1, rounds + 1):
        seed_i = seed + round_idx if seed is not None else None
        # The barabasi_albert_graph function has a bug affecting reproducibility, see https://github.com/Qiskit/rustworkx/issues/1480
        # original_graph = barabasi_albert_graph(n, p, seed=seed_i)
        original_graph = undirected_gnp_random_graph(n, p, seed=seed_i)
        original_edges = original_graph.edge_list()
        matching = max_weight_matching(original_graph, max_cardinality=True)
        degrees = degree_sequence(original_edges)
        deg_seq_str = degree_sequence_repr(degrees)
        strategy = StrategyClass(degrees=degrees)

        _, __ = havel_hakimi_general(degrees, strategy=strategy)
        hh_matching = strategy.get_matching_edges()
        msize = len(hh_matching) if hh_matching else 0
        if use_naive_strategy:
            assert check_legal_matching(hh_matching), "Naive strategy produced an illegal matching!"

        max_deg_seq_matching_size = maximum_matching_size_numpy(degrees)

        if len(deg_seq_str) == 0:
            degseq_log.write(f"{n},{p:.4f},{round_idx},'no deg sequence'\n")
        else:
            degseq_log.write(f"{n},{p:.4f},{round_idx},{deg_seq_str}\n")
            degseq_log.write(f"Original max matching size: {len(matching)}\n")
            degseq_log.write(f"HH matching size:           {msize}\n")
            degseq_log.write(f"MAX matching size:          {max_deg_seq_matching_size}    ---> success: {msize >= len(matching)},{max_deg_seq_matching_size - msize} \n")

def run_experiment(
    # n_range=range(4, 251, 6),
    # p_range=np.linspace(0.01, 0.26, 5),
    # rounds=75,
    # save_every=15,
    # n_range=range(4, 101, 2),
    n_range=range(102, 301, 6),
    p_range=np.linspace(0.002, 0.02, 5),
    # p_range=np.linspace(0.3, 0.5, 4),
    rounds=50,
    base_dir="experiment_results/matching_aware_general",
    degseq_log_filename="degseq_matching_log.txt",
    use_naive_strategy=False,
    seed=None
):
    # Uncomment for Barabasi-Albert graphs (p_range is the range of m in this case)
    # p_range = range(2, 11)
    if seed is not None:
        degseq_log_filename = f"degseq_matching_log_naive_s{seed}.txt" if use_naive_strategy else f"degseq_matching_log_s{seed}.txt"
        # Uncomment for Barabasi-Albert graphs
        # degseq_log_filename = f"b_degseq_matching_log_naive_s{seed}.txt" if use_naive_strategy else f"b_degseq_matching_log_s{seed}.txt"
    StrategyClass = NaiveMatchingAwareStrategy if use_naive_strategy else MatchingAwareStrategy
    ensure_dir(base_dir)
    degseq_log_filename = os.path.join(base_dir, degseq_log_filename)
    with open(degseq_log_filename, "w") as degseq_log:
        degseq_log.write("Experiment started at {}\n\n".format(datetime.now()))
        for n in n_range:
            for p in p_range:
                if p >= n: # for Barabasi-Albert graph (m < n)
                    continue
                run_rounds_for_np_general(StrategyClass, n, p, rounds, degseq_log, seed=seed)
        degseq_log.write("\nExperiment ended at {}".format(datetime.now()))


if __name__ == "__main__":
    # Generate n random seeds
    n = 5
    SEEDS = [random.randint(0, 10000) for _ in range(n)]
    # SEEDS = [2045, 1342, 7021, 6293, 9540]  # np.linspace(0.01, 0.26, 5)
    # SEEDS = [8423, 4576, 3081, 8468, 794]  # np.linspace(0.002, 0.02, 5)
    # SEEDS = [7298, 1237, 4039, 1549, 1637]  # np.linspace(0.3, 0.5, 4)
    # SEEDS = [4408, 1317, 586, 6992, 8536]  # for Barabasi-Albert graphs m=range(2, 11)
    
    # SEEDS = [4336, 525, 6891, 3070, 39]  # n_range=range(102, 301, 6), p_range=np.linspace(0.002, 0.02, 5)
    # SEEDS = [4231, 9729, 7418, 4317, 4094]  # n_range=range(102, 301, 6), np.linspace(0.002, 0.02, 5)

    use_naive_strategy = False  # Set to True to use NaiveMatchingAwareStrategy

    for seed in SEEDS:
        print(f"Running experiment with seed: {seed}")
        random.seed(seed)
        np.random.seed(seed)
        run_experiment(use_naive_strategy=use_naive_strategy, seed=seed)
