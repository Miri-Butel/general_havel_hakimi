import os
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime
import random

from graph_utils import check_legal_matching, degree_sequence, degree_sequence_repr, generate_graph_with_perfect_matching
from havel_hakimi_algorithm import havel_hakimi_general
from graph_visualization import visualize_graph
from strategies.matching_aware_strategy import MatchingAwareStrategy
from strategies.naive_matching_aware_strategy import NaiveMatchingAwareStrategy

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def save_figure(original_edges, matching, hh_edges, hh_matching, n, p, round_idx, save_dir, deg_seq_str):
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle(f"n={n}, p={p:.2f}, round={round_idx}, deg_seq=({deg_seq_str})", fontsize=14)
    visualize_graph(original_edges, highlight_edges=matching, ax=axes[0],
                    title=f"Original Graph\nPerfect Matching size: {len(matching) if matching else 0}")
    visualize_graph(hh_edges, highlight_edges=hh_matching, ax=axes[1],
                    title=f"HH Algorithm\nMatching size: {len(hh_matching) if hh_matching else 0}")
    fig.tight_layout()
    fig.savefig(os.path.join(save_dir, f"graph_n{n}_p{p:.2f}_round{round_idx}.png"))
    plt.close(fig)

def run_rounds_for_np_perfect_matching(StrategyClass, n, p, rounds, save_every,
                                       save_dir, degseq_log_filename, edges_log_file):
    matching_sizes = []
    matching_size_counter = Counter()
    degseq_log_path = os.path.join(save_dir, degseq_log_filename)
    # with open(degseq_log_path, "w") as degseq_log:
        # degseq_log.write("n,p,round,degree_sequence,matching_size\n")
    for round_idx in range(1, rounds + 1):
        strategy = StrategyClass()
        original_edges, matching = generate_graph_with_perfect_matching(n, p)
        degrees = degree_sequence(original_edges)
        deg_seq_str = degree_sequence_repr(degrees)
        is_graphical, hh_edges = havel_hakimi_general(degrees, strategy=strategy)
        hh_matching = strategy.get_matching_edges()
        msize = len(hh_matching) if hh_matching else 0
        matching_sizes.append(msize)
        matching_size_counter[msize] += 1
        if use_naive_strategy:
            assert check_legal_matching(hh_matching), "Naive strategy produced an illegal matching!"

        edges_log_file.write(f"Round {round_idx}: n={n}, p={p:.4f}, degree_sequence={deg_seq_str}\n")
        edges_log_file.write(f"HH edges: {sorted(original_edges)}\n")
        edges_log_file.write(f"HH matching: {sorted(hh_matching)}\n")

        # degseq_log.write(f"{n},{p:.4f},{round_idx},\"{deg_seq_str}\",{msize}\n")

        # if round_idx % save_every == 0:
        #     save_figure(
        #         original_edges, matching,
        #         hh_edges if is_graphical else original_edges,
        #         hh_matching,
        #         n, p, round_idx, save_dir, deg_seq_str
        #     )
    return matching_sizes, matching_size_counter

def save_statistics(n, p, rounds, matching_sizes, matching_size_counter, save_dir, log_file):
    avg = np.mean(matching_sizes)
    median = np.median(matching_sizes)
    min_val = np.min(matching_sizes)
    max_val = np.max(matching_sizes)
    std_val = np.std(matching_sizes)
    # Sort distribution by matching size (key) descending
    sorted_dist = ', '.join(f'{k}: {v}' for k, v in sorted(matching_size_counter.items(), reverse=True))
    stats_str = (
        f"n={n}, p={p:.2f} | rounds={rounds}\n"
        f"  avg matching size: {avg:.2f}\n"
        f"  median: {median}\n"
        f"  min: {min_val}\n"
        f"  max: {max_val}\n"
        f"  std: {std_val:.2f}\n"
        f"  distribution: {{{sorted_dist}}}\n"
    )
    # print(stats_str)
    log_file.write(stats_str + "\n")

    # dist_path = os.path.join(save_dir, "matching_size_distribution.csv")
    # with open(dist_path, "w") as f:
    #     f.write("matching_size,count\n")
    #     for size, count in sorted(matching_size_counter.items(), reverse=True):
    #         f.write(f"{size},{count}\n")

def run_experiment(
    # n_range=range(4, 251, 6),
    p_range=np.linspace(0.01, 0.26, 5),
    # rounds=75,
    # save_every=15,
    n_range=range(4, 101, 2),
    # p_range=np.linspace(0.02, 0.2, 5),
    # p_range=np.linspace(0.03, 0.5, 4),
    rounds=50,
    save_every=10,
    base_dir="experiment_results",
    log_filename="experiment_log.txt",
    edges_log_filename="edges_log.txt",
    degseq_log_filename="degseq_matching_log.txt",
    use_naive_strategy=False,
    seed=None
):
    StrategyClass = NaiveMatchingAwareStrategy if use_naive_strategy else MatchingAwareStrategy
    if seed is not None:
        log_filename = f"experiment_log_s{seed}.txt"
        edges_log_filename = f"edges_log_s{seed}.txt"
    if use_naive_strategy:
        log_filename = f"experiment_log_naive_s{seed}.txt" if seed else "experiment_log_naive.txt"
        edges_log_filename = f"edges_log_naive_s{seed}.txt" if seed else "edges_log_naive.txt"

    log_path = os.path.join(base_dir, log_filename)
    ensure_dir(base_dir)
    with open(log_path, "w") as log_file:
        log_file.write(f"Experiment started at {datetime.now()}\n\n")
        log_file.write(f"n_range: {list(n_range)}\np_range: {list(p_range)}\nrounds: {rounds}\nsave_every: {save_every}\n\n")

        with open(os.path.join(base_dir, edges_log_filename), "w") as edges_log:
            for n in n_range:
                for p in p_range:
                    save_dir = os.path.join(base_dir, f"n_{n}", f"p_{p:.2f}")
                    # ensre_dir(save_dir)
                    matching_sizes, matching_size_counter = run_rounds_for_np_perfect_matching(
                        StrategyClass, n, p, rounds, save_every, save_dir, 
                        degseq_log_filename, edges_log)
                    save_statistics(n, p, rounds, matching_sizes, matching_size_counter, save_dir, log_file)


if __name__ == "__main__":
    # Generate 20 random seeds
    SEEDS = [random.randint(0, 10000) for _ in range(10)]
    use_naive_strategy = True  # Set to True to use NaiveMatchingAwareStrategy

    for seed in SEEDS:
        print(f"Running experiment with seed: {seed}")
        random.seed(seed)
        np.random.seed(seed)
        run_experiment(use_naive_strategy=use_naive_strategy, seed=seed)
