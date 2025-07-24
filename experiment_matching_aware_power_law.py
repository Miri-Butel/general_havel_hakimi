import os
import numpy as np
from datetime import datetime
import random
from havel_hakimi_algorithm import havel_hakimi_general
from strategies.matching_aware_strategy import MatchingAwareStrategy
from strategies.naive_matching_aware_strategy import NaiveMatchingAwareStrategy
from graph_utils import check_legal_matching, degree_sequence_repr, maximum_matching_size_numpy, generate_power_law_degree_sequence

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def run_rounds_for_np_general(StrategyClass, n, p, rounds, degseq_log, seed=None) -> int:
    graphical_sequences_count = 0
    degseq_log.write("n,p,round,degree_sequence,matching_size\n")
    for round_idx in range(1, rounds + 1):
        strategy = StrategyClass()
        seed_i = seed + round_idx if seed is not None else None
        degrees = generate_power_law_degree_sequence(n, p, seed_i)
        deg_seq_str = degree_sequence_repr(degrees)

        is_graphical, __ = havel_hakimi_general(degrees, strategy=strategy)
        if not is_graphical:
            # degseq_log.write(f"{n},{p:.4f},{round_idx},'not graphical'\n")
            # print(f"Round {round_idx}, n={n}, Degree sequenceis not graphical, skipping...")
            continue
        graphical_sequences_count += 1
        hh_matching = strategy.get_matching_edges()
        msize = len(hh_matching) if hh_matching else 0
        if use_naive_strategy:
            assert check_legal_matching(hh_matching), "Naive strategy produced an illegal matching!"

        max_deg_seq_matching_size = maximum_matching_size_numpy(degrees)

        if len(deg_seq_str) == 0:
            degseq_log.write(f"{n},{p:.4f},{round_idx},'no deg sequence'\n")
        else:
            degseq_log.write(f"{n},{p:.4f},{round_idx},{deg_seq_str}\n")
            degseq_log.write(f"HH matching size:           {msize}\n")
            degseq_log.write(f"MAX-deg matching size:      {max_deg_seq_matching_size}, {msize == max_deg_seq_matching_size}\n") #    ---> success: {msize >= len(matching)},{max_deg_seq_matching_size - msize} \n")
    return graphical_sequences_count

def run_experiment(
    # n_range=range(4, 101, 2),
    n_range=range(102, 301, 6),
    a_range=[1.8, 1.9, 2, 2.1, 2.3],
    rounds=50,
    base_dir="experiment_results/power_law_degree_sequences",
    degseq_log_filename="pl_degseq_matching_log.txt",
    use_naive_strategy=False,
    seed=None
    ):
    if seed is not None:
        degseq_log_filename = f"pl_degseq_matching_log_naive_s{seed}.txt" if use_naive_strategy else f"pl_degseq_matching_log_s{seed}.txt"
    StrategyClass = NaiveMatchingAwareStrategy if use_naive_strategy else MatchingAwareStrategy
    ensure_dir(base_dir)
    degseq_log_filename = os.path.join(base_dir, degseq_log_filename)
    graphical_sequences_count = 0
    with open(degseq_log_filename, "w") as degseq_log:
        degseq_log.write("Experiment started at {}\n\n".format(datetime.now()))
        for n in n_range:
            for a in a_range:
                graphical_sequences_count += run_rounds_for_np_general(StrategyClass, n, a, rounds, degseq_log, seed=seed)
        total_rounds = len(n_range) * len(a_range) * rounds
        print(f"Total graphical sequences found: {graphical_sequences_count} out of {total_rounds} rounds. ({graphical_sequences_count / total_rounds:.2%})")
        degseq_log.write("\nExperiment ended at {}".format(datetime.now()))


if __name__ == "__main__":
    # Generate n random seeds
    n = 5
    SEEDS = [random.randint(0, 10000) for _ in range(n)]
    # SEEDS = [4983, 228, 1064, 532, 658]  # n_range=range(4, 101, 2), a_range=[1.8, 1.9, 2, 2.1, 2.3]
    # SEEDS = [1407, 7356, 8529, 4830, 2161]  # n_range=range(102, 301, 6), a_range=[1.8, 1.9, 2, 2.1, 2.3]

    use_naive_strategy = False  # Set to True to use NaiveMatchingAwareStrategy

    for seed in SEEDS:
        print(f"Running experiment with seed: {seed}")
        random.seed(seed)
        np.random.seed(seed)
        run_experiment(use_naive_strategy=use_naive_strategy, seed=seed)
