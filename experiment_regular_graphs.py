import os
from datetime import datetime
from havel_hakimi_algorithm import havel_hakimi_general
from strategies.matching_aware_strategy import MatchingAwareStrategy
from strategies.naive_matching_aware_strategy import NaiveMatchingAwareStrategy
from utils import ensure_dir


def run_regular_graph_experiment(
    d_range=range(1, 70),
    n_max=500,
    log_filename="regular_graph_experiment_log.txt",
    base_dir="regular_graph_experiment_results",
    use_naive_strategy=False
):
    StrategyClass = NaiveMatchingAwareStrategy if use_naive_strategy else MatchingAwareStrategy
    if use_naive_strategy:
        log_filename = "regular_graph_experiment_log_naive.txt"

    ensure_dir(base_dir)
    log_path = os.path.join(base_dir, log_filename)
    with open(log_path, "w") as log_file:
        log_file.write(f"Regular Graph Experiment started at {datetime.now()}\n\n")
        log_file.write("d,n,matching_size,is_perfect_matching\n")

        for d in d_range:
            for n in range(d + 1, n_max + 1):  # we must have n >= d+1
                if (d * n) % 2 != 0:  # make sure that the sum of degrees is even
                    continue
                degrees = [d] * n
                strategy = StrategyClass(degrees=degrees)
                is_graphical, hh_edges = havel_hakimi_general(degrees, strategy=strategy)
                if not is_graphical:
                    print(f"Skipping d={d}, n={n} as it is not graphical.")
                    continue
                hh_matching = strategy.get_matching_edges()
                matching_size = len(hh_matching) if hh_matching else 0
                is_perfect_matching = (matching_size == n // 2)

                log_file.write(f"{d},{n},{matching_size},{is_perfect_matching}\n")

        log_file.write(f"\nRegular Graph Experiment ended at {datetime.now()}")


if __name__ == "__main__":
    # SEED = 42
    # import random
    # random.seed(SEED)

    use_naive_strategy = False  # Set to True to use NaiveMatchingAwareStrategy
    run_regular_graph_experiment(use_naive_strategy=use_naive_strategy)
